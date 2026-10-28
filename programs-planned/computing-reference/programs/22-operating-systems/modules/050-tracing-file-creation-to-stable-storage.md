---
module_id: OS-050
program: Operating Systems
level: 1
module_number: 50
title: Tracing File Creation to Stable Storage
status: complete
last_verified: 2026-09-04
---

# Tracing File Creation to Stable Storage

## One-Page Review

### Governing question

What must happen between an application's request to create a file and a justified claim that the intended data, metadata, name, and replacement relationship will survive the declared failure model?

### Essential definitions

- **Creation** atomically resolves a final name and, when absent, allocates and links a new filesystem object under parent-directory authority.
- **Dirty state** is modified cached data or metadata that has not reached its required persistence boundary.
- **Delayed allocation** postpones choosing physical extents until writeback, enabling better placement while deferring space errors.
- **Writeback** transfers dirty cache state toward a backing device or server but does not alone define application durability.
- A **journal transaction** records protected updates and a commit boundary so recovery can avoid partially applied metadata transitions.
- A **flush** orders earlier device-cache writes toward nonvolatile media; **force unit access (FUA)** asks that a particular write reach the device's persistence domain.
- **`fsync`** requests file data and required metadata synchronization; a newly created or renamed directory entry can require separate synchronization of its containing directory.
- A **crash-consistency contract** specifies which recovered states are allowed after failure at each acknowledged boundary.

### Central model, mechanism, or theorem

Trace intent `I=(parent,name,content,metadata,replacement,failure_model)`. Safe publication normally uses a stable directory handle, exclusive private candidate creation, complete short-write handling, metadata finalization, file synchronization, atomic rename into the destination, directory synchronization, and error-preserving cleanup. Each success advances a contract state; no call is credited with a stronger guarantee than its interface and storage stack provide.

The full path crosses application buffers, syscall and VFS validation, dentries and inodes, page cache, allocation and quota, filesystem transactions, block queues, controller caches, and a declared persistence domain. Durability is end-to-end: one layer's completion cannot compensate for ignored errors, missing ordering, dishonest caches, unsafe power-loss behavior, or failure to persist the namespace entry.

### Critical invariants

- The created or replaced name resolves beneath the intended stable parent without a check-use race.
- File content, size, ownership, permissions, labels, and allocation describe one permitted version before publication.
- Every partial write and delayed allocation, quota, writeback, journal, device, and synchronization error is observed and retained.
- Required data reaches its dependency boundary before metadata is committed as referencing it.
- Atomic rename provides an allowed namespace transition, while directory synchronization supplies the distinct persistence obligation.
- Recovery exposes only states permitted by the filesystem mode and completed barriers; it never treats torn metadata as committed.
- Verification observes recovered bytes and metadata after an actual or faithfully modeled failure, not merely pre-crash cache state.

### Common failures

Common errors are creating at a checked pathname after resolution races, assuming one `write` transfers every byte, treating close as synchronization, ignoring delayed `ENOSPC`, equating writeback with stable storage, using rename as a durability barrier, synchronizing the file but not its new directory entry, trusting a device that lies about flushes, restoring privileged metadata before final content, and testing only graceful shutdown rather than abrupt failure and recovery.

### Compact example

To replace `config`, create an unnamed or unpredictable private candidate in the same filesystem, write and validate all bytes, apply ordinary metadata, synchronize the candidate, atomically rename it over `config`, then synchronize the containing directory. Before the file sync, new content can be missing or incomplete under the contract. After file sync but before rename, the old name remains authoritative. After rename but before directory sync, the live namespace shows new content but crash recovery may still expose an allowed old-or-new state. After directory sync succeeds, the workflow can claim the new named version under the stated local-filesystem and device assumptions.

### Connections

[OS-043](043-file-allocation.md), [OS-045](045-buffer-cache-and-page-cache.md), [OS-046](046-journaling.md), and [OS-047](047-crash-consistency.md) supply allocation, caching, transactions, and recovery. [OS-048](048-filesystem-permissions.md) and [OS-049](049-virtual-filesystem-layers.md) supply authorization and dispatch.

## Governing Question

“The write succeeded” is an incomplete statement. It can mean bytes entered a userspace buffer, crossed a system-call boundary, dirtied cached pages, reached a block queue, entered a volatile controller cache, or crossed a defined nonvolatile boundary. These moments have different failure consequences.

