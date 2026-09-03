---
module_id: LSDS-012
program: Large-Scale Data Systems Engineering
level: 1
module_number: 12
title: Metadata Servers and Namespace
status: complete
last_verified: 2026-09-03
---

# Metadata Servers and Namespace

## One-Page Review

### Governing question

How can a distributed storage system resolve human names into stable objects, apply multi-item namespace changes atomically, serve cached reads, survive metadata-server failure, and scale hot directories without making the namespace ambiguous?

### Essential definitions

- A **namespace** is the authoritative mapping from names in a context to objects and attributes.
- A **directory entry** or **dentry** maps `(parent identity, component name)` to an inode/object identity and type.
- An **inode** is a stable identity plus attributes such as type, ownership, mode, timestamps, size, layout, and link count.
- **Path resolution** walks components from an explicit root or current directory through directory entries.
- A **namespace transaction** moves the authoritative state from one valid version to another atomically.
- A **metadata journal** records ordered committed mutations; a **checkpoint** materializes a compact state at a known log position.
- A **capability** or **lease** delegates bounded authority or cache validity until revocation, expiry, or fencing.
- A **metadata shard** is an ownership unit assigned to one authority at a particular routing epoch.
- A **snapshot** is an immutable namespace/data view rooted at a declared logical point.
- **Fencing** prevents an obsolete metadata authority from continuing to commit mutations after failover.

### Central model, mechanism, or theorem

Represent a directory entry as `D_v(p,n) -> i` at namespace version `v`. Path resolution composes these mappings from a root identity. A mutation supplies identities and version preconditions, passes authorization and invariant checks, appends a durable transaction at log sequence `s`, publishes a new namespace version, and invalidates incompatible caches. Recovery loads checkpoint `C_k`, replays committed journal entries with sequence greater than `k`, and must produce the same authoritative state.

Atomic rename is a namespace transaction, not a copy-and-delete data operation. Sharding changes which metadata authority executes the transaction, not its externally promised semantics. A scalable design therefore needs explicit routing epochs and a protocol for operations crossing ownership boundaries.

### Critical invariants

- Names are interpreted relative to a specific namespace/root and normalization policy.
- Directory entries refer to stable identities; path strings never replace identity.
- Every committed mutation preserves directory, link-count, type, quota, and cycle invariants.
- A successful atomic operation is wholly visible or wholly absent at its linearization point.
- Only a fenced current authority may commit in an ownership epoch.
- Acknowledged metadata survives under the declared journal/checkpoint durability contract.
- Cached metadata is used only under a valid version, lease, or capability.
- Snapshot roots and retained versions protect referenced objects from premature reclamation.
- Namespace routing and data placement remain separate decisions.

### Common failures

Frequent failures are storing only full paths, confusing a checkpoint helper with a failover replica, acknowledging before journal durability, replaying an uncommitted tail, serving caches after authority changes, granting non-fenced leases, splitting a cross-directory rename into visible halves, hashing names without handling hot single directories or multi-shard operations, measuring data throughput instead of metadata operations, and deleting unlinked objects before open handles and snapshots release them.

### Compact example

Suppose `(root,"projects")->inode 20`, `(20,"alpha")->inode 91`, and `(root,"archive")->inode 30`. Rename `/projects/alpha` to `/archive/alpha` must atomically remove `(20,"alpha")`, add `(30,"alpha")->91`, update affected directory versions and timestamps, preserve inode 91, and append one recoverable transaction. Readers may see the old or new name according to the consistency contract, but never a committed state where both are absent merely because the implementation performed two uncoordinated writes.

### Connections

[LSDS-011](011-distributed-block-storage.md) supplies stable block identities and the namespace/data-path separation. [LSDS-013](../ROADMAP.md) develops replication and erasure coding; [LSDS-014](../ROADMAP.md) develops data read/write pipelines. [LSDS-003](003-range-hash-and-consistent-partitioning.md) supplies routing epochs, and [LSDS-009](009-cluster-failure-assumptions.md) supplies the failure model.

## Governing Question

Distributed data systems expose names because users and applications cannot organize billions of immutable handles directly. A pathname such as `/research/run-42/events.parquet` looks simple, but resolving and mutating it may require authorization at several ancestors, directory lookups across metadata shards, cache-coherence decisions, quota checks, block-layout metadata, a durable journal commit, and notifications to clients.

The metadata service is usually small in bytes compared with stored data yet dense in dependencies. One rename can touch a source directory entry, destination entry, inode link state, parent timestamps, quotas, snapshots, and audit records. It must not become half visible. A metadata failure can make healthy data blocks unreachable because clients no longer know which identities are current or authorized.

The governing question is therefore not merely where to store file attributes. It is how to make names, identities, transactions, persistence, caching, routing, recovery, and evidence agree. Centralizing authority simplifies transactions but limits memory and request throughput. Partitioning authority adds capacity but creates routing, coordination, and migration problems. Relaxing semantics can remove coordination, but only if the interface states the relaxation honestly.

## Why This Matters

Metadata is on the control path for create, open, stat, list, rename, unlink, permission changes, snapshots, and block discovery. A cluster may deliver terabytes per second of data while failing under a create storm or a single hot directory. Small-file workloads amplify this imbalance because every small payload still needs identities, directory entries, permissions, timestamps, and lifecycle state.

