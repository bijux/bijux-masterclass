---
module_id: DSE-043
program: Data Structures Engineering
level: 1
module_number: 43
title: Disjoint-Set Forests
status: complete
last_verified: 2026-08-30
---

# Disjoint-Set Forests

## One-Page Review

### Governing question

How can an engineer maintain a partition under repeated merges so equivalence queries are correct, nearly constant amortized time, memory-safe, and explicit about identity, mutation, concurrency, rollback, and evidence?

### Essential definitions

- A **disjoint-set union (DSU)** or **union–find** structure represents a partition of a universe into pairwise disjoint nonempty sets.
- `make_set(x)` creates the singleton set `{x}` when dynamic membership is supported.
- `find(x)` returns a representative naming the current set containing `x`.
- `union(x,y)` replaces the two containing sets by their union, doing nothing if they are already equal.
- A **disjoint-set forest** stores one parent per element; each root is its own parent and represents one component.
- **union by size/rank** attaches a smaller/shallower root under a larger/deeper root.
- **path compression** rewrites nodes on a find path to point directly to the root.
- **path splitting/halving** rewrites paths incrementally during traversal.
- `alpha(n)` is the inverse Ackermann function appearing in the classical amortized bound; it grows extraordinarily slowly but is not literally a universal constant.
- A **rollback DSU** logs reversible union changes and normally avoids destructive path compression.

### Central model, mechanism, or theorem

For dense elements `0..n-1`, store `parent[n]` and either `size[n]` or `rank[n]`. Initially `parent[x]=x` and root metadata is one/zero. `find` follows parents to a root. `union` first finds both roots; if equal it reports a redundant merge. Otherwise union by size attaches the smaller root to the larger and adds its size to the winner.

The forest invariant makes equivalence exact: two elements occupy the same partition block if and only if their root representatives are equal. Linking only roots prevents cycles. Path compression preserves membership because every rewritten parent is an ancestor in the same tree. Union by size alone bounds tree height by `floor(log2 n)`: whenever a node's depth increases, the containing set size at least doubles. With path compression and union by rank/size, a sequence of `m` operations on `n` elements has the classical `O(m alpha(n))` amortized bound under the standard model.

The guarantee is amortized over a sequence, not worst-case constant latency for one operation. Path compression mutates during reads, invalidates rollback history unless logged, and introduces write races under concurrency. Stable component identity also needs a separate policy because the chosen root depends on union order and tie-breaking.

### Critical invariants

1. Every admitted element has exactly one parent in the universe, and following parents terminates at a self-parent root.
2. Only a root may become the child of another root during union; no operation links arbitrary interior nodes.
3. Two elements are equivalent exactly when `find` returns the same root.
4. Stored root size equals the number of elements in its tree; rank follows its declared upper-bound rule. Nonroot metadata is ignored or has explicitly defined meaning.
5. Component count begins at admitted-element count, decrements exactly once per successful union, and never changes for a redundant union or find.
6. Compression, splitting, or halving only redirects a node to an ancestor in the same tree and cannot create or merge components.
7. Bounds, membership, reset, reuse, external-key mapping, representative stability, and invalidation policies are explicit.
8. Concurrent or persistent publication never exposes a parent cycle, a root with inconsistent metadata, or an unprotected reclaimed mapping/version.

### Common failures

- Assigning `parent[x]=y` without first finding roots, which can create deep trees or cycles.
- Updating size/rank on a nonroot or adding sizes during a redundant union.
- Incrementing rank on every merge instead of only equal-rank root merges.
- Calling a read-only-looking `find` concurrently even though path compression writes parents.
- Treating a root index as a durable business component ID.
- Using recursive find on an attacker-created or corrupted chain and exhausting the stack.
- Combining path compression with rollback but logging only union links.
- Forgetting to include isolated singleton components in counts or output.
- Using DSU for deletion or connectivity in a fully dynamic graph; ordinary DSU only merges.
- Claiming `O(1)` worst-case operations because `alpha(n)` is small in practical ranges.

### Compact example

Ten singleton elements receive eight successful balanced unions, leaving components `{0..7}` and `{8,9}`. Before compression, element 7 has parent depth three; `find(7)` returns root 0 and reduces its depth to one without changing the component count or membership. Unioning 3 and 7 is redundant and leaves root size eight. Merging 9 with 7 produces one component of size ten. A validator independently checks root termination, root sizes, and component count.

### Connections