The governing question asks for an end-to-end trace and a precise claim at each acknowledgement. The design must connect namespace safety, object state, cache state, allocation, filesystem ordering, device persistence, recovery, and post-crash evidence.

## Why This Matters

Configuration replacement, database manifests, package installation, checkpoints, logs, and software updates depend on named data surviving failures. A structurally consistent filesystem can still recover an old application version or an empty newly named file if the application omitted required ordering.

Failures also arrive late. Delayed allocation can make an accepted write fail during writeback; a network server can reject space reservation at synchronization; a device can report an error after several requests have been merged. Losing the error creates false success.

This trace is a compact systems lesson. It connects APIs, concurrency, memory, security, storage, distributed acknowledgements, and testing, showing why no local optimization can be evaluated outside the complete contract.

## Prerequisites and Retrieval

Review [OS-003](003-system-calls-and-user-kernel-transitions.md), [OS-021](021-critical-sections-in-the-kernel.md), [OS-038](038-memory-mapped-files.md), [OS-041](041-files-directories-and-namespaces.md), [OS-042](042-inodes-and-metadata.md), [OS-043](043-file-allocation.md), [OS-045](045-buffer-cache-and-page-cache.md), [OS-046](046-journaling.md), [OS-047](047-crash-consistency.md), [OS-048](048-filesystem-permissions.md), and [OS-049](049-virtual-filesystem-layers.md).

Retrieve these distinctions:

- pathname resolution and object use must be coupled when another actor can mutate names;
- directory entries and inodes are different metadata with different persistence needs;
- a successful short write is progress, not completion of the requested buffer;
- dirty page-cache bytes are visible to local reads before they are persistent;
- logical allocation, physical extent selection, and durable allocation metadata can occur at different times;
- journal commit, checkpoint to home locations, device-cache completion, and stable media are distinct;
- atomic visibility under rename does not itself imply post-crash durability;
- a filesystem guarantee is conditional on lower layers honoring ordering and flush contracts.

## Learning Objectives

After this module, you should be able to:

1. trace secure create and replacement requests through VFS, caches, allocation, journaling, queues, and devices;
2. distinguish write acceptance, writeback, file synchronization, directory synchronization, and media persistence;
3. explain delayed allocation, partial writes, retained errors, and reservation failures;
4. derive ordering constraints among data, inode metadata, journal commits, rename, and directory persistence;
5. design crash-safe create-new, replace-existing, append-log, and multi-file publication workflows;
6. adapt claims for copy-on-write, direct-I/O, memory-mapped, remote, and persistent-memory storage;
7. test crash points and recovered states with evidence sufficient for an explicit failure model.

## Core Exposition

### Define the durability claim

Start with the failure model. A process crash preserves kernel state; a kernel panic can lose volatile kernel caches; sudden power loss can lose CPU, memory, controller, and device volatile state; media failure can destroy acknowledged sectors; distributed partition can leave server status uncertain.

“Durable” must name which failures are covered, which persistence domain is trusted, and whether old or new state is acceptable. Replication, backup, and media redundancy are separate from local write ordering.

### Capture application intent

Intent includes the parent directory, final name, bytes, expected ownership and permissions, replacement rule, concurrent-writer policy, and completion point. It should state whether an existing file may be overwritten and whether readers may observe an intermediate version.

Multi-file invariants require a transaction protocol above ordinary single-name rename. The filesystem cannot infer that two independently synchronized files form one application unit.

### Resolve a stable parent

Open a trusted directory and perform handle-relative operations beneath it with explicit symbolic-link, mount-crossing, and escape rules. This binds creation to a stable namespace object rather than repeating an attacker-controlled absolute pathname.

The kernel checks search and write authority on the actual parent, sticky and mount policy where relevant, credentials, quotas, and security hooks. A preflight permission check cannot authorize a later resolution safely.

### Select create semantics

Exclusive creation prevents accidental replacement. A private unpredictable temporary name can support later atomic publication. An unnamed temporary inode, where supported, avoids exposing an intermediate name and is linked only after complete preparation.

The candidate normally resides in the target filesystem so the final rename remains an atomic same-filesystem namespace operation. Cross-filesystem rename fails rather than silently becoming a copy with different failure semantics.

### Allocate the in-memory object

