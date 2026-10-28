---
module_id: DSE-057
program: Data Structures Engineering
level: 2
module_number: 57
title: Persistent Union-Find Trade-Offs
status: complete
last_verified: 2026-08-30
---

# Persistent Union-Find Trade-Offs

## One-Page Review

### Governing question

Which persistence model and representation should maintain evolving equivalence classes when classical path compression mutates queries, version histories branch or roll back, and correctness, cost, lifetime, concurrency, and evidence must remain explicit?

### Essential definitions

- A **disjoint-set union** (DSU) or **union-find** maintains a partition under `find` and `union`.
- A **representative** is a chosen root/name for one class; only representative equality, not its identity stability, is normally semantic.
- A **parent forest** stores each element's parent, with roots pointing to themselves.
- **union by rank/size** links the shallower/smaller root under the deeper/larger root.
- **path compression** changes parent links along a find path to point nearer the representative.
- A **persistent DSU** exposes past partitions through version handles while preserving the advertised query/update model.
- **rollback DSU** records mutations on an undo stack and restores states in last-in, first-out order; it is not arbitrary full persistence.
- **partial persistence** permits queries of old versions but updates only the newest version.
- **full persistence** permits updates from any retained version, creating a version tree.
- **observational persistence** allows hidden internal mutation when every client-observable version behaves as an immutable value.

### Central model, mechanism, or theorem

Classical ephemeral DSU combines union by rank/size with path compression, yielding inverse-Ackermann amortized behavior under its exact mutable model. Persistence changes the problem because `find` itself writes many parent cells. Copying or versioning every compression write can overwhelm the mechanism, and a query cannot silently change one version if the API treats versions as immutable values without an updated return.

A simple fully persistent design stores immutable parent/rank arrays or maps, performs union by rank, and does not compress on read-only `find`. Rank proves forest height at most `floor(log2 n)`: a rank-`r` root represents at least `2^r` elements. Cost is path length times persistent-array access, plus persistent updates; this is often slower than the classical bound but easy to reason about and branch safely.

Rollback DSU keeps mutable arrays, union by size/rank, and a log of changed cells/component count. Snapshot is a log length; rollback undoes to that length. Avoid path compression or log every compression write, otherwise rollback is incomplete. It excels for depth-first offline algorithms but snapshot handles are stack positions, not freely updateable persistent roots.

More advanced persistent arrays and the Conchon–Filliâtre construction hide rerooting/path-compression side effects behind an observationally persistent interface and formal proof. Their guarantees depend on exact representation, access pattern, language semantics, and proof—not on a generic claim that path compression is compatible with all persistence.

### Critical invariants

1. Every element index is in range; following parents terminates at a self-parent root with no nontrivial cycle.
2. `find(version,x)` returns a representative whose class equals the partition denoted by that version.
3. Two elements are connected exactly when their finds in the same version return the same representative.
4. Union merges exactly two distinct classes or returns an equivalent/identical version for an already-connected pair.
5. Rank/size fields are authoritative only at roots and satisfy the chosen linking/height proof.
6. A persistent operation never changes any older version's observable partition; hidden mutations preserve observational equivalence.
7. Rollback logs every mutated field required to restore parent, rank/size, component count, and auxiliary metadata exactly.
8. Version/snapshot handles belong to the correct structure/generation and obey partial/full/LIFO validity rules.
9. Reclamation retains all parent/rank storage, diff chains, logs, readers, and versions still reachable.
10. Complexity claims name path compression, union heuristic, persistent-array cost, version topology, rerooting, rollback, and workload.

### Common failures

- Calling a rollback stack “fully persistent” because it can revisit earlier states.
- Performing path compression but logging only union changes.
- Mutating shared parents in a supposedly immutable branch.
- Copying a whole array per union and reporting only forest height, not `Theta(n)` copying.
- Assuming the inverse-Ackermann bound survives a different persistence/query model.
- Treating representative IDs as permanent class identities across unions/versions.
- Incrementing rank on unequal-rank union or trusting rank on nonroots.
- Accepting snapshot/version handles from another DSU or after destructive truncation.
- Forgetting component count/size/metadata during rollback.
- Using DSU for arbitrary online edge deletion; deletion can split a class and is not a union-find operation.

### Compact example

Create eight singleton elements. In one history union `(0,1)`, `(2,3)`, then `(0,2)`, producing class `{0,1,2,3}`. Branch from the two-union version and union `(4,5)` instead; the first branch remains unchanged. Continue the first branch with `(4,5)`, `(5,6)`, then `(3,5)`, producing `{0,1,2,3,4,5,6}` and singleton `{7}`. The executable uses immutable tuples and union by rank without compression, validates every partition/root/rank, and reports maximum depth two; its tuple copies are `Theta(n)` and are not performance evidence.

### Connections

[DSE-043](043-disjoint-set-forests.md) supplies the classical forest, union heuristics, and compression baseline. [DSE-051](051-path-copying.md) and [DSE-052](052-structural-sharing.md) supply persistence/lifetime models. [DSE-053](053-persistent-lists-and-queues.md) shows why amortized proofs must match version traces. [DSE-054](054-persistent-balanced-trees.md) and [DSE-055](055-hash-array-mapped-tries.md) provide immutable map/array-trie substrates. The [program roadmap](../ROADMAP.md) next studies fat nodes and broader persistence models.

## Governing Question

Does the application need immutable branching versions, old-time queries, LIFO rollback, or merely backtracking convenience—and which union heuristic, compression policy, persistent array/log mechanism, and evidence correctly implements that exact model?

## Why This Matters

