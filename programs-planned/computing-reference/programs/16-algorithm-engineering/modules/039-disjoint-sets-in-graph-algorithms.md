---
module_id: ALGE-039
program: Algorithm Engineering
level: 1
module_number: 39
title: Disjoint Sets in Graph Algorithms
status: complete
last_verified: 2026-09-05
---

# Disjoint Sets in Graph Algorithms

## One-Page Review

### Governing question

How can a graph algorithm maintain a changing partition under edge insertions, answer whether two vertices are already connected, and preserve correctness, near-linear aggregate cost, deterministic evidence, and explicit limits on deletion and concurrency?

### Essential definitions

- A **partition** divides a universe into nonempty, pairwise-disjoint blocks whose union is the universe.
- `make_set(x)` creates singleton block $\{x\}$.
- `find(x)` returns a representative of the block containing $x$.
- `union(x,y)` merges two distinct blocks and reports whether a merge occurred.
- A **disjoint-set forest** represents each block as a rooted parent tree.
- **Union by size** attaches the smaller root below the larger root.
- **Union by rank** attaches the lower-rank root below the higher-rank root and increments only an equal-rank winner.
- **Path compression** redirects vertices visited by `find` toward the root.
- A **representative** is an internal identity, not necessarily a semantic minimum or permanent leader.
- $\alpha(n)$ denotes an inverse-Ackermann growth function in common amortized bounds.

### Central model, mechanism, or theorem

Initially each vertex is its own root. `find` follows parents until `parent[r]=r`. `union` first finds both roots; if equal, the proposed edge lies within an existing component. Otherwise it attaches one root to the other and decreases the component count.

Union by size or rank prevents tall trees; path compression flattens the searched paths without changing block membership. Under the standard pointer-machine/RAM analysis, their combination supports a sequence of operations in nearly linear total time, commonly summarized as $O((m+n)\alpha(n))$ for $m$ operations on $n$ elements. This is an amortized sequence bound, not proof that every operation takes a fixed constant number of steps.

In an undirected incremental graph, DSU blocks equal connected components of the edges accepted so far. An edge $(u,v)$ creates a cycle exactly when `find(u)==find(v)` before insertion. Kruskal uses the same test to preserve a forest while scanning edges by weight.

### Critical invariants

- The element universe and stable identity mapping are fixed unless explicit insertion is supported.
- Every parent index is valid; following parents terminates at a self-parent root.
- Two elements are in the same abstract block exactly when their roots are equal.
- Only roots are linked during `union`; linking arbitrary input vertices can split or misrepresent blocks.
- Root size equals block cardinality under union-by-size; nonroot sizes are ignored.
- Rank never decreases and is only a structural upper-bound certificate, not necessarily current height after compression.
- Path compression changes representation but not the represented partition.
- A successful union reduces the component count by one; a redundant union changes no abstract block.
- For incremental undirected connectivity, DSU blocks match graph connected components after each processed edge.
- Result evidence is bound to vertex and edge identities, order policy, and one input snapshot.

### Common failures

Frequent failures include omitting isolated vertices; accepting unknown identities; linking nonroots; using stale roots after another union; decrementing component count on a redundant edge; changing size on a rejected merge; confusing representative identity with a stable canonical label; recursively overflowing on an adversarial chain; corrupting parents during partial compression; applying ordinary DSU to directed reachability; pretending it supports deletion; sharing mutable arrays without synchronization; and quoting $\alpha(n)$ as a per-operation worst-case constant without assumptions.

### Compact example

Start with $\{a\},\{b\},\{c\},\{d\}$. Insert $ab$, merging to $\{a,b\}$; insert $cd$, giving $\{c,d\}$; insert $bc$, merging all four. Before inserting $ad$, both endpoints have the same root, so $ad$ closes a cycle and is rejected by a forest-building algorithm.

### Connections

