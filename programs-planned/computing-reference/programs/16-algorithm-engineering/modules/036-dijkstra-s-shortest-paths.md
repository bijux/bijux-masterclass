---
module_id: ALGE-036
program: Algorithm Engineering
level: 1
module_number: 36
title: Dijkstra's Shortest Paths
status: complete
last_verified: 2026-09-05
---

# Dijkstra's Shortest Paths

## One-Page Review

### Governing question

How can we compute minimum additive path costs from one source in a weighted directed or undirected graph, prove when a tentative label becomes final, and reject weight, arithmetic, representation, or lifecycle conditions that invalidate the label-setting argument?

### Essential definitions

- A **walk** follows edges and may repeat vertices; a **path** has no repeated vertices.
- Path weight is the sum of its edge weights under a declared arithmetic policy.
- The **shortest-path distance** $\delta(s,v)$ is the minimum weight of any path from source $s$ to $v$, or infinity if none exists.
- A **distance label** $d[v]$ is a current upper bound on $\delta(s,v)$.
- **Relaxation** of edge $u\to v$ tests whether $d[u]+w(u,v)$ improves $d[v]$.
- A vertex is **settled** when the algorithm has proved its label final.
- The **frontier** contains discovered but unsettled vertices keyed by tentative distance.
- A **predecessor map** records one selected shortest-path witness, not every shortest path.
- A **stale heap entry** is an older key superseded by a smaller current label.
- A **shortest-path tree** minimizes source-to-vertex path weights; it is not a minimum spanning tree.
- A **label-setting** algorithm finalizes a vertex once; a **label-correcting** algorithm may revise labels repeatedly.

### Central model, mechanism, or theorem

For a finite graph with nonnegative edge weights, Dijkstra initializes $d[s]=0$, all other labels to infinity, and repeatedly settles the unsettled vertex $u$ with minimum tentative label. It relaxes every outgoing edge:

$$
d[v]\leftarrow\min\bigl(d[v],d[u]+w(u,v)\bigr).
$$

At selection time, $d[u]=\delta(s,u)$. Suppose a shorter path to $u$ existed. On that path, let $y$ be the first unsettled vertex and $x$ its settled predecessor. Relaxing $x\to y$ established $d[y]\le\delta(s,y)$. Nonnegative remaining edges give $\delta(s,y)\le\delta(s,u)<d[u]$, contradicting that $u$ had minimum tentative label.

With adjacency lists and a binary heap using duplicate insertions, runtime is $O((n+m)\log n)$ and auxiliary label, predecessor, settled, and heap state is $O(n+m)$ in the worst case. Indexed heaps can bound queue occupancy differently. Dense-array selection takes $O(n^2)$ and may suit dense graphs.

### Critical invariants

- The vertex universe, directedness, logical edges, source, weight domain, arithmetic, tie policy, and graph snapshot are fixed.
- Every edge weight is nonnegative; zero weights are valid.
- $d[s]=0$ and each finite label equals the weight of an actual discovered source path.
- Therefore $d[v]\ge\delta(s,v)$ whenever $\delta$ is defined.
- Every settled vertex has final label $d[v]=\delta(s,v)$.
- The heap exposes a minimum current unsettled label; stale or already-settled entries are discarded.
- Relaxation uses checked addition and compares values in a coherent total order.
- A predecessor changes only with a strict improvement under the basic contract, preventing tie rewrites from creating witness cycles.
- Unreachable vertices remain explicitly infinite and have no predecessor path.
- Early target exit is valid only when the target is settled, not merely discovered.
- Output is bound to one graph and weight snapshot and published only after certificate validation.

### Common failures

Frequent failures include accepting a negative edge; treating discovery as finalization; stopping when the target first enters the heap; using FIFO order on unequal weights; selecting stale heap entries; confusing the algorithm with breadth-first search, Prim, or A*; overflowing `d[u] + w`; letting NaN enter comparisons; using an inadequate infinity sentinel; losing zero-weight edges in a matrix where zero means “absent”; constructing predecessor cycles through equal-distance rewrites; omitting isolated or target-only vertices; silently symmetrizing direction-dependent edges; mixing units; mutating weights during the run; returning a partial distance map as complete; and claiming a shortest route when the modeled scalar cost omits constraints or time dependence.

### Compact example

For edges $s\to a$ of weight $4$, $s\to b$ of weight $1$, and $b\to a$ of weight $2$, discovery first gives $d[a]=4$ and $d[b]=1$. Settling $b$ relaxes $a$ to $3$. The path $s\to b\to a$ is shorter than the direct edge. Stopping when $a$ was first discovered would return the wrong answer.

### Connections