Union-find powers Kruskal's algorithm, connected-component labeling, unification, type inference, equivalence closure, congruence/decision procedures, image processing, clustering, percolation, and offline connectivity. Many of these algorithms also backtrack, speculate, branch, or ask historical queries.

The famous efficiency result belongs to a particular ephemeral algorithm: mutable parent/rank arrays, union heuristic, path compression, and a sequence of operations over one evolving state. Persistence is especially subtle because `find`, usually thought of as a query, performs destructive optimization. An old version and a new version may share the very parent cell that compression wants to rewrite.

There is no single “persistent union-find.” A pure immutable forest without compression is easy and fully branchable but may multiply persistent-array costs. A rollback forest is fast for depth-first traversal but only undoes a mutation stack. A partially persistent history can answer time-stamped queries while updating the latest partition. A semi-persistent/persistent-array construction may expose an immutable interface while mutating hidden representations. Each supports different client programs.

Representative identity also misleads systems design. Union chooses one root; later union may choose another. Across versions, equal classes can have different roots and unequal historical classes may reuse the same integer as representative. Application entities need stable IDs separate from DSU root names.

## Prerequisites and Retrieval

Retrieve parent forests, rank/size, path compression/halving/splitting, inverse-Ackermann amortization, validation, and applications from [DSE-043](043-disjoint-set-forests.md). Retrieve persistence levels, version roots, changed frontiers, failure, reclamation, concurrency, and serialization from [DSE-051](051-path-copying.md), and physical sharing/reachability from [DSE-052](052-structural-sharing.md).

Retrieve persistent amortization cautions from [DSE-053](053-persistent-lists-and-queues.md) and immutable indexed-map substrate choices from [DSE-054](054-persistent-balanced-trees.md) and [DSE-055](055-hash-array-mapped-tries.md). You should be able to prove rank height, distinguish amortized/worst-case and partial/full/confluent persistence, and trace an undo log exactly.

## Learning Objectives

After completing this module, you can:

1. specify partition semantics independently from representatives and forest shape;
2. derive union-by-rank height bounds without path compression;
3. explain why classical path compression conflicts with simple persistent interfaces;
4. implement and validate a pure fully persistent union-by-rank model;
5. design rollback snapshots/logs and state their LIFO limitations;
6. compare partial persistence, fat nodes, persistent arrays, rerooting, and hidden mutation;
7. choose a design for backtracking, historical, branching, or offline connectivity workloads;
8. specify handles, failure, concurrency, serialization, reclamation, and security;
9. validate every version/partition plus logs and structural sharing; and
10. benchmark parent accesses/writes, copying, reroots, log bytes, depth, retention, and tail behavior.

## Core Exposition

**Define a partition, not a forest.** For a fixed universe `U={0,...,n-1}`, a DSU version denotes an equivalence relation: reflexive, symmetric, and transitive. `find(v,x)` returns some representative for `x`'s equivalence class in version `v`. `connected(v,x,y)` compares representatives. `union(v,x,y)` returns a version whose partition is the least coarsening merging those two classes.

The representative is not normally semantic. Clients must not assume the smallest element, first argument, memory address, or stable root unless explicitly guaranteed. A canonical representative policy can be added but may conflict with rank/size efficiency. Store application component IDs/metadata through a merge policy rather than exposing parent roots as durable identifiers.

Universe policy matters. A fixed-size DSU validates every index. Dynamic `make_set` adds elements and complicates version-local membership, arrays, handles, serialization, and union between generations. This module's executable uses a fixed universe.

An already-connected union can return the identical root/version value. A system may still create a separate commit record for provenance. Separate partition root from version metadata. Find on empty/out-of-range input is a typed error and changes no state.

**Recall the ephemeral optimal design.** Parent array initially satisfies `parent[x]=x`; rank/size initializes zero/one. Find follows parents. Union finds roots, links lower rank/size beneath higher, and increments rank only when equal. Path compression rewrites every visited parent to the root; halving/splitting rewrite subsets.

Without compression, union by rank gives logarithmic height. A root of rank zero has at least one element. Rank increases from `r` to `r+1` only by merging two rank-`r` trees, so the resulting tree contains at least `2^(r+1)` elements. Therefore `rank<=floor(log2 n)` and find is `O(log n)` parent steps.

With union by rank and compression, a sequence has the classical inverse-Ackermann amortized bound under the mutable-array model. This is not a worst-case bound for every individual call, not a claim about arbitrary persistent arrays, and not permission to omit writes/allocation from measurements.

Path compression is semantically partition-preserving: it changes shape but not roots/classes. Operationally it writes potentially every node on the path. That distinction enables hidden optimizations but creates persistence and rollback obligations.

**Pure immutable DSU is the baseline.** Represent version `V=(Parent,Rank,Components)`, where Parent/Rank are persistent indexed collections. Read-only find follows `Parent` without compression. Union gets roots; if equal returns `V`; otherwise writes one root parent and perhaps one rank, decreases component count, and returns a new version.

The forest proof is direct. Parent changes only at a root and points to another root, so it cannot create a cycle. Rank-linking preserves the height theorem. Old Parent/Rank roots remain immutable. Branches from any version are valid, giving full persistence.

Cost depends on the substrate. If Parent/Rank are balanced maps, each parent lookup costs `O(log n)`, and a height-`O(log n)` find can cost `O(log^2 n)`. A persistent vector/trie can reduce access/update constants/asymptotics under its model. Copying a flat `n`-tuple/array per write costs `Theta(n)` despite logarithmic forest depth. Report both levels.

Compression could be purely functional if find returns `(representative,newVersion)` and writes persistent parents along the path. But every query then creates/returns state, client code must thread it, old branches retain precompression nodes, and persistent-array writes have costs. The classic amortized proof must be redone for this interface/version graph. Read-only queries may be preferable.

