---
module_id: OS-046
program: Operating Systems
level: 1
module_number: 46
title: Journaling
status: complete
last_verified: 2026-09-04
---

# Journaling

## One-Page Review

### Governing question

How should a filesystem use a write-ahead journal to make multi-block metadata changes recoverable despite concurrency, reordering, torn writes, finite log space, I/O errors, and sudden failure?

### Essential definitions

- A **journal** is a persistent log of changes or intentions used to recover filesystem state.
- A **transaction** groups updates that cross one recoverability boundary.
- **Write-ahead logging** requires recoverable log records to reach stable storage before affected home locations can depend on them.
- A **commit record** marks a transaction whose required journal contents are complete under the format and storage contract.
- **Checkpointing** copies committed updates to home locations and eventually makes their log space reusable.
- A **revoke record** prevents replay of an older logged image after the same block was freed or repurposed.
- A **transaction credit** reserves journal and metadata capacity before an operation modifies state.
- **Replay** scans the recovery log, validates records, and reapplies eligible committed transactions idempotently.

### Central model, mechanism, or theorem

Represent transaction `T_i=(i,W_i,R_i,D_i,c_i)`: sequence `i`, logged metadata writes `W_i`, revoked home blocks `R_i`, ordered data dependencies `D_i`, and commit evidence `c_i`. Its lifecycle is `running -> locked -> flushing -> committed -> checkpointed -> reclaimed`, with abort as an error terminal state.

Recovery accepts `T_i` only if descriptor, payload, sequence, length, feature, checksum, and commit evidence validate. It replays each eligible `W_i(b)` unless a relevant later revoke forbids that image. The journal is a finite circular resource: head cannot overwrite transactions whose recovery information is still needed. Filesystem consistency follows only when transaction scope includes every cross-structure invariant and lower-layer ordering makes commit evidence truthful.

### Critical invariants

- Every modified journaled buffer is covered by a live handle with sufficient credit before mutation becomes dirty.
- A commit record is persistent only after all required descriptor, payload, revoke, ordering, checksum, and flush conditions hold.
- Uncommitted, malformed, wrong-sequence, wrong-filesystem, or checksum-invalid records are never replayed as committed state.
- Revoke processing prevents stale metadata images from overwriting blocks repurposed by later state.
- Checkpointing never makes log space reusable while recovery could still require its transaction.
- Transaction and lock ordering avoids waiting cycles among writers, commit, checkpoint, allocation, reclaim, and nested filesystems.
- Journal consistency, file-data durability, namespace durability, and whole-application atomicity remain distinct claims.

### Common failures

Common mistakes are writing home metadata before its log is stable, treating syscall return as journal commit, omitting transaction credits for tree splits, replaying until the first plausible commit without sequence validation, forgetting revokes on block reuse, wrapping a circular journal over uncheckpointed records, equating metadata journaling with data journaling, ignoring volatile device caches, assuming replay is harmless when repeated, and claiming `fsync(file)` durably publishes a new filename without the required directory synchronization.

### Compact example

A create operation allocates inode 42 and block 900, updates their bitmaps, initializes inode metadata, and adds a directory entry. All dependent metadata images enter transaction 17 before its commit record. If power fails before commit, replay ignores transaction 17; after a valid commit, replay applies the complete set. If block 900 is later freed and reused as file data, a revoke prevents an older journal image from corrupting the new contents.

### Connections

[OS-043](043-file-allocation.md), [OS-044](044-filesystem-free-space-management.md), and [OS-045](045-buffer-cache-and-page-cache.md) supply mappings, ownership, and writeback. [OS-047](../ROADMAP.md) broadens journaling into crash-consistency analysis, and [OS-050](../ROADMAP.md) composes a complete filesystem.

## Governing Question

A filesystem operation can change directories, inodes, allocation maps, quotas, reference counts, and checksums. Storage can persist only a prefix or reordered subset of those writes when power fails.

The governing question is how to encode enough intent or after-images to recover one coherent state without synchronously overwriting every home block. The answer combines bounded transactions, write-ahead ordering, commit validation, checkpoint discipline, revocation, and idempotent replay.

## Why This Matters

Without a recovery protocol, one interrupted create or truncate can leave a name pointing to an unallocated inode, two files owning one block, or allocated storage unreachable. Full scanning can detect some damage but is expensive and ambiguous.

