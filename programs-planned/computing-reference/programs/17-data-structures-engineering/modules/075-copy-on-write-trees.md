---
module_id: DSE-075
program: Data Structures Engineering
level: 2
module_number: 75
title: Copy-on-Write Trees
status: complete
last_verified: 2026-08-30
---

# Copy-on-Write Trees

## One-Page Review

### Governing question

How can a tree publish durable updates by writing a new root-reachable version while preserving old snapshots, preventing premature reuse, and bounding write and space amplification?

### Essential definitions

- **Copy-on-write (CoW)** leaves published nodes immutable; an update allocates replacements and publishes a new root that reaches the new version.
- **Path copying** recreates each node from a changed leaf to the root while reusing unchanged subtrees.
- A **version/root generation** identifies one immutable logical tree image; multiple live roots may share nodes.
- A **snapshot** pins a root/version. A clone creates a writable lineage initially sharing that root's reachable nodes.
- A **shadow/private tree** is constructed outside the published namespace until its root is durably selected.
- **Reachability** is graph membership from every live root, not merely the current root.
- **Reference count/backreference** records sharing explicitly; **tracing** instead computes reachability from roots. Both require crash-consistent ownership.
- **Root publication** changes the authoritative root/generation only after all newly referenced descendants and required allocation metadata are durable.

### Central model, mechanism, or theorem

In an immutable tree of height h, an update without structural fan-out copies `O(h)` nodes and shares everything off the search path. A split/merge can copy additional siblings and ancestors but remains proportional to the structurally modified paths under the variant's bounds. If k nodes are copied and page size is P, metadata write volume is at least roughly kP plus root/allocation/checksum overhead; CoW trades simpler version atomicity and snapshots for write and space amplification.

Let `Roots_live` include the current root, snapshots, clones, readers, backups, replicas, and recovery checkpoints that still matter. A node is reclaimable only if it is unreachable from the complete live-root set and no in-flight I/O/log/reference can resurrect or address its generation. Publishing a new current root does not make the old path free while an old root remains live.

Crash safety follows a scoped protocol: allocate and write new children; verify checksums and identities; write copied ancestors whose child references include those checksums/generations; satisfy durability; atomically select a new root record with monotone generation and checksum; recover by choosing the newest valid fully reachable root. CoW alone does not guarantee atomic sector writes, flush ordering, correct free-space metadata, or application `fsync` semantics.

### Critical invariants

1. Published nodes are immutable for their lifetime; updates never overwrite bytes reachable by a live root.
2. Each root reaches a structurally valid ordered tree and nodes/blocks with matching identity, generation, type, and checksum.
3. The new root represents the abstract update; the old root remains the exact old logical value.
4. Untouched subtrees may be shared, but ownership accounting reflects every live reference or root reachability.
5. New descendants become durable before the root that references them is selected.
6. Reclamation/reuse cannot race readers, snapshots, clones, I/O completion, WAL/intent records, replication, or recovery.
7. Space exhaustion, failed publication, and crash leave a recoverable old or new version plus reconcilable private garbage.

### Common failures

- Copying only the modified leaf while mutating a published parent pointer in place.
- Treating language-level object immutability as durable CoW without allocation, flush, root, and recovery rules.
- Publishing a new root before descendant writes or device barriers complete.
- Freeing old path nodes after commit without considering snapshots, readers, clones, backups, or replicas.
- Updating reference counts in place and making the ownership metadata less crash-safe than the tree.
- Storing a checksum beside the same damaged block and claiming end-to-end parent-child authentication.
- Assuming CoW removes all logging needs, including synchronous-write intent, allocator recovery, or logical transactions.
- Ignoring fragmentation and free-space pressure until CoW cannot allocate the pages required to commit.

### Compact example

A balanced immutable BST contains `2,4,6,8,10,12,14`. Inserting 13 creates a leaf 13 and copies nodes 14, 12, and 8. Nodes 2,4,6,10 are shared by identity. The old root still excludes 13; the new root includes it. With both roots live, none of the eleven distinct allocated nodes is reclaimable. After dropping the old root, its three replaced path nodes become unreachable.

### Connections

DSE-033 provides balanced tree invariants, DSE-071 page durability, DSE-072/073 multiway routing, DSE-067 generation/ABA concerns, and DSE-074 atomic root generation publication. Filesystems, databases, immutable functional structures, MVCC, snapshot replication, and backup systems all refine the same live-root/reachability idea.