Path copying the forest as node objects is difficult because elements need direct access to their version-specific node/parent. A persistent indexed map from element to parent is the usual indirection. Raw node handles from one version cannot silently traverse another.

**Rollback DSU is a different contract.** Keep mutable Parent/Size and a stack of change records. Union by size without path compression changes at most one parent, one root size/rank, and component count. Before mutation, push enough old values or a no-op marker. `snapshot()` returns current log length. `rollback(s)` pops/reverses changes until length `s`.

Find is read-only and `O(log n)` worst-case from union by size/rank. Union is logarithmic for its two finds plus constant logged writes; rollback work is proportional to undone successful changes, often `O(1)` per union record. Exact bounds depend on interface and logging.

Path compression breaks the small-log property: find may write many parents. Either disable it or log every write and restore in reverse. Logging compression can expand time/space and complicate queries. “Compression is only an optimization” does not justify unlogged mutations.

Snapshot handles are stack positions in one mutation timeline. Rolling back from state `S3` to `S1` and performing a new union normally discards or overwrites the future `S2/S3`; retaining both requires copied logs/state or a persistent version structure. A rollback DSU supports disciplined depth-first search, not arbitrary full persistence.

Validate snapshot ownership, generation, `0<=s<=currentLogLength`, and whether forward/future handles remain valid after rollback. Untrusted clients should not submit raw stack indices. Nested RAII/context scopes can guarantee rollback on exceptions/cancellation.

Offline dynamic connectivity is a classic match: put each edge's active time interval into nodes of a time segment tree; depth-first traverse, apply node edges, answer leaf-time queries, and rollback on return. This handles deletions offline because time recursion restores states; the DSU itself still only unions.

**Partial persistence supports time-indexed queries.** Updates create a linear latest-version sequence; old versions are queryable but not updateable. One approach stores parent/rank change histories tagged by version and binary-searches the latest change not after query time. A partially persistent union-find can exploit monotone unions and version order more specifically than a general transformation.

Historical `find(x,t)` follows parent values as of `t`. The root at current time may not be the root at `t`. Rank/size queries likewise use historical values. Path compression performed for current time can add history records or be restricted; it must not change old-time answers.

Version identifiers need monotonicity, bounds, and generation. Serialization stores the update timeline and version semantics. Deleting old histories requires proving no query/reader/legal hold needs them.

Partial persistence is ideal when data arrives chronologically and clients ask past connectivity but never branch updates—for example some temporal equivalence analyses. It is not full persistence.

**Persistent arrays can hide mutation.** A simple functional array backed by a tree/trie has predictable immutable behavior but nonconstant access. Baker-style/rerootable persistent arrays represent one version as a mutable concrete array and other versions as difference records. Accessing an old version reroots the chain: apply/reverse diffs so that version becomes concrete while leaving inverse diffs for the formerly concrete version.

Rerooting mutates representation links/arrays internally. If implemented correctly, all version reads return their immutable logical arrays: observational persistence. Access cost depends on diff-chain distance and usage pattern; repeated switching between versions can reroot repeatedly. Cycles, reentrancy, exceptions mid-reroot, concurrent access, and lifetime require care.

Conchon and Filliâtre build a persistent union-find using persistent arrays and hidden side effects, retain a persistent interface, perform path compression, analyze efficiency, and formalize correctness/observational persistence in Coq. This is evidence for their construction—not a blanket recipe to mutate behind any immutable API.

The parent array may be mutable inside a DSU record so find can install a compressed persistent-array version while preserving the record's logical partition. Aliasing and interface abstraction are essential: clients must not observe the mutable cell/array/diff orientation. Language memory model and concurrency can invalidate assumptions if ported casually.

If a pure functional API is mandatory, a verified rerooting implementation may still qualify observationally but not as “no mutation.” Disclose thread-safety and operational effects. Audit exceptions so reroot/compression is atomic or recoverable.

**General persistence transformations have limits.** Fat nodes store versioned field values in nodes; node copying creates replacements when modification capacity fills. These techniques rely on bounded in-degree/updates and version navigation assumptions. A parent forest has direct indexed element lookup plus compression writes spread along paths; the index and node versioning must be included.

A fat parent record can store `(version,newParent)` changes and find selects the applicable record. In partial persistence with linear versions, binary search works. Full version trees need ancestry tests/version labels rather than numeric `<=`. Compression adds many versioned modifications and can consume space.

Copy-on-write pages/arrays copy blocks, not whole arrays. This gives snapshots with page-level sharing but writes can amplify by page size; path compression may dirty many pages. Radix/persistent vectors copy logarithmic nodes. Log-structured overlays store changes and periodically materialize/compact; reads traverse overlays.

Choose based on universe size, union/find ratio, version branching, old-version locality, memory, runtime, and implementation proof. No representation dominates.

**Full and confluent questions need precision.** Full persistence allows `union(v,x,y)` for any retained `v`, forming a version tree. The pure immutable baseline provides this. Rerooted arrays may support persistent values but performance depends on switching/branching access. Rollback alone does not.

Confluent persistence would combine two partitions/versions. The natural least equivalence containing both relations can be computed by replaying/unioning all class relations, but version-DAG ancestry, duplicate work, and complexity must be defined. Union of two DSU *elements* is not confluent merge of two DSU *versions*.

Merging branches requires element universe/schema match and policy for component metadata. Connectivity relations only coarsen, so relation join exists, but reconstructing it efficiently and tracking provenance are separate algorithms. Do not advertise ordinary `union(x,y)` as version merge.

