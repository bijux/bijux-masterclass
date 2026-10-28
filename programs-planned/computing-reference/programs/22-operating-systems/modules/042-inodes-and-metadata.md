---
module_id: OS-042
program: Operating Systems
level: 1
module_number: 42
title: Inodes and Metadata
status: complete
last_verified: 2026-09-04
---

# Inodes and Metadata

## One-Page Review

### Governing question

How should an operating system represent, cache, authorize, mutate, expose, and persist filesystem-object metadata while preserving identity, reference lifetimes, concurrency semantics, and crash-recovery invariants?

### Essential definitions

- An **inode** is a filesystem object's metadata-bearing identity within a filesystem; it is not a pathname or directory entry.
- A **dentry** is an in-memory name-to-object lookup result, while a directory entry is the filesystem namespace record.
- An **inode number** identifies an allocation slot within a filesystem, but may be reused after reclamation.
- A **generation** or version distinguishes successive occupants of a reused identifier when the filesystem supports it.
- **Logical size** is the byte offset after the last logical byte; **allocated space** records storage charged or mapped and need not equal logical size.
- **Extended attributes** are named metadata values outside the fixed inode fields; ACLs and security labels can be represented through them.
- **Dirty metadata** has changed in memory but is not necessarily durable on stable storage.

### Central model, mechanism, or theorem

Model object identity as `I=(F,n,g)`: filesystem instance `F`, inode number `n`, and generation `g`. Its state at logical time `t` is `M_I(t)=(type,mode,owner,links,size,blocks,times,flags,attributes,mapping,...)`. Names refer to `I`; open files, mappings, and kernel references can preserve `I` after its last name disappears.

A metadata read is an observation governed by an API contract, cache protocol, and concurrency rules. It need not be a transactionally simultaneous snapshot of every field. A metadata mutation must authorize the requested transition, serialize conflicting state, preserve cross-field invariants, mark the correct records dirty, and participate in the filesystem's ordering and recovery protocol. Return from a syscall proves only the contract that syscall documents—not necessarily stable-storage durability.

### Critical invariants

- A pathname, dentry, descriptor, inode number, and full object identity are never treated as interchangeable.
- Every live namespace reference and open reference points to an allocated object of the expected generation.
- Link count and namespace changes remain balanced under success, failure, replay, and recovery.
- Type, size, block mapping, allocated-space accounting, quotas, and timestamps obey filesystem-specific cross-field rules.
- Permission, ACL, label, immutable, append-only, and ownership policy is checked before an authorized metadata transition becomes visible.
- Concurrent readers receive at least the API's documented field and freshness guarantees; stronger snapshot claims require stronger synchronization.
- Dirty metadata becomes durable only through the declared writeback, journal, flush, and directory-persistence protocol.

### Common failures

Common mistakes are using inode number alone as a permanent global ID, treating `ctime` as creation time, equating size with allocated bytes, assuming one `stat` result is a globally atomic snapshot, trusting cached remote attributes indefinitely, updating ACLs without their mode-bit relationship, reclaiming an unlinked but open object, interpreting mapped owners without mount context, and assuming file synchronization also persists a newly created directory entry.

### Compact example

A sparse one-megabyte file has identity `(fs7,42,3)` but only 8 KiB allocated. Removing its last directory entry changes link count to zero without invalidating an existing open reference. Only after that reference closes can the filesystem reclaim the object; if inode number 42 is later reused, a changed generation prevents a stale handle from silently naming the new object.

### Connections

[OS-039](039-shared-pages-and-page-cache.md) explains shared cached data, and [OS-041](041-files-directories-and-namespaces.md) separates names from objects. [OS-043](../ROADMAP.md) through [OS-050](../ROADMAP.md) build allocation, directories, links, mounting, consistency, and VFS design on inode metadata.

## Governing Question

Metadata appears to be a collection of fields returned by `stat`, but each field participates in identity, authorization, accounting, caching, synchronization, or recovery. Some state is fixed-format on disk, some is variable-length, some exists only in memory, and some is synthesized by a remote or virtual filesystem.

The governing question is how to maintain one coherent object abstraction across those representations. The answer requires explicit identity scope, per-operation consistency, cross-field invariants, lifecycle references, and a durability contract.