Namespace correctness protects more than convenience. If a rename loses an entry, a dataset becomes unreachable. If an old metadata server remains writable after failover, two histories can authorize different objects under one name. If cache revocation is incomplete, one client can overwrite or expose state based on stale permissions. If snapshots and deletion are reconciled incorrectly, garbage collection can destroy retained evidence.

Recovery time matters separately from steady latency. A compact in-memory namespace can answer reads quickly, but a multi-hour journal replay violates availability objectives. Frequent checkpoints shorten replay and may consume I/O and pause resources. A warm standby reduces failover delay only if it has a complete ordered log and the previous writer is fenced.

Scaling also changes failure blast radius. A single namespace server has one authority boundary. Static federation isolates tenants or workloads but introduces mount-table and cross-volume limitations. Dynamic subtree ownership preserves hierarchical locality yet needs safe migration. Hashing directory entries balances broad workloads but can scatter listings and make one logical directory a distributed transaction surface.

## Prerequisites and Retrieval

Recall partition keys, consistent routing, and epochs from [LSDS-002](002-horizontal-partitioning.md) and [LSDS-003](003-range-hash-and-consistent-partitioning.md). Recall locality and cache tiers from [LSDS-004](004-data-locality.md), execution-graph demand from [LSDS-005](005-distributed-task-graphs.md), serialization from [LSDS-008](008-serialization-across-workers.md), failure assumptions from [LSDS-009](009-cluster-failure-assumptions.md), and resource accounting from [LSDS-010](010-reasoning-about-work-movement-and-state-at-scale.md).

From [LSDS-011](011-distributed-block-storage.md), retrieve the distinctions among pathname, inode/file version, block handle, placement, inventory, and bytes. You should understand trees, maps, logs, checkpoints, transactions, locks, leases, consensus, fencing, caches, snapshots, quotas, Unicode, access control, latency percentiles, and recovery objectives.

## Learning Objectives

After completing this module, you should be able to:

- distinguish path components, directory entries, inodes, file versions, block maps, and physical locations;
- specify path resolution under roots, mount points, links, normalization, and authorization;
- define atomic create, link, unlink, and rename effects using stable identities;
- explain journal durability, sequence numbers, checkpoints, replay, and truncation;
- distinguish active/standby availability from namespace federation and active sharding;
- design fencing and idempotency for metadata failover and client retry;
- evaluate leases, capabilities, cache invalidation, and session recovery;
- compare static partitioning, hashing, dynamic subtrees, and directory fragmentation;
- reason about cross-shard transactions and ownership migration;
- estimate namespace memory, journal rate, checkpoint time, and replay time;
- diagnose hot directories, lock contention, cache pressure, and small-file amplification;
- specify snapshots, quotas, garbage-collection roots, authorization, and audit evidence; and
- design consequence-appropriate validation for a metadata service.

## Core Exposition

### Names, identities, and metadata classes

A pathname is a sequence of names interpreted from a root. It is not the object identity. Renaming a file changes directory mappings while the inode and open handles can remain the same. Hard links let several directory entries identify one inode. Symbolic links store another path-like value and require a new resolution step. Mounts or referrals cross namespace boundaries.

Separate metadata classes because they have different consistency and scaling needs. Namespace metadata includes dentries, inodes, ownership, permissions, timestamps, link counts, layouts, quotas, and snapshot roots. Block metadata maps a file version and offsets to stable block handles. Placement metadata locates block copies. Storage-node inventory reports observed copies. Audit metadata records who requested which operation and outcome.

A durable identity should include a filesystem or namespace identifier plus inode/object number and generation. Reuse without a generation permits a stale handle to name a new object accidentally. Externally exposed file handles must remain interpretable across metadata-server restart or return a precise stale-handle failure.

### Path resolution

Resolve `/a/b/c` by starting from a named root identity and repeatedly looking up `(current_inode, component)`. At each step, verify that the current object is a searchable directory and enforce authorization under the filesystem's credential and ACL semantics. Resolution returns an identity and observed version, not merely a canonical string.

Relative paths add a current-directory identity. `.` and `..`, mount crossings, chroot-like roots, symlinks, case folding, Unicode normalization, trailing separators, reserved names, and maximum traversal depth must be explicit. Normalization before lookup must match creation; otherwise visually or canonically equivalent names can become surprising aliases or bypass policy.

Concurrent mutation makes naïve walks unsafe. An ancestor can be renamed or permissions can change between component reads. Designs use locks, version validation, leases, transactions, or a declared weaker contract. A result should bind the root, identities, versions, credentials, and routing epoch used to obtain it.

### Directory entries and inode invariants

A directory entry maps a name within one parent directory to an inode identity and type hint. The inode owns durable attributes. This split makes rename and hard link manageable: names move or multiply while identity persists. It also means directory-entry type hints and cached attributes can become stale and need validation rules.

Directories form a rooted structure, while hard links to non-directories can make the overall name graph a directed acyclic or general graph depending on semantics. Prevent directory hard links or perform cycle checks so `..`, traversal, and reclamation remain coherent. Link count should equal authoritative directory references plus any contract-specific internal references.

Unlink removes a name, not necessarily the object immediately. Open handles, snapshots, pending transactions, replication/recovery, and retention holds may keep the inode and blocks live. Reclamation begins only after every authoritative root and grace condition releases them.

