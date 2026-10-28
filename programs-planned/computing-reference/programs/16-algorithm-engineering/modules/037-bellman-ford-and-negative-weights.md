---
module_id: ALGE-037
program: Algorithm Engineering
level: 1
module_number: 37
title: Bellman-Ford and Negative Weights
status: complete
last_verified: 2026-09-05
---

# Bellman-Ford and Negative Weights

## One-Page Review

### Governing question

How can repeated relaxation compute source distances with signed edges, prove finite optima, and distinguish unreachable vertices from every vertex made unbounded below by a source-reachable negative cycle?

### Essential definitions

- A **distance label** $d[v]$ is the weight of a currently known source walk.
- **Relaxation** replaces a label when extending a known walk across one edge is cheaper.
- A **complete pass** considers every pinned logical edge once.
- A **label-correcting** algorithm may improve the same vertex repeatedly.
- A **negative cycle** is a directed cycle whose edge weights sum below zero.
- An **affected vertex** is reachable from a negative cycle that is itself reachable from the source.
- A **fixed point** has no relaxable edge under the declared arithmetic.
- A **cycle witness** names directed edges whose checked total is negative.
- $+\infty$ denotes unreachable; $-\infty$ denotes unbounded below, not a finite machine number.

### Central model, mechanism, or theorem

Bellman-Ford solves single-source shortest paths on a finite directed graph with signed additive edge weights. Unlike Dijkstra's label-setting method, it is **label-correcting**: a vertex may improve repeatedly as cheaper paths with more edges become known. A reachable negative-weight cycle makes the ordinary minimum undefined for the cycle and every vertex reachable from it; costs can be driven toward negative infinity by repeating the cycle.

For source $s$, initialize $d[s]=0$ and every other label to infinity. A relaxation of edge $u\to v$ with weight $w(u,v)$ applies

$$
d[v]\leftarrow\min(d[v],d[u]+w(u,v)).
$$

After complete relaxation passes, every source path with at most the corresponding number of edges has had an opportunity to propagate. Any simple path has at most $n-1$ edges, so $n-1$ full passes suffice when no relevant negative cycle exists. If a reachable edge can still improve on an additional pass, some reachable negative-weight cycle exists.

### Critical invariants

- Every finite label is the weight of an actual source walk, so it is an upper bound on a finite shortest-path value.
- Labels never increase.
- After pass $k$, each vertex label is no greater than the weight of every source path using at most $k$ edges; in-place ordering may discover still longer paths sooner.
- Strict predecessor updates preserve an actual witness edge for each improvement.
- Infinity is never added to a weight; arithmetic is checked under a declared numeric policy.
- A full pass with no change establishes every reachable edge inequality and permits safe early termination.
- Detection concerns cycles reachable from the chosen source, not arbitrary disconnected cycles.
- Vertices reachable from a detected negative cycle have value $-\infty$ under the extended shortest-walk model; unaffected finite and unreachable vertices must remain distinguishable.
- Cycle witnesses, affected sets, and partial labels are bound to the same immutable graph snapshot.

### Common failures

Common failures include running only $n-2$ passes; treating edge order as semantics; adding a weight to infinity; confusing any negative edge with a negative cycle; reporting a disconnected negative cycle; detecting a reachable cycle but returning its downstream labels as finite; claiming the first relaxable edge itself lies on the cycle; extracting a predecessor cycle without walking back $n$ times; updating predecessors on equality; overflowing fixed-width arithmetic; using a sentinel that collides with a valid value; stopping mid-pass; scanning only adjacency reachable under stale state; mutating the graph between computation and detection; and using floating NaN in ordered comparisons.

### Compact example

Edges $s\to a=4$, $s\to b=5$, and $a\to b=-3$ contain a negative edge but no cycle. Relaxation eventually changes $d[b]$ from five to one through $a$. Bellman-Ford returns a valid finite answer. Adding $b\to a=1$ creates cycle $a\to b\to a$ of total weight $-2$. Because the cycle is reachable from $s$, repeating it makes the values for $a$, $b$, and their descendants unbounded below.

### Connections

