---
module_id: ALGE-035
program: Algorithm Engineering
level: 1
module_number: 35
title: Minimum Spanning Trees
status: complete
last_verified: 2026-09-05
---

# Minimum Spanning Trees

## One-Page Review

### Governing question

How can we connect every vertex of a weighted undirected graph at minimum total edge weight, prove each greedy choice safe, and distinguish the mathematical optimum from representation, numeric, tie, and domain-modeling policy?

### Essential definitions

- A **spanning tree** is a connected, acyclic subgraph containing every vertex.
- A **minimum spanning tree** (MST) minimizes the sum of selected edge weights among all spanning trees.
- A **minimum spanning forest** (MSF) contains one MST for every connected component of a disconnected graph.
- A **cut** $(S,V\setminus S)$ partitions the vertices; an edge **crosses** it when its endpoints lie on opposite sides.
- A cut **respects** a forest $A$ when no edge of $A$ crosses the cut.
- A **light edge** is a minimum-weight edge crossing a specified cut.
- The **cut property** makes a light crossing edge safe for some MST extending a respected forest.
- The **cycle property** excludes a strictly heaviest edge on a cycle from every MST.
- **Kruskal's algorithm** scans edges by nondecreasing weight and joins different forest components.
- **Prim's algorithm** grows one tree by repeatedly selecting a light edge leaving the current tree.
- **Borůvka's algorithm** lets every current component select a light outgoing edge and contracts the resulting forest.
- A **certificate** binds the selected edges, total weight, component coverage, graph snapshot, and optimality evidence.

### Central model, mechanism, or theorem

Let $G=(V,E,w)$ be a finite connected undirected graph. If forest $A$ is contained in some MST, a cut respects $A$, and edge $e$ has minimum weight among edges crossing the cut, then $A\cup\{e\}$ is contained in some MST.

Take an MST $T$ containing $A$. If $e\in T$, it is already safe. Otherwise adding $e$ creates one cycle. That cycle crosses the cut again at edge $f$. Because the cut respects $A$, $f\notin A$, and because $e$ is light, $w(e)\le w(f)$. Replacing $f$ by $e$ yields a spanning tree no heavier than $T$, hence another MST containing $A\cup\{e\}$.

This exchange proof supports Kruskal, Prim, and Borůvka under different respected cuts. With comparison sorting and disjoint sets, Kruskal takes $O(m\log m)$ time; with adjacency lists and a binary heap, Prim takes $O(m\log n)$ time. Both use $O(n+m)$ stored graph data and linear auxiliary structures, subject to implementation details.

### Critical invariants

- The vertex universe, logical undirected edge identity, endpoint policy, weight domain, and graph snapshot are fixed.
- Every retained edge has two declared endpoints and one comparable, finite weight under a total ordering policy.
- The selected set is always a forest; adding an edge joins two previously separate forest components.
- Each greedy edge is light for a cut that respects the current selected forest.
- Kruskal processes logical edges in nondecreasing deterministic order and disjoint-set representatives match current forest components.
- Prim's key for an outside vertex is the lightest known edge from the tree, and stale heap entries never become selected edges.
- Borůvka choices are interpreted as a set of safe component-crossing edges, with duplicate selections coalesced.
- A connected $n$-vertex success contains exactly $n-1$ selected edges and reaches every vertex.
- A disconnected input returns an explicit MSF or a disconnected error according to contract; it is never mislabeled an MST.
- Total-weight accumulation has declared exactness, overflow, NaN, infinity, and unit semantics.
- Tie-breaking changes which optimum may be returned, not the minimum total, when comparisons are sound.
- Publication follows independent tree/forest and optimality validation.

### Common failures

Frequent failures include treating directed arcs as undirected without authorization; omitting isolated vertices; confusing an MST with a shortest-path tree; selecting the globally lightest incident edge without a safe-cut argument; adding a cycle edge; using stale Prim heap keys; stopping Kruskal after $n-1$ scanned rather than selected edges; reporting a tree on a disconnected graph; assuming equal weights imply multiple MSTs or distinct weights are necessary for uniqueness; using NaN in an ordinary comparison sort; overflowing an integer total; mixing units; coalescing parallel edges before retaining the lightest logical alternative; relying on unstable component or edge identities; and claiming minimum construction cost when the domain actually permits Steiner points, capacities, redundancy, directions, or nonlinear costs.

### Compact example

For triangle edges $ab=1$, $bc=2$, and $ac=4$, the cut $\{a\}\mid\{b,c\}$ makes $ab$ safe. After selecting $ab$, cut $\{a,b\}\mid\{c\}$ makes $bc$ safe. The result $\{ab,bc\}$ has weight $3$. Adding $ac$ would create a cycle whose strictly heaviest edge is $ac$, so no MST uses it.

### Connections