[DSE-002](002-representation-invariants.md), [DSE-003](003-operation-contracts.md), and [DSE-008](008-iterators-and-traversal-protocols.md) supply invariant, failure, and mutation-during-traversal discipline. [DSE-041](041-adjacency-matrices-lists-and-edge-arrays.md) and [DSE-042](042-compressed-sparse-graph-layouts.md) provide graph identities/layouts. The [program roadmap](../ROADMAP.md) next applies forests to connectivity, spanning structures, offline algorithms, and system-scale components.

## Governing Question

Which universe, equivalence semantics, representative policy, union heuristic, path-shortening rule, metadata, update model, concurrency or rollback requirement, and persistence boundary produce the right disjoint-set forest for a real system?

## Why This Matters

Disjoint-set forests solve a deceptively narrow problem: equivalence classes only merge. That restriction makes them extraordinarily useful. Kruskal's minimum-spanning-forest algorithm rejects an edge when its endpoints already share a component. Image labeling merges neighboring pixels. Type inference and unification maintain equalities. Percolation experiments, clustering, account/entity linking, network connectivity, and offline query algorithms repeatedly ask whether two items have become connected.

The textbook code fits on a page, but production contracts do not. Elements may be external strings rather than dense indices. Duplicate insertion, absent keys, reset, and mapping ownership need semantics. Components may carry aggregates. The chosen root may leak as an ID and then change on a later union. Compression mutates parent state on a query. Concurrent writers can create cycles or lose metadata updates. Rollback conflicts with compression. A serialized forest can preserve accidental topology or only the logical partition. Adversarial inputs can target bounds, arithmetic, recursion, or output amplification.

The celebrated inverse-Ackermann bound is also easy to misuse. It applies to sequences with specified heuristics and a precise cost model. It is not a proof of one-operation constant latency, thread safety, cache efficiency, or suitability for deletions. Engineering begins by proving the simpler partition invariants, then attaches performance and lifecycle claims no stronger than the implementation and evidence support.

## Prerequisites and Retrieval

Retrieve abstract/concrete representation distinctions from [DSE-001](001-abstract-data-types-and-concrete-representations.md), invariants from [DSE-002](002-representation-invariants.md), and operation/failure contracts from [DSE-003](003-operation-contracts.md). Retrieve cost sequences from [DSE-004](004-time-space-and-allocation-cost.md), locality from [DSE-006](006-memory-locality-and-cache-behavior.md), generic identity constraints from [DSE-007](007-genericity-and-type-constraints.md), traversal mutation from [DSE-008](008-iterators-and-traversal-protocols.md), property tests from [DSE-009](009-property-based-testing-of-data-structures.md), and benchmark controls from [DSE-010](010-benchmarking-a-structure-without-misleading-results.md).

## Learning Objectives

After completing this module, you should be able to:

1. specify partition, membership, representative, union, and failure semantics;
2. derive the parent-forest and component-metadata invariants;
3. implement iterative find with full compression and union by size or rank;
4. prove logarithmic height for weighted union without compression;
5. state the inverse-Ackermann amortized result accurately and distinguish it from worst-case latency;
6. attach component aggregates without corrupting redundant-union behavior;
7. select compression, halving, splitting, rollback, persistence, or concurrency variants;
8. protect external-key mappings, stable identities, integer arithmetic, and hostile inputs;
9. validate the forest independently against a reference partition; and
10. benchmark operation sequences, path depths, writes, contention, and memory rather than isolated happy paths.

## Core Exposition

**Specify the partition abstractly.** A universe `U` is divided into blocks whose union is `U` and whose pairwise intersections are empty. The core operations are singleton creation, representative lookup, and union. Some fixed-universe APIs create all `n` singletons at construction. Dynamic APIs admit keys over time. Decide what absent `find`, duplicate `make_set`, and capacity exhaustion do before choosing storage.

`find(x)` need not return the smallest, oldest, or most meaningful member. It returns an implementation representative satisfying stability only until a union can change the root. If an application needs a stable cluster ID, store an aggregate such as minimum admitted ID at the root, allocate an external component object, or maintain an indirection layer. Do not accidentally promise root identity because early tests happen to preserve it.

The dense fixed-universe representation stores one parent per integer element. At initialization, `parent[x]=x`; every element is a singleton root. A root's `size` is one. Component count is `n`. External keys require a map `key -> dense_index` and often a reverse vector. The map's hashing, equality, memory, lifetime, and denial-of-service behavior are then part of the DSU system even though the forest remains array-based.

An explicit membership bit may distinguish unused capacity from admitted elements. Reusing a removed index is unsafe because ordinary DSU has no element deletion and prior handles may still name it. Use generations in handles, rebuild a new universe, or prohibit reuse. If dynamic admission appends indices, checked capacity growth and mapping insertion should succeed before publishing the new member.

