---
module_id: ALGE-031
program: Algorithm Engineering
level: 1
module_number: 31
title: Breadth-First Search
status: complete
last_verified: 2026-09-05
---

# Breadth-First Search

## One-Page Review

### Governing question

How do we preserve breadth-first search's exact hop-distance and predecessor guarantees while adapting graph representation, frontier organization, parallel discovery, memory movement, determinism, and failure handling to the deployed graph and machine?

### Essential definitions

- A **graph contract** fixes directedness, vertex identity, edge multiplicity, self-loop behavior, snapshot semantics, and neighbor access.
- The **unweighted distance** $\delta_S(v)$ is the minimum number of edges on a path from any source in $S$ to $v$, or $\infty$ when no such path exists.
- A **frontier** $F_k$ is the set of vertices first reached at distance $k$.
- A **discovery claim** changes a vertex from undiscovered to discovered and assigns its final level.
- A **predecessor** or **parent** $p(v)$ is a vertex at level $d(v)-1$ joined to $v$ by an admissible edge.
- A **BFS tree** is one valid predecessor tree for a single source; a **BFS forest** has one root for each source or connected component.
- **Push** traversal scans outgoing edges from the current frontier.
- **Pull** traversal scans undiscovered vertices for an incoming neighbor in the current frontier.
- A **sparse frontier** stores vertex identities; a **dense frontier** commonly stores membership bits.
- A **level-synchronous** implementation completes discovery for level $k+1$ before expanding it.
- **Direction optimization** selects push or pull by estimated work while preserving the same level contract.
- A **validation certificate** combines roots, levels, predecessor edges, edge inequalities, and coverage evidence.

### Central model, mechanism, or theorem

Let $G=(V,E)$ be a finite directed graph, let $\varnothing\ne S\subseteq V$, and give every edge unit cost. Breadth-first search returns a distance label $d$ and optional parent $p$ such that

$$
d(v)=\delta_S(v)
$$

for every reachable vertex $v$, while unreachable vertices retain $d(v)=\infty$. For every discovered non-source vertex,

$$
(p(v),v)\in E
\quad\text{and}\quad
d(v)=d(p(v))+1.
$$

The sequential mechanism places every source in a FIFO queue at level zero, claims a vertex before enqueueing it, and assigns each newly claimed neighbor one level beyond the vertex being expanded. The queue therefore exposes vertices in nondecreasing level order.

Correctness follows from two inequalities. Parent chains construct paths of length $d(v)$, so $\delta_S(v)\le d(v)$. Induction along a shortest path shows that BFS discovers $v$ by level $\delta_S(v)$, so $d(v)\le\delta_S(v)$. Thus equality holds. Parallel, distributed, algebraic, bidirectional, and external-memory variants are correct only when their discovery and level boundaries preserve equivalent obligations.

### Critical invariants

- Vertex and edge orientation semantics are normalized before traversal.
- Every source is claimed at level zero before any expansion.
- A vertex is claimed at most once for ordinary one-parent BFS, and the claim occurs before publication to a work queue.
- Every frontier contains exactly the vertices first discovered at its level.
- A child receives level $k+1$ only from an edge whose expanded endpoint has level $k$.
- Every published parent is an original admissible edge and decreases level by exactly one.
- No level $k+1$ work is expanded while level $k$ can still generate undiscovered vertices unless an asynchronous proof replaces the barrier.
- Neighbor order, parent ties, and source order are contractual when reproducible output is required.
- Directed pull traversal uses incoming adjacency; outgoing adjacency answers a different question.
- Early exit, depth limits, resource caps, and cancellation cannot turn incomplete exploration into an unreachable claim.
- Graph data, traversal metadata, validation, and publication are bound to one immutable snapshot or a proved consistency model.
- Benchmarks include representation construction, initialization, validation, output, and failed runs whenever the application pays those costs.

### Common failures

Frequent failures include marking vertices only when dequeued; allowing duplicate claims to overflow the queue; using a stack or priority policy while still calling the result BFS; treating discovery order as unique; assuming a single-source traversal covers disconnected vertices; using outgoing adjacency for pull on a directed graph; applying BFS to unequal edge costs; stopping an imbalanced bidirectional search at an unproved first collision; racing non-atomic visited checks; accepting a nondeterministic parent when the API promises a canonical path; clearing billion-entry arrays for tiny reachable components; measuring only edge scans while hiding construction and communication; treating traversed edges per second as application latency; reusing metadata across snapshots; publishing partial levels as complete; and validating only that every parent pointer names some vertex.

### Compact example

Suppose the directed edges are

$$
s\to a,\quad s\to b,\quad
a\to c,\quad b\to c,\quad
c\to t.
$$

The frontiers are

$$
F_0=\{s\},\qquad
F_1=\{a,b\},\qquad
F_2=\{c\},\qquad
F_3=\{t\}.
$$

Vertex $c$ may choose $a$ or $b$ as parent, depending on source and neighbor order or on the winner of a parallel claim. Its distance remains 2 either way. If the output contract requires the smaller parent under a declared order, “first successful claim” is insufficient in a parallel implementation; parent selection must be made deterministic without changing the level.

### Connections

[ALGE-001](./001-problem-statements-inputs-outputs-and-constraints.md) supplies the contract model, [ALGE-003](./003-loop-invariants-for-algorithm-correctness.md) supplies invariant proofs, [ALGE-006](./006-best-worst-expected-and-amortized-cost.md) supplies qualified costs, [ALGE-020](./020-engineering-a-sort-for-real-data-distributions.md) supplies measurement discipline, and [ALGE-030](./030-selecting-a-design-paradigm-from-problem-structure.md) supplies evidence-gated selection. Later graph modules build on the level and predecessor contracts established here.

## Governing Question

How can a simple level-order traversal remain provably correct and operationally useful when graphs are directed, disconnected, implicit, skewed, parallel, distributed, larger than memory, mutable, or subject to deterministic-output requirements?

Textbook BFS is a short queue loop. Engineered BFS is a contract spanning representation, discovery ownership, output semantics, cost accounting, validation, and lifecycle. The mathematical result may be only distances. A caller may instead need one path, a canonical path, all predecessors on shortest paths, a forest, vertices within a radius, or a stream of level events. Those outputs are not interchangeable.

The execution regime also changes the useful mechanism. Sparse high-diameter graphs often favor a conventional push frontier. A broad frontier in a low-diameter graph may make pull cheaper. Shared-memory workers need atomic claims and balanced work. Distributed workers need ownership, deduplication, and termination. GPUs need enough fine-grained work to hide latency. External-memory systems must organize scans and duplicate elimination around blocks. None of these changes licenses a different distance answer.

## Why This Matters

BFS is the basic exact algorithm for minimum-edge-count paths. It also supplies levels, reachability, component traversals in undirected graphs, parity information, shortest-path DAGs, bipartiteness witnesses, broadcast schedules, web or state-space exploration, and a primitive inside more elaborate graph algorithms. A defect in discovery semantics can therefore contaminate many downstream results.

The algorithm is also a revealing systems workload. Neighbor accesses are data dependent. Degrees can be extremely skewed. Frontiers can change from one vertex to most of the graph and back again. Many workers may race for the same popular vertex. Useful computation per edge is small, so memory bandwidth, cache misses, atomics, synchronization, allocation, and communication often dominate arithmetic.

Correctness and speed interact. Marking on dequeue appears to reduce synchronization but admits duplicates. Sorting neighbors creates reproducibility but costs time and memory unless the representation is already canonical. Pull traversal may reduce redundant edge examinations but needs reverse adjacency for directed graphs. Generation stamps avoid repeated clears but add width, wraparound, and concurrency obligations. A performance decision is safe only when its semantic effect is explicit.

## Prerequisites and Retrieval

Retrieve:

- finite directed and undirected graphs, vertices, edges, walks, paths, reachability, and connected components;
- sets, sequences, functions, induction, contradiction, and minimum arguments;
- queues, arrays, bitmaps, hash tables, adjacency lists, adjacency matrices, and compressed sparse row storage;
- asymptotic time and space, output-sensitive cost, cache locality, bandwidth, and external-memory block transfers;
- atomic compare-and-swap, barriers, memory visibility, work partitioning, and distributed ownership;
- immutable snapshots, versioning, cancellation, restart, validation, atomic publication, and rollback;
- Boolean vectors, sparse matrices, masks, and semiring-style graph operations;
- experimental design, workload distributions, percentiles, counters, and independent bounded oracles.

You should be able to distinguish a vertex identity from its array index and a path's number of edges from its numeric edge cost.

## Learning Objectives

After completing this module, you should be able to:

1. state a single-source or multi-source BFS contract with explicit unreachable, parent, tie, and failure semantics;
2. derive BFS from a FIFO discovery invariant rather than memorize a queue loop;
3. prove exact unit-edge distances and predecessor validity using complementary inequalities;
4. calculate representation-sensitive time, space, initialization, and output costs;
5. choose among queues, level arrays, sparse frontiers, dense bitmaps, push, pull, bidirectional search, and repeated-search metadata;
6. preserve exact levels under shared-memory, GPU, distributed, algebraic, and external-memory execution;
7. identify when unequal weights, dynamic updates, canonical-path requirements, or incomplete exploration require a different contract or algorithm;
8. validate distances, parents, coverage, and snapshot identity independently;
9. design fair BFS benchmarks and interpret edge-throughput metrics without hiding end-to-end cost;
10. operate traversal with budgets, observability, restart, publication, and reevaluation evidence.

## Core Exposition

### Fix the graph and output contract

Start with the observable graph. Define:

- whether edges are directed or undirected;
- whether parallel edges and self-loops exist and whether they are semantically distinct;
- the stable identity and ordering of vertices and edges;
- whether neighbor iteration is repeatable;
- whether the graph is materialized, generated implicitly, remote, compressed, or filtered;
- which immutable snapshot or consistency rule the traversal observes;
- whether a missing vertex, dangling neighbor, malformed record, or unavailable shard is invalid input or an incomplete read.

Then define the output. A distance-only result differs from:

- one arbitrary shortest path;
- one deterministic shortest path under a declared source and neighbor order;
- the lexicographically smallest vertex sequence among all shortest paths;
- all predecessor edges that participate in shortest paths;
- every shortest path, whose output can be exponential;
- a traversal event stream;
- a full forest over disconnected vertices;
- a radius-limited or target-limited result.

Ordinary BFS fixes distances but does not make its tree unique. If two level-$k$ vertices both point to a new vertex, either is a valid level-$k$ parent. Sequential adjacency order resolves the race incidentally; a parallel compare-and-swap winner may vary between runs. Make that difference part of the API.

For filtered graphs, specify whether forbidden vertices are absent, cannot be entered, cannot be expanded, or may appear only as terminal results. Each interpretation induces a different edge relation. Validate the effective graph contract, not merely the stored graph.

### Define unit-edge distance precisely

For a nonempty source set $S$, define

$$
\delta_S(v)
=
\min_{s\in S}\min\{
\text{number of edges in }P:
P\text{ is a directed path from }s\text{ to }v
\},
$$

with $\delta_S(v)=\infty$ if no such path exists. For one source $s$, write $\delta(s,v)$.

The metric counts edges, not stored weights, geometric length, latency, risk, or monetary cost. BFS solves a weighted shortest-path problem only when all admissible edges have the same positive cost, because minimizing edge count then minimizes total cost. With weights in $\{0,1\}$, use a deque-based 0–1 shortest-path algorithm. With arbitrary nonnegative weights, use a priority-ordered method such as Dijkstra's algorithm. Negative weights need a different contract and algorithm.

For every directed edge $(u,v)$ whose tail is reachable,

$$
\delta_S(v)\le\delta_S(u)+1.
$$

For an undirected edge with both endpoints reachable, applying the inequality in both orientations gives

$$
|\delta_S(u)-\delta_S(v)|\le1.
$$

These edge inequalities are central validation conditions, but they are not alone a complete certificate: labels also need roots, predecessor paths, and coverage.

### Derive the sequential queue mechanism

Maintain a distance map or array initialized to $\infty$, an optional parent map, and a FIFO queue. For each source in the declared source order:

1. if it is not already claimed, set its distance to zero;
2. set its parent to the root marker;
3. enqueue it.

Then repeat:

1. dequeue $u$;
2. inspect each admissible outgoing neighbor $v$ in the declared order;
3. if $v$ is undiscovered, claim it immediately;
4. assign $d(v)=d(u)+1$ and $p(v)=u$;
5. enqueue $v$ exactly once.

Claim before enqueue. If the implementation waits until dequeue, several parents can enqueue the same vertex. Correct final distances may survive in a small graph, but work and memory can grow drastically, events can repeat, parent selection becomes confused, and fixed-capacity queues can fail.

FIFO order is not cosmetic. If vertices are enqueued in nondecreasing level order, dequeue preserves that order. Replacing the queue with a stack produces depth-first behavior. Replacing it with a priority queue can implement a different shortest-path policy. A generic graph-library buffer changes semantics when it changes ordering.

### Execute a deterministic, validated BFS

This implementation normalizes neighbor order, claims on enqueue, supports multiple sources, returns explicit level groups, and validates its certificate against every edge reachable from the sources. It deliberately leaves unreachable vertices out of the finite maps. Its ordinary vertex-reachability contract permits normalization to coalesce parallel neighbor entries; an edge-event or multiplicity-sensitive contract would forbid that step.