Journaling reduces recovery to validated log work and permits asynchronous home writes. It also introduces new failure modes: full journals, credit deadlocks, stale replay, commit-record lies, checksum gaps, and hidden writeback errors.

Applications depend on the boundary. A journal can make filesystem metadata structurally consistent while recent file contents are old or absent. Durable application protocols must still synchronize data and names according to the exposed contract.

## Prerequisites and Retrieval

Review [OS-024](024-atomic-operations.md), [OS-025](025-deadlock-conditions-and-avoidance.md), [OS-042](042-inodes-and-metadata.md), [OS-043](043-file-allocation.md), [OS-044](044-filesystem-free-space-management.md), and [OS-045](045-buffer-cache-and-page-cache.md).

Retrieve these distinctions:

- an in-memory critical section is not a persistent atomic transaction;
- a file mapping and allocation map form one ownership invariant;
- dirty cache, submitted I/O, completed I/O, flushed device state, journal commit, and checkpoint are different stages;
- journal placement and home placement can be on one device or separate devices;
- metadata-only, ordered-data, writeback-data, and full-data journaling make different promises;
- a commit marker is trustworthy only under checksums, sequence, and device ordering;
- replay restores filesystem-format consistency, not arbitrary application transactions;
- finite log capacity must be reserved before locks and modifications make rollback difficult.

## Learning Objectives

After this module, you should be able to:

1. model journal transactions, handles, credits, descriptors, payloads, revokes, commits, checkpoints, and circular reuse;
2. compare physical after-image, logical, intent, metadata-only, ordered, and data journaling;
3. trace transaction admission, buffer access, commit, flush, checkpoint, abort, and replay;
4. reason about storage ordering, checksums, torn writes, sequence wrap, external journals, and feature compatibility;
5. specify transaction scope for allocation, rename, truncate, orphan, quota, and reference-count invariants;
6. separate filesystem recovery from application durability and atomicity;
7. test journaling through crash injection, corruption, concurrency, exhaustion, and evidence.

## Core Exposition

### Persistent atomicity problem

Locks make concurrent memory transitions appear atomic but do not force related disk sectors to persist together. Power loss can expose any ordering the storage contract allows.

A recovery protocol restricts valid persistent states. It must cover both data structures and the lower-layer ordering that makes a transaction boundary observable after reboot.

### Journal purpose

A journal records metadata changes or intentions before home-location reuse can make partial state authoritative. Recovery reads a bounded log instead of inferring every interrupted operation from the entire volume.

The log is not automatically a historical audit trail. Checkpoint and wrap deliberately overwrite old recovery information.

### Physical journaling

Physical or block journaling records after-images of metadata blocks plus target identities. Replay copies validated images to their home locations.

This is simple and independent of metadata semantics but can log an entire block for a small field change. Replaying a stale image over a repurposed block requires revocation defenses.

### Logical journaling

Logical logging records operations such as inserting a directory entry or adjusting an extent. Records can be compact but replay must understand format semantics and version compatibility.

Every logical action needs an idempotence or exactly-once recovery design. Preconditions, object generations, and partial prior application complicate replay.

### Intent and completion records

Large operations can log an intent, perform bounded subtransactions, and later log completion. Recovery finishes or cancels unresolved work.

Intent records preserve ownership between transactions, supporting truncation, extent freeing, and repair that cannot fit in one commit.

### Metadata journaling

Metadata-only journaling logs structural blocks but writes ordinary file data directly to home locations. It reduces log traffic while requiring an explicit data-ordering mode.

Recovery can yield a structurally valid file containing old data unless initialization and ordering prevent stale disclosure.

### Ordered-data mode

Ordered mode writes newly associated file data before committing metadata that exposes it. The data itself need not appear in the journal.

This protects selected dependencies, not all application write order. Overwrites and unrelated files follow the precise filesystem contract.

### Writeback-data mode

A weaker mode can allow metadata commit before ordinary data writeback. It improves scheduling freedom but after a crash recent files can contain older contents under documented semantics.

Security still requires newly allocated blocks to avoid disclosing prior owners. Zeroing, unwritten extents, or other initialization mechanisms remain mandatory.

### Data journaling