**The forest encodes equivalence by reachability to roots.** Each element points to another element in its tree. A root points to itself. Since parent links are functional, acyclic, and root-terminated, each element has exactly one root. Define `find(x)` as that root. The sets induced by equal roots are disjoint and cover admitted elements, hence form a partition.

To merge elements `x` and `y`, compute roots `rx=find(x)` and `ry=find(y)`. If equal, the partition already contains their union; return false/no-change. Otherwise link exactly one root beneath the other. Connecting two trees with one root-to-root edge yields one acyclic tree and merges exactly their two blocks. Decrement component count once. This proof fails if code links arbitrary `x` beneath `y`: the nodes can lie inside trees, and a link can produce a cycle or detach the interpretation of root metadata.

A naïve union can create a length-`n-1` chain, making find linear. **Union by size** attaches the smaller root beneath the larger and adds sizes at the winner. Ties use a deterministic or unspecified policy. **Union by rank** stores an upper bound related to tree height: attach lower rank beneath higher; when ranks tie, select a root and increment only its rank. Size and rank are different. After compression, rank is not current height and should not be recomputed casually.

Weighted union without compression has height at most `floor(log2 n)`. Consider a node whose depth increases because its root tree is attached below another. Under union by size, the destination tree has size at least the source tree, so the node's new component has at least twice its previous size. A component containing any node cannot exceed `n`; therefore that node's depth can increase at most `floor(log2 n)` times. The same doubling-style argument applies to rank, with a rank-`r` root containing at least `2^r` nodes.

This logarithmic proof already provides robust behavior. Path compression improves sequences further. A two-pass iterative find first walks to the root, then walks the original path again and points each visited node directly to the root. It avoids recursion depth and makes the mutation explicit. The second pass must preserve the old next parent before overwriting it.

Path halving sets each visited node to its grandparent while advancing; path splitting sets every visited node to its grandparent and advances differently. Both shorten paths incrementally with fewer structural phases. Exact reads/writes, concurrency interaction, and resulting shape differ. Name the chosen variant in code and benchmarks instead of labeling any parent rewrite “compression.”

Compression preserves equivalence: every new parent is the existing root or an ancestor on the same root path. It cannot cross between trees. It also cannot change root size or component count. Nonroot size entries may retain stale historical values; the API must read size only through `size[find(x)]` or clear nonroot metadata to make misuse obvious.

**The amortized result is sequence-based.** Tarjan's classical analysis shows that linking by rank/size with path compression supports operation sequences in `O(m alpha(n))` time under standard formulations, with small variations in parameters and models. `alpha` is the inverse of a rapidly growing Ackermann function and is tiny for conceivable data sizes. But mathematical accuracy matters: it is not literally constant as an asymptotic function, and an individual find may traverse a nonconstant path before compressing it.

Amortized time does not cap tail latency. A system that must bound every operation may choose union by size without compression for logarithmic worst-case paths, scheduled compression, or another representation. Real time also includes bounds checks, external mapping, cache misses, atomics, allocator behavior, and component aggregate work. A microbenchmark observing 20 ns does not prove the asymptotic theorem; the theorem does not predict the exact nanoseconds.

**Metadata turns DSU into a component service.** Size is the simplest aggregate. Minimum key, maximum timestamp, sum, bounding box, parity constraint, member list handle, or application state may live at roots. On a successful merge, combine losing-root metadata into the winner exactly once. A redundant union must not double-count. The combine operator needs associativity or a deterministic order if results must not depend on union schedule.

Some metadata is not incrementally mergeable or becomes expensive: sorted member lists, histograms, and external resources need ownership and failure rules. If combination can throw/fail after the parent is linked, the forest and metadata diverge. Prepare a fallible result before structural publication, use a reversible operation, or declare a basic guarantee with a repair path. Moving root-owned resources must leave the loser in a defined nonroot state.

Weighted/potential DSU stores a relation between a node and its parent, enabling parity, distance differences, or group-valued constraints. Find accumulates potentials to the root and compression must rewrite each node's potential to preserve the same relation. Union derives the new root-to-root potential from the asserted relationship. This is a different invariant surface; copying plain compression while forgetting potential updates returns plausible but wrong constraints.

**Applications inherit the monotone-update limit.** In Kruskal's algorithm, begin with one set per vertex. Process edges by nondecreasing weight. An edge joining distinct sets is selected and its components unioned; an edge within one set would create a cycle and is rejected. DSU supplies connectivity for the prefix of selected edges. It does not prove the cut/exchange theorem that makes Kruskal optimal.

