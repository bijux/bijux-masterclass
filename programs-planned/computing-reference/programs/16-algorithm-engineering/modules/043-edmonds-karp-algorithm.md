---
module_id: ALGE-043
program: Algorithm Engineering
level: 1
module_number: 43
title: Edmonds-Karp Algorithm
status: complete
last_verified: 2026-09-05
---

# Edmonds-Karp Algorithm

## One-Page Review

### Governing question

Why does choosing a shortest residual augmenting path with breadth-first search turn Ford-Fulkerson into a capacity-independent polynomial algorithm, and how should that guarantee be preserved in an implementation?

### Essential definitions

- **Edmonds-Karp** is Ford-Fulkerson with an augmenting path having the fewest residual edges.
- An unweighted **breadth-first search (BFS)** from $s$ finds residual distances $d_f(v)$ and a shortest $s$-$t$ path.
- A residual edge is **critical** in an augmentation when its residual capacity equals the path bottleneck and becomes zero.
- A **distance label** is the number of residual edges in a shortest path from $s$ to a vertex; unreachable vertices have distance infinity.
- The **augmentation count** is bounded combinatorially, independently of capacity magnitudes.
- The standard adjacency-list running time is $O(VE^2)$: $O(VE)$ augmentations, each using $O(E)$ graph work up to conventional $V+E$ terms.

### Central model, mechanism, or theorem

Repeat BFS over positive residual directions, recover an $s$-$t$ predecessor path, augment by its bottleneck, and stop when BFS cannot reach $t$.

After an augmentation along a shortest residual path, shortest residual distances from $s$ never decrease. If a directed residual edge $(u,v)$ becomes critical, disappears, and later becomes critical again, it must first reappear through flow sent on its reverse; this forces the distance to its tail to increase by at least two. Each directed residual edge can therefore be critical only $O(V)$ times. Since every augmentation saturates at least one critical edge, there are $O(VE)$ augmentations and $O(VE^2)$ total adjacency-list time.

### Critical invariants

- The current original-edge flow remains feasible and matches its residual graph.
- BFS traverses exactly positive residual directions from one pinned snapshot.
- A vertex is discovered once; its predecessor records residual edge identity and direction.
- Every predecessor edge moves from level $i$ to level $i+1$.
- The recovered $s$-$t$ path has minimum edge count in the current residual graph.
- Augmentation uses one positive bottleneck and commits atomically.
- Residual distance labels are nondecreasing across completed augmentations.
- At least one path edge becomes critical in every augmentation.
- `optimal` is returned only after residual exhaustion and certificate validation.

### Common failures

Failures include using a priority queue or weighted capacities instead of unweighted BFS levels; marking vertices only when dequeued; terminating on discovery without a valid predecessor edge; storing only predecessor vertices when parallel edges exist; traversing zero residuals; reusing stale distances after augmentation; claiming $O(E^2)$ by forgetting the $V$ factor; deriving the bound from capacity values; assuming BFS minimizes bottleneck or total capacity; publishing a resource-limited flow as optimal; and using a residual representation whose reverse pairing is corrupt.

### Compact example

If the residual graph offers paths with edge counts two and four, Edmonds-Karp chooses a two-edge path even when its bottleneck is smaller. This choice is about combinatorial distance, not immediate flow gain. The monotone evolution of shortest-path levels, rather than large bottlenecks, supports the polynomial bound.

### Connections