Full-data journaling writes file data through the journal with metadata, then checkpoints both. It can give stronger transaction coupling at the cost of extra writes and log bandwidth.

Application atomicity remains bounded by transaction splitting and API guarantees. A large write can span multiple filesystem transactions.

### Transaction handles

A mutating operation joins a running transaction through a handle. Nested calls can share that handle under implementation rules; every start has a matching stop.

Stopping a handle ends that updater's participation but need not commit immediately. Group commit batches many operations for throughput.

### Credits

Before taking deep locks or dirtying buffers, a handle reserves enough log space for worst-case metadata changes, revokes, and tree splits. This prevents mid-operation journal exhaustion.

Credit estimation includes indirect effects such as quota and allocation metadata. Extension can fail; the operation must restart at a safe boundary or use deferred intents.

### Running and committing transactions

One transaction can accept new handles while an earlier transaction commits. The transition to locked state prevents new joiners and waits for existing handles to stop.

The commit thread writes descriptors, payloads, revokes, and commit evidence in the required order. Work on a new transaction can proceed without modifying frozen images owned by the committing one.

### Buffer ownership

Before modifying a journaled buffer, code obtains create, write, or undo access. The journal preserves the version needed by an earlier committing transaction if the live buffer changes again.

After mutation, marking journal metadata dirty connects the buffer to the handle and transaction. Dirtying outside this protocol can escape recovery.

### Descriptor blocks

A descriptor identifies the transaction, home targets, payload layout, flags, and checksums according to the journal format. Parsing validates lengths, bounds, sequence, feature set, and escape encoding.

Payload blocks alone are not replayable evidence. They require a valid descriptor and terminal commit record for the same transaction.

### Commit record

The commit block or record states that the transaction's required journal contents reached the declared persistence boundary. It follows those contents under write-ahead ordering.

If missing, torn, wrong-sequence, or checksum-invalid, recovery discards the transaction. A plausible magic number alone is insufficient.

### Checksums

Journal checksums detect torn or corrupted descriptors, payloads, revokes, commit blocks, and superblocks within their coverage. The format states seed, UUID, algorithm, byte order, and excluded fields.

Checksums do not create ordering or repair corrupted valid-checksum semantics. Recovery also validates block ranges, sequence continuity, targets, features, and transaction shape.

### Escaping log payloads

A raw metadata block can begin with bytes resembling a journal header. Physical journals escape or tag such payloads so replay does not parse user metadata as log control.

Encoding and decoding are covered by checksums and bounds. Malformed escape state terminates or rejects recovery conservatively.

### Revoke records

If a previously journaled metadata block is freed and later repurposed, replaying the old image would corrupt its new role. A revoke tells recovery not to apply the obsolete logged image.

Revocation is sequence-aware. It is not merely a general “newer update wins” mechanism, and adding a block to a current transaction follows implementation-specific revoke-table rules.

### Checkpointing

After commit, journaled images can be copied to home locations. When every recovery dependency for a transaction is safely at home or superseded, the tail can advance.

Checkpoint completion differs from commit. A committed transaction is recoverable from the log even before home blocks are current.

### Circular log

The journal reuses a bounded ring. Head marks new append space; tail marks the oldest recovery-required transaction.

Wrap uses sequence numbers and geometry to distinguish current records from old bytes. Admission blocks or triggers checkpoint before head could overwrite live recovery information.

### Sequence numbers

Monotonic transaction identifiers order records and revokes. Recovery expects valid progression and bounds scanning by known head, tail, clean state, or invalid record.

Finite-width wrap requires modular comparison rules. Arbitrary old sectors must not be mistaken for the current epoch.

### Journal superblock

The journal superblock records geometry, head or start state, sequence, features, checksum configuration, UUIDs, and clean or error status.

Mount validates it against the filesystem and supported features. An external journal with the wrong identity is rejected rather than replayed into another volume.

### External journals

Placing the journal on another device can separate traffic or latency. It also creates a multi-device failure and ordering problem.

Identity matching, availability, flush support, failure policy, and recovery pairing are explicit. Losing the external journal can make the filesystem unrecoverable even when home data survives.

### Device write caches

Devices can acknowledge writes before nonvolatile persistence. Preflush and force-unit-access-like mechanisms establish ordering and durability if the device honors them.

