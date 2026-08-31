---
module_id: DBE-072
program: Database Engineering
level: 2
module_number: 72
title: Write-Ahead Logging
status: complete
last_verified: 2026-08-30
---

# Write-Ahead Logging

## One-Page Review

### Governing question

What ordering protocol lets a database acknowledge committed transactions and write dirty pages independently while still reconstructing an authorized state after a crash?

### Essential definitions

A **write-ahead log** (WAL) is an ordered, integrity-protected record of state transitions whose required prefix reaches a declared durable boundary before any dependent data-page write or synchronous commit acknowledgement. A **log sequence number** (LSN) identifies a position in that order. A page's **pageLSN** identifies the latest logged change reflected in that page image. The **insert LSN** bounds complete records published to log memory; the **write LSN** bounds bytes submitted to the storage path; the **flush LSN** bounds the contiguous prefix confirmed durable under the configured persistence contract. A transaction's **commit LSN** identifies its commit record. **Steal** permits an uncommitted dirty page to be written; **no-force** permits commit without writing all of the transaction's data pages. **Redo** reapplies a logged effect missing from data pages; **undo** removes an uncommitted effect that reached them. A **torn write** contains only part of an intended page or record.

### Central model, mechanism, or theorem

For every page image `I` with `I.pageLSN = L`, the image may cross the durable data boundary only after the WAL prefix through `L` is durable:

$$
durableWAL \ge I.pageLSN.
$$

For a synchronous durability contract, transaction `T` may be acknowledged committed only after the required durability boundary contains its commit record:

$$
ack(T) \Rightarrow durableWAL \ge commitLSN(T).
$$

These are ordering implications, not statements that a write system call is durable. If the log has sufficient redo/undo information, intact record boundaries, recoverable transaction/page identity, and idempotent recovery rules, WAL permits the high-performance **steal/no-force** buffer policy: pages may be evicted before commit, and commit need not force random data pages.

### Critical invariants

- Reserve an LSN, construct a complete record, and publish it before exposing the corresponding page mutation to a writer.
- Never advance `flushLSN` past a hole, partial record, corrupt record, or unconfirmed persistence boundary.
- Before writing a captured page image with `pageLSN=L`, make WAL durable through `L`; compare with the captured image, not a later in-memory version.
- Before acknowledging synchronous commit, make the relevant local or replicated commit prefix durable according to the advertised contract.
- Detect a partial or corrupt log tail and stop at the last verified contiguous record; never invent a record from plausible bytes.
- Preserve transaction identity, page/object identity and generation, record length/type, LSN relationships, and integrity coverage.
- Make redo idempotent or guarded by page/log state; make undo restartable and log its progress where repeated failure is admitted.
- Retain every log record still needed by crash recovery, replicas, archives, backups, decoding consumers, or the oldest checkpoint/recovery point.
- Treat `write`, `flush`, `apply`, `commit`, `replicate`, and `acknowledge` as different events.

### Common failures

Common failures are describing WAL as merely an append-only file; flushing a page before its record; acknowledging after copying into a process or kernel buffer; advancing the durable frontier over a gap; assigning an LSN before a record is fully publishable; racing a page writer with a later mutation; assuming sector atomicity; accepting a syntactically plausible corrupt tail; recycling segments still needed by a lagging consumer; allowing log-full deadlock; confusing database redo WAL with a logical replication or audit log; treating checkpoints as durability barriers for every commit; replaying non-idempotent effects twice; logging plaintext secrets without retention controls; and benchmarking throughput without crash-cut verification.

### Compact example

Suppose page A is updated at LSNs 10 and 25, page B at 18, transaction 1 commits at 30, transaction 2's abort record is at 35, and page A changes again at 40 after the writer captured its LSN-25 image. At `flushLSN=17`, neither captured page may persist. At 18, B may persist; at 25, the captured A image may persist, but the live A frame remains dirty because it contains LSN 40. Transaction 1 cannot receive a synchronous acknowledgement at 25 and can at 30. One group flush through 35 can release waiters at 30 and 35. A crash with a verified prefix ending at 30 makes transaction 1 a winner and transaction 2 a loser in the stated undo/redo model.

### Connections

Retrieve [Life of a Transactional Write](010-life-of-a-transactional-write.md), [Dirty Pages and Writeback](028-dirty-pages-and-writeback.md), [Checksums and Page Corruption](029-checksums-and-page-corruption.md), and [Failure Models](071-failure-models.md). Continue through [the roadmap](../ROADMAP.md) to LSNs, undo/redo, checkpoints, ARIES, group commit, crash recovery, log shipping, backups, and verified restore.

## Governing Question

Database pages are updated in memory, commits are latency-sensitive, and random page writes are far more difficult to coordinate than an ordered log stream. A crash can occur between any two instructions, system calls, device operations, or acknowledgements. What must be ordered, made durable, identified, and checked so that restart can distinguish committed work, incomplete work, and page images at different points in history?

The answer is not “write everything twice.” WAL is a protocol connecting concurrency control, buffer management, transaction state, storage persistence, and recovery. Its proof obligation is conditional: given a failure model and a trustworthy durable-write interface, the log must contain enough verified history before dependent state escapes volatile memory. The details of log record semantics and recovery determine what “enough” means.

## Why This Matters

Without WAL, a system using a no-force policy can acknowledge a transaction whose dirty pages have not reached storage and then lose its effects. A system using steal can write an uncommitted change and then lack the information needed to remove it. Forcing every transaction's data pages at commit avoids one problem but creates random I/O, makes latency depend on the transaction's entire dirty set, and still needs atomicity across multiple pages. WAL concentrates the critical durable work into an ordered stream and decouples data-page writeback from commit.

This performance benefit is inseparable from correctness. PostgreSQL 18 describes the central rule as flushing the WAL describing changes before data-file changes and notes that one WAL synchronization can cover many transactions. SQL Server documentation similarly requires the relevant log records on disk before a dirty page is written. InnoDB uses redo during crash recovery and undo for incomplete transactions. SQLite's WAL mode uses a different file-level design—readers consult a WAL alongside the database and a checkpoint transfers changes—but it still illustrates that “WAL” names a family of designs rather than one universal record format.