For an incremental graph, union each inserted undirected edge. `same(u,v)` answers current connectivity, including isolated singleton vertices. Deleting an edge cannot split a DSU component. Continuing to answer from the old forest yields false connectivity. Fully dynamic connectivity requires more sophisticated data structures, rebuilds, or an offline transformation.

Offline deletion can reverse time: if all final active edges are known, build them, process operations backward, and turn forward deletions into reverse additions. Segment-tree-over-time methods assign each edge to time intervals and use rollback DSU while traversing the tree. These work because query ordering and reversibility are redesigned; ordinary online DSU has not gained deletion.

Component enumeration is not free. Calling find on all `n` elements and grouping costs `Theta(n)` plus mapping/output, even if each find is nearly constant amortized. Maintaining explicit member lists can make enumeration cheap but complicates union and memory. Small-to-large list merging moves each member `O(log n)` times, but exposes another invalidation and ownership surface.

**Rollback changes the optimization choice.** A rollback DSU records enough state for every successful union: losing root, winning root, previous winner size/rank/metadata, and component count or a marker for redundancy. A snapshot is a history-stack length; rollback pops until that length. Union by size keeps tree height logarithmic without path compression.

Full compression rewrites many parents during find. To roll it back, every rewrite must be logged in order, increasing history and complicating queries. Therefore common rollback designs omit compression. They retain logarithmic find through weighting and achieve predictable reversible updates. Persistent versions may use path copying or immutable trees, but ordinary array mutation plus a history stack only supports stack-disciplined rollback, not arbitrary branching versions.

Never expose a rollback snapshot integer without binding it to the DSU instance/generation. Rolling back past an application's live handles or external side effects can violate higher-level invariants. Component metadata must be restored with the structure. A redundant union often pushes a no-op marker if callers expect exactly one rollback action per attempted union.

**Concurrency is a different algorithm, not a mutex removal.** A coarse lock around every find/union is the simplest linearizable implementation. Compression can run under the lock; root metadata and component count stay coherent. Read-mostly workloads may offer an uncompressed read-only find under a shared lock and compressed finds under exclusive access, but parent changes by union still require synchronization.

Naïve lock-free union can create a two-cycle: thread A decides to link root `r` under `s` while thread B links `s` under `r`. Rank/size comparisons plus deterministic root-ID tie-breaking and compare-and-swap protocols prevent opposing choices, but validation after races remains essential. Losing a root CAS requires refinding; blindly updating size can double-count or update a node that ceased to be a root.

Concurrent path compression writes parent pointers. Atomic parent loads/stores prevent data races but do not alone prove linearizability, acyclicity, metadata correctness, or progress. Algorithms may use splitting with CAS, root locking, or phases. Component count and aggregates need their own atomic/lock protocol. Memory order must guarantee initialized mapping/metadata is visible with published membership.

False sharing can dominate dense parent arrays when threads update nearby elements. Random root choice, deterministic tie rules, or workload partitions affect contention. Parallel bulk union algorithms often alternate hooking roots and shortcutting paths in rounds rather than reuse sequential union verbatim. Benchmark skewed hot components, adversarial equal-rank merges, stalled threads, retries, and correctness histories.

**Persistence should favor logical meaning.** Serializing `parent` and rank/size exactly preserves accidental topology but creates a format coupled to compression history, integer width, mapping, and implementation version. A logical partition can instead serialize external element keys and a stable component label, then rebuild balanced forests on load. This loses physical reproducibility but is often more durable.

If storing physical arrays, include format version, admitted count/capacity, widths, mapping digest, component count, metadata schema, checksum/authentication, and snapshot generation. Validate parent bounds before dereferencing, detect cycles independently, find every root, recompute root sizes, verify component count, and validate metadata. A self-consistent malicious partition may still be unauthorized business data, so verify provenance separately.

Crash-safe mutation needs a log or copy-on-write snapshot. Persisting `parent[loser]=winner` before winner size can expose a recoverable partition with stale aggregate; persisting size first can count members not yet linked. A write-ahead logical union log plus deterministic replay, or immutable replacement, is easier to reason about. Flush/fence order and torn-write detection are storage contracts beyond in-memory correctness.

**Security begins with the universe boundary.** Validate dense indices before reading `parent[x]`; negative-to-unsigned casts are dangerous. Bound dynamic elements, mapping bytes, history, metadata, and enumeration output. Hash-flooding attacks may target external-key admission even while forest operations remain fast. Use a suitable map/threat model and avoid exposing internal capacity or stale entries.