## Governing Question

How do path copying and atomic root selection become a complete storage protocol rather than a slogan that hides allocator, snapshot, durability, reclamation, and performance failures?

## Why This Matters

In-place tree updates require recovery to interpret partially changed pages and structural operations. CoW instead builds a new version while the old version stays readable. A single root switch can publish a whole graph. Snapshots are cheap because they retain a root rather than duplicate every node; readers can traverse immutable versions without observing partial mutation; backups and replication can identify version boundaries.

The trade is displaced complexity. One logical update can rewrite a leaf-to-root path and amplify small changes into full-page writes. Old and new graphs share nodes, so reclamation becomes global version accounting. Physical allocation fragments over time. A nearly full device may be unable to complete a CoW update even though the logical replacement would not grow data. Root records, free-space trees, reference counts, checksums, and synchronous semantics still need carefully ordered recovery.

CoW is also used too casually in memory. A persistent functional tree can prove old-version immutability, yet say nothing about durable bytes or concurrent memory reclamation. Conversely, a filesystem may group many changes into transaction generations and use extra intent logging for synchronous promises. This module keeps abstract persistence, durable shadow paging, snapshots/clones, and product-specific transaction protocols distinct.

## Prerequisites and Retrieval

Retrieve:

- ordered-tree range/balance invariants, path length, split/merge, and structural induction;
- immutable values, structural sharing, alias identity, and persistent functional updates;
- page IDs/generations, checksums, allocation/free space, flush/barrier, torn write, and root metadata;
- MVCC snapshots, epochs/hazard reclamation, ABA, reference counts, tracing, and replication retention;
- crash consistency, idempotent recovery, fault injection, reachability audit, and amplification measurement.

Diagnostic retrieval: if a height-three update copies a leaf and three ancestors, an old snapshot shares every off-path subtree. The four old path nodes are not automatically free: the old root still reaches them. Reclamation is a property of all live roots and outstanding references, not of the current root alone.

## Learning Objectives

After this module, you can:

1. define immutable nodes, path copying, root versions, snapshots, clones, and live-root reachability;
2. prove old/new abstract semantics and structural sharing for tree updates;
3. derive height-related metadata write amplification and explain its limitations;
4. design page IDs/generations, child authentication, root rings/slots, and flush ordering;
5. compare reference counting, backreferences, tracing, epochs, and delayed free for shared graphs;
6. handle splits, merges, batches, synchronous promises, ENOSPC, crash, and allocator recovery;
7. specify snapshot/clone/delete, backup, replication, migration, scrub, and rollback operations;
8. validate logical versions, page bytes, root selection, reachability, ownership, faults, and performance separately.

## Core Exposition

**Start with abstract persistence.** Model a tree value as an immutable root reference. `update(root,key,value)` returns `root'`; it never changes any node reachable from root. Recursive descent returns a new changed child, then creates a new parent with that child and all unchanged child references reused. Induction proves root still denotes the old map and root' the updated map if the local transformation preserves ordering/balance.

**Identity differs from equality.** A shared subtree is the same node/block referenced by multiple versions, not merely an equal copy. Tests should inspect object/page identities and reachability as well as key-value equality. Deduplication may later make separately created equal blocks shared, but that introduces hashing, collision, encryption, privacy, and reference-accounting obligations not inherent to CoW.

**Path copying extends through structural changes.** Inserting into a multiway leaf may fit by copying the leaf and every ancestor. A split allocates left/right results and copies the parent with a new separator; propagation may reach a new root. Deletion/merge can copy siblings and ancestors. Batch nearby updates together to avoid repeatedly copying shared prefixes, but preserve deterministic conflict/order semantics and bound dirty memory.

**Give every durable block an identity.** A child reference should identify location, generation/birth transaction, type/level, encoded length, checksum algorithm/value, and perhaps compression/encryption context. The child validates its own header and the parent-held expectation. Page generations prevent stale I/O or references from accepting a recycled location. Fixed endian/version and checked parsing remain mandatory.

**Write children before parents.** Allocate private blocks, encode/checksum leaves, submit writes, then build parents referencing final child identities/checksums. Continue to the root. Wait for required completion and durability in the storage stack. Finally write/select a root record containing generation, root reference/checksum, feature/version, allocator checkpoint/intent, and its own checksum. If root selection is not atomically written, use redundant slots/rings with sequence and validation.