[ALGE-031](./031-breadth-first-search.md) supplies reachability, [ALGE-033](./033-topological-ordering.md) supplies the acyclic signed-weight special case, [ALGE-034](./034-strongly-connected-components.md) identifies cycle regions, and [ALGE-036](./036-dijkstra-s-shortest-paths.md) contrasts nonnegative label setting. [ALGE-038](../ROADMAP.md#block-04--graph-algorithms) next extends shortest paths to all pairs.

## Governing Question

How should an implementation compute and certify source distances when edges may be negative, while distinguishing finite optima, unreachable vertices, reachable negative-cycle effects, cycle witnesses, ordering artifacts, arithmetic failure, and incomplete execution?

The core algorithm is short, but its result contract is not. “Negative cycle found” should say whether the cycle is source-reachable, provide a checkable witness when required, and identify every output vertex whose finite label is invalidated. A graph may also contain a disconnected negative cycle that has no effect on the selected source.

The proof uses bounded path length, not greedy settlement. Its implementation must therefore make a **pass** precise: a complete traversal of one pinned logical edge set. In-place updates can travel through multiple edges during one pass, so edge order affects intermediate traces and early convergence, but not the final classification when the full obligations are met.

## Why This Matters

Signed costs occur in currency transformations, credits and penalties, constraint graphs, schedule offsets, difference constraints, residual networks, and reweighted optimization models. A negative edge can be entirely legitimate. A reachable negative cycle, however, signals either an unbounded objective or a model inconsistency under the additive walk interpretation.

The algorithm is also a compact lesson in dynamic programming and proof engineering. Correctness follows from a path-edge bound and repeated local closure. Negative-cycle detection is a theorem about one extra relaxation, not a heuristic based on “very negative” numbers. Independent certificates separate achievable witness paths, edge inequalities, reachability, and negative-cycle evidence.

Production failures are usually outside the five-line pseudocode: numeric wraparound creates false improvements, asynchronous cancellation creates a non-pass, in-place edge order destroys deterministic traces, a predecessor chain points into but not around a cycle, or a service publishes finite labels for descendants of an unbounded cycle. These are observable contract defects.

## Prerequisites and Retrieval

Retrieve:

- directed graphs, walks, paths, cycles, reachability, adjacency and edge-list representations;
- exact signed arithmetic, infinity, overflow, total ordering, and units;
- relaxation, distance-label upper bounds, predecessors, and shortest-path certificates;
- induction over path length, pigeonhole reasoning, contradiction, and loop invariants;
- [ALGE-031](./031-breadth-first-search.md) for reachability;
- [ALGE-033](./033-topological-ordering.md) for acyclic shortest paths;
- [ALGE-034](./034-strongly-connected-components.md) for cycle regions;
- [ALGE-036](./036-dijkstra-s-shortest-paths.md) for nonnegative label setting and edge-inequality certificates.

You should be able to explain why a repeated vertex decomposes a walk into a prefix, a cycle, and a suffix, and why removing a nonnegative cycle cannot increase path cost.

## Learning Objectives

After completing this module, you should be able to:

1. specify finite, unreachable, and negative-infinity shortest-walk outcomes;
2. derive Bellman-Ford relaxation from bounded-edge dynamic programming;
3. prove why $n-1$ complete passes cover all simple source paths;
4. prove the extra-pass criterion for source-reachable negative cycles;
5. implement deterministic in-place Bellman-Ford with checked signed integers;
6. extract and validate a concrete negative-cycle witness;
7. propagate cycle effects to every downstream vertex without contaminating unaffected output;
8. distinguish synchronous from in-place passes and safe from unsafe early termination;
9. validate finite distances, reachability, affected sets, and cycle evidence independently;
10. choose among Bellman-Ford, DAG relaxation, Dijkstra, queue heuristics, and all-pairs methods.

## Core Exposition

### Specify the result domain first

Let $G=(V,E)$ be a finite directed multigraph with $n=|V|$, source $s\in V$, and exact signed edge weights $w:E\to\mathbb Z$. A walk may repeat vertices and edges. Its weight is the sum of edge weights.

For a vertex $v$, there are three semantic outcomes:

1. **unreachable:** no directed walk from $s$ reaches $v$, represented by $+\infty$;
2. **finite:** reachable, with a minimum walk weight attained by a simple path;
3. **unbounded below:** a negative cycle is reachable from $s$ and can reach $v$, represented by $-\infty$ in an extended result model.

The last outcome is not a very small finite distance. If walk $p$ reaches negative cycle $C$, and a suffix reaches $v$, traversing $C$ another $q$ times decreases the total by $q|w(C)|$. No minimum exists.

Declare directedness, parallel-edge identity, source, complete vertex universe, weight type and units, overflow behavior, graph revision, output scope, tie policy, cancellation semantics, and whether a cycle witness is mandatory. Do not silently reinterpret walks as simple paths: minimizing only over simple paths remains finite but is a different computational problem.

### Derive relaxation from bounded-edge paths

Define $D_k(v)$ as the minimum weight of any source-to-$v$ path using at most $k$ edges, with infinity if none exists. Then

$$
D_0(s)=0,\qquad D_0(v)=+\infty\quad(v\ne s),
$$

and the recurrence is

$$
D_k(v)=\min\left(D_{k-1}(v),\min_{(u,v)\in E}
\bigl(D_{k-1}(u)+w(u,v)\bigr)\right).
$$

A synchronous implementation stores the preceding row and computes the next row, matching this equality exactly. Standard Bellman-Ford usually updates one distance array in place. An early edge improvement can then feed a later edge in the same pass. Consequently, after pass $k$ the in-place label may represent more than $k$ edges, but it is at least as good as every path of at most $k$ edges. This one-sided invariant is sufficient.

Relax only from a finite tail. The expression $+\infty+w$ is mathematical shorthand under extended arithmetic; machine code using a maximum sentinel can wrap or fabricate a finite candidate.

### Prove the $n-1$ pass bound

Assume no negative cycle is both reachable from $s$ and able to reach $v$. Consider a minimum-weight source-to-$v$ walk. If it repeats a vertex, the repeated segment is a cycle. A negative repeated cycle would contradict the assumption; removing a zero or positive cycle does not increase weight. Repeating this removal yields a simple path with at most $n-1$ edges and no greater weight.

By induction on path length, after pass $k$, the label of each vertex is no greater than the weight of every source path with at most $k$ edges. The base $k=0$ follows from initialization. For a path of at most $k$ edges ending in $u\to v$, its prefix uses at most $k-1$ edges. The induction hypothesis bounds $d[u]$, and the pass relaxes $u\to v$, bounding $d[v]$ by the whole path.

Every finite label is also the weight of an actual source walk, so it cannot be less than a finite optimum. After $n-1$ passes, these inequalities meet for every unaffected reachable vertex.

### Prove negative-cycle detection

After $n-1$ complete passes, scan all edges once more. Suppose reachable edge $u\to v$ still satisfies

$$
d[u]+w(u,v)<d[v].
$$

The new witness walk contains at least $n$ edges in the proof accounting. Among its vertices, some vertex repeats. If every repeated cycle had nonnegative weight, removing cycles would produce a simple path of at most $n-1$ edges no heavier than the witness, contradicting closure after the preceding passes. Therefore a reachable negative cycle exists.

Conversely, let reachable cycle $C$ have negative total weight. If all its edge inequalities were satisfied, summing them around the cycle would cancel every distance label and yield $0\le w(C)<0$, impossible. Thus at least one reachable edge remains relaxable. Detection is exact under the declared arithmetic and completed-pass assumptions.

A relaxable edge need not itself belong to the negative cycle; it may be downstream. It is a seed for finding the affected region, not automatically the witness.

### Implement finite distances and cycle classification

The following deterministic implementation sorts stable edge identities, uses exact Python integers, distinguishes unreachable and affected vertices, extracts a predecessor-cycle witness, and validates its negative weight. The returned pre-classification finite labels for affected vertices are internal evidence only; callers receive their semantic status as negative infinity.

<!-- bijux-verify: {"id":"deterministic-bellman-ford","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"finite_distances=(('a', '4'), ('b', '2'), ('c', '5'), ('s', '0'), ('x', 'inf'))\nfinite_path_c=('s', 'a', 'b', 'c')\nfinite_valid=True\ncycle_affected=('a', 'b', 'c', 'd')\ncycle_witness=('a', 'b', 'c', 'a')\ncycle_weight=-2\nsource_status=finite\n","stderr":""}} -->
```python
from math import inf


def normalize(vertices, edges):
    vertices = set(vertices)
    seen = set()
    ordered = []
    adjacency = {vertex: [] for vertex in vertices}
    for edge_id, tail, head, weight in edges:
        if edge_id in seen:
            raise ValueError(f"duplicate edge identity: {edge_id}")
        if tail not in vertices or head not in vertices:
            raise ValueError(f"unknown endpoint: {edge_id}")
        if not isinstance(weight, int):
            raise ValueError("weights must be exact integers")
        seen.add(edge_id)
        ordered.append((edge_id, tail, head, weight))
        adjacency[tail].append(head)
    return tuple(sorted(ordered)), {
        vertex: tuple(sorted(heads))
        for vertex, heads in adjacency.items()
    }


def canonical_cycle(vertices):
    body = vertices[:-1]
    rotations = [body[i:] + body[:i] for i in range(len(body))]
    chosen = min(rotations)
    return tuple(chosen + chosen[:1])


def bellman_ford(vertices, edges, source):
    ordered, adjacency = normalize(vertices, edges)
    vertices = tuple(sorted(adjacency))
    if source not in adjacency:
        raise ValueError("source is outside the vertex universe")
    distance = {vertex: inf for vertex in vertices}
    predecessor = {vertex: None for vertex in vertices}
    predecessor_edge = {vertex: None for vertex in vertices}
    distance[source] = 0

    for _ in range(len(vertices) - 1):
        changed = False
        for edge_id, tail, head, weight in ordered:
            if distance[tail] != inf and distance[tail] + weight < distance[head]:
                distance[head] = distance[tail] + weight
                predecessor[head] = tail
                predecessor_edge[head] = edge_id
                changed = True
        if not changed:
            break

    probe = dict(distance)
    probe_predecessor = dict(predecessor)
    probe_edge = dict(predecessor_edge)
    improved = []
    for edge_id, tail, head, weight in ordered:
        if probe[tail] != inf and probe[tail] + weight < probe[head]:
            probe[head] = probe[tail] + weight
            probe_predecessor[head] = tail
            probe_edge[head] = edge_id
            improved.append(head)

    if not improved:
        return ordered, adjacency, distance, predecessor, set(), None, None

    affected = set(improved)
    stack = list(improved)
    while stack:
        tail = stack.pop()
        for head in adjacency[tail]:
            if head not in affected:
                affected.add(head)
                stack.append(head)

    vertex = improved[-1]
    for _ in vertices:
        vertex = probe_predecessor[vertex]
    backward = [vertex]
    cursor = probe_predecessor[vertex]
    while cursor != vertex:
        backward.append(cursor)
        cursor = probe_predecessor[cursor]
    forward = canonical_cycle(list(reversed(backward)) + [backward[-1]])
    edge_by_id = {edge_id: (tail, head, weight)
                  for edge_id, tail, head, weight in ordered}
    cycle_weight = sum(edge_by_id[probe_edge[head]][2]
                       for head in forward[1:])
    if cycle_weight >= 0:
        raise AssertionError("extracted cycle is not negative")
    return (ordered, adjacency, distance, predecessor, affected,
            forward, cycle_weight)


def path_to(source, target, distance, predecessor):
    if distance[target] == inf:
        return None
    path = []
    seen = set()
    cursor = target
    while cursor is not None:
        if cursor in seen:
            raise ValueError("predecessor cycle")
        seen.add(cursor)
        path.append(cursor)
        if cursor == source:
            return tuple(reversed(path))
        cursor = predecessor[cursor]
    raise ValueError("finite label lacks a source witness")


def validate_finite(ordered, source, distance, predecessor):
    if distance[source] != 0 or predecessor[source] is not None:
        return False
    for _, tail, head, weight in ordered:
        if distance[tail] != inf and distance[head] > distance[tail] + weight:
            return False
    for vertex, value in distance.items():
        if vertex != source and value != inf:
            parent = predecessor[vertex]
            if parent is None or not any(
                tail == parent and head == vertex
                and distance[parent] + weight == value
                for _, tail, head, weight in ordered
            ):
                return False
            path_to(source, vertex, distance, predecessor)
    return True


vertices = {"s", "a", "b", "c", "x"}
finite_edges = (
    ("sa", "s", "a", 4), ("sb", "s", "b", 5),
    ("ab", "a", "b", -2), ("bc", "b", "c", 3),
    ("ac", "a", "c", 4),
)
result = bellman_ford(vertices, finite_edges, "s")
ordered, _, distance, predecessor, affected, _, _ = result
display = lambda value: "inf" if value == inf else str(value)
print("finite_distances=" + str(tuple(
    (v, display(distance[v])) for v in sorted(vertices))))
print(f"finite_path_c={path_to('s', 'c', distance, predecessor)}")
print(f"finite_valid={not affected and validate_finite(ordered, 's', distance, predecessor)}")

cycle_vertices = {"s", "a", "b", "c", "d"}
cycle_edges = (
    ("sa", "s", "a", 1), ("ab", "a", "b", 1),
    ("bc", "b", "c", 1), ("ca", "c", "a", -4),
    ("bd", "b", "d", 2),
)
result = bellman_ford(cycle_vertices, cycle_edges, "s")
_, _, cycle_distance, _, affected, witness, weight = result
print(f"cycle_affected={tuple(sorted(affected))}")
print(f"cycle_witness={witness}")
print(f"cycle_weight={weight}")
print("source_status=" + ("negative-infinity" if "s" in affected else
                           "finite" if cycle_distance["s"] != inf else "unreachable"))
```

The executable uses one extra in-place scan for both detection and predecessor evidence. Exact witness extraction follows predecessor pointers $n$ times before collecting the cycle: any chain of $n$ predecessor edges among $n$ vertices has entered a repeated region. Canonical rotation makes the same directed cycle print from its smallest stable vertex.

### Classify every affected vertex

An improved vertex on the detection pass is reachable from some relevant negative cycle or lies downstream of one. Starting a directed reachability traversal from all improved heads identifies the full affected set. Every reached vertex has value $-\infty$ because another traversal of the negative cycle can precede the suffix to that vertex.

Do not propagate backward to ancestors that cannot be revisited after the cycle. In the executable example, $a,b,c,d$ are affected, while source $s$ remains finite because the cycle has no path back to $s$. A disconnected negative cycle is never seeded because its tails remain unreachable at infinity.

For a single target, a reachable negative cycle matters only if it can reach the target. A global SSSP API should still classify all vertices; a target-only API may intersect source reachability, negative-cycle regions, and reverse target reachability.

### Extract a checkable cycle witness

Predecessors after the detection relaxation may form a tree feeding into a cycle. The initially improved vertex can therefore be downstream rather than on the cycle. Follow predecessors at least $n$ steps to enter a cycle, then continue until the starting vertex repeats. Reverse the predecessor traversal to obtain forward edge direction.

A valid witness must check:

- every listed vertex and stable edge exists in the pinned graph;
- consecutive edges have the declared direction;
- the first and last vertex match and an interior vertex does not repeat;
- every predecessor edge corresponds to the recorded relaxation evidence;
- checked recomputation of the edge sum is strictly negative;
- the cycle is reachable from the source.

Multiple negative cycles and edge orders can yield different valid witnesses. Deterministic edge order and cycle rotation support replay but do not make one witness canonical across all correct implementations.

### Use early termination safely

If a complete pass performs no strict improvement, every reachable edge inequality already holds. With predecessor witness paths, these inequalities certify finite optima, and another pass would also change nothing. Early termination is safe.

Stopping after an unchanged prefix of the edge list is unsafe: a later edge might improve. Stopping after one vertex's outgoing list is unchanged is also unsafe. In parallel or distributed variants, “no change” requires a barrier or termination protocol proving that every logical edge was considered against the intended state and no update remains in flight.

In-place passes depend on edge order for how quickly improvements propagate. Synchronous two-array passes have deterministic hop-bounded semantics and straightforward parallel reads, but use more memory and may converge later in wall-clock work. Both need the same fixed-point and detection obligations.

### Validate finite output independently

For vertices not classified as affected, validate:

1. source distance and predecessor policy;
2. independent source reachability;
3. a tight valid predecessor edge for every finite non-source label;
4. predecessor chains that reach the source without cycling;
5. every edge inequality $d[v]\le d[u]+w(u,v)$ whose endpoints are unaffected and whose tail is finite;
6. no edge from a finite or affected reachable region was silently omitted;
7. graph identity, arithmetic policy, and status publication.

Tight predecessor paths prove achievability. Edge inequalities prove by induction that the label is no greater than every source path. The two directions meet at equality. For affected vertices, replace finite-certificate obligations with source-to-cycle reachability, a negative witness, and cycle-to-vertex reachability.

An independent oracle for small graphs can enumerate simple paths and cycles. A second Bellman-Ford implementation is useful but can share parsing or arithmetic defects. Linear-programming difference constraints or Floyd-Warshall on a bounded graph provide different cross-checks.

### Govern arithmetic, infinity, and evidence

Signed weights make underflow as dangerous as overflow. For fixed-width integers, check addition before every relaxation or use a wider verified accumulator. Do not rely on wraparound behavior, saturating arithmetic, or an arbitrary iteration threshold. Saturating at a minimum value can hide continued strict decreases and suppress cycle detection.

Use tagged states for unreachable and negative infinity, or prove sentinels cannot collide with valid finite values. Reject NaN because comparisons cease to form a coherent total order. Floating rounding can produce tiny apparent improvements; define tolerances only with a proof of what they preserve, because a tolerance can also hide a genuinely negative cycle.

A successful local run proves only observed behavior in its recorded environment. The executable above does not prove all graphs, machine types, edge loaders, concurrent snapshots, or service integrations. Mathematical arguments establish the abstract algorithm under assumptions; implementation correspondence and operational controls require separate evidence.

### Preserve snapshots, cancellation, and publication

Vertex count $n$, edge passes, detection, reachability propagation, witness extraction, and validation must refer to one graph revision. Inserting an edge between the final ordinary pass and detection can manufacture a false “algorithm failure”; deleting a witness edge invalidates evidence.

A resumable checkpoint records graph digest, source, weight and arithmetic policy, stable edge order, completed-pass count, position within the current pass, distances, predecessors and predecessor-edge identities, changed flag, cancellation status, and output generation. A mid-pass checkpoint is not a completed pass.

Cancellation yields incomplete, not unreachable or finite-complete. Quarantine labels until final validation. Atomically publish per-vertex status, finite values and paths where applicable, affected-set evidence, cycle witness, graph revision, algorithm version, arithmetic contract, and validator outcome.

### Understand complexity and practical variants

Scanning $m$ logical edges for at most $n-1$ ordinary passes plus detection costs $O(nm)$ time and $O(n)$ label/predecessor storage beyond the graph. Early termination can reduce actual passes but not the worst-case bound. Witness and affected-set traversal add $O(n+m)$.

Queue-based label-correcting variants process vertices whose outgoing edges may improve. They can be fast on favorable inputs but retain poor worst cases and need careful queue-membership, cycle-detection, and adversarial-resource controls. They are engineering alternatives, not permission to quote a better universal bound.

The current [Boost.Graph 1.92.0 documentation](https://www.boost.org/doc/libs/latest/libs/graph/doc/html/graph/algorithms/shortest_paths/bellman_ford_shortest.html) describes Bellman-Ford as $O(VE)$ and exposes a final minimized/not-minimized visitor test; current [SciPy 1.18.0 documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csgraph.bellman_ford.html) reports a negative-cycle error rather than a per-vertex affected classification. These are version-specific interface behaviors, not the abstract result contract required of every implementation.

## Definitions and Notation

- $G=(V,E)$: finite directed multigraph.
- $n=|V|$, $m=|E|$: vertex and logical-edge counts.
- $s$: selected source.
- $w(e)$: exact signed additive edge weight.
- $p$, $W(p)$: a directed walk or path and its total weight.
- $C$, $W(C)$: a directed cycle and its total weight.
- $D_k(v)$: minimum source-to-$v$ path weight using at most $k$ edges.
- $d[v]$: current mutable distance label.
- $\pi[v]$: selected predecessor vertex; $\pi_E[v]$ is its stable edge identity.
- **relaxable edge:** finite-tail edge whose candidate is strictly below its head label.
- **complete pass:** one traversal of every pinned logical edge.
- **fixed point:** label state in which no reachable edge is relaxable.
- **affected vertex:** vertex reachable from a source-reachable negative cycle.
- $+\infty$: unreachable state.
- $-\infty$: unbounded-below state, not a finite machine number.
- **synchronous pass:** reads the preceding label vector and writes a separate next vector.
- **in-place pass:** later edges can observe earlier improvements in the same traversal.

## Mechanisms, Invariants, or Proof Structure

### Initialization

Set the source label to zero and all others to infinity. The source empty walk witnesses zero; no other finite claim exists.

### Preservation

Every strict update appends one real edge to an existing finite witness. Labels remain actual-walk weights and decrease monotonically. Predecessor and edge identity change atomically with the label.

### Bounded-path coverage

Induction on $k$ shows that $k$ complete passes cover every source path with at most $k$ edges. In-place propagation may be ahead of this lower guarantee but never behind it.

### Finite optimality

When no relevant negative cycle exists, cycle removal yields a simple optimal path with at most $n-1$ edges. Coverage plus the actual-witness upper-bound invariant establishes equality.

### Negative-cycle theorem

An improvement after $n-1$ passes implies a witness walk whose cycle-removal argument requires a negative repeated cycle. Conversely, summing satisfied inequalities around a reachable negative cycle would imply $0\le W(C)<0$.

### Termination

The outer loop has at most $n-1$ finite passes, and each pass scans a finite edge sequence. Early exit follows only from a complete unchanged pass. Detection and affected propagation are separately finite.

### Certificate split

Finite vertices require reachability, tight predecessor paths, and edge inequalities. Affected vertices require source reachability, a directed negative cycle, and reachability from that cycle. Unreachable vertices require independent non-reachability evidence within the pinned graph.

## Alternatives and Trade-Offs

### Bellman-Ford versus Dijkstra

Dijkstra is usually faster on nonnegative weights because safe minimum-label settlement avoids repeated full scans. Bellman-Ford admits negative edges and detects reachable negative cycles. Rejecting negatives and choosing Dijkstra is a valid policy only when the input contract supports rejection.

### Bellman-Ford versus DAG relaxation

A validated topological order permits one $O(n+m)$ pass even with negative edges because no directed cycle exists. Bellman-Ford is appropriate when cycles are allowed or acyclicity is unavailable.

### Synchronous versus in-place

Synchronous rows match the $D_k$ recurrence exactly and parallelize reads naturally, but need another vector. In-place scans use less state and may propagate faster, but traces depend on edge order and concurrent writes need stronger reasoning.

### Full scans versus active queues

Full scans have simple deterministic worst-case accounting. Active queues can avoid irrelevant edges but expose queue duplication, unfairness, adversarial ordering, and more complex negative-cycle evidence.

### One witness versus complete affected classification

One negative cycle proves the global finite SSSP contract failed. It does not identify every $-\infty$ vertex. Complete APIs should propagate effects; diagnostic APIs should also retain at least one stable witness.

## Failure Modes and Misconceptions

- **Negative edge means failure:** only a relevant negative cycle makes the walk optimum unbounded.
- **Any graph cycle is harmful:** zero and positive cycles do not decrease a walk.
- **Any negative cycle is relevant:** it must be reachable from the chosen source.
- **The relaxable edge is the cycle:** it can be downstream; predecessor walk-back is required.
- **All reachable vertices become $-\infty$:** only descendants of relevant negative cycles do.
- **$n-2$ passes are enough:** a simple path may contain $n-1$ edges.
- **Edge order changes the answer:** it changes in-place traces and convergence speed, not a valid final classification.
- **One unchanged edge or prefix permits exit:** only a complete unchanged pass establishes closure.
- **Infinity can be added normally:** finite sentinels can overflow or create fake reachability.
- **Saturation is safe:** clamping can hide continuing negative-cycle improvements.
- **Equality should rewrite predecessors:** zero-weight tight edges can create witness cycles.
- **Very negative means negative cycle:** magnitude is irrelevant; the extra-pass theorem is structural.
- **A finite array after detection is usable:** affected labels are transient and have no finite optimum meaning.
- **Cancellation means no path:** it means computation is incomplete.
- **A library exception classifies output:** some interfaces signal only that a cycle exists; downstream status needs more work.

## Worked Examples

### Example 1

**Situation.** Edges are $s\to a=4$, $s\to b=5$, and $a\to b=-3$.

Initialization gives $(d[s],d[a],d[b])=(0,\infty,\infty)$. Relaxing the source edges gives four and five. Relaxing $a\to b$ changes five to $4-3=1$. No edge can then improve. The predecessor path $s\to a\to b$ has weight one, and all edge inequalities hold.

**Conclusion.** A negative edge is compatible with a finite optimum when no reachable negative cycle exists.

### Example 2

**Situation.** A chain $s\to v_1\to v_2\to v_3\to v_4$ has unit weights, but the in-place edge order is the reverse of the chain.

On pass one, only $s\to v_1$ can improve because every later chain tail was scanned earlier while infinite. Each subsequent pass advances the finite frontier by one edge. The four-edge path needs four passes, which equals $n-1$ for five vertices.

**Conclusion.** The $n-1$ bound is attainable under an unfavorable but valid edge order.

### Example 3

**Situation.** The same chain's edges are scanned from source outward.

In one in-place pass, $v_1$ becomes one, then $v_2$ becomes two, and so on through $v_4=4$. The next complete pass is unchanged, so early termination is safe. A synchronous implementation would still advance one hop per row.

**Conclusion.** In-place order affects convergence trace, while complete-pass invariants preserve the result.

### Example 4

**Situation.** Edges $s\to a=1$, $a\to b=1$, $b\to c=1$, and $c\to a=-4$ form a reachable cycle.

The cycle weight is $1+1-4=-2$. After reaching $a$, repeating the cycle $q$ times reduces walks to $a,b,c$ by $2q$. An extra pass must find some relaxable cycle edge because satisfied inequalities around the cycle would sum to $0\le-2$.

**Conclusion.** The affected vertices have no finite minimum; a concrete negative sum certifies why.

### Example 5

**Situation.** Source component is $s\to t=3$. A disconnected component has $x\to y=-2$ and $y\to x=1$.

The disconnected cycle weighs $-1$, but both $d[x]$ and $d[y]$ remain infinity. No relaxation from an infinite tail occurs. Distance to $t$ is three, and the source-relative run reports no relevant negative cycle.

**Conclusion.** Bellman-Ford detection is source-relative unless a super-source is deliberately added.

### Example 6

**Situation.** Reachable negative cycle $a\to b\to a$ has an outgoing edge $b\to d=100$, while no path returns to source $s$.

Values for $a$ and $b$ are unbounded below. For any bound $B$, repeat the cycle enough times before taking $b\to d$ to obtain a walk to $d$ below $B$; hence $d$ is also affected. The source remains finite because the cycle cannot reach it.

**Conclusion.** Propagate effects forward from cycle evidence, not to every ancestor or every reachable vertex.

### Example 7

**Situation.** After detection, predecessor of improved vertex $z$ is $y$, predecessor of $y$ is $b$, and predecessors then cycle $b\leftarrow a\leftarrow c\leftarrow b$.

Starting collection at $z$ would produce a tail, not a cycle. Walking backward $n$ times must enter the repeated predecessor region. Collecting until repeat and reversing direction yields forward cycle $b\to c\to a\to b$, whose stable edges and total must be checked.

**Conclusion.** An improved endpoint is a lead to evidence, not itself proof of cycle membership.

### Example 8

**Situation.** Signed 32-bit label is $-2{,}147{,}483{,}640$ and an edge has weight $-20$.

The mathematical candidate is $-2{,}147{,}483{,}660$, below the minimum $-2{,}147{,}483{,}648$. Two's-complement wrap can turn it into a large positive value, suppressing a true improvement; saturation at the minimum can also prevent later strict decreases. Checked addition or a wider accumulator is required.

**Conclusion.** Underflow can hide negative cycles just as overflow can invent short paths.

### Example 9

**Situation.** A parallel implementation sees no local change on one worker while another worker still holds an update message.

Local silence is not a fixed point. The termination detector must establish that all pinned edges were processed for the logical pass, all updates are visible under the chosen synchronous or asynchronous semantics, and no message remains in flight. Otherwise early termination can publish stale labels.

**Conclusion.** Distributed quiescence needs protocol evidence; a local Boolean is insufficient.

### Example 10

**Situation.** Currency edges encode $-\log r_{uv}$ for exchange rate $r_{uv}>0$. A directed cycle has total transformed weight $-0.006$ before fees.

A negative sum means the product of quoted rates exceeds one in the idealized snapshot. It does not establish executable profit: fees, bid/ask direction, quantity limits, precision, latency, and simultaneous availability belong in the model. Validate the exact transformation and cycle under pinned quotes.

**Conclusion.** Negative-cycle mathematics can reveal model opportunity while remaining conditional on data and execution assumptions.

## Cross-Program Connections

- Data Structures Engineering owns edge lists, queues, compact adjacency, predecessor storage, and stable identity structures.
- Database Engineering and Data Engineering own snapshot consistency, change capture, numeric schema, lineage, and atomic output publication.
- Theory of Computation and Mathematical Foundations connect cycle-removal, induction, fixed points, and unbounded optimization.
- Network Engineering applies label correction in routing contexts but adds protocol policy, convergence, topology change, and loop prevention.
- Distributed Systems owns barriers, asynchronous termination, message duplication, checkpoint consistency, and partitioned execution.
- Security Engineering reviews malicious graph size, extreme weights, NaN, overflow, witness spoofing, and denial-of-service inputs.
- [ALGE-036](./036-dijkstra-s-shortest-paths.md) handles nonnegative label setting. [ALGE-038](../ROADMAP.md#block-04--graph-algorithms) develops all-pairs methods; negative-cycle semantics must remain explicit there.

## References

1. Richard Bellman, “On a Routing Problem,” *Quarterly of Applied Mathematics* 16(1), 87–90, 1958, DOI [10.1090/qam/102435](https://doi.org/10.1090/qam/102435). Primary source; bibliographic and paper records checked 2026-09-05.
2. Lester R. Ford Jr., *Network Flow Theory*, RAND Paper P-923, 1956. [RAND bibliographic record](https://www.rand.org/pubs/papers/P923.html), checked 2026-09-05.
3. Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein, *Introduction to Algorithms*, 4th ed., MIT Press, 2022, §22.4. [Official publisher record](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/), checked 2026-09-05.
4. Robert Sedgewick and Kevin Wayne, *Algorithms*, 4th ed., Addison-Wesley, 2011, §4.4. [Author-maintained shortest-path material](https://algs4.cs.princeton.edu/44sp/), checked 2026-09-05.
5. Jeff Erickson, *Algorithms*, 1st ed., 2019, shortest-path chapter. [Author-hosted book](https://jeffe.cs.illinois.edu/teaching/algorithms/), checked 2026-09-05.
6. Ravindra K. Ahuja, Thomas L. Magnanti, and James B. Orlin, *Network Flows: Theory, Algorithms, and Applications*, Prentice Hall, 1993, shortest-path chapters. [MIT-hosted bibliographic record](https://dspace.mit.edu/handle/1721.1/49424), checked 2026-09-05.
7. Boost C++ Libraries, “Bellman-Ford Shortest Paths,” Boost.Graph 1.92.0 documentation. [Official documentation](https://www.boost.org/doc/libs/latest/libs/graph/doc/html/graph/algorithms/shortest_paths/bellman_ford_shortest.html), checked 2026-09-05.
8. SciPy developers, “`scipy.sparse.csgraph.bellman_ford`,” SciPy 1.18.0 documentation. [Official documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csgraph.bellman_ford.html), checked 2026-09-05.

## Exercises

### Exercise 1

Run in-place Bellman-Ford from $s$ on ordered edges $c\to d=1$, $b\to c=-2$, $a\to b=3$, $s\to a=2$, and $s\to d=10$. Show every successful relaxation by pass, the first unchanged pass, final distances, and predecessors.

### Exercise 2

Prove both directions of the reachable negative-cycle detection theorem: an improvement after $n-1$ complete passes implies a reachable negative cycle, and a reachable negative cycle prevents all its edge inequalities from being simultaneously satisfied.

### Exercise 3

An implementation uses signed 64-bit labels, `MIN` as negative infinity, `MAX` as unreachable, relaxes `MAX + weight`, stops when one worker reports no updates, and returns every current label after detecting a cycle. Diagnose at least five defects and give precise repairs.

### Exercise 4

Choose an algorithm and evidence plan for: a nonnegative sparse road snapshot; a dependency DAG with negative credits; a cyclic constraint graph with signed edges; and a dense all-pairs problem. Compare Dijkstra, topological relaxation, Bellman-Ford, and an all-pairs method.

### Exercise 5

Design a resumable service that evaluates signed difference constraints supplied by an untrusted tenant. It must return finite potentials or a source-reachable negative-cycle witness, classify affected variables, survive cancellation, and never publish results from mixed graph revisions.

## Answers to the Exercises

### Answer 1

Initialize $d[s]=0$ and all other labels to infinity. On pass one, the first three edges have infinite tails. Edge $s\to a$ sets $d[a]=2$ with predecessor $s$; edge $s\to d$ sets $d[d]=10$ with predecessor $s$.

On pass two, $a\to b$ sets $d[b]=5$ with predecessor $a$; the earlier $b\to c$ position has already passed. On pass three, $b\to c$ sets $d[c]=3$ with predecessor $b$; $c\to d$ has already passed. On pass four, $c\to d$ improves $d[d]$ from ten to four with predecessor $c$. The next complete pass changes nothing.

Final distances are $d[s]=0$, $d[a]=2$, $d[b]=5$, $d[c]=3$, and $d[d]=4$. Predecessors form path $s\to a\to b\to c\to d$ of weight $2+3-2+1=4$. The trace demonstrates why reverse edge order can require $n-1$ improving passes.

### Answer 2

After $n-1$ passes, assume reachable edge $u\to v$ improves. Its new label witnesses a source walk whose relevant improvement was not captured by any simple path of at most $n-1$ edges. A walk with at least $n$ edges repeats a vertex. If all repeated cycles were nonnegative, removing them would leave a simple source path no heavier than the improving walk. That path has at most $n-1$ edges and should already have bounded $d[v]$, a contradiction. At least one repeated reachable cycle is negative.

Conversely, suppose reachable cycle $v_0\to v_1\to\cdots\to v_k=v_0$ has negative total weight. If every cycle edge were non-relaxable, then $d[v_{i+1}]\le d[v_i]+w_i$ for all $i$. Summing cancels all distance terms and yields $0\le\sum_iw_i<0$, impossible. Thus some cycle edge remains relaxable. Reachability ensures its tail label is finite. Nonnegative-cycle removal is used in the first direction; summing edge inequalities establishes the second.

### Answer 3

First, `MAX + weight` can overflow or fabricate reachability. Branch on the tagged unreachable state before checked addition. Second, finite arithmetic can overflow or underflow; use a wider verified accumulator or explicit bounds checks. Third, `MIN` collides with a possible finite value and saturation can hide continued decreases; use a tagged negative-infinity status.

Fourth, one worker's silence is not global quiescence. Use a barrier for synchronous passes or a termination protocol covering all work and in-flight updates. Fifth, current labels of affected vertices are not finite answers. Extract and validate a reachable negative cycle, propagate forward to classify every affected vertex, and publish $-\infty$ status rather than a transient number.

Also pin the graph revision across $n$, scans, detection, extraction, propagation, and validation; update label, predecessor, and edge identity atomically; distinguish cancellation from completion; and reject NaN or incoherent units.

### Answer 4

For a nonnegative sparse road snapshot, use heap Dijkstra after validating nonnegative weights and pinning direction, units, and restrictions. Check returned paths, edge inequalities, arithmetic, and snapshot identity.

For a dependency DAG with negative credits, first validate acyclicity and a topological order, then relax once in that order in $O(n+m)$. Bellman-Ford would be correct but wastes the proved structure. For a cyclic signed constraint graph, use Bellman-Ford because negative cycles are meaningful inconsistency or unboundedness evidence; return a checked witness and affected classification.

For dense all-pairs output, use an all-pairs method chosen by density, signed weights, and negative-cycle policy—often Floyd-Warshall for a dense matrix, or Johnson-style reweighting for sparse graphs after a Bellman-Ford potential pass. Validate matrix diagonals, sampled path witnesses, triangle inequalities, negative-cycle semantics, and complete output shape. The next module develops those choices.

### Answer 5

Parse tenant vertices and stable directed constraint edges into an immutable content-addressed revision. Validate quotas, endpoint membership, exact signed numeric bounds, units, duplicate identity, and source or super-source policy. A super-source with zero edges to every variable deliberately makes every component reachable when global feasibility is required.

Run deterministic edge-order Bellman-Ford with checked wider arithmetic. At each strict improvement, atomically record label, predecessor vertex, predecessor edge, pass, and revision. A checkpoint contains revision digest, completed-pass count, intra-pass cursor, label and predecessor arrays, changed state, arithmetic policy, and algorithm version. Resume only after digest and invariant validation; cancellation returns incomplete and publishes no potentials.

After $n-1$ completed passes, run a complete detection pass. If unchanged, validate source state, tight predecessor witnesses, and every edge inequality before atomically publishing finite or unreachable potentials. If changed, follow a recorded predecessor $n$ times, collect a directed cycle, verify stable edges and a strictly negative checked sum, and prove source reachability. Traverse forward from all improved heads to classify affected variables as negative infinity. Publish status, witness, affected set, revision, checks, and limitations atomically; retain rate limits, audit logs, and memory/time ceilings for hostile graphs.