Iterative find avoids stack exhaustion from corrupted or legacy chains. It still needs cycle defenses when loading untrusted data: a step limit, coloring, or tortoise-hare validation performed before treating the object as live. Production in-memory find may omit repeated cycle checks after construction if all mutations are encapsulated and invariants have been established; clarify the trust boundary.

Stable-root expectations can become authorization bugs. If access policy is stored by representative ID and a union changes the root, privileges can disappear or attach incorrectly. Put authorization on a stable component object or define an audited merge policy. Similarly, tenant-separated universes must never admit a cross-tenant union merely because dense indices collide.

Resource amplification remains possible. A request to enumerate a huge component can cost linear time and output. A stream of unique external keys consumes mapping and arrays. Rollback histories can grow without bound. Rate-limit or paginate output, cap admission/history, and account resources per owner. The inverse-Ackermann theorem covers none of these costs.

**Evidence starts with an independent partition model.** For small tests, maintain a component label per element. A reference union scans and relabels all members of one block, deliberately using a different representation. After every generated operation, compare `same(x,y)`, component count, sizes, and group membership. Relabel root names canonically because representatives may differ while partitions are equal.

Independently validate the forest: every parent is in range; root walks terminate; roots self-parent; number of distinct roots equals component count; every root's recomputed member count equals stored size; nonroot ranks/sizes are never used; and any rank rule holds. For a compressed forest, verify compression did not change canonicalized groups. Validate external map/reverse-map bijection and generations.

Exhaust small universes and union sequences, including `n=0`, one element, self-union, repeated union, reverse argument order, equal/unequal sizes, last index, all elements connected, all isolated, balanced merges, and deliberately long legal trees. Generate arbitrary equivalence relations, build through different union orders, and compare the logical partition even when roots and shapes differ.

Metamorphic properties include idempotence `union(x,x)` and repeated `union(x,y)`; symmetry of `same`; reflexivity; transitivity; monotone connectivity; component count decreasing exactly on a successful merge; size sum over roots equaling admitted count; find preserving partition; and permutation invariance after remapping element IDs. Union order may change roots and shape but not the transitive closure of the same undirected pair set.

Failure injection targets mapping growth, array growth, aggregate combination, serialization, and log writes. Rollback tests compare every prefix/suffix against a freshly replayed reference. Weighted/potential variants use an independent constraint solver on small cases. Persistent versions compare all live version branches. Concurrent variants require linearizability or their documented weaker criterion, cycle/metadata checks after quiescence, forced opposing-root races, sanitizers, retry/livelock metrics, and stalled-thread scenarios.

Benchmarks use sequences, not one warmed-up find. Vary `n`, union/find ratio, successful/redundant unions, pair locality, balanced versus adversarial order, component-size skew, external-key mapping, compression variant, metadata width, and enumeration. Measure distributions of latency, parent reads/writes, traversed depth before/after compression, bytes, cache misses, branch behavior, allocation, throughput scaling, contention, CAS retries, and rollback history. Separate initialization, mapping, steady operations, enumeration, serialization, and validation.

The executable below uses dense fixed membership, union by size, deterministic root-ID tie-breaking, iterative full compression, component size, and explicit validation. A balanced merge schedule creates a depth-three path before compression. The trace demonstrates redundant union, two components, group enumeration, a final merge, and all-parent compression. It is finite sequential evidence, not a proof of the amortized theorem, rollback, concurrency, persistent recovery, external-key safety, or production performance.