<!-- bijux-verify: {"id":"deterministic-validated-bfs","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"single distances=(('a', 0), ('b', 1), ('c', 1), ('d', 2), ('e', 2), ('f', 2), ('g', 3))\nsingle parents=(('a', None), ('b', 'a'), ('c', 'a'), ('d', 'b'), ('e', 'b'), ('f', 'c'), ('g', 'd'))\nsingle layers=(('a',), ('b', 'c'), ('d', 'e', 'f'), ('g',)) scans=9\npath a-g=('a', 'b', 'd', 'g')\nmulti distances=(('a', 0), ('b', 1), ('c', 1), ('d', 2), ('e', 2), ('f', 2), ('g', 3), ('x', 0), ('y', 1)) scans=10 validation=passed\n","stderr":""}} -->
```python
from collections import deque
from dataclasses import dataclass


@dataclass(frozen=True)
class Search:
    distance: dict[str, int]
    parent: dict[str, str | None]
    layers: tuple[tuple[str, ...], ...]
    edge_scans: int


def normalize(graph):
    vertices = set(graph)
    normalized = {}
    for vertex, neighbors in graph.items():
        if any(neighbor not in vertices for neighbor in neighbors):
            raise ValueError(f"unknown neighbor from {vertex}")
        normalized[vertex] = tuple(sorted(set(neighbors)))
    return normalized


def breadth_first(graph, sources):
    graph = normalize(graph)
    roots = tuple(sorted(set(sources)))
    if not roots or any(root not in graph for root in roots):
        raise ValueError("sources must be nonempty graph vertices")

    distance = {}
    parent = {}
    queue = deque()
    for root in roots:
        distance[root] = 0
        parent[root] = None
        queue.append(root)

    edge_scans = 0
    while queue:
        vertex = queue.popleft()
        for neighbor in graph[vertex]:
            edge_scans += 1
            if neighbor not in distance:
                distance[neighbor] = distance[vertex] + 1
                parent[neighbor] = vertex
                queue.append(neighbor)

    layers = tuple(
        tuple(sorted(vertex for vertex, level in distance.items()
                     if level == wanted))
        for wanted in range(max(distance.values()) + 1)
    )
    return graph, Search(distance, parent, layers, edge_scans)


def validate(graph, sources, search):
    roots = set(sources)
    assert set(search.distance) == set(search.parent)
    assert set(search.layers[0]) == roots
    assert set().union(*map(set, search.layers)) == set(search.distance)

    for vertex, level in search.distance.items():
        assert vertex in search.layers[level]
        if vertex in roots:
            assert level == 0 and search.parent[vertex] is None
        else:
            predecessor = search.parent[vertex]
            assert predecessor is not None
            assert vertex in graph[predecessor]
            assert search.distance[predecessor] + 1 == level

    for tail in search.distance:
        for head in graph[tail]:
            assert head in search.distance
            assert search.distance[head] <= search.distance[tail] + 1


def path_to(search, target):
    if target not in search.distance:
        return None
    reverse_path = []
    vertex = target
    while vertex is not None:
        reverse_path.append(vertex)
        vertex = search.parent[vertex]
    return tuple(reversed(reverse_path))


graph = {
    "a": ("c", "b"),
    "b": ("e", "d"),
    "c": ("f", "d"),
    "d": ("g",),
    "e": ("g",),
    "f": ("g",),
    "g": (),
    "x": ("y",),
    "y": (),
}

normalized, single = breadth_first(graph, ("a",))
validate(normalized, ("a",), single)
print(f"single distances={tuple(sorted(single.distance.items()))}")
print(f"single parents={tuple(sorted(single.parent.items()))}")
print(f"single layers={single.layers} scans={single.edge_scans}")
print(f"path a-g={path_to(single, 'g')}")

normalized, multi = breadth_first(graph, ("x", "a"))
validate(normalized, ("a", "x"), multi)
print(
    f"multi distances={tuple(sorted(multi.distance.items()))} "
    f"scans={multi.edge_scans} validation=passed"
)
```

The validator does more than replay parents. Parent chains prove a path no longer than each label; edge inequalities and closure from reachable tails rule out missed shorter paths and missed reachable vertices. In a production system, snapshot identity, filter version, source set, arithmetic width, and publication status must also be checked.

### Prove exact distances with two bounds

First prove that labels never understate a realizable path. Each source has a zero-edge path. Whenever BFS assigns $d(v)=d(u)+1$, it records edge $(u,v)$. Induction on the parent chain constructs a source-to-$v$ path containing exactly $d(v)$ edges. Therefore

$$
\delta_S(v)\le d(v).
$$

Next prove BFS does not discover a vertex too late. Consider a shortest path

$$
s=x_0,x_1,\ldots,x_\ell=v,
\qquad s\in S,
$$

where $\ell=\delta_S(v)$. Sources are discovered at level zero. Assume $x_i$ is discovered with $d(x_i)\le i$. Before BFS can expand any vertex beyond that level, FIFO order expands $x_i$ and examines $(x_i,x_{i+1})$. If $x_{i+1}$ is new, it receives label at most $i+1$; if already discovered, its label is no larger. By induction,

$$
d(v)\le\ell=\delta_S(v).
$$

Combining the two inequalities gives $d(v)=\delta_S(v)$. The argument also proves reachability coverage: every vertex on every finite shortest path is eventually discovered if the traversal completes and neighbor generation is complete.

Notice the premises. The graph must be finite or exploration must have an explicit finite target boundary. Neighbor iteration must enumerate every admissible outgoing edge. Claims and queue operations must not be lost. A resource cap changes termination status; it does not preserve a complete unreachable conclusion.

### Account for representation-sensitive cost

Let $V_R$ be the vertices reachable from $S$, and let

$$
E_R=\{(u,v)\in E:u\in V_R\}.
$$

With adjacency lists or compressed sparse row storage, each reachable vertex is expanded once and each edge in $E_R$ is inspected once. Traversal work is

$$
\Theta(|V_R|+|E_R|).
$$

If dense arrays are cleared across the whole vertex universe, initialization adds $\Theta(|V|)$. A generation-stamp or sparse-map design can make metadata work proportional to reached vertices, but adds lookup, width, reuse, and wraparound obligations. For an undirected graph stored in both orientations, an abstract edge commonly contributes two adjacency entries.

An adjacency matrix makes each expansion scan a row of $|V|$ possible neighbors, giving $\Theta(|V_R||V|)$ inspections and $\Theta(|V|^2)$ representation bits or words. That can be appropriate for genuinely dense graphs, bit-parallel operations, or algebraic kernels, but it is wasteful for sparse graphs.

For an implicit graph, replace $|E_R|$ with total neighbor-generation work. If generating or validating a neighbor costs $g(u,v)$, then

$$
T
=
\Theta(|V_R|)
+
\sum_{u\in V_R}\sum_{v\in N^+(u)}\Theta(g(u,v)).
$$

Hashing large states, canonicalizing puzzles, reading remote adjacency, decompressing blocks, and evaluating filters are real traversal costs.

Metadata requires up to $\Theta(|V|)$ distance, parent, and visited storage. The active queue can also be linear. A level-frontier implementation retains current and next frontiers, whose peak depends on graph width, not diameter alone. Path reconstruction to target $t$ costs $\Theta(d(t)+1)$ output work.

### Choose representation with the workload

Adjacency lists offer flexible updates and direct iteration but may allocate many small objects and pointers. Compressed sparse row stores offsets plus contiguous neighbor identifiers, improving locality and reducing per-edge overhead for static graphs. A directed pull implementation also needs compressed sparse columns, explicit incoming lists, or another correct reverse-edge access path.

Representation choices affect semantics:

- sorting neighbor identifiers makes local order deterministic but may discard stored edge order;
- deduplicating parallel neighbors preserves ordinary reachability and distance but not edge-identity events or multiplicity-sensitive output;
- relabeling vertices can improve locality but requires exact source and result lifting;
- compressing identifiers or offsets requires range checks and widening before arithmetic;
- storing only a subgraph or cache requires completeness evidence for an unreachable claim;
- lazily deleted edges need snapshot-visible filtering.

Measure construction separately and together with traversal. If one graph supports thousands of searches, expensive CSR construction, transpose creation, relabeling, or compression may amortize. For a single small search, conversion can dominate. Bind every derived representation to the source graph digest or version and the filter contract.

### Make parent and tie semantics explicit

Distances are unique; BFS trees generally are not. Possible contracts include:

1. any predecessor at the previous level;
2. the first predecessor under stable sequential neighbor order;
3. the minimum predecessor identifier among all previous-level neighbors;
4. the lexicographically smallest full shortest path;
5. every previous-level predecessor.

These require increasingly different work. A parallel atomic claim naturally implements “some winner,” not minimum parent. To obtain minimum predecessor after distances are final, scan incoming neighbors $u$ with

$$
d(u)+1=d(v)
$$

and choose the minimum under the declared order. This adds edge work but makes the choice independent of scheduling. The lexicographically smallest entire path may require an ordering of predecessor path ranks, not merely the smallest immediate parent.

All-predecessor output forms a shortest-path directed acyclic graph because every predecessor edge increases level by one. The number of predecessor edges is at most $|E_R|$, but enumerating all shortest paths through that graph can be exponential. State whether the output is the compact predecessor relation or every expanded path.

### Handle target, radius, source, and component variants

For a single target and ordinary claim-on-enqueue BFS, the first discovery of the target fixes its minimum distance. The implementation can stop after assigning its parent if the contract asks for any one shortest path. It cannot claim complete distances for other queued vertices or complete coverage of the target's level.

A radius limit $r$ may expand levels $0$ through $r-1$ and report vertices through level $r$. Decide whether edges leaving level $r$ must be inspected for validation or boundary counts. A work or time budget is different from a semantic radius: budget exhaustion returns incomplete, while completing a declared radius can return a complete bounded result.

Multi-source BFS initializes every source at distance zero. It computes

$$
d(v)=\min_{s\in S}\delta(s,v).
$$

Source ordering affects ownership ties but not distance. A virtual super-source with unit edges would add one to every distance; a zero-cost virtual edge needs a different mechanism. Direct level-zero initialization is the clean construction.

Single-source BFS reaches only one directed reachable set. To form an undirected component forest, iterate through all vertices and launch BFS at each still-unseen vertex. In directed graphs, this produces traversal trees dependent on outer order, not strongly connected components. Do not label that forest as an SCC decomposition.

### Use bidirectional search only with a stopping proof

For a known target in an unweighted graph, search forward from the source and backward from the target. In a directed graph, the backward search must traverse incoming edges. Whenever a forward-reached edge or vertex meets backward-reached state, construct a candidate path. For a crossing edge $(u,v)$, its length is

$$
d_s(u)+1+d_t(v).
$$

Idealized branching factor $b$ and solution depth $D$ suggest reducing explored states from roughly $b^D$ to roughly $2b^{D/2}$. Real graphs have duplicates, skew, asymmetry, and frontier overhead, so this is a regime hypothesis.

“Stop at the first collision” is safe only for a precisely proved expansion policy. Expanding the smaller frontier can advance the two sides to different depths. Maintain the best complete candidate and a lower bound on any path through unexpanded levels; stop only when that lower bound cannot improve the candidate. Preserve enough parent state on both sides to join and validate the path.

Bidirectional search is poor when there is no specific target, reverse adjacency is unavailable, one side explodes, or the full distance map is required.

### Represent frontiers sparsely or densely

A sparse frontier stores the identities in $F_k$ and iterates only their adjacency. It is efficient when $|F_k|$ and incident work are small. A dense bitmap permits constant-time membership tests, word-parallel set operations, and pull traversal, but scanning or clearing it may cost $\Theta(|V|)$ per level.

Conversions have costs:

- sparse to dense sets one bit per frontier identity and may clear or epoch-tag the bitmap;
- dense to sparse scans words and extracts set bits;
- duplicate candidate lists need filtering or atomic claims;
- two frontier buffers need capacity for worst observed widths;
- compression saves bandwidth only if decode work and random access fit.

Select by estimated incident work and representation cost, not vertex count alone. Ten high-degree vertices can generate more edges than a million low-degree vertices. Record frontier vertices, frontier edges, undiscovered vertices, conversion bytes, and duplicate attempts by level.

### Switch between push and pull without changing levels

Top-down push examines outgoing edges from the current frontier:

$$
W_{\mathrm{push}}(k)
=
\sum_{u\in F_k}\deg^+(u).
$$

When a broad frontier points repeatedly to the same small undiscovered set, much of this work loses discovery races. Bottom-up pull considers each undiscovered vertex and asks whether any incoming neighbor lies in $F_k$. Its worst scan bound is

$$
W_{\mathrm{pull}}(k)
\le
\sum_{v\in U_k}\deg^-(v),
$$

but it can stop scanning $v$ as soon as one frontier neighbor is found. Pull is attractive when the chance of an early hit is high and frontier membership is cheap.

Direction-optimizing BFS uses push in sparse levels, pull across one or more dense levels, then often returns to push. Thresholds are machine-, representation-, and graph-dependent. They are performance policy, not correctness proof. A safe switch:

- completes one level before changing direction;
- uses the same visited state and snapshot;
- gives pull correct incoming adjacency;
- claims only previously unseen vertices;
- assigns every new vertex the next level;
- preserves or reconstructs the promised parent semantics.

For directed graphs, scanning outgoing neighbors of an undiscovered vertex asks whether it points into the frontier, which is not whether the frontier can reach it. That mistaken pull reverses reachability.

### Engineer shared-memory traversal

A level-synchronous shared-memory design partitions the current frontier or its incident edges across workers. Each worker examines neighbors and attempts an atomic transition from undiscovered to level $k+1$. Exactly one claim owner publishes the ordinary parent and next-frontier identity.

The atomic state transition must precede or atomically accompany publication. Enqueue-then-mark allows duplicates; mark-without-release before another worker reads parent state can expose an incomplete record. Specify the memory-order relation between distance, parent, and frontier visibility.

Degree skew makes equal vertex counts unequal work. Useful strategies include:

- prefix sums over frontier degrees followed by edge-range partitioning;
- dynamic chunks or work stealing;
- splitting individual high-degree vertices;
- thread-local candidate buffers followed by deduplication;
- sparse and dense kernels with different scheduling;
- padding or partitioning hot metadata to reduce contention.

Barriers separate levels in a conventional proof. Removing them can be correct, but the replacement must ensure a vertex is not expanded at a nonfinal level and that termination does not overlook messages or work. “Eventually consistent visited bits” is not enough.

Parent races deserve separate treatment. If any parent is permitted, the atomic winner is valid. If minimum parent is required, use an atomic minimum restricted to level-$k$ candidates or a deterministic postpass. If callbacks have side effects, define whether they run once per edge attempt, once per successful claim, or once per finalized vertex.

### Engineer GPU and distributed traversal

GPUs need enough independent work to hide memory latency. Vertex-parallel push assigns vertices, but one high-degree vertex can monopolize a worker. Edge-parallel and prefix-sum-based schemes flatten adjacency work. Candidate compaction, duplicate elimination, frontier conversion, and atomic contention can dominate. Coalescing and representation layout matter more than the few instructions in the BFS recurrence.

Distributed memory assigns each vertex and its adjacency to an owner. A level commonly performs:

1. local expansion of owned frontier work;
2. routing of remote discovery candidates to destination owners;
3. owner-side deduplication and claim;
4. construction of the next distributed frontier;
5. a completion or termination agreement for the level.

Partitioning affects communication volume and balance. One-dimensional vertex ownership is simple but can send many remote candidates. Two-dimensional decompositions can reduce some communication at the price of more complex collectives and metadata. High-degree hubs create hot owners. Compressing vertex lists, combining duplicates, and separating local from remote edges can help.

The correctness contract must survive message duplication, reordering, retry, worker loss, and restart. Idempotent claims can tolerate duplicate candidates. Missing messages cannot. A checkpoint must bind graph snapshot, sources, completed level, visited state, parents, ownership map, and pending-message protocol. Publication waits for global coverage and validation, not merely an empty local queue.

### Express BFS algebraically

Let $A_{uv}=1$ exactly when directed edge $(u,v)$ exists, and let row vector $f_k$ mark frontier $F_k$. Boolean matrix-vector style propagation computes candidates

$$
c_k=f_k\otimes A,
$$

where multiplication is logical conjunction and addition is logical disjunction. Equivalently,

$$
c_k(v)=1
\Longleftrightarrow
\exists u\in V:
f_k(u)=1\land A_{uv}=1.
$$

Mask already seen vertices:

$$
f_{k+1}=c_k\land\neg\operatorname{seen}_k.
$$

Sparse linear-algebra libraries can choose representations and kernels for the frontier and mask. Orientation remains critical: a column-vector convention may require $A^\mathsf{T}$. Boolean propagation produces levels but not necessarily a parent. Parent selection needs a valued operator that carries an identity under a defined tie rule or a separate predecessor pass.

Algebraic notation does not make every level cheap. Sparse matrix-vector work depends on frontier density, mask behavior, storage orientation, and implementation. Validate the mathematical orientation with a small asymmetric directed graph before benchmarking.

### Respect external-memory and remote-adjacency costs

When adjacency does not fit RAM, random neighbor access can dominate. A naive queue may repeatedly fetch small remote blocks. Level-oriented external algorithms generate candidate vertices, sort or partition them, remove duplicates and previously visited identities, then obtain adjacency in block-friendly order.

The cost model includes:

- block size and cache capacity;
- adjacency index and compression;
- frontier and visited representation;
- candidate sort, merge, and deduplication I/O;
- number of levels and repeated scans;
- temporary disk, checksums, and manifests;
- remote request batching, retry, and rate limits.

An external or remote store must distinguish “no adjacency” from “adjacency unavailable.” Only the first can support an unreachable conclusion. Persist immutable level outputs and bind them to input and filter versions. After interruption, resume only from a completed level whose frontier, visited set, and parent records reconcile.

### Reduce repeated initialization safely

Running many BFS queries can spend more time clearing metadata than traversing small components. A generation array stores a search identifier for each touched vertex; a vertex is unseen in the current search when its stored generation differs. This turns global clearing into touched-state writes.

Generation identifiers have a finite width. On wraparound, stale entries can become falsely current. Use a width whose lifetime is justified, perform a safe full reset before reuse, or pair identifiers with a larger epoch. Concurrent searches need distinct ownership and cannot share mutable parent or queue state accidentally.

Repeated searches may amortize graph construction, reverse adjacency, relabeling, and frontier buffers. They do not justify reusing distances after the graph, source set, filter, or semantics change. Dynamic BFS maintenance is a separate algorithmic problem; ordinary recomputation on an immutable snapshot is often the safest baseline.

### Validate a BFS certificate independently

For a completed finite search, validate at least:

1. every source exists, has distance zero, and has the root parent marker;
2. no nonsource has distance zero;
3. every finite-distance nonsource has one promised parent;
4. the parent edge exists in the effective graph;
5. parent distance plus one equals child distance;
6. following parents reaches a source without a cycle;
7. every edge from a finite-distance tail leads to a finite-distance head with label at most tail label plus one;
8. unreachable labels use the declared sentinel and no stale parent;
9. level and parent numeric types cannot overflow;
10. graph, source, filter, ordering, and implementation versions match the traversal record.

Conditions 1–7 prove exact distances and reachable-set coverage when adjacency enumeration is complete. For an undirected graph, also check the symmetric absolute level difference. At bounded scale, compare against an independent all-pairs or repeated-relaxation oracle rather than a second copy of the same BFS loop.

Metamorphic checks include permuting storage while preserving a nondeterministic-parent contract; adding a self-loop without changing distances; duplicating an edge without changing ordinary reachability; adding an isolated vertex without changing reached labels; relabeling vertices bijectively and lifting results; and adding a new source, which can only decrease or preserve distances.

Inject malformed neighbors, duplicate messages, queue-capacity failure, cancellation, checkpoint restart, missing shards, generation wraparound, and snapshot changes. A validator failure blocks publication.

### Measure the actual application

Useful per-run and per-level observations include:

- reached vertices and inspected adjacency entries;
- frontier vertices, frontier edges, and peak frontier bytes;
- successful claims, duplicate attempts, and atomic contention;
- push or pull mode and conversion cost;
- bytes read, cache misses, memory bandwidth, and decompression;
- local and remote candidates, messages, bytes, imbalance, and barrier time;
- construction, initialization, traversal, parent canonicalization, validation, and output time;
- status, depth, resource-cap event, cancellation, retry, and fallback;
- graph, source, ordering, representation, and implementation versions.

Traversed edges per second can compare kernels under a precise benchmark definition. It is not a substitute for end-to-end latency, cost per query, peak memory, energy, or time to a target. An implementation can report high edge throughput by inspecting edges the application could have avoided.

Benchmark multiple graph families: paths, grids, trees, stars, cliques, high-diameter road-like graphs, low-diameter hub graphs, disconnected graphs, directed asymmetric graphs, and representative production snapshots. Keep source selection, warm state, construction, validation, and stopping conditions equal. Retain failed and incomplete runs.

### Operate traversal as a versioned computation

Before launch, record the effective graph version, sources, output contract, direction policy, deterministic-order policy, resource budgets, and validator. During execution, make cancellation cooperative and preserve an explicit incomplete state. Treat overflow, malformed graph data, unavailable adjacency, lost distributed work, and validation failure as errors, not unreachable vertices.

Publish results atomically after the requested scope completes and validation passes. A radius-limited result can be complete for its radius while explicitly unknown beyond it. A target-only result can contain a validated path without claiming a full distance map. Preserve the prior published generation until the new one activates.

Reevaluate representation and direction thresholds when degree distribution, component size, source distribution, hardware, memory budget, network topology, graph update rate, or output contract changes. The enduring artifact is not one threshold; it is the evidence tying a policy to a regime.

## Definitions and Notation

Let $G=(V,E)$ be a finite graph with $n=|V|$ vertices and $m=|E|$ abstract edges. For a directed graph, $(u,v)\in E$ permits movement from $u$ to $v$. For an undirected graph, each edge permits both orientations even if stored once.

- The **effective graph** is the exact vertex and edge relation remaining after snapshot selection, authorization, filtering, and malformed-data policy.
- A **source set** $S$ is a nonempty subset of $V$ whose members begin at level zero.
- A **walk** may repeat vertices and edges. A **path** here is a walk without repeated vertices; a shortest unit-edge walk always has a path representative.
- Vertex $v$ is **reachable** from $S$ if an effective directed path begins at some $s\in S$ and ends at $v$.
- $\delta_S(v)$ is the minimum edge count of such a path, or $\infty$ if none exists.
- A **distance label** $d(v)$ is an algorithm output intended to equal $\delta_S(v)$.
- A **level** $L_k$ is $\{v\in V:\delta_S(v)=k\}$.
- A **frontier** $F_k$ is the implementation representation of vertices being used to generate level $k+1$; a correct level-synchronous BFS has $F_k=L_k$ within its requested scope.
- A vertex is **undiscovered** when the current search has made no valid claim for it.
- A **claim** is the linearization event that assigns a vertex its finite level for the current search.
- A **parent** $p(v)$ is a predecessor selected to certify one shortest path. Roots use an explicit null or self marker, never stale storage.
- A **BFS tree** contains one parent edge for every reachable nonsource vertex under a single source.
- A **BFS forest** contains one such rooted structure per source or per outer component traversal.
- A **shortest-path predecessor relation** contains every edge $(u,v)$ satisfying $d(u)+1=d(v)$; it can be much larger than one tree.
- A **discovery order** lists claim events. It depends on source, neighbor, and concurrency order unless canonicalized.
- A **completion order** lists finished expansions and need not equal discovery order.
- **CSR** stores one offset per vertex plus contiguous outgoing neighbor identifiers.
- **CSC** is the corresponding compressed incoming-edge representation.
- A **sparse frontier** enumerates frontier vertices; a **dense frontier** supports membership over the vertex universe, commonly with a bitmap.
- **Push** maps outgoing adjacency from $F_k$ to candidates.
- **Pull** maps undiscovered vertices to incoming adjacency and tests for a member of $F_k$.
- **Work** counts total operations across workers; **span** is the longest dependence chain under the stated model.
- A **snapshot** is the graph revision and visibility rule against which every adjacency read and output claim is interpreted.
- A result is **complete** only for its declared source, target, radius, graph, and output scope. A resource-limited partial traversal is **incomplete**, not a proof of unreachability.

Use $N^+(u)$ and $\deg^+(u)$ for outgoing neighbors and degree, and $N^-(v)$ and $\deg^-(v)$ for incoming neighbors and degree. In an undirected graph, write $N(v)$ and $\deg(v)$. Let $D=\max_{v\in V_R}\delta_S(v)$ be reached depth and

$$
B_{\max}=\max_{0\le k\le D}|L_k|
$$

be maximum level width. These parameters describe different risks: a path has large $D$ and tiny width; a star has depth one and a frontier nearly as large as $V$.

## Mechanisms, Invariants, or Proof Structure

### Queue-order invariant

At the beginning of each sequential loop iteration, queue labels are nondecreasing from front to back. If the front has level $k$, every queued vertex has level $k$ or $k+1$.

Initially all queued sources have level zero. Assume the invariant before dequeueing $u$ at level $k$. Existing queued vertices have level $k$ or $k+1$. Newly discovered neighbors receive $k+1$ and are appended, so order remains nondecreasing. Once the last level-$k$ vertex leaves, the new front has level $k+1$. The claim-on-enqueue rule prevents a later path from adding the same vertex again.

This invariant is the operational bridge between a FIFO container and shortest-hop semantics. A library abstraction called a queue is insufficient if its pop policy is not FIFO.

### Frontier exactness invariant

After all vertices of level $k-1$ have been expanded and before any vertex of level $k$ is expanded,

$$
F_k
=
\{v\in V:\delta_S(v)=k\}.
$$

Soundness follows because every claimed member has a parent chain of exactly $k$ edges. Completeness follows by taking the penultimate vertex on any shortest $k$-edge path: it lies at level $k-1$, is expanded, and exposes the final edge. A level-synchronous parallel implementation can use this invariant directly even though it has no single FIFO order.

### Exact-distance theorem

Assume:

1. $G$ is finite and fixed for the traversal;
2. sources are valid and all initialized at level zero;
3. expansion enumerates every effective outgoing neighbor;
4. each undiscovered vertex is claimed from a current-level edge before joining the next frontier;
5. every generated frontier is eventually expanded until the requested traversal completes.

Then BFS assigns $d(v)=\delta_S(v)$ exactly to the reachable vertices.

The constructive parent-chain argument proves $\delta_S(v)\le d(v)$. Induction along a shortest path proves $d(v)\le\delta_S(v)$. The second argument also proves every reachable vertex is claimed. No performance optimization may weaken one of the five premises without supplying a replacement proof.

### Parent-certificate theorem

Suppose a finite labeling has:

- every source at level zero with a root marker;
- every finite nonsource $v$ with edge $(p(v),v)$ and $d(p(v))+1=d(v)$;
- every edge $(u,v)$ from a finite $u$ leading to finite $v$ with $d(v)\le d(u)+1$.

Repeatedly following parents strictly decreases a nonnegative integer label, so it reaches a source without cycling and constructs a path of length $d(v)$. Thus $\delta_S(v)\le d(v)$. Applying the edge inequality along any source-to-$v$ path gives $d(v)\le$ its length; minimizing gives $d(v)\le\delta_S(v)$. Closure across every edge from a finite tail ensures a reachable vertex cannot be omitted. Therefore the finite labels are exactly the shortest-hop distances.

This certificate assumes the validator sees the complete effective outgoing adjacency. A missing shard can make a false result pass a partial scan.

### Work and storage theorem

Under constant-time array claims and adjacency iteration, every reached vertex is enqueued and dequeued once, and each outgoing adjacency entry of a reached vertex is inspected once. Hence traversal work is

$$
\Theta(|V_R|+|E_R|).
$$

The lower bound is tight for the explicit completed output: BFS must at least identify every reached vertex, and an adversarial unseen outgoing edge can reveal a new vertex. Whole-universe initialization changes the end-to-end bound to

$$
\Theta(|V|+|E_R|).
$$

Storage beyond the graph is $\Theta(|V|)$ with dense metadata, or $\Theta(|V_R|)$ expected storage with suitable sparse maps, plus active work. Storing distances and one parent uses two values per reached vertex. Storing all shortest-path predecessor edges can use $\Theta(|E_R|)$.

### Multi-source reduction

Initializing $S$ at level zero is equivalent for distances to adding a conceptual super-source with zero-cost edges to every $s\in S$ and then subtracting no level. Ordinary unit-edge BFS cannot represent those zero-cost edges directly without adding one, so simultaneous initialization is the implementation mechanism.

For any vertex $v$, take the closest source $s^*$. The single-source proof along its shortest path shows $d(v)\le\delta(s^*,v)$. Every parent chain ends at some source, so its length is at least $\min_{s\in S}\delta(s,v)$. Therefore

$$
d(v)=\min_{s\in S}\delta(s,v).
$$

Root ownership is a tie rule separate from this equality.

### Deterministic-parent refinement

Let distances already be exact and let $\prec$ be a total order over vertex identities. Define

$$
p_{\min}(v)
=
\min_{\prec}\{u:(u,v)\in E\land d(u)+1=d(v)\}.
$$

The set is nonempty for each reachable nonsource vertex. Selecting its minimum produces a deterministic valid BFS tree independent of discovery races. A postpass over incoming edges is easy to prove. An online atomic-min implementation is also possible, but parent finalization must wait until every level-$d(v)-1$ candidate is accounted for.

This rule does not automatically produce the lexicographically smallest full path. Immediate parent identity and predecessor-path order are different objectives.

### Level-synchronous parallel refinement

Assume $F_k=L_k$. Workers inspect the appropriate edges and atomically claim only previously unseen endpoints for $F_{k+1}$. Every successful claim has a length-$k+1$ parent chain, proving soundness. Every level-$k+1$ vertex has a shortest-path predecessor in $L_k$, whose edge is inspected, proving completeness. A barrier or equivalent termination agreement freezes $F_{k+1}$ before expansion. Induction over $k$ recovers frontier exactness.

Duplicate candidate messages are harmless only if owner-side claim is idempotent and no required callback counts raw candidates as vertices. Lost candidates violate completeness. A relaxed implementation must specify the linearization point and visibility of level, parent, and frontier publication.

### Push-pull equivalence

Push constructs

$$
C_{k+1}^{\mathrm{push}}
=
\{v\notin\operatorname{seen}_k:
\exists u\in F_k,\ (u,v)\in E\}.
$$

Correct directed pull constructs

$$
C_{k+1}^{\mathrm{pull}}
=
\{v\notin\operatorname{seen}_k:
\exists u\in N^-(v)\cap F_k\}.
$$

These sets are equal by the definition of incoming adjacency. Therefore direction selection can preserve exact frontiers. Using $N^+(v)$ in the pull expression instead computes vertices that can reach the frontier by one edge, not vertices the frontier can reach.

### Bidirectional candidate invariant

Forward labels certify source-to-vertex path prefixes. Backward labels, computed over reversed directed edges, certify vertex-to-target suffixes. A shared vertex $x$ yields candidate length $d_s(x)+d_t(x)$. A scanned crossing edge $(u,v)$ yields $d_s(u)+1+d_t(v)$.

The best candidate is an upper bound on the optimal distance. The minimum possible length through all not-yet-connected level pairs is a lower bound. Termination is sound only when this lower bound is at least the best candidate. The exact lower-bound expression depends on whether complete levels, individual vertices, or priority-ordered pairs are expanded; derive it for the chosen policy instead of copying a first-meeting rule.

### Snapshot and publication invariant

Let $r$ identify the effective graph revision. Every adjacency block, source, filter, checkpoint, distance, parent, and validation result must be interpreted under $r$. If an edge read belongs to another revision, the proof concerns no single graph.

A completed published record contains:

$$
(r,S,\text{scope},\text{ordering},d,p,\text{status},E_{\mathrm{validation}}).
$$

Cancellation, unavailable adjacency, numeric overflow, lost work, or failed validation produces a failed or incomplete record. Atomic activation prevents readers from mixing a new distance map with old parent or graph metadata.

## Alternatives and Trade-Offs

| Approach | Best fit | Principal advantage | Principal obligation or cost |
|---|---|---|---|
| FIFO adjacency-list BFS | General sparse unit-edge graph | Simple tight work bound | Random adjacency access and linear metadata |
| Level arrays | Parallel or batched levels | Explicit frontier invariant | Two buffers, deduplication, and barriers |
| CSR push | Static sparse graph | Compact sequential edge access | Build cost and awkward updates |
| Dense-matrix BFS | Dense or bit-parallel graph | Regular operations | Quadratic representation and row scans |
| Sparse frontier | Small incident frontier | Avoids whole-universe scans | Irregular work and duplicate claims |
| Dense bitmap frontier | Broad frontier | Fast membership and word parallelism | Universe scans and conversion |
| Pull traversal | Broad frontier with many early hits | Can avoid redundant push edges | Incoming adjacency and undiscovered scan |
| Direction-optimizing BFS | Frontier density changes sharply | Adapts edge examinations | Tuned switching policy and dual representations |
| Bidirectional BFS | One source-target query | Can reduce explored depth | Reverse access and proved stopping rule |
| Multi-source BFS | Nearest of many sources | One traversal for minimum source distance | Root tie and ownership semantics |
| Generation-stamped metadata | Many small repeated searches | Avoids full clears | Epoch width, reset, and concurrency |
| Shared-memory BFS | Graph fits one coherent memory | Low communication | Atomics, contention, balance, visibility |
| GPU BFS | Large frontiers and suitable layout | High memory-level parallelism | Irregular degrees, compaction, and transfer |
| Distributed BFS | Graph exceeds one node | Aggregate capacity | Routing, ownership, deduplication, and termination |
| Algebraic BFS | GraphBLAS-style pipeline | Composable sparse kernels | Orientation, mask, semiring, and parent semantics |
| External-memory BFS | Adjacency exceeds RAM | Block-aware exact traversal | Sorting, deduplication, repeated I/O, and restart |
| 0–1 deque shortest path | Edge weights are zero or one | Linear-style specialized relaxation | Not ordinary visited-once BFS |
| Dijkstra-style search | Nonnegative unequal weights | Exact weighted distances | Priority queue and relaxation semantics |
| A* search | One target plus admissible heuristic | May reduce explored states | Heuristic and stopping proof |
| Depth-first search | Reachability with depth structure | Low frontier memory on some graphs | Does not give minimum hop distances |

Choose ordinary BFS when the contract is unit-edge distance or level reachability and the reachable state fits the resource policy. Choose a specialized frontier representation from measured graph and machine facts. Choose a different shortest-path algorithm when edge costs differ. Choose external, distributed, or implicit-state mechanisms when the representation—not the recurrence—is the obstruction.

Early exit reduces work for one target but cannot satisfy a full-map contract. Bidirectional search reduces idealized depth but adds reverse state and termination complexity. Direction optimization may reduce inspected edges on hub graphs but can lose on paths or high-diameter sparse frontiers. A deterministic parent postpass adds cost but cleanly separates distance parallelism from output reproducibility.

## Failure Modes and Misconceptions

1. **Mark on dequeue:** multiple predecessors enqueue the same vertex.
2. **Non-FIFO buffer:** a stack, heap, or unordered pop policy invalidates the queue-order proof.
3. **Weighted overreach:** minimum hop count is reported as minimum unequal edge cost.
4. **Orientation loss:** an undirected representation is assumed for a directed contract.
5. **Wrong pull adjacency:** outgoing neighbors of an undiscovered vertex reverse the intended traversal.
6. **Dangling neighbor:** an unknown vertex is silently invented or ignored.
7. **Stale metadata:** distance or parent data from an earlier search masquerades as current.
8. **Generation wraparound:** an old stamp becomes equal to a reused search identifier.
9. **Invalid root state:** a source retains a nonroot parent or nonzero distance.
10. **Parent without edge:** a stored predecessor is not adjacent in the effective graph.
11. **Same-level parent:** a parent edge fails to reduce the level by one.
12. **Incomplete closure:** a reachable outgoing edge leads to a vertex labeled unreachable.
13. **Queue overflow as absence:** resource exhaustion becomes a false no-path answer.
14. **Cancellation as completion:** partial frontiers are published as a full traversal.
15. **Radius ambiguity:** stopping at depth $r$ is confused with proving nothing exists beyond $r$.
16. **Target-exit overclaim:** reaching one target is reported as complete level or graph coverage.
17. **Single-component overclaim:** one source is claimed to traverse a disconnected graph.
18. **Directed forest confusion:** an outer BFS forest is called a strongly connected decomposition.
19. **Discovery-order mythology:** one incidental adjacency order is presented as the unique BFS order.
20. **Parent-race nondeterminism:** an arbitrary atomic winner violates a canonical-output promise.
21. **Local-minimum confusion:** smallest immediate parent is assumed to yield the smallest full path.
22. **All-path explosion:** a compact predecessor DAG is expanded without output bounds.
23. **Duplicate-edge side effects:** parallel edges repeat callbacks that were promised once per vertex.
24. **Self-loop defect:** a self-loop changes distance or causes a duplicate claim.
25. **Dense-clear dominance:** every search clears $|V|$ metadata for a tiny reached set.
26. **Matrix on sparse data:** quadratic scans hide behind the phrase constant-time adjacency.
27. **Conversion blindness:** CSR, transpose, relabeling, or bitmap conversion is excluded from paid cost.
28. **Frontier-count heuristic:** push/pull switches by vertices while ignoring incident edges.
29. **Threshold universalism:** constants tuned on one graph family are treated as a theorem.
30. **Unbalanced frontier work:** equal vertex chunks strand workers behind hubs.
31. **Non-atomic claim:** check-then-set races publish a vertex more than once.
32. **Visibility gap:** a frontier identity becomes visible before its level and parent.
33. **Barrier removal without proof:** next-level vertices expand while shorter claims remain possible.
34. **Lost distributed candidate:** deduplication or retry logic deletes the only discovery message.
35. **Local termination:** empty queues on some owners are mistaken for global completion.
36. **Checkpoint mismatch:** visited state, frontier, parents, or pending messages come from different levels.
37. **Snapshot mixture:** adjacency reads from different graph revisions create no coherent result.
38. **Partial-store absence:** unavailable remote adjacency is treated as an empty neighbor list.
39. **Throughput substitution:** a high TEPS number is called low application latency.
40. **Weak validation:** testing only sample paths misses global edge and coverage violations.

## Worked Examples

### Example 1

**Question:** Trace deterministic BFS from $s$ when sorted outgoing adjacency is $s:(a,b)$, $a:(c,d)$, $b:(d)$, $c:(t)$, $d:(t)$, and $t:()$.

**Reasoning:** Start with queue $[s]$. Expanding $s$ claims $a,b$, producing $[a,b]$. Expanding $a$ claims $c,d$, producing $[b,c,d]$. Expanding $b$ sees $d$ already claimed. Expanding $c$ claims $t$; expanding $d$ sees $t$ already claimed.

The levels are

$$
L_0=\{s\},\quad
L_1=\{a,b\},\quad
L_2=\{c,d\},\quad
L_3=\{t\}.
$$

Parents are $p(a)=p(b)=s$, $p(c)=p(d)=a$, and $p(t)=c$ under this order.

**Engineering conclusion:** Claiming at enqueue makes the trace and one-parent callbacks unique. A different valid neighbor order can change parents without changing levels.

### Example 2

**Question:** Can labels $d(s)=0$, $d(a)=1$, $d(b)=1$, and $d(c)=3$ be valid if edges include $(s,a)$, $(s,b)$, and $(a,c)$?

**Reasoning:** Edge $(a,c)$ requires

$$
d(c)\le d(a)+1=2.
$$

The proposed label 3 violates the edge inequality. Even if $c$ has a parent chain of length 3 through other vertices, the direct two-edge path $s,a,c$ proves a shorter route.

**Engineering conclusion:** Parent replay alone proves that labels are achievable; scanning every effective edge is what detects an overlooked shorter path.

### Example 3

**Question:** What happens if $r$ vertices at one level all point to previously unseen vertex $x$ and discovery is marked only when $x$ is dequeued?

**Reasoning:** Each predecessor observes $x$ as unseen and enqueues it, so the queue receives $r$ copies. With mark-on-enqueue, the first predecessor claims $x$ and the remaining $r-1$ inspections lose harmlessly. In layered fan-in graphs, repeated duplicate publication can multiply across levels if duplicate dequeues also expand.

**Engineering conclusion:** The visited transition is a work and capacity invariant, not merely a final-answer detail. In parallel code it needs one atomic claim owner.

### Example 4

**Question:** Compare CSR and matrix storage for $n=100{,}000$ vertices and $m=600{,}000$ directed adjacency entries.

**Reasoning:** With 64-bit offsets and 32-bit neighbor identifiers, basic CSR payload is

$$
(100{,}000+1)\cdot8
+600{,}000\cdot4
=3{,}200{,}008\text{ bytes},
$$

about 3.05 MiB before alignment and metadata. A bit matrix needs

$$
100{,}000^2\text{ bits}
=1{,}250{,}000{,}000\text{ bytes},
$$

about 1.16 GiB; a byte matrix needs 10 GB decimal. If all vertices are reached, CSR inspects 600,000 neighbor entries, whereas ordinary matrix row scans inspect $10^{10}$ positions.

**Engineering conclusion:** The same abstract $\Theta(n+m)$ BFS claim applies only when the representation enumerates existing neighbors rather than all possible pairs.

### Example 5

**Question:** In directed graph $s\to a\to t$, can pull from frontier $\{a\}$ discover $t$ by scanning $t$'s outgoing neighbors?

**Reasoning:** No. Vertex $t$ has no outgoing neighbor, yet it is reachable from $a$. Pull must ask whether

$$
N^-(t)\cap\{a\}\ne\varnothing.
$$

Because $a\in N^-(t)$, it discovers $t$. Scanning $N^+(t)$ would instead test whether $t$ points toward the frontier.

**Engineering conclusion:** An undirected implementation can hide orientation errors because incoming and outgoing sets coincide. Validate with asymmetric directed fixtures.

### Example 6

**Question:** Frontier vertices $a$ and $b$ both have edges to unseen $v$. What may a parallel BFS publish?

**Reasoning:** Either atomic claim may win. Both give $d(v)=d(a)+1=d(b)+1$, so either parent is distance-correct. If the contract says “any shortest path,” the race is admissible. If the contract says the smaller parent under $a\prec b$, a winner-takes-all claim can violate it.

**Engineering conclusion:** Keep the fast distance claim, then select

$$
p(v)=\min_{\prec}\{u:(u,v)\in E\land d(u)+1=d(v)\}
$$

in a deterministic pass, or prove an equivalent online reduction.

### Example 7

**Question:** What levels result on a $5$ by $5$ four-neighbor grid with sources at opposite corners $(0,0)$ and $(4,4)$?

**Reasoning:** For cell $(i,j)$,

$$
d(i,j)
=
\min(i+j,\ 8-i-j).
$$

The level sizes are 2, 4, 6, 8, and 5 for levels 0 through 4, totaling 25 cells. The five cells with $i+j=4$ are equally distant from both sources.

**Engineering conclusion:** Multi-source BFS computes nearest-source hop distance in one run. Ownership of the middle diagonal still needs a declared source tie rule.

### Example 8

**Question:** Why can bidirectional BFS help in an ideal tree with branching factor 10 and source-target distance 6?

**Reasoning:** A one-sided complete expansion through depth 6 can contain

$$
\sum_{i=0}^{6}10^i
=1{,}111{,}111
$$

vertices. Two symmetric expansions through depth 3 contain about

$$
2\sum_{i=0}^{3}10^i
=2{,}222
$$

vertices, roughly 500 times fewer.

**Engineering conclusion:** This is an idealized regime calculation, not a universal bound for arbitrary graphs. Reverse adjacency, duplicate states, asymmetric branching, joining, and a sound lower-bound stopping test remain necessary.

### Example 9

**Question:** A frontier has 100,000 vertices of average outgoing degree 20. Only 50,000 vertices remain unseen, and each pull scan finds a frontier predecessor within its first four incoming checks. Which direction has the lower edge-inspection estimate?

**Reasoning:** Push estimates

$$
100{,}000\cdot20=2{,}000{,}000
$$

edge inspections. Pull needs at most $50{,}000\cdot4=200{,}000$ under the stated ordering, ten times fewer. Later, if the frontier shrinks to 100 vertices at degree 20 while 40,000 unseen vertices need 50 incoming checks on average, push estimates 2,000 and pull 2,000,000.

**Engineering conclusion:** Direction is a per-level policy driven by incident work and early-hit behavior. Vertex density alone is an incomplete feature.

### Example 10

**Question:** Edges are $s\to t$ of cost 10, $s\to a$ of cost 1, and $a\to t$ of cost 1. What does BFS return for $t$?

**Reasoning:** BFS minimizes edge count and discovers $t$ directly at level 1. That path costs 10. The two-edge path through $a$ costs 2 and is the minimum-cost route.

**Engineering conclusion:** The BFS result is correct for hop distance and wrong for unequal-weight distance. Use a nonnegative weighted shortest-path algorithm for the cost contract; do not alter BFS's visited rule and hope weights work.

## Cross-Program Connections

- [Theory of Computation & Complexity](../../15-theory-of-computation-and-complexity/ROADMAP.md) supplies graph reachability, reductions, lower bounds, and state-space models.
- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) owns queues, bitmaps, hash sets, CSR-style layouts, compressed representations, and concurrent discovery maps.
- [Database Engineering](../../18-database-engineering/ROADMAP.md) connects BFS to recursive queries, graph storage, external joins, snapshots, and cost-based execution.
- [Computer Architecture](../../23-computer-architecture/ROADMAP.md) explains cache misses, bandwidth, atomics, SIMD bitmaps, GPU execution, and NUMA effects.
- [Concurrent & Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) supplies linearization points, memory visibility, barriers, work partitioning, and deterministic reductions.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies ownership, message delivery, termination, checkpoints, global validation, and atomic publication.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) supplies authorization-aware graph filtering, adversarial resource limits, isolation, and fail-closed incomplete status.
- [API & Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) owns pagination, cancellation, versioned result contracts, idempotent jobs, and observability at the traversal boundary.