VFS lookup obtains a negative final dentry or an atomic-open path. The filesystem allocates an inode identity, initializes type and ownership, derives mode and ACL state, charges quotas, and prepares directory and allocation metadata under locks and a transaction where applicable.

Publication must not expose a half-initialized inode. On error, reservations, references, transaction credits, and private candidates are released without deleting unrelated names.

### Establish initial metadata

Creation derives owner, group, permissions, default ACLs, timestamps, and security labels from parent, credentials, requested mode, umask, mount idmapping, and policy. These are part of the object's state, not ornamental fields.

Create with least privilege. Content or ownership changes can clear set-ID bits and file capabilities; privileged executable metadata is deliberately applied only after trusted content and ordinary metadata are final.

### Return the open file

The successful syscall installs a descriptor for one open file description. The descriptor pins the object even if its temporary name is removed, and later writes use the opened identity rather than re-resolving the path.

Close-on-exec should be requested atomically when needed. Leaked descriptors can expose authority or keep deletion, unmount, and storage reclamation from completing.

### Copy from application memory

A write validates descriptor mode, offset or append semantics, length, limits, seals, and credentials, then copies or pins user bytes under the selected I/O path. Signals, faults, limits, and capacity can yield partial progress.

The application advances by the returned count and retries only the remainder under its interruption policy. Reissuing the whole buffer after a short write duplicates data.

### Enter the page cache

Buffered writes locate or allocate cache pages, copy bytes, mark affected regions uptodate and dirty under the mapping contract, update inode size and timestamps, and charge dirty-memory accounting. Local reads can now observe new data.

This success often acknowledges volatile kernel state. Memory pressure, background thresholds, age, explicit synchronization, or filesystem policy later initiates writeback.

### Reserve space and quota

Some filesystems reserve enough resources at write time; others use delayed allocation and choose extents during writeback. Delayed allocation improves contiguity and reduces metadata work but moves `ENOSPC`, quota, or allocation failure later.

A robust workflow keeps sufficient reservation guarantees or treats synchronization as the authoritative completion point. It does not discard errors because the earlier write returned its byte count.

### Map logical ranges to extents

During allocation, the filesystem maps logical file offsets to physical blocks, extents, object-store keys, or remote ranges. Sparse holes need no physical data until written; unwritten extents can reserve space without exposing stale disk contents.

Allocation updates free-space indexes, extent trees, inode size or block counts, and quota state. These metadata dependencies must be recoverable together.

### Start writeback

Writeback selects dirty ranges, locks or stabilizes pages, allocates storage as needed, constructs I/O requests, marks work in progress, and submits data toward the backing layer. Concurrent writes can redirty a page while earlier content is in flight.

Completion clears only the state actually written. Failure retains or records an error and leaves data eligible for retry or explicit failure handling under the filesystem contract.

### Build block requests

The block layer can split, merge, queue, prioritize, and remap requests through partitions, encryption, volume managers, and device drivers. Each layer must preserve sector ranges, dependency order, completion, and error propagation.

Checksums or encryption add metadata and ordering. A data request completing before its integrity metadata can be unsafe unless the format and recovery rules tolerate that state.

### Device caches and persistence domains

A device may acknowledge a write after placing data in volatile cache. Cache flushes request that prior writes reach the declared persistence domain; FUA can request nonvolatile completion for a particular command. Ordering features are useful only when every layer forwards them correctly.

Power-loss protection can expand the trustworthy persistence domain, but it is a hardware and configuration claim requiring evidence. Disabling barriers on unsupported assumptions trades correctness for apparent speed.

### Filesystem transaction dependencies

A journaling filesystem groups protected metadata changes into transactions. Descriptors and payload blocks are written before a commit record; recovery replays only transactions meeting validity and commit rules.

In ordered-data modes, file data needed by newly committed metadata is issued before that metadata commit. In metadata-only writeback modes, recovery can preserve structure without guaranteeing the new file bytes. Full data journaling provides stronger ordering at additional I/O cost.

### Journal commit and checkpoint

Commit makes a transaction recoverable from the journal after required ordering and flushes. Checkpoint later copies journaled metadata to home locations and eventually permits journal-space reuse.

An application normally cares that recovery can reconstruct its state, not that every metadata block already occupies its final home location. Confusing commit with checkpoint creates unnecessary latency or incorrect recovery reasoning.

### File synchronization