Deletions are unsupported because removing a union relation can split a component and requires knowing alternate connecting edges/proof history. Rollback can undo the latest union in its timeline; offline dynamic connectivity schedules edge intervals; fully dynamic online connectivity requires other data structures.

**Metadata and identity require ownership.** Root rank/size is structural; after compression nonroot fields may be stale/ignored. Component aggregates (sum, members, canonical name, payload) need a merge function and rollback/persistence updates. If aggregates are not invertible, rollback logs old values. Full branching copies/shares persistent metadata.

Representative IDs can change when classes merge and differ across histories. Return connectivity/classes, or expose opaque version-scoped reps. If clients cache reps, tag with DSU/version and revalidate. Serialization never treats parent root as permanent external entity ID.

Enumerating members is not supported efficiently by bare parent forests. Maintain member lists/trees with additional update/rollback costs or scan all elements. Component count is constant-time only if updated/restored exactly. Class size under union-by-size is available at roots, version-specific.

**Failure behavior depends on mechanism.** Pure persistent union constructs new parent/rank roots privately; allocation or metadata failure leaves old roots unchanged. Find is read-only. A functional compression result publishes last and can be discarded on failure.

Rollback union mutates arrays after logging old values. Push a complete record before each mutation or use an exception-safe transaction so failure restores immediately. A no-op union either logs a marker for one-operation rollback alignment or documents that snapshot/log length changes only on successful merges.

Rerooting must survive allocation/exceptions during diff reversal. Establish an order that always leaves a valid orientation or recover using guards. Recursive reroot/find on hostile/deep chains can overflow. Cancellation/thread interruption cannot strand a half-rerooted shared representation.

Validate `n` and counters against overflow. Rank cannot exceed logarithmic bound for valid fixed universe; an impossible rank indicates corruption. Memory exhaustion must reject without publishing partial versions or silently dropping history.

**Concurrency changes hidden-mutation assumptions.** Pure immutable versions are safe for concurrent readers after publication/lifetime pinning. Independent writers create branches. A shared latest version needs lock/CAS/transaction conflict policy; CAS losers release candidates/retry.

Rollback DSU is normally single-owner mutable state. Sharing across threads requires a lock around operations/snapshot/rollback and prohibits one thread rolling back another's assumptions. A rollback scope should be thread/task confined.

Rerooting persistent arrays mutate orientation during reads. Concurrent access requires synchronization or a proven concurrent design; otherwise races can expose corrupt arrays/diffs. Calling the public values immutable is not a thread-safety proof. Path compression writes also contend.

Parallel offline algorithms can give each task a copied/persistent DSU root or carefully partition rollback scopes. Sharing large immutable parent maps helps but allocator/memory bandwidth matters. Deterministic representative selection may be needed for reproducible output.

Reclamation of persistent parents/diffs/logs uses roots/readers/tasks. Epochs/hazards/managed GC protect internal objects, but retention telemetry remains. Never truncate history/log storage while a version/snapshot reader can access it.

**Serialization should encode partitions/version semantics, not raw pointers.** For one snapshot, serialize canonical class labels or parent/rank arrays after validation, plus universe/schema and component metadata. Rebuilding may choose different representatives but must preserve equivalence. Canonical minimum-member labels improve portability at `Theta(n)` scan cost.

For a version history, store an initial universe and successful union operations/commit DAG, or persistent parent/rank graph records. Operation logs replay deterministically only with a specified union/representative/metadata policy. Checkpoints bound replay. Rollback stacks are execution state, not automatically durable histories.

Structural graph formats validate IDs/ranges, parent termination/acyclicity per version, root ranks/sizes, component count, version topology, diffs, and quotas. Reroot orientation/mutable arrays are process-local implementation details; serialize logical arrays/history.

Crash-safe publication writes parent/rank/log/checkpoint dependencies, checksums, and commit manifest before exposing a root. Recovery chooses a complete commit. GC traces all retained versions/checkpoints/readers/backups. In-memory persistence proves none of this.

Universe/element encoding, union heuristic, rank semantics, metadata, and format changes require migration/rebuild. Verify equivalence classes for every retained version or explicitly retire unsupported history.

**Security and resources follow history.** Bound universe, versions/branches/snapshots, union/find rate, parent/diff/log length, depth, component metadata, reader age, serialized history, diagnostics, and memory. Attackers can create many no-op/branch versions, alternate reroot access, pin old roots, or force expensive metadata merges.

Validate handles are authenticated/owned by the DSU/tenant/generation. Do not accept arbitrary array indices, log lengths, or internal representatives. Partition histories can reveal relationships later “deleted”; authorization and retention apply per version.

Hostile formats may contain parent cycles, out-of-range parents, impossible ranks/sizes, component-count mismatch, version cycles, huge diff chains, and decompression bombs. Validate iteratively under quotas before queries. Avoid logging full sensitive component membership.

Timing/path depth/reroot direction/log size can leak shape/history. Use isolation where adversaries share a structure. Compression changes timing across queries; do not promise constant-time confidentiality.

**Evidence compares partitions, not roots.** Maintain an independent immutable reference partition per version, for example canonical class-label sets. Generate union, find, connected, branch, same-class no-op, snapshot/rollback, and historical queries. Compare every retained version after every operation.

Validate forests per version: array lengths/ranges, acyclicity, termination, rank/size rules, component count, and equivalence against reference. Across versions check old partition isolation and sharing/changed cells. For hidden mutation, force many access/reroot orders and verify observational results remain identical.

Exhaust small universes and all union rank cases, chains/balanced trees, duplicate/self unions, branch from every version, alternating old/new access, compression, snapshot nesting, rollback to every boundary, rollback then new future, invalid/stale/cross-DSU handles, and exceptions at each write/log/diff step.