## Why This Matters

Programs use metadata to decide whether an object is safe to open, executable, writable, billable, backed up, indexed, synchronized, or eligible for deletion. Kernel subsystems use it to locate blocks, enforce access, reclaim caches, account quotas, and recover after failure.

Incorrect reasoning creates security and reliability defects. A check-then-use race can authorize one object and mutate another. A stale network attribute can conceal revoked permissions. Confusing logical size with allocation can defeat capacity planning, while premature inode reuse can redirect stale handles.

Metadata is also part of the persistent format. Field width, byte order, feature flags, checksums, and versioning determine whether old and new implementations can interpret the same storage safely.

## Prerequisites and Retrieval

Review [OS-021](021-critical-sections-in-the-kernel.md), [OS-024](024-atomic-operations.md), [OS-037](037-copy-on-write.md), [OS-039](039-shared-pages-and-page-cache.md), and [OS-041](041-files-directories-and-namespaces.md).

Retrieve these distinctions:

- a pathname names an object through a directory relation; it is not object identity;
- a VFS inode is an in-memory object, while a disk inode is one filesystem's persistent encoding;
- hard-link count measures namespace references under filesystem rules, not all live references;
- logical size, allocated units, reserved space, shared extents, and physical bytes are different quantities;
- `mtime` tracks content modification, `ctime` tracks inode-status change, `atime` tracks access, and birth time is a separate optional field;
- mode bits, ACLs, extended attributes, security labels, mount options, and credentials jointly influence access;
- syscall completion, writeback completion, journal commitment, device-cache flush, and recoverability are distinct events;
- a cached metadata read has an explicit or implicit freshness policy.

## Learning Objectives

After this module, you should be able to:

1. distinguish pathnames, directory entries, dentries, inode numbers, generations, open files, and persistent inode records;
2. interpret common metadata fields without confusing logical, allocated, cached, or durable state;
3. reason about link counts, open references, deletion, orphan handling, reclamation, and identifier reuse;
4. design permission, ownership, ACL, extended-attribute, timestamp, quota, and flag transitions;
5. specify concurrency and consistency contracts for metadata reads and writes;
6. construct writeback, synchronization, journaling, and crash-recovery obligations for metadata;
7. test local, remote, virtual, corrupted, and version-skewed metadata behavior.

## Core Exposition

### Names and object identity

A directory entry binds a component name to a filesystem object. Hard links create multiple such bindings. The inode carries object state shared by all hard-linked names, so changing mode or size through one name is visible through the others.

Object identity is scoped to a filesystem instance. An inode number such as 42 is meaningless without that scope and can be recycled after deletion. Stable external handles add a generation or equivalent validation token.

### VFS inode and disk inode

The Linux VFS inode is an in-memory abstraction used across filesystem implementations. A block filesystem may instantiate it from a persistent inode table or tree; a pseudo-filesystem can synthesize it without a disk record.

Do not assume the in-memory structure is the disk format. They differ in layout, lifetime, locking, cached state, and extensibility. Filesystem code translates between them and controls writeback.

### Inode cache lifecycle

Lookup can find an existing cached inode or read and instantiate one. Open files and dentries retain references, while cache reclaim can evict an inactive inode. Eviction must release private state without losing dirty changes or live references.

The cache accelerates access but is not an independent authority. Local mutation, remote invalidation, and filesystem revalidation determine when cached fields may be used.

### Type and mode

Mode commonly combines object type with owner, group, and other permission bits plus special bits. Types include regular file, directory, symbolic link, FIFO, socket, character device, and block device.

Some directory-entry formats cache a type hint for faster traversal. That hint must agree with authoritative object state or be treated as unknown; it does not turn the directory entry into the inode.

### Ownership and credential context

Owner and group identifiers are interpreted through the caller's credential and mount context. An idmapped mount can present a mapping between filesystem ownership and userspace-visible IDs without rewriting every persistent inode.

Authorization therefore cannot compare raw integers without the applicable mapping. Creation, `chown`, set-ID clearing, and quota charging need one explicit mapping model.

### Permission bits and ACLs