`fsync(file)` requests dirty file data and associated metadata needed by its contract to reach the backing storage, then waits and reports errors. `fdatasync` can omit metadata not required for later data retrieval while still persisting size changes needed to read appended bytes.

Synchronization includes previously deferred allocation and can therefore report space or quota failures. It also surfaces retained writeback errors associated with the open or mapping under implementation rules.

### Why close is different

Close releases an application reference and may initiate work, but portable crash-safe design does not treat it as a persistence barrier. Some errors can appear on close, yet close success still need not mean stable media.

Applications must check close where the interface can report errors, while using the explicit synchronization operation required by their durability protocol.

### Atomic rename publication

Same-filesystem rename can atomically replace a destination so concurrent resolvers observe an allowed old or new binding rather than a missing middle state. Existing open descriptors continue to identify their old objects.

Atomic visibility says nothing by itself about which namespace binding survives a crash. The rename's directory metadata must enter the filesystem's persistent recovery state.

### Directory synchronization

Synchronizing the candidate file does not necessarily persist the directory entry that names it. After create, link, unlink, or rename, open and synchronize every containing directory required by the operation and filesystem contract.

A replacement across two directories changes both namespace objects and can require both directory handles. The exact guarantee is filesystem and platform specific, so the protocol records its dependencies rather than relying on folklore.

### Safe replacement protocol

Open the target directory, create a private candidate without following an attacker-controlled final object, write every byte, validate content, set ordinary metadata, synchronize the candidate, atomically rename it to the destination, then synchronize the directory. Only then acknowledge durable publication under the declared contract.

If a crash occurs earlier, recovery may expose the old file, a private candidate, or another state explicitly allowed at that barrier. Cleanup after restart handles orphaned candidates without guessing that their content is complete.

### Create-new protocol

For a new name that must persist, exclusive creation and writing are followed by file synchronization and parent-directory synchronization. If readers must not see incomplete content, use a private candidate and link or rename only after file preparation.

The application decides whether a leftover private candidate is safe to remove, resume, or quarantine. A recognizable record format with version and checksum supports that decision.

### Append-log protocol

Atomic append positioning prevents overlapping offsets under supported concurrent-writer semantics, but record integrity also needs framing, length bounds, checksum, and a commit rule. One large write is not universally an indivisible record.

Batch synchronization amortizes latency and defines a loss window. The acknowledgement returned to each producer must match whether its batch has actually crossed the required persistence boundary.

### Memory-mapped writes

Mapped stores dirty page-cache state through memory faults rather than ordinary write calls. `msync` and file synchronization have distinct interfaces and platform details; truncation and concurrent mapping writeback add races.

CPU cache persistence for direct-access memory can require architecture-specific flush and ordering instructions. Ordinary block-device assumptions cannot simply be transplanted to byte-addressable persistent memory.

### Direct and synchronous I/O

Direct I/O reduces or bypasses page-cache data movement but still has alignment, metadata, allocation, device-cache, and concurrency obligations. It does not automatically make a write durable.

Synchronous open flags request defined data- or file-integrity completion for each write. They simplify the caller protocol at latency cost and still depend on filesystem and device compliance.

### Copy-on-write filesystems

A copy-on-write filesystem writes new blocks and later switches parent or root pointers. Checksums and transactional trees can detect or avoid torn in-place metadata, but ordering and device persistence remain necessary.

Snapshots preserve earlier roots but are not automatically independent backups. Data referenced by a newly durable root must itself be durable, and redundancy cannot correct every software or correlated-device failure.

### Remote filesystems

A client write may be stable only in client memory, server memory, server nonvolatile cache, or replicated storage. Protocol acknowledgements and stability classes define which boundary was reached; reconnect and replay logic handle uncertain completion.

Client `fsync` must map to the server protocol's commit semantics. Local directory synchronization cannot create a guarantee stronger than the server and backing system advertise.

### Error preservation

Track the first or relevant error without overwriting it during cleanup. Distinguish write progress, allocation failure, synchronization failure, rename failure, directory synchronization failure, and candidate cleanup failure.

After uncertain synchronization, retry may be safe, unnecessary, or insufficient depending on state. Verification or a higher-level transaction identifier can resolve ambiguity; silently acknowledging is never valid.

### Crash recovery