### Namespace transactions

Define each mutation as preconditions, reads, writes, invariant checks, a linearization point, and a response. Create requires an absent target name, a valid parent, authorization, quota, a fresh identity, and initialized attributes. Link adds a dentry and increments link state atomically. Unlink removes a dentry and updates link state. Rename couples removal and insertion, replacement rules, directory ancestry, and parent attributes.

Atomic does not necessarily mean globally serializable. State the scope: one directory, one shard, one namespace, or a transaction group. Also state visibility to concurrent reads, list operations, caches, snapshots, and retries. An operation ID makes a retry return the original outcome rather than applying the mutation twice.

Locks can protect in-memory structures, but durable atomicity comes from a recoverable commit protocol. Fine-grained locks improve concurrency while introducing lock ordering and deadlock risks. Optimistic version checks reduce uncontended locking but retry under hotspots. Distributed transactions add prepare/commit state and recovery obligations.

### Journals, checkpoints, and replay

An ordered metadata journal records transactions with sequence numbers, checksums, transaction boundaries, and enough information for deterministic redo or state-machine replay. A success response should correspond to the documented durability point: memory, local persistent media, replicated quorum, or another explicit contract.

A checkpoint is a consistent materialization of namespace state at log position `k`. Recovery loads that image, validates its identity and checksum, then replays committed entries with sequence greater than `k` in order. It must reject gaps, corrupt records, incompatible versions, and uncommitted partial tails rather than invent state.

Checkpoint creation must capture a consistent version while mutations continue or establish a bounded pause. Publishing a checkpoint is itself atomic: write and verify a candidate, then install a manifest that binds image digest, format, namespace identity, and included log position. Retain an older known-good image until the new one is proven usable.

Journal retention follows confirmed recovery consumers. Truncating because a checkpoint file merely exists can strand a standby that has not installed it. Monitor log bytes and age, checkpoint duration, replay rate, consumer lag, corruptions, and restore trials.

### High availability and fencing

Active/standby metadata servers provide redundant execution for one namespace authority. The standby tails the ordered journal or replicated state machine and may keep a warm in-memory view. Failover selects a new active only after proving it has the required committed prefix and fencing the previous active's ability to write journals, publish checkpoints, grant leases, or authorize data mutations.

Failure detection alone is not fencing. A paused process or partitioned host can resume. Use quorum leadership terms, storage write epochs, revoked credentials, power/network fencing, or another mechanism that the old authority cannot bypass. Every mutation and delegated token should carry a term/epoch that storage and peers validate.

Read-only followers or observers can scale metadata reads, but their staleness contract must be visible. A client that just created a file may require session or read-after-write routing to an authority at least as current as its observed commit index.

### Leases, capabilities, and client caches

Client metadata caches eliminate repeated RPCs for hot paths and attributes. Cache safety requires a validity rule: immutable version, time-bounded lease, server-revocable capability, validation token, or a deliberately weak TTL contract. A cached pathname result must usually bind parent identity/version and target generation.

Capabilities can delegate specific rights such as reading attributes, buffering file writes, or caching directory entries. Granularity improves concurrency but enlarges revocation state. Before a conflicting mutation commits, the authority may need acknowledgements that incompatible capabilities are returned or fenced.

Lease duration trades steady RPC load against failure and revocation delay. Clock uncertainty, session identity, reconnect, duplicate revocation, lost acknowledgement, and server epoch changes require design. Expiry is not sufficient if a client can continue writing to storage nodes with an unfenced old token.

### Snapshots and namespace versions

A snapshot names an immutable logical view. It needs a snapshot ID, root identity, creation transaction/log position, policy, and references to retained inode/data versions. A timestamp alone is not a complete snapshot identity because clocks can collide or skew.

Copy-on-write can share unchanged metadata and blocks. Mutation creates new versions along the affected path or records deltas while the snapshot retains old references. Snapshot deletion removes a root; asynchronous reclamation must respect other snapshots, clones, open handles, legal holds, and replication state.

Snapshot semantics should say whether open/uncommitted writes are included, whether the namespace and referenced data are mutually consistent, how quotas charge shared bytes, and what restore does to newer paths. A crash-consistent filesystem snapshot is not automatically an application-consistent database backup.

### Namespace partitioning choices

A single active metadata authority offers the simplest global transaction boundary and strong locality in one memory image. It scales vertically and can support very high request rates, but memory, CPU, lock contention, journal throughput, and failover recovery create ceilings.

Static federation assigns independent roots or volumes to different metadata authorities. It scales and isolates failure/load, but administrators or routing layers decide boundaries. Cross-volume rename may be unsupported or degrade to copy-and-delete. Global listings, quotas, snapshots, and policy become compositions of separate authorities.

Hash partitioning spreads dentries or inodes by key, balancing many independent names. It scatters hierarchical locality and directory listings, and cross-parent mutations often span shards. Range partitioning preserves ordered scans but risks skew. Directory fragmentation hashes entries only for hot directories, keeping cold subtrees local.

Dynamic subtree partitioning assigns hierarchical regions to active metadata servers and moves boundaries with demand. It preserves common path locality and adapts to workloads, but migration needs ownership epochs, state transfer, forwarding, cache/capability handoff, and a safe cutover.

### Routing and ownership epochs

