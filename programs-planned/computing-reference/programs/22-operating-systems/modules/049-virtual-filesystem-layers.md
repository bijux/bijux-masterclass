---
module_id: OS-049
program: Operating Systems
level: 1
module_number: 49
title: Virtual Filesystem Layers
status: complete
last_verified: 2026-09-04
---

# Virtual Filesystem Layers

## One-Page Review

### Governing question

How can one kernel interface support local, remote, stacked, pseudo, and userspace filesystems while preserving each implementation's semantics, object identity, concurrency, security, caching, error, and durability contracts?

### Essential definitions

- A **virtual filesystem layer (VFS)** maps generic pathname, descriptor, metadata, and I/O operations to filesystem-specific operation tables.
- A **filesystem type** is a registered implementation capable of creating or discovering filesystem instances.
- A **superblock** represents one mounted filesystem instance and its global state, root, limits, and lifecycle operations.
- A **mount** attaches a superblock subtree to a namespace location with a particular view and per-mount policy.
- A **dentry** caches the association between a parent, a name, and an inode or a negative lookup result.
- An **inode** represents a filesystem object and its metadata independently of any one pathname.
- A **file object** represents an open file description: the opened path, access mode, offset, credentials, and filesystem operations shared by duplicated descriptors.
- An **address space** connects an inode or block device to cached pages and filesystem-specific read, write, and invalidation operations.

### Central model, mechanism, or theorem

For request `R=(op,N,S,P,F,C,t)`, the VFS resolves pathname `P` from starting object `S` in mount namespace `N`, obtains stable mount, dentry, and inode references, applies credentials `C`, and dispatches `op` through an operation table. The selected implementation returns data, metadata, namespace change, or a precise error. An open descriptor then references a file object rather than re-resolving its original pathname.

The VFS is a common protocol, not a promise that every filesystem has identical semantics. Correctness requires explicit capability discovery, stable lifetime rules, cache-coherency contracts, lock ordering, and operation-specific durability. Generic code must not invent support when an operation is absent or erase important differences between local, network, stacked, pseudo, and userspace implementations.

### Critical invariants

- Every live object reference pins the object and every containing mount needed for safe use.
- A dentry's parent/name relation and inode association are validated against the filesystem's coherency rules before use.
- Namespace mutation follows a global lock order and publishes no partially linked topology.
- Generic dispatch invokes only supported operations and preserves filesystem-specific errors, partial progress, and retry rules.
- Dirty cached state remains associated with the authoritative object and is written, invalidated, or failed under a defined contract.
- Unmount, freeze, eviction, and daemon failure cannot free state still reachable by an active reference or in-flight request.
- Security and identity checks use the actual mount, inode, credentials, idmapping, and operation rather than pathname text alone.

### Common failures

Common errors are equating a mount with a superblock, treating a dentry as an inode, assuming one inode has one pathname, storing descriptor state in an inode, returning success for an unsupported method, retaining negative dentries without revalidation, holding filesystem locks across unbounded userspace or network waits, violating rename lock order, assuming page-cache writeback means stable storage, and presenting overlay or FUSE behavior as indistinguishable from a local filesystem.

### Compact example

`/local/config` and `/remote/config` both receive the generic `read` operation. Path lookup selects different mounts; each mount identifies an object and an operation table. The VFS dispatches the same operation to `memfs.read` or `netfs.read`, while the open file stores the chosen implementation and object identity. Uniform syntax therefore coexists with different latency, failure, coherency, and durability behavior.

### Connections

[OS-041](041-files-directories-and-namespaces.md), [OS-042](042-inodes-and-metadata.md), and [OS-045](045-buffer-cache-and-page-cache.md) establish names, objects, and cached data. [OS-048](048-filesystem-permissions.md) supplies authorization, while [OS-050](../ROADMAP.md) traces VFS writes through caches and filesystem persistence.

## Governing Question

Applications expect `open`, `read`, `write`, `stat`, `rename`, and related interfaces to work across many filesystems. Those filesystems differ profoundly: some journal to disks, some speak remote protocols, some synthesize state, some combine lower and upper trees, and some delegate requests to a userspace daemon.

The governing question is how the kernel can offer a stable interface without confusing uniform entry points with uniform behavior. The answer is an object protocol with explicit dispatch, reference lifetimes, caching rules, lock order, feature negotiation, and error semantics.