Recovery validates journal records, checksums, generations, or copy-on-write roots and selects a consistent committed state. It replays or rolls back according to the filesystem design, then repairs allocation and orphan state as specified.

Filesystem consistency does not prove application transaction consistency. The application validates version, length, checksum, sequence, and cross-file relationships before accepting recovered content.

### Observability

Trace stable parent and inode identities, write ranges and returned counts, dirty and writeback transitions, allocation, transaction identifiers, block completions, flushes, file and directory synchronization, rename, errors, and recovery selection.

Instrumentation distinguishes request submission from durable completion and records mount, filesystem mode, storage topology, volatile-cache settings, and clock basis. Sensitive names and content are minimized.

### Testing and assurance

Place controlled crash points after creation, each partial write, allocation, data submission, journal payload, flush, commit, file sync, rename, and directory sync. Reboot or remount, run recovery, bypass warm caches where required, and inspect actual bytes and metadata.

Vary filesystems, mount modes, queue depth, memory pressure, capacity, quota, device cache, power-loss behavior, and concurrent readers and writers. Retain seeds, traces, images, recovered state, hashes, hardware details, and limitations.

Assurance names application-protocol, VFS, filesystem, block-layer, device, hardware, security, concurrency, recovery, and independent-verification reviewers. A graceful-shutdown test or successful `fsync` call without recovered-state evidence is not certification.

## Definitions and Notation

Let intended version `V=(D,N,B,M)` contain parent directory object `D`, final name `N`, byte string `B`, and required metadata `M`. Let storage path `L=(page_cache,filesystem,journal,block_stack,device,persistence_domain)`.

Let events be `c` candidate creation, `w` completion of all application writes, `a` physical allocation, `d` required data persistence, `m` required inode-metadata persistence, `r` atomic rename publication, and `q` required directory persistence. A common replacement dependency is `w -> d,m -> r -> q`, where an implementation can batch internal work but cannot violate the observable recovery contract.

Define acknowledgement level `A_k` as the strongest completed and successfully reported barrier. Recovered state set `Recover(A_k,F)` depends on filesystem mode and failure model `F`. A durability claim is sound only if every state in that set satisfies the application's accepted outcome predicate.

Let `E_write`, `E_wb`, `E_file_sync`, `E_rename`, and `E_dir_sync` be errors at write, writeback, file synchronization, rename, and directory synchronization. Success requires handling the returned byte count and proving none of the required error channels was discarded.

## Mechanisms, Invariants, or Proof Structure

1. **Declare failure and outcome.** Name the persistence domain and allowed recovered versions before selecting APIs.
2. **Bind the namespace.** Resolve a trusted parent once and use handle-relative, no-escape creation and replacement operations.
3. **Create privately.** Allocate an exclusive candidate in the destination filesystem with restrictive initial authority.
4. **Complete content.** Handle short writes, interruptions, size limits, checksums, allocation, quota, and mapping interactions.
5. **Finalize metadata.** Apply approved ownership, permissions, ACLs, labels, timestamps, and privilege state in dependency order.
6. **Synchronize the object.** Persist required data, allocation, size, inode metadata, and retained errors through the declared device boundary.
7. **Publish atomically.** Rename or link under the intended concurrent-writer policy without a missing or partial destination state.
8. **Synchronize the namespace.** Persist affected directory entries and parent metadata before durable acknowledgement.
9. **Propagate every failure.** Preserve partial progress and errors from application, filesystem, block, device, and cleanup boundaries.
10. **Recover by contract.** Replay, roll back, or select roots, then validate application version, length, checksum, and relationships.
11. **Test real crash points.** Cut power or faithfully inject failure at every dependency boundary and inspect cold recovered state.
12. **Retain evidence.** Record code, kernel, filesystem, mode, topology, hardware, flush behavior, traces, images, outcomes, and limitations.