## References

1. Edward F. Moore. [*The Shortest Path Through a Maze*](https://books.google.com/books/about/The_Shortest_Path_Through_a_Maze.html?id=IVZBHAAACAAJ), in *Proceedings of an International Symposium on the Theory of Switching*, Part II, 1959, pp. 285–292. Foundational shortest-path wave exploration.
2. C. Y. Lee. [“An Algorithm for Path Connections and Its Applications”](https://doi.org/10.1109/TEC.1961.5219222), *IRE Transactions on Electronic Computers* 10(3), 1961, pp. 346–365. Primary wavefront routing treatment and early engineering application.
3. Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein. [*Introduction to Algorithms*, fourth edition](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/), MIT Press, 2022. Authoritative sequential BFS, shortest-path, predecessor, and complexity foundations.
4. Jeff Erickson. [*Algorithms*](https://jeffe.cs.illinois.edu/teaching/algorithms/), self-published open textbook, 2019. Proof-oriented graph traversal and shortest-path treatment.
5. Boost Contributors. [“Breadth-First Search”](https://www.boost.org/doc/libs/latest/libs/graph/doc/html/graph/algorithms/traversal/breadth_first_search.html), Boost.Graph documentation, consulted 2026-09-05. Current generic buffer, visitor, color-map, and complexity contract.
6. Graph500 Steering Committee. [*Graph500 Benchmark Specification*](https://graph500.org/?page_id=12), Version 2.0, 2017; consulted 2026-09-05. Official BFS kernel, validation, and traversed-edge performance specification.
7. Scott Beamer, Krste Asanović, and David Patterson. [“Direction-Optimizing Breadth-First Search”](https://www.scottbeamer.net/pubs/beamer-sc2012.pdf), SC12, 2012. Primary push-pull hybrid design and empirical evaluation.
8. Duane Merrill, Michael Garland, and Andrew Grimshaw. [“Scalable GPU Graph Traversal”](https://research.nvidia.com/publication/2012-02_scalable-gpu-graph-traversal), PPoPP 2012. Primary work-efficient GPU BFS and fine-grained load-balancing treatment.
9. Charles E. Leiserson and Tao B. Schardl. [“A Work-Efficient Parallel Breadth-First Search Algorithm”](https://doi.org/10.1145/1810479.1810534), SPAA 2010, pp. 303–314. Primary shared-memory parallel BFS analysis and implementation.
10. Julian Shun and Guy E. Blelloch. [“Ligra: A Lightweight Graph Processing Framework for Shared Memory”](https://jshun.csail.mit.edu/ligra.pdf), PPoPP 2013, pp. 135–146. Primary frontier abstraction and density-adaptive edge mapping.
11. Benjamin Brock et al. [*The GraphBLAS C API Specification*, Version 2.1.0](https://graphblas.org/docs/GraphBLAS_API_C_v2.1.0.pdf), GraphBLAS Forum, 2023. Official sparse linear-algebra API and BFS example.
12. Scott Beamer, Krste Asanović, and David Patterson. [“The GAP Benchmark Suite”](https://arxiv.org/abs/1508.03619), 2015; [reference implementation](https://github.com/sbeamer/gapbs). Primary standardized graph-kernel workloads, methodology, and direction-optimizing BFS baseline.
13. Adam L. Buchsbaum, Michael Goldwasser, Suresh Venkatasubramanian, and Jeffery R. Westbrook. [“On External Memory Graph Traversal”](https://doi.org/10.1145/338219.338650), SODA 2000, pp. 859–860. Primary external-memory directed BFS and undirected traversal results.

## Exercises

### Exercise 1

Run deterministic single-source BFS from $s$ over the directed graph with vertices $\{s,a,b,c,d,e,t,z\}$ and edges

$$
(s,b),(s,a),(a,c),(a,d),(b,c),(b,e),(c,t),(d,t),(e,d).
$$

Neighbors are inspected in alphabetical order. Give every distance, frontier, and parent. Show the queue after each expansion. If the implementation stops when $t$ is first discovered, state exactly what is and is not complete.

### Exercise 2

Prove that roots, parent-level edges, and the directed edge inequality form an exact completed BFS certificate when the validator sees every effective outgoing edge. Then give the smallest counterexample you can find showing why parent chains alone do not prove shortest distances.

### Exercise 3

A static directed graph has 50 million vertices and 400 million adjacency entries. Estimate basic storage for:

- CSR with 64-bit offsets and 32-bit neighbor identifiers;
- one 32-bit distance per vertex;
- one 64-bit parent per vertex;
- one visited bitmap and one dense-frontier bitmap.

Report decimal bytes and GiB. Then calculate the size of a one-bit adjacency matrix and the additional payload of a same-format reverse CSR. State at least five important peak-memory costs omitted by these payload estimates and decide which representation supports ordinary push and correct directed pull.

### Exercise 4

A parallel implementation checks a non-atomic visited byte, appends a candidate to the next frontier, then attempts an atomic claim. It lets workers begin expanding the next frontier immediately, uses outgoing adjacency for pull on a directed graph, switches direction when frontier vertex count exceeds ten percent of $|V|$, returns arbitrary atomic-winner parents despite a minimum-parent contract, and maps cancellation to unreachable. Diagnose each defect and design a safe level-synchronous direction policy.

### Exercise 5

Transfer BFS to an unfamiliar production constraint. A nightly immutable package-dependency snapshot has 800 million package vertices and 6 billion directed records $(x,y)$ meaning package $x$ depends directly on package $y$. Data is sharded across 64 workers. Given 50,000 compromised packages, output for every transitively affected package its minimum number of reverse-dependency hops and the smallest package-identifier predecessor among all valid previous-level predecessors. Results must be exact for one snapshot, resumable after worker loss, and never published as complete when a shard is unavailable.

Select and justify an algorithm and data layout. Compare at least two alternatives. Define direction, ownership, tie handling, communication, checkpoints, validation, publication, metrics, and failure status.

## Answers to the Exercises

### Answer 1

Alphabetical adjacency is:

$$
s:(a,b),\quad
a:(c,d),\quad
b:(c,e),\quad
c:(t),\quad
d:(t),\quad
e:(d).
$$

Start by claiming $s$:

| Expanded vertex | Newly claimed | Queue after expansion |
|---|---|---|
| none | $s$ | $[s]$ |
| $s$ | $a,b$ | $[a,b]$ |
| $a$ | $c,d$ | $[b,c,d]$ |
| $b$ | $e$ | $[c,d,e]$ |
| $c$ | $t$ | $[d,e,t]$ |
| $d$ | none; $t$ is seen | $[e,t]$ |
| $e$ | none; $d$ is seen | $[t]$ |
| $t$ | none | $[]$ |

Thus

$$
L_0=\{s\},\quad
L_1=\{a,b\},\quad
L_2=\{c,d,e\},\quad
L_3=\{t\}.
$$

The isolated vertex $z$ has distance $\infty$. The finite labels and parents are

| Vertex | Distance | Parent |
|---|---:|---|
| $s$ | 0 | root |
| $a$ | 1 | $s$ |
| $b$ | 1 | $s$ |
| $c$ | 2 | $a$ |
| $d$ | 2 | $a$ |
| $e$ | 2 | $b$ |
| $t$ | 3 | $c$ |
| $z$ | $\infty$ | none |

Stopping when $c$ discovers $t$ proves the displayed $s$-to-$t$ path has minimum hop count and that every already claimed vertex has its final distance. It does not complete expansion of $d$, $e$, or $t$, does not prove full reachable-set coverage if those vertices have additional outgoing edges, does not complete an edge-event stream, and does not justify a full distance map. The result status can be complete for the one-target path contract and incomplete for whole-graph traversal.

### Answer 2

Let $S$ be the roots. Parent conditions give every finite nonsource $v$ a parent with a real edge and label one smaller. Labels are nonnegative integers, so repeated parents terminate at a level-zero root and form a path of length $d(v)$. Therefore

$$
\delta_S(v)\le d(v).
$$

For any directed source-to-$v$ path $x_0,x_1,\ldots,x_\ell$, the root condition gives $d(x_0)=0$. Repeatedly applying the edge inequality gives

$$
d(x_i)\le d(x_{i-1})+1\le i.
$$

Hence $d(v)\le\ell$. Minimize over all such paths to obtain $d(v)\le\delta_S(v)$. The two inequalities prove equality for every finite vertex.

Coverage follows from complete outgoing-edge validation. If a reachable vertex were omitted, choose the first omitted vertex on a path from a source. Its predecessor has a finite label, so the validator's closure and edge check require the omitted vertex to have a finite label, a contradiction. Parent descent also prevents cycles.

For a counterexample to parent-only validation, use edges

$$
(s,a),\quad(a,v),\quad(s,v).
$$

Labels $d(s)=0$, $d(a)=1$, $d(v)=2$ with parents $p(a)=s$ and $p(v)=a$ have valid parent chains, yet the direct edge $(s,v)$ proves $\delta(s,v)=1$. The edge inequality on $(s,v)$ rejects $2\le1$.

### Answer 3

CSR offsets require

$$
(50{,}000{,}000+1)\cdot8
=400{,}000{,}008\text{ bytes}.
$$

Neighbor identifiers require

$$
400{,}000{,}000\cdot4
=1{,}600{,}000{,}000\text{ bytes}.
$$

The basic forward CSR payload is therefore 2,000,000,008 bytes. Distances add 200,000,000 bytes and parents add 400,000,000 bytes. Each bitmap needs

$$
\frac{50{,}000{,}000}{8}
=6{,}250{,}000\text{ bytes},
$$

so two add 12,500,000 bytes. The stated total is

$$
2{,}612{,}500{,}008\text{ bytes}
\approx2.43\text{ GiB}.
$$

A one-bit adjacency matrix needs

$$
\frac{(50{,}000{,}000)^2}{8}
=312{,}500{,}000{,}000{,}000\text{ bytes},
$$

or 312.5 TB decimal, about 284.2 TiB. A reverse CSR with the same widths adds another 2,000,000,008 bytes, bringing the listed dual-orientation payload and metadata to 4,612,500,016 bytes, about 4.30 GiB.

Omitted peak costs include allocator and alignment overhead, graph labels and edge properties, sparse frontier arrays, current and next frontier coexistence, duplicate candidate buffers, thread-local queues, sort or prefix-sum scratch, atomic-width padding, NUMA replication, input parsing buffers, reverse-index construction, validation state, checkpoints, and runtime bookkeeping. A sparse frontier containing every vertex would itself need 200,000,000 bytes with 32-bit identifiers.

Forward CSR supports push over outgoing edges. Correct directed pull needs reverse CSR or another complete incoming-edge index. Keeping both may be justified for repeated direction-optimized searches; otherwise its build time and roughly 2.0 GB decimal payload must enter the decision.

### Answer 4

The initial visited-byte read races and cannot authorize publication. Appending before a successful claim puts duplicates and possibly unowned parent data into the frontier. Reverse the order: attempt one atomic undiscovered-to-$k+1$ transition first, publish level and the permitted parent under a specified visibility relation, then append exactly once for the winning claim. A thread-local candidate scheme may publish duplicates temporarily only if a later owner-side reduction is explicit and callbacks do not treat them as unique vertices.

Immediate next-frontier expansion destroys the ordinary level proof. Complete every worker's level-$k$ edge work, reconcile claims and parent reductions, finalize $F_{k+1}$, and establish a barrier or equivalent distributed termination event before expanding it.

Directed pull must inspect incoming adjacency of each undiscovered vertex. Outgoing adjacency computes reverse reachability. Build and version a reverse representation, restrict pull to undirected graphs, or remain in push.

The ten-percent vertex threshold ignores degree and hit probability. Estimate at least current frontier incident edges, remaining incident edges, undiscovered vertices, frontier representation, conversion cost, and measured early-exit behavior. Use hysteresis so small measurement noise does not switch kernels repeatedly. Treat the threshold as versioned regime policy and preserve a correct push fallback.

An arbitrary claim winner cannot satisfy minimum-parent output. Either atomically reduce all level-$k$ predecessor identifiers before finalizing the level or compute minimum qualifying incoming predecessor after distances are fixed. Test ties under forced schedules.

Cancellation is incomplete. Return reached labels only under an explicitly partial contract, retain no unreachable claims for unexplored state, and prevent complete publication.

A safe level loop is:

1. freeze current frontier $F_k$ and effective snapshot;
2. choose push or pull using available cost features and a correctness-admissible representation;
3. generate candidates only from level $k$ to unseen vertices;
4. claim levels atomically and collect all data needed by the parent tie rule;
5. reconcile worker state and finalize deterministic parents;
6. validate frontier uniqueness, level, and ownership invariants;
7. persist a completed-level checkpoint if required;
8. publish $F_{k+1}$ to expansion only after global completion.

### Answer 5

The requested relation runs opposite the stored dependency edge. Record $(x,y)$ says $x$ depends on $y$; if $y$ is compromised, $x$ is one reverse-dependency hop away. Build a snapshot-bound reverse CSR or distributed incoming index whose effective edge is $y\to x$. Validate that every source record is represented exactly once in the derived orientation.

Run one distributed multi-source level-synchronous BFS with all 50,000 compromised packages at level zero. Partition vertex ownership by a stable function or balanced range. Owners hold visited distance, current parent candidate, reverse adjacency for owned expansion, and frontier state. Push expands affected packages along dependency-to-dependent edges. Remote dependent candidates are batched by owner, compressed if worthwhile, and deduplicated at the receiver.

For a newly reached $v$ at level $k+1$, every candidate $u$ from level $k$ is semantically valid. Because the output requires the smallest package identifier, do not finalize the first message's parent. Reduce all same-level candidates with minimum, then close the level after every sender and receiver agrees that level-$k$ messages are complete. The result is

$$
p(v)
=
\min\{u:(u,v)\in E_{\mathrm{reverse}}\land d(u)+1=d(v)\}.
$$

Direction optimization is optional. Push is the simple exact baseline. Pull can help when the frontier is broad, but it would scan still-unaffected packages and needs the original stored direction $x\to y$ to ask whether package $x$ depends on a current-frontier package $y$. Both orientations must be bound to the same snapshot, and the switch must occur only between completed levels.

Fifty thousand independent BFS runs repeat edge work, require an expensive per-vertex minimum reduction, and make deterministic provenance harder. An asynchronous propagation system might reduce barriers, but first-arrival distance and parent are unsafe under reordering unless it implements monotone relaxation, quiescence detection, and final minimum-parent reduction. A centralized queue cannot hold the graph or absorb hub traffic. Algebraic distributed BFS is an admissible alternative if its matrix orientation, mask, parent reduction, and communication behavior implement the same contract.

Checkpoint only completed levels. A checkpoint binds:

- snapshot and reverse-index digests;
- source-set digest and ordering;
- ownership map and worker topology;
- completed level $k$;
- visited distances through $k$;
- finalized parents through $k$;
- the exact next frontier or a reproducible derivation;
- message sequence or reconciliation evidence;
- implementation and schema versions.

After worker loss, discard uncommitted next-level effects or replay them idempotently. A shard unavailable during expansion or validation makes the run incomplete; an empty response is not accepted as empty adjacency.

Validation checks source roots, parent membership in the reverse graph, parent level differences, every reverse edge's distance inequality from finite tails, coverage across all 64 shards, absence of cycles by decreasing levels, deterministic minimum parents among all previous-level incoming candidates, numeric bounds, counts, checksums, and snapshot identity. Use small snapshots with an independent in-memory oracle, then validate the full certificate in distributed scans.

Measure per level: frontier vertices and edges, local and remote candidates, duplicate ratio, bytes by destination, hot-owner skew, compute and wait time, checkpoint bytes, push/pull mode, parent-reduction work, reverse-index construction, validation, restart, and end-to-end publication latency. Retain failures and retries.

Write immutable result and evidence objects under a new generation. Atomically activate them only after every owner reports terminal coverage, messages reconcile, the last frontier is empty, validation passes, and source and snapshot digests match. Preserve the previous generation on failure. The published status is complete only for that exact nightly snapshot and source set.