## Why This Matters

The VFS is on the path of nearly every program. A lifetime error can become use-after-free; a lookup race can violate namespace isolation; a lock inversion can deadlock the machine; an incorrect writeback assumption can lose acknowledged data.

Abstraction quality also determines extensibility. A new filesystem should reuse pathname walking, descriptor tables, polling, memory mapping, and permission hooks without copying all generic logic. At the same time, the interface must let the implementation express unsupported operations and unusual coherency or persistence rules honestly.

Operational debugging depends on knowing the layers. The same `EIO` may originate in generic validation, a filesystem method, a userspace daemon, a remote server, or delayed writeback. Engineers need stable identities and boundary-specific telemetry to locate the fault.

## Prerequisites and Retrieval

Review [OS-021](021-critical-sections-in-the-kernel.md), [OS-022](022-spinlocks-and-interrupt-context.md), [OS-038](038-memory-mapped-files.md), [OS-041](041-files-directories-and-namespaces.md), [OS-042](042-inodes-and-metadata.md), [OS-045](045-buffer-cache-and-page-cache.md), and [OS-048](048-filesystem-permissions.md).

Retrieve these distinctions:

- a pathname is resolved, while an open descriptor refers to a stable open file description;
- hard links allow several dentries to refer to one inode;
- a mount namespace selects a topology view, not a second copy of file data;
- cached data and cached names have different validity and invalidation rules;
- an operation can succeed partially, complete asynchronously, or report an error later;
- reference counting solves lifetime ownership but does not by itself solve semantic races;
- read visibility, writeback completion, filesystem commit, and stable-media durability are separate claims;
- authorization composes credentials, path traversal, object metadata, mount context, and security policy.

## Learning Objectives

After this module, you should be able to:

1. map system calls through mount, dentry, inode, file, and address-space objects;
2. distinguish filesystem types, superblocks, mounts, dentries, inodes, and open file descriptions;
3. explain operation-table dispatch, feature negotiation, fallback, and unsupported-operation behavior;
4. reason about positive and negative lookup caching, revalidation, page-cache ownership, and writeback;
5. design reference, eviction, freeze, unmount, and failure lifecycles without dangling state;
6. apply lock ordering and retry patterns to lookup, create, unlink, link, and rename;
7. evaluate stacked, remote, pseudo, and userspace filesystems without hiding semantic differences;
8. construct tests and evidence for VFS correctness, security, performance, and durability boundaries.

## Core Exposition

### Abstraction boundary

The VFS owns generic entry points, object lifetimes, pathname traversal, descriptor integration, common permission hooks, and dispatch. A filesystem owns its on-disk, remote, synthetic, or delegated representation and implements the methods it supports.

This division avoids copying generic machinery into each implementation. It does not authorize generic code to emulate every missing method or claim stronger atomicity, coherency, or durability than the implementation provides.

### Filesystem types

A registered filesystem type describes how to obtain a filesystem context and construct or locate an instance. Registration makes the implementation discoverable; it does not mount anything by itself.

Type names, module ownership, parameters, and supported mount modes need controlled lifetimes. Registration must prevent new users before code or type state can be unloaded.

### Filesystem context and mount construction

A modern mount flow separates context creation, option parsing, parameter validation, tree acquisition, and attachment. Parsing converts external text or structured options into typed internal state before mutating a live instance.

Validation rejects incompatible combinations early. Tree acquisition may allocate a new superblock or find a shareable existing instance. Namespace attachment is a later topology operation and should not expose a half-configured tree.

### Superblocks

A superblock represents one filesystem instance. It commonly holds the root dentry, block-size and limit information, dirty state, backing-device or remote-session state, inode indexes, and superblock operations.

Several mounts can refer to the same superblock. A superblock therefore cannot safely store policy that varies per mount unless that policy is deliberately lifted into the instance contract.

### Mounts

A mount joins a root within one superblock to a mountpoint in a namespace. It supplies topology and view-specific properties such as propagation, read-only state, and possibly an identity mapping.

Bind mounts and multiple namespace attachments demonstrate why mount and superblock are distinct. The same inode may be reachable through different mount paths and policies without duplicating underlying data.

### Dentries

A dentry represents a name relative to a parent and caches lookup outcome. A positive dentry refers to an inode; a negative dentry records that the name was absent under observed state.