[ALGE-031](./031-breadth-first-search.md) supplies BFS invariants, [ALGE-041](./041-flow-networks-and-residual-graphs.md) supplies residual state, and [ALGE-042](./042-ford-fulkerson-method.md) supplies augmentation and stopping correctness. [ALGE-044](../ROADMAP.md#block-05--flows-matching-and-combinatorial-optimization) will batch work in level graphs with Dinic's algorithm; [ALGE-045](../ROADMAP.md#block-05--flows-matching-and-combinatorial-optimization) develops the flow-cut theorem.

## Governing Question

Given a finite directed flow network, how does shortest-residual-path selection produce a maximum flow with a capacity-independent $O(VE^2)$ operation bound, and what representation, arithmetic, lifecycle, and evidence disciplines keep an implementation faithful to that proof?

The essential improvement is not that BFS is usually fast. It is that BFS exposes residual levels whose evolution can be charged to directed edges. The path policy creates a structural progress measure even when bottleneck sizes are tiny or capacities are arbitrary exact reals.

## Why This Matters

Ford-Fulkerson shows how residual augmentation works, but arbitrary path choices may take pseudo-polynomial time on integer inputs and may fail to terminate on arbitrary real inputs. Edmonds-Karp replaces numeric progress analysis with a combinatorial one. It is a canonical example of algorithm engineering: a small policy constraint makes the proof and operational guarantee substantially stronger.

The algorithm is also a bridge to more advanced flow methods. Dinic retains the same shortest-path levels but sends a blocking flow before rebuilding them. Push-relabel replaces complete paths with local admissible pushes. Understanding why levels are monotone makes these later designs easier to compare without reducing them to library names.

## Prerequisites and Retrieval

Retrieve BFS queue and discovery invariants, directed multigraphs, residual capacity, forward/reverse pairing, path reconstruction, bottleneck augmentation, cuts, asymptotic charging arguments, exact arithmetic, and snapshot transactions. Review [ALGE-031](./031-breadth-first-search.md), [ALGE-041](./041-flow-networks-and-residual-graphs.md), and [ALGE-042](./042-ford-fulkerson-method.md).

## Learning Objectives

After completing this module, you should be able to:

1. specify Edmonds-Karp as shortest-edge-count residual augmentation;
2. implement residual BFS with stable predecessor edge-directions;
3. prove that BFS predecessor paths are shortest in edge count;
4. prove residual distances from $s$ never decrease after augmentation;
5. define a critical edge and derive its two-level recurrence gap;
6. derive $O(VE)$ augmentations and $O(VE^2)$ graph-operation time;
7. distinguish capacity independence from constant-time arbitrary-precision arithmetic;
8. validate optimality, feasibility, path-policy, and trace evidence separately;
9. govern memory, cancellation, snapshots, determinism, and adversarial inputs;
10. choose between Edmonds-Karp and later maximum-flow algorithms for a stated context.

## Core Exposition

### Specify shortest residual augmentation

Let $f$ be a feasible flow on a finite directed multigraph. Build adjacency over every positive forward or reverse residual direction. Run ordinary unweighted BFS from $s$. When a vertex $v$ is first discovered from $u$, set

$$
d_f(v)=d_f(u)+1
$$

and record the exact residual edge used. If $t$ is discovered, its predecessor chain gives a path with the fewest residual edges. Compute the minimum residual capacity on this path and augment exactly as in Ford-Fulkerson. Rebuild BFS state after every augmentation because the residual graph changed.

The policy minimizes edge count, not capacity, cost, latency, bottleneck, or physical distance. Any tie among shortest paths is legal. A stable adjacency order makes traces reproducible but is not needed for the asymptotic proof.

### Preserve the BFS proof obligation

BFS enqueues a vertex when first discovered, not when later removed. The queue contains vertices in nondecreasing distance. Every residual edge examined from a distance-$i$ vertex either discovers its head at $i+1$ or reaches an already discovered vertex no farther away. Thus the recorded predecessor chain to $t$ has length $d_f(t)$ and is shortest.

With parallel and anti-parallel originals, a predecessor vertex is insufficient. Store `(previous_vertex, residual_slot)` or `(previous_vertex, original_edge_id, direction)`. The latter identifies whether augmentation increases or cancels which logical flow.

### Prove distance monotonicity

Let $f'$ result from augmenting $f$ along a shortest residual path. Consider any shortest residual path to vertex $v$ in $G_{f'}$. Traverse it from $s$ and compare each edge with $G_f$.

An edge already present in $G_f$ obeyed $d_f(y)\le d_f(x)+1$. A newly created residual edge must be the reverse of an edge $(y,x)$ used on the augmenting path. Along that old shortest path, $d_f(x)=d_f(y)+1$, so for the new edge $(x,y)$, $d_f(y)=d_f(x)-1\le d_f(x)+1$.

Applying these inequalities along a new shortest path shows it cannot reach a vertex at a level below its previous shortest level. Hence