Write-ahead logging fails if a commit becomes durable before required log payloads. Barriers are part of correctness, not an optional performance decoration, unless an equivalent persistence guarantee exists.

### Transaction dependencies

Metadata can depend on file data initialization, allocation ownership, quota reservation, orphan recording, or earlier commits. The journal records or enforces a dependency graph without cycles.

Waiting for a commit while holding a lock needed by its writers or checkpoint is a deadlock. Lock and transaction-credit order is designed together.

### Nested filesystems and recursion

A task should not hold an unfinished transaction on one journal and enter another path that can block cyclically. Filesystem reclaim and writeback contexts add recursion constraints.

Reserved handles and no-filesystem-reclaim allocations preserve progress in carefully bounded paths. Unbounded nested journaling is not safe composability.

### Group commit

Many handles can share a transaction and one flush, amortizing device latency. Synchronous callers can wait for the transaction containing their change.

Larger batches increase throughput but extend latency and recovery work. Commit timers and explicit requests bound residence.

### Fast commits

A fast-commit area can record compact filesystem-specific deltas between full commits. It reduces latency and log traffic when operations fit its supported set.

Unsupported or failed cases fall back to a full commit. Replay must be idempotent, validate the delta region, and compose with the preceding full checkpoint.

### Replay scan

Recovery establishes journal identity and geometry, then scans candidate transactions in sequence. It validates every descriptor, payload, revoke, checksum, and commit before applying.

Malformed length or target never controls unchecked I/O. Recovery bounds memory, time, transaction size, and record count against hostile disk images.

### Replay idempotence

Applying recovery twice should yield the same filesystem state for the covered log. Physical after-images are naturally repeatable when targets remain valid and revokes are respected.

Logical records need explicit guards, versions, or deterministic set operations. Incrementing a counter blindly on every replay is not idempotent.

### Replay ordering

Eligible transactions replay in sequence so later committed images supersede earlier ones as specified. Revokes are gathered and interpreted over the correct transaction window.

Recovery persists or marks replay completion before normal mutation can reuse the log ambiguously. A crash during recovery is itself recoverable.

### Abort handling

An I/O, checksum, memory, or internal error can abort the journal. New mutating handles fail, outstanding callers receive errors, and the filesystem may remount read-only.

Continuing writes after recovery guarantees are lost compounds damage. Preserve the first meaningful error and expose operational state.

### Journal fullness

Long-running handles, pinned checkpoints, slow home I/O, or undersized credits can exhaust the ring. Admission then waits, forces commit/checkpoint, or returns an error according to context.

No waiter holds a resource required for the space-producing path. Metrics distinguish running, committing, checkpointing, reserved, and free log blocks.

### Orphan tracking

An inode can be unlinked while open or be mid-truncate across a crash. An orphan list or file records objects needing recovery completion.

Adding and removing orphan state is journaled with link, size, mapping, and allocation transitions. Replay and orphan processing are bounded and idempotent.

### Rename and directories

A namespace transaction updates source and destination entries, parent metadata, link counts, and replaced-object state atomically within filesystem scope. Journaling preserves structural consistency.

Application durable publication still synchronizes file content and affected directories under the platform contract. Namespace atomicity, journal atomicity, and durability are separate axes.

### Large operations

Truncate, snapshot deletion, and repair can touch more metadata than one transaction allows. The operation uses restartable chunks plus durable intents or orphan state.

Every intermediate committed state is format-consistent and retains enough ownership to resume. Credits bound work rather than pretending an unbounded atomic transaction exists.

### Journaling and writeback

Page-cache writeback prepares data mappings and may require unwritten-extent conversion after I/O. Journal transactions record the metadata that makes completed data reachable.

Writeback errors propagate even when metadata transactions themselves commit. A valid journal cannot turn failed data I/O into successful file durability.

### `fsync` and `fdatasync`

Synchronization waits for applicable dirty data, required metadata, journal transaction commit, and device persistence under filesystem rules. `fdatasync` can omit metadata not needed for subsequent data retrieval.

The containing directory can require separate synchronization for a newly created or renamed entry. Applications check every return and retain recovery logic.

### Whole-filesystem synchronization

`syncfs` targets the filesystem containing an open descriptor, while broader sync interfaces schedule or wait according to platform semantics. Freeze additionally blocks mutation to establish a stable administrative window.

