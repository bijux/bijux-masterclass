---
module_id: ALGE-038
program: Algorithm Engineering
level: 1
module_number: 38
title: All-Pairs Shortest Paths
status: complete
last_verified: 2026-09-05
---

# All-Pairs Shortest Paths

## One-Page Review

### Governing question

How can we compute, reconstruct, and certify shortest paths for every ordered vertex pair while choosing an algorithm that matches graph density, signed weights, negative-cycle policy, output size, and numeric representation?

### Essential definitions

- **All-pairs shortest paths** (APSP) returns a distance for each ordered pair $(i,j)$.
- A **distance matrix** stores $D[i,j]$, using infinity when $j$ is unreachable from $i$.
- An **intermediate vertex** is internal to a path, excluding its endpoints.
- A **next-hop matrix** stores the first vertex after $i$ on one selected shortest path to $j$.
- **Floyd-Warshall** admits vertices as intermediates one at a time.
- **Johnson reweighting** converts signed edges to nonnegative reduced costs without changing path order.
- A pair is **affected** when its source can reach a negative cycle and that cycle can reach its target.
- **Output sensitivity** matters because an explicit $n\times n$ answer already costs $\Theta(n^2)$ space.

### Central model, mechanism, or theorem

Order vertices $v_1,\ldots,v_n$. Let $D^{(k)}[i,j]$ be the minimum weight of an $i$-to-$j$ path whose intermediate vertices are drawn from $\{v_1,\ldots,v_k\}$. A best path either avoids $v_k$ or uses it, giving

$$
D^{(k)}[i,j]=\min\left(D^{(k-1)}[i,j],
D^{(k-1)}[i,k]+D^{(k-1)}[k,j]\right).
$$

Initialization uses zero on the diagonal, the lightest direct parallel edge off-diagonal, and infinity otherwise. In-place Floyd-Warshall evaluates the recurrence in $O(n^3)$ time and $O(n^2)$ output storage. Afterward, $D[k,k]<0$ identifies a negative cycle through the closure; every pair $(i,j)$ with finite $D[i,k]$ and $D[k,j]$ is unbounded below.

### Critical invariants

- Vertex order, edge set, directedness, weights, arithmetic, and graph revision are fixed.
- Phase $k$ permits exactly the first $k$ vertices as intermediates.
- Infinity is checked before addition, and finite addition cannot overflow or produce NaN.
- The diagonal begins at zero even if no explicit self-edge exists; a negative self-edge may improve it.
- Parallel edges initialize to their minimum weight, not the last observed value.
- A next-hop update is atomic with its strict distance improvement.
- Negative diagonal entries are detection evidence, not finite self-distances.
- Affected pairs are propagated through reachability on both sides of a negative cycle.
- Path reconstruction has a hop/cycle bound and never interprets affected pairs as finite.
- Published matrices share one vertex-index map and snapshot identifier.

### Common failures

Typical failures include using zero to mean “no edge”; omitting diagonal zeros; overwriting a lighter parallel edge; adding infinity; overflowing a candidate; swapping loop order so the phase invariant fails; updating next hops on equality and creating cycles; returning a finite matrix after finding a negative diagonal; marking every pair affected by any negative cycle; reconstructing an unreachable pair; mixing vertex-index versions; choosing cubic dense work for a huge sparse graph without justification; and forgetting that materializing all pairs itself can dominate memory and I/O.

### Compact example

If $a\to b=3$, $b\to c=-2$, and $a\to c=8$, then admitting $b$ changes $D[a,c]$ from eight to $3-2=1$. The negative edge is valid. Adding $c\to b=1$ creates cycle $b\to c\to b$ of weight $-1$; then every pair whose source reaches $b$ and whose target is reachable from $b$ is unbounded below.

### Connections