Clients need to find the authority for a path or identity. They can contact a root/router, follow referrals, consult a versioned shard map, or cache prior routes. A routing answer must carry an epoch and authoritative redirect path. Redirect loops and split ownership indicate control-plane failure.

During migration, distinguish source owner, target owner, and committed routing map. One safe pattern transfers a snapshot and journal delta, quiesces or forwards new mutations, commits ownership in a consensus-controlled map, fences the source for the new epoch, then retires forwarding after caches converge.

Identity-based routing survives rename better than full-path hashing. Path-based sharding makes the owner change whenever an ancestor moves. Hybrid schemes keep subtree locality while using stable subtree IDs in the routing map.

### Cross-shard mutations

A rename between metadata shards cannot be implemented as independent unlink and create if atomic rename is promised. It needs a coordinator or deterministic ownership rule, participant locks/version reservations, a durable decision, idempotent commit/abort, and recovery from coordinator or participant failure.

Two-phase commit can preserve atomicity but may block when the coordinator's decision is unavailable unless the decision is replicated and recovery is carefully designed. A shared consensus log provides strong ordering at a scaling cost. Ownership co-location avoids many distributed transactions but can concentrate hot workloads.

Some systems explicitly forbid cross-volume atomic rename. That is a valid design when the API exposes the boundary. Silently implementing copy then delete changes identity, failure behavior, quota, permissions, and partial visibility and is not equivalent.

### Hotspots, small files, and concurrency

Metadata load is measured in operations, touched items, lock/transaction scope, journal bytes, and cache working set—not payload bytes. A million zero-byte file creates can be more stressful than reading one terabyte file. Recursive scans and directory listings create read amplification and cache churn.

A hot single directory defeats coarse subtree partitioning. Directory fragmentation, batched create, per-client staging areas, or application-level name bucketing can spread work. Each alters listing order, transaction scope, operational complexity, or user-visible layout.

Global locks, root/ancestor locks, allocator locks, quota counters, journal flushes, capability recalls, and a single RPC queue can serialize otherwise independent requests. Measure queueing and lock hold/wait by operation and key. Aggregate CPU below 100% does not prove spare capacity when one authority thread is saturated.

### Capacity and recovery accounting

Namespace memory includes inode records, dentries, block references, snapshots, ACLs/xattrs, routing state, leases/capabilities, indexes, object overhead, allocator fragmentation, and runtime caches. Use measured distributions rather than one average multiplied by file count. Millions of small files usually make per-object overhead dominant.

Journal rate equals mutation rate times encoded bytes plus batching/replication overhead. Checkpoint time depends on state size, serialization, storage/network bandwidth, consistency mechanism, and competing traffic. Recovery time includes checkpoint fetch/validation, replay, index/cache reconstruction, role election, fencing, client reconnect, and storage inventory reconciliation.

Provision headroom for bursts, failover, migration, snapshots, replay, and cache recall. A standby with equal steady memory can still fail during recovery if replay temporarily holds old and new structures. Test maximum supported state, not only average production state.

### Security, tenancy, and audit

Authorization belongs in path resolution and mutation, not only at mount time. Traversing a path can require search permission on each directory. ACLs, ownership, groups, capabilities, impersonation, tenant roots, and administrative bypasses need explicit evaluation order and versioning.

Metadata leaks names, dataset structure, sizes, timestamps, ownership, and research or customer activity even when file bytes are encrypted. Protect RPCs, journals, checkpoints, snapshots, diagnostics, and backups. Separate tenant identities and namespace IDs so a block or inode handle cannot cross boundaries accidentally.

Audit records should bind authenticated principal, effective credentials, namespace and object identities, operation ID, old/new names where policy permits, authorization decision, metadata epoch/transaction, result, and time source. Logs need integrity, retention, minimization, and access controls; indiscriminate full paths can expose sensitive names.

### Observability and evidence

Track request rate and latency by operation, success/error/retry, shard, directory/inode, tenant, and consistency path. Add lock waits, transaction conflicts, journal append/fsync latency, checkpoint age/duration, replay throughput, standby lag, failover duration, routing redirects, capability recall latency, cache hit/miss, and memory by metadata class.

Cardinality requires care. Raw pathnames and object IDs are sensitive and unbounded label values. Use sampled traces, protected drill-down indexes, heavy-hitter sketches, and bounded buckets. Preserve transaction IDs and epochs in traces so a timeout can be followed through retry and recovery.

A correctness claim requires history-based concurrency tests, crash injection around commit/checkpoint boundaries, stale-authority and stale-client tests, snapshot/reclamation tests, and restore drills. A scalability claim requires workload distributions including hot directories, cold trees, small files, cross-shard operations, cache state, and failures. Neither follows from a microbenchmark of cached `stat` calls.

## Definitions and Notation

Let namespace state at committed version `v` be `N_v=(D_v,I_v,S_v,Q_v)`: directory map `D`, inode/attribute map `I`, snapshot roots `S`, and quota/accounting state `Q`. A dentry key `(p,n)` combines stable parent inode `p` and normalized component `n`; its value is a generation-qualified target identity `i`.

Path resolution `R(N_v,r,[n_1,...,n_k],c)` starts at root `r`, applies `D_v` component by component, and evaluates credential context `c`. Its result includes target identity and observed versions or a precise failure. Symlink and mount traversal extend the state machine and must have loop/depth bounds.