These mechanisms use journal commit and checkpoint primitives but do not make unrelated application operations one atomic transaction.

### Mount and recovery policy

Mount options can select data mode, commit interval, barriers, error response, and replay behavior when supported. Skipping required replay exposes known inconsistent state.

Operational policy records exact options and kernel or filesystem version. Changing a durability mode changes the system contract and test matrix.

### Observability and experiments

Record handle type, requested and used credits, transaction ID and state, dirty buffers, ordered dependencies, revokes, descriptor and commit I/O, flushes, checkpoint tail, wait reason, abort error, replay decisions, and recovery result.

Preserve filesystem and journal images, geometry, UUIDs, feature flags, mount options, device-cache settings, crash point, workload seed, raw traces, and limitations.

### Security and assurance

Adversarial tests corrupt lengths, targets, UUIDs, sequences, checksums, features, revokes, head and tail, and commit records. Stress credit exhaustion, nested paths, replay bombs, I/O errors, block reuse, and crashes during replay.

Assurance names filesystem-format, journal, storage, concurrency, recovery, security, application-durability, and independent-verification reviewers. Successful clean unmount is not crash-consistency certification.

## Definitions and Notation

Let circular journal capacity be `L` blocks, head `H`, tail `Q`, and transaction `T_i=(i,W_i,R_i,D_i,c_i)`. `W_i` maps home block identifiers to logged after-images, `R_i` is the revoke set, `D_i` is the ordered-data dependency set, and `c_i` is commit evidence.

Let transaction state `S_i` be `running`, `locked`, `flushing`, `committed`, `checkpointed`, `reclaimed`, or `aborted`. Let handle `h=(i,k,u)` reserve `k` metadata-buffer credits and `u` revoke credits in transaction `i`.

Define `valid(T_i)` only when journal identity, supported features, sequence, bounds, descriptor, payload, revoke, checksums, and commit record all validate. Recovery applies `W_i(b)` only for valid committed transactions and when revoke semantics do not suppress that image.

Write-ahead order is `persist(log_payload_i and required dependencies) happens_before persist(commit_i) happens_before reuse(home or log state that relies on commit_i)`. Checkpointing may follow commit asynchronously.

## Mechanisms, Invariants, or Proof Structure

1. **Define transaction scope.** Include every inode, directory, allocation, quota, reference, checksum, and orphan change needed for one recoverable invariant.
2. **Reserve credits early.** Estimate worst-case buffers, revokes, tree splits, and journal space before acquiring locks that the commit path needs.
3. **Acquire journal access.** Preserve older committing images, associate each modified buffer with one handle, and mark it dirty through the journal protocol.
4. **Freeze a transaction.** Stop new joiners, wait for active handles, and capture ordered data dependencies and immutable log images.
5. **Persist write-ahead records.** Write validated descriptors, payloads, revokes, and required data before terminal commit evidence.
6. **Commit truthfully.** Use checksums, sequence, flush, and device ordering so a valid commit implies all recovery inputs are persistent.
7. **Checkpoint safely.** Write home locations, retain errors, and advance the tail only when replay no longer needs the transaction.
8. **Reuse defensively.** Prevent circular overwrite, stale sequence confusion, and old-image replay after block repurposing.
9. **Replay boundedly.** Validate before allocation or I/O, apply only committed eligible records in order, and make repeated or interrupted replay safe.
10. **Abort honestly.** Stop new mutation, propagate the first relevant error, preserve evidence, and enter a safe read-only or failed state.
11. **Expose durability precisely.** Separate handle stop, transaction commit, checkpoint, file synchronization, directory synchronization, and application atomicity.
12. **Preserve evidence.** Retain IDs, credits, record checks, ordering, device completions, crash points, replay decisions, and limitations.