Dentries accelerate repeated path walking and retain aliases. Because rename, create, unlink, remote changes, or filesystem-specific rules can invalidate cached conclusions, lookup must use sequence validation, locks, leases, expiry, or a revalidation method as appropriate.

### Inodes

An inode is the VFS representation of one filesystem object and its metadata. It contains stable filesystem identity, type, ownership, permissions, timestamps, size, state flags, mapping, and operation vectors.

One inode can have many dentry aliases because of hard links. An unlinked inode can remain alive while file objects, memory mappings, or other references exist. Names and object lifetime must therefore remain separate.

### File objects and descriptors

A successful open allocates a file object representing an open file description. It records access mode, flags, current offset where applicable, path reference, private implementation state, and file operations.

Descriptor duplication and process inheritance can share that file object and offset. Separate opens of the same inode create separate file objects. Per-open state belongs here, not in the shared inode.

### Address spaces and cached pages

An address-space object associates cached pages with an inode or another backing object. Its operations populate, dirty, write back, invalidate, migrate, and release cached state.

The VFS and memory manager can provide common caching while the filesystem controls how page indexes map to storage or remote objects. Direct I/O, memory mapping, truncation, holes, and writeback errors require explicit coordination with this cache.

### Operation tables

Operation vectors make dynamic dispatch explicit. Superblock operations manage instance-wide state; inode operations govern names and metadata; file operations govern opened-handle behavior; address-space operations govern cached data; dentry operations customize name-cache behavior.

A missing method means unsupported or selects only a documented generic fallback. Generic code must never manufacture success. Each callback contract specifies required locks, sleepability, ownership transfer, return conventions, and permissible reentry.

### Lookup path

Path walking starts from the namespace root, current directory, or explicit directory handle. For each component it selects a mount, consults the dentry cache, invokes filesystem lookup when necessary, follows symbolic links under limits, and checks traversal policy.

Fast read-copy-update lookup can avoid reference increments and locks while sequence counters prove that observed topology remained stable. On uncertainty it falls back to a reference-walk path. Restart is a correctness mechanism, not an exceptional failure.

### Open path

Open combines resolution with final-component rules, permissions, creation or truncation if requested, and file-object initialization. Atomic open hooks can let a filesystem perform lookup and creation without a vulnerable gap.

Once installed in the descriptor table, the file object pins its path and implementation state. Later rename or unlink does not redirect the descriptor to another inode.

### Read and write dispatch

A read validates the file mode and request, then uses iterator-based or filesystem-specific file operations, often through the page cache. A write also handles append serialization, size limits, space allocation, dirty accounting, and partial progress.

The syscall result reflects its defined completion point. Buffered write success usually means bytes entered kernel-managed state, not that a device or remote server has made them durable.

### Metadata dispatch

`stat` can use inode state but may require filesystem revalidation. `setattr` operations such as truncate, ownership change, and timestamp update coordinate permissions, cached pages, quotas, leases, security labels, and persistent metadata.

Extended attributes and access-control data use operation-specific hooks and namespaces. Unsupported metadata must produce a precise error rather than disappearing during copy or restore.

### Namespace mutation

Create, link, unlink, mkdir, rmdir, and rename operate on parent directories and dentries as well as target inodes. The implementation validates topology, permissions, type rules, link counts, quotas, and replacement constraints before publication.

Rename is particularly demanding because two parents, a source, an optional victim, mount boundaries, and ancestor relationships can participate. A documented directory-locking order prevents cycles and ensures that concurrent lookup observes an allowed old or new state.

### Reference ownership

Every object type defines who acquires and releases references. A file pins its path; a positive dentry pins its inode under the dentry contract; a mount pins its superblock; asynchronous requests retain every object required at completion.

Reference counts prevent reclamation while a known reference exists. Cache membership, deferred RCU reclamation, weak lookup handles, and semantic validity still require separate rules.

### Eviction and reclamation

Memory pressure can shrink dentries and inodes that have no active use. Eviction first removes discoverability, then flushes or discards state under the filesystem contract, releases private resources, and waits for safe deferred reclamation where required.

Dirty state cannot be silently reclaimed. An unlinked but open inode remains eligible for I/O until the final references and mappings disappear, after which deletion and storage recovery can complete.