Metamorphic relations include reflexive connectivity; symmetry; union idempotence/commutativity by partition equality; connectivity monotonicity along a union-only lineage; branch isolation; rollback restoration; replay equivalence; representative membership; component count decreases iff classes differ; and serialization/rebuild partition equality.

Fault-inject parent/rank access/update, allocation, log push/pop, metadata merge, compression, reroot steps, root CAS, serialization write/flush/publication, and reclamation. Concurrent tests race readers/latest writers, prohibited rollback/reroot sharing, release, and cancellation under sanitizers/model checking where possible.

Benchmarks vary `n`, union/find ratio, successful/no-op unions, balanced/adversarial histories, compression policy, substrate, branch factor/depth, old/new version access locality, rollback nesting, reroot switching, retained roots/readers, metadata size, runtime/allocator/GC, threads, and serialization. Report parent reads/writes, rank comparisons, path depth, persistent array accesses/copies/bytes, diff/reroot steps, log bytes, allocations/reclamation/retention, cache behavior, latency quantiles, GC pauses, CAS retries, and validation.

The executable below uses immutable parent/rank tuples, union by rank, and read-only find. It creates linear and branching versions, verifies partitions, forest/rank/component invariants, idempotent root reuse, and maximum depth. Tuple updates copy `Theta(n)` and the trace has no path compression, rollback, persistent-array rerooting, concurrency, storage, or performance proof.