Traditional access checks combine effective credentials, object owner, group membership, and mode bits. POSIX ACLs add named-user and named-group entries plus a mask that constrains applicable group-class permissions.

Changing a file's mode can transform or constrain its ACL. Implementations must update the representations consistently so a stale ACL does not silently restore permission removed through mode bits.

### Extended attributes

Extended attributes associate names and byte values with an object. Linux namespaces such as `user`, `trusted`, `security`, and `system` have different access and interpretation rules.

Values can hold ACL encodings, security labels, capabilities, origin data, or application metadata. Bound names and values, validate namespaces, account storage, and make multi-record updates recoverable.

### Security labels and capabilities

Mandatory-access-control labels and file capabilities may live in extended attributes but are kernel-interpreted authority, not inert application tags. Copy, archive, restore, and overlay operations must decide whether and how to preserve them.

Untrusted callers must not be allowed to manufacture privileged labels or capabilities merely because an interface can set arbitrary bytes.

### Link count

The link count records directory references according to filesystem semantics. Adding or removing a hard link changes both a directory record and the target count as one recoverable logical operation.

Directory counts can encode topology-specific relationships or use a sentinel when an exact count exceeds a format's capacity. Code uses the filesystem contract rather than assuming one universal directory formula.

### Open-unlinked objects

When the final name is removed, link count becomes zero but an open file, mapping, current directory, or internal reference can keep the inode alive. Existing handles continue to address that object even though new pathname lookup cannot find it.

The filesystem records or reconstructs orphan state so a crash cannot leak blocks or free storage still required by recovery. Reclamation occurs only at the terminal lifetime predicate.

### Inode reuse and generation

After complete reclamation, an inode number can return to the free pool. Reuse is safe for ordinary fresh lookup but dangerous for stale file handles or caches that remember only the number.

A generation value changes across reuse and is validated with the filesystem identity. Generation width, wraparound, restore, snapshot, and server reboot behavior still need an explicit threat model.

### Logical size

For a regular file, size usually identifies the logical end offset. A write beyond end can create a hole; truncation can reduce the logical range and discard or defer mapped storage.

Directories, symbolic links, devices, and virtual filesystems can assign different meanings. Never infer exact physical storage or valid read behavior from `size` alone.

### Allocated space and block counts

Metadata interfaces often report allocation in fixed accounting units, such as 512-byte units, independently of the filesystem block size. Sparse files may have large logical size and little allocation.

Compression, reflinks, delayed allocation, inline data, metadata overhead, reservations, and shared extents make “bytes on disk” policy-dependent. Capacity and billing systems state which measure they use.

### Data mapping metadata

An inode or related structure connects logical offsets to blocks, extents, inline bytes, or filesystem-specific objects. The fixed inode may contain a root or pointer rather than the full mapping.

Size and mapping updates must agree across allocation, writeback, truncation, clone, and recovery. No reachable mapping may exceed format bounds or reference unowned storage.

### Access time

Access time records eligible reads or executions, but updating it on every access adds writes. Policies such as `noatime`, `relatime`, strict updates, and lazy persistence trade fidelity for cost.

Consumers must learn the mounted policy. Atime is unsuitable as a precise universal audit trail because updates can be suppressed, deferred, coarsened, cached, or lost in a crash.

### Modification, change, and birth times

Modification time tracks content changes. Change time tracks inode-status changes such as mode, ownership, link count, or content update; it is not creation time. Birth time is a separate optional field.

Timestamp resolution, clock adjustment, overflow range, rounding, and filesystem support affect comparisons. Preserve “field unavailable” rather than inventing a plausible timestamp.

### Lazy timestamp persistence

Linux `lazytime` can update timestamps in memory while deferring their disk write until another inode update, synchronization, eviction, or a policy deadline. Reads can observe the fresh cached value before it is crash durable.

This illustrates three states: logically updated, visible through the cache, and persistently recoverable. Tests must distinguish them.

### `stat` and `statx` observations

Metadata APIs return a selected projection of object state. Linux `statx` includes a result mask telling the caller which requested fields are actually supplied and can expose birth time, mount ID, direct-I/O alignment, and other extensions.

Under concurrent mutation, different returned fields can reflect different instants. A result must not be advertised as a transactionally atomic inode snapshot unless the interface and filesystem guarantee that property.