The storage boundary is the dangerous seam. A database can order calls correctly while a filesystem, controller, virtualized volume, or device violates the assumed ordering or persistence behavior. PostgreSQL's current reliability documentation explicitly discusses `fsync`, write-through behavior, battery-backed caches, and the risk of storage that falsely reports success. SQLite's atomic-commit analysis similarly makes assumptions about sectors, flushes, and powersafe overwrite visible. WAL proves nothing beyond the persistence contract it actually receives.

Finally, WAL becomes a shared production resource. Crash recovery, physical replication, change capture, archive retention, backup correctness, and point-in-time recovery may all depend on its positions. A stalled consumer can prevent recycling; a full log can stop writes; an incorrectly discarded segment can make recovery impossible. An elite design treats log correctness, capacity, security, observability, and recovery drills as one system.

## Prerequisites and Retrieval

Retrieve the following ideas before proceeding:

- transactions have a begin, zero or more state changes, and a terminal commit or abort decision;
- a buffer pool can contain a newer page image than durable storage;
- a dirty page is an in-memory image whose relevant state has not yet crossed its required persistence boundary;
- a process write, kernel acceptance, controller receipt, device-cache receipt, and nonvolatile persistence are distinct;
- atomicity says incomplete transactions have no committed effect, while durability scopes which acknowledged commits survive which failures;
- a checksum detects covered corruption but does not by itself select the correct historical image;
- latches protect short internal critical sections; transaction locks or MVCC protect logical isolation over longer intervals;
- recovery needs a trusted starting point, a verified log prefix, deterministic record interpretation, and rules for redo and possibly undo;
- a checkpoint bounds discovery/recovery work but does not retroactively make unsafe ordering correct.

DBE-071 defines the crash, storage, corruption, and acknowledgement models. DBE-072 derives the logging invariants. Later modules refine LSN representation, log records, recovery passes, checkpointing, ARIES, commit batching, replication, and restore.

## Learning Objectives

After completing this module, you should be able to:

1. state and justify both the log-before-data and commit-before-acknowledgement rules;
2. distinguish insertion, publication, write, flush, durable prefix, page application, transaction commit, replication, and client acknowledgement;
3. relate steal/no-steal and force/no-force policies to redo and undo requirements;
4. design record identity, LSN, pageLSN, transaction-chain, integrity, and tail-detection structures;
5. reason about concurrent log insertion, page capture, group flush, partial writes, log recycling, and repeated recovery failure;
6. evaluate physical, logical, and physiological logging choices without confusing mechanism with product terminology;
7. construct deterministic crash-cut and storage-fault tests with authoritative state oracles;
8. operate WAL capacity, retention, security, observability, rollout, and rollback as production responsibilities.

## Core Exposition

**Begin with volatile and durable state.** Let `V` contain process memory and any other state lost under the selected crash model. Let `D_log` be the durable log prefix and `D_data` the set of durable data-page images. A transaction update first changes volatile structures. To make recovery possible, the system creates a log record that names the affected logical or physical object, the transaction, the operation or images needed for recovery, and ordering metadata. The critical relationship is not wall-clock time; it is the durable order represented by LSNs.

An LSN is commonly a monotonically ordered byte position or record identifier. It need not be a timestamp, and wall clocks should not determine recovery order. An implementation may reserve positions concurrently, but the durable frontier is a **contiguous prefix**. If records cover positions 100–199 and 300–399 but 200–299 is incomplete, `flushLSN` cannot become 399. Waiters for later LSNs remain blocked until the hole is filled and the complete prefix is flushed.

**Separate four log frontiers.** The insert frontier says complete records are available to the log subsystem. The write frontier says bytes have been submitted below the database. The flush frontier says a contiguous prefix is durable according to the storage contract. A replication frontier may separately say a standby received, wrote, flushed, or applied the prefix. Implementations name these differently, but collapsing them makes false acknowledgements likely.

Publishing also needs a memory-ordering protocol. A worker may reserve an LSN range, populate a record, compute its checksum, and then mark the range complete. A flusher must not observe the completion marker before the record contents. A page-changing worker must not expose the page as writable by the background writer before the corresponding log record is publishable. Locks, atomics, barriers, or a centralized insertion latch implement this invariant; “LSNs are increasing” alone does not.

**The first WAL rule is log before data.** If a captured page image `I` includes updates through `I.pageLSN=L`, the system must make the necessary WAL prefix through `L` durable before allowing that image to become durable data state. This supplies redo information for committed changes missing from older disk pages and, in undo/redo designs, undo information for uncommitted changes present in newer pages.

The comparison is against the captured image. Suppose the writer copies page A at pageLSN 25, releases its latch, and a foreground worker advances the in-memory page to 40. The writer may flush the captured LSN-25 image after WAL reaches 25; it need not wait for 40. But it must not mark the current frame clean, because the LSN-40 change was not in the captured image. Page-write completion therefore needs generation or LSN comparison, not a blind dirty-bit clear.

**The second WAL rule is commit before acknowledgement.** In a synchronous local durability mode, the database appends a commit record and waits until the required WAL prefix is durably flushed before reporting success. A crash before the response but after durable commit produces an ambiguous client outcome, but recovery retains the transaction. A crash after response must retain it within the promised failure boundary. A response lost in transit is an application retry/idempotency problem, not permission to forget a durable commit.

Asynchronous commit deliberately weakens that rule. PostgreSQL 18 documents that `synchronous_commit=off` can acknowledge before local WAL flush, potentially losing recent transactions while recovering to a consistent earlier state. That is a scoped durability policy, not “WAL disabled.” Such a mode is inappropriate when the client immediately causes an irreversible external effect based on the acknowledgement unless a higher-level protocol closes the gap.

**WAL enables steal/no-force.** Buffer policies form a two-by-two design space. **Force** writes every transaction's affected pages at commit; **no-force** allows them to remain dirty, requiring redo for committed changes absent from disk. **Steal** lets the buffer manager write a page containing an uncommitted change; **no-steal** prevents it, avoiding transaction undo from data pages but complicating memory pressure. ARIES is designed for steal/no-force and uses physiological log records, pageLSNs, transaction chains, compensation log records, and repeating history. Other engines choose different structures, but they must close the same information gaps.