<!-- bijux-verify: {"id":"persistent-union-find-version-trace","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"v3_partition=0,1,2,3|4|5|6|7\nv5_partition=0,1|2,3|4,5|6|7\nv7_partition=0,1,2,3,4,5,6|7\nv3_components=5\nv7_components=2\nconnected_v7_0_6=True\nisolated_v3_0_6=True\nbranch_isolated=True\nsame_union_reuses_root=True\nmax_depth=2\nall_partitions=True\nall_invariants=True\nevidence=finite_persistent_union_find_trace\n","stderr":""}} -->
```python
def create(size):
    return (tuple(range(size)), tuple(0 for _ in range(size)), size)


def find(version, element):
    parent = version[0]
    current = element
    depth = 0
    while parent[current] != current:
        current = parent[current]
        depth += 1
    return current, depth


def replace(values, index, value):
    return values[:index] + (value,) + values[index + 1 :]


def union(version, left, right):
    parent, rank, components = version
    root_left, _ = find(version, left)
    root_right, _ = find(version, right)
    if root_left == root_right:
        return version
    if rank[root_left] < rank[root_right]:
        root_left, root_right = root_right, root_left
    parent = replace(parent, root_right, root_left)
    if rank[root_left] == rank[root_right]:
        rank = replace(rank, root_left, rank[root_left] + 1)
    return (parent, rank, components - 1)


def partition(version):
    groups = {}
    for element in range(len(version[0])):
        root, _ = find(version, element)
        if root not in groups:
            groups[root] = []
        groups[root].append(element)
    ordered = sorted(tuple(group) for group in groups.values())
    return tuple(ordered)


def render(version):
    return "|".join(",".join(str(element) for element in group) for group in partition(version))


def valid(version):
    parent, rank, components = version
    size = len(parent)
    if len(rank) != size or components != len(partition(version)):
        return False
    for element in range(size):
        seen = set()
        current = element
        while parent[current] != current:
            if current in seen or not 0 <= parent[current] < size:
                return False
            seen.add(current)
            if rank[current] >= rank[parent[current]]:
                return False
            current = parent[current]
        if not 0 <= rank[current] <= size.bit_length():
            return False
    return True


v0 = create(8)
v1 = union(v0, 0, 1)
v2 = union(v1, 2, 3)
v3 = union(v2, 0, 2)
v4 = union(v3, 4, 5)
v5 = union(v2, 4, 5)
v6 = union(v4, 5, 6)
v7 = union(v6, 3, 5)
same = union(v7, 0, 6)

versions = (v0, v1, v2, v3, v4, v5, v6, v7)
expected = (
    ((0,), (1,), (2,), (3,), (4,), (5,), (6,), (7,)),
    ((0, 1), (2,), (3,), (4,), (5,), (6,), (7,)),
    ((0, 1), (2, 3), (4,), (5,), (6,), (7,)),
    ((0, 1, 2, 3), (4,), (5,), (6,), (7,)),
    ((0, 1, 2, 3), (4, 5), (6,), (7,)),
    ((0, 1), (2, 3), (4, 5), (6,), (7,)),
    ((0, 1, 2, 3), (4, 5, 6), (7,)),
    ((0, 1, 2, 3, 4, 5, 6), (7,)),
)
max_depth = max(find(version, element)[1] for version in versions for element in range(8))

print("v3_partition=" + render(v3))
print("v5_partition=" + render(v5))
print("v7_partition=" + render(v7))
print("v3_components=" + str(v3[2]))
print("v7_components=" + str(v7[2]))
print("connected_v7_0_6=" + str(find(v7, 0)[0] == find(v7, 6)[0]))
print("isolated_v3_0_6=" + str(find(v3, 0)[0] != find(v3, 6)[0]))
print("branch_isolated=" + str(partition(v4) != partition(v5)))
print("same_union_reuses_root=" + str(same is v7))
print("max_depth=" + str(max_depth))
print("all_partitions=" + str(tuple(partition(version) for version in versions) == expected))
print("all_invariants=" + str(all(valid(version) for version in versions)))
print("evidence=finite_persistent_union_find_trace")
```

## Definitions and Notation

- `U={0,...,n-1}` is a fixed element universe.
- `Π_v` is the equivalence relation/partition denoted by version `v`.
- `Parent_v[x]` is `x`'s parent in version `v`; a root `r` satisfies `Parent_v[r]=r`.
- `find(v,x)` returns a representative of `x`'s class in `Π_v`.
- `union(v,x,y)=v'` yields the least partition coarsening `Π_v` that relates `x,y`.
- `Rank_v[r]` or `Size_v[r]` is authoritative at roots under the named linking heuristic.
- `Components_v` is the number of classes and decreases exactly on a successful merge.
- `depth_v(x)` is the number of parent edges to a root.
- A **compression write set** is every parent cell changed by find/halving/splitting.
- A **rollback record** contains every old field needed to reverse one mutation unit.
- `snapshot()` returns an opaque same-DSU rollback position; `rollback(s)` restores it under LIFO rules.
- Partial persistence has a linear version order; full persistence has a version tree; confluent persistence may form a DAG.
- A **persistent array diff** records `(index,old/new value,adjacent version)` according to its orientation.
- **Rerooting** reverses a diff path so a selected logical array version becomes concretely materialized.
- **Observational persistence** means internal state may change but public results for every version remain those of immutable values.

## Mechanisms, Invariants, or Proof Structure

**Partition abstraction.** Parent reachability groups elements by final self-parent root. Acyclicity/termination make find total. Representative equality induces an equivalence relation. Union changes one root parent and therefore merges exactly two classes.

**Rank-height proof.** Only roots link. Lower rank attaches beneath higher; equal rank increments the winner. By induction, rank `r` implies at least `2^r` class members. Thus maximum rank/height is logarithmic without compression. Nonroot ranks are ignored but parent rank must be greater in the simple invariant.

**Pure persistence proof.** Parent/rank indexed values are immutable. Union writes replacements in new persistent arrays/maps and reuses other storage. Find performs no writes. Induction over operations gives full branch isolation. Substrate access/copy costs are included separately.

**Rollback proof.** Before every mutable field change, log its location/old value or one complete union record. Rollback reverses records in strict reverse order, restoring parent, size/rank, component count, and metadata. Disabling compression bounds writes; if enabled, every compression write is logged.

**Historical proof.** A versioned field lookup selects the latest change applicable to queried time/ancestor. Historical find uses historical parent at every step. Updates only latest version under partial persistence. Version ordering/ancestry and field histories must agree.

**Observational hidden-mutation proof.** Rerooting/compression may change array/diff orientation or cached parents, but a refinement relation maps every public version handle to the same logical Parent/Rank arrays before and after. Operations preserve refinement, including exceptions/concurrency assumptions.

**Complexity decomposition.** Count forest depth/parent steps, persistent indexed access/update, tuple/page/node copy bytes, compression writes, log records, diff/reroot distance, allocation/reclamation, and version access pattern. Classical alpha bounds apply only after matching the exact algorithm/model.

**Lifecycle proof.** Version/snapshot handles are validated; roots/readers/tasks retain necessary arrays/maps/diffs/logs; publication is last; rollback/reroot failures restore a valid state; reclamation waits for every owner.

## Alternatives and Trade-Offs

| Design | Persistence behavior | Strength | Cost/limitation |
|---|---|---|---|
| Full array copy | Fully branchable | Simplest isolation | `Theta(n)` bytes per changed array |
| Immutable map parent/rank | Fully branchable | Straightforward proof | Path × map lookup, often `O(log^2 n)` |
| Persistent vector/trie arrays | Fully branchable | Better indexed sharing | Node-copy constants; compression writes |
| No-compression union by rank | Any above | Logarithmic depth, read-only find | Weaker than classical amortized bound |
| Functional compression returning version | Fully branchable API possible | Shortens returned branch | Stateful query/API threading and new analysis |
| Rollback arrays + log | LIFO backtracking | Fast, compact for DFS/offline work | Not arbitrary old-version updates; no cheap compression |
| Versioned/fat parent histories | Partial/full depending labels | Historical queries | History search, compression growth, ancestry complexity |
| Rerooting persistent arrays | Observational persistence | Near mutable access for local versions | Hidden mutation, reroot costs, thread/failure proof |
| Rebuild/checkpoint log | Historical/replay | Durable/simple audit | Replay/compaction and query latency |

Choose the weakest model satisfying the algorithm. A rollback DSU is often superior for DFS offline connectivity; a pure persistent vector DSU is safer for arbitrary branches; the advanced rerooted design belongs where its proof/runtime assumptions can be preserved.

## Failure Modes and Misconceptions

1. **Rollback called persistence:** it only restores a single stack timeline unless futures are retained separately.
2. **Compression omitted from log:** rollback leaves changed parents and wrong future costs/shape, possibly semantics with metadata.
3. **Representative as entity ID:** roots change on union and differ by version.
4. **Alpha bound copied blindly:** persistent-array and version operations change the model.
5. **Whole-copy cost hidden:** logarithmic forest height does not make tuple/array clone logarithmic.
6. **Rank updated incorrectly:** increment only the chosen root on equal-rank merge.
7. **Old-time find uses current parents:** historical answers become too coarse.
8. **Hidden mutation called thread-safe:** observational immutability does not synchronize reroot/compression.
9. **Stale handle accepted:** another DSU/generation/log future can corrupt rollback or query.
10. **Arbitrary deletion expected:** DSU cannot split connectivity without more information/structure.
11. **Metadata not restored:** component count/size/aggregate disagrees after rollback.
12. **Latest-root memory counted:** old roots, readers, diffs, logs, and allocator garbage retain storage.

## Worked Examples

### Example 1

**Rank bound.** A rank-3 root arose from equal-rank merges. By induction it represents at least `2^3=8` elements. In a universe of seven, rank three is impossible. Conclusion: rank supplies both height proof and corruption check.

### Example 2

**Pure branch.** From version with `{0,1}` and `{2,3}`, one branch unions `0,2`; another unions `4,5`. Each persistent parent/rank root changes independently. Conclusion: full persistence preserves two incomparable futures; representative integers may overlap without sharing partitions.

### Example 3

**Compression write set.** Path `7→6→4→0` compressed by find changes parents of 7,6 (and possibly 4) to 0. A rollback log containing only union root changes cannot restore the old forest. Conclusion: log every compression write or disable compression.

### Example 4

**Rollback snapshot.** At log length 10 take `s`; perform three successful unions; rollback to `s` pops three complete records. A no-op union either pushed a marker or did not change log by contract. Conclusion: operation-level undo alignment must match logging policy.

### Example 5

**Stale future.** Snapshot `s2` was taken after `s1`; rollback to `s1`, then create another union. Trying to “roll forward” to raw length `s2` reads records from the abandoned future or new branch. Conclusion: raw lengths are not freely persistent version handles.

### Example 6

**Map substrate multiplication.** Rank gives at most `log n` parent hops, but a balanced persistent map parent lookup costs `log n`; find can cost `log^2 n`. Conclusion: analyze forest and indexed substrate composition, not only DSU theory.

### Example 7

**Historical query.** Union `(a,b)` at version 3 and `(b,c)` at 8. `connected(a,c,5)` is false; current-parent traversal at version 8 says true. Conclusion: every parent lookup in historical find must use version 5.

### Example 8

**Reroot access order.** Versions form diff chain `v0-v1-v2`; `v2` is concrete. Reading `v0` reverses diffs so `v0` is concrete and preserves inverse information for v1/v2. Reading v2 reroots back. Conclusion: logical values persist while physical access work depends on version locality.

### Example 9

**Offline deletion.** Edge `(u,v)` is active on time interval `[2,7)`. Add it to covering time-segment nodes; DFS unions on entry and rollbacks on exit. Leaf time 8 correctly excludes it. Conclusion: rollback plus offline scheduling handles deletions without teaching DSU to split sets online.

### Example 10

**Design choice.** A theorem prover branches arbitrarily and queries old states concurrently. A single rollback stack is unsafe; choose immutable persistent indexed parents without compression first, or a proven persistent-array design if performance demands and concurrency is addressed. Conclusion: version topology and thread model dominate the heuristic choice.

## Cross-Program Connections

- Algorithm engineering: inverse-Ackermann amortization, rank proofs, offline segment-tree traversal, and substrate composition require model-specific analysis.
- Programming languages: hidden mutation, abstract types, persistent arrays, backtracking type inference, and observational equivalence connect semantics to runtime effects.
- Formal methods: partition refinement, acyclic forests, rollback simulation, and Coq/Isabelle developments support machine-checked correctness.
- Concurrent programming: immutable versions, mutable rollback scopes, rerooting reads, CAS publication, and reclamation have different synchronization needs.
- Database engineering: snapshot handles, linear histories, version trees, logs/checkpoints, reader retention, and vacuum resemble MVCC lifecycle.
- Graph algorithms: Kruskal, offline dynamic connectivity, and temporal connectivity choose DSU persistence according to edge-update scheduling.
- Security engineering: stale/cross-tenant handles, history pinning, malicious parent graphs, and sensitive equivalence histories require validation/quotas.
- Performance engineering: parent steps, array/map access, copies, reroots, logs, cache locality, allocation, and GC determine practical trade-offs.

## References

1. Sylvain Conchon and Jean-Christophe Filliâtre, “A Persistent Union-Find Data Structure,” ML Workshop, 2007. https://usr.lmf.cnrs.fr/~jcf/publis/puf-wml07.pdf
2. Jean-Christophe Filliâtre, author-maintained persistent array and persistent union-find implementations. https://usr.lmf.cnrs.fr/~jcf/software.en.html
3. James R. Driscoll, Neil Sarnak, Daniel D. Sleator, and Robert E. Tarjan, “Making Data Structures Persistent,” *Journal of Computer and System Sciences* 38(1), 1989. https://www.cs.cmu.edu/~sleator/papers/making-data-structures-persistent.pdf
4. C. Gaibisso, G. Gambosi, and M. Talamo, “A Partially Persistent Data Structure for the Set-Union Problem,” RAIRO, 1990. https://www.numdam.org/article/ITA_1990__24_2_189_0.pdf
5. Paul F. Dietz and Rajeev Raman, “Persistence, Amortization and Randomization,” University of Rochester technical report, 1991. https://urresearch.rochester.edu/institutionalPublicationPublicView.action?institutionalItemId=4899
6. Robert Sedgewick and Kevin Wayne, `WeightedQuickUnionPathCompressionUF`, *Algorithms, 4th Edition* official implementation. https://algs4.cs.princeton.edu/15uf/WeightedQuickUnionPathCompressionUF.java.html
7. Robert Sedgewick and Kevin Wayne, “Case Study: Union-Find,” *Algorithms, 4th Edition*. https://algs4.cs.princeton.edu/15uf/
8. Archive of Formal Proofs, “Relational Disjoint-Set Forests,” current proof document. https://isa-afp.org/browser_info/current/AFP/Relational_Disjoint_Set_Forests/document.pdf

## Exercises

### Exercise 1

**Prove the rank bound.** Give a complete induction that union by rank without path compression has height at most `floor(log2 n)`. State which implementation checks make the theorem applicable.

### Exercise 2

**Trace rollback with and without compression.** Starting from a parent chain and snapshot, perform a compressing find and one union. List the minimal log records required to restore exactly; compare with a no-compression union-by-size design.

### Exercise 3

**Design a fully persistent API.** Specify types/contracts for fixed-universe creation, find, connected, union, version handles, representatives, branching, iteration of classes, errors, and serialization. Choose a parent/rank substrate and derive costs.

### Exercise 4

**Choose among persistence models.** Select and justify designs for (a) Kruskal; (b) depth-first offline dynamic connectivity; (c) historical queries with latest-only unions; and (d) concurrent arbitrary theorem-prover branches. Include evidence and failure needs.

### Exercise 5

**Transfer to durable equivalence histories.** Design a crash-safe service that stores union commits and answers historical/branch queries. Include stable identities, commit DAG, checkpoints, conflict/confluent semantics, recovery, GC, migration, authorization, and verification; explain why raw rollback logs or representatives are insufficient.

## Answers to the Exercises

### Answer 1

Claim: a root of rank `r` contains at least `2^r` elements. Base: initial roots rank zero contain one. A rank changes only when two distinct equal-rank `r` roots merge; the winner rank becomes `r+1` and contains at least `2^r+2^r=2^(r+1)`. Unequal-rank merge does not change the winner rank and only increases its size. Parent links always attach lower/equal rank root under higher/incremented root, so rank strictly increases along each edge and path length is at most root rank.

For a universe of `n`, `2^r<=n`, hence `r<=floor(log2 n)` and height obeys the same bound. Applicability requires fixed valid indices, self-rooted acyclic initialization, unions linking roots only, lower under higher, increment only on equal ranks, no later rank decrease/corruption, and find following the version's parents. Path compression can shorten paths and does not invalidate the upper bound if performed correctly, but persistent/rollback writes need separate accounting.

### Answer 2

Suppose snapshot forest has `7→6→4→0` and compression rewrites `parent[7]=0`, `parent[6]=0`, and perhaps `parent[4]=0` if it was not already. Log each changed cell with its old parent in write order; rollback restores in reverse. Then union roots `r,s`: log losing root's old self-parent, winning root's old size/rank if changed, old component count, and any aggregate. A complete transaction marker can group these records. No-op policy is explicit.

Without compression, find writes nothing. Union by size changes only losing root parent, winning root size, and component count, so one fixed record restores all. This makes rollback space/time predictable and forest depth logarithmic. Logging only union while allowing compression is insufficient even if partition equivalence happens to remain: exact snapshot shape/metadata and subsequent rollback behavior are not restored.

### Answer 3

Use opaque `UniverseId`, `Version`, and version-scoped `Representative`; `create(n)->Version`; `find(v,x)->Rep`; `connected(v,x,y)->bool`; `union(v,x,y)->Version`; optional `classes(v)` explicitly costs at least a scan; and `serialize(v/history)` uses logical classes/validated version records. Reject out-of-range elements, foreign/stale universe/version handles, schema mismatches, and overflow. State that representative equality is valid only within the same version/universe and is not durable entity identity. Any version may be unioned, creating branches; old partitions remain unchanged.

Choose persistent vector/HAMT-like indexed parent/rank structures, union by rank, and read-only find. If parent access/update is `A(n)`/`U(n)`, find is `O(A(n) log n)` and union two finds plus one parent and optional rank update; allocation/bytes follow substrate path copies. A balanced map gives roughly `O(log^2 n)` find; a high-branch persistent vector can improve practical/index cost. Component count is stored. Validate every root's forest/ranks/partition, branches, allocation failure, lifetime, concurrent publication, and serialization. Do not claim classical compression bounds.

### Answer 4

Kruskal needs one forward ephemeral history: use mature weighted/ranked path-compressed DSU. Offline dynamic connectivity traverses a time segment tree depth-first: use rollback union-by-size/rank without compression, snapshot on entry, rollback on exit. Historical latest-only unions fit partial persistence with versioned parent/rank histories or a specialized partially persistent DSU; test time-indexed finds.

Concurrent arbitrary theorem-prover branches require fully persistent immutable indexed parents or the formally justified persistent-array construction with a concurrency-safe port; a single rollback stack and unsynchronized rerooting are inappropriate. For each choice validate partitions/invariants, operation schedule, failures, handles, memory retention, and target benchmarks. Classical bounds are quoted only for exact algorithms; report writes/logs/copies/reroots and tail behavior.

### Answer 5

Assign stable universe and element IDs independent of representatives. A commit contains parent commit(s), canonical union operation(s), component-metadata policy, author/provenance, schema, and checksum; a root/checkpoint identifies a validated logical partition. Serialize operations plus periodic immutable parent/rank or canonical-class checkpoints. Write dependencies/checkpoint, flush/checksum, then atomically publish the commit manifest. Recovery selects complete commits and replays deterministically from the nearest valid checkpoint.

Branch commits can coexist. A confluent merge must define the least equivalence containing both partitions or replay both operation sets, resolve component metadata, deduplicate ancestry, and bound work; ordinary element union is not this merge. Readers pin commits; GC traces heads, readers, backups, replicas, and legal holds. Migrations rebuild/check every retained partition under new element/metadata/format rules. Authorize per universe/commit/history and redact sensitive diagnostics.

Validate commit DAG acyclicity/references, operation indices, checkpoint parent termination/ranks/counts, replay/checkpoint equivalence, metadata, quotas, and hashes. Fault-inject writes/flush/root publication, corrupt/truncate records, stall readers, interrupt GC/migration, and test concurrent commits. Raw rollback logs depend on one process timeline and abandoned futures; representatives are version-local, so neither is a durable public identity/history format.