[ALGE-033](./033-topological-ordering.md) supplies the DAG special case, [ALGE-036](./036-dijkstra-s-shortest-paths.md) supplies nonnegative single-source closure, and [ALGE-037](./037-bellman-ford-and-negative-weights.md) supplies signed single-source detection and potentials. [ALGE-039](../ROADMAP.md#block-04--graph-algorithms) next returns to disjoint-set mechanisms in graph algorithms.

## Governing Question

What exact matrix, path, reachability, and negative-cycle contract should an APSP service provide, and when should it use Floyd-Warshall, repeated single-source search, Johnson's algorithm, or a specialized alternative?

APSP is not merely “run shortest path many times.” The explicit answer has quadratic cardinality, negative cycles affect source-target pairs rather than only vertices, and path reconstruction needs consistent next-hop evidence. Density, query shape, update rate, memory, numeric policy, and output format are part of algorithm selection.

## Why This Matters

All-pairs distances support network analysis, dependency impact, routing tables, facility placement, graph metrics, scheduling, constraint closure, and database reachability. Dense closure is often simpler and more auditable than many frontier searches. Sparse graphs may favor Johnson reweighting or repeated Dijkstra.

Floyd-Warshall is also a canonical dynamic program: the phase invariant explains why loop order matters and generalizes to Boolean transitive closure and other algebraic closures. Its short implementation can still fail through infinity arithmetic, aliasing, negative cycles, path-witness corruption, or a mismatched vertex-index map.

## Prerequisites and Retrieval

Retrieve directed paths and cycles; adjacency matrices and lists; relaxation; Dijkstra and Bellman-Ford; dynamic-programming recurrences; induction; triangle inequalities; exact signed arithmetic, infinity, overflow, and asymptotic output bounds. Review [ALGE-036](./036-dijkstra-s-shortest-paths.md) and [ALGE-037](./037-bellman-ford-and-negative-weights.md).

## Learning Objectives

After completing this module, you should be able to:

1. specify APSP distances, paths, unreachable pairs, and negative-cycle-affected pairs;
2. derive and prove the Floyd-Warshall intermediate-set recurrence;
3. initialize diagonal, parallel edges, infinity, and next hops correctly;
4. implement deterministic Floyd-Warshall with bounded reconstruction;
5. detect negative cycles from the final diagonal and classify affected pairs;
6. derive Johnson reduced costs and prove path-order preservation;
7. compare dense cubic closure with repeated single-source methods;
8. reason about quadratic output, memory layout, blocking, and publication;
9. validate matrices with paths, triangle inequalities, reachability, and independent oracles;
10. handle arithmetic, snapshots, cancellation, incremental updates, and partial-query boundaries.

## Core Exposition

### Define the complete result

For finite directed multigraph $G=(V,E)$ with signed additive weights, ordinary APSP asks for $\delta(i,j)$ for every ordered pair. The semantic states are unreachable ($+\infty$), finite optimum, and unbounded below ($-\infty$) when an $i$-reachable negative cycle can reach $j$.

Decide whether the product contains only distances, one path per finite pair, next hops, predecessor rows, reachability, affected-pair flags, or an on-demand query interface. An explicit distance matrix has $n^2$ cells: at eight bytes per cell, $50{,}000^2$ cells require 20,000,000,000 bytes before witnesses and overhead.

### Derive Floyd-Warshall

Fix stable vertex order $v_1,\ldots,v_n$. Before any intermediate is admitted, $D^{(0)}[i,i]=0$, $D^{(0)}[i,j]$ is the minimum direct-edge weight for $i\ne j$, and otherwise infinity.

Consider an optimal path allowed to use intermediates through $v_k$. If it avoids $v_k$, its value is $D^{(k-1)}[i,j]$. If it uses $v_k$ and no relevant negative cycle makes the pair unbounded, split at $v_k$: both pieces use only earlier allowed intermediates. Taking the cheaper case yields the recurrence in the review.

Induction on $k$ proves the phase invariant. The outer loop must be the intermediate vertex. Arbitrarily placing `k` inside `i` or `j` can allow and then depend on vertices outside the claimed phase, invalidating the proof even when some test graphs happen to pass.

### Implement distances and one selected path

This exact-integer implementation retains the lightest parallel edge, rejects unknown endpoints, guards infinity before addition, updates next hops only on strict improvement, and reconstructs with a vertex-count bound.

<!-- bijux-verify: {"id":"deterministic-floyd-warshall","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"row_a=(('a', '0'), ('b', '3'), ('c', '1'), ('d', '3'))\nrow_b=(('a', 'inf'), ('b', '0'), ('c', '-2'), ('d', '0'))\nrow_c=(('a', 'inf'), ('b', '6'), ('c', '0'), ('d', '2'))\nrow_d=(('a', 'inf'), ('b', '4'), ('c', '2'), ('d', '0'))\npath_a_d=('a', 'b', 'c', 'd')\nnegative_diagonal=()\nvalid=True\n","stderr":""}} -->
```python
from math import inf


def floyd_warshall(vertices, edges):
    vertices = tuple(sorted(set(vertices)))
    known = set(vertices)
    distance = {(i, j): (0 if i == j else inf)
                for i in vertices for j in vertices}
    next_hop = {(i, j): None for i in vertices for j in vertices}
    seen = set()
    for edge_id, tail, head, weight in edges:
        if edge_id in seen or tail not in known or head not in known:
            raise ValueError(f"invalid edge: {edge_id}")
        if not isinstance(weight, int):
            raise ValueError("weights must be exact integers")
        seen.add(edge_id)
        if weight < distance[tail, head]:
            distance[tail, head] = weight
            next_hop[tail, head] = head

    for middle in vertices:
        for source in vertices:
            if distance[source, middle] == inf:
                continue
            for target in vertices:
                if distance[middle, target] == inf:
                    continue
                proposal = (distance[source, middle]
                            + distance[middle, target])
                if proposal < distance[source, target]:
                    distance[source, target] = proposal
                    next_hop[source, target] = next_hop[source, middle]
    return vertices, distance, next_hop


def path_to(vertices, source, target, distance, next_hop):
    if distance[source, target] == inf:
        return None
    if source == target:
        return (source,)
    path = [source]
    for _ in vertices:
        source = next_hop[source, target]
        if source is None:
            raise ValueError("finite distance lacks next-hop evidence")
        path.append(source)
        if source == target:
            return tuple(path)
    raise ValueError("next-hop cycle")


def validate(vertices, edges, distance, next_hop):
    for source in vertices:
        if distance[source, source] != 0:
            return False
        for target in vertices:
            if distance[source, target] != inf:
                path_to(vertices, source, target, distance, next_hop)
    for _, tail, head, weight in edges:
        for source in vertices:
            if distance[source, tail] != inf:
                if distance[source, head] > distance[source, tail] + weight:
                    return False
    return True


vertices = {"a", "b", "c", "d"}
edges = (
    ("ab", "a", "b", 3), ("ac", "a", "c", 8),
    ("ad", "a", "d", 7), ("bc", "b", "c", -2),
    ("cd", "c", "d", 2), ("db", "d", "b", 4),
)
vertices, distance, next_hop = floyd_warshall(vertices, edges)
display = lambda value: "inf" if value == inf else str(value)
for source in vertices:
    row = tuple((target, display(distance[source, target]))
                for target in vertices)
    print(f"row_{source}={row}")
print(f"path_a_d={path_to(vertices, 'a', 'd', distance, next_hop)}")
print("negative_diagonal=" + str(tuple(
    vertex for vertex in vertices if distance[vertex, vertex] < 0)))
print(f"valid={validate(vertices, edges, distance, next_hop)}")
```

The validator checks selected path termination and every source-plus-edge inequality. For full certificate strength, it should also recompute each selected path weight and independently check reachability; bounded tests can enumerate simple paths.

### Detect and propagate negative cycles

After closure, $D[k,k]<0$ proves a negative closed walk and therefore contains a negative cycle. Pair $(i,j)$ is affected exactly when some such $k$ satisfies $D[i,k]<+\infty$ and $D[k,j]<+\infty$. Mark that pair $-\infty$ rather than returning its transient numeric cell.

Not every pair is affected. Sources unable to reach the cycle and targets unreachable from it retain their finite or unreachable status. Path reconstruction must reject affected pairs. For diagnostics, extract a concrete directed negative cycle using Bellman-Ford predecessor evidence or a witness-capable matrix scheme; a negative diagonal alone is a detection certificate, not a human-readable edge witness.

### Prove Johnson reweighting

For sparse signed graphs without negative cycles, add a super-source with zero edges to all vertices and run Bellman-Ford to obtain potentials $h(v)$. Define reduced edge weight

$$
w'(u,v)=w(u,v)+h(u)-h(v).
$$

Bellman-Ford inequalities give $h(v)\le h(u)+w(u,v)$, hence $w'(u,v)\ge0$. Along path $p$ from $s$ to $t$, potential terms telescope:

$$
w'(p)=w(p)+h(s)-h(t).
$$

Every $s$-to-$t$ path receives the same offset, so path ordering is preserved. Run Dijkstra from every source under $w'$, then recover $\delta(s,t)=\delta'(s,t)-h(s)+h(t)$. Johnson costs one Bellman-Ford pass plus $n$ nonnegative searches and is commonly preferable for sparse graphs.

### Compare costs and output

Floyd-Warshall takes $\Theta(n^3)$ arithmetic/comparison work and $\Theta(n^2)$ matrix space. Its regular memory access, simple proof, and negative-diagonal test suit dense graphs and moderate matrices. Blocking can improve cache behavior but must preserve dependency order between diagonal, row/column, and remaining blocks.

Repeated binary-heap Dijkstra is appropriate for nonnegative sparse graphs. Johnson extends that plan to signed sparse graphs without negative cycles. Repeated Bellman-Ford is usually expensive. If only a few sources or targets are queried, do not materialize APSP; use source-limited, reverse-graph, or indexed methods and name the reduced output contract.

### Validate and operate the matrix

Check dimensions, vertex-index bijection, diagonal policy, unreachable states, negative-cycle status, and snapshot digest. For every finite pair with a requested witness, verify directed edge identities and recompute weight. Check triangle inequalities $D[i,j]\le D[i,k]+D[k,j]$ when operands are finite and unaffected. Compare reachability with independent traversal.

Metamorphic checks include vertex renaming, edge-record permutation, adding an isolated vertex, adding a dominated parallel edge, transposing the graph and matrix together, and scaling all exact weights by a positive constant. Increasing one edge cannot reduce a finite distance; decreasing one edge cannot increase one, though negative-cycle status may change.

Pin vertices, edges, weights, index map, algorithm, matrices, witnesses, and validation to one immutable revision. Cancellation returns incomplete tiles or rows only under an explicit partial-result contract. Publish distance/status matrix, index dictionary, witness policy, negative-cycle evidence, arithmetic metadata, graph digest, and validation outcome atomically.

Current [SciPy 1.18.0 shortest-path documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csgraph.shortest_path.html) exposes automatic, Floyd-Warshall, Dijkstra, Bellman-Ford, and Johnson choices and warns that directed-false behavior can be incorrect when opposing directed weights differ. Treat such behavior as version-specific evidence, not a universal graph-model rule.

## Definitions and Notation

- $D^{(k)}[i,j]$: best $i$-to-$j$ path using only the first $k$ vertices internally.
- $D[i,j]$: final distance/status matrix cell.
- $N[i,j]$: selected next hop from $i$ toward $j$.
- **closure:** completion of all intermediate phases.
- **negative diagonal:** a cell $D[k,k]<0$ after signed closure.
- **reduced cost:** Johnson weight $w'(u,v)=w(u,v)+h(u)-h(v)$.
- **potential:** Bellman-Ford label $h(v)$ used for reweighting.
- **affected pair:** source-target pair whose walks are unbounded below.
- **matrix blocking:** partitioning cells into cache-sized tiles under preserved dependencies.

## Mechanisms, Invariants, or Proof Structure

Initialization represents paths with no intermediate vertices. Phase $k$ partitions eligible paths into those avoiding or using $v_k$. Induction proves recurrence closure. Strict next-hop updates retain one improving decomposition. Negative diagonals detect negative closed walks; two-sided reachability classifies affected pairs. Johnson potentials establish nonnegative reduced edges, and telescoping establishes path-order preservation. Finite certificates combine reachability, reconstructed path equality, and all triangle or edge inequalities.

## Alternatives and Trade-Offs

- **Floyd-Warshall:** dense, regular, simple, cubic, quadratic storage.
- **Repeated Dijkstra:** sparse and nonnegative; heap and adjacency choices dominate.
- **Johnson:** sparse and signed without negative cycles; more moving parts and conversion arithmetic.
- **Repeated DAG relaxation:** excellent when one validated topological order applies.
- **Boolean Warshall:** reachability rather than weighted distance, using OR/AND closure.
- **Partial-source computation:** avoids unused rows but is not APSP completeness.
- **Precomputed indexes:** accelerate query workloads at the cost of update and model-specific complexity.

## Failure Modes and Misconceptions

- Zero is not a safe absence marker when zero-weight edges exist.
- Negative edges do not alone invalidate Floyd-Warshall or Johnson's potential phase.
- A negative diagonal must change affected-pair semantics; it is not just a warning.
- Loop permutation is not automatically legal in an in-place dynamic program.
- Next-hop ties can cycle if equality rewrites lack a well-founded policy.
- One negative cycle does not affect sources that cannot reach it or targets it cannot reach.
- Johnson reduced edges are nonnegative only when potentials satisfy every edge inequality.
- Explicit APSP cannot use subquadratic output space while materializing every pair.
- Cache blocking changes schedule, not recurrence obligations.
- A complete matrix for yesterday's graph is not valid for today's snapshot.

## Worked Examples

### Example 1

**Situation.** $a\to b=3$, $b\to c=-2$, $a\to c=8$. Admitting $b$ proposes $3+(-2)=1$, so $D[a,c]$ improves to one and next hop becomes $b$. **Conclusion.** The recurrence combines two already-closed subpaths.

### Example 2

**Situation.** Parallel edges $a\to b$ weigh seven and two. Initialization must store two regardless of input order; last-write storage could retain seven. **Conclusion.** Parallel-edge minimization is a correctness obligation.

### Example 3

**Situation.** $D[a,k]=+\infty$ and $D[k,b]=-5$. A maximum-integer sentinel plus negative five can appear finite. Guard the infinity operand before checked addition. **Conclusion.** Extended arithmetic must not be implemented as unchecked sentinel arithmetic.

### Example 4

**Situation.** Final diagonal has $D[c,c]=-4$, with finite $D[a,c]$ and $D[c,d]$, but $D[e,c]=+\infty$. Pairs $(a,d)$ and $(c,d)$ are affected; $(e,d)$ is not affected through this cycle. **Conclusion.** Negative-cycle effects require reachability on both sides.

### Example 5

**Situation.** Potentials are $h(u)=2$, $h(v)=-3$, and edge $u\to v$ weighs $-4$. Reduced cost is $-4+2-(-3)=1\ge0$. Every $s$-to-$t$ path receives offset $h(s)-h(t)$. **Conclusion.** Reweighting removes negative edges without changing within-pair path order.

### Example 6

**Situation.** Four vertices produce 16 distance cells. At eight bytes each the raw matrix is 128 bytes; a next-hop matrix of four-byte indices adds 64 bytes. At large $n$, both scale quadratically. **Conclusion.** Witness and output representation belong in capacity planning.

### Example 7

**Situation.** A next-hop row rewrites equal-cost choices $a\to b$ and $a\to c$ as later phases arrive. Without strict updates, zero-cost alternatives can make reconstruction alternate indefinitely. **Conclusion.** Distance correctness does not guarantee witness termination.

### Example 8

**Situation.** A sparse graph has one million vertices but only ten requested sources. A full matrix has $10^{12}$ cells, while ten source searches output at most ten million cells. **Conclusion.** Query scope can dominate the algorithmic decision.

### Example 9

**Situation.** Transpose every directed edge and recompute APSP. The new matrix should equal the transpose of the original status/distance matrix, including affected-pair direction. **Conclusion.** Graph transposition is a strong metamorphic test.

### Example 10

**Situation.** An edge changes after half the matrix tiles are computed. Combining old and new tiles can violate triangle inequalities and path evidence. Restart or use a proved incremental algorithm bound to versioned dependencies. **Conclusion.** Atomic snapshot identity is part of APSP correctness.

## Cross-Program Connections

- Data Structures Engineering owns matrices, compressed sparse layouts, heaps, maps, and witness storage.
- Database and Data Architecture Engineering own graph snapshots, indexes, materialized views, lineage, and atomic publication.
- Computer Architecture influences blocking, locality, vectorization, bandwidth, and numeric width.
- Distributed Systems owns partitioned closure schedules, barriers, checkpoint consistency, and termination.
- Network Engineering consumes routing distances but adds policy and dynamic topology.
- Security Engineering reviews adversarial size, overflow, NaN, index confusion, and resource exhaustion.

## References

1. Robert W. Floyd, “Algorithm 97: Shortest Path,” *Communications of the ACM* 5(6), 345, 1962, DOI [10.1145/367766.368168](https://doi.org/10.1145/367766.368168). Primary source checked 2026-09-05.
2. Stephen Warshall, “A Theorem on Boolean Matrices,” *Journal of the ACM* 9(1), 11–12, 1962, DOI [10.1145/321105.321107](https://doi.org/10.1145/321105.321107). Primary-source record checked 2026-09-05.
3. Donald B. Johnson, “Efficient Algorithms for Shortest Paths in Sparse Networks,” *Journal of the ACM* 24(1), 1–13, 1977, DOI [10.1145/321992.321993](https://doi.org/10.1145/321992.321993). Primary source checked 2026-09-05.
4. Thomas H. Cormen et al., *Introduction to Algorithms*, 4th ed., MIT Press, 2022, §§23.1–23.3. [Official publisher record](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/), checked 2026-09-05.
5. Jeff Erickson, *Algorithms*, 1st ed., 2019, all-pairs shortest-path material. [Author-hosted book](https://jeffe.cs.illinois.edu/teaching/algorithms/), checked 2026-09-05.
6. SciPy developers, “`scipy.sparse.csgraph.shortest_path`,” SciPy 1.18.0 manual. [Official documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csgraph.shortest_path.html), checked 2026-09-05.

## Exercises

### Exercise 1

Initialize and trace Floyd-Warshall for vertices $(a,b,c)$ with edges $a\to b=4$, $b\to c=-1$, $a\to c=7$, and $c\to a=3$. Show every strict improvement and final matrix.

### Exercise 2

Prove the intermediate-set recurrence and explain why the outer intermediate loop is required by the in-place proof.

### Exercise 3

Diagnose an implementation that uses zero for absent edges, `int32` unchecked addition, last-write parallel edges, equality next-hop updates, and returns its numeric matrix despite a negative diagonal.

### Exercise 4

Choose Floyd-Warshall, repeated Dijkstra, Johnson, or limited-source computation for a dense 2,000-vertex signed graph, a sparse nonnegative 100,000-vertex graph requiring every row, and a sparse million-vertex graph with twelve source queries.

### Exercise 5

Design a versioned APSP service that supports path reconstruction, negative-cycle affected-pair status, cancellation, and independent validation without mixing graph revisions.

## Answers to the Exercises

### Answer 1

Initialize diagonal zeros, $D[a,b]=4$, $D[b,c]=-1$, $D[a,c]=7$, $D[c,a]=3$, and other cells infinity. Admitting $a$ improves $D[c,b]$ to $3+4=7$. Admitting $b$ improves $D[a,c]$ from seven to $4-1=3$. Admitting $c$ improves $D[b,a]$ to $-1+3=2$. No other strict improvement occurs.

Rows $(a,b,c)$ are $(0,4,3)$, $(2,0,-1)$, and $(3,7,0)$. Cycle $a\to b\to c\to a$ weighs six, so no diagonal becomes negative.

### Answer 2

For phase $k$, any eligible optimal path either avoids $v_k$, giving the preceding-phase value, or uses it. With no relevant negative-cycle repetition, split at $v_k$ into $i\to v_k$ and $v_k\to j$ pieces whose internal vertices belong to earlier phases. Their sum gives the second recurrence term; taking the minimum covers both exhaustive cases. Initialization covers paths with no intermediate.

Induction on $k$ proves the invariant. Making `k` outermost completes every preceding-phase subproblem before phase-$k$ combinations use it. Arbitrary loop permutation can read cells updated using later intermediates and destroys that induction; a different schedule needs its own dependency proof.

### Answer 3

Use a tagged absence/infinity state so legitimate zero edges survive. Retain the minimum parallel-edge weight independent of record order. Guard infinite operands and perform checked wider addition so overflow cannot fabricate improvements. Update next hops only on strict distance improvement or a proved well-founded tie rule, and bound reconstruction hops.

A negative diagonal means some pairs are unbounded below. For each negative-diagonal vertex $k$, mark pairs with finite source-to-$k$ and $k$-to-target reachability as affected and reject finite reconstruction for them. Return tagged $-\infty$, finite, or unreachable states plus cycle evidence and snapshot identity—not the transient numeric matrix.

### Answer 4

For a dense 2,000-vertex signed graph, Floyd-Warshall is a strong default if cubic time and quadratic memory fit; it handles signed edges and exposes negative diagonals with regular storage. For a sparse nonnegative 100,000-vertex graph requiring every row, repeated Dijkstra matches sparsity, though the $10^{10}$-cell output may itself make the request infeasible and should trigger capacity review.

For a sparse million-vertex graph with twelve sources, run twelve source-limited searches rather than APSP: Dijkstra if all reachable weights are nonnegative, or an appropriate signed method/potential plan otherwise. The product must be labeled twelve-source distances, not all pairs.

### Answer 5

Assign stable vertex and edge identities and build an immutable content-addressed graph revision with declared directedness, exact numeric policy, and vertex-index bijection. Choose the algorithm from density and signed-cycle requirements. Checkpoint revision, algorithm version, phase/source and cursor, matrices or rows, witness state, and arithmetic metadata; validate the digest before resume. Cancellation publishes only explicit incomplete status unless a separately validated partial-row contract exists.

For finite pairs, validate reachability, bounded next-hop termination, every directed witness edge, recomputed path weight, and triangle/edge inequalities. For each negative diagonal or Bellman-Ford witness, validate a directed negative cycle and classify pairs by source-to-cycle and cycle-to-target reachability. Atomically publish status/distance cells, index map, paths or next hops, graph digest, cycle evidence, validation outcome, and limitations. Never combine tiles, rows, witnesses, or indexes from different revisions.