**Recovery validates, not merely chooses the largest number.** Enumerate candidate root records under format rules. Reject torn/checksum-invalid/unsupported candidates. For a selected candidate, validate required root and perhaps lazy descendants with parent expectations; define fallback when the newest record points to missing/corrupt data. Reconcile blocks allocated by failed private generations. Never accept generation alone as proof of a complete tree.

**The finite model shows structural sharing and root-set reclamation.** It uses immutable binary nodes so the path is easy to inspect. Inserting 13 copies three ancestors plus the new leaf, retains four shared old nodes, and computes unreachable old-only nodes after snapshot removal.

<!-- bijux-verify: {"id":"persistent-path-copy-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"base_inorder=2,4,6,8,10,12,14\nupdated_inorder=2,4,6,8,10,12,13,14\nbase_root=8\nupdated_root=8\ncopied_or_new_nodes=4\nshared_nodes=4\nbase_unchanged=True\nlookup_base_13=False\nlookup_updated_13=True\ndistinct_nodes_with_both_roots=11\nreclaimable_after_old_drop=3\nvalid=True\nevidence=persistent_path_copy_model\n","stderr":""}} -->
```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Node:
    key: int
    left: object = None
    right: object = None


def insert(node, key):
    if node is None:
        return Node(key)
    if key < node.key:
        return Node(node.key, insert(node.left, key), node.right)
    if key > node.key:
        return Node(node.key, node.left, insert(node.right, key))
    return node


def lookup(node, key):
    while node is not None:
        if key == node.key:
            return True
        node = node.left if key < node.key else node.right
    return False


def inorder(node):
    if node is None:
        return []
    return inorder(node.left) + [node.key] + inorder(node.right)


def identities(node):
    if node is None:
        return set()
    return {id(node)} | identities(node.left) | identities(node.right)


def valid(node, low=None, high=None):
    if node is None:
        return True
    ordered = (low is None or low < node.key) and (high is None or node.key < high)
    return ordered and valid(node.left, low, node.key) and valid(node.right, node.key, high)


base = Node(8, Node(4, Node(2), Node(6)), Node(12, Node(10), Node(14)))
updated = insert(base, 13)
base_ids = identities(base)
updated_ids = identities(updated)
shared = base_ids & updated_ids
both = base_ids | updated_ids
old_only = base_ids - updated_ids
print("base_inorder=" + ",".join(str(key) for key in inorder(base)))
print("updated_inorder=" + ",".join(str(key) for key in inorder(updated)))
print(f"base_root={base.key}")
print(f"updated_root={updated.key}")
print(f"copied_or_new_nodes={len(updated_ids - base_ids)}")
print(f"shared_nodes={len(shared)}")
print(f"base_unchanged={inorder(base) == [2, 4, 6, 8, 10, 12, 14]}")
print(f"lookup_base_13={lookup(base, 13)}")
print(f"lookup_updated_13={lookup(updated, 13)}")
print(f"distinct_nodes_with_both_roots={len(both)}")
print(f"reclaimable_after_old_drop={len(old_only)}")
print(f"valid={valid(base) and valid(updated)}")
print("evidence=persistent_path_copy_model")
```

The model has no balancing, pages, byte serialization, allocator, persistence, concurrent writers/readers, crash, checksum, batching, snapshots beyond two in-memory roots, or measured amplification. Python object identity is used only to count sharing during this run. Exact output proves one finite immutable update, not durable CoW.

**Snapshots are root retention.** Creating a read-only snapshot records another durable root reference and retention metadata. A clone initially references the same root but publishes future writes to its own lineage. Define snapshot naming, transaction boundary, recursive/nested behavior, deletion, quotas, send/receive, rollback, and whether external data/intent logs are included. “Instant” refers to metadata creation, not future space cost or remote durability.

**Reference accounting is part of the transaction.** Per-block reference counts make local free decisions but every increment/decrement and recursive release must be crash-consistent, idempotent, overflow-safe, and auditable. Backreferences explain owners but add metadata writes. Root tracing avoids per-edge counts but can be expensive and needs a stable root set. Hybrid delayed-reference systems batch work. The tree/free-space/reference structures can depend on one another, so define bootstrap and recovery order.

**Readers pin versions, not mutable pages.** A reader acquires a root generation and prevents required nodes from reuse until release. Immutable nodes reduce content latching, but caches, reference metadata, root tables, and reclamation still synchronize. Long readers/snapshots cause retained space. Detect abandoned reader registrations after process crash under a safe lease/transaction table protocol; never infer liveness solely from wall-clock delay.

**Concurrent writers need serialization or merge.** A single writer can build from current root and compare/publish generation. Multiple writers starting from root r cannot both blindly publish: the loser rebases/retries, or a transaction layer merges disjoint logical effects with conflict detection. CAS on a root pointer provides only volatile atomicity unless the persistent/root-record protocol gives equivalent crash semantics.

**Synchronous durability may need an intent path.** If root generations commit in batches, an application `fsync` promise cannot simply wait indefinitely or return early. Systems may force a generation sync or log intent that recovery replays into a later CoW tree. This log has ordering, checksum, idempotence, space, and failure semantics. Therefore “CoW needs no log” is too broad.

**Space is a correctness resource.** Reserve enough free blocks and metadata for worst-case path copies, splits, reference updates, and root commit. Handle ENOSPC before overwriting or publishing anything. Snapshots can pin old extents; fragmentation can make allocation fail despite aggregate free bytes; cleaner/rebalancer itself needs workspace. Expose reservation, pinned-by-snapshot, pending-free, fragmentation, and metadata/data space separately.

**Scrub the graph.** Validate root slots, parent-to-child checksum/generation/type, ordering/balance, cycles, duplicate ownership rules, reference counts/backrefs, all live roots, allocated/reachable/free disjointness, and orphan private generations. With redundancy, repair from a verified alternate copy and update ownership safely. Do not run destructive repair by default; preserve evidence and allow read-only recovery/export.

**Measure amplification and tails.** Record logical bytes changed, new data/metadata/reference/root/intent bytes, allocator/cleaner writes, physical device bytes, trims, and retained old bytes. Workloads vary update locality, batch size, tree height, snapshots, clone divergence, compression, free-space pressure, sync frequency, and crash recovery. Report latency distributions and space growth, not only average update throughput.

## Definitions and Notation

Let version v have root `R_v`; `Reach(R_v)` is its node set. Live roots `L` include current, snapshots, clones, readers, backups/replicas, and recovery checkpoints by policy. `Reach(L)=union Reach(r)`. Node x is reclaimable only if `x not in Reach(L)` and all in-flight reference conditions are clear.

Let h be height, P page bytes, k copied/new pages for a logical update, `W_logical` changed payload bytes, and `W_physical` device writes. Write amplification is a declared ratio such as `W_physical/W_logical`; specify inclusion of replication, intent log, reference tree, cleaner, compression, and failed writes. Generation g and `PageId:generation` are distinct where locations are reused.

## Mechanisms, Invariants, or Proof Structure

### Abstract version proof

1. Assume every published node is immutable and locally valid.
2. Descend according to ordering; recursively obtain a new changed child.
3. Construct a new parent with that child and unchanged child identities shared.
4. Prove local ordering/balance and abstract map update at each return.
5. Conclude old root is unchanged and new root represents exactly the operation.
6. Extend split/merge proof to every copied sibling/ancestor and batched conflict order.

### Durable publication proof

1. Reserve private identities and record ownership intent without exposing a root.
2. Encode/checksum/write new descendants, then ancestors with validated child references.
3. Complete required write and barrier semantics through the actual device/replica stack.
4. Write a checksummed monotone root record in an atomic/redundant selection scheme.
5. Recover by validating candidate roots and selecting/falling back under documented rules.
6. Reconcile private/orphan allocations while retaining every block reachable by a live root.

### Reclamation proof

1. Enumerate the authoritative live-root and in-flight-reference set.
2. Maintain crash-consistent reference/backreference changes or trace exact reachability.
3. Retire unreachable nodes before reuse; attach generation to every later reference/I/O.
4. Wait for reader/epoch, snapshot/clone, backup/replica, log, and recovery boundaries.
5. Reconcile allocated, reachable, retired, pending-free, and free sets after crash.
6. Test reuse/ABA and reference-update crashes; do not infer universal safety from clean shutdown.

## Alternatives and Trade-Offs

| Choice | Strength | Cost/proof burden |
|---|---|---|
| In-place + WAL | low page rewrite for small update | redo/undo and partial structure complexity |
| Full-path CoW | simple immutable versions/root switch | write/space amplification |
| Delta/logged nodes | smaller foreground writes | read/consolidation/recovery complexity |
| Per-block reference count | local reclamation | update amplification and crash recursion |
| Backreferences | explain sharing/repair | metadata size and write burden |
| Root tracing | simple ownership source | scan cost and stable-root requirement |
| Single writer | deterministic publication | write concurrency bottleneck |
| Optimistic multiwriter | parallel preparation | conflict/rebase/wasted work |
| Transaction batching | shares copied paths | sync latency and dirty-memory pressure |
| Immediate snapshot | cheap creation | future retention and quota surprise |
| Parent-held checksum | child cannot self-vouch | ancestor rewrite and root trust burden |
| Local checksum | simple page validation | weaker end-to-end identity context |

## Failure Modes and Misconceptions

- **“CoW means copy the whole tree.”** Copy changed paths and share immutable subtrees.
- **“The old root can be freed after commit.”** Live snapshots/readers/clones may still reach it.
- **“Immutable objects are crash-consistent.”** Durable allocation, ordering, root selection, and recovery are separate.
- **“Highest root generation always wins.”** Validate checksum, format, descendants, and device/replica quorum rules.
- **“Checksum means atomic write.”** It detects selected corruption; selection/fallback defines atomic outcome.
- **“Reference count zero is enough.”** Ensure update durability, no stale reference/I/O, generation safety, and recursive accounting.
- **“Snapshots cost no space.”** Creation is cheap; divergence pins old blocks and metadata.
- **“CoW needs no WAL.”** Sync intent, logical transactions, reference updates, or allocator recovery may still use logs.
- **“Free space is only a performance issue.”** Commit may require additional blocks and fail safely under pressure.
- **“CAS root supports many writers.”** Conflict semantics and persistent publication remain.
- **“Logical writes equal device writes.”** Full pages, metadata, replication, cleaner, and failed private generations amplify.
- **“One crash test proves recovery.”** Exercise every allocation/write/barrier/root/reference/free boundary and reorder/fault model.

## Worked Examples

### Example 1

**Problem.** Insert 13 into the compact example.

**Derivation.** Create 13; copy 14 with left=13; copy 12 with new right; copy 8 with new right. Reuse nodes 4,2,6,10.

**Conclusion.** Four new nodes implement a height-three path update while old tree remains intact.

### Example 2

**Problem.** Both old and new roots remain live.

**Derivation.** Their union has eleven distinct nodes: seven old plus four new. Old-only copied nodes 8,12,14 remain reachable through old root and cannot be freed.

**Conclusion.** Sharing/reclamation is computed over roots, not current version.

### Example 3

**Problem.** Old snapshot is deleted and no reader/replica retains it.

**Derivation.** Trace new root: old copies of 8,12,14 are absent; shared 2,4,6,10 remain. Retire the three old-only nodes, then reuse only after generation/epoch/recovery barriers.

**Conclusion.** Unreachability precedes safe physical reuse.

### Example 4

**Problem.** Crash after child and parent writes but before root record.

**Derivation.** Old root remains selected and consistent. New private blocks are unreachable; manifest/allocation recovery later reclaims or resumes them.

**Conclusion.** Unpublished writes are garbage, not a half-visible version.

### Example 5

**Problem.** Crash after root record write with a torn newest slot.

**Derivation.** Reject checksum/format-invalid slot and fall back to prior valid root. Redundant root selection must specify atomic granule and wrap/sequence rules.

**Conclusion.** CoW relies on robust root-record recovery.

### Example 6

**Problem.** Parent checksum expects child X, but X is corrupt.

**Derivation.** Reject/mark subtree, try verified redundant copy if policy permits, and never let X's adjacent self-checksum override parent expectation.

**Conclusion.** Parent-held authentication strengthens end-to-end detection.

### Example 7

**Problem.** Two writers derive roots v+1a and v+1b from v.

**Derivation.** Only one may publish directly. The other detects generation conflict and aborts/rebases or uses a transaction merge proven for its logical changes.

**Conclusion.** Immutable preparation does not resolve write conflicts.

### Example 8

**Problem.** A 4 KiB logical update copies four 16 KiB metadata pages plus root/reference writes.

**Derivation.** Tree metadata alone writes at least 64 KiB, ratio 16 before data, allocator, intent, replication, and cleaner. Compression/device behavior can change physical bytes.

**Conclusion.** State amplification numerator and denominator precisely.

### Example 9

**Problem.** A snapshot pins 2 TiB of old extents while current logical data is 1 TiB.

**Derivation.** Snapshot creation was cheap, but divergence prevents reclamation. Quota/space telemetry must attribute referenced/exclusive/pinned bytes and deletion progress.

**Conclusion.** Snapshot lifecycle is capacity engineering.

### Example 10

**Problem.** ENOSPC occurs halfway through preparing a split path.

**Derivation.** Do not publish root; retain old tree. Journal/reservation identifies private blocks for cleanup. Test cleaner workspace and metadata reserve so recovery does not need unavailable space.

**Conclusion.** Allocation failure must preserve the prior version.

## Cross-Program Connections

- **Database Engineering:** shadow paging, MVCC roots, transaction commit, intent logging, snapshots, clones, backups, and catalog publication refine this protocol.
- **Operating Systems:** atomic-write units, cache flush, FUA/barriers, delayed allocation, TRIM, device error, and mmap visibility determine durability.
- **Concurrent and Parallel Programming:** immutable readers, writer conflicts, epochs/hazards, ABA generations, and lock-free root publication govern memory safety.
- **Distributed Systems:** replicated roots, quorum durability, snapshot transfer, clone lineage, log retention, and garbage collection expand the live-root set.
- **Security Engineering:** authenticated child references, rollback attacks, corrupt root selection, stale generation, malicious graphs, and resource exhaustion are trust boundaries.
- **Performance Engineering:** batching, locality, amplification, fragmentation, free-space reserves, snapshot retention, cleaner load, and sync tails require measurement.

## References

1. Ohad Rodeh, [“B-trees, Shadowing, and Clones”](https://research.ibm.com/publications/b-trees-shadowing-and-clones), *ACM Transactions on Storage* 3(4), 2008. Primary CoW B-tree algorithms for shadowing, snapshots/clones, and concurrency.
2. Btrfs Project, [“Btrfs Design”](https://btrfs.readthedocs.io/en/stable/dev/dev-btrfs-design.html), current developer documentation accessed 2026-08-30. Official tree format, CoW logging, generations, root updates, and reference behavior.
3. Btrfs Project, [“B-trees”](https://btrfs.readthedocs.io/en/latest/dev/dev-btrees.html), current developer documentation accessed 2026-08-30. Official root-tree, extent-tree, reference, and allocation topology.
4. Btrfs Project, [“Introduction”](https://btrfs.readthedocs.io/en/stable/Introduction.html), current documentation accessed 2026-08-30. Official snapshot, checksum, fault-tolerance, and CoW feature context.
5. OpenZFS Project, [“Copy-on-Write”](https://openzfs.github.io/openzfs-docs/Basic%20Concepts/Copy-on-write.html), current documentation accessed 2026-08-30. Official block-pointer tree, uberblock, transaction group, snapshot, and intent-log explanation.
6. OpenZFS Project, [“Pool Structure”](https://openzfs.github.io/openzfs-docs/Basic%20Concepts/Pool%20Structure/index.html), current documentation accessed 2026-08-30. Official root/label, allocation, vdev, and storage hierarchy context.
7. Joel Coburn et al., [“NV-Heaps: Making Persistent Objects Fast and Safe with Next-Generation, Non-Volatile Memories”](https://www.cs.utexas.edu/ftp/dburger/papers/SOSP09.pdf), *ASPLOS*, 2011. Primary comparison of logging and shadow paging under persistent-memory failure models.
8. Linux kernel documentation, [“BTRFS”](https://docs.kernel.org/filesystems/btrfs.html), current documentation accessed 2026-08-30. Official kernel interface and durability/feature context for a production CoW tree filesystem.

## Exercises

### Exercise 1

Prove immutable path-copy insertion preserves the old map, produces the updated map, and shares exactly off-path subtrees. Extend the reasoning to a multiway leaf split and state write-amplification limits.

### Exercise 2

Given live roots R0 and R1 with reachability sets `{a,b,c,d,e}` and `{f,b,c,g,e}`, plus an in-flight read of d, compute shared, root-exclusive, union, and reclaimable nodes before/after dropping R0 and completing the read. State generation rules.

### Exercise 3

Design a durable CoW page/root protocol: identities, checksums, allocation reservation, child-to-parent writes, root slots, barriers, synchronous intent, recovery selection/fallback, ENOSPC, and orphan cleanup. Name every crash point to test.

### Exercise 4

Design snapshot, writable clone, deletion, reference/reachability, backup/replica, quota, scrub/repair, migration, and rollback semantics for a shared CoW tree. Include long-lived and corrupt-reference cases.

### Exercise 5

Audit a CoW store that mutates reference counts in place, chooses highest root generation without descendant validation, frees blocks when absent from current root, immediately reuses IDs, returns fsync before generation commit, and reports write amplification using logical metadata only.

## Answers to the Exercises

### Answer 1

Induct on the search path. Base insertion creates a new leaf and changes no old node. At each return, construct a new locally valid parent containing the new child and reuse every unaffected immutable child identity; the old parent still points to old children. Thus the old root's reachable graph/map is unchanged, while the new root differs exactly by the logical insertion. Ordering follows descent intervals; balance follows the tree variant's repair.

For a full multiway leaf, allocate legal left/right results containing every entry once, copy/promote the variant's separator, then copy parents; cascading splits can create a new root while all old nodes remain. Without splits, O(h) nodes/pages are new. Splits, sibling redistribution, reference/root/allocator metadata, batching, compression, and device writes change constants and numerator; no universal byte amplification follows from height alone.

### Answer 2

Shared is `{b,c,e}`. R0-exclusive is `{a,d}`; R1-exclusive is `{f,g}`; union is `{a,b,c,d,e,f,g}`. With both roots live nothing in the union is reclaimable. After dropping R0, a is unreachable and can be retired, but d remains protected by the in-flight read. After that read completes and no snapshot/log/replica/I/O reference remains, d can also be retired.

Retirement is not immediate reuse: attach generation to every block reference, wait the epoch/hazard and durable recovery boundary, ensure stale I/O/log cannot address the old generation, record free-space transition crash-consistently, then reuse under a new generation. Shared b,c,e remain reachable through R1.

### Answer 3

Use versioned fixed-endian pages with page ID/generation/type/level/owner/birth transaction/length, checksum, and checked slots; parent references carry child identity, generation, type, encoded size, checksum, and encryption/compression context. Reserve worst-case data/metadata/reference/root space and journal private ownership. Write/check children, then parents, completing required barriers. Store redundant checksummed root slots/ring entries with monotone sequence, definition/features, root reference, allocator/reference checkpoint, and synchronous state.

For fsync either force the generation through durable root selection or durably log replayable idempotent intent before acknowledging. Recovery rejects torn/unsupported root records, validates root/required descendants and allocation epoch, selects newest complete candidate or falls back, replays intent, reconciles reachable/private/free blocks, and preserves evidence on corruption. Test crash/error/reorder at every reserve, data write, child write, reference update, barrier, root write, root barrier, intent, free, checkpoint, cleanup, and replica acknowledgment, including ENOSPC and lost/torn/late I/O.

### Answer 4

A snapshot durably pins a validated root/version at a transaction boundary; clone begins with that root and publishes its own lineage. Deletion removes the root name atomically but only schedules graph references for release. Define nested roots, recursive snapshot scope, external intent/data inclusion, read-only versus writable, naming, retention, legal holds, resume/send/receive, rollback, and version compatibility.

Maintain crash-consistent counts/backrefs or trace all roots; audit both against actual graph, handle cycles/corrupt pointers with bounds, and delay reuse for readers/backups/replicas/logs. Quotas report referenced, exclusive, shared, pinned, pending-free, and metadata bytes plus asynchronous deletion progress. Scrub validates parent-held checksums, identity/generation, tree invariants, ownership, and redundancy before repair. Backup/replica acknowledgments govern root/log retention. Migration reads old versions, writes a private new graph, verifies, publishes, retains rollback root, and reclaims only after all readers/replicas upgrade.

### Answer 5

In-place counts can become inconsistent with tree commit; log/CoW/delayed-reference them transactionally and independently reconcile. Highest generation is insufficient: validate root checksum/format and required descendants, with explicit fallback. Current-root absence ignores snapshots/readers/clones/backups/replicas; compute the full live-root/in-flight set. Immediate ID reuse creates ABA for stale pointers, I/O, and logs; retire with generation and epoch/recovery barriers.

An fsync acknowledgment must correspond to durable generation/root or replayable durable intent under documented storage barriers. Amplification must state physical numerator: new data and metadata pages, reference/free trees, root/intent, replication, cleaner, retries/private failures, compression, and device bytes, divided by a stated logical payload. Gate the design with abstract version proofs, byte/parser tests, root/reference audits, exhaustive crash/reorder/ENOSPC tests, concurrency/reuse schedules, snapshot lifecycle tests, and workload-tail/space measurements.