### Freeze, synchronization, and unmount

Freeze quiesces mutation in ordered stages so snapshots or consistency operations observe a stable point. Synchronization initiates and waits for defined writeback classes, while filesystem commit may additionally flush journals, device caches, or remote acknowledgements.

Unmount detaches topology and eventually tears down the instance. Busy references can reject ordinary unmount; forced or lazy variants have narrower guarantees and do not make in-flight state magically safe. Shutdown orders new-operation exclusion, drain, writeback, detach, and destruction.

### Locking and restart

VFS locking protects topology, per-inode state, file position, cached pages, and implementation state at different granularities. A single global lock would simplify proofs but destroy concurrency.

Correct designs declare acquisition order and which callbacks may sleep or recurse. They release or avoid locks before unbounded remote and userspace waits, then revalidate generations on return. Optimistic lookup retries when a sequence changes.

### Error and partial-progress contracts

Errors identify absent names, unsupported operations, stale handles, permission denial, cross-device requests, retryable conflicts, interrupted waits, space exhaustion, I/O failure, and daemon or server loss. Collapsing these into one generic failure prevents safe recovery.

Reads and writes may transfer some bytes before encountering an error. Delayed writeback errors can surface on later write, synchronization, or close-related paths under the interface contract. Callers and filesystems must preserve both progress and pending failure.

### Security hooks and idmapped views

Permission checks occur during traversal, final operation, and particular metadata or content transitions. They use the actual credentials, inode, mount, security context, and operation. Security modules can add policy at stable VFS hooks.

An idmapped mount changes ownership interpretation for that view without rewriting all inode owners. Helpers must receive the relevant mount mapping; comparing raw identifiers outside that context can authorize incorrectly.

### Network filesystems

A network filesystem maps VFS objects onto server-side identifiers and protocol operations. Dentries, attributes, and data may require leases, expiry, change tokens, callbacks, or revalidation because another client can mutate authoritative state.

Offline operation and local caching trade availability and latency against coherence. Server errors, session recovery, duplicate requests, credential expiry, and uncertain commit require protocol-specific state machines rather than local-filesystem assumptions.

### Netfs cache helpers

Kernel helper layers can coordinate reads, writes, and local caching for network filesystems while leaving protocol semantics to the consumer. Requests describe byte ranges, sources, destinations, completion, and failure.

Shared helpers reduce duplicated cache machinery, but they do not decide remote consistency, authorization, or durability. Those remain explicit responsibilities of the network filesystem and server protocol.

### Userspace filesystems

FUSE-like designs forward VFS requests to a userspace daemon through a kernel transport. Requests need unique identities, bounded payloads, interrupt and cancellation behavior, credential context, and exact reply validation.

The daemon may crash, hang, recurse into its own mount, or return malformed data. Mount policy defines trust, caching, timeout, abort, and access behavior; kernel locks must not be held in ways that turn daemon delay into system-wide deadlock.

### Stacked filesystems

A stacked filesystem presents objects derived from lower filesystems. Overlay designs can select a lower object for reads and create an upper copy for mutation, using whiteouts or opaque-directory metadata to represent removals and hiding.

Copy-up changes identity and may need to preserve or deliberately transform ownership, timestamps, ACLs, xattrs, capabilities, holes, and data. Rename, hard links, memory mappings, export handles, and synchronization cross multiple layers and require documented semantics.

### Pseudo filesystems

Pseudo filesystems expose kernel state as names and objects without conventional persistent media. Their inodes can be synthesized, and reads or writes may invoke live control operations rather than access stored bytes.

The VFS object contract still supplies lookup, descriptors, poll, permissions, and lifetime. Tools must not infer ordinary-file atomicity, seekability, size, or persistence merely because the interface uses a pathname.

### Stable handles and export

Some consumers need to reconstruct objects from filesystem identifiers rather than pathnames. Export operations encode an identity plus generation information and later decode it while detecting deletion or reuse.

An inode number alone may be recycled and is not universally sufficient. Stable-handle support is an explicit filesystem capability with authorization and namespace boundaries.

### Observability

Useful telemetry records operation, filesystem and mount identity, stable object identity where safe, cache hit or revalidation, callback boundary, latency, bytes, retry, cancellation, and final error. Sensitive path and credential data require minimization.