### Stable-handle inspection

Inspecting metadata through an already opened descriptor avoids resolving a pathname again. It binds the query to the opened object even after rename or unlink.

This removes namespace substitution between lookup and inspection, but does not freeze metadata. Other writers can still change the same object unless the caller obtains the required synchronization or version check.

### Metadata mutation

Operations such as `chmod`, `chown`, truncate, timestamp setting, flag changes, and attribute updates first validate type, credentials, mount policy, immutable state, limits, and filesystem support.

The mutation then serializes conflicting fields, applies side effects such as clearing set-ID bits or updating change time, marks state dirty, and returns according to its visibility contract.

### Locking and sequence validation

Inode locks protect compound mutations, while smaller spinlocks, atomics, or sequence counters can protect specific fields and optimistic reads. Lock order must compose with page-cache, directory, quota, journal, and writeback locks.

Optimistic readers validate that no relevant sequence changed. A retry is part of correctness, not merely a performance fallback.

### Metadata writeback

Dirty metadata can be written asynchronously in batches. Writeback selects records, establishes data-versus-metadata ordering, reports errors, and eventually clears dirty state only for changes actually covered by successful I/O.

A later mutation racing writeback must not be lost when completion clears flags. Versioned dirty state or locked transitions separate the written generation from newer changes.

### Journaling and copy-on-write

A journal can record metadata updates so replay produces an old or new coherent state after interruption. Copy-on-write filesystems instead publish new trees through ordered roots. Neither label alone specifies application durability.

The recovery invariant covers inode, allocation, directory, quota, checksum, and orphan records together. Replay must be idempotent and reject malformed or uncommitted state.

### File and directory synchronization

File synchronization requests data and required metadata according to the platform contract. On Linux, `fsync` on a file does not necessarily persist the directory entry that names it; the containing directory also needs synchronization for that requirement.

Crash-safe create or replacement therefore specifies content writes, file synchronization, namespace publication, parent-directory synchronization, error handling, and device assumptions.

### Checksums and validation

Persistent inode checksums detect some corruption and misdirected writes. ext4, for example, incorporates filesystem identity, inode number, and inode bytes into its inode checksum.

A checksum cannot prove semantic correctness or freshness. Readers also validate type, length, feature flags, extent bounds, ownership of referenced blocks, and cross-record relationships.

### Format evolution

Persistent formats reserve fields, record inode size, and gate interpretations behind compatible, read-only-compatible, or incompatible features. Readers access extension fields only when the recorded structure length includes them.

Upgrade, downgrade, byte-order, unknown-feature, timestamp-range, and integer-overflow paths are part of correctness. An old implementation must refuse a format it cannot safely interpret.

### Quotas and project identity

User, group, or project identifiers can select accounting domains. Allocation and ownership changes reserve or transfer charges before publishing state and undo them on failure.

Delayed allocation and shared extents complicate the charged quantity. The quota policy must define logical, exclusive, referenced, or physical accounting rather than leaving it implicit.

### Remote attribute caching

Network filesystems cache attributes to reduce round trips. Freshness can depend on leases, close-to-open rules, validation timers, change attributes, server callbacks, or explicit invalidation.

Stale size or permissions can be a documented consistency outcome, but security boundaries require a policy for authoritative revalidation. Server reboot and lost replies add uncertainty to updates.

### Observability and experiments

Record filesystem and mount identity, inode and generation, operation, requested and returned fields, cache source, version before and after, credentials and mappings, dirty state, writeback and journal events, errors, synchronization calls, crash point, and recovery result.

Avoid logging sensitive attribute values or labels by default. Preserve raw traces, tool versions, mount options, workload seeds, and limitations so another reviewer can reproduce the claim.

### Security and assurance

Adversarial tests race path replacement, chmod, chown, truncate, unlink, reuse, ACL updates, xattr limits, mapping changes, quota exhaustion, writeback errors, malformed inodes, remote invalidation, and crashes.

Assurance names filesystem-format, VFS, concurrency, security, storage, recovery, distributed-systems, and independent-verification reviewers. Passing a local `stat` test does not certify durable or race-free metadata behavior.

## Definitions and Notation