Redo-only systems can avoid recovery undo by ensuring uncommitted state cannot enter the durable database image, often through copy-on-write, shadowing, private pages, or applying a committed log. Undo-only designs force committed pages but retain before-images for uncommitted state. Undo/redo WAL supports flexible buffer management but records both effects or enough semantics to reverse them. The labels describe recovery information and policy, not merely whether files named “redo” or “undo” exist.

**Choose log record semantics deliberately.** A physical record describes byte/slot/page changes and makes redo deterministic against a named page generation, but it can be verbose and tied to representation. A logical record describes an operation such as “insert key K,” which is compact and representation-independent but may require locks, indexes, uniqueness context, and deterministic semantics during recovery. A physiological record identifies a page physically and an operation logically within that page, balancing locality and flexibility. ARIES popularized this middle ground.

A robust record commonly contains a type/version, total length, LSN, previous-record LSN for the transaction, transaction ID and epoch, object/page identity and generation, redo/undo payload or operation, flags, and checksum or authenticated integrity field. The header and trailer must allow forward scanning, tail validation, and sometimes backward navigation. Variable-length or cross-block records need explicit continuation rules. Unknown mandatory versions must stop recovery rather than be guessed.

**Make page state comparable to log state.** The pageLSN says which log change the page image reflects. During redo, if the durable page already has `pageLSN >= record.LSN` under the correct identity/generation semantics, the record can usually be skipped; otherwise its redo is applied and pageLSN advanced. This is an idempotence guard, not a universal proof: a corrupt page may carry a forged or corrupted high LSN, and logical operations may need different repeatability conditions. Page checksum, identity, generation, and format validation precede trusting pageLSN.

Transaction chains support rollback. A record's `prevLSN` points to the transaction's preceding record. Undo walks backward and applies inverse information. If a crash occurs during recovery, repeating an unlogged undo could duplicate it. ARIES writes compensation log records (CLRs) describing completed undo and where to continue, making rollback progress restartable and avoiding undo of an undo. DBE-077 develops that complete algorithm; WAL provides its substrate.

**Treat the tail as hostile input.** A crash can leave a partially written log block, a complete block without the latest flush, stale sectors, reordered blocks, or corrupt length/checksum fields. Recovery must identify the last verified contiguous record using block/segment identity, LSN ranges, lengths, checksums, and expected continuity. It truncates or ignores the invalid suffix according to a specified procedure. Scanning for a byte pattern that looks like a header can resurrect garbage.

Data pages can tear independently. PostgreSQL's current `full_page_writes` behavior logs a full image for the first change to a page after a checkpoint so recovery can replace a mixed old/new page; it can compress such images. InnoDB documents a doublewrite buffer as another product mechanism. These are implementation strategies for page-write failure, not substitutes for WAL ordering. Atomic-write-capable storage can change the mechanism only after the full stack's contract is established.

**A flush is a storage protocol.** A successful `write` may mean only that the kernel copied bytes. A database uses `fsync`, `fdatasync`, `O_DSYNC`, `O_SYNC`, platform equivalents, or a direct-I/O protocol to request persistence and ordering. The guarantee depends on filesystem, device mapper, virtualization, controller caches, device firmware, power-loss protection, barriers, and error propagation. A battery-backed cache can be within the durable boundary if its failure assumptions and monitoring support that claim. A volatile cache that lies about flush destroys it.

Do not infer atomicity from common sector sizes. Records spanning sectors or log blocks can tear. Even when an aligned sector write is atomic under one device, intervening layers can split or reorder it. Log formats use checksummed blocks, redundant metadata, sequence/generation values, and conservative tail rules because the storage interface is fallible.

**Group commit amortizes synchronization.** Suppose transactions wait for commit LSNs 30, 33, and 35. A coordinator chooses target 35, writes the contiguous log through 35, executes one durability operation, advances `flushLSN` to 35 only on confirmed success, and wakes all waiters whose required LSN is at most 35. The system may deliberately wait a short interval to collect peers, trading individual latency for throughput. PostgreSQL 18 documents `commit_delay` and `commit_siblings` as one current policy; the general mechanism is independent of those settings.

Correct grouping needs one-owner or coordinated flush state, monotone targets, error fan-out, and no early waiter release. A failed flush cannot be reported as success to some waiters because their records happen to be in a buffer. A follower that observes another flusher working must recheck `flushLSN` after wakeup. Very large transactions or record producers need fairness so small commits neither starve nor bypass required order.

The following executable explores one finite WAL schedule. It assumes an undo/redo model, intact records, and a trustworthy flush primitive; it is evidence for the stated schedule, not a production implementation.