A transaction `T=(id,pre,read,write,e)` has idempotency ID, version/identity preconditions, read set, write set, and authority epoch `e`. If committed at log sequence `s`, applying all committed transactions through `s` yields `N_s`. Atomicity requires no externally visible state containing only a strict subset of `write(T)`.

Let checkpoint `C_k` encode a valid `N_k`. Let journal suffix `J_(k,s]` contain complete ordered committed transactions `k+1` through `s`. Correct recovery satisfies `Replay(C_k,J_(k,s])=N_s`. Sequence gaps, duplicate non-idempotent application, or an uncommitted tail violate the premise.

Let routing map `M_e` assign each metadata ownership unit `u` to an authority under epoch `e`. A request valid in `e` must be executed by the assigned, unfenced authority or redirected with evidence of a later map. Migration changes `M_e` while preserving one commit authority per unit and declared operation semantics.

For item count `x_j` and measured resident bytes `b_j` in metadata class `j`, estimated resident state is `B=sum_j(x_j*b_j)+B_runtime`. If usable occupancy target is `rho` with `0<rho<1`, installed memory must be at least `B/rho` before failover/replay headroom and replicas. Treat averages and occupancy as assumptions, not universal constants.

## Mechanisms, Invariants, or Proof Structure

To design or audit a metadata namespace:

1. Define roots, names, normalization, stable identities, generations, and handle lifetime.
2. Specify path traversal, links, mounts, permissions, and concurrent-ancestor behavior.
3. Model every mutation with preconditions, invariant-preserving writes, idempotency, and visibility.
4. Bind success to a named journal/consensus durability and sequence position.
5. Define checkpoint creation, publication, validation, replay, retention, and restore evidence.
6. Specify leadership, fencing, standby freshness, client sessions, and cache/capability invalidation.
7. Select ownership units, routing epochs, hotspot policy, migration, and cross-shard semantics.
8. Protect snapshot/open-handle/retention roots through garbage collection.
9. Account memory, journal, checkpoint, replay, lock, RPC, and cache resources under real distributions.
10. Test concurrency, crash boundaries, stale actors, corruption, overload, migration, and recovery.

The fixture below models a tiny versioned directory map and an atomic rename with inode/version preconditions. It also estimates selected resident metadata classes. It is an executable reasoning aid, not a production filesystem, authorization system, persistent journal, or distributed transaction protocol.