Tracing must avoid altering lock timing so drastically that races disappear or deadlocks emerge. Correlation identifiers help connect one syscall to asynchronous writeback, userspace requests, or network operations.

### Testing and assurance

Unit tests cover method contracts, absent callbacks, reference transfers, and error mapping. Concurrency tests race lookup, rename, unlink, mount, unmount, truncate, memory mapping, writeback, and reclamation with deterministic fault injection.

Integration tests run multiple filesystem families and check semantic differences explicitly. Crash and recovery tests inspect reconstructed state; performance tests measure cache hit, miss, contention, and tail latency without turning benchmarks into correctness claims.

Assurance identifies VFS, filesystem, memory-management, security, userspace-daemon, network-protocol, concurrency, recovery, and independent reviewers. Passing a dispatch toy or one local filesystem test does not certify the VFS.

## Definitions and Notation

Let filesystem type `T` construct instance `S_b`, a superblock. Let mount `M=(S_b,r,p,f,i)` attach root dentry `r` at namespace point `p` with flags `f` and identity mapping `i`.

Let dentry `D=(parent,name,I?,g_d)` associate a parent and name with optional inode `I` under dentry generation or validation state `g_d`. `I?=none` denotes a negative dentry. Let inode `I=(S_b,key,type,meta,A,g_i)` have filesystem identity `key`, metadata, address space `A`, and generation `g_i`.

Let open file `F=(M,D,I,mode,flags,pos,ops,private)` and process descriptor map `FD[d]=F`. Duplicated descriptors can reference the same `F`; independently opened files can reference the same `I` through different `F` objects.

For request `R=(op,N,S,P,F,C,t)`, dispatch is `VFS(R) -> operation_T(op, context)` after generic validation and stable object acquisition. Absence of `operation_T` for `op` yields a documented fallback or `unsupported`, never fabricated success.

Define lifetime safety as `reachable(X,t) implies refs(X,t)>0` for every object `X` whose storage could otherwise be reclaimed. This condition is necessary but not sufficient: cached state must also be semantically valid for the operation and generation.

## Mechanisms, Invariants, or Proof Structure

1. **Parse and validate.** Convert external mount or syscall arguments into bounded typed state and reject unsupported combinations.
2. **Acquire a namespace view.** Pin the starting path, namespace, mount, and credentials used by the request.
3. **Resolve names.** Consult dentries, cross mounts, invoke lookup and revalidation, and retry optimistic walks when generations change.
4. **Bind stable objects.** Retain the selected mount, dentry, inode, and any parent or victim needed for the operation.
5. **Authorize precisely.** Apply traversal, object, parent, mount-idmap, capability, and security-module policy for the requested operation.
6. **Select a method.** Choose the appropriate superblock, inode, file, address-space, or dentry operation and reject absent support.
7. **Execute under declared concurrency.** Follow lock order, avoid unbounded waits while holding incompatible locks, and revalidate after dropped locks.
8. **Publish atomically.** Expose namespace and metadata transitions only at allowed observation points and preserve rollback or recovery state.
9. **Account for partial progress.** Return completed bytes or objects while retaining later error information under the interface contract.
10. **Manage cached state.** Associate data and metadata with authoritative identity, record dirty state, and invalidate or revalidate by generation.
11. **Drain before destruction.** Exclude new work, cancel or finish in-flight requests, flush required state, detach topology, and release references in order.
12. **Preserve evidence.** Record implementation, identities, generations, dispatch, waits, retries, errors, persistence boundary, and test limitations.