<!-- bijux-verify: {"id":"replacement-crash-boundaries","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"after=create-candidate recovered=old\nafter=write-content recovered=old\nafter=file-fsync recovered=old\nafter=rename recovered=old-or-new\nafter=directory-fsync recovered=new\n","stderr":""}} -->
```python
states = (
    ("create-candidate", "old"),
    ("write-content", "old"),
    ("file-fsync", "old"),
    ("rename", "old-or-new"),
    ("directory-fsync", "new"),
)

for completed_action, allowed_recovery in states:
    print(f"after={completed_action} recovered={allowed_recovery}")
```

The executable table demonstrates one deliberately conservative replacement contract. It does not execute system calls, crash a machine, model a particular filesystem, prove that old data survives every failure, or test real storage persistence.

## Alternatives and Trade-Offs

- In-place overwrite uses less space but exposes torn or mixed content; private-candidate rename provides atomic visibility at extra allocation and metadata cost.
- Unnamed temporary files reduce intermediate namespace exposure but are not universally supported; named candidates improve portability and require secure naming and cleanup.
- Delayed allocation improves layout and batching but defers space errors; early reservation gives earlier certainty and can fragment or overreserve.
- Buffered I/O improves cache reuse and aggregation but separates acceptance from persistence; direct I/O reduces copying while retaining alignment and metadata obligations.
- Per-write synchronization simplifies acknowledgement but increases latency; group commit improves throughput and enlarges the admitted loss window.
- Metadata journaling reduces journal bandwidth but needs data-ordering discipline; data journaling strengthens recovery at higher write amplification.
- Copy-on-write avoids overwriting committed trees but consumes new space and depends on parent-pointer and device ordering.
- File-only synchronization is cheaper but may omit a new name; directory synchronization closes that gap at additional latency.
- Strict device flushes protect volatile caches but cost performance; power-loss-protected hardware can reduce that cost only with verified configuration.
- Checksums detect corruption but do not guarantee freshness or repair; replication can repair some faults and introduces acknowledgement and quorum semantics.
- Application transaction logs coordinate multi-file state but duplicate protocol work; relying on single-file atomic replacement is simpler and narrower.
- Fault injection is reproducible but approximates real failure; physical power-cut testing is stronger and more expensive and hazardous.

## Failure Modes and Misconceptions

- **“Create success means the name is durable.”** It can establish only live in-memory namespace state.
- **“One write transfers the whole buffer.”** Short writes and interruptions require explicit progress handling.
- **“The page cache is stable storage.”** It is normally volatile kernel-managed state.
- **“Writeback success equals application commit.”** Namespace and other metadata barriers can remain.
- **“Close is equivalent to `fsync`.”** Portable crash-safe protocols use the explicit synchronization contract.
- **“`fsync(file)` persists a newly created name.”** The containing directory can require separate synchronization.
- **“Rename makes the replacement durable.”** It supplies atomic namespace visibility, not necessarily crash persistence.
- **“A journal contains all file data.”** Metadata-only and ordered modes have narrower data behavior.
- **“Journal commit means blocks reached home locations.”** Recovery can replay a committed transaction before checkpoint.
- **“Successful writes cannot later get `ENOSPC`.”** Delayed allocation can surface capacity failure during writeback or sync.
- **“Direct I/O is automatically durable.”** Device cache, metadata, ordering, and synchronous flags still matter.
- **“A flush always reaches nonvolatile media.”** Every layer and device must implement the advertised contract honestly.
- **“Filesystem consistency proves application consistency.”** Application versions and multi-file invariants need their own protocol.
- **“A clean reboot tests crash safety.”** It drains caches and avoids the failure window under study.

## Worked Examples

### Example 1

A configuration writer creates `.config.private`, loops until every byte is written, verifies a checksum, synchronizes the file, renames it over `config`, and synchronizes the directory before acknowledging.

### Example 2

A 1 MiB write returns 640 KiB because a signal arrives. The caller advances its buffer and offset by 640 KiB; replaying all 1 MiB would duplicate the prefix.

### Example 3

Delayed allocation accepts dirty pages while free space appears available. Concurrent consumers exhaust capacity, and `fsync` reports `ENOSPC`; the application must not publish success.

### Example 4

An ordered journaling mode writes new file data before committing metadata that points to it. Recovery avoids exposing metadata that references unwritten stale blocks, though application durability still requires synchronization.

### Example 5

The file candidate is synchronized and then renamed, but the directory is not synchronized. Live readers see the new file; after power loss, the documented recovered set can still permit the old binding.

### Example 6

A block device acknowledges data into volatile cache. The filesystem submits a flush before the journal commit record and uses ordered completion; without truthful flush support, the recovery proof fails.

### Example 7

An append log synchronizes every 100 records. Each record has length, sequence, payload, and checksum; recovery scans until the last complete valid record, and acknowledgements state which batch was durable.

### Example 8

A memory-mapped database changes pages and calls only ordinary file close. The process exits cleanly, but its intended transaction boundary is undefined; it must use the documented mapping and file synchronization protocol.

### Example 9

A remote client receives an unstable write acknowledgement, then loses the connection before commit. On reconnect it uses request identity and server state to resolve uncertainty instead of blindly reporting success.

### Example 10

A crash injector stops the machine after directory sync returns. Recovery mounts the raw image, reads the named file from a cold path, and verifies identity, length, content checksum, mode, and expected absence of the private candidate.

## Cross-Program Connections

[Computer Architecture](../../23-computer-architecture/ROADMAP.md) connects memory ordering, DMA, controller caches, nonvolatile domains, and cache flush instructions. [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) connects extent trees, free-space indexes, journals, checksums, and copy-on-write roots.

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) connects acknowledgement levels, uncertain completion, replication, idempotency, leases, and recovery. [Security Engineering](../../25-security-engineering/ROADMAP.md) connects safe path resolution, least-privilege creation, labels, capabilities, integrity, and adversarial replacement.

[Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies end-to-end requirements, dependency analysis, fault injection, traceability, and evidence. Within this program, [OS-061](../ROADMAP.md) begins device and driver depth, while [OS-065](../ROADMAP.md) and [OS-068](../ROADMAP.md) deepen scheduling and NVMe queues.

## References

- Linux man-pages project, [open(2)](https://man7.org/linux/man-pages/man2/open.2.html), current page checked 2026-09-04. Creation, exclusive and temporary files, synchronized I/O flags, descriptors, errors, and pathname-relative operation.
- Linux man-pages project, [write(2)](https://man7.org/linux/man-pages/man2/write.2.html), current page checked 2026-09-04. Partial writes, interruptions, append behavior, delayed errors, and the distinction between successful write and disk commitment.
- Linux man-pages project, [fsync(2)](https://man7.org/linux/man-pages/man2/fsync.2.html), current page checked 2026-09-04. File and data synchronization, metadata, device caches, delayed errors, and separate directory synchronization.
- Linux man-pages project, [rename(2)](https://man7.org/linux/man-pages/man2/rename.2.html), current page checked 2026-09-04. Atomic replacement, open descriptors, same-object behavior, cross-filesystem errors, and rename variants.
- Linux man-pages project, [msync(2)](https://man7.org/linux/man-pages/man2/msync.2.html), current page checked 2026-09-04. Synchronization of memory-mapped file ranges, flags, alignment, and errors.
- Linux kernel documentation, [Overview of the Linux Virtual File System](https://docs.kernel.org/filesystems/vfs.html), current page checked 2026-09-04. VFS objects, creation and rename hooks, address-space operations, writeback, synchronization, and lifecycle.
- Linux kernel documentation, [ext4 Journal](https://docs.kernel.org/filesystems/ext4/journal.html), current page checked 2026-09-04. JBD2 records, commits, replay, checkpoints, data modes, checksums, barriers, and fast commits.
- Linux kernel documentation, [ext4 Allocators](https://docs.kernel.org/filesystems/ext4/allocators.html), current page checked 2026-09-04. Block and inode allocation, delayed allocation, multiblock allocation, and free-space structures.
- Linux kernel documentation, [Writeback Cache Control](https://docs.kernel.org/block/writeback_cache_control.html), current page checked 2026-09-04. Volatile write caches, flush requests, FUA, ordering, queue capabilities, and device contracts.
- Linux kernel documentation, [Direct Access for Files](https://docs.kernel.org/filesystems/dax.html), current page checked 2026-09-04. Direct mappings, cache flush and invalidation interactions, filesystem support, and persistent-memory access.

## Exercises

### Exercise 1

Specify crash-safe protocols for creating a new visible file and atomically replacing an existing file. Give allowed recovered states after every syscall boundary.

### Exercise 2

Trace one buffered extending write from user memory through allocation, journaling, block submission, device cache, `fsync`, and recovery. Account for every error.

### Exercise 3

Compare ordered metadata journaling, data journaling, and copy-on-write publication for new file data. State what each mechanism does and does not prove.

### Exercise 4

Design a durable append log and a two-file generation update for local and remote storage. Define acknowledgement, checksums, concurrency, and uncertain completion.

### Exercise 5

Build a crash-test and assurance plan for the replacement workflow. Include namespace attacks, capacity faults, dishonest caches, cold recovery, and evidence.

## Answers to the Exercises

### Answer 1

For create-new without early visibility, open the trusted parent, create a private same-filesystem candidate exclusively, write and validate all bytes, finalize approved metadata, synchronize the file, link or rename to the final absent name under a no-replace rule, and synchronize the parent directory. Before publication, recovery may show no final name and possibly an orphan or private candidate. After publication but before parent sync, live state contains the new name while the documented crash contract can permit absence. After successful directory sync, require the complete new named version under the declared device assumptions.

For replacement, use the same candidate preparation, synchronize it, atomically rename over the destination, then synchronize affected directories. Before rename, the old name must remain the accepted version. After rename but before directory sync, accept old or complete new according to the conservative contract, never a partially written new version. After directory sync, require new. At every error, retain old when possible, never acknowledge, and clean a candidate only through its stable handle or verified private name.

### Answer 2

The syscall copies a returned count from user memory into cache pages, updates inode size and timestamps, charges dirty memory, and can stop on a fault, signal, limit, or immediate space policy. Delayed allocation may reserve approximately or wait until writeback. Writeback locks ranges, chooses extents, charges exact blocks and quota, records allocation and inode metadata in a transaction, and submits data requests. It retains allocation, quota, checksum, mapping, and I/O errors.

The block stack splits, merges, remaps, encrypts, and queues requests while preserving range and order. The device can acknowledge volatile cache before media. The filesystem orders required data before protected metadata, submits journal payload and commit with flush or FUA semantics, and later checkpoints. `fsync` waits for required data and metadata, forces commit and device persistence under its contract, and reports retained failures including delayed `ENOSPC`. Recovery validates committed transactions and reconstructs allocation, size, and content; application verification checks length and checksum. No earlier layer's success erases a later error.

### Answer 3

Ordered metadata journaling records metadata and ensures relevant new data is issued before committing metadata that references it. It protects structural consistency and avoids exposing stale blocks through newly committed mappings, but not every application-level update without synchronization. Data journaling records both file data and metadata through the journal, strengthening atomic recovery and increasing write amplification and journal pressure.

Copy-on-write writes new data and metadata blocks and atomically advances a durable parent or root pointer, retaining the previous tree until the switch. It avoids torn in-place updates and supports snapshots, but needs free space, correct reference accounting, checksums or validation, device ordering, and a synchronized publication point. None of the three automatically coordinates independent application files, defeats dishonest device caches, provides backup, or makes an unsynchronized rename durable.

### Answer 4

Frame each log record with version, length, monotonically scoped sequence, payload, and checksum. Serialize or allocate append positions under documented atomicity, handle short writes, and synchronize batches. A producer receives durable acknowledgement only after its batch's commit barrier; recovery accepts complete valid records through the last committed sequence and ignores a torn suffix.

For two files, write immutable generation-stamped candidates, synchronize both, and then atomically replace one small manifest that names their generation; synchronize the manifest and its directory. Readers validate matching generations and checksums. On remote storage, map each barrier to server stable-write or transaction semantics, use idempotent request IDs, and resolve connection-loss uncertainty by querying the manifest generation. A local cache acknowledgement cannot be upgraded to remote durable success.

### Answer 5

Use a hostile directory and race symlink, rename, mount, and replacement attempts against stable-handle resolution. Inject short writes, signals, memory pressure, quota and space exhaustion, allocation failures, writeback errors, journal checksum failures, dropped flushes, reordering, device resets, and candidate-cleanup failures. Crash after candidate allocation, each write prefix, metadata update, data submission, journal payload, commit request, file sync return, rename, and directory sync return.

For each cut, boot or remount from an independently captured image, allow filesystem recovery, bypass warm caches, and verify final name, stable object identity where available, exact bytes, length, checksum, ownership, mode, ACL, label, privilege metadata, private-candidate state, allocation integrity, and unrelated files. Test verified power-loss-protected and deliberately volatile or dishonest cache configurations. Preserve source revision, kernel, filesystem and mount mode, hardware and firmware, topology, workload seed, crash point, syscall and block traces, journal or image snapshots, recovery logs, raw outcomes, and limitations for named application, VFS, filesystem, storage, hardware, security, concurrency, recovery, and independent reviewers.