<!-- bijux-verify: {"id":"namespace-transaction-accounting","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"before_projects=inode-91 before_archive=None\ncommit_seq=4 moved_inode=inode-91\nafter_projects=None after_archive=inode-91\nstale_retry=precondition_conflict snapshot_projects=inode-91\nresident_bytes=9173145600 installed_at_75pct=12230860800\n","stderr":""}} -->
```python
MIB = 1024 * 1024

directory = {
    ("inode-1", "projects"): "inode-20",
    ("inode-1", "archive"): "inode-30",
    ("inode-20", "alpha.parquet"): "inode-91",
}
versions = {"inode-1": 1, "inode-20": 7, "inode-30": 2}
snapshot_directory = dict(directory)
log_seq = 3


def lookup(parent, name, view):
    return view.get((parent, name))


def atomic_rename(source_parent, source_name, target_parent, target_name,
                  expected_source, expected_source_version,
                  expected_target_version):
    global log_seq
    source_key = (source_parent, source_name)
    target_key = (target_parent, target_name)
    if (
        directory.get(source_key) != expected_source
        or versions[source_parent] != expected_source_version
        or versions[target_parent] != expected_target_version
        or target_key in directory
    ):
        return "precondition_conflict", None

    candidate = dict(directory)
    moved = candidate.pop(source_key)
    candidate[target_key] = moved
    directory.clear()
    directory.update(candidate)
    versions[source_parent] += 1
    versions[target_parent] += 1
    log_seq += 1
    return "committed", moved


print(
    "before_projects="
    f"{lookup('inode-20', 'alpha.parquet', directory)} "
    "before_archive="
    f"{lookup('inode-30', 'alpha.parquet', directory)}"
)
status, moved = atomic_rename(
    "inode-20", "alpha.parquet", "inode-30", "alpha.parquet",
    "inode-91", 7, 2,
)
assert status == "committed"
print(f"commit_seq={log_seq} moved_inode={moved}")
print(
    "after_projects="
    f"{lookup('inode-20', 'alpha.parquet', directory)} "
    "after_archive="
    f"{lookup('inode-30', 'alpha.parquet', directory)}"
)
stale_status, _ = atomic_rename(
    "inode-20", "alpha.parquet", "inode-30", "other.parquet",
    "inode-91", 7, 2,
)
print(
    f"stale_retry={stale_status} snapshot_projects="
    f"{lookup('inode-20', 'alpha.parquet', snapshot_directory)}"
)

resident_bytes = (
    13_000_000 * 320  # inodes
    + 13_000_000 * 160  # directory entries
    + 72_000_000 * 32  # block references
    + 600 * MIB  # runtime indexes, sessions, and caches in this model
)
installed_at_75pct = (resident_bytes * 4 + 2) // 3
print(
    f"resident_bytes={resident_bytes} "
    f"installed_at_75pct={installed_at_75pct}"
)
```

The rename publishes a complete candidate map only after every precondition passes. A repeated stale request cannot remove the destination or recreate the source. The copied snapshot still resolves the pre-rename name. Real implementations need locks or optimistic concurrency, durable log ordering, authorization, replacement rules, crash recovery, and multi-server coordination.

Proof obligations differ. Namespace safety proves structural invariants and atomic visibility. Recovery proves checkpoint-plus-log equivalence. High availability proves one writable authority per epoch and bounded failover under named faults. Cache coherence proves conflicting rights are revoked or fenced. Scalability claims require measured workload and resource evidence.

## Alternatives and Trade-Offs

A single active namespace provides a straightforward global order and avoids distributed metadata transactions. Its limits are vertical memory/CPU, shared locks, journal service, and failover recovery. Read replicas help read-heavy workloads but do not remove the mutation authority bottleneck.

Active/standby improves availability but not write scaling. Active/active sharding improves aggregate capacity while adding routing, migrations, distributed operations, and larger failure state. Calling two standbys “three metadata servers” does not mean three-way write throughput.

Static federation gives clear isolation and independent failure domains. It makes boundaries durable operational concerns and weakens global operations. A router or mount table can present one view but cannot manufacture atomic cross-namespace transactions without participating authorities.

Subtree partitioning preserves hierarchical locality and efficient recursive work. It can hotspot at one busy subtree. Hashing balances independent entries but fans out listings and parent-scoped operations. Directory fragmentation combines approaches at the cost of per-directory shard metadata.

Pessimistic locking gives predictable conflict control but can deadlock or convoy. Optimistic concurrency performs well with low contention but retries under hotspots. Leases amortize coordination while extending stale-client recovery. Capabilities are more expressive and more stateful.

Write-ahead logs support incremental persistence and replay. Copy-on-write trees can make checkpoints and snapshots cheap but complicate space reclamation. Periodic full images bound replay while consuming serialization bandwidth. Incremental checkpoints reduce work but lengthen dependency chains and restore complexity.

Strict POSIX-like semantics ease application reasoning and require coordination. Session, close-to-open, or bounded-staleness contracts can improve caching and availability. A relaxed contract is useful only when applications can observe and handle it.

Synchronous metadata durability narrows acknowledged-loss windows at latency cost. Group commit amortizes flushes and introduces batch delay. Asynchronous acknowledgement can be fast but must state that acknowledged operations may disappear after failure.

## Failure Modes and Misconceptions

- **“The path is the file ID.”** Rename and hard links disprove this; use stable generation-qualified identity.
- **“A directory is just a map.”** It also participates in traversal permissions, link/cycle rules, transactions, quotas, snapshots, and cache coherence.
- **“Rename is copy then delete.”** That changes identity and exposes partial failure unless the interface explicitly defines a cross-volume copy operation.
- **“An edit log file means mutations are durable.”** Durability depends on transaction framing, flush/quorum acknowledgement, checksums, and recoverable ordering.
- **“A checkpoint is a backup.”** A checkpoint may share failure domains and may omit data bytes, keys, configuration, audit, or application consistency.
- **“A secondary NameNode is automatically a hot standby.”** Checkpoint production and failover authority are different roles.
- **“Leader election prevents split brain.”** The obsolete writer must be fenced at every mutation sink.
- **“TTL caching is coherent.”** TTL bounds time but does not guarantee conflicting mutations wait for invalidation.
- **“More MDS processes means more write throughput.”** Standbys improve availability; only active partitioned ownership can increase aggregate authority throughput.
- **“Hash sharding solves hotspots.”** One popular name/inode, shared quota, journal, or cross-shard transaction can still serialize work.
- **“Equal inode counts mean balanced load.”** Operation mix, directory fan-out, cache locality, ACL size, block references, and client contention differ.
- **“Data availability implies namespace availability.”** Healthy blocks can be inaccessible when metadata authority or routing fails.
- **“Unlinked means deletable.”** Open handles, snapshots, clones, holds, and pending recovery can retain the object.
- **“Snapshot time identifies exact state.”** Use a transaction/log position and snapshot ID; clocks are insufficient.
- **“Cached permission checks remain safe after policy change.”** Credential, ACL, parent, capability, and authority versions must invalidate incompatible decisions.
- **“A successful retry is a second successful mutation.”** Idempotency should return the original outcome without reapplying effects.
- **“Fast cached stat proves namespace scalability.”** It omits mutations, journals, misses, hot directories, failover, and recovery.
- **“Average metadata bytes per file is enough.”** Tail distributions, object overhead, snapshots, leases, and replay headroom matter.
- **“Replication makes bad metadata correct.”** Replicas can consistently preserve the same invalid transaction; invariants and recovery validation remain necessary.
- **“Internal validation certifies legal retention or research governance.”** Domain authorities must approve consequence-bearing lifecycle rules.

## Worked Examples

### Example 1

**Situation:** `/teams/a/report` is renamed to `/archive/report` within one authority. **Reasoning:** Resolve both parents to stable identities, validate source identity/generation and destination rule, lock or version-reserve both dentries in deterministic order, update removal/insertion and parent attributes in one journaled transaction, preserve the file inode, publish once, and invalidate caches. The payload blocks need not move.

### Example 2

**Situation:** The same rename crosses two independent federated namespaces. **Reasoning:** If the interface does not provide distributed atomic rename, return a cross-device/boundary error. A client may explicitly copy, validate, and delete, but that has new identity, quota, permissions, time, and partial-failure semantics.

### Example 3

**Situation:** An active metadata server stops heartbeating, a standby wins election, and the old process resumes. **Reasoning:** Election is insufficient. The new term must fence the old server's journal writes, checkpoint publication, metadata tokens, and data-node mutation authority before acknowledging new commits.

### Example 4

**Situation:** Checkpoint `C_800` exists; the journal contains committed 801–845 plus a partial record 846. **Reasoning:** Validate the checkpoint and contiguous framed journal, replay 801–845 exactly once, reject/truncate the uncommitted tail according to protocol, and recover `N_845`. Never infer commitment from bytes merely present at EOF.

### Example 5

**Situation:** A client caches `(parent 20,"alpha")->inode 91` under a capability; another client renames it. **Reasoning:** The metadata authority must revoke or downgrade the incompatible capability and wait/fence according to contract before publishing the rename. A bare cache TTL permits stale observations until expiry and is a weaker interface.

### Example 6

**Situation:** One directory receives 250,000 creates per second while other subtrees are idle. **Reasoning:** Moving whole cold subtrees will not split this key. Consider directory fragmentation, application buckets, batch allocation, and journal/allocator sharding; then test listing, rename, quota, ordering, and recovery costs.

### Example 7

**Situation:** Thirteen million inodes average 320 resident bytes, thirteen million dentries 160 bytes, 72 million block references 32 bytes, and runtime state is 600 MiB. **Reasoning:** The fixture totals 9,173,145,600 bytes. At 75% occupancy, ceiling division requires 12,230,860,800 bytes before standby duplication and transient recovery headroom.

### Example 8

**Situation:** An inode has no live dentry after unlink but remains open and appears in two snapshots. **Reasoning:** Its live namespace link count can be zero while open-handle and snapshot roots retain versions. Reclamation waits until those roots, holds, and safety grace expire; storage inventory alone cannot authorize deletion.

### Example 9

**Situation:** A read-only metadata follower is 500 transactions behind. **Reasoning:** It may serve explicitly bounded-stale reads. A client carrying a just-observed commit index must route to an authority/follower at least that current to obtain read-after-write behavior.

### Example 10

**Situation:** A clinical research namespace needs a recovery claim. **Reasoning:** Test encrypted checkpoint restore, contiguous journal replay, identity/generation preservation, permissions and audit integrity, snapshot/hold retention, key availability, fenced failover, and representative application consistency. Obtain named privacy, security, records, research-governance, and recovery review; a metadata checksum alone is insufficient.

## Cross-Program Connections

[Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) supplies trees, tries, hash tables, copy-on-write structures, indexes, reference counts, and garbage collection. [Database Engineering](../../18-database-engineering/ROADMAP.md) supplies transactions, write-ahead logs, checkpoints, MVCC, concurrency control, and recovery.

[Operating Systems](../../22-operating-systems/ROADMAP.md) supplies inodes, dentries, links, path traversal, permissions, page cache, and local filesystem persistence. [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) owns consensus, leader terms, fencing, leases, distributed transactions, linearizability, and fault models.

[Security Engineering](../../25-security-engineering/ROADMAP.md) supplies authentication, authorization, capability discipline, key management, audit integrity, and tenant isolation. [Network Engineering](../../24-network-engineering/ROADMAP.md) supplies RPC failure, partitions, topology, latency, and load balancing.

[Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md) owns authoritative identifiers, retention, lineage, data domains, residency, and recovery policy. [Platform Engineering](../../29-platform-engineering/ROADMAP.md) owns service provisioning, tenancy, observability, upgrades, capacity, and operational objectives.

GFS illustrates centralized master metadata separated from direct chunkserver data transfer. HDFS documents NameNode namespace state, image/edit-log persistence, HA fencing, and independent federated namespaces. CephFS demonstrates a resizable MDS cluster, client capabilities, metadata journaling in RADOS, and dynamic subtree partitioning. NFSv4 documents a filesystem namespace that can traverse server boundaries through referrals and locations.

## References

- Sanjay Ghemawat, Howard Gobioff, and Shun-Tak Leung, [*The Google File System*](https://research.google/pubs/the-google-file-system/), SOSP, 2003. Primary master metadata, namespace, operation log, checkpoint, lease, and direct-data-path design.
- Apache Hadoop Project, [*HDFS Architecture*](https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html), checked 2026-09-03. Official current NameNode namespace, block map, edit log, image, checkpoint, and DataNode separation documentation.
- Apache Hadoop Project, [*HDFS High Availability Using the Quorum Journal Manager*](https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-hdfs/HDFSHighAvailabilityWithQJM.html), checked 2026-09-03. Official active/standby, shared edits, automatic failover, and fencing guidance.
- Apache Hadoop Project, [*HDFS Federation*](https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-hdfs/Federation.html), checked 2026-09-03. Official independent namespaces, block pools, namespace volumes, scalability, and isolation model.
- Apache Hadoop Project, [*HDFS NameNode Fine-Grained Locking*](https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-hdfs/NamenodeFGL.html), checked 2026-09-03. Official current namespace, block-management, path, inode, and global lock design context.
- Sage A. Weil et al., [*Ceph: A Scalable, High-Performance Distributed File System*](https://www.usenix.org/event/osdi06/tech/full_papers/weil/weil.pdf), OSDI, 2006. Primary decoupled metadata/data paths and dynamic subtree partitioning design.
- Ceph Foundation, [*Ceph File System*](https://docs.ceph.com/en/latest/cephfs/), checked 2026-09-03. Official current MDS cluster, RADOS metadata journal, direct data access, and coherent client-cache overview.
- Ceph Foundation, [*Configuring Multiple Active MDS Daemons*](https://docs.ceph.com/en/latest/cephfs/multimds/), checked 2026-09-03. Official current dynamic subtree, static pinning, ephemeral pinning, and balancing guidance.
- Ceph Foundation, [*MDS Cache Configuration*](https://docs.ceph.com/en/latest/cephfs/cache-configuration/), checked 2026-09-03. Official capabilities, directory-entry leases, recall, cache pressure, and memory controls.
- David Noveck and Charles Lever, [*Network File System (NFS) Version 4 Protocol*](https://www.rfc-editor.org/rfc/rfc7530), RFC 7530, 2015. Standards-track filesystem, state, locking, rename, filehandle, and multi-server namespace semantics.

## Exercises

### Exercise 1

Specify the complete metadata transaction for renaming `/a/x` to `/b/y` when `y` already names another file and replacement is allowed. Include identities, preconditions, invariants, persistence, caches, retry, and reclamation.

### Exercise 2

A checkpoint includes transaction 40,000. The journal has complete committed entries 40,001–46,000 at 75,000 replayed operations per second and a corrupt gap at 45,100. Calculate the ideal replay time without the gap, then state the correct recovery response.

### Exercise 3

Compare active/standby, static federation, hash-sharded dentries, and dynamic subtree partitioning for a workload with many tenant roots plus one directory receiving most creates.

### Exercise 4

Estimate resident metadata and 70%-occupancy installed memory for 20 million inodes at 400 bytes, 25 million dentries at 180 bytes, 100 million block references at 40 bytes, and 1.5 GiB runtime state. State omitted terms.

### Exercise 5

Design validation and review evidence for migrating an irreplaceable public-records archive subtree between metadata shards while clients remain active.

## Answers to the Exercises

### Answer 1

Resolve `/a`, `/b`, source `x`, and destination `y` to generation-qualified identities under one root/routing epoch and credentials. Preconditions bind source/destination parent versions, source identity, replacement target identity/type, ancestry, authorization, quotas, holds, and idempotency ID. One transaction removes `(a,x)`, replaces `(b,y)` with the source identity, updates both parents and link/reclamation state for the displaced inode, preserves rename/cycle rules, and commits at one durable log sequence. Revoke incompatible caches/capabilities before promised visibility. Retry returns the recorded result. The displaced inode is reclaimed only after links, opens, snapshots, holds, and grace roots release it.

### Answer 2

There are 6,000 journal entries, so ideal replay is `6000/75000=0.08` seconds before decoding, I/O, validation, indexes, and role transition. The corrupt gap destroys the premise of a contiguous authoritative suffix. Stop normal promotion, retry from independent verified journal copies or an alternate checkpoint/log chain, preserve evidence, and escalate recovery policy. Skipping entry 45,100 would invent a state and can violate namespace invariants.

### Answer 3

Active/standby provides simple semantics and fast failover but leaves the one-active throughput ceiling. Static federation maps tenant roots to independent authorities, giving isolation and scalable aggregate load, yet the hot directory still saturates its namespace and cross-root operations weaken. Hashing its dentries can distribute creates but fans out listings and makes parent-scoped or cross-entry operations coordinated. Dynamic subtrees balance tenant roots and preserve locality but cannot split one hot directory unless directory fragmentation is added. A plausible design federates strong isolation domains, uses active HA per domain, dynamically assigns normal subtrees, and explicitly fragments the exceptional directory after validating its listing, rename, quota, and recovery semantics.

### Answer 4

The selected state is `20,000,000*400 + 25,000,000*180 + 100,000,000*40 + 1.5*2^30 = 18,110,612,736` bytes. At 70% target occupancy, installed memory is at least `ceil(18,110,612,736/0.70)=25,872,303,909` bytes, about 24.10 GiB. Omitted terms include ACLs/xattrs, snapshots, versions, quotas, leases/capabilities, routing, language/container overhead, allocator fragmentation, indexes, journals, checkpoint buffers, failover duplication, replay transients, monitoring, kernel memory, and distribution tails.

### Answer 5

Record source subtree identity, snapshot/log position, source and target ownership epochs, routing-map decision, complete metadata-state digest or invariant inventory, active capabilities/sessions, authorization, open handles, snapshots/holds, quotas, and referenced block versions. Exercise concurrent reads, creates, rename in/out, retry, source/target crash, routing-cache staleness, journal corruption, rollback, and old-owner fencing. Verify transfer snapshot plus deltas, one commit authority at cutover, idempotent cross-shard decisions, cache handoff, preserved file handles, audit continuity, and no early reclamation. Measure outage, redirect/retry tails, backlog, and recovery. Named reviewers should include storage/filesystem operators, distributed-systems and security engineers, records/legal authorities, archive custodians, accessibility and user representatives, and independent recovery assurance. Internal checks do not constitute statutory records approval.