[ALGE-002](./002-preconditions-postconditions-and-correctness.md) supplies contract reasoning, [ALGE-003](./003-loop-invariants-for-algorithm-correctness.md) supplies invariant proofs, [ALGE-022](./022-greedy-choice-and-exchange-arguments.md) supplies exchange arguments, [ALGE-031](./031-breadth-first-search.md) supplies connectivity traversal, and [ALGE-034](./034-strongly-connected-components.md) contrasts directed mutual reachability with undirected connectivity. [ALGE-036](../ROADMAP.md#block-04--graph-algorithms) next develops shortest paths, which optimize distances from a source rather than total connecting weight.

## Governing Question

Given a finite weighted undirected graph, how should an implementation produce a spanning tree of provably minimum total weight—or a minimum spanning forest or explicit failure for disconnected input—while preserving edge identity, deterministic ties, numeric validity, and the limits of the model?

The phrase “connect everything as cheaply as possible” hides several contracts. Are edges undirected? Are parallel alternatives distinct? Is every vertex mandatory? Are weights exact integers, decimal money, floating estimates, or ordered tuples? Must the result be one tree or a forest? Does the domain require redundancy or capacity? The MST theorem answers only after those choices define $G=(V,E,w)$.

The essential algorithmic idea is not “take cheap edges.” Greedy choices are correct because each chosen edge is light across a cut that respects the partial forest. The exchange proof shows how to transform an optimum so it contains that choice without raising cost. Kruskal, Prim, and Borůvka are different mechanisms for repeatedly exposing such cuts.

An implementation should return more than edge names. It needs connectivity status, total weight under a declared arithmetic policy, stable edge identities, tie policy, graph revision, and evidence that the result is a forest spanning the intended vertices. High-risk uses also need an optimality certificate or an independently implemented checker.

## Why This Matters

MSTs are foundational in network design, clustering, image segmentation, approximation, geometric processing, broadcast backbones, taxonomy construction, and as subroutines in more advanced algorithms. They are also a model-selection lesson: minimizing the total of existing undirected links is not the same as minimizing routes from a source, supporting traffic, surviving failures, or designing new junctions.

The cut and cycle properties generalize beyond one named algorithm. They let reviewers justify a selected edge, reject an impossible edge, verify an output, analyze sensitivity, and understand why tie choices can differ while total weight remains optimal.

Engineering details matter even for linear-sized output. Kruskal may sort billions of edge records. Prim may push several stale keys per vertex. Parallel edges need stable identity. Floating weights may include NaN or values whose displayed decimal differs from their binary sum. A disconnected graph has no spanning tree but does have a well-defined MSF. Correctness must cover these states explicitly.

Classic algorithms remain current. Boost.Graph 1.92.0 documents generic Kruskal and Prim implementations with property-map and graph-concept requirements. Such library behavior is version-sensitive; the cut theorem, exchange proof, and $n-1$ tree invariant are durable.

## Prerequisites and Retrieval

Retrieve:

- finite undirected graphs, vertices, logical edges, endpoints, paths, cycles, connected components, trees, and forests;
- edge weights, total orders, sums, exact and floating arithmetic, overflow, NaN, infinity, and physical units;
- cuts, crossing edges, set partitions, equivalence relations, and proof by exchange;
- sorting, priority queues, binary heaps, disjoint-set union, path compression, union by rank or size, and adjacency lists;
- loop invariants, induction, asymptotic work, auxiliary space, and lower-bound awareness;
- stable identities, immutable snapshots, duplicate records, external sorting, cancellation, checkpoints, and atomic publication;
- traversal-based connectivity validation, component labels, and independent certificates;
- property, differential, metamorphic, exhaustive, adversarial, and fault-injection testing.

You should be able to prove that a finite undirected graph is a tree exactly when it is connected and has $n-1$ edges, or equivalently when it is acyclic and has $n-1$ edges.

## Learning Objectives

After completing this module, you should be able to:

1. specify MST and MSF contracts over a precise weighted undirected multigraph or normalized simple graph;
2. prove the cut property through an exchange argument and derive the cycle property;
3. derive Kruskal, Prim, and Borůvka as applications of safe cuts;
4. prove forest preservation, spanning completion, and optimality for the classic algorithms;
5. implement deterministic Kruskal with disjoint sets and a bounded independent validator;
6. analyze sorting, heap, disjoint-set, adjacency, output, and external-memory costs;
7. reason correctly about equal weights, uniqueness, negative weights, self-loops, and parallel edges;
8. govern integer overflow, floating exceptional values, unit normalization, and stable tie keys;
9. validate coverage, acyclicity, connectivity, total weight, edge provenance, and optimality evidence;
10. recognize when shortest paths, Steiner trees, arborescences, survivable networks, or constrained design—not MST—is the real problem.

## Core Exposition

### Specify the weighted undirected input

Declare the complete vertex set separately from edges so isolated vertices remain visible. Give every logical edge a stable identity, two endpoints, and a weight. In a multigraph, two edges with the same endpoints can remain distinct alternatives. A self-loop can never help span another vertex and is rejected by forest selection, but retaining it may matter for provenance and validation.

Define the weight domain:

- exact signed integers with a checked total width;
- fixed-scale decimals for money;
- rationals or symbolic ordered values;
- finite IEEE floating values after rejecting NaN and declaring infinity policy;
- lexicographic tuples such as `(cost, risk, edge_id)` when the objective truly is lexicographic.

Tie keys used for deterministic output are not necessarily part of the optimization objective. Sorting by `(weight, stable_edge_id)` selects one repeatable MST among weight-optimal alternatives. It does not claim that edge ID has domain value.

Decide whether disconnected input returns an MSF, returns partial diagnostic data with failure, or is rejected before optimization. State whether every connected component, including an isolated vertex with an empty tree, appears in the forest result.

### Define spanning trees and minimum weight

A spanning subgraph uses all vertices. A tree is connected and acyclic. Therefore a spanning tree $T$ satisfies

$$
V(T)=V,\qquad |E(T)|=|V|-1,
$$

and connects every vertex. Its weight is

$$
w(T)=\sum_{e\in E(T)}w(e).
$$

An MST minimizes this sum over all spanning trees. Negative weights are allowed: a spanning tree still has exactly $n-1$ edges, so negative cycles cannot be repeated. For a disconnected graph, no spanning tree exists; an MSF minimizes independently within each connected component.

An MST is not generally unique. The minimum total weight is unique as a value under exact comparison, while several edge sets may attain it. Distinct edge weights are sufficient for a unique MST but not necessary. A graph can contain equal-weight edges that never compete across a relevant cut.

### Prove the cut property

Let $A$ be a forest contained in some MST. Let cut $(S,V\setminus S)$ respect $A$, meaning no selected edge crosses it. Let $e$ be a minimum-weight crossing edge.

Choose an MST $T$ containing $A$. If $e\in T$, the claim holds. Otherwise $T\cup\{e\}$ has exactly one cycle because a tree has one path between the endpoints of $e$. That cycle crosses from $S$ to its complement on $e$ and must cross back on some edge $f$. Since the cut respects $A$, $f\notin A$. Lightness gives $w(e)\le w(f)$.

Set

$$
T'=T-\{f\}+\{e\}.
$$

Removing a cycle edge restores a spanning tree, $T'$ still contains $A\cup\{e\}$, and

$$
w(T')=w(T)-w(f)+w(e)\le w(T).
$$

Because $T$ is minimum, equality must hold and $T'$ is an MST. Thus $e$ is safe: at least one MST extends the new forest. With ties, the theorem does not say every MST contains $e$.

### Derive the cycle property

Let $e$ be strictly heavier than every other edge on a cycle. Suppose an MST $T$ contains $e$. Removing it splits $T$ across a cut. The original cycle contains another edge $f$ crossing that cut, and $w(f)<w(e)$. Then $T-e+f$ is a spanning tree with smaller weight, a contradiction. Therefore no MST contains a strictly heaviest cycle edge.

If several cycle edges tie for maximum, the conclusion weakens: at least one maximum edge can be excluded, but a particular tied edge may belong to some MST. Strictness matters.

Cut and cycle properties are dual review tools. A light cut edge has inclusion evidence; a strictly heavy cycle edge has exclusion evidence. They do not justify arbitrary collections without forest and compatibility invariants.

### Derive Kruskal's algorithm

Sort logical edges by nondecreasing weight with a stable tie policy. Begin with one singleton forest component per vertex. For each edge $e=\{u,v\}$:

- if $u$ and $v$ are already in the same forest component, skip $e$ because it would create a cycle;
- otherwise select $e$ and merge the two components.

Before selecting $e$, take $S$ as the current tree containing $u$. The cut between $S$ and the remaining vertices respects the forest. Any lighter crossing edge would have been processed earlier and, if it still crossed two forest components then, would have been selected. Thus $e$ is light for this cut and safe.

Disjoint-set union implements the component test. With path compression and union by rank or size, all operations cost $O(m\alpha(n))$ beyond sorting, where $\alpha$ is the inverse Ackermann function. Comparison sorting dominates at $O(m\log m)$. Preordered or bounded-integer weights can change the sorting bound, but only under their declared model.

### Implement deterministic Kruskal and bounded verification

The following implementation preserves parallel edge identities, ignores self-loops through the component test, returns explicit connectivity, checks the forest, and uses exhaustive spanning-tree enumeration only as a bounded example oracle.

<!-- bijux-verify: {"id":"deterministic-kruskal-mst","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"edges=(('ab', 'a', 'b', 1), ('cd', 'c', 'd', 1), ('ef', 'e', 'f', 1), ('bc', 'b', 'c', 2), ('de', 'd', 'e', 2))\ntotal=7 connected=True\nvalid=True\n","stderr":""}} -->
```python
from itertools import combinations


class DisjointSet:
    def __init__(self, vertices):
        self.parent = {vertex: vertex for vertex in vertices}
        self.size = {vertex: 1 for vertex in vertices}

    def find(self, vertex):
        while vertex != self.parent[vertex]:
            self.parent[vertex] = self.parent[self.parent[vertex]]
            vertex = self.parent[vertex]
        return vertex

    def union(self, left, right):
        left, right = self.find(left), self.find(right)
        if left == right:
            return False
        if self.size[left] < self.size[right]:
            left, right = right, left
        self.parent[right] = left
        self.size[left] += self.size[right]
        return True


def normalize(vertices, edges):
    vertices = set(vertices)
    normalized = []
    seen_ids = set()
    for edge_id, left, right, weight in edges:
        if edge_id in seen_ids:
            raise ValueError(f"duplicate edge identity: {edge_id}")
        if left not in vertices or right not in vertices:
            raise ValueError(f"unknown endpoint: {edge_id}")
        if not isinstance(weight, int):
            raise TypeError("this contract requires exact integer weights")
        seen_ids.add(edge_id)
        low, high = sorted((left, right))
        normalized.append((edge_id, low, high, weight))
    return vertices, tuple(normalized)


def kruskal(vertices, edges):
    vertices, edges = normalize(vertices, edges)
    sets = DisjointSet(vertices)
    selected = []
    total = 0
    for edge in sorted(edges, key=lambda e: (e[3], e[0])):
        edge_id, left, right, weight = edge
        if sets.union(left, right):
            selected.append(edge)
            total += weight
    roots = {sets.find(vertex) for vertex in vertices}
    return tuple(selected), total, len(roots) <= 1


def is_tree(vertices, edges):
    if len(edges) != max(0, len(vertices) - 1):
        return False
    sets = DisjointSet(vertices)
    for _, left, right, _ in edges:
        if not sets.union(left, right):
            return False
    return len({sets.find(vertex) for vertex in vertices}) <= 1


def validate_small_mst(vertices, all_edges, selected):
    vertices, all_edges = normalize(vertices, all_edges)
    if not is_tree(vertices, selected):
        return False
    selected_ids = {edge[0] for edge in selected}
    if not selected_ids <= {edge[0] for edge in all_edges}:
        return False
    target = sum(edge[3] for edge in selected)
    best = None
    for candidate in combinations(all_edges, max(0, len(vertices) - 1)):
        if is_tree(vertices, candidate):
            weight = sum(edge[3] for edge in candidate)
            best = weight if best is None else min(best, weight)
    return best is not None and target == best


vertices = set("abcdef")
edges = (
    ("ab", "a", "b", 1), ("ac", "a", "c", 4),
    ("bc", "b", "c", 2), ("bd", "b", "d", 5),
    ("cd", "c", "d", 1), ("ce", "c", "e", 3),
    ("de", "d", "e", 2), ("df", "d", "f", 6),
    ("ef", "e", "f", 1),
)
selected, total, connected = kruskal(vertices, edges)
print(f"edges={selected}")
print(f"total={total} connected={connected}")
print(f"valid={validate_small_mst(vertices, edges, selected)}")
```

The exhaustive verifier considers only $\binom{9}{5}=126$ candidate subsets, so it is appropriate for this fixture and inappropriate for production. A scalable checker uses structural validation plus cut/cycle or replacement-edge certificates.

The `connected` expression treats an empty graph and a singleton as connected under the algorithm's chosen convention. A product API should state its empty-graph policy explicitly.

### Derive Prim's algorithm

Choose a root $r$. Maintain tree vertex set $S$, initially $\{r\}$, and for each outside vertex the lightest known edge from $S$. Repeatedly select a minimum-key outside vertex, add its connecting edge, and relax incident edges.

The cut $(S,V\setminus S)$ respects the selected tree. The minimum key represents a light edge across that cut, so the cut property proves it safe. After selection, extend $S$ and repeat. On a connected graph, every outside set has a crossing edge until all vertices join.

An adjacency matrix with linear minimum scans gives $O(n^2)$ time and can suit dense graphs. Adjacency lists with a binary heap give $O(m\log n)$ time under a common duplicate-entry implementation. An indexed heap supports decrease-key; a simpler heap pushes new keys and discards stale entries when popped. Selecting stale entries without checking current membership and key can add cycles or nonminimum edges.

To return an MSF, restart Prim at every unvisited vertex. Do not silently call a single-root partial tree a forest.

### Derive Borůvka's algorithm

Begin with singleton forest components. In one round, each component chooses a lightest edge leaving it. Each choice is safe by the cut property applied to that component. Add the distinct chosen edges that join different current components and merge.

Even when two components choose the same edge, select it once. Simultaneous choices can appear cyclic under careless handling with ties; a deterministic union pass retains a safe acyclic subset. After a successful round, each nonisolated component merges with at least one other, so component count at least halves. There are $O(\log n)$ rounds, each scanning $m$ edges in a straightforward implementation.

Borůvka exposes component-parallel work and combines well with other algorithms. Parallelism still needs deterministic edge ownership, duplicate coalescing, synchronized component snapshots, and safe union semantics.

### Establish uniqueness and tie behavior

If every edge weight is distinct, the MST is unique. Suppose two MSTs $T$ and $T'$ differ. Let $e$ be the lightest edge in their symmetric difference and assume $e\in T$. Adding $e$ to $T'$ creates a cycle containing some $f\in T'\setminus T$. By choice and distinctness, $w(e)<w(f)$, so replacing $f$ produces a lighter tree, contradiction.

The converse is false. Consider a triangle with weights $1,2,2$ plus a leaf attached by weight $5$. The weight-one edge is mandatory; among the two weight-two triangle edges, actually either can combine with the weight-one edge, so that example is nonunique. To show equal weights with uniqueness instead, use a path whose edge weights are $1,1,2$: it is already the only spanning tree despite equal weights. Graph structure, not weight distinctness alone, determines uniqueness.

A useful edge-level characterization is:

- an edge belongs to every MST if it is the unique light edge across some cut;
- an edge belongs to no MST if it is strictly heaviest on some cycle;
- tied alternatives may belong to some but not all MSTs.

Sensitivity analysis and replacement-edge computation refine these statements, but belong to later depth.

### Handle negative, parallel, and exceptional weights

Negative weights need no special algorithm: sorted greedy choices and exchange proofs remain valid. Self-loops are never selected because they do not join components. Parallel edges are valid; a heavier parallel edge is dominated for the basic objective, but retain edge identity until policy authorizes reduction.

For floating weights, reject NaN because it breaks ordinary total comparisons. Decide whether infinities mean forbidden edges, valid extremely costly edges, or invalid input. Normalize signed zero if serialization matters. Summation order can change a floating total even when the edge set is fixed; use exact source units, decimal arithmetic, compensated summation with limitations, or a specified order according to the evidence required.

Never compare weights with an arbitrary epsilon inside sorting: a nontransitive “approximately less” relation can invalidate the sort and greedy proof. If measurements have uncertainty, model intervals, scenarios, or a robust objective rather than pretending near equality is exact equality.

### Validate structure and optimality

Structural validation checks:

1. every selected edge identity exists with matching endpoints and weight;
2. every declared vertex is present;
3. selected edges are acyclic;
4. selected edges connect each required input component;
5. a connected $n$-vertex result has $n-1$ edges;
6. reported total equals a checked recomputation;
7. result and input share snapshot and normalization policy.

These checks prove a spanning tree, not minimum weight. For bounded graphs, exhaustive enumeration is an independent oracle. For scalable verification, one certificate method roots the selected tree and preprocesses maximum-edge-on-path queries. For each non-tree edge $e=\{u,v\}$, require

$$
w(e)\ge \max\{w(f):f\text{ lies on the tree path }u\leadsto v\}.
$$

If a lighter non-tree edge existed, replacing a heavier path edge would improve the tree. If all inequalities hold, no single exchange improves it; the cycle property establishes optimality. The checker must use exact weight and tie semantics.

For an MSF, first independently find input connected components while ignoring self-loops. Validate one spanning tree and the exchange inequalities within each component, including isolated vertices.

### Engineer scale, determinism, and recovery

Kruskal benefits from sequential edge sorting and compact disjoint-set arrays. At large scale, use external sort with stable edge records, record spill volume, and preserve exact weights. Prim benefits when adjacency is already partitioned by vertex and the active frontier is manageable. Dense graphs may favor matrix scans. Borůvka can reduce components before another algorithm and expose parallel scans.

Deterministic output requires stable vertex and edge IDs, total weight order, total tie order, normalization, and snapshot. Disjoint-set representatives are internal and must not become external component identity. Parallel union order can change forest structure among ties even while weight remains minimum.

Cancellation yields an incomplete forest, not an MSF. A Kruskal checkpoint needs graph and sorted-run identity, next edge position, disjoint-set state or replay position, selected edge IDs, checked total, and output position. Prim needs visited state, current keys, parent edges, heap with stale-entry policy, and component restarts. Validate before resume.

Publish status, tree or forest edges, input components, total, arithmetic policy, tie policy, graph digest, and validation result atomically. A graph mutation after selection creates a new problem; do not relabel the old certificate as current.

### Respect the domain boundary

An MST minimizes the sum of selected existing undirected edges while connecting mandatory vertices. It does not minimize source-to-vertex distances; Prim's MST is not Dijkstra's shortest-path tree. It does not introduce new junctions as a Steiner tree may. It does not orient reachability like a minimum arborescence. It does not enforce degree, capacity, latency, geography, reliability, or redundancy constraints.

Before production use, ask whether costs are additive and independent, whether every vertex is mandatory, whether an edge can carry all required demand, whether one failure may disconnect the network, and whether direction matters. If not, the MST can still provide a lower bound, heuristic, or baseline, but label it accordingly.

### Test and observe the implementation

For small graphs, enumerate all $n-1$ edge subsets and compare minimum valid totals. Differentially compare Kruskal, Prim, and Borůvka by total and validity, not exact edge set under ties.

Metamorphic properties include:

- bijective vertex and edge renaming preserves mapped optimal edge sets under corresponding tie policies;
- adding a constant to every edge weight preserves MST edge sets because every tree has $n-1$ edges;
- multiplying all weights by a positive constant preserves optimum sets;
- adding a self-loop changes no MST;
- duplicating an edge with a heavier parallel copy changes no optimum;
- lowering a selected edge preserves at least one optimum containing it;
- transposing storage endpoints of undirected edges changes nothing;
- a strictly heaviest cycle edge is never selected;
- every selected edge is light across the cut created by deleting it from the returned tree.

Inject unknown endpoints, duplicate edge IDs, disconnected vertices, self-loops, parallel ties, negative values, integer overflow, NaN, infinity, comparison failure, iterator failure, sort spill exhaustion, cancellation, checkpoint corruption, snapshot replacement, and output failure.

Observe $n$, logical and physical $m$, component count, selected count, weight distribution, tie groups, self-loops, parallel records, sort bytes and runs, heap pushes and stale pops, disjoint-set finds and path lengths, maximum frontier, total arithmetic, validation cost, snapshot age, cancellations, and publication status.

## Definitions and Notation

Let $G=(V,E,w)$ be a finite undirected graph with weight function $w:E\to W$, where $W$ has a declared total comparison and summation policy. Let $n=|V|$ and $m=|E|$.

- A **walk** may repeat vertices and edges; a **path** has no repeated vertices.
- A **cycle** is a closed path with at least one edge under the multigraph convention.
- A **forest** is an acyclic undirected graph.
- A **tree** is a connected forest.
- A **spanning tree** has vertex set $V$ and is a tree.
- An **MST** minimizes $w(T)=\sum_{e\in T}w(e)$ over all spanning trees.
- An **MSF** is the union of an MST for each connected component.
- A **cut** $(S,V\setminus S)$ has $\varnothing\ne S\ne V$ for the connected case.
- An edge **crosses** a cut when exactly one endpoint lies in $S$.
- A cut **respects** $A$ when no edge of $A$ crosses it.
- A **light edge** attains minimum weight among the edges crossing a cut.
- A **safe edge** can be added to $A$ while preserving the existence of an MST containing the enlarged set.
- A **fundamental cycle** is the unique cycle created by adding one non-tree edge to a tree.
- A **fundamental cut** is the cut created by removing one tree edge.
- A **tie policy** imposes deterministic selection among equal-weight logical edges.
- An **optimality certificate** provides independently checkable evidence that no lighter spanning tree exists.

For a selected tree $T$ and non-tree edge $e=\{u,v\}$, write $P_T(u,v)$ for the unique tree path between its endpoints.

## Mechanisms, Invariants, or Proof Structure

### Generic safe-edge obligations

Maintain forest $A$ contained in some MST. Before adding $e$, exhibit a cut respecting $A$ and prove $e$ is light across it. The exchange construction replaces one crossing edge in an existing MST, preserves spanning and acyclicity, retains all earlier selected edges, and does not increase weight.

### Kruskal obligations

The disjoint-set partition equals connected components of selected forest $A$. Each accepted edge joins distinct components and preserves acyclicity. All earlier edges precede the current edge under total `(weight, tie)` order. The component cut is respected, and no lighter crossing edge remains unselected, so the accepted edge is safe. Selected-edge count increases and is bounded by $n-c$, proving termination for $c$ input components.

### Prim obligations

Selected edges form one tree on $S$. Every outside key is the lightest examined edge from $S$ to that vertex, and all adjacency of vertices in $S$ has been examined. The minimum current key is therefore light across $(S,V\setminus S)$. Stale heap entries are rejected against current membership and key. Each accepted edge adds exactly one vertex.

### Borůvka obligations

Current selected edges form a forest whose trees define components. Each component's chosen outgoing edge is light across its component cut. Duplicate choices are coalesced, and union checks retain an acyclic safe subset. Every nonisolated component merges, reducing component count geometrically.

### Certificate obligations

Coverage plus acyclicity and $n-1$ edges establish a spanning tree for a connected input. Exact total recomputation establishes the reported objective value. For every non-tree edge, comparison against the maximum edge on its fundamental tree path establishes that no cycle exchange can improve the tree; the exchange theorem extends this to global optimality.

## Alternatives and Trade-Offs

### Kruskal versus Prim

Kruskal is natural for edge lists, external sorting, sparse graphs, and MSF output. Prim is natural when adjacency is available and one connected tree grows from a root. Their practical costs depend on sorting, heap behavior, graph density, identifiers, and memory locality. Both rely on the same cut theorem.

### Prim matrix versus heap

An $O(n^2)$ matrix or dense-array implementation avoids heap overhead and predictable scans can win on dense graphs. A heap with adjacency lists avoids scanning absent edges and suits sparse graphs. Compare actual representation and cache behavior, not just headline bounds.

### Borůvka versus sequential greedy growth

Borůvka exposes per-component parallel choices and rapidly reduces component count. It repeatedly scans edges and needs synchronized component labels. Hybrid algorithms use Borůvka contraction before Kruskal or Prim. Complexity alone does not guarantee parallel speedup.

### One MST versus stable MST

Any MST satisfies the objective. Reproducible systems may require the lexicographically least edge sequence or stable edge IDs, adding sorting and identity constraints. Do not mistake deterministic selection for mathematical uniqueness.

### Exact versus floating weights

Exact integers or fixed decimals simplify comparison and totals but require width and scale governance. Floating values model measurements naturally but need finite-value validation, stable comparison, and explicit summation evidence. Approximate comparisons are not a total order and cannot be inserted casually into the proof.

### MST versus richer network models

Shortest-path trees minimize source distances; Steiner trees may add vertices; arborescences are directed; survivable networks add redundancy; degree-constrained and capacitated designs add feasibility conditions. Use MST only when its objective and feasible set match the decision.

## Failure Modes and Misconceptions

- **Directed-edge erasure:** converting arcs to undirected links can invent reachability the domain forbids.
- **Missing isolated vertices:** edge-derived enumeration hides disconnected input.
- **MST versus shortest paths:** low total tree weight does not minimize distance from any root.
- **Cheap-edge intuition:** an edge is safe through a respected cut, not merely because its absolute weight is small.
- **Cycle admission:** accepting an edge within one current component destroys the forest invariant.
- **Kruskal stopping error:** count selected edges, not scanned edges.
- **Stale Prim entry:** a previously good heap key may no longer represent the current minimum or an outside vertex.
- **Partial-tree success:** one Prim run on a disconnected graph does not span the graph.
- **Borůvka duplicate:** two components can choose the same logical edge; insert it once.
- **Tie overclaim:** equal weights do not prove nonuniqueness, and deterministic output does not prove uniqueness.
- **Cycle-property overclaim:** exclusion of a maximum edge requires strict heaviness for a specific edge.
- **Self-loop selection:** a loop connects no components and cannot enter a spanning forest.
- **Parallel-edge collapse:** endpoint deduplication can discard the cheaper or differently owned alternative.
- **NaN comparison:** NaN breaks the total ordering premise.
- **Epsilon sorting:** approximate less-than may be nontransitive.
- **Overflowed total:** correct edges with a wrapped sum produce a false objective report.
- **Mixed units:** adding dollars, milliseconds, and risk scores without an explicit model has no meaningful optimum.
- **Unstable IDs:** equal-weight choices can drift between runs and invalidate downstream references.
- **Mixed snapshots:** selection and validation against different edge sets prove nothing about either revision.
- **Model mismatch:** capacity, redundancy, direction, or new junctions require another optimization problem.

## Worked Examples

### Example 1

**Situation.** Determine whether edges $ab$, $bc$, and $ca$ form a spanning tree on $V=\{a,b,c,d\}$.

The selected subgraph omits every incident edge to $d$, so it is not connected and does not span operationally even though $d$ is declared. It also contains cycle $a,b,c,a$. A four-vertex tree must contain three edges, but edge count alone is insufficient: these three edges have both a cycle and an isolated vertex.

**Conclusion.** A spanning-tree validator must check declared-vertex coverage and acyclicity/connectivity, not only $n-1$ edges.

### Example 2

**Situation.** Forest $A=\{ab\}$ lies in a graph with $ab=1$, $ac=3$, $bc=2$, and $cd=4$. Show a safe next edge.

Take cut $S=\{a,b\}$ and complement $\{c,d\}$. It respects $A$. Crossing edges are $ac$ of weight three and $bc$ of weight two, so $bc$ is light and safe. Any MST containing $ab$ can exchange its crossing connection for $bc$ without increasing weight.

**Conclusion.** The safe choice depends on a cut respected by the current forest; $bc$ is justified even though another unselected edge elsewhere might be lighter.

### Example 3

**Situation.** Cycle edges have weights $ab=2$, $bc=5$, $cd=3$, and $da=4$.

Edge $bc$ is strictly heaviest. If a spanning tree contained it, deleting it would form a cut crossed by at least one other cycle edge on the route from $b$ to $c$. That replacement has weight at most four, producing a lighter tree. Therefore no MST contains $bc$.

**Conclusion.** A strictly heaviest cycle edge has a local exclusion certificate.

### Example 4

**Situation.** Run Kruskal on the executable graph.

Weight-one edges `ab`, `cd`, and `ef` join six vertices into three two-vertex components. At weight two, `bc` joins components $AB$ and $CD$, then `de` joins that component to $EF$. Five edges now span six vertices. Later edges would join vertices already connected and are skipped. Total is $1+1+1+2+2=7$.

**Conclusion.** Every accepted edge merges two forest components; the result has $n-1=5$ edges and verified minimum total seven.

### Example 5

**Situation.** Prim has current tree $S=\{a,b\}$. Heap contains old entry `(7,c,ac)` and newer entry `(3,c,bc)` after examining $b$.

The heap pops weight three first and selects `bc`, adding $c$. Later `(7,c,ac)` is stale because $c\in S$ and must be discarded. An implementation that selects it would add an edge within the tree, creating a cycle. If stale entries can tie, compare stable edge identity and current recorded key as well as membership.

**Conclusion.** Duplicate heap entries are safe only with an explicit stale-entry rejection invariant.

### Example 6

**Situation.** Graph has edges $ab=1$ and $cd=2$ on $V=\{a,b,c,d,e\}$.

No edge crosses among the three connected components $\{a,b\}$, $\{c,d\}$, and $\{e\}$. An MST of all five vertices does not exist. The MSF contains $ab$, $cd$, and an empty tree on isolated $e$, with total three under a sum-over-components convention.

**Conclusion.** Disconnected input needs an explicit forest result or error; two selected edges are not a spanning tree of five vertices.

### Example 7

**Situation.** Decide whether repeated weights force multiple MSTs in a path $a-b-c-d$ with weights $1,1,2$.

The graph itself is already a tree. Removing any edge disconnects it, and no alternative edge exists, so its only spanning tree is the entire graph. The repeated weight-one values create no exchange choice. By contrast, a four-cycle of all weight one has four distinct MSTs obtained by deleting any one edge.

**Conclusion.** Distinct weights guarantee uniqueness, but equal weights do not determine it; graph exchange structure does.

### Example 8

**Situation.** A floating edge list contains weights `1.0`, `2.0`, and NaN, and code sorts with ordinary comparisons.

NaN is neither less than, equal to, nor greater than ordinary values under IEEE comparison. A sort may retain an incidental position that does not represent a total weight order, invalidating the premise that all lighter edges precede the current edge. Reject NaN at normalization. If infinity is permitted, specify its order and whether it denotes a usable edge.

**Conclusion.** Numeric validation is part of the greedy proof because the algorithms require a coherent total comparison.

### Example 9

**Situation.** Kruskal externally sorts $m=800{,}000{,}000$ edge records of 32 bytes each and creates two full run copies during one merge stage.

One edge array is

$$
800{,}000{,}000\times32=25{,}600{,}000{,}000\text{ bytes}\approx23.84\text{ GiB}.
$$

Input plus two run copies require $76{,}800{,}000{,}000$ bytes, about $71.53$ GiB, before indexes, disjoint sets, filesystem metadata, and safety margin.

**Conclusion.** “Sort the edges” needs an I/O and storage budget; asymptotic time alone is not an execution plan.

### Example 10

**Situation.** A fiber planner may place new junction boxes anywhere, yet models only direct links among existing offices and returns their MST.

The computed tree is optimal among networks whose vertices are exactly the offices and whose edges are the offered direct links. A Steiner solution may introduce a junction and use less total fiber. Capacity, street geometry, redundancy, permits, and failure tolerance may further change feasibility. The MST remains a useful baseline or upper bound only if labeled with those restrictions.

**Conclusion.** Algorithmic optimality is always relative to the modeled feasible set and objective.

## Cross-Program Connections

- Data Structures Engineering owns disjoint-set, heap, adjacency, and compact edge representation; Algorithm Engineering owns safe-edge proofs and algorithm selection.
- Theory of Computation owns broader optimization complexity; MST is polynomial, while several nearby constrained variants are harder.
- Computer Architecture affects sorting, heap, memory locality, vectorization, and bandwidth but not the cut theorem.
- Network Engineering may use MST as a cost baseline, then add capacity, latency, direction, and resilience requirements.
- Distributed Systems adds partition ownership, parallel union, duplicate delivery, checkpoints, and deterministic publication.
- Data Engineering uses MST-like structures in clustering and similarity graphs, where weight semantics and sparsification determine meaning.
- Security Engineering must review whether attacker-controlled NaN, overflow, edge volume, or identifiers can corrupt ordering or exhaust resources.
- [ALGE-034](./034-strongly-connected-components.md) handles directed mutual reachability. [ALGE-036](../ROADMAP.md#block-04--graph-algorithms) will distinguish source-distance optimization from total spanning weight.

## References

1. Joseph B. Kruskal Jr., “On the Shortest Spanning Subtree of a Graph and the Traveling Salesman Problem,” *Proceedings of the American Mathematical Society* 7(1), 48–50, 1956, DOI [10.1090/S0002-9939-1956-0078686-7](https://doi.org/10.1090/S0002-9939-1956-0078686-7). Primary source; checked 2026-09-05.
2. Robert C. Prim, “Shortest Connection Networks and Some Generalizations,” *Bell System Technical Journal* 36(6), 1389–1401, 1957, DOI [10.1002/j.1538-7305.1957.tb01515.x](https://doi.org/10.1002/j.1538-7305.1957.tb01515.x). Primary source; checked 2026-09-05.
3. Jaroslav Nešetřil, Eva Milková, and Helena Nešetřilová, “Otakar Borůvka on Minimum Spanning Tree Problem: Translation of Both the 1926 Papers, Comments, History,” *Discrete Mathematics* 233, 3–36, 2001, DOI [10.1016/S0012-365X(00)00224-7](https://doi.org/10.1016/S0012-365X(00)00224-7). Translation and historical record; checked 2026-09-05.
4. Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein, *Introduction to Algorithms*, 4th ed., MIT Press, 2022, chapter 21. [Official publisher record](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/), checked 2026-09-05.
5. Jeff Erickson, *Algorithms*, 1st ed., 2019, minimum spanning trees chapter. [Author-hosted book](https://jeffe.cs.illinois.edu/teaching/algorithms/), checked 2026-09-05.
6. Robert Sedgewick and Kevin Wayne, *Algorithms*, 4th ed., Addison-Wesley, 2011, §4.3. [Author-maintained MST material](https://algs4.cs.princeton.edu/43mst/), checked 2026-09-05.
7. Boost C++ Libraries, “Kruskal Minimum Spanning Tree,” Boost.Graph 1.92.0 documentation. [Official documentation](https://www.boost.org/latest/libs/graph/doc/kruskal_min_spanning_tree.html), checked 2026-09-05.
8. Boost C++ Libraries, “Prim Minimum Spanning Tree,” Boost.Graph 1.92.0 documentation. [Official documentation](https://www.boost.org/latest/libs/graph/doc/prim_minimum_spanning_tree.html), checked 2026-09-05.
9. Bernhard Korte and Jens Vygen, *Combinatorial Optimization: Theory and Algorithms*, 6th ed., Springer, 2018. [Official DOI record](https://doi.org/10.1007/978-3-662-56039-6), checked 2026-09-05.

## Exercises

### Exercise 1

For vertices $\{a,b,c,d\}$ and weighted edges $ab=1$, $ac=4$, $bc=2$, $bd=5$, and $cd=3$, run deterministic Kruskal, show every disjoint-set decision, compute the total, and identify one cut certificate for each selected edge.

### Exercise 2

Prove the cycle property for a strictly heaviest edge. Then give a tied cycle showing why “strictly” cannot be removed from the claim that a particular edge belongs to no MST.

### Exercise 3

A Prim implementation pushes improved keys but never removes old heap entries. Construct a graph and trace showing how selecting stale entries can create a cycle or wrong total. State a complete stale-entry policy.

### Exercise 4

Choose and defend an MST implementation for an undirected graph with 200 million vertices and 1.5 billion exact integer-weight edges stored as an edge list on SSD. Memory cannot hold all edges, isolated vertices matter, repeatable output is required, and the result needs independently checkable optimality evidence.

### Exercise 5

A utility asks for the “cheapest reliable regional network.” Links have construction cost, capacity, failure probability, direction-dependent permits, and a requirement to survive any one link failure. Explain why a plain MST is insufficient, specify a more honest modeling workflow, and identify any legitimate role for MST evidence.

## Answers to the Exercises

### Answer 1

Sort by weight: $ab(1)$, $bc(2)$, $cd(3)$, $ac(4)$, $bd(5)$. Initially every vertex is separate. Select $ab$, merging $\{a\}$ and $\{b\}$. Select $bc$, merging $\{a,b\}$ with $\{c\}$. Select $cd$, merging $\{a,b,c\}$ with $\{d\}$. Three selected edges span four vertices, so later edges are unnecessary and would form cycles. Total weight is $1+2+3=6$.

For $ab$, cut $\{a\}\mid\{b,c,d\}$ has crossing weights one and four, so $ab$ is light. After selecting $ab$, cut $\{a,b\}\mid\{c,d\}$ is respected and has crossing edges $bc(2)$, $ac(4)$, and $bd(5)$, so $bc$ is light. After selecting $ab,bc$, cut $\{a,b,c\}\mid\{d\}$ is respected and has $cd(3)$ and $bd(5)$, so $cd$ is light. Each selection is safe.

### Answer 2

Assume cycle $C$ has edge $e$ with $w(e)>w(f)$ for every other $f\in C$, and suppose MST $T$ contains $e$. Removing $e$ partitions $T$ into two trees. The rest of cycle $C$ connects the endpoints of $e$, so at least one other cycle edge $f$ crosses this partition. Adding $f$ restores a spanning tree. Since $w(f)<w(e)$, tree $T-e+f$ is lighter, contradicting minimality. Thus no MST contains $e$.

For the tied case, take a triangle with all three weights one. Every pair of edges is a spanning tree of total two. Each edge is a maximum-weight cycle edge, but each belongs to two MSTs. The valid weaker conclusion is that some maximum edge can be omitted; no particular tied edge is excluded from every MST.

### Answer 3

Let edges be $ra=10$, $rb=1$, and $ba=2$, rooted at $r$. Initial heap holds key one for $b$ and ten for $a$. Pop $b$, select $rb$, and improve $a$ to two by pushing `ba` while old `ra` remains. Pop two, select $ba$, and mark $a$ in the tree. Later old key ten for $a$ appears. Selecting it would add $ra$ within the existing tree, forming cycle $r-b-a-r$ and reporting total thirteen rather than correct three.

On every pop, reject an entry if its vertex is already in the tree. If not, require that weight, predecessor edge ID, and any tie fields equal the current best record for that vertex; otherwise it is stale. Mark the vertex selected exactly once, then relax only edges to outside vertices under the same total comparison policy.

### Answer 4

Use external-sort Kruskal as the leading design because input is already an edge list and cannot fit memory. Preserve stable edge IDs and sort by exact `(weight, edge_id)` using durable runs under the repository's storage and recovery policy. Keep vertices in a separate canonical file so isolated vertices survive. A memory-mapped or partitioned disjoint-set structure needs wide parent and size fields, measured random-I/O behavior, and checkpointable merge progress. Borůvka contraction may reduce state first if measured scans and parallelism justify its additional coordination.

Return an explicit MSF if the graph is disconnected, including isolated components. Check integer total width before selection and use a wider or arbitrary-precision accumulator. Checkpoints bind input digest, run manifests, next merge position, disjoint-set/replay state, selected IDs, total, and output position. Stable sort and tie keys make the chosen optimum repeatable.

Independently validate edge provenance, vertex/component coverage, selected count, acyclicity, connectivity per input component, and total. Build a scalable optimality certificate using maximum-edge-on-tree-path queries for every non-tree edge, or use an independently implemented equivalent checker. Record sort bytes, run counts, SSD I/O, disjoint-set access, peak storage, component distribution, validation cost, and graph revision. Bounded exhaustive fixtures and differential Prim/Borůvka tests supplement but do not replace full-output certification.

### Answer 5

A plain MST assumes undirected existing links, additive scalar cost, no capacity constraints, and only ordinary connectivity. It intentionally has no redundancy: every tree edge is a bridge, so any link failure disconnects the result. It cannot encode direction-dependent permits, probability interactions, traffic demand, or the requirement to survive one failure.

First define mandatory sites, candidate physical links, directional feasibility, demand and capacity, failure model, service constraint, and a comparable economic objective. The feasible network likely needs two-edge connectivity or another survivable-network constraint, possibly with capacitated flow and scenario or reliability optimization. Multiobjective cost and risk need an explicit scalarization, constraint, or Pareto policy rather than mixed units.

An MST can remain a rigorously labeled lower-cost baseline when every feasible reliable network contains a connected undirected backbone, an initialization for an augmentation heuristic, or a comparison showing the price of redundancy. Its total is not automatically a valid lower bound if the richer model permits Steiner junctions or changes edge costs. Validate the final design against capacity and single-failure scenarios separately from the MST certificate.