[ALGE-031](./031-breadth-first-search.md) computes components by traversal, while [ALGE-035](./035-minimum-spanning-trees.md) uses disjoint sets in Kruskal. [ALGE-034](./034-strongly-connected-components.md) shows why directed mutual reachability requires different machinery. [ALGE-040](../ROADMAP.md#block-04--graph-algorithms) next compares graph representation and traversal engineering.

## Governing Question

Given a stable vertex universe and a stream or ordering of undirected edges, how should an implementation maintain component membership, expose cycle/merge decisions, and supply evidence that its parent forest still represents exactly the graph partition intended by the calling algorithm?

DSU answers a deliberately narrow question: equivalence under merges. It does not store graph paths, directions, edge weights, deletion history, or why two vertices became connected unless the caller records that evidence. Its speed comes from this restricted interface.

## Why This Matters

Disjoint sets support Kruskal MST construction, incremental connectivity, undirected cycle detection, connected-component labeling, image segmentation, percolation experiments, clustering, unification-like grouping, and offline algorithms. The same three operations appear inside many larger proofs.

The data structure is a good example of separating abstraction from representation. The abstract state is a partition. Parent pointers, ranks, sizes, and compression are implementation choices. A representative may change after a merge even though block membership remains stable. APIs that leak the root as a permanent business identifier turn a harmless optimization into externally visible breakage.

Performance claims also require precision. Union-by-size alone gives logarithmic tree height. Compression alone can behave differently. Their combined inverse-Ackermann analysis is amortized over a sequence and depends on a conventional machine and operation model. Real costs include identity lookup, cache misses, allocation, synchronization, input parsing, and graph-edge sorting.

## Prerequisites and Retrieval

Retrieve equivalence relations and partitions; rooted trees and forests; undirected paths, connectivity, cycles, and spanning forests; arrays, maps, recursion and iteration; logarithms and amortized analysis; stable identity and snapshot concepts; [ALGE-031](./031-breadth-first-search.md) for traversal connectivity and [ALGE-035](./035-minimum-spanning-trees.md) for Kruskal's use of DSU.

## Learning Objectives

After completing this module, you should be able to:

1. specify the disjoint-set abstract partition independently of its parent representation;
2. implement `make_set`, `find`, and `union` with explicit failure behavior;
3. prove parent-forest validity and partition preservation;
4. prove logarithmic height for union by size or rank without compression;
5. explain, without overstating, the amortized inverse-Ackermann result;
6. derive incremental undirected connectivity and cycle detection;
7. use DSU correctly inside Kruskal and component labeling;
8. validate parents, roots, sizes, component counts, and graph correspondence;
9. handle stable identities, determinism, snapshots, serialization, cancellation, and concurrency;
10. recognize directed, deletion, rollback, fully dynamic, and path-witness boundaries.

## Core Exposition

### Define the abstract partition

Let universe $U$ contain $n$ stable elements. A partition $\mathcal P$ is a set of blocks such that every element belongs to exactly one block. `find(x)` may return any representative identifying $x$'s current block, subject only to equality consistency:

$$
\operatorname{find}(x)=\operatorname{find}(y)
\quad\Longleftrightarrow\quad
x\text{ and }y\text{ occupy the same block}.
$$

`union(x,y)` replaces their two blocks by their union when distinct. It never splits blocks. Decide whether repeated insertion is an idempotent success or a `False`/already-connected result. Reject unknown elements rather than silently creating them unless dynamic insertion is part of the contract.

### Represent blocks as rooted forests

Store `parent[x]`. A root points to itself; every nonroot points to another element in its block. `find` follows this functional graph to a root. Correctness requires no directed parent cycle except a root self-loop.

Naive union can attach a large tree below a singleton repeatedly, creating height $n-1$. `find` then becomes linear. Union by size attaches the smaller root below the larger. If a vertex's depth increases because its root was attached, the containing block at least doubles. A block can double at most $\lfloor\log_2 n\rfloor$ times, so height is logarithmic without compression.

Union by rank uses an upper-bound proxy. Ranks differ: attach lower below higher without changing the winner. Ranks equal: choose one winner and increment its rank. A rank-$r$ root represents at least $2^r$ elements, so rank is at most $\lfloor\log_2 n\rfloor$.

### Compress paths without changing meaning

Full path compression first finds root $r$, then redirects each parent on the searched path to $r$. Path halving redirects every other vertex toward its grandparent during traversal; path splitting redirects every visited vertex to its grandparent. They have different write patterns but preserve the same block because every new parent is an ancestor in the same tree.

Compression invalidates interpretations of rank as exact current height. Rank remains useful for union decisions and analysis but should not be recomputed casually. Compression also writes during `find`, so a nominally read-only query is mutating and needs synchronization in shared implementations.

### Implement a deterministic, validated DSU

The implementation below uses stable comparable vertex names, union by size, iterative full compression, explicit redundant-union results, and an independent graph-partition check.

<!-- bijux-verify: {"id":"deterministic-disjoint-sets","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"accepted=('ab', 'cd', 'bc')\nrejected=('ad', 'ee')\ncomponents=(('a', 'b', 'c', 'd'), ('e',))\ncomponent_count=2\nvalid=True\n","stderr":""}} -->
```python
class DisjointSets:
    def __init__(self, elements):
        elements = tuple(sorted(elements))
        if len(elements) != len(set(elements)):
            raise ValueError("duplicate element")
        self.parent = {x: x for x in elements}
        self.size = {x: 1 for x in elements}
        self.component_count = len(elements)

    def find(self, element):
        if element not in self.parent:
            raise KeyError(element)
        root = element
        seen = set()
        while self.parent[root] != root:
            if root in seen:
                raise ValueError("parent cycle")
            seen.add(root)
            root = self.parent[root]
        while self.parent[element] != element:
            next_element = self.parent[element]
            self.parent[element] = root
            element = next_element
        return root

    def union(self, left, right):
        left_root = self.find(left)
        right_root = self.find(right)
        if left_root == right_root:
            return False
        if (self.size[left_root], left_root) < (self.size[right_root], right_root):
            left_root, right_root = right_root, left_root
        self.parent[right_root] = left_root
        self.size[left_root] += self.size[right_root]
        self.component_count -= 1
        return True

    def components(self):
        groups = {}
        for element in sorted(self.parent):
            groups.setdefault(self.find(element), []).append(element)
        return tuple(sorted(tuple(group) for group in groups.values()))


def validate(dsu, vertices, edges):
    vertices = set(vertices)
    if set(dsu.parent) != vertices:
        return False
    roots = []
    for vertex in vertices:
        root = dsu.find(vertex)
        roots.append(root)
        if dsu.parent[root] != root:
            return False
    groups = dsu.components()
    if len(groups) != dsu.component_count:
        return False
    if any(dsu.size[group[0] if dsu.parent[group[0]] == group[0]
                            else dsu.find(group[0])] != len(group)
           for group in groups):
        return False

    adjacency = {vertex: [] for vertex in vertices}
    for _, left, right in edges:
        if left not in vertices or right not in vertices:
            return False
        adjacency[left].append(right)
        adjacency[right].append(left)
    unseen = set(vertices)
    graph_groups = []
    while unseen:
        start = min(unseen)
        reached = {start}
        stack = [start]
        while stack:
            vertex = stack.pop()
            for neighbor in adjacency[vertex]:
                if neighbor not in reached:
                    reached.add(neighbor)
                    stack.append(neighbor)
        unseen -= reached
        graph_groups.append(tuple(sorted(reached)))
    return groups == tuple(sorted(graph_groups)) and len(set(roots)) == len(groups)


vertices = {"a", "b", "c", "d", "e"}
edges = (("ab", "a", "b"), ("cd", "c", "d"),
         ("bc", "b", "c"), ("ad", "a", "d"),
         ("ee", "e", "e"))
dsu = DisjointSets(vertices)
accepted, rejected = [], []
for edge_id, left, right in edges:
    (accepted if dsu.union(left, right) else rejected).append(edge_id)
print(f"accepted={tuple(accepted)}")
print(f"rejected={tuple(rejected)}")
print(f"components={dsu.components()}")
print(f"component_count={dsu.component_count}")
print(f"valid={validate(dsu, vertices, edges)}")
```

The stable tie rule chooses the lexicographically larger root when equal sizes because of the tuple comparison and swap; another declared rule would be equally correct. Neither root should escape as a permanent domain identifier.

### Prove graph-component correspondence

For an undirected edge prefix $E_k$, maintain that two vertices share a DSU block exactly when a path between them uses edges in $E_k$. Initially, only zero-edge self paths exist, matching singleton blocks.

For new edge $(u,v)$, if roots differ, merging their blocks represents every path formed by a path to $u$, the new edge, and a path from $v$. No vertices outside those components become connected. If roots match, an earlier path already joins $u$ and $v$; the edge changes no connectivity. Induction proves the invariant.

This also proves cycle detection for a forest-building scan. Different roots mean adding the edge connects two trees and cannot form a cycle. Equal roots mean an existing path plus the new edge forms a cycle (including a self-loop under the chosen graph definition).

### Use DSU in Kruskal without losing evidence

Sort stable logical undirected edges by `(weight, tie_key)`. For each edge, query both roots before union. Accept and union only when distinct. The DSU graph invariant proves accepted edges remain a forest; the MST cut property proves the weight-ordered crossing edge is safe.

DSU does not prove edge order or MST optimality by itself. A Kruskal certificate needs input-edge provenance, ordering evidence, accepted/rejected decisions, spanning status, checked total weight, and cut/optimality validation. Isolated vertices must be created before edges are scanned.

### State the amortized result honestly

Tarjan's classical analysis shows that rank/size discipline combined with path compression supports intermixed operations in inverse-Ackermann amortized time under a specified model. Common texts simplify the sequence bound to $O((m+n)\alpha(n))$. Exact parameterizations differ across analyses, so state which theorem and operation model is used.

Amortized means an expensive `find` can be paid for by many cheap operations across the sequence. It does not supply a strict real-time latency bound for each call. For hard per-operation deadlines, use a representation and bound suited to that requirement, perhaps union by rank without compression for logarithmic worst-case depth.

### Validate representation and semantics

A representation validator checks the element universe, parent range, termination at self roots, absence of nonroot cycles, component count, root size totals, nonnegative/legal ranks, and optional serialization checksum. A semantic validator builds components independently with BFS/DFS over the processed undirected edges and compares partitions without comparing representative names.

For small universes, compare every pair: root equality must equal independent reachability. Metamorphic properties include edge-order permutation preserving final components, duplicate edges preserving the partition, vertex renaming preserving mapped blocks, self-loops changing nothing, and adding an isolated vertex adding exactly one block.

### Respect deletions, rollback, direction, and concurrency

Ordinary DSU is monotone: blocks merge and never split. Deleting a bridge may divide a component, which parent forests cannot discover. Fully dynamic connectivity needs different data structures. Offline deletion workloads can reverse time and turn deletions into insertions; rollback DSU can undo a stack-disciplined history, usually avoiding ordinary path compression because its many writes complicate rollback.

DSU represents undirected connectivity or another explicit equivalence relation. Directed reachability is not symmetric and strongly connected components do not generally remain correct under the same simple operations.

Concurrent `find` compression and `union` writes can race, lose size updates, create parent cycles, or expose linearization ambiguity. Use a proved concurrent algorithm or external synchronization. Pin the identity map and operation log; checkpoints record parent, size/rank, component count, processed-edge position, algorithm version, and input digest. Cancellation returns an incomplete prefix result unless that prefix is itself the promised product.

Current [Princeton Algorithms union-find material](https://algs4.cs.princeton.edu/15uf/) demonstrates weighted quick union and compression and describes the inverse-Ackermann practical bound. The durable claims here remain tied to Tarjan's theorem and the stated model rather than a particular teaching implementation.

## Definitions and Notation

- $U$: fixed element universe; $n=|U|$.
- $\mathcal P$: abstract partition of $U$.
- `parent[x]`: forest parent of element $x$.
- **root:** element $r$ satisfying `parent[r]=r`.
- **representative:** returned root identity for a block.
- **size:** root metadata equal to current block cardinality.
- **rank:** monotone structural upper-bound metadata used for union choice.
- **compression:** parent rewrites along a `find` path toward its root.
- **successful union:** merge of two previously distinct blocks.
- **redundant union:** request whose elements already share a block.
- $\alpha$: inverse-Ackermann function under the cited amortized analysis.

## Mechanisms, Invariants, or Proof Structure

Initialization creates one valid rooted tree per singleton. `find` terminates by parent-forest acyclicity and returns the block root. Compression preserves ancestry within the same block. Union links roots only, so it merges exactly two trees without a cycle. Size/rank discipline bounds structural growth; compression yields the stronger aggregate analysis. Induction over the processed undirected edge prefix proves DSU blocks equal graph components. A same-root edge closes a cycle; a different-root edge joins two components.

## Alternatives and Trade-Offs

- **Quick find:** constant representative lookup but linear block relabeling on merge.
- **Naive quick union:** cheap link but can create linear-height trees.
- **Union by size/rank:** logarithmic height without compression and simple metadata.
- **Path compression variants:** excellent aggregate performance with different write/cache behavior.
- **BFS/DFS:** reconstructs paths and handles a static snapshot directly, but repeated incremental queries can be expensive.
- **Rollback DSU:** supports stack-disciplined undo with additional history and restricted compression.
- **Fully dynamic connectivity:** supports deletions but is substantially more complex.
- **Concurrent DSU:** needs explicit memory-model and linearizability proofs.

## Failure Modes and Misconceptions

- A root is not a durable semantic leader or smallest member unless explicitly maintained.
- Path compression does not change the abstract partition.
- Rank after compression is not exact tree height.
- Union must link roots, not arbitrary requested elements.
- Redundant union must not decrement component count or add sizes.
- DSU answers connectivity but does not return a graph path.
- Ordinary DSU does not support arbitrary deletion or directed reachability.
- Near-constant amortized cost is not constant worst-case latency.
- Final component equality does not validate every intermediate cycle decision.
- A thread-safe map around unsafe parent rewrites is not automatically a correct concurrent DSU.

## Worked Examples

### Example 1

**Situation.** Merge $a,b$, then $c,d$, then $b,c$. The blocks progress from four singletons to $\{a,b\}$, $\{c,d\}$, then $\{a,b,c,d\}$. **Conclusion.** Union depends on roots, not the surface arguments.

### Example 2

**Situation.** Repeated naive unions attach the existing root under a new singleton. After $n-1$ steps, the first element can have depth $n-1$. **Conclusion.** Correct partition semantics alone do not guarantee acceptable performance.

### Example 3

**Situation.** Under union by size, element depth increases only when its whole tree attaches to an equal-or-larger tree. Its containing size at least doubles, limiting increases to $\lfloor\log_2 n\rfloor$. **Conclusion.** The height bound follows from a doubling argument.

### Example 4

**Situation.** Parent chain $a\to b\to c\to d\to d$ is searched from $a$. Full compression changes parents of $a,b,c$ to $d$ while all still represent the same block. **Conclusion.** Compression changes witnesses, not membership.

### Example 5

**Situation.** Forest edges already connect $u$ to $v$. A proposed edge $(u,v)$ sees equal roots; the existing path plus the new edge forms a cycle. **Conclusion.** Same-root testing is correct for undirected incremental cycle detection.

### Example 6

**Situation.** Vertex $z$ has no incident edge. If it is omitted from initialization, a component audit reports too few blocks. **Conclusion.** The vertex universe cannot be inferred only from edge endpoints.

### Example 7

**Situation.** Two equal-size roots use different tie rules on two hosts. Both partitions are correct, but root IDs differ. Comparing serialized parents byte-for-byte produces a false mismatch. **Conclusion.** Validate blocks extensionally or declare deterministic ties.

### Example 8

**Situation.** Delete the only edge between two subtrees in a previously connected graph. DSU still has one merged block and cannot split it. **Conclusion.** Monotone union state cannot answer general deletion workloads.

### Example 9

**Situation.** Two threads simultaneously attach roots $a$ and $b$ in opposite directions. Without coordination they can create $a\to b\to a$. **Conclusion.** Concurrent union needs a proved linearization and atomic parent protocol.

### Example 10

**Situation.** Kruskal sees equal-weight parallel edges after two endpoints are already connected. DSU rejects both for the current forest, but the MST proof also needs their stable weights and order evidence. **Conclusion.** DSU certifies component decisions, not the whole optimization theorem.

## Cross-Program Connections

- Data Structures Engineering owns the general DSU representation and amortized analysis; Algorithm Engineering owns its graph-algorithm contracts and certificates.
- Operating Systems and Concurrent Programming own memory ordering, atomic updates, locking, and linearizability.
- Database and Data Engineering own identity maps, operation logs, snapshots, checkpoints, and incremental pipelines.
- Network Engineering distinguishes undirected connectivity from directed routing and policy.
- Security Engineering reviews hostile element IDs, bounds, corrupted parent arrays, and denial-of-service sequences.
- Software Architecture owns whether representatives may cross service boundaries as durable identities.

## References

1. Robert Endre Tarjan, “Efficiency of a Good But Not Linear Set Union Algorithm,” *Journal of the ACM* 22(2), 215–225, 1975, DOI [10.1145/321879.321884](https://doi.org/10.1145/321879.321884). Primary source checked 2026-09-05.
2. Harold N. Gabow and Robert Endre Tarjan, “A Linear-Time Algorithm for a Special Case of Disjoint Set Union,” *Journal of Computer and System Sciences* 30(2), 209–221, 1985, DOI [10.1016/0022-0000(85)90014-5](https://doi.org/10.1016/0022-0000(85)90014-5). Primary source checked 2026-09-05.
3. Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein, *Introduction to Algorithms*, 4th ed., MIT Press, 2022, Chapter 19. [Official publisher record](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/), checked 2026-09-05.
4. Robert Sedgewick and Kevin Wayne, *Algorithms*, 4th ed., Addison-Wesley, 2011, §1.5. [Author-maintained union-find material](https://algs4.cs.princeton.edu/15uf/), checked 2026-09-05.
5. Jon Kleinberg and Éva Tardos, *Algorithm Design*, Pearson, 2005, clustering and MST applications. [Official publisher record](https://www.pearson.com/en-us/subject-catalog/p/algorithm-design/P200000003259), checked 2026-09-05.

## Exercises

### Exercise 1

Starting from eight singletons, apply union by size to $(0,1),(2,3),(4,5),(6,7),(1,3),(5,7),(3,7)$, breaking equal-size ties toward the smaller root. Show parent roots, root sizes, and component count after each merge.

### Exercise 2

Prove that union by size without compression gives height at most $\lfloor\log_2 n\rfloor$ and that full path compression preserves the represented partition.

### Exercise 3

Diagnose a DSU that links `parent[x]=y` without finding roots, decrements count on every union request, exposes roots as customer IDs, recursively finds without validation, and is shared unsafely by threads.

### Exercise 4

Choose DSU, traversal, rollback DSU, or a fully dynamic connectivity structure for: a static one-query graph, an insertion-only million-query stream, an offline add/delete timeline, and an online arbitrary-deletion service.

### Exercise 5

Design a resumable Kruskal edge-processing service for untrusted graph uploads. Specify DSU invariants, stable identities, checkpoints, validation, cancellation, and the evidence needed beyond DSU to claim an MST or MSF.

## Answers to the Exercises

### Answer 1

After $(0,1)$ root 0 has size 2; after $(2,3)$ root 2 has size 2; after $(4,5)$ root 4 has size 2; after $(6,7)$ root 6 has size 2. Counts descend from eight to four. Merge $(1,3)$ finds roots 0 and 2; the tie chooses 0, whose size becomes 4, count three. Merge $(5,7)$ chooses root 4 over 6, size 4, count two. Merge $(3,7)$ finds roots 0 and 4; tie chooses 0, size 8, count one. Nonroot size fields are ignored. Parent chains may be compressed during the finds, but every element's final root is 0.

### Answer 2

When an element's depth increases under union by size, the root of its tree was attached beneath a root whose tree was at least as large. Its new component size is at least twice its old size. Starting from one and never exceeding $n$, depth can increase at most $\lfloor\log_2 n\rfloor$ times.

For compression, let searched chain be $x=x_0,x_1,\ldots,x_k=r$. Every $x_i$ already belongs to root $r$'s block. Replacing any `parent[x_i]` by $r$ retains a valid path to the same root and changes no relation `find(a)==find(b)`. No edge points outside the block, so the abstract partition is preserved.

### Answer 3

Linking arbitrary $x$ to $y$ can detach or misrepresent a subtree; find both roots and link only distinct roots. Decrement count and update size/rank only after a successful distinct-root merge. A representative can change, so return stable customer identity separately and keep roots internal.

Iterative find avoids stack exhaustion; validate element membership, parent range, and cycles when consuming untrusted or restored state. Concurrent compression and union require a proved concurrent algorithm or external serialization—ordinary map safety is insufficient. Add snapshot/version binding and compare partitions rather than root names.

### Answer 4

For one static connectivity query, BFS/DFS is simplest and returns a path if needed. For an insertion-only stream with many queries, DSU matches monotone equivalence updates. For an offline add/delete timeline, segment-tree-over-time plus rollback DSU or reverse processing may convert active intervals into stack-disciplined unions. Avoid ordinary compression unless rollback records every write.

For an online service with arbitrary deletions and interleaved queries, use a fully dynamic connectivity structure or recompute according to scale and latency; ordinary DSU cannot split a block. State whether multiedges and self-loops affect deletion counts.

### Answer 5

Parse a complete stable vertex universe and logical undirected edges into an immutable digest. Validate quotas, endpoints, unique edge IDs, weights, units, NaN/overflow policy, and deterministic `(weight,tie_key)` order. Initialize every vertex, including isolates. At each edge, find both roots; if distinct, record the decision and union roots by size/rank. Checkpoint the input digest, sorted-stream position, parent and size/rank arrays, component count, accepted edge IDs, checked total, algorithm version, and cancellation state.

On resume, validate digest, parent forest, root metadata, accepted-edge count, and replay boundary. Cancellation returns incomplete rather than an MST. At completion, independently verify edge provenance, forest acyclicity, per-component coverage, selected count, total arithmetic, and DSU/BFS component agreement. DSU evidence alone does not prove sorted order or optimality; add Kruskal cut/order evidence or an independent MST certificate. Publish MST versus MSF status, stable selected edges, components, total, graph revision, tie policy, and validation outcome atomically.