Let `F` be a mounted filesystem instance, `n` an inode number, `g` a generation, and `I=(F,n,g)` a validated object identity. Let `D_t(parent,name)=I` denote the directory relation at time `t`, `M_t(I)` the logical inode state, `C_t(I)` a cached observation, and `P_t(I)` recoverable persistent state.

Let `h_t(I)` be the link count and `r_t(I)` the number of other lifetime-preserving references under the filesystem's model. A simplified reclamation predicate is `reclaimable_t(I) iff h_t(I)=0 and r_t(I)=0 and recovery obligations are discharged`.

For a regular file, let `s(I)` be logical size, `a(I)` allocation reported in the API's stated units, and `Q(I)` the quota charge. In general, `s(I)`, `a(I)`, physical exclusive bytes, and `Q(I)` are not equal.

A metadata observation `O=(mask,values,v)` names returned fields and an optional version `v`. The mask is part of the result: absence is not zero. Define `visible_t(I)`, `dirty_t(I)`, and `durable_t(I)` separately; visibility does not imply durability.

## Mechanisms, Invariants, or Proof Structure

1. **Resolve identity.** Bind operations to a validated filesystem, inode number, and generation through a pathname or retained handle.
2. **Validate representation.** Check record size, checksum, byte order, feature set, field widths, type, and referenced structures before trusting persistent metadata.
3. **Authorize in context.** Apply credentials, ID mappings, mode, ACL, labels, flags, mount policy, and operation-specific rules to the same object that will change.
4. **Serialize conflicts.** Use a documented lock order or sequence protocol across inode, mapping, page cache, directory, quota, journal, and writeback state.
5. **Preserve cross-field state.** Keep size, mappings, blocks, quotas, link count, timestamps, flags, ACLs, and attributes mutually consistent.
6. **Publish visibility.** Establish the operation's linearization point and return only fields and freshness promised by the API.
7. **Track lifetimes.** Prevent reclamation while any name, open file, mapping, cache reference, or recovery structure preserves the object.
8. **Order persistence.** Mark dirty generations, write data and metadata in the required order, commit or publish recovery state, flush as required, and propagate errors.
9. **Recover safely.** Replay or select roots idempotently, finish orphan processing, reconcile allocation and quota state, and reject corrupt references.
10. **Reuse defensively.** Recycle identifiers only after terminal reclamation and change or validate the generation for stale external references.
11. **Bound resources.** Limit sizes, timestamps, xattr names and values, ACL entries, mappings, link counts, retries, quotas, and recovery work.
12. **Preserve evidence.** Retain versions, masks, mappings, mount options, traces, crash points, and counterexamples sufficient to audit the claimed contract.