<!-- bijux-verify: {"id":"finite-wal-schedule","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"records=6\nlog_bytes=608\ninitial_flush_lsn=17\npage_a_flush_at_17=false\npage_b_flush_at_17=false\npage_b_flush_at_18=true\npage_a_flush_at_18=false\npage_a_flush_at_25=true\ncurrent_page_clean_at_25=false\ntxn1_ack_at_25=false\ntxn1_ack_at_30=true\ngroup_flush_target=35\ndurable_prefix_contiguous=true\ncrash_prefix_lsn=30\ntxn1_status=winner\ntxn2_status=loser\nredo_required=true\nundo_required=true\nstorage_flush_contract=required\nevidence=finite_wal_schedule\n","stderr":""}} -->
```python
records = [
    {"lsn": 10, "txn": 1, "kind": "update", "page": "A", "bytes": 120},
    {"lsn": 18, "txn": 2, "kind": "update", "page": "B", "bytes": 80},
    {"lsn": 25, "txn": 1, "kind": "update", "page": "A", "bytes": 160},
    {"lsn": 30, "txn": 1, "kind": "commit", "page": None, "bytes": 64},
    {"lsn": 35, "txn": 2, "kind": "abort", "page": None, "bytes": 64},
    {"lsn": 40, "txn": 3, "kind": "update", "page": "A", "bytes": 120},
]

captured_pages = {"A": 25, "B": 18}
current_page_lsn = {"A": 40, "B": 18}

def page_flush_legal(page: str, flush_lsn: int) -> bool:
    return flush_lsn >= captured_pages[page]

def lower(value: bool) -> str:
    return str(value).lower()

print(f"records={len(records)}")
print(f"log_bytes={sum(record['bytes'] for record in records)}")
print("initial_flush_lsn=17")
print(f"page_a_flush_at_17={lower(page_flush_legal('A', 17))}")
print(f"page_b_flush_at_17={lower(page_flush_legal('B', 17))}")
print(f"page_b_flush_at_18={lower(page_flush_legal('B', 18))}")
print(f"page_a_flush_at_18={lower(page_flush_legal('A', 18))}")
print(f"page_a_flush_at_25={lower(page_flush_legal('A', 25))}")
print(f"current_page_clean_at_25={lower(current_page_lsn['A'] <= 25)}")
print(f"txn1_ack_at_25={lower(25 >= 30)}")
print(f"txn1_ack_at_30={lower(30 >= 30)}")
print(f"group_flush_target={max(30, 35)}")

crash_prefix = 30
durable_records = [record for record in records if record["lsn"] <= crash_prefix]
winner_txns = {
    record["txn"] for record in durable_records if record["kind"] == "commit"
}
updated_txns = {
    record["txn"] for record in durable_records if record["kind"] == "update"
}
loser_txns = updated_txns - winner_txns

print("durable_prefix_contiguous=true")
print(f"crash_prefix_lsn={crash_prefix}")
print(f"txn1_status={'winner' if 1 in winner_txns else 'loser'}")
print(f"txn2_status={'loser' if 2 in loser_txns else 'winner'}")
print(f"redo_required={lower(bool(winner_txns))}")
print(f"undo_required={lower(bool(loser_txns))}")
print("storage_flush_contract=required")
print("evidence=finite_wal_schedule")
```

**Manage the log as a finite resource.** A circular log can reuse space only below every required retention frontier. Candidate consumers include crash recovery from the oldest needed checkpoint/dirty page, active transaction undo, replicas, archive shipping, backup start positions, point-in-time recovery policy, and logical decoding/change-data-capture slots. The safe recycle LSN is the minimum required position across those consumers, after accounting for segment boundaries and metadata durability.

Checkpointing narrows recovery discovery and permits recycling; it does not mean all data pages are current unless it is a sharp/quiescent checkpoint with that explicit policy. Fuzzy checkpoints record enough state while transactions and writeback continue. They must themselves be logged and interpreted under crash cuts. A checkpoint record whose related metadata or WAL is not durable cannot authorize discarding history.

Capacity planning links production rate and retention time. If WAL is generated at peak sustained rate `r` bytes/s and the longest admitted consumer lag is `t`, the lower-bound payload is `r*t`, before burst, checkpoint, full-page-image, transaction, archive retry, safety, and resize margins. A 200 MiB/s burst lasting 15 minutes produces about 175.8 GiB. Sizing to a daily average would fail. Backpressure should begin before exhaustion and identify the blocking consumer; silently discarding required history converts capacity pressure into unrecoverability.

Log-full handling must avoid circular dependency. If an active transaction needs new log space to abort but its own earliest record prevents reuse, reserved emergency/rollback capacity, transaction size limits, spill policy, or admission control is required. ENOSPC, quota changes, archive failures, read-only transitions, and partial segment allocation are correctness tests, not mere monitoring cases.

**Distinguish WAL consumers and formats.** Crash-recovery WAL is often physical or physiological and coupled to storage format. A logical replication stream describes committed logical changes and may omit physical maintenance. A statement log depends on deterministic execution and complete environment. An audit log targets accountability and may require tamper evidence, actor context, and different retention. One stream can feed another, but no name implies interchangeable recovery guarantees.

Physical log shipping replays WAL on a compatible standby. Receipt, kernel write, durable flush, replay/apply, and query visibility are separate acknowledgement levels. PostgreSQL 18's synchronous modes expose several of these boundaries. Replication does not repair a local WAL rule violation, and local WAL durability does not prove remote failover durability. Membership, timelines/epochs, fencing, compatibility, and retained positions extend the proof.

**Protect confidentiality and integrity.** WAL may contain old and new row values, index keys, identifiers, schema details, or secrets that applications later delete. Apply least privilege, secure transport, encryption at rest where the threat model requires it, key availability during recovery, controlled archive access, and time-bounded retention. Redaction can conflict with recoverability and must be designed at the data model rather than by damaging records.

Checksums detect accidental changes within coverage; keyed authentication or signatures address different tampering threats. Integrity metadata must bind record contents to stream identity, position, version, and preferably segment/generation context so valid records cannot be silently relocated. Recovery and observability must avoid printing payloads into less-protected logs.

**Validate the proof at cut points.** Construct a deterministic schedule of transaction updates, log reservation/publication, page capture, write submission/completion, commit record, log write/flush, response, checkpoint, recycle, and recovery actions. Crash before and after each boundary. Then vary process death, OS crash, power loss, torn/reordered/lost/corrupt/lying writes, ENOSPC, read errors, and another crash during redo or undo.

The oracle is an authoritative committed-transaction ledger plus page/log integrity and application invariants. After recovery, every synchronously acknowledged transaction inside the tested failure model must be present, no uncommitted transaction may be visible, indexes and base data must agree, record/page identities and checksums must validate, and replay must converge when repeated. “The server restarted” is not enough.

Model checking or deterministic simulation can cover finite schedules and invariant violations. Unit/property tests cover codecs, lengths, checksums, LSN comparisons, wraparound, and corrupt tails. Fault injection exercises real error paths. Power-cut testing on the qualified storage stack tests the persistence premise. Restore drills test archived history. Each evidence type is explicitly scoped; none establishes universal correctness.

**Operate measurable frontiers.** Observe insert/write/flush LSN and their byte/time gaps; commit flush latency and group size; WAL bytes by record class; full-page-image rate; log buffer pressure; dirty-page and checkpoint rates; archive/replica/decoder lag; oldest retained LSN and blocking consumer; capacity and exhaustion forecast; flush errors and duration tails; recovery start/end positions and redo/undo rates; corrupt-tail or checksum events; and durability-mode changes.

Deploy WAL format or policy changes with versioned decoders, mixed-version compatibility evidence, canaries, controlled crash tests, capacity headroom, and recovery rollback plans. A writer that emits a new mandatory record before every possible recovery binary can understand it can make rollback impossible. The safe rollback unit includes on-disk log format, data format, checkpoint metadata, replica versions, archives, and keys—not just an application package.

## Definitions and Notation

Let the WAL be a sequence of complete records `R_1, R_2, ...` ordered by LSN. Let `end(R)` be the first LSN after record `R`. Let `insertLSN`, `writeLSN`, and `flushLSN` be monotone frontiers with the intended relationship `flushLSN <= writeLSN <= insertLSN`, acknowledging that implementations may represent endpoints differently.

For transaction `T`, `commitLSN(T)` is the LSN of its durable decision record under this model, and `prevLSN(R)` links a record to the previous record for the same transaction. For a captured page image `I`, `pageLSN(I)` is the latest log record reflected in the image. `currentPageLSN(P)` may exceed the captured value if a writer copied the page and released its latch before I/O completed.

Define:

- **log-before-data:** `persistData(I) => flushLSN >= pageLSN(I)`;
- **commit-before-ack:** `ack_sync(T) => flushLSN >= end(commitRecord(T))`, adjusted if an implementation names the start rather than end position;
- **verified prefix:** every record up to the frontier has valid boundaries, continuity, version, identity, and integrity under the format contract;
- **winner:** a transaction with the required durable commit decision in the recovered prefix;
- **loser:** an active/uncommitted transaction whose logged effects may require undo;
- **redoable:** the log contains a deterministic, safe way to reconstruct a missing effect;
- **undoable:** the log contains a deterministic, safe way to reverse an escaped uncommitted effect;
- **recovery point:** the earliest LSN from which required analysis/redo can begin using the durable checkpoint and page state;
- **retention frontier:** the oldest LSN required by one consumer;
- **recycle frontier:** the minimum safe position across all required consumers.

“Durable” always names a boundary and failure model: process crash, OS crash, power loss, device failure, or replicated-domain loss. “Applied” means a record's effect has reached an in-memory or durable page as stated. “Committed” is a database decision; “acknowledged” is an external observation. They are deliberately not synonyms.

## Mechanisms, Invariants, or Proof Structure

The WAL argument has four layers.

**1. Publication invariant.** Before a page mutation can be captured for durable write, the corresponding complete log record is visible to the log flusher at its reserved LSN. This excludes holes and half-built records from the prefix. Concurrency primitives establish memory visibility and ownership.

**2. Data ordering invariant.** Before page image `I` becomes durable, the verified WAL prefix contains the recovery record(s) through `pageLSN(I)`. Therefore, after a crash, any escaped update is explainable by durable history. If the transaction committed but the page is old, redo can install it. If it did not commit but the page contains it, an undo/redo design can remove it. The conclusion depends on record sufficiency and correct recovery, not ordering alone.

**3. Acknowledgement invariant.** Before acknowledging a synchronous commit, the verified prefix contains the commit record at the promised local/remote persistence boundary. Therefore, under the admitted crash model, recovery classifies the transaction as a winner. This does not guarantee that the client received the response, that replicas applied it, or that an asynchronous policy retains it.

**4. Recovery idempotence invariant.** Recovery validates a trusted starting point and prefix, redoes only effects absent from the correct page generation, and performs restartable undo for losers. A subsequent crash at any recovery cut point leads to another valid analysis rather than duplicate logical effects or lost undo progress.

A proof review must make the following assumptions explicit: record reservation/publication is race-free; LSN order matches recovery dependencies; log and page identities cannot be confused across generations; the checksum/authentication model is sufficient for admitted corruption; the persistence API honors ordering; page writes have an admitted tear-repair mechanism; the correct checkpoint and log prefix are retained; redo/undo operations meet their repeatability rules; transaction outcome records are interpreted consistently; and failures during recovery are included.

The finite executable verifies only arithmetic and Boolean implications for one schedule. It does not model caches, memory ordering, codecs, storage failures, latches, transactions, recovery implementation, or real durability. Those require layered tests and proof artifacts.

## Alternatives and Trade-Offs

**Force/no-steal** simplifies recovery intuition but couples commit to page I/O and can pin large uncommitted working sets. **No-force/steal with undo/redo WAL** improves throughput and buffer flexibility at the cost of complex records and recovery. **Redo-only with private/copy-on-write state** avoids recovery undo but pays for version management, garbage collection, commit installation, and potentially write amplification. **Shadow paging** atomically switches a root to new pages but fragments storage and complicates concurrency and large updates.

**Physical logging** has deterministic local replay and direct pageLSN tests but couples the log to layout and may be voluminous. **Logical logging** can be compact and representation-independent but requires deterministic semantics and enough concurrency context. **Physiological logging** combines physical page identity with logical action inside the page, but recovery remains tightly integrated with page structure.

**Synchronous commit** narrows acknowledged-data loss within its storage boundary but adds flush latency. **Asynchronous commit** reduces latency and increases throughput while accepting a recent acknowledged-loss window. **Group commit** amortizes flush cost while adding queueing and coordination. **Battery-backed or nonvolatile caches** can reduce durable latency if their health, power, firmware, and replacement behavior are inside the model.

**Full-page images** repair torn pages and simplify first-change recovery but increase WAL volume, especially after checkpoints. **Doublewrite**, atomic-write interfaces, copy-on-write pages, or redundancy provide different repair paths and write costs. Turning a protection off is safe only under a proven replacement contract, not a benchmark preference.

**Large WAL capacity** absorbs bursts and consumer lag but expands storage cost and potentially recovery/operational exposure. **Frequent checkpoints** can shorten recovery and reclaim space while causing page-write pressure and more first-change full images. **Longer intervals** smooth writeback but retain more WAL and enlarge recovery work. The optimum follows measured workload and recovery objectives, never capacity alone.

**One crash-recovery stream** is efficient for engine recovery but often unsuitable as a stable public CDC or audit contract. Separate derived logical/audit streams add processing and consistency boundaries but give consumers versioning, filtering, privacy, and retention appropriate to their purpose.

## Failure Modes and Misconceptions

1. **“Append means durable.”** Append describes placement; durability requires a verified persistence operation across the actual stack.
2. **“The WAL rule means flush the newest pageLSN.”** It applies to the captured image. A later live version remains dirty but need not delay the older image.
3. **“Increasing LSNs imply a durable prefix.”** Concurrent reservation can leave holes; the flush frontier cannot cross an incomplete record.
4. **“Commit record inserted means committed to the client.”** Insertion, write, flush, replicated flush, apply, and acknowledgement are different frontiers.
5. **“WAL removes torn-page risk.”** Ordinary redo may not reconstruct a mixed old/new page without full-page images, atomic writes, doublewrite, or another repair mechanism.
6. **“Checkpoints flush every commit.”** Fuzzy checkpoints summarize state and bound recovery; per-commit durability remains a WAL rule.
7. **“A checksum finds the correct tail.”** It detects covered corruption probabilistically; continuity, identity, length, version, and conservative truncation also matter.
8. **“Redo can always run twice.”** Physical pageLSN guards or explicitly idempotent logical operations are required; external effects demand separate protocols.
9. **“Undo can be repeated freely.”** Without logged progress such as CLRs, a second recovery may undo an undo or repeat a non-idempotent inverse.
10. **“A replica has the WAL.”** Received, written, durably flushed, replayed, visible, and eligible after fencing are distinct states.
11. **“More WAL capacity fixes lag.”** It delays exhaustion; it does not repair a stuck archive, replica, backup, or decoder.
12. **“Delete from tables deletes from WAL.”** Historical values can persist in log segments and archives under different access and retention policies.
13. **“One crash test validates durability.”** Process kills do not validate OS, power, controller, device, reordering, corruption, or repeated recovery failures.
14. **“Database restart success is the oracle.”** Silent loss, partial commit visibility, index inconsistency, or skipped corrupt records can remain.
15. **“Rollback means reinstall the old binary.”** New WAL/data/checkpoint formats may make old recovery code unable to start safely.
16. **“WAL proves universal durability.”** Every conclusion is conditional on the failure model, record semantics, recovery logic, storage contract, and retained evidence.

## Worked Examples

### Example 1

**Situation.** A writer captured page A at `pageLSN=25`. The live frame then advanced to 40. WAL is durable through 25. May the captured image be written, and may the frame be marked clean?

**Reasoning.** The captured bytes contain effects only through 25, so the log-before-data rule is satisfied. The live frame contains an additional change at 40 that is absent from the captured image. Completion must compare the captured and current versions.

**Conclusion.** Write the captured image, but retain the frame's dirty state until an image containing LSN 40 is safely persisted.

### Example 2

**Situation.** Workers reserve record ranges ending at 120, 180, and 240. The middle worker stalls; records through 120 and 181–240 are complete. Can the flusher publish or flush through 240?

**Reasoning.** The durable log is a contiguous parseable prefix. The missing range prevents a decoder from reaching later records reliably and may contain a dependency. Monotone numeric allocation is not completeness.

**Conclusion.** The publish/flush frontier stops at 120 until the hole is completed or a specified cancellation/fill protocol repairs it.

### Example 3

**Situation.** Transaction T's update record is at 500 and commit record ends at 560. The page is already durable, the log has been written to the kernel through 560, but `flushLSN=520`. May synchronous success be returned?

**Reasoning.** Page persistence cannot substitute for an atomic multi-page commit decision, and kernel buffering is outside the selected power-loss boundary. The durable prefix lacks the complete commit record.

**Conclusion.** No. Wait until the configured durable frontier covers the commit record; otherwise advertise and account for asynchronous durability.

### Example 4

**Situation.** Commit waiters require LSNs 700, 735, and 710. One flush can cover 735 at 2 ms fixed cost plus 0.01 ms per KiB; the 35 KiB range costs 2.35 ms. Three separate flushes cost at least 6 ms before byte cost.

**Reasoning.** Choosing the maximum target creates one durable prefix that subsumes all three requirements. Each waiter is released only after `flushLSN` reaches its own target. Added queueing must be included in tail-latency policy.

**Conclusion.** Group flush through 735 amortizes fixed persistence cost without weakening the acknowledgement invariant.

### Example 5

**Situation.** A 16 KiB data page may tear on the qualified stack. An update record contains only a 40-byte tuple delta. After crash, the page contains its old first half and new second half.

**Reasoning.** Applying the delta assumes a valid old page, which the torn image is not. WAL ordering ensured the delta was durable but did not make the page atomic. A full-page image, doublewrite copy, atomic page write, or equivalent repair source is needed.

**Conclusion.** WAL ordering is necessary but insufficient for torn-page recovery under this storage model.

### Example 6

**Situation.** A log block header and checksum are valid at LSN 900, the next record declares an impossible length crossing beyond the available durable bytes, and later bytes contain the normal record magic.

**Reasoning.** The impossible record breaks the verified prefix. Searching later bytes for magic risks treating stale or payload bytes as records. Recovery accepts only the last complete, continuous, integrity-valid boundary.

**Conclusion.** Stop at 900 and handle the suffix by the documented tail procedure; never skip forward heuristically.

### Example 7

**Situation.** A system generates 200 MiB/s during a 15-minute peak while an archive may legitimately lag that long. What is the payload lower bound before safety margins?

**Reasoning.** `200 * 15 * 60 = 180,000 MiB`. Dividing by 1024 gives `175.78125 GiB`. Average rate, segment metadata, checkpoints, full-page images, retries, active transactions, and headroom are not yet included.

**Conclusion.** Plan for more than 175.8 GiB; a capacity derived from the daily average would violate the admitted burst-and-lag model.

### Example 8

**Situation.** Transaction U updates a page and its uncommitted image is stolen to disk. Its durable update record has a before-image, but the crash prefix has no commit record.

**Reasoning.** Recovery classifies U as a loser. The escaped update is explainable and undoable because the before-image and transaction chain are durable. If the record had only redo information, the chosen steal policy would lack required recovery information.

**Conclusion.** Undo U using restartable logged progress; recovery information must match buffer policy.

### Example 9

**Situation.** A primary reports that a standby has received commit WAL in its process buffer. Both machines then lose power. The service promised remote power-loss durability.

**Reasoning.** Receipt is not remote durable flush. The acknowledgement boundary was weaker than the advertised failure model, even though replication occurred. A remote-write mode may survive a standby process crash while failing an OS/power crash.

**Conclusion.** Require and observe the exact remote durable frontier plus membership/fencing conditions before making the stronger promise.

### Example 10

**Situation.** A canary writer emits a new mandatory record type. Recovery tests pass on the new binary, but rollback would start an old binary that treats the type as unknown.

**Reasoning.** WAL is a persistent compatibility interface. Once the new record is in every retained recovery path, binary rollback alone is unsafe. The rollout needed reader-before-writer ordering or a reversible format gate.

**Conclusion.** Stop rollout and use the compatible recovery path; future changes must prove mixed-version read, write, replay, archive, and rollback behavior before emission.

## Cross-Program Connections

- **Data Structures Engineering:** WAL buffers, rings, segment indexes, checksums, and pageLSN maps turn abstract sequence and storage structures into correctness-critical implementations.
- **Data Engineering:** CDC and stream processing consume ordered changes but need a stable logical contract, retention, idempotence, and privacy beyond engine recovery records.
- **Data Architecture Engineering:** recovery positions, archival tiers, sovereignty, lifecycle, and RPO/RTO connect a local log to enterprise data guarantees.
- **API and Service Engineering:** a lost commit response creates an ambiguous outcome; idempotency keys and status queries bridge database commit and client retries.
- **Platform Engineering:** filesystems, volumes, controllers, power-loss protection, monitoring, upgrades, and fault injection determine whether the durable boundary is real.
- **Concurrent and Parallel Programming:** LSN reservation, publish barriers, flush leadership, waiter wakeup, and page-capture races require explicit happens-before reasoning.
- **Functional Programming:** an immutable event history resembles WAL, but replayable domain events and physical recovery records have different semantics and compatibility contracts.
- **Object-Oriented Programming:** page, record, transaction, and storage abstractions must expose invariants rather than allow subclasses to bypass ordering.
- **Software Engineering Patterns:** append, commit, checkpoint, retry, and recovery are protocols whose state machines, tests, observability, and compatibility matter more than pattern names.
- **Security Engineering:** WAL retention expands the sensitive-data surface and requires access control, encryption/key recovery, integrity protection, and auditability.

## References

1. C. Mohan, D. Haderle, B. Lindsay, H. Pirahesh, and P. Schwarz, “ARIES: A Transaction Recovery Method Supporting Fine-Granularity Locking and Partial Rollbacks Using Write-Ahead Logging,” *ACM Transactions on Database Systems*, 17(1), 1992. Primary algorithm paper; retrieved 2026-08-30 from [IBM Research](https://research.ibm.com/publications/aries-a-transaction-recovery-method-supporting-fine-granularity-locking-and-partial-rollbacks-using-write-ahead-logging).
2. PostgreSQL Global Development Group, [PostgreSQL 18: Write-Ahead Logging](https://www.postgresql.org/docs/18/wal-intro.html), current version reviewed 2026-08-30. Official log-before-data, commit, performance, backup, and PITR overview.
3. PostgreSQL Global Development Group, [PostgreSQL 18: WAL Internals](https://www.postgresql.org/docs/18/wal-internals.html), current version reviewed 2026-08-30. Official page, record, segment, and implementation details.
4. PostgreSQL Global Development Group, [PostgreSQL 18: Write Ahead Log Configuration](https://www.postgresql.org/docs/18/runtime-config-wal.html), current version reviewed 2026-08-30. Official `fsync`, synchronization method, full-page-write, compression, synchronous-commit, and group-commit settings.
5. PostgreSQL Global Development Group, [PostgreSQL 18: Asynchronous Commit](https://www.postgresql.org/docs/18/wal-async-commit.html), current version reviewed 2026-08-30. Official acknowledgement and recent-loss semantics.
6. PostgreSQL Global Development Group, [PostgreSQL 18: Reliability](https://www.postgresql.org/docs/18/wal-reliability.html), current version reviewed 2026-08-30. Official storage-stack, cache, flush, and power-loss discussion.
7. SQLite Project, [Write-Ahead Logging](https://www.sqlite.org/wal.html), official documentation reviewed 2026-08-30. Contrasting WAL-index, reader end-mark, checkpoint, concurrency, and operational design.
8. SQLite Project, [Atomic Commit in SQLite](https://www.sqlite.org/atomiccommit.html), official documentation reviewed 2026-08-30. Explicit filesystem, sector, flush, atomicity, and powersafe-overwrite assumptions.
9. Oracle, [MySQL 8.4 Reference Manual: InnoDB Redo Log](https://dev.mysql.com/doc/refman/8.4/en/innodb-redo-log.html), current version reviewed 2026-08-30. Official redo capacity and file lifecycle.
10. Oracle, [MySQL 8.4 Reference Manual: InnoDB Recovery](https://dev.mysql.com/doc/refman/8.4/en/innodb-recovery.html), current version reviewed 2026-08-30. Official redo application and rollback of incomplete transactions.
11. Microsoft, [SQL Server Transaction Log Architecture and Management Guide](https://learn.microsoft.com/en-us/sql/relational-databases/sql-server-transaction-log-architecture-and-management-guide?view=sql-server-ver17), current documentation reviewed 2026-08-30. Official WAL rule, log records, truncation, and architecture.
12. Microsoft, [Write Pages in the Database Engine](https://learn.microsoft.com/en-us/sql/relational-databases/writing-pages?view=sql-server-ver17), current documentation reviewed 2026-08-30. Official dirty-page write and log-before-page behavior.
13. Jim Gray and Andreas Reuter, *Transaction Processing: Concepts and Techniques*, Morgan Kaufmann, 1993. Durable treatment of recovery, logging, commit, storage, and transaction-processing models.

## Exercises

### Exercise 1

Define `insertLSN`, `writeLSN`, `flushLSN`, `pageLSN`, and `commitLSN`. State the two WAL ordering rules and explain why neither “record appended” nor “page written” alone proves synchronous transaction durability.

### Exercise 2

A page writer captures page P at LSN 140. P advances in memory to 170 before its I/O completes. The log is durable through 150. Trace whether the captured write is legal, whether the frame becomes clean, and what changes when the durable frontier reaches 170.

### Exercise 3

Design a record and recovery-tail validation procedure for variable-length records that may cross 4 KiB log blocks. Include identity, continuity, corruption, unknown versions, incomplete suffixes, and the rule for advancing `flushLSN`.

### Exercise 4

Compare steal/no-force undo/redo WAL with a redo-only copy-on-write design for a high-write transactional service. Address commit latency, buffer pressure, write amplification, recovery complexity, space reclamation, large transactions, and storage-failure assumptions.

### Exercise 5

An unfamiliar multi-region database promises that an acknowledged payment survives loss of the primary region. Design the WAL-related proof and production evidence required before accepting the claim. Include local/remote frontiers, group commit, replication, fencing, compatibility, capacity, security, fault injection, recovery oracle, canary, and rollback.

## Answers to the Exercises

### Answer 1

`insertLSN` bounds complete records published to the log subsystem; `writeLSN` bounds the contiguous bytes submitted to the lower storage path; `flushLSN` bounds the verified contiguous prefix confirmed durable under the declared model. `pageLSN` is the latest logged change contained in one page image, and `commitLSN` identifies a transaction's commit decision record. Log-before-data requires `persistData(I) => flushLSN >= pageLSN(I)`. Synchronous commit-before-ack requires the relevant durable prefix to cover the complete commit record before success. Append may end in volatile process/kernel/device cache; a page write may contain one transaction's changes but cannot atomically establish a multi-page transaction decision. Only the ordered log plus sufficient recovery semantics closes both gaps.

### Answer 2

The captured image contains state only through 140. Because `flushLSN=150`, its log dependency is durable and the write is legal. Completion must compare the captured LSN 140 with the current LSN 170, so the frame stays dirty; clearing it would lose knowledge that the LSN-170 change remains unpersisted. When WAL reaches 170, the old captured image does not magically include 170. The writer must capture and persist a new image (or know another completed write contains it) before marking the current frame clean. This distinguishes write eligibility from current-page cleanliness.

### Answer 3

Use versioned block headers binding stream/database identity, timeline/generation, block start LSN, block sequence, payload length, flags, and checksum/authentication coverage. Each record carries type/version, total length, its LSN/end position, transaction and object/page identity/generation, previous transaction LSN where needed, payload integrity, and explicit continuation metadata. A scanner begins from trusted durable metadata, verifies block identity and expected next position, bounds every length before allocation/read, reconstructs continuations only across the declared next block, validates the complete record, and rejects unknown mandatory versions. It stops at the first missing, partial, discontinuous, impossible, or integrity-invalid record and never searches later bytes for magic. Publication marks a range complete only after contents and integrity are visible; `flushLSN` advances only through complete published records after the storage flush succeeds. Fuzzing covers zero/max lengths, wraparound, duplicate blocks, stale generations, bit flips, truncation at every byte, and hostile length fields.

### Answer 4

Steal/no-force permits eviction of uncommitted pages and avoids forcing random pages at commit; synchronous commit usually waits for an ordered log flush. It handles memory pressure and large dirty sets well, but requires redo for committed missing pages, undo for escaped loser effects, transaction chains, pageLSNs, torn-page protection, restartable rollback, and careful log retention. Copy-on-write keeps committed roots pointing to immutable old pages while building private/new pages, so recovery can often select a committed root and redo committed log without undoing shared pages. It pays in page/tree copying, write amplification, fragmentation, garbage collection, root publication, and space pressure from long readers or transactions. Neither removes storage assumptions: WAL needs ordered durable prefixes and repairable page writes; copy-on-write needs atomic/durable root publication and correct reachability/reclamation. Choose from measured workload, failure model, transaction size, recovery objectives, and operational evidence rather than a universal ranking.

### Answer 5

Define the promise first: payment commit acknowledgement must survive permanent primary-region loss while preserving exactly one authorized logical effect. Trace update and commit records through complete local publication, local write/flush, transport, remote receipt/write/flush, quorum or designated-standby decision, acknowledgement, replay, visibility, and failover eligibility. State whether acknowledgement waits for remote durable flush or apply, what “region loss” includes, and how epochs/quorum membership and fencing prevent the old primary from continuing. Group commit may batch up to a monotone target but releases no payment before its required remote frontier; failures fan out without false success.

Prove record identity/integrity, commit ordering, redo/undo or redo-only sufficiency, tail handling, checkpoint/retention, compatible mixed-version recovery, encryption/key availability, least-privilege archive access, and enough capacity for peak rate plus maximum admitted outage/lag. Test deterministic cuts before/after every local and remote frontier, lost/reordered/duplicate messages, partitions, false suspicion, region power loss, corrupt/torn/lying writes, ENOSPC, archive failure, and crashes during promotion/recovery. The oracle reconciles idempotency key, authoritative transaction ledger, balances, external payment-rail outcome, commit/replication LSNs, page/log integrity, and absence of duplicate effects. Canary with constrained traffic and retained old-format compatibility; rollback includes binaries, WAL/data/checkpoint formats, replicas, archives, membership metadata, and keys. Reject the claim if any acknowledged cut loses the payment, if a stale primary can write, if recovery cannot parse retained WAL, or if the evidence tests only process termination rather than the promised regional boundary.