[ALGE-002](./002-preconditions-postconditions-and-correctness.md) supplies contract reasoning, [ALGE-003](./003-loop-invariants-for-algorithm-correctness.md) supplies invariants, [ALGE-011](./011-linear-and-binary-search.md) supplies ordered selection ideas, [ALGE-031](./031-breadth-first-search.md) supplies the equal-weight special case, and [ALGE-035](./035-minimum-spanning-trees.md) distinguishes total connecting weight from source distance. [ALGE-037](../ROADMAP.md#block-04--graph-algorithms) next handles negative weights with Bellman–Ford.

## Governing Question

Given a source and nonnegative additive edge weights, how should an implementation compute exact reachable distances and reconstruct valid shortest paths while making finalization, numeric behavior, tie policy, unreachable state, and graph identity explicit?

Dijkstra's algorithm is often summarized as “always visit the closest vertex.” That slogan omits the proof boundary. The chosen vertex is safe only because its label is the least unsettled upper bound and every untraversed edge adds a nonnegative amount. One negative edge destroys that argument even when the graph has no negative cycle.

The mathematical answer is a distance function. Production callers may also need a target path, all predecessor paths, counts, stable tie choices, an early-stop status, overflow evidence, or a certificate. Each output has its own completeness condition. A settled target supports one-target exit; a discovered target does not. A valid distance map does not prove that the graph included every real-world road or dependency.

Representation choices are observable. A duplicate-entry heap needs stale-key rejection. An indexed heap needs correct decrease-key positions. A matrix may conflate zero weight with no edge. Floating addition can overflow or round. A route graph can change while processing. The proof applies to the effective graph and arithmetic actually used.

## Why This Matters

Single-source shortest paths support routing, dependency costs, game movement, static analysis, geographic systems, scheduling subproblems, graph databases, and many optimization routines. They also teach a fundamental pattern: maintain feasible upper bounds, prove a greedy finalization event, and expose the exact assumption that makes it irreversible.

Dijkstra is the right baseline when weights are nonnegative and additive. When all weights are equal, BFS is simpler. When negative weights exist, Bellman–Ford or another appropriate method is required. On a DAG, topological relaxation is linear even with negative edges. For one target with an admissible consistent heuristic, A* can reduce explored work. The problem structure chooses the algorithm.

The distinction from minimum spanning trees matters. Prim and Dijkstra can look nearly identical with a heap, but Prim keys a vertex by the lightest single crossing edge; Dijkstra keys it by total source-path weight. An MST can give poor source distances, and a shortest-path tree can have nonminimum total edge weight.

Current libraries expose implementation-specific contracts. Boost.Graph 1.92.0 documents nonnegative weights, customizable maps and combine/compare operations, and $O(V\log V+E)$ for its documented heap route. SciPy 1.18.0 documents sparse-matrix conversions, multiple-source shapes, method selection, and limitations for direction-dependent distances when `directed=False`. These facts are current API evidence, not changes to the theorem.

## Prerequisites and Retrieval

Retrieve:

- finite directed and undirected graphs, walks, paths, cycles, reachability, adjacency, and graph snapshots;
- edge weights, additive path cost, total orders, exact integers, floating values, infinity, overflow, and units;
- priority queues, binary heaps, indexed heaps, duplicate insertions, maps, arrays, and stable identities;
- BFS, relaxation, triangle inequalities, induction, contradiction, upper bounds, and loop variants;
- asymptotic work, auxiliary space, sparse and dense representations, cache behavior, and output cost;
- predecessor trees, path reconstruction, cycle detection, and independent validation;
- immutable snapshots, cancellation, checkpointing, deterministic ties, and atomic publication;
- property, differential, metamorphic, exhaustive, adversarial, and fault-injection testing.

You should be able to explain why a known path provides an upper bound on the unknown shortest distance and why nonnegative suffixes preserve ordering.

## Learning Objectives

After completing this module, you should be able to:

1. specify single-source shortest paths over a precise graph, weight, arithmetic, source, and output contract;
2. derive relaxation and prove the distance-label upper-bound invariant;
3. prove Dijkstra's minimum-label finalization theorem under nonnegative weights;
4. construct counterexamples for negative edges, premature target exit, stale entries, and overflow;
5. implement deterministic Dijkstra with duplicate heap entries and checked predecessor reconstruction;
6. validate distances through source, predecessor, reachability, and edge inequalities;
7. compare dense arrays, binary heaps, indexed heaps, buckets, BFS, DAG relaxation, Bellman–Ford, and A*;
8. handle zero weights, parallel edges, equal shortest paths, unreachable vertices, and isolated sources;
9. govern numeric types, infinity sentinels, units, snapshots, cancellation, checkpoints, and publication;
10. distinguish mathematical path optimality from route feasibility and domain-model completeness.

## Core Exposition

### Specify the effective weighted graph

Declare $G=(V,E,w)$, source $s\in V$, directedness, logical edge identity, endpoint policy, and one immutable revision. Define whether parallel edges remain distinct. Self-loops of nonnegative weight cannot improve a strict label, but they remain input edges and may matter for provenance.

Define the weight algebra. The ordinary proof uses a zero value, addition, and a total comparison compatible with adding nonnegative weights. Common safe contracts include checked nonnegative integers and finite nonnegative decimal values. Floating values require explicit NaN rejection, infinity policy, rounding expectations, and a specified evidence standard.

Decide whether output includes:

- all distances or only one settled target;
- one predecessor per reachable non-source vertex;
- all equal-cost predecessors;
- paths materialized eagerly or reconstructed on demand;
- settlement order and trace evidence;
- unreachable vertices with infinity or omitted entries;
- a cutoff radius or resource-limited partial result;
- stable tie behavior across runs.

These choices affect storage, determinism, and completeness. A predecessor map for one chosen tree cannot answer how many shortest paths exist.

### Define distance and optimal substructure

For path $p=(v_0,\ldots,v_k)$, define

$$
w(p)=\sum_{i=0}^{k-1}w(v_i,v_{i+1}).
$$

The shortest-path distance is

$$
\delta(s,v)=\min\{w(p):p\text{ is a path from }s\text{ to }v\},
$$

with infinity when no path exists. Under nonnegative weights, removing a repeated cycle never increases path cost, so a simple shortest path exists for every reachable vertex in a finite graph.

Every prefix of a shortest path is shortest between its endpoints under the additive model. If a cheaper path to a prefix endpoint existed, substituting it would create a cheaper path to the final endpoint. This optimal-substructure fact supports predecessor witnesses and relaxation.

Shortest distances obey every edge inequality:

$$
\delta(s,v)\le\delta(s,u)+w(u,v).
$$

This is a directed triangle inequality: append edge $u\to v$ to a shortest path to $u$.

### Derive relaxation

Initialize $d[s]=0$ and $d[v]=\infty$ for $v\ne s$. A finite label always corresponds to a discovered path. Relaxing $u\to v$ computes candidate $d[u]+w(u,v)$. If smaller than $d[v]$, store it and set predecessor of $v$ to $u$.

Because every label is the weight of an actual path,

$$
d[v]\ge\delta(s,v).
$$

Relaxation preserves this upper-bound invariant: the new candidate is also an actual path. Labels decrease monotonically but never below the optimum. Once all edges of a known shortest path have been relaxed in order, its destination label equals the true distance.

Checked addition matters. If a fixed-width candidate wraps from a large positive number to a negative number, it is not the represented path sum and the invariant fails. Check before adding, use a wider accumulator, or use arbitrary precision.

### Prove greedy finalization

Let $S$ be settled vertices, each already satisfying $d[x]=\delta(s,x)$. Select unsettled $u$ with minimum finite $d[u]$. Suppose for contradiction that a path $p$ from $s$ to $u$ has weight less than $d[u]$.

On $p$, let $y$ be the first unsettled vertex and $x$ its preceding settled vertex. When $x$ was settled, edge $x\to y$ was relaxed. Because $d[x]=\delta(s,x)$ is no greater than the weight of the prefix of $p$ ending at $x$, relaxation gives

$$
d[y]\le d[x]+w(x,y)\le w(p[s\leadsto y]).
$$

All remaining edges from $y$ to $u$ are nonnegative, so

$$
d[y]\le w(p[s\leadsto y])\le w(p)<d[u].
$$

This contradicts selecting $u$ as the minimum-label unsettled vertex. Therefore $d[u]=\delta(s,u)$, and settlement is irreversible.

The proof permits zero weights. They can create equal-distance settlement choices but no cheaper path through a later vertex. It does not permit negative edges.

### Implement deterministic heap Dijkstra

This implementation accepts a complete vertex universe and directed edges with stable identities, requires exact nonnegative integers, uses duplicate heap entries with stale rejection, preserves deterministic adjacency and heap tie order, reconstructs witness paths, and independently validates the result.

<!-- bijux-verify: {"id":"deterministic-dijkstra","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"settled=('s', 'b', 'a', 'c', 'd')\ndistances=(('a', '3'), ('b', '1'), ('c', '4'), ('d', '7'), ('s', '0'), ('x', 'inf'))\npredecessors=(('a', 'b'), ('b', 's'), ('c', 'a'), ('d', 'c'), ('s', None), ('x', None))\npath_to_d=('s', 'b', 'a', 'c', 'd')\npath_to_x=None\nvalid=True\n","stderr":""}} -->
```python
import heapq
from math import inf


def normalize(vertices, edges):
    vertices = set(vertices)
    graph = {vertex: [] for vertex in vertices}
    seen = set()
    for edge_id, tail, head, weight in edges:
        if edge_id in seen:
            raise ValueError(f"duplicate edge identity: {edge_id}")
        if tail not in vertices or head not in vertices:
            raise ValueError(f"unknown endpoint: {edge_id}")
        if not isinstance(weight, int) or weight < 0:
            raise ValueError("weights must be nonnegative exact integers")
        seen.add(edge_id)
        graph[tail].append((head, weight, edge_id))
    return {vertex: tuple(sorted(outgoing))
            for vertex, outgoing in graph.items()}


def dijkstra(vertices, edges, source):
    graph = normalize(vertices, edges)
    if source not in graph:
        raise ValueError("source is outside the vertex universe")
    distance = {vertex: inf for vertex in graph}
    predecessor = {vertex: None for vertex in graph}
    distance[source] = 0
    heap = [(0, source)]
    settled = set()
    settled_order = []
    while heap:
        candidate, vertex = heapq.heappop(heap)
        if vertex in settled or candidate != distance[vertex]:
            continue
        settled.add(vertex)
        settled_order.append(vertex)
        for head, weight, _ in graph[vertex]:
            proposal = candidate + weight
            if proposal < distance[head]:
                distance[head] = proposal
                predecessor[head] = vertex
                heapq.heappush(heap, (proposal, head))
    return graph, distance, predecessor, tuple(settled_order)


def path_to(source, target, distance, predecessor):
    if distance[target] == inf:
        return None
    reversed_path = []
    seen = set()
    vertex = target
    while vertex is not None:
        if vertex in seen:
            raise ValueError("predecessor cycle")
        seen.add(vertex)
        reversed_path.append(vertex)
        if vertex == source:
            return tuple(reversed(reversed_path))
        vertex = predecessor[vertex]
    raise ValueError("finite label lacks a source predecessor chain")


def validate(graph, source, distance, predecessor):
    if distance[source] != 0 or predecessor[source] is not None:
        return False
    reachable = {source}
    stack = [source]
    while stack:
        vertex = stack.pop()
        for head, _, _ in graph[vertex]:
            if head not in reachable:
                reachable.add(head)
                stack.append(head)
    for vertex in graph:
        if (distance[vertex] < inf) != (vertex in reachable):
            return False
        if vertex != source and distance[vertex] < inf:
            parent = predecessor[vertex]
            if parent is None or not any(
                head == vertex and distance[parent] + weight == distance[vertex]
                for head, weight, _ in graph[parent]
            ):
                return False
            path_to(source, vertex, distance, predecessor)
        for head, weight, _ in graph[vertex]:
            if distance[vertex] < inf and distance[head] > distance[vertex] + weight:
                return False
    return True


vertices = {"s", "a", "b", "c", "d", "x"}
edges = (
    ("sa", "s", "a", 4), ("sb", "s", "b", 1),
    ("ba", "b", "a", 2), ("bc", "b", "c", 5),
    ("ac", "a", "c", 1), ("ad", "a", "d", 7),
    ("cd", "c", "d", 3), ("bd", "b", "d", 10),
)
graph, distance, predecessor, settled = dijkstra(vertices, edges, "s")
display = lambda value: "inf" if value == inf else str(value)
print(f"settled={settled}")
print(f"distances={tuple((v, display(distance[v])) for v in sorted(vertices))}")
print(f"predecessors={tuple((v, predecessor[v]) for v in sorted(vertices))}")
print(f"path_to_d={path_to('s', 'd', distance, predecessor)}")
print(f"path_to_x={path_to('s', 'x', distance, predecessor)}")
print(f"valid={validate(graph, 's', distance, predecessor)}")
```

The validator checks structural and optimality conditions without rerunning Dijkstra: reachability agrees with finite labels, every predecessor edge is tight, each finite chain reaches the source without cycling, and every edge satisfies the distance inequality. These conditions certify shortest distances under the same graph and arithmetic contract.

### Handle stale heap entries correctly

Python's standard heap has no indexed decrease-key. The implementation pushes a new `(distance, vertex)` pair whenever a label improves. Old entries remain. When popped, an entry is live only if its key equals the current label and the vertex is unsettled.

The heap can therefore contain $O(m)$ entries in a worst case even though only $n$ vertices settle. Runtime remains within the common $O((n+m)\log n)$ bound. An indexed heap keeps one position per vertex and supports decrease-key, typically limiting queue storage to $O(n)$ but increasing implementation complexity.

Tie tuples require comparable stable vertex keys. If domain vertex objects are not mutually comparable, include a monotonic insertion counter or stable canonical key. The counter makes a run deterministic only when discovery order is deterministic; a stable key supports cross-run reproducibility.

### Reconstruct paths without inventing witnesses

On strict improvement, set $\pi[v]=u$. For a reachable non-source vertex, the chosen predecessor edge must satisfy

$$
d[v]=d[\pi[v]]+w(\pi[v],v).
$$

Following predecessors should terminate at $s$. With strictly positive weights, distances strictly decrease backward. With zero-weight edges they need not, so careless equal-distance predecessor rewrites can create a cycle even while distance labels remain correct. The basic implementation relaxes only from settled vertices and updates predecessors only on strict improvement. Therefore a predecessor points to a vertex settled earlier; following settlement ranks backward is well-founded and every reachable chain ends at $s$.

If all shortest paths are required, store the predecessor relation containing every tight incoming edge after distances are final. Zero-weight tight edges can form cycles, so this relation is not necessarily a DAG. Counting shortest paths then needs additional assumptions or SCC treatment.

### Explain failure on negative edges

Take edges $s\to u$ of weight $2$, $s\to v$ of weight $5$, and $v\to u$ of weight $-10$. Dijkstra settles $u$ at distance $2$ before $v$. Later path $s\to v\to u$ has weight $-5$, contradicting finalization. A standard implementation that never reopens settled vertices returns the wrong result.

No negative cycle is needed. The proof fails because the unsettled suffix from $v$ to $u$ can reduce path weight; the first unsettled vertex no longer has a prefix no greater than the whole path.

Scanning reachable edges for negativity before running gives a clear failure but costs a graph pass. Rejecting during relaxation may discover the problem only after some labels were published internally. Never expose them as complete. The next module develops Bellman–Ford, which repeatedly corrects labels and detects reachable negative cycles.

### Support early exit and bounded search honestly

For one target $t$, stop when $t$ is extracted with its current minimum label and settled. At that moment the proof applies. Do not stop when $t$ is inserted or first relaxed: a later frontier vertex may yield a cheaper route.

For a distance radius $R$, once the minimum live heap key exceeds $R$, every unsettled reachable vertex has distance greater than $R$. Return settled distances within the radius and label others outside-bound or unknown according to contract. Resource cancellation is different: it may stop before the next minimum is known and yields an incomplete result.

Bidirectional Dijkstra can reduce exploration for one source-target query, but its stopping condition is not “frontiers meet.” It requires consistent forward/reverse weights, minimum frontier keys, a best complete path, and a proof that no unseen combination can improve it. Treat it as a separate algorithm.

### Choose the priority structure from weights and graph shape

- Linear scanning of unsettled labels gives $O(n^2+m)$ and predictable dense behavior.
- A binary heap gives common sparse-graph bounds and simple duplicate-entry implementations.
- An indexed heap supports decrease-key with $O(n)$ queue positions.
- Integer buckets can exploit bounded nonnegative integer weights; complexity depends on the maximum weight or distance range.
- Radix heaps exploit monotone extracted integer keys under a suitable machine model.
- Specialized parallel methods relax the globally sequential minimum requirement under different invariants.

Do not quote a priority-queue bound without its operations and key model. Fibonacci heaps provide attractive theoretical decrease-key bounds but pointer-heavy constants and locality can make other structures preferable in practice.

### Validate distances independently

A scalable certificate checks:

1. $d[s]=0$ and source predecessor policy;
2. unreachable labels agree with an independent reachability traversal;
3. every reachable non-source vertex has a valid tight predecessor edge;
4. predecessor chains reach $s$ without cycles;
5. every edge $u\to v$ with finite $d[u]$ satisfies $d[v]\le d[u]+w(u,v)$;
6. all additions and comparisons follow the declared numeric policy;
7. graph, weights, source, and output share a snapshot identifier.

Tight predecessor paths prove $d[v]$ is achievable, hence $\delta(s,v)\le d[v]$. Edge inequalities imply by induction over any source path that $d[v]\le$ its weight, hence $d[v]\le\delta(s,v)$. Together they prove equality.

For bounded graphs, enumerate simple paths or use Bellman–Ford as an independent oracle. Differentially comparing two heap implementations is weaker when they share parsing, arithmetic, or relaxation defects.

### Govern arithmetic and infinity

For unsigned or signed fixed-width integers, check `distance + weight` before addition. The infinity sentinel must exceed every representable valid path distance or be represented as a separate tagged state. A maximum integer used as both infinity and a valid distance is ambiguous.

Floating NaN breaks total comparison and must be rejected. Positive infinity may represent an unusable edge or unreachable state only under a declared policy. Rounding can make mathematically equal path sums compare differently; deterministic behavior requires fixed operation order and should not be confused with real-number exactness.

Weights must share meaning and units. Adding latency, price, risk, and hop count without a declared scalarization does not yield a meaningful shortest path. Lexicographic or multiobjective costs require compatible comparison and addition properties and often produce more than one nondominated label per vertex, outside ordinary Dijkstra.

### Preserve snapshots, cancellation, and publication

Changing an edge weight after its tail settles can invalidate every descendant label. Bind vertex enumeration, adjacency, weights, source, heap, labels, predecessors, validation, and result to one immutable or transactionally consistent graph revision.

A checkpoint records graph digest, source, arithmetic and tie policy, settled set, labels, predecessors, live and stale heap entries or enough state to rebuild them, adjacency cursor state if relaxation is interruptible, and output position. Validate finite-label witnesses and heap consistency before resuming.

Cancellation is neither unreachable nor complete. Return an explicit incomplete status and state exactly which vertices were settled under the pinned snapshot. Unless the API promises partial settled labels, quarantine the intermediate map. Publish status, distances, predecessor evidence, graph revision, source, numeric policy, and validator outcome atomically.

### Respect dynamic and time-dependent boundaries

Recomputing from a new snapshot is often safer than trying to repair labels after changes. Decreasing or inserting an edge can improve many descendants; increasing or deleting a predecessor-tree edge can invalidate a subtree but alternate equal paths may limit damage. Dynamic shortest paths require separate algorithms and update evidence.

Time-dependent routing needs an edge cost that depends on departure time. A label-setting method can work under the FIFO property—departing later cannot arrive earlier along the same edge—but ordinary static Dijkstra does not model this automatically. Negative effective costs, waiting, schedules, and multiple criteria need their own formulation.

### Test and operate the implementation

For small nonnegative graphs, enumerate simple paths and compare exact distances. Metamorphic properties include:

- bijective vertex renaming preserves mapped distances;
- permuting edge records changes no distances;
- adding an unreachable component changes no old distances;
- adding a nonnegative self-loop changes no distances;
- adding a dominated parallel edge changes no distances;
- multiplying all weights by a positive exact constant scales finite distances;
- adding a constant to every edge does **not** generally preserve shortest paths because paths have different edge counts;
- every returned predecessor edge is tight;
- decreasing one edge can never increase a distance;
- increasing one edge can never decrease a distance.

Inject unknown endpoints, missing source, negative edges, zero cycles, parallel ties, huge weights, integer overflow, NaN, infinity, stale heap entries, incomparable keys, allocation failure, callback failure, cancellation after every event, snapshot replacement, corrupt checkpoints, and output failure.

Observe vertices and logical edges, reachable and settled counts, relaxation attempts and successes, heap pushes, stale pops, maximum heap size, equal-distance alternatives, zero-weight edges, maximum finite distance, arithmetic rejections, adjacency and queue time, memory, cutoff exits, cancellations, snapshot age, validation time, and publication status.

## Definitions and Notation

Let $G=(V,E,w)$ be a finite directed graph; an undirected edge is represented by a contractually paired relation. Let $n=|V|$, $m=|E|$, and source $s\in V$.

- A **walk** follows directed edges and may repeat vertices.
- A **path** is a walk without repeated vertices.
- $w(p)$ is the additive weight of path $p$.
- $\delta(s,v)$ is the minimum source-to-$v$ path weight, or infinity when unreachable.
- $d[v]$ is a tentative distance label.
- $\pi[v]$ is the selected predecessor of $v$.
- **Relaxing** $u\to v$ applies $d[v]\leftarrow\min(d[v],d[u]+w(u,v))$ and updates evidence on strict improvement.
- $S$ is the settled vertex set.
- The **frontier** contains discovered vertices outside $S$ with finite labels.
- A **tight edge** satisfies $d[v]=d[u]+w(u,v)$.
- A **stale entry** has a key different from the vertex's current label or names an already-settled vertex.
- A **label-setting** algorithm settles each vertex at most once.
- A **label-correcting** algorithm may process improved labels repeatedly.
- A **shortest-path tree** is one predecessor tree whose root-to-vertex paths attain all finite distances.
- A **distance certificate** combines feasible tight paths with lower-bound edge inequalities.

The symbol infinity is a tagged unreachable value in the mathematical model, not necessarily the largest machine integer.

## Mechanisms, Invariants, or Proof Structure

### Initialization and relaxation obligations

Initially only $s$ has finite label, representing the empty path of weight zero. Each strict relaxation appends one edge to an already represented path, so every finite label remains achievable and is an upper bound on the optimum. Labels only decrease.

### Settlement obligations

Before extraction, the priority structure must identify a minimum current unsettled label. Stale entries are discarded. The contradiction proof selects the first unsettled vertex on a supposedly cheaper path and relies on its predecessor having been settled and relaxed. Nonnegative suffix weight is the exact premise that orders this prefix below the selected label.

### Predecessor obligations

Every reachable non-source predecessor edge exists and is tight. Chains are acyclic and terminate at $s$. Strict-improvement updates make witness history well founded even with zero-weight graph cycles. Alternative tie policies need an explicit acyclicity proof.

### Termination and complexity obligations

Each vertex settles at most once, so successful extractions are bounded by $n$. Each outgoing logical edge is relaxed once from its settled tail. In a duplicate-entry binary heap, every successful relaxation can push one entry, bounding pushes by $m+1$ and giving $O((n+m)\log n)$ time under comparison-heap costs.

### Certificate obligations

Tight source-rooted predecessor paths prove achievability. Edge inequalities prove no source path is cheaper by induction over path edges. Reachability identifies exactly which labels may be infinite. Snapshot and arithmetic binding ensure both sides describe the same problem.

## Alternatives and Trade-Offs

### Dijkstra versus BFS

BFS is Dijkstra specialized to equal unit weights, using a FIFO queue because discovery layers already order distance. Use BFS for unweighted hop count; a heap adds needless cost.

### Dijkstra versus Bellman–Ford

Dijkstra settles once and requires nonnegative weights. Bellman–Ford repeatedly corrects labels, handles negative edges, and detects reachable negative cycles at higher worst-case cost. Reject rather than silently choose when weight assumptions are unknown.

### Dijkstra versus DAG relaxation

A DAG permits one topological edge pass in $O(n+m)$ even with negative weights because dependencies never return. Detecting or knowing acyclicity can therefore beat heap ordering.

### Dijkstra versus A*

A* adds a heuristic lower bound toward one target. With appropriate admissibility and consistency it can settle less of the graph; with zero heuristic it reduces to Dijkstra. Heuristic computation, reopening policy, and stopping proof are additional obligations.

### Dense scan versus heap

Dense scanning gives predictable $O(n^2)$ behavior without stale entries. Heaps exploit sparse adjacency but add allocation and irregular access. Representation, density, and hardware measurements decide.

### Indexed heap versus duplicate insertion

Indexed heaps bound one queue position per vertex and provide decrease-key but maintain fragile position maps. Duplicate insertion is simple and robust but can retain $O(m)$ stale entries. Both need exact minimum-current-label semantics.

### One path versus all paths

One predecessor gives a compact witness. All tight predecessors expose alternatives but zero-weight cycles complicate counting and enumeration. Materializing every shortest path can be exponential in output.

## Failure Modes and Misconceptions

- **Negative-edge acceptance:** finalization can be invalid without any negative cycle.
- **Discovery equals settlement:** a first path need not be shortest.
- **Premature target exit:** stop only when the target is extracted with its live minimum key.
- **FIFO on unequal weights:** discovery layers no longer represent additive distance.
- **Stale-entry selection:** outdated keys can repeat work or violate finalization logic.
- **No settled guard:** zero cycles and duplicates can cause unnecessary processing or witness corruption.
- **Equal-distance predecessor rewrite:** tie updates can create predecessor cycles.
- **Overflowed addition:** wrapped candidates cease to represent path weights.
- **Sentinel collision:** a valid maximum-distance value can be mistaken for infinity.
- **NaN key:** comparisons no longer form a coherent total order.
- **Zero means absent:** sparse or matrix encodings can erase legitimate zero-weight edges.
- **Silent symmetrization:** directed costs cannot generally be treated as undirected.
- **Missing vertices:** edge-derived universes omit isolated targets and sources.
- **MST confusion:** minimum total connecting weight differs from minimum source distances.
- **A* confusion:** Dijkstra uses no goal heuristic; adding one changes proof obligations.
- **Static-graph assumption:** changing weights after settlement invalidates labels.
- **Partial-as-complete:** cancellation does not establish distances for unsettled vertices.
- **Scalar-model overclaim:** one additive score may omit capacity, timing, risk, or policy constraints.
- **Asymptotic overclaim:** heap traffic, graph layout, and output can dominate wall time.
- **Path existence overclaim:** finite labels certify modeled edges, not real-world availability.

## Worked Examples

### Example 1

**Situation.** Run Dijkstra on $s\to a=4$, $s\to b=1$, and $b\to a=2$.

Settle $s$ at zero and relax labels to $d[a]=4$, $d[b]=1$. The minimum frontier label is $b=1$, so settle $b$. Relaxing $b\to a$ proposes $1+2=3$, improving $a$. Settle $a$ at three. Predecessors yield $s\to b\to a$.

**Conclusion.** First discovery does not finalize a label; minimum-key settlement plus relaxation produces distance three.

### Example 2

**Situation.** The target $t$ is first relaxed to $10$ from $s$, while frontier vertex $u$ has label $3$ and edge $u\to t=2$.

Stopping at discovery returns ten. Dijkstra instead settles $u$ because three is the minimum key, relaxes $t$ to five, then eventually settles $t$ at five. Only that extraction invokes the finalization proof.

**Conclusion.** Early target exit is correct at live minimum extraction, not insertion or first relaxation.

### Example 3

**Situation.** Edges are $s\to u=2$, $s\to v=5$, and $v\to u=-10$.

The standard algorithm settles $u$ at two before $v$. After settling $v$, it discovers path weight $5-10=-5$ to an already-settled vertex. The nonnegative-suffix inequality used in the proof is false.

**Conclusion.** One reachable negative edge can break label setting even without a negative cycle; use a suitable algorithm or reject the graph.

### Example 4

**Situation.** Heap holds stale `(9,x)` after a later relaxation pushes `(4,x)`.

The entry with key four pops first, matches current $d[x]$, and settles $x$. When key nine later pops, `x` is already settled and the entry is discarded. If another vertex improvement left `(6,y)` while current $d[y]=5$, the key mismatch would also identify staleness before settlement.

**Conclusion.** Duplicate-entry heaps are correct when every pop validates both settlement state and current key.

### Example 5

**Situation.** Edges $s\to a=0$, $a\to b=0$, and $s\to b=1$ contain zero weights.

Settle $s$ at zero, producing $d[a]=0$ and $d[b]=1$. Settle $a$ next at zero and relax $b$ to zero. Then settle $b$. Nonnegative proof inequalities allow equality. A tie policy may settle multiple zero-distance vertices in either valid order.

**Conclusion.** Dijkstra requires nonnegative, not strictly positive, weights; witness tie handling must still avoid predecessor cycles.

### Example 6

**Situation.** Compare a shortest-path tree and MST on undirected triangle $sa=2$, $sb=2$, $ab=1$ rooted at $s$.

The shortest-path tree uses $sa$ and $sb$: distances to $a$ and $b$ are both two, and total tree edge weight is four. An MST uses $ab$ plus either source edge, total three. In that MST the source distance to the vertex reached through $ab$ is three, worse than its direct distance two.

**Conclusion.** Minimizing every root distance and minimizing total selected edge weight are different objectives.

### Example 7

**Situation.** Validate distances $d[s]=0$, $d[a]=2$, $d[b]=5$ for edges $s\to a=2$, $a\to b=1$, and $s\to b=5$.

Labels are achievable through direct predecessors, but edge $a\to b$ violates the required inequality because $d[b]=5>2+1=3$. Thus a path of weight three disproves the claimed distance. Replacing $d[b]$ with three and predecessor $a$ makes all inequalities tight or satisfied.

**Conclusion.** Feasible witness paths alone prove upper bounds; edge inequalities supply the lower-bound side of optimality.

### Example 8

**Situation.** A signed 32-bit implementation has $d[u]=2{,}147{,}483{,}640$ and edge weight $20$.

The mathematical proposal is $2{,}147{,}483{,}660$, greater than the maximum $2{,}147{,}483{,}647$. Wrapping arithmetic may produce a negative value, which appears better than every valid nonnegative distance and corrupts heap order. The implementation must reject, widen, saturate with carefully proved semantics, or use arbitrary precision.

**Conclusion.** Checked addition is part of the path-label invariant, not merely defensive programming.

### Example 9

**Situation.** A graph has $n=40{,}000{,}000$ vertices. Distances and predecessors each use 64-bit words, and settled state uses one byte per vertex, excluding alignment and heap storage.

The two word arrays use

$$
2\times40{,}000{,}000\times8=640{,}000{,}000\text{ bytes}.
$$

Settled state adds $40{,}000{,}000$ bytes, totaling $680{,}000{,}000$ bytes, about $648.50$ MiB. A duplicate heap can require much more and must be budgeted from relaxation behavior.

**Conclusion.** Linear per-vertex state is substantial at scale, and heap occupancy can dominate it.

### Example 10

**Situation.** A route engine minimizes nominal travel minutes, but one edge is closed at certain departure times and another requires a vehicle permit.

Static Dijkstra can correctly minimize the scalar weights in its snapshot while returning an infeasible real trip. The graph must encode availability and vehicle state, or use time-dependent and resource-constrained shortest-path models. The result should name data timestamp and assumptions.

**Conclusion.** Algorithmic optimality is exact only for the modeled graph, objective, and constraints.

## Cross-Program Connections

- Data Structures Engineering owns heaps, maps, compact adjacency, and indexed-priority invariants; Algorithm Engineering owns shortest-path proof and selection.
- Theory of Computation owns complexity of richer constrained path problems; ordinary nonnegative SSSP is only one boundary.
- Computer Architecture influences heap locality, adjacency layout, integer width, and parallel memory traffic.
- Network Engineering applies shortest paths to routing but adds protocol metrics, convergence, policy, equal-cost multipath, and failures.
- Database Engineering and Data Engineering use graph costs and lineage but must pin snapshots and data currency.
- Distributed Systems adds partitioned queues, relaxed ordering, message delay, duplicate work, and termination evidence.
- Security Engineering reviews adversarial weights, overflow, NaN, graph-size denial of service, and untrusted identifiers.
- [ALGE-035](./035-minimum-spanning-trees.md) contrasts the MST objective. [ALGE-037](../ROADMAP.md#block-04--graph-algorithms) introduces negative-weight label correction, and [ALGE-038](../ROADMAP.md#block-04--graph-algorithms) extends to all-pairs distances.

## References

1. Edsger W. Dijkstra, “A Note on Two Problems in Connexion with Graphs,” *Numerische Mathematik* 1, 269–271, 1959, DOI [10.1007/BF01386390](https://doi.org/10.1007/BF01386390). Primary source; publisher and CWI institutional records checked 2026-09-05.
2. Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein, *Introduction to Algorithms*, 4th ed., MIT Press, 2022, §§22.1–22.3. [Official publisher record](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/), checked 2026-09-05.
3. Robert Sedgewick and Kevin Wayne, *Algorithms*, 4th ed., Addison-Wesley, 2011, §4.4. [Author-maintained shortest-path material](https://algs4.cs.princeton.edu/44sp/), checked 2026-09-05.
4. Jeff Erickson, *Algorithms*, 1st ed., 2019, shortest-path chapter. [Author-hosted book](https://jeffe.cs.illinois.edu/teaching/algorithms/), checked 2026-09-05.
5. Boost C++ Libraries, “Dijkstra's Shortest Paths,” Boost.Graph 1.92.0 documentation. [Official documentation](https://www.boost.org/doc/libs/latest/libs/graph/doc/html/graph/algorithms/shortest_paths/dijkstra_shortest_paths.html), checked 2026-09-05.
6. SciPy developers, “`scipy.sparse.csgraph.shortest_path`,” SciPy 1.18.0 manual. [Official documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csgraph.shortest_path.html), checked 2026-09-05.
7. Alexander Schrijver, *Combinatorial Optimization: Polyhedra and Efficiency*, Springer, 2003, shortest-path sections. [Official publisher record](https://link.springer.com/book/9783540443896), checked 2026-09-05.
8. Ravindra K. Ahuja, Thomas L. Magnanti, and James B. Orlin, *Network Flows: Theory, Algorithms, and Applications*, Prentice Hall, 1993, shortest-path chapters. [MIT-hosted bibliographic record](https://dspace.mit.edu/handle/1721.1/49424), checked 2026-09-05.

## Exercises

### Exercise 1

Run Dijkstra from $s$ on edges $s\to a=6$, $s\to b=2$, $b\to a=1$, $b\to c=5$, $a\to c=2$, and $c\to d=1$. Show every live extraction, successful relaxation, final distance, and predecessor.

### Exercise 2

Give a complete proof that the minimum-label unsettled vertex is safe to settle when all edge weights are nonnegative. Identify exactly where nonnegativity and prior relaxation are used.

### Exercise 3

A service uses unsigned 32-bit distances, maximum integer as infinity, duplicate heap entries, and updates predecessors on `proposal <= distance`. Diagnose at least four correctness or evidence risks and give precise repairs.

### Exercise 4

Choose among dense-scan Dijkstra, indexed-heap Dijkstra, duplicate-heap Dijkstra, BFS, topological relaxation, and Bellman–Ford for three workloads: a dense nonnegative graph, a huge sparse unit-weight graph, and a sparse DAG with negative edges. Justify representation and validation choices.

### Exercise 5

Design a shortest-route service for versioned road data with zero-cost connectors, closures, turn restrictions, time-dependent travel, cancellation, and reproducible incident replay. State what ordinary Dijkstra can solve, what model changes are required, and what evidence is published.

## Answers to the Exercises

### Answer 1

Initialize $d[s]=0$ and others infinity. Extract $s$ and relax $a$ to six through $s$ and $b$ to two through $s$. Extract $b$ at two. Relax $b\to a$ to $2+1=3$, replacing predecessor of $a$ with $b$; relax $c$ to seven through $b$. Extract $a$ at three, discarding the later stale key six when encountered. Relax $a\to c$ to $3+2=5$, replacing predecessor of $c$ with $a$.

Extract $c$ at five, later discarding stale key seven, and relax $d$ to six through $c$. Extract $d$ at six. Final distances are

$$
d[s]=0,\quad d[b]=2,\quad d[a]=3,\quad d[c]=5,\quad d[d]=6.
$$

Predecessors are $\pi[b]=s$, $\pi[a]=b$, $\pi[c]=a$, and $\pi[d]=c$. The path to $d$ is $s\to b\to a\to c\to d$ of weight six.

### Answer 2

Maintain that every settled $x$ has $d[x]=\delta(s,x)$ and every finite label is the weight of a discovered source path. Let $u$ be the unsettled vertex of minimum finite label. Assume a cheaper source-to-$u$ path $p$ exists. Traverse $p$ from $s$ and choose its first unsettled vertex $y$; its predecessor $x$ on $p$ is settled.

When $x$ settled, the algorithm examined and relaxed $x\to y$. Since $d[x]=\delta(s,x)$ and the prefix used in a minimum counterexample has its stated path weight, relaxation ensures $d[y]$ is no greater than the weight of the prefix through $y$. This is where complete outgoing-edge relaxation of settled vertices is used.

Every edge on the remaining suffix from $y$ to $u$ is nonnegative, so the prefix weight through $y$ is no greater than the whole path weight. Therefore

$$
d[y]\le w(p[s\leadsto y])\le w(p)<d[u].
$$

But $y$ is unsettled, contradicting that $u$ had minimum tentative label. Hence no cheaper $p$ exists. Since $d[u]$ is itself achievable, $d[u]=\delta(s,u)$. Nonnegativity is used exactly in comparing the prefix with the whole path; a negative suffix destroys that inequality.

### Answer 3

First, unsigned addition can wrap to a small value. Check `weight > MAX - distance` before addition or use a wider/arbitrary-precision accumulator. Second, using `MAX` as infinity collides with a valid path of exactly `MAX`; use a tagged unreachable state or reserve the sentinel and reject path totals that reach it.

Third, duplicate heap entries require rejecting entries whose key differs from current distance and entries for settled vertices. Without both checks, stale work can violate event and resource contracts. Fourth, updating on equality can create predecessor cycles across zero-weight tight edges. Update the basic witness only on strict improvement, or apply a proved well-founded tie rule such as predecessor rank from settlement order.

Also reject negative inputs before trusting completion, require a stable comparable heap tie key, retain isolated vertices, and bind arithmetic and output to one graph snapshot. Validate reachability, source state, tight predecessor chains, and every edge inequality.

### Answer 4

For a dense nonnegative graph already in a matrix, use dense-scan Dijkstra. Its $O(n^2)$ sequential access can avoid heap overhead, and matrix scanning is not asymptotically worse than reading dense edges. Preserve a separate absence marker so zero weights remain representable. Validate with predecessor tightness and all matrix edge inequalities.

For a huge sparse unit-weight graph, use BFS with adjacency lists or compressed sparse rows. FIFO layers are exact distances, avoid logarithmic heap work, and are easy to validate by parent depth and edge layer inequalities.

For a sparse DAG with negative edges, use topological relaxation after validating acyclicity and obtaining a topological order. It runs in $O(n+m)$ and negative edges are safe because no vertex needs cyclic reconsideration. If acyclicity cannot be established, choose Bellman–Ford or reject according to contract. An indexed or duplicate heap Dijkstra is invalid merely because some weights are negative.

Between heap variants for an ordinary sparse nonnegative graph, indexed heaps control queue memory while duplicate heaps simplify code; decide from measured improvement frequency, memory, and implementation risk. The graph and numeric contract precede the data-structure choice.

### Answer 5

Pin an immutable road-data revision containing stable vertex and directed-edge IDs, units, legal vehicle class, and closure timestamp. Zero-cost connectors are valid nonnegative edges. Turn restrictions usually require an expanded state graph whose vertices include the incoming-road or maneuver state; simply deleting one road edge may be insufficient.

Ordinary Dijkstra solves a static additive nonnegative snapshot. Time-dependent travel requires state and edge functions evaluated at arrival time plus a FIFO-property proof for label setting, or another time-dependent algorithm. Closures varying during a trip need an explicit departure-time snapshot or replanning policy. Multiple constraints such as height, permits, or toll budgets may require state expansion or resource-constrained methods.

Use stable tie keys for replay, checked duration arithmetic, live-key heap validation, and early exit only on target settlement. Cancellation returns an incomplete status with the pinned revision, never unreachable. A checkpoint contains revision, source/target state, labels, predecessors, settled set, heap, model version, and arithmetic policy.

Publish route status, vertex/edge path, total modeled cost, departure time, data revision, vehicle and turn assumptions, algorithm/model version, and certificate results. Independently check every path edge and restriction, recompute total, verify tight predecessors and edge inequalities for the computed search scope, and record that live conditions after the snapshot are not guaranteed.