$$
d_{f'}(v)\ge d_f(v)
$$

for every vertex reachable before and after, treating infinity in the usual extended order. The proof concerns distances after completed atomic augmentations, not partially updated residual state.

### Charge critical edges

Every augmentation has at least one residual edge whose capacity equals the bottleneck; that directed edge becomes saturated and disappears. Call it critical. Suppose residual direction $(u,v)$ is critical at one augmentation and later critical again. Between those events it must reappear, which requires an augmentation using the reverse direction $(v,u)$.

At the first critical event, the edge lies on a shortest path, so $d(v)=d(u)+1$. When the reverse is later used on a shortest path, its levels satisfy $d'(u)=d'(v)+1$. Distance monotonicity gives $d'(v)\ge d(v)$. Combining,

$$
d'(u)=d'(v)+1\ge d(v)+1=d(u)+2.
$$

Thus the tail level of a directed residual edge rises by at least two before that direction can be critical again. Finite reachable levels are at most $|V|-1$, so each directed residual edge becomes critical only $O(V)$ times.

There are $O(E)$ residual directions when each original edge has a paired reverse slot. Every augmentation has a critical edge. Therefore the number of augmentations is $O(VE)$. BFS plus path recovery and updates cost $O(V+E)$, conventionally $O(E)$ after restricting to relevant nontrivial networks, yielding $O(VE^2)$.

### Interpret the bound honestly

The augmentation bound does not depend on the numeric values of capacities. Under exact arithmetic, it supplies finite termination even when positive bottlenecks are not integral. This resolves the arbitrary-path nontermination problem by controlling path choice.

The standard bound counts graph and arithmetic operations. If capacities are huge integers or exact rationals, addition, subtraction, minimum comparison, and storage do not necessarily take constant time. A bit-complexity account must include operand widths and representation growth. Floating arithmetic still requires an explicit tolerance and feasibility policy; a combinatorial iteration bound does not repair corrupted residual comparisons.

### Execute deterministic Edmonds-Karp

The following implementation derives residual directions from logical flows, uses stable sorted adjacency, marks vertices on discovery, stores exact edge-directions, applies updates to a copy, and validates every committed flow.

<!-- bijux-verify: {"id":"edmonds-karp-bfs","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"augmentations=((2, ('sa:f', 'at:f'), 2), (2, ('sb:f', 'bt:f'), 3), (3, ('sa:f', 'ab:f', 'bt:f'), 1))\nflows=(('ab', 1), ('at', 2), ('bt', 4), ('sa', 3), ('sb', 3))\nvalue=6\nvalid=True\nresidual_path=False\n","stderr":""}} -->
```python
from collections import deque


edges = {
    "sa": ("s", "a", 4), "sb": ("s", "b", 3),
    "ab": ("a", "b", 2), "at": ("a", "t", 2),
    "bt": ("b", "t", 4),
}
vertices = {"s", "a", "b", "t"}


def residual_adjacency(flow):
    adjacency = {vertex: [] for vertex in vertices}
    for edge_id, (tail, head, capacity) in sorted(edges.items()):
        if flow[edge_id] < capacity:
            adjacency[tail].append((head, edge_id, "f", capacity - flow[edge_id]))
        if flow[edge_id] > 0:
            adjacency[head].append((tail, edge_id, "r", flow[edge_id]))
    for steps in adjacency.values():
        steps.sort(key=lambda step: (step[0], step[1], step[2]))
    return adjacency


def bfs_path(flow):
    adjacency = residual_adjacency(flow)
    distance = {"s": 0}
    predecessor = {}
    queue = deque(["s"])
    while queue and "t" not in distance:
        tail = queue.popleft()
        for head, edge_id, direction, residual in adjacency[tail]:
            if head not in distance:
                distance[head] = distance[tail] + 1
                predecessor[head] = (tail, edge_id, direction, residual)
                queue.append(head)
    if "t" not in distance:
        return None
    path = []
    cursor = "t"
    while cursor != "s":
        prior, edge_id, direction, residual = predecessor[cursor]
        path.append((edge_id, direction, residual))
        cursor = prior
    return tuple(reversed(path))


def validate(flow):
    if set(flow) != set(edges):
        return False
    balance = {vertex: 0 for vertex in vertices}
    for edge_id, (tail, head, capacity) in edges.items():
        amount = flow[edge_id]
        if not isinstance(amount, int) or not 0 <= amount <= capacity:
            return False
        balance[tail] -= amount
        balance[head] += amount
    return balance["a"] == balance["b"] == 0 and -balance["s"] == balance["t"]


def solve():
    flow = {edge_id: 0 for edge_id in edges}
    trace = []
    while (path := bfs_path(flow)) is not None:
        delta = min(residual for _, _, residual in path)
        candidate = dict(flow)
        for edge_id, direction, _ in path:
            candidate[edge_id] += delta if direction == "f" else -delta
        if not validate(candidate):
            raise AssertionError("infeasible augmentation")
        flow = candidate
        trace.append((len(path), tuple(f"{e}:{d}" for e, d, _ in path), delta))
    return flow, tuple(trace)


flow, trace = solve()
print(f"augmentations={trace}")
print(f"flows={tuple(sorted(flow.items()))}")
print(f"value={flow['sa'] + flow['sb']}")
print(f"valid={validate(flow)}")
print(f"residual_path={bfs_path(flow) is not None}")
```

Path lengths in the observed trace are $2,2,3$, consistent with nondecreasing sink distance. The final cut leaving $\{s,a,b\}$ has capacity $2+4=6$, equal to the returned value. The execution is one reproducible example, while the proofs establish the general structural claims under their assumptions.

### Audit the implementation against the proof

Test that BFS scans only strictly positive residuals, marks at enqueue time, and records level-increasing predecessor edges. For bounded small graphs, enumerate feasible integral flows or compare against a structurally different solver. Recompute final capacity, conservation, value, residual reachability, and cut equality without trusting the algorithm's mutable arrays.

For a diagnostic trace, record iteration, path residual IDs, pre-update levels, bottleneck, critical edge IDs, pre/post value, flow digest, and snapshot digest. A proof-aware audit can check shortest path length, nondecreasing distance labels, correct signed updates, and at least one newly saturated path direction. Do not require a particular tie-broken path unless determinism is part of the API.

Metamorphic tests include vertex renaming, edge insertion-order permutation under canonical ordering, adding disconnected or zero-capacity structure, and scaling all exact capacities by a positive integer. Scaling changes flow values and bottlenecks but should not change a deterministic policy's residual path identities when comparisons are only positivity and adjacency order.

### Engineer lifecycle and resource behavior

Bind graph, capacities, source/sink, current flow, residual state, BFS queue, distances, predecessors, and output to one revision. An augmentation is a transaction. A checkpoint should occur only at a validated committed flow or must encode enough transaction state for proved recovery.

Edmonds-Karp is polynomial, but $O(VE^2)$ can still be impractical. Dense graphs make $E=\Theta(V^2)$ and the bound becomes $O(V^5)$. Enforce vertex, edge, capacity representation, memory, work, trace, and wall-clock limits. Cancellation returns the last committed feasible flow as incomplete unless the final residual-exhaustion certificate was already validated.

Queue memory is $O(V)$; predecessor and distance maps are $O(V)$; explicit paired residual adjacency is $O(V+E)$. Avoid clearing huge maps with unsafe sentinels when generation counters or compact arrays are appropriate, but validate generation overflow and index domains.

### Relate current libraries without inheriting claims

Current Boost.Graph documentation exposes `edmonds_karp_max_flow`, with capacity, residual-capacity, reverse-edge, color, predecessor, and vertex-index maps; it documents the general $O(VE^2)$ bound and requires reverse edges. These interface requirements align with the chapter's state and identity invariants.

Current OR-Tools documentation exposes a `SimpleMaxFlow` API, solver status, optimal value, per-arc flows, and source/sink sides of a cut, but the public example does not make Edmonds-Karp path selection part of its contract. A library's maximum-flow result and certificate can be used for independent comparison without assuming the same algorithm or trace.

## Definitions and Notation

- $f,f'$: feasible flows immediately before and after one augmentation.
- $G_f$: residual graph containing positive residual directions.
- $d_f(v)$: shortest residual edge count from $s$ to $v$, or infinity.
- $P$: BFS-selected shortest residual $s$-$t$ path.
- $\Delta$: minimum residual capacity along $P$.
- **critical edge**: path residual direction saturated by the augmentation.
- $V=|V|$, $E=|E|$: vertex and original-edge counts; paired residual directions remain $O(E)$.
- **capacity-independent bound**: augmentation bound not expressed using capacity magnitudes.
- **graph-operation complexity**: analysis treating governed arithmetic operations as unit cost unless stated otherwise.

## Mechanisms, Invariants, or Proof Structure

BFS establishes shortest residual levels and an edge-identified predecessor path. Bottleneck augmentation preserves feasibility and raises value. Augmentation can remove residual directions and create only reverses of path directions. This structure prevents shortest residual distances from decreasing. A residual direction that becomes critical twice must disappear, reappear through its reverse, and have its tail level rise by at least two. Each direction is critical $O(V)$ times; some direction is critical on every augmentation; hence $O(VE)$ augmentations. Each BFS and update takes $O(E)$ conventional adjacency-list work, producing $O(VE^2)$. Residual exhaustion plus flow-cut equality certifies optimality.

## Alternatives and Trade-Offs

- **Arbitrary DFS Ford-Fulkerson:** smaller conceptual mechanism; lacks a capacity-independent iteration guarantee.
- **Edmonds-Karp:** deterministic with canonical adjacency and easy to verify; worst-case $O(VE^2)$ is expensive on large or dense graphs.
- **Dinic:** reuses one BFS level graph for many augmentations; stronger general bound with more internal state.
- **Capacity scaling:** organizes work by residual magnitude; suited to governed integer capacities but depends on numeric scales.
- **Push-relabel:** local operations and different performance profile; more complex invariants and certificates during execution.
- **Explicit residual arrays:** fast scans and updates; require exact reverse pairing and lifecycle control.
- **Derived residual adjacency:** clear original flow source of truth; repeated construction costs allocation and time.
- **Canonical tie-breaking:** reproducible trace; may add sorting/preprocessing cost and does not improve the asymptotic bound.
- **Final certificate only:** compact evidence; full traces aid diagnosis but invite storage and privacy risks.

## Failure Modes and Misconceptions

- BFS minimizes number of residual edges, not bottleneck, capacity sum, or domain latency.
- Marking only on dequeue can enqueue a vertex repeatedly and destabilize predecessor semantics.
- A predecessor vertex without residual edge identity cannot update parallel edges safely.
- Distances must be recomputed after each augmentation; the residual graph changed.
- Distance monotonicity applies across committed augmentations, not during partial mutation.
- Every augmentation has a critical edge, but it need not be unique.
- The number of augmentations is $O(VE)$, not merely $O(E)$.
- $O(VE^2)$ graph operations do not make arbitrary-precision arithmetic free.
- Polynomial worst-case time does not mean acceptable production latency.
- Resource-limited feasibility is not optimality.
- A library result does not validate input units, freshness, or domain modeling.

## Worked Examples

### Example 1

**Situation.** Residual paths have edge counts two and three. Their bottlenecks are one and ten respectively. BFS selects the two-edge path and augments one. **Conclusion.** Edmonds-Karp optimizes residual hop count, not immediate flow gain.

### Example 2

**Situation.** BFS discovers $a$ at level one and $t$ from $a$ at level two. A later scan finds a three-edge route to $t$. Because $t$ was marked on first discovery, its predecessor stays on the shortest path. **Conclusion.** Enqueue-time discovery preserves BFS distance semantics.

### Example 3

**Situation.** Path residuals are $(8,3,3,9)$. Bottleneck three makes two directions critical simultaneously. **Conclusion.** Every augmentation has at least one chargeable critical edge, and may have several.

### Example 4

**Situation.** Direction $(u,v)$ is critical when levels are 4 and 5. Before it can be critical again, reverse $(v,u)$ must lie on a shortest path, forcing the new level of $u$ to be at least 6. **Conclusion.** Repeated criticality consumes at least two tail levels.

### Example 5

**Situation.** A graph has 100 vertices and 500 original edges. The asymptotic charging bound permits on the order of $VE=50{,}000$ augmentations and $VE^2=25{,}000{,}000$ edge-scan units up to constants. **Conclusion.** Polynomial is a growth classification, not a latency promise.

### Example 6

**Situation.** Two parallel residual directions lead from $u$ to $v$; one has residual two, the other seven. A vertex-only predecessor is ambiguous. **Conclusion.** BFS discovery metadata must retain exact residual identity.

### Example 7

**Situation.** Scaling every integral capacity by 1,000 scales all bottlenecks and the final value. Positivity and canonical adjacency are unchanged, so the sample policy selects the same path identities. **Conclusion.** Edmonds-Karp's combinatorial trace need not depend on magnitude.

### Example 8

**Situation.** A 4,000-vertex dense graph can have about 16 million directed edges before residual pairing. Even one BFS is expensive and memory-heavy. **Conclusion.** A polynomial bound does not remove admission control and representation planning.

### Example 9

**Situation.** Cancellation occurs after a candidate path is updated but before validation. Transaction rollback restores the preceding feasible flow and digest. **Conclusion.** Only committed iteration boundaries are safe partial results and checkpoints.

### Example 10

**Situation.** Final flow value is 12, reached-set cut capacity is 12, all outward crossing edges are saturated, and all inward crossing flow is zero. **Conclusion.** The compact flow-cut certificate supports optimality independently of the BFS trace.

## Cross-Program Connections

- Data Structures Engineering owns queue representations, predecessor maps, adjacency scans, generation counters, and parallel-edge identity.
- Theory of Computation connects monotone measures, termination, partial correctness, and unit-cost versus bit-complexity models.
- Software Testing and Quality Engineering owns property, metamorphic, differential, adversarial, and certificate-validation strategies.
- Systems and Platform Engineering own memory/work admission control, cancellation, checkpointing, observability, and deterministic replay.
- Database Engineering owns immutable revisions, atomic augmentations, recovery, and provenance.
- Security Engineering reviews hostile graph sizes, capacity encodings, queue/trace exhaustion, overflow, and result-status confusion.

## References

1. Jack Edmonds and Richard M. Karp, “Theoretical Improvements in Algorithmic Efficiency for Network Flow Problems,” *Journal of the ACM* 19(2), 248–264, 1972, DOI [10.1145/321694.321699](https://doi.org/10.1145/321694.321699). Primary paper and bibliographic record checked 2026-09-05.
2. Lester R. Ford Jr. and Delbert R. Fulkerson, *Flows in Networks*, Princeton University Press, 1962; 2025 digital edition. [Official publisher record](https://doi.org/10.1515/9780691273457), checked 2026-09-05.
3. Ravindra K. Ahuja, Thomas L. Magnanti, and James B. Orlin, *Network Flows: Theory, Algorithms, and Applications*, Prentice Hall, 1993, shortest augmenting path analysis. [MIT-hosted record](https://dspace.mit.edu/handle/1721.1/49424), checked 2026-09-05.
4. Thomas H. Cormen et al., *Introduction to Algorithms*, 4th ed., MIT Press, 2022, Chapter 24. [Official publisher record](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/), checked 2026-09-05.
5. Jeff Erickson, *Algorithms*, 1st ed., 2019, maximum-flow chapter. [Author-hosted book](https://jeffe.cs.illinois.edu/teaching/algorithms/), checked 2026-09-05.
6. Boost C++ Libraries, “Edmonds-Karp Maximum Flow” and “Network Flow,” current Boost.Graph documentation. [Official documentation](https://www.boost.org/doc/libs/latest/libs/graph/doc/html/graph/algorithms/network_flow/network_flow_overview.html), checked 2026-09-05.
7. Google, “Maximum Flows,” OR-Tools documentation, updated 2026-03-18. [Official documentation](https://developers.google.com/optimization/flow/maxflow), checked 2026-09-05.

## Exercises

### Exercise 1

State the Edmonds-Karp loop and explain exactly what BFS minimizes. For one BFS run, state the queue, discovery, predecessor, path, and bottleneck invariants.

### Exercise 2

Prove that if a directed residual edge $(u,v)$ is critical, disappears, and later becomes critical again, then the shortest residual distance to $u$ has increased by at least two. Use this to derive the augmentation and running-time bounds.

### Exercise 3

Diagnose an implementation that traverses `residual >= 0`, marks on dequeue, stores only predecessor vertices, reuses levels after augmentation, mutates the live flow edge-by-edge, and uses unchecked arbitrary-size uploads.

### Exercise 4

Compare Edmonds-Karp, Dinic, push-relabel, and arbitrary DFS Ford-Fulkerson for explainability, worst-case guarantee, state complexity, deterministic replay, and suitability for an adversarial service.

### Exercise 5

Design evidence and lifecycle controls for a cancellable Edmonds-Karp service over exact integer capacities. Include snapshot identity, per-iteration checks, optional trace fields, resource limits, checkpoints, final certificate, and status semantics.

## Answers to the Exercises

### Answer 1

From a feasible flow, build positive residual adjacency, run unweighted BFS from $s$, recover the predecessor path to $t$, augment by its minimum residual, validate and commit, and repeat. Stop normally when $t$ is unreachable. BFS minimizes residual edge count only; it does not maximize bottleneck or minimize a capacity/cost sum.

The queue is processed in nondecreasing distance, and a vertex is marked and enqueued once at discovery. Each predecessor names a positive residual edge from level $i$ to level $i+1$. The recovered chain is connected, acyclic, and shortest. Its bottleneck is the positive minimum on that same snapshot. Signed updates preserve feasibility and raise value exactly by the bottleneck.

### Answer 2

When $(u,v)$ is first critical on a shortest path, $d(v)=d(u)+1$. Its saturation removes that direction. To become available again, some later augmentation must send flow through reverse direction $(v,u)$. When that reverse lies on a shortest augmenting path, its then-current labels satisfy $d'(u)=d'(v)+1$.

Distance monotonicity gives $d'(v)\ge d(v)$, so $d'(u)\ge d(v)+1=d(u)+2$. Finite tail levels are below $V$; therefore each directed residual edge can be critical only $O(V)$ times. With $O(E)$ directions and at least one critical direction per augmentation, there are $O(VE)$ augmentations. Each BFS, reconstruction, and update takes $O(E)$ conventional adjacency-list work, giving $O(VE^2)$ total.

### Answer 3

Residual traversal requires strict positivity; zero-capacity slots are not edges of $G_f$. Mark on enqueue so each vertex receives its shortest distance and one stable predecessor. Store the exact residual slot or original edge ID plus direction to disambiguate parallel and anti-parallel edges. Rebuild distances after every augmentation because residual edges may disappear or appear.

Apply the path to a candidate or rollback transaction, revalidate capacity, conservation, value increase, and snapshot, then commit atomically. Admission control must bound vertices, edges, capacity representation, memory, $VE^2$ work estimate, trace volume, and wall time. Checked arithmetic and explicit cancellation/resource statuses remain required.

### Answer 4

Edmonds-Karp has a transparent BFS trace and $O(VE^2)$ bound, making it strong for teaching, verification, and moderate graphs. Dinic retains BFS levels but computes blocking flows, improving general asymptotic performance while adding current-arc and level-graph state. Push-relabel uses local excess/height invariants and is often a stronger general-purpose implementation choice, but its execution is less path-explanatory. Arbitrary DFS Ford-Fulkerson is simplest mechanically but has a pseudo-polynomial integer bound and unsafe arbitrary-real termination behavior.

For an adversarial service, a maintained bounded algorithm, strict admission control, and independent certificate checks matter more than trace simplicity. Canonical ordering can make any deterministic implementation replayable, but does not itself improve the bound.

### Answer 5

Canonicalize and hash the immutable graph, terminals, units, edge IDs, capacities, and numeric policy. Each iteration records the snapshot digest, BFS level/predecessor state or its digest, exact residual path IDs, bottleneck, critical directions, pre/post value, and flow digest when a full audit trace is requested. Validate shortest-level predecessor relations, signed updates, feasibility, and exact value increase before atomic commit.

Bound graph size, paired residual memory, capacity bit width, predicted $VE^2$ work, wall time, checkpoint frequency, and trace retention. A checkpoint contains the last committed flow, graph and policy digests, iteration, validated value, and no ambiguous partial transaction. Cancellation or resource exhaustion returns `feasible_incomplete`; invalid input, arithmetic failure, and invariant failure remain separate.

On normal exhaustion, independently BFS again, compute the reached set and crossing originals, validate outward saturation, zero inward crossing flow, conservation, source/sink value, and flow-cut equality. Publish status, edge flows, value, cut certificate, input digest, algorithm/policy and toolchain versions, resource use, and limitations. The certificate supports optimality for that snapshot, not domain-model fitness or production throughput.