<!-- bijux-verify: {"id":"disjoint-set-forest-trace","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"initial_components=10\nmerge_results=1,1,1,1,1,1,1,1\ncomponents_after_batches=2\ndepth_7_before=3\nfind_7=0\ndepth_7_after=1\nsame_3_7=True\nredundant_merge=False\nsize_7=8\ngroups_before=0:0,1,2,3,4,5,6,7;8:8,9\nfinal_merge=True\nfinal_components=1\nsize_9=10\nparents=0,0,0,0,0,0,0,0,0,0\ninvariant=True\nevidence=finite_disjoint_set_forest_trace\n","stderr":""}} -->
```python
class DisjointSet:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        self.components = n

    def find(self, x):
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[x] != x:
            next_x = self.parent[x]
            self.parent[x] = root
            x = next_x
        return root

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.size[rx] < self.size[ry] or (self.size[rx] == self.size[ry] and rx > ry):
            rx, ry = ry, rx
        self.parent[ry] = rx
        self.size[rx] += self.size[ry]
        self.components -= 1
        return True

    def depth(self, x):
        depth = 0
        while self.parent[x] != x:
            x = self.parent[x]
            depth += 1
        return depth

    def validate(self):
        n = len(self.parent)
        if any(not 0 <= p < n for p in self.parent):
            return False
        counts = {}
        for x in range(n):
            seen = set()
            current = x
            while self.parent[current] != current:
                if current in seen:
                    return False
                seen.add(current)
                current = self.parent[current]
            counts[current] = counts.get(current, 0) + 1
        return len(counts) == self.components and all(self.size[root] == count for root, count in counts.items())


dsu = DisjointSet(10)
merges = [(0, 1), (2, 3), (0, 2), (4, 5), (6, 7), (4, 6), (0, 4), (8, 9)]
results = [dsu.union(x, y) for x, y in merges]
depth_before = dsu.depth(7)
root_seven = dsu.find(7)
depth_after = dsu.depth(7)
same = dsu.find(3) == dsu.find(7)
redundant = dsu.union(3, 7)
size_seven = dsu.size[dsu.find(7)]
groups = {}
for x in range(10):
    groups.setdefault(dsu.find(x), []).append(x)
groups_text = ";".join(f"{root}:" + ",".join(map(str, members)) for root, members in sorted(groups.items()))
final_merge = dsu.union(9, 7)
size_nine = dsu.size[dsu.find(9)]
for x in range(10):
    dsu.find(x)

print("initial_components=10")
print("merge_results=" + ",".join("1" if result else "0" for result in results))
print(f"components_after_batches={len(groups)}")
print(f"depth_7_before={depth_before}")
print(f"find_7={root_seven}")
print(f"depth_7_after={depth_after}")
print(f"same_3_7={same}")
print(f"redundant_merge={redundant}")
print(f"size_7={size_seven}")
print(f"groups_before={groups_text}")
print(f"final_merge={final_merge}")
print(f"final_components={dsu.components}")
print(f"size_9={size_nine}")
print("parents=" + ",".join(map(str, dsu.parent)))
print(f"invariant={dsu.validate()}")
print("evidence=finite_disjoint_set_forest_trace")
```

## Definitions and Notation

Let `U` be the admitted universe and `Pi` its partition. Write `x ~ y` when `x` and `y` are in the same block. For dense storage, `P[x]` is parent, `S[r]` is size at root `r`, and `C` is component count. A representative `R(x)` is the root reached from `x`. Height and depth describe physical forest topology, not abstract partition structure. `m` denotes operation-sequence length and `n=|U|`; `alpha` denotes the inverse Ackermann function under the cited analysis convention.

A **successful union** merges two previously distinct blocks. A **redundant union** observes one block and makes no logical change. A **compression write** changes topology without changing `Pi`. A **canonical partition** for tests replaces arbitrary roots with a deterministic label such as each block's minimum element. A **snapshot** in rollback DSU is a history position, not automatically a durable or branching version.

## Mechanisms, Invariants, or Proof Structure

Correctness has three independent layers. Forest validity proves bounded parent references, acyclicity, and one self-parent root per tree. Partition validity defines blocks by equal roots and proves root-to-root union merges exactly two blocks. Metadata validity recomputes root sizes/count and verifies updates occur exactly once on successful merges.

Performance adds separate lemmas: size/rank linking yields logarithmic height by doubling; compression rewrites only within a tree; the classical amortized analysis bounds a sequence with both heuristics by inverse-Ackermann factors. External maps, aggregates, enumeration, rollback logs, synchronization, persistence, and hostile validation require their own costs and proofs and are never hidden inside the forest theorem.

## Alternatives and Trade-Offs

| Design | Strength | Cost or restriction |
|---|---|---|
| naïve parent forest | minimal implementation | linear-height adversarial chains |
| union by size/rank | logarithmic worst-case height without compression | root metadata and tie policy |
| full compression | excellent repeated-query amortization | query writes, rollback/concurrency complexity |
| splitting/halving | one-pass shortening | different writes and proof/concurrency details |
| rollback weighted DSU | reversible offline algorithms | normally no compression; stack-only history |
| persistent DSU | queries across versions | path-copying/version memory and complexity |
| external-key DSU | arbitrary identities | map ownership, hashing, memory, key lifecycle |
| concurrent/parallel union–find | shared bulk/incremental workloads | atomics/locks, retries, metadata and proof surface |
| explicit component labels/lists | direct stable labels/enumeration | expensive relabel/merge or list ownership |

Choose based on monotone versus reversible updates, stable identity, tail-latency needs, query/write ratio, component metadata, element universe, concurrency, and persistence—not only the smallest observed `alpha`.

## Failure Modes and Misconceptions

- The root is an implementation representative, not automatically the canonical member or permanent component identifier.
- Path compression improves future paths but mutates on `find`; `const`, shared-lock, snapshot, and rollback claims must account for writes.
- Rank is not size and, after compression, is not current height.
- Only root metadata is authoritative unless another invariant explicitly maintains nonroot values.
- Redundant union must not decrement component count or combine aggregates twice.
- DSU answers connectivity under inserted relations; it cannot explain the path or produce a witness without extra structure.
- Ordinary DSU cannot split a component after edge/relation deletion.
- The inverse-Ackermann bound does not include mapping, enumeration, serialization, I/O, or user aggregate costs.
- Atomic parents alone do not prevent cycles, lost size updates, or unsafe component identity under concurrency.
- Persisting arrays preserves bytes, not necessarily a stable semantic format or authorized partition.

## Worked Examples

### Example 1

Starting from four singleton roots, `union(0,1)` and `union(2,3)` create two size-two trees. `union(1,3)` must first find roots; linking element 1 directly to 3 would connect interior nodes and ignore root metadata. Root-to-root linking produces one size-four tree.

### Example 2

Under union by size, a node reaching depth five must belong to a component of at least `2^5=32` elements. Its depth cannot increase again and again without the component doubling, which gives the logarithmic height bound before compression.

### Example 3

A path `7->6->4->0` becomes `7->0`, `6->0`, and `4->0` after full two-pass compression from 7. Set membership, root size, and component count do not change; only parent topology and future cost change.

### Example 4

If size-eight roots 2 and 10 tie, a deterministic rule may select smaller root 2. Reversing union arguments still produces root 2. This improves reproducibility but does not make 2 a durable business identity after it later joins a larger component.

### Example 5

A component stores the sum of account balances. On a successful union, add loser sum once to winner. A repeated union of already-equivalent accounts must return false and leave the sum unchanged; otherwise replayed events inflate balances.

### Example 6

A rollback DSU at history position 12 performs three union attempts, one redundant. If one action per attempt is contractual, history records two structural changes and one no-op marker. Rolling back to 12 restores parents, sizes, metadata, and component count exactly.

### Example 7

An incremental graph inserts edges `(a,b)` and `(b,c)`; DSU correctly reports `a~c`. Deleting `(b,c)` may disconnect `c`, but the forest remains merged. Correct handling requires rebuild, offline reverse processing, or a fully dynamic connectivity structure.

### Example 8

Two threads see equal roots `r` and `s`. If each stores the other as parent, the result is a two-cycle. A concurrent algorithm uses a deterministic orientation and conditional atomic root update, then retries/refinds when its expected root changed.

### Example 9

A loaded parent array `[1,2,0]` has every value in range yet forms a cycle with no self-parent root. Range checks alone are insufficient; loader validation must detect termination/cycles before any unrestricted find.

### Example 10

One million successful/redundant operations can be fast while enumerating all groups still reads every element and emits linear output. Service limits and benchmarks must treat enumeration separately from `find`/`union` amortization.

## Cross-Program Connections

- **Algorithms:** minimum spanning forests, connected components, unification, percolation, and offline dynamic connectivity rely on DSU's monotone partition.
- **Database engineering:** stable logical IDs, replay/idempotence, snapshots, logs, and compaction resemble durable state-management concerns.
- **Concurrent programming:** parent hooking, shortening, linearization, CAS retries, metadata races, and false sharing require specialized proofs.
- **Security engineering:** tenant boundaries, authorization identity, hostile indices/mappings, stack safety, and resource caps surround the core arrays.
- **Distributed systems:** a local DSU is not a distributed consensus protocol; merging replicated equivalence facts needs ordering, convergence, provenance, and deletion semantics.
- **Programming languages:** type-variable unification and equivalence-class implementations attach domain-specific metadata and explanations.
- **Testing and reliability:** reference partitions, metamorphic closure, rollback replay, parser fuzzing, and concurrent history checking are reusable evidence patterns.

## References

1. [Robert Sedgewick and Kevin Wayne, *Algorithms, 4th Edition*: Union–Find Case Study](https://algs4.cs.princeton.edu/15uf/).
2. [Princeton University, *Union-Find Algorithms* lecture notes](https://www.cs.princeton.edu/~rs/AlgsDS07/01UnionFind.pdf).
3. [Princeton Algorithms, `UF` API documentation](https://algs4.cs.princeton.edu/code/javadoc/edu/princeton/cs/algs4/UF.html).
4. [petgraph, `UnionFind` API documentation](https://docs.rs/petgraph/latest/petgraph/unionfind/struct.UnionFind.html).
5. [NetworkX, `UnionFind` maintained implementation](https://networkx.org/documentation/stable/_modules/networkx/utils/union_find.html).
6. [LLVM, `EquivalenceClasses` maintained implementation](https://llvm.org/doxygen/EquivalenceClasses_8h_source.html).
7. [Jeff Erickson, *Algorithms*](https://jeffe.cs.illinois.edu/teaching/algorithms/book/Algorithms-JeffE.pdf).
8. [Stanford CS166, *Disjoint-Set Forests* lecture notes](https://web.stanford.edu/class/archive/cs/cs166/cs166.1166/lectures/05/Small05.pdf).

## Exercises

### Exercise 1

For `n=8`, apply union by size with smaller-root tie-breaking to `(0,1),(2,3),(4,5),(6,7),(0,2),(4,6),(0,4)`. Give parent and root-size arrays before compression, the depth of 7, and arrays after `find(7)` with full compression.

### Exercise 2

Prove that union by size without path compression gives maximum height at most `floor(log2 n)`. State exactly when a node's depth increases and why this causes a doubling argument.

### Exercise 3

Design a DSU whose components maintain minimum external key and sum of weights. Specify successful/redundant union, representative exposure, combine failure, overflow, and validation semantics.

### Exercise 4

Explain why ordinary compressed DSU cannot support rollback or arbitrary edge deletion directly. Give one correct rollback design and one correct offline approach for a sequence containing connectivity queries and deletions.

### Exercise 5

Specify an evidence plan for a concurrent union–find over dense IDs. Include abstract semantics, sequential reference comparison, forced races, metadata/count validation, progress measurements, memory ordering/lifetime, and workload benchmarks.

## Answers to the Exercises

### Answer 1

The first four unions yield parents `[0,0,2,2,4,4,6,6]` and root sizes two. `(0,2)` makes 2 a child of 0; `(4,6)` makes 6 a child of 4; `(0,4)` makes 4 a child of 0. Before compression, parents are `[0,0,0,2,0,4,4,6]`; authoritative root size is `size[0]=8` (loser entries may remain stale by contract). The path from 7 is `7->6->4->0`, depth three. Full `find(7)` rewrites 7 and 6 to 0; 4 already points to 0, producing `[0,0,0,2,0,4,0,0]`. Nodes 3 and 5 are not on that path and need not be compressed.

### Answer 2

Fix an element `x`. Its depth increases only when the current root of its tree is attached beneath another root. Because the algorithm attaches the smaller tree beneath a tree at least as large, the newly merged component containing `x` has size at least twice its prior component. After `k` depth increases it therefore contains at least `2^k` elements. It cannot exceed `n`, so `2^k<=n` and `k<=floor(log2 n)`. Parent changes within the existing tree are absent because this variant performs no compression.

### Answer 3

Map external keys to dense elements but expose `component_info(x)`, not internal root. Each root stores member count, minimum key, and checked weight sum. A successful union finds roots, precomputes `new_min=min(...)` and a checked sum before linking, selects a winner by size/tie rule, links once, installs combined metadata, and decrements count. A redundant union returns false and changes nothing. If key comparison or sum fails, the private/prepared combine fails before structural publication, leaving the forest unchanged. Overflow is an explicit error or domain-specific wider/saturating policy, never accidental wrap. Validation walks all elements, recomputes canonical groups, minima, sums, root sizes, and component count, and ignores or clears loser metadata.

### Answer 4

Compression rewrites an unbounded number of parents during a query, so logging only union links cannot restore an earlier topology. Ordinary DSU also stores only the transitive merged partition; it lacks the bridge/witness structure needed to split after deleting a relation. A rollback design uses union by size without compression and logs losing root, winning root, previous winner metadata, and component count (plus no-op markers if required); snapshots are history lengths. For offline deletions, process operations backward when feasible so a forward deletion becomes a reverse addition, or place each edge on a segment tree covering its active time interval and traverse it with rollback DSU, answering queries at leaves.

### Answer 5

Define linearizable `find/same/union` or a precise weaker batch contract, representative nondurability, and metadata/count semantics. Generate histories and compare completed operations with a sequential reference/linearizability checker; after quiescence validate parent bounds, no cycles, root termination, canonical partition, root sizes, and component count. Force opposing equal-rank unions, union versus compression, repeated redundant unions, hot-root metadata updates, delayed/stalled threads, and CAS failure/retry. Use race and memory sanitizers where available and document atomic memory orders plus object/mapping lifetime. Measure latency distributions, throughput scaling, parent reads/writes, retries, false sharing, component skew, union/find ratios, successful/redundant rates, and adversarial schedules on pinned hardware. Separate algorithmic correctness from performance and reclamation evidence.