<!-- bijux-verify: {"id":"vfs-operation-dispatch","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"path=/local/config fs=memfs object=m1 data=local\npath=/remote/config fs=netfs object=n7 data=remote\nsame-vfs-operation=read implementations=memfs,netfs\n","stderr":""}} -->
```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Mount:
    prefix: str
    filesystem: str


objects = {
    ("memfs", "/config"): ("m1", "local"),
    ("netfs", "/config"): ("n7", "remote"),
}


def memfs_read(object_id: str, data: str) -> str:
    return data


def netfs_read(object_id: str, data: str) -> str:
    return data


operations = {"memfs": {"read": memfs_read}, "netfs": {"read": netfs_read}}
mounts = (Mount("/local", "memfs"), Mount("/remote", "netfs"))


def vfs_read(path: str) -> tuple[str, str, str]:
    mount = next(item for item in mounts if path.startswith(item.prefix + "/"))
    relative_path = path[len(mount.prefix) :]
    object_id, stored_data = objects[(mount.filesystem, relative_path)]
    data = operations[mount.filesystem]["read"](object_id, stored_data)
    return mount.filesystem, object_id, data


for requested_path in ("/local/config", "/remote/config"):
    filesystem, object_id, data = vfs_read(requested_path)
    print(f"path={requested_path} fs={filesystem} object={object_id} data={data}")
print("same-vfs-operation=read implementations=memfs,netfs")
```

The executable example verifies only mount selection and operation-table dispatch over two immutable dictionaries. It does not model real lookup, references, locks, credentials, caching, I/O, networks, userspace daemons, errors, or durability.

## Alternatives and Trade-Offs

- Operation tables make implementations modular but distribute behavior across callbacks; monolithic branching centralizes control and scales poorly.
- Aggressive dentry caching reduces lookup latency but enlarges revalidation and invalidation obligations, especially for remote filesystems.
- RCU path walking improves read concurrency but requires sequence validation and fallback; reference walking is simpler and more expensive.
- Fine-grained locks improve throughput but multiply ordering proofs; coarse locks simplify reasoning and create contention.
- Generic fallbacks reduce implementation work but can accidentally claim semantics a filesystem cannot provide; explicit unsupported errors are honest but less convenient.
- Buffered I/O unifies caching and memory mapping but delays error and durability; direct I/O reduces cache interaction while adding alignment and coherency constraints.
- Shared superblocks save resources but limit per-instance variation; separate instances isolate policy and consume more memory and connections.
- Userspace filesystems improve extensibility and fault isolation but add context switches, daemon availability, and trust boundaries.
- Stacking composes features without rewriting lower filesystems but complicates identity, copy-up, metadata, locking, and persistence.
- Client caching improves network availability and latency but weakens immediate coherence and revocation unless leases or validation constrain it.
- Lazy unmount removes namespace reachability quickly but defers resource teardown; strict unmount gives a clearer completion point and can remain busy.
- Rich tracing accelerates diagnosis but adds overhead, sensitive metadata, and timing perturbation.

## Failure Modes and Misconceptions

- **“The VFS makes every filesystem behave identically.”** It standardizes interfaces while preserving documented semantic differences.
- **“A superblock is a mount.”** One instance can have several namespace attachments and view policies.
- **“A dentry is an inode.”** A dentry represents a name association; aliases can share one inode, and negative dentries have none.
- **“One inode has one pathname.”** Hard links, bind mounts, rename, and namespace views defeat that assumption.
- **“Per-open state belongs in the inode.”** It belongs in the file object shared by descriptors for that open description.
- **“A missing callback can return success.”** It must select a documented generic implementation or report unsupported behavior.
- **“Reference counting prevents all races.”** It prevents premature reclamation, not stale semantic observations or lock-order bugs.
- **“A cached negative dentry stays true.”** Creation or remote change can require invalidation, expiry, or revalidation.
- **“Kernel locks can span any callback.”** A callback may sleep, recurse, or wait on a daemon or server and deadlock the system.
- **“Buffered write success proves persistence.”** It often proves only acceptance into volatile kernel state.
- **“Unmount frees everything immediately.”** Active files, mappings, asynchronous work, and deferred reclamation constrain teardown.
- **“Overlay copy-up preserves identity.”** It can create a new upper object with distinct identity and metadata transformations.
- **“A userspace filesystem is trusted kernel code.”** Replies, delays, credentials, cancellation, and malformed data cross a trust boundary.
- **“Inode number alone is a permanent handle.”** Reuse requires generation or filesystem-defined export identity.

## Worked Examples

### Example 1

Two bind mounts expose one superblock at different namespace paths. Each mount has its own read-only or idmapped view, while both resolve to the same underlying inode.

### Example 2

A lookup misses `report` and installs a negative dentry. Concurrent creation invalidates or replaces that entry; lookup cannot retain absence forever.

### Example 3

Two descriptors produced by `dup` share one file object and offset. A separate `open` of the same inode creates another file object with an independent offset.

### Example 4

An optimistic path walk observes a rename sequence change. It discards the speculative result and retries with stable references instead of using a mixed topology.

### Example 5

A cross-directory rename locks parents under the documented order, verifies that the destination is not beneath the source where prohibited, and publishes one namespace transition.

### Example 6

A buffered write returns its byte count, then writeback receives an I/O error. The filesystem retains that error so a later synchronization path can report failure.

### Example 7

A network filesystem caches attributes with a lease and server change token. Lease expiry triggers revalidation rather than treating old size and permissions as authoritative.

### Example 8

A FUSE daemon stops replying. The transport aborts or times out requests under mount policy, releases waiters, and prevents teardown from freeing request state too early.

### Example 9

An overlay read uses a lower object. The first write copies data and approved metadata to an upper object, then redirects the overlay dentry while preserving defined open-handle behavior.

### Example 10

A pseudo-file reports size zero yet produces live text on every read. Generic tools must use returned bytes and interface semantics instead of assuming stored regular-file behavior.

## Cross-Program Connections

[Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) connects hash tables, trees, caches, reference graphs, and concurrent reclamation. [Computer Architecture](../../23-computer-architecture/ROADMAP.md) connects memory ordering, cache coherence, DMA, and persistence barriers.

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) connects leases, retries, duplicate suppression, partial failure, and server authority. [Security Engineering](../../25-security-engineering/ROADMAP.md) connects stable-object authorization, namespaces, confused deputies, daemon trust, and audit.

[Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies interface contracts, lifecycle hazards, fault containment, evidence, and assurance. Within this program, [OS-050](../ROADMAP.md) follows writes to stable storage and later modules deepen journaling, network filesystems, and observability.

## References

- Linux kernel documentation, [Overview of the Linux Virtual File System](https://docs.kernel.org/filesystems/vfs.html), current page checked 2026-09-04. Filesystem registration, superblocks, inodes, dentries, file objects, address spaces, and operation tables.
- Linux kernel documentation, [Pathname lookup](https://docs.kernel.org/filesystems/path-lookup.html), current page checked 2026-09-04. Name resolution, dentries, reference walking, RCU walking, sequence validation, mounts, symbolic links, and final components.
- Linux kernel documentation, [Locking](https://docs.kernel.org/filesystems/locking.html), current page checked 2026-09-04. Lock and callback expectations for filesystem operation tables.
- Linux kernel documentation, [Filesystem Mount API](https://docs.kernel.org/filesystems/mount_api.html), current page checked 2026-09-04. Filesystem contexts, option parsing, validation, tree construction, reconfiguration, and mounting.
- Linux kernel documentation, [Directory Locking](https://docs.kernel.org/filesystems/directory-locking.html), current page checked 2026-09-04. Lock ordering and invariants for lookup, create, unlink, link, and rename.
- Linux kernel documentation, [FUSE](https://docs.kernel.org/filesystems/fuse/fuse.html), current page checked 2026-09-04. Kernel-daemon transport, request processing, interrupts, mount options, control, and failure behavior.
- Linux kernel documentation, [Overlay Filesystem](https://docs.kernel.org/filesystems/overlayfs.html), current page checked 2026-09-04. Upper and lower trees, work directories, copy-up, whiteouts, credentials, metadata, and export behavior.
- Linux kernel documentation, [Network Filesystem Helper Library](https://docs.kernel.org/filesystems/caching/netfs-api.html), current page checked 2026-09-04. Buffered network I/O, local caching, request lifecycles, and error handling.
- Linux kernel documentation, [Idmappings](https://docs.kernel.org/filesystems/idmappings.html), current page checked 2026-09-04. Caller, filesystem, and mount identity mappings in VFS helpers and ownership operations.
- Linux man-pages project, [open(2)](https://man7.org/linux/man-pages/man2/open.2.html), current page checked 2026-09-04. File descriptors, open file descriptions, offsets, creation, flags, errors, and path races.

## Exercises

### Exercise 1

Trace `open`, cached `read`, buffered `write`, `fsync`, rename, and close through VFS objects and operation tables. State reference and error ownership at every boundary.

### Exercise 2

Design dentry and inode cache rules for a local filesystem and a lease-based network filesystem. Include negative entries, rename, remote mutation, and eviction.

### Exercise 3

Specify a deadlock-resistant lifecycle for a userspace filesystem from mount through daemon failure and unmount. Include cancellation and recursive access.

### Exercise 4

Analyze overlay copy-up of an open executable with hard links, ACLs, capabilities, memory mappings, and a concurrent rename. Identify semantics that must be declared.

### Exercise 5

Build a validation and assurance plan for a new VFS implementation. Cover behavior, concurrency, failure, security, performance, recovery, and evidence.

## Answers to the Exercises

### Answer 1

Mount construction yields a superblock and root dentry, then namespace attachment creates a mount. `open` pins its start, walks mounts and dentries, invokes lookup or revalidation, obtains the inode, authorizes the final operation, calls atomic-open or open hooks, and installs a file object. The descriptor owns a reference to that file; the file pins path, inode under the object contract, operations, credentials or private state as required.

Cached `read` dispatches through file operations and address-space helpers, pins affected pages and request state, then returns bytes or a precise error. Buffered `write` validates mode, serializes append where required, updates cached pages and dirty accounting, and can return partial progress. `fsync` dispatches file and filesystem writeback or commit and reports retained errors. Rename acquires parents and victims in order, invokes inode operations, and atomically updates dentries. Close drops the descriptor reference; final file release invokes the implementation and releases path and private state. Every asynchronous continuation pins its objects until completion.

### Answer 2

For the local filesystem, index dentries by parent and name, allow positive and negative entries, use directory generations or mutation locks for validity, and update aliases atomically during link, unlink, and rename. Cache inodes by filesystem identity plus generation; retain dirty or open inodes and evict only after removing discoverability and completing required writeback.

For the network filesystem, add server file handles, change tokens, lease or attribute expiry, credential and export context, reconnect generation, and callbacks or explicit invalidation. A negative entry expires or is invalidated when another client may create the name. Rename invalidates affected parent generations and aliases. On lease loss, server restart, or uncertain mutation, revalidate rather than extend a stale result. Eviction releases local memory but cannot pretend to delete authoritative server state.

### Answer 3

Create a typed mount context, validate options, establish the daemon channel, and publish the tree only when the connection is usable. Assign every request an identity and state machine; retain mount, object, credentials, buffers, and waiter references until a validated reply, interruption, timeout, or abort reaches one terminal state. Bound message sizes and outstanding work.

Never hold namespace or inode locks across an unbounded daemon wait unless the callback contract proves it safe. Detect access through the served mount by the daemon and provide a documented escape or rejection strategy. On daemon loss, prevent new requests, mark the connection aborted, wake waiters with precise errors, resolve cancellation/reply races exactly once, drain transport ownership, detach the namespace, and reclaim state only after files, mappings, requests, and deferred callbacks are gone.

### Answer 4

Declare when copy-up occurs, whether an already open lower file continues to reference lower state or is redirected, how mappings observe the transition, and whether hard-linked overlay names remain linked after copying. Select one lock order covering overlay dentries, upper and lower parents, the lower object, candidate upper object, and concurrent rename.

Copy content and sparse layout under a coherent snapshot or state what concurrent writes may produce. Map ownership through the active mounts, preserve approved ACLs and labels, and do not restore file capabilities or set-ID state until trusted content is final. Record which xattrs are internal whiteout or opacity metadata. Publish the upper dentry atomically, clean abandoned candidates, propagate errors and space exhaustion, and define which layers `fsync` must commit. Test rename before, during, and after publication plus lower deletion, mapping writeback, crash, and recovery.

### Answer 5

Build contract tests for every supported and absent superblock, inode, file, dentry, and address-space method. Exercise ordinary files, directories, links, special and synthetic objects, multiple mounts, idmaps, descriptors, mappings, export handles, and feature negotiation. Check exact results, partial counts, errno values, retained writeback failures, and durability only at documented boundaries.

Race lookup, negative caching, create, link, unlink, cross-directory rename, truncate, writeback, reclaim, freeze, mount, daemon or server loss, and unmount. Inject allocation, storage, network, malformed-reply, cancellation, timeout, and crash faults. Use lock-order checking, reference and memory sanitizers, model-based operation histories, and recovered-state inspection. Measure hit and miss latency, contention, memory pressure, and tail behavior separately from correctness. Preserve source revision, kernel and filesystem configuration, mounts, seeds, traces, stable identities, generations, requests, raw outcomes, and limitations for named VFS, filesystem, memory, security, distributed, recovery, performance, and independent reviewers.