<!-- bijux-verify: {"id":"inode-metadata-lifetime","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"identity=fs7:42:3 size=1048576 allocated=8192 sparse=True\nafter-unlink links=0 open=1 reclaimable=False\nafter-close links=0 open=0 reclaimable=True\n","stderr":""}} -->
```python
inode = {
    "filesystem": "fs7",
    "number": 42,
    "generation": 3,
    "size": 1_048_576,
    "allocated": 8_192,
    "links": 1,
    "open_references": 1,
}


def reclaimable(record: dict[str, int | str]) -> bool:
    return record["links"] == 0 and record["open_references"] == 0


identity = f'{inode["filesystem"]}:{inode["number"]}:{inode["generation"]}'
print(
    f'identity={identity} size={inode["size"]} allocated={inode["allocated"]} '
    f'sparse={inode["allocated"] < inode["size"]}'
)
inode["links"] -= 1
print(
    f'after-unlink links={inode["links"]} open={inode["open_references"]} '
    f'reclaimable={reclaimable(inode)}'
)
inode["open_references"] -= 1
print(
    f'after-close links={inode["links"]} open={inode["open_references"]} '
    f'reclaimable={reclaimable(inode)}'
)
```

The executable model demonstrates identity scope, sparse logical-versus-allocated size, and name-independent lifetime. It intentionally omits path resolution, permissions, ACLs, mappings, locking, writeback, crashes, and actual filesystem behavior.

## Alternatives and Trade-Offs

- Fixed inode records enable direct indexing and predictable reads but constrain field growth; trees or object records improve flexibility at indexing cost.
- Large inodes hold more attributes inline and reduce extra reads but consume more fixed metadata space.
- Strict access-time updates provide fresher information but increase write amplification; relative, disabled, or lazy updates weaken timestamp meaning.
- Rich ACLs and labels express policy beyond mode bits but enlarge the authorization state and copy or restore attack surface.
- Optimistic sequence-validated reads reduce lock contention but can retry and still provide only a field-level observation contract.
- Eager synchronous metadata writeback simplifies some failure reasoning but raises latency; asynchronous batching requires dirty-generation and error discipline.
- Metadata journaling reduces recovery work but adds log traffic; copy-on-write trees avoid in-place overwrite but add amplification and root-publication complexity.
- Aggressive inode reuse conserves finite identifiers but increases stale-handle pressure; delayed reuse consumes capacity and still needs generations.
- Long remote attribute leases reduce latency and server load but increase staleness windows; revalidation improves freshness at network cost.
- Checksums improve corruption detection but consume space and CPU and cannot replace semantic validation or redundancy.
- Project quotas provide workload-level accounting but complicate inheritance, ownership transfer, reflinks, and recovery.
- Portable basic `stat` fields ease application compatibility; richer interfaces expose masks and capabilities but require feature-aware callers.

## Failure Modes and Misconceptions

- **“The filename is in the inode.”** Names live in directory relations; an inode can have several names or none.
- **“Inode number is globally unique forever.”** It is filesystem-scoped and reusable; stable handles need instance and generation validation.
- **“Link count zero means the object is gone.”** Open files, mappings, and recovery references can preserve it.
- **“`ctime` means creation time.”** It records inode-status change; birth time is a separate optional field.
- **“Size is disk usage.”** Sparse, compressed, inline, shared, reserved, and metadata storage separate the quantities.
- **“A successful `statx` filled every field.”** The result mask identifies available fields.
- **“One metadata structure is one atomic snapshot.”** Concurrent updates can yield fields sampled at different moments under the documented API.
- **“`fsync(file)` always persists the name.”** Directory-entry persistence can require synchronizing the parent directory.
- **“Mode bits are the complete policy.”** ACLs, labels, capabilities, flags, mount policy, and mapped identities can also govern access.
- **“Extended attributes are harmless user tags.”** Some namespaces contain kernel-interpreted authority and require privilege.
- **“The cached owner integer has universal meaning.”** ID mappings and mount context affect interpretation.
- **“Clearing dirty after I/O is trivial.”** A concurrent new mutation can be lost without generation-aware completion.
- **“A checksum makes the inode correct.”** It detects selected byte corruption, not semantic inconsistency, rollback, or malicious valid checksums.
- **“Local metadata behavior predicts network behavior.”** Remote caching, leases, reboot, and uncertain replies change freshness and failure semantics.

## Worked Examples

### Example 1

Two hard links `report` and `archive/report` identify `(fs7,42,3)`. Changing mode through either name changes the same inode; deleting one name decrements link count without copying content.

### Example 2

A sparse file has logical size 1 TiB and 16 MiB of allocated extents. A backup tool using size for capacity prediction overestimates physical reads, while one copying only allocation without hole semantics can change the restored layout.

### Example 3

An open temporary file is unlinked immediately. Link count reaches zero, but the file remains readable and consumes space until its final open reference closes; crash recovery must also finish any recorded orphan.

### Example 4

A server reuses inode number 42 after reclamation. A client handle containing generation 3 is rejected when the new occupant has generation 4 instead of silently exposing unrelated content.

### Example 5

A process requests birth time with `statx`, but the result mask omits that field. Correct code reports “unavailable”; treating the zero-initialized field as the epoch fabricates evidence.

### Example 6

While one thread changes ownership and another truncates a file, a metadata query observes the new owner and old size. This can satisfy the documented non-atomic field contract even though no single instant had the whole combination the caller imagined.

### Example 7

With lazy timestamp persistence, a read updates cached atime and a following query sees it. Power loss before synchronization restores the older on-disk atime, so visibility did not imply durability.

### Example 8

An administrator removes group write through mode bits on a file with an extended ACL. The ACL mask is updated consistently; leaving the old mask effective would regrant access contrary to the requested transition.

### Example 9

A container sees a mapped owner of 1000 while the filesystem stores a different kernel identifier. Authorization and `chown` use the mount mapping rather than comparing the displayed value directly to raw disk fields.

### Example 10

A service writes a new configuration, synchronizes the file, renames it over the live name, and synchronizes the parent directory. Its recovery claim names all steps; file synchronization alone would not establish durable publication of the name.

## Cross-Program Connections

[Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) connects fixed records, trees, checksums, caches, and versioned identity. [Data Engineering](../../19-data-engineering/ROADMAP.md) connects schema evolution, metadata catalogs, lineage, storage accounting, and freshness.

[Security Engineering](../../25-security-engineering/ROADMAP.md) supplies authorization, identity mapping, labels, capabilities, TOCTOU analysis, and audit design. [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) connects leases, cached attributes, generation validation, uncertain outcomes, and server recovery.

Within this program, [OS-037](037-copy-on-write.md), [OS-039](039-shared-pages-and-page-cache.md), and [OS-041](041-files-directories-and-namespaces.md) supply copy-on-write, cache, and naming foundations; [OS-043](../ROADMAP.md) through [OS-050](../ROADMAP.md) apply inode invariants to allocation and complete filesystem designs.

## References

- Linux kernel documentation, [Overview of the Linux Virtual File System](https://docs.kernel.org/filesystems/vfs.html), current page checked 2026-09-04. In-memory inode and dentry objects, inode cache lifecycle, lookup, attribute operations, writeback, eviction, synchronization, and filesystem abstraction.
- Linux kernel documentation, [ext4 Index Nodes](https://docs.kernel.org/filesystems/ext4/inodes.html), current page checked 2026-09-04. Metadata placement, inode-table addressing, modes, size, blocks, links, flags, mappings, generation, checksums, extended fields, project IDs, and timestamps.
- Linux kernel documentation, [Idmappings](https://docs.kernel.org/filesystems/idmappings.html), current page checked 2026-09-04. Filesystem, mount, and caller identity mappings for ownership checks, creation, and ownership changes.
- Linux kernel documentation, [File system locks](https://docs.kernel.org/filesystems/locking.html), current page checked 2026-09-04. VFS inode, attribute, permission, xattr, timestamp, and writeback locking contexts.
- Linux man-pages project, [inode(7)](https://man7.org/linux/man-pages/man7/inode.7.html), current page checked 2026-09-04. File type, mode, ownership, links, size, blocks, timestamps, and mount-controlled timestamp semantics.
- Linux man-pages project, [statx(2)](https://man7.org/linux/man-pages/man2/statx.2.html), current page checked 2026-09-04. Requested and returned field masks, extended metadata, pathname and descriptor-relative selection, synchronization flags, and mixed-moment field observations.
- Linux man-pages project, [xattr(7)](https://man7.org/linux/man-pages/man7/xattr.7.html), current page checked 2026-09-04. Extended-attribute namespaces, access rules, storage limits, filesystem support, and security uses.
- Linux man-pages project, [acl(5)](https://man7.org/linux/man-pages/man5/acl.5.html), current page checked 2026-09-04. Access and default ACL entries, masks, object creation, permission checks, and mode changes.
- Linux man-pages project, [mount(2)](https://man7.org/linux/man-pages/man2/mount.2.html), current page checked 2026-09-04. `noatime`, `relatime`, strict access-time, and lazy timestamp update and persistence policies.
- Linux man-pages project, [fsync(2)](https://man7.org/linux/man-pages/man2/fsync.2.html), current page checked 2026-09-04. File data and associated metadata synchronization, error behavior, and the separate need to synchronize a containing directory for directory entries.

## Exercises

### Exercise 1

Specify a metadata identity and observation API. Cover filesystem scope, generations, requested and returned fields, unavailable values, concurrency, handles, and remote freshness.

### Exercise 2

Design hard-link removal, open-unlinked lifetime, orphan recovery, reclamation, and inode reuse. State invariants for failures and crashes.

### Exercise 3

Design an authorized metadata-mutation transaction for ownership, mode, ACL, labels, timestamps, and project quotas under an idmapped mount.

### Exercise 4

Specify crash-safe publication of a newly created file. Include data, inode metadata, directory entries, synchronization, errors, and recovery evidence.

### Exercise 5

Build a test and assurance plan for inode metadata across local, virtual, and remote filesystems. Include concurrency, corruption, versioning, limits, caching, and reviewers.

## Answers to the Exercises

### Answer 1

Represent identity as filesystem-instance token, inode number, and generation; retain a descriptor or validated handle when stability matters. The query accepts a field mask and synchronization or freshness policy, and returns an availability mask, values, source or version information, and explicit errors. A missing birth time is unavailable, not zero. Document whether fields may come from different moments and how a caller can request revalidation.

Path-based selection resolves once under stated follow rules, while descriptor-based selection addresses the already opened object. Remote results identify cache age, lease or change token, and server epoch when available. Reject stale generations and filesystem-instance mismatch. Strong snapshot consumers use a filesystem-provided version protocol or application lock rather than inferring atomicity from one structure.

### Answer 2

Unlink stabilizes parent and target, verifies the current binding, removes the directory entry, decrements link count, and records any zero-link live object in the filesystem's recovery structure as one recoverable operation. The object remains allocated while open files, mappings, cached references protected by the lifecycle protocol, or recovery work preserve it.

Final close or eviction checks zero links and zero preserving references, completes pending writeback, releases mappings, quotas, xattrs, and blocks, then makes the inode slot reusable. Recovery replays committed namespace and count changes and processes orphan records idempotently. Reuse assigns a new generation; stale handles must fail even if the number is identical. Fault injection at every persistence boundary must yield the old object, the valid unlinked object, or complete reclamation—never a reachable freed block or a new object accepted under the old generation.

### Answer 3

Resolve the object to a stable handle and translate caller, mount, and filesystem IDs explicitly. Authorize ownership change, mode, ACL, label, timestamp, immutable or append-only state, mount flags, and quota transfer against one credential snapshot. Reserve destination quota before publishing and reject unsupported namespaces, oversized ACLs, invalid masks, privilege-bearing labels, or unmappable IDs.

Acquire locks in the filesystem's inode, xattr, quota, journal, and writeback order. Compute the complete new state: mapped owner and group, mode and ACL mask agreement, required set-ID clearing, label policy, timestamps including change time, project identity, and quota charges. Journal or copy-on-write all affected records, publish one authorized transition, and unwind reservations on failure. Record mapping version and policy evidence without exposing sensitive values.

### Answer 4

Create the file in the intended parent without replacement or use a private staging name under the same filesystem. Write content, validate size and required metadata, apply ownership, mode, ACLs, attributes, and labels through the opened handle, then synchronize the file and check every delayed writeback error. Publish with the appropriate atomic rename or link operation and synchronize the containing directory; synchronize every affected parent when the platform contract requires it.

Specify assumptions about filesystem mode, journal or copy-on-write behavior, device flushes, and remote server stability. Inject crashes before and after data write, inode update, file sync, namespace publication, and directory sync. Recovery must expose either the previous complete name or the new complete object according to the stated point, with no dangling entry, leaked allocation, unbalanced quota, or silent error.

### Answer 5

Generate regular, sparse, inline, compressed where supported, reflinked, huge, empty, multiply linked, unlinked-open, directory, symlink, device, and virtual objects. Exercise field masks, timestamp ranges and policies, ACL and xattr limits, mapped ownership, project quotas, truncation, chmod and chown side effects, concurrent stat and mutation, dirty writeback generations, I/O errors, identifier reuse, unknown format features, malformed sizes, checksum failures, and allocation inconsistencies.

For remote filesystems, vary lease, revalidation, disconnect, server reboot, lost reply, and generation reuse. For crash tests, preserve disk images or journal traces at controlled persistence points and independently check namespace, inode, block, quota, and orphan invariants after recovery. Record kernels, filesystems, mount options, server versions, workload seeds, field masks, raw outputs, and limitations. Named VFS, filesystem-format, concurrency, security, storage, recovery, distributed-systems, and independent-verification reviewers assess claims; no single local test certifies portable metadata semantics.