<!-- bijux-verify: {"id":"journal-commit-replay","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"transaction=17 committed=False replayed=none\ntransaction=17 committed=True replayed=bitmap,directory,inode\ntransaction=18 revoke=bitmap replayed=directory,inode\n","stderr":""}} -->
```python
home = {"inode": "old", "bitmap": "old", "directory": "old"}
updates = {"inode": "new", "bitmap": "new", "directory": "new"}


def replay(committed: bool, revoked: set[str]) -> list[str]:
    applied = []
    if committed:
        for block in sorted(updates):
            if block not in revoked:
                home[block] = updates[block]
                applied.append(block)
    return applied


print(f"transaction=17 committed=False replayed={','.join(replay(False, set())) or 'none'}")
print(f"transaction=17 committed=True replayed={','.join(replay(True, set()))}")
print(f"transaction=18 revoke=bitmap replayed={','.join(replay(True, {'bitmap'}))}")
```

The executable model demonstrates commit-gated after-image replay and one revoke filter. It omits record parsing, sequence windows, physical I/O, checksums, circular reuse, checkpointing, idempotence hazards, and real filesystem behavior.

## Alternatives and Trade-Offs

- Physical after-images simplify replay but log full blocks; logical records reduce bytes but couple recovery to semantic versions.
- Metadata-only journaling reduces write amplification but needs data-ordering rules; data journaling strengthens coupling at much greater bandwidth cost.
- Larger transactions improve batching and group commit but raise latency, credit demand, recovery work, and lock duration.
- Frequent commits reduce exposure windows but increase flush traffic; long intervals improve throughput but delay durability.
- Internal journals simplify device management; external journals can isolate traffic but add identity and multi-device failure dependencies.
- Checksums detect torn or corrupt log records but cost CPU and do not replace ordering or semantic validation.
- Asynchronous commit can overlap I/O when checksums and ordering support it but expands the proof surface.
- Fast commits reduce common-case latency but require delta replay and full-commit fallback paths.
- Eager checkpointing frees log space quickly but competes with foreground I/O; lazy checkpointing improves batching but can stall on journal fullness.
- Intent-based chunking bounds transactions but exposes more intermediate recovery states.
- Barriers protect volatile-cache ordering but add latency; disabling them is safe only with an equivalent verified persistence contract.
- Strict error shutdown preserves integrity but reduces availability; continuing after journal abort risks compounding corruption.

## Failure Modes and Misconceptions

- **“A lock makes disk updates atomic.”** It orders memory concurrency, not power-failure persistence.
- **“Stopping a handle commits it.”** The transaction can batch and commit later.
- **“A commit magic number proves completion.”** Sequence, length, checksum, identity, and storage ordering also matter.
- **“Journaled means all file data is journaled.”** Metadata, ordered, writeback, and data modes differ.
- **“Committed means checkpointed.”** Committed updates can still reside only in journal recovery state.
- **“Checkpointed records can always be overwritten.”** Later dependencies or incomplete home I/O can retain them.
- **“Newer metadata automatically defeats old replay.”** Block reuse requires correct revoke semantics.
- **“Checksums create write ordering.”** They detect corruption but do not force persistence order.
- **“A huge operation is one atomic journal transaction.”** Credits and bounded logs often require restartable chunks.
- **“Replay can trust disk lengths.”** Every value is hostile until bounded and validated.
- **“Replay once is enough to test.”** A crash during replay requires idempotent recovery.
- **“Journal consistency proves application atomicity.”** Application records can span filesystem transactions and names.
- **“`fsync(file)` always persists its filename.”** Directory synchronization can be separately required.
- **“Disabling barriers is a free speedup.”** It can invalidate the commit-before-payload proof.

## Worked Examples

### Example 1

A create dirties inode, inode bitmap, block bitmap, directory, and quota blocks. Credits reserve every worst-case buffer before directory locks make restart costly.

### Example 2

Power fails after descriptor and payload writes but before commit. Recovery validates the records yet discards the transaction because terminal evidence is absent.

### Example 3

Power fails after a valid commit but before checkpoint. Recovery copies the after-images to home locations and restores the coherent new state.

### Example 4

A metadata block is freed and reused as file data after an older logged image exists. Revoke processing prevents replay from overwriting the new data with stale metadata.

### Example 5

A device persists the commit before earlier payloads because its volatile cache ignored ordering. The valid-looking commit lacks its inputs, showing why flush semantics are part of journaling.

### Example 6

Journal head approaches the tail while a checkpoint write is stalled. New handles wait without holding the allocation lock required by checkpoint progress.

### Example 7

A million-block truncate uses a durable free intent and bounded transactions. Every crash leaves the remaining work discoverable without one unbounded credit reservation.

### Example 8

Fast commit cannot encode a particular operation. The filesystem falls back to a full commit rather than silently omitting recovery state.

### Example 9

An I/O error aborts the journal. New mutations fail and the mount enters its configured error state while the original error remains visible.

### Example 10

A service writes and synchronizes a candidate file, renames it over `live`, then synchronizes the parent directory. The application protocol states more than “the filesystem journals metadata.”

## Cross-Program Connections

[Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) connects circular buffers, checksums, sequence arithmetic, trees, and state machines. [Database Engineering](../../18-database-engineering/ROADMAP.md) connects write-ahead logging, commit records, group commit, checkpoints, recovery, and idempotence while retaining different transaction semantics.

[Computer Architecture](../../23-computer-architecture/ROADMAP.md) connects device queues, volatile caches, ordering, atomic sectors, and flushes. [Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies failure models, cross-layer contracts, fault injection, traceability, and assurance.

Within this program, [OS-043](043-file-allocation.md), [OS-044](044-filesystem-free-space-management.md), and [OS-045](045-buffer-cache-and-page-cache.md) supply persistent structures and writeback; [OS-047](../ROADMAP.md) and [OS-050](../ROADMAP.md) broaden recovery and integrated design.

## References

- Linux kernel documentation, [ext4 Journal (jbd2)](https://docs.kernel.org/filesystems/ext4/journal.html), current page checked 2026-09-04. Journal layout, identities, features, headers, descriptors, payloads, revokes, commits, checksums, fast commits, replay idempotence, and checkpoints.
- Linux kernel documentation, [The Linux Journalling API](https://docs.kernel.org/filesystems/journalling.html), current page checked 2026-09-04. Journal lifecycle, nested handles, buffer access, credits, transaction restart, flush, update exclusion, fast commits, locking, and state.
- Linux kernel documentation, [ext4 General Information](https://docs.kernel.org/admin-guide/ext4.html), current page checked 2026-09-04. Data modes, commit intervals, barriers, error policies, journal replay, delayed allocation, and mount behavior.
- Linux kernel documentation, [Explicit volatile write-back cache control](https://docs.kernel.org/block/writeback_cache_control.html), current page checked 2026-09-04. Volatile device caches, flushes, force unit access, request ordering, and filesystem correctness.
- Linux kernel documentation, [Overview of the Linux Virtual File System](https://docs.kernel.org/filesystems/vfs.html), current page checked 2026-09-04. Dirty inodes, writeback, synchronization, freeze, errors, and filesystem lifecycle.
- Linux kernel documentation, [ext4 Orphan File](https://docs.kernel.org/filesystems/ext4/orphan.html), current page checked 2026-09-04. Crash recovery for unlinked or truncating inodes, block layout, checksums, and journaled orphan updates.
- Linux kernel documentation, [iomap Supported File Operations](https://docs.kernel.org/filesystems/iomap/operations.html), current page checked 2026-09-04. Page-cache writeback, mapping allocation, delayed reservation cleanup, I/O completion, unwritten conversion, direct I/O, and errors.
- Linux man-pages project, [fsync(2)](https://man7.org/linux/man-pages/man2/fsync.2.html), current page checked 2026-09-04. File data and metadata persistence, `fdatasync`, device completion, errors, and separate directory synchronization.
- Linux man-pages project, [sync(2) and syncfs(2)](https://man7.org/linux/man-pages/man2/sync.2.html), current page checked 2026-09-04. System-wide and filesystem-scoped synchronization, waiting behavior, and writeback error reporting.
- Linux man-pages project, [mount(2)](https://man7.org/linux/man-pages/man2/mount.2.html), current page checked 2026-09-04. Mount flags, synchronous modes, lazy timestamps, remount behavior, and filesystem-specific options.

## Exercises

### Exercise 1

Specify a physical metadata journal from handle admission through commit, checkpoint, circular reuse, and recovery. Include formats, credits, errors, and ordering.

### Exercise 2

Compare metadata-only writeback, ordered-data, and full-data journaling for stale disclosure, performance, write amplification, and application durability.

### Exercise 3

Design revoke and generation handling for a metadata block that is freed, reused as data, journaled again, and encountered during replay.

### Exercise 4

Design a bounded crash-safe truncate and rename workflow using credits, intents, orphan tracking, synchronization, and error propagation.

### Exercise 5

Build a test and assurance plan for journaling. Include corruption, circular wrap, concurrency, device caches, crashes during replay, evidence, and reviewers.

## Answers to the Exercises

### Answer 1

Define a versioned superblock with journal UUID, filesystem identity, geometry, head, tail, next sequence, feature masks, checksum scheme, and clean or abort state. Before mutation, a handle reserves worst-case descriptor, payload, revoke, and split credits. It obtains access to each buffer, preserves any prior committing image, changes it, and marks it dirty through the journal. Freezing stops new joiners and waits for handles; commit writes descriptors, payloads, revokes, ordered dependencies, checksums, and finally commit evidence with required flushes.

Checkpoint writes committed images home and advances the tail only when all recovery dependencies complete. Ring admission proves head will not overwrite the tail. Recovery validates identity, features, bounds, sequences, every record, checksum, and commit; it gathers revokes and replays eligible after-images in order. Missing or invalid commit discards a transaction. I/O error aborts new mutation and remains observable. Repeated and interrupted recovery yields the same home state.

### Answer 2

Metadata-only writeback mode logs structural updates but permits ordinary data scheduling with relatively weak coupling; recovery stays structurally consistent while recent contents may be old, though new allocations must never expose stale bytes. Ordered mode additionally completes newly associated data before committing metadata that exposes it, reducing stale-data outcomes while adding dependency waits. Full-data mode writes data through the log and couples it with metadata more strongly, at the cost of extra writes, journal bandwidth, and checkpoint traffic.

Measure transaction bytes, device writes, flushes, throughput, tail latency, recovery time, and crash outcomes for create, append, overwrite, rename, and truncate. None of the modes automatically makes multiple application files one transaction. Applications still use file and directory synchronization and their own commit protocol according to the filesystem's documented semantics.

### Answer 3

Identify every journal record by filesystem and journal UUID, transaction sequence, home block, type, and checksum. When the metadata block is freed, add the sequence-scoped revoke before later reuse can become recovery-visible. Reallocation as file data initializes it and commits new ownership under ordering rules. Recovery first validates the transaction window and builds revoke state, then suppresses the obsolete metadata after-image that would overwrite the repurposed block.

If a still-later transaction journals the block again as metadata, its valid new record follows the journal's rule for removing or superseding revoke state. Tests cover sequence wrap, duplicate revokes, missing commit, corrupt target, external-journal mismatch, crashes after free and reuse, and repeated replay. A raw “highest sequence wins” shortcut is rejected unless it exactly implements the format semantics.

### Answer 4

For large truncate, log an intent or orphan record that preserves the inode and remaining range, then remove extents in bounded credited transactions. Each transaction atomically updates inode size or progress, mappings, free space, reference counts, quota, checksums, and intent state. Recovery resumes idempotently; final completion removes orphan or intent state. Locks are released before transaction restart in a state that remains valid.

For rename publication, first write and synchronize candidate data and retrieval-required metadata. A bounded namespace transaction updates source and destination directories, parent metadata, victim lifetime, and link counts. Check its error, then synchronize every parent directory required by the platform contract. Propagate journal abort, delayed writeback, allocation, quota, and device errors; never report application durability from rename atomicity alone.

### Answer 5

Generate transactions at minimum and maximum credits, nested handles, concurrent join and freeze, checkpoint pressure, ring wrap, sequence wrap boundaries, external-journal mismatch, data modes, fast-commit fallback, revokes, block reuse, orphan cleanup, large intents, journal full, abort, unmount, freeze, and synchronization. Corrupt every header field, length, feature, target, escape flag, checksum, revoke, commit, superblock, head, and tail.

Cut power or an emulated device at every descriptor, payload, dependency, flush, commit, home write, checkpoint, tail advance, replay write, and replay-completion point; repeat recovery interruptions. Test volatile-cache reorder and false completion. Verify directory, inode, allocation, quota, reference, orphan, checksum, and data-initialization invariants after every recovery. Preserve disk and journal images, geometry, UUIDs, options, device settings, seeds, I/O traces, replay decisions, raw results, and limitations. Named format, journal, storage, concurrency, recovery, security, application-durability, and independent-verification reviewers assess claims.
