---
module_id: ALGE-078
program: Algorithm Engineering
level: 2
module_number: 78
title: Dynamic Connectivity
status: complete
last_verified: 2026-09-05
---

# Dynamic Connectivity

## One-Page Review

### Governing question

How can an undirected graph answer connectivity queries while edges are inserted and deleted, and which incremental, offline, forest, replacement-edge, complexity, and consistency model makes each answer valid?

### Essential definitions

- At logical time $t$, an undirected graph is $G_t=(V,E_t)$; vertices $u,v$ are **connected** when an undirected path joins them.
- **Incremental connectivity** permits edge insertion only; **decremental connectivity** permits deletion only; **fully dynamic connectivity** permits both.
- An algorithm is **online** when it must answer before seeing future updates; an **offline** algorithm receives the complete operation trace.
- A **tree edge** belongs to a maintained spanning forest; a **non-tree edge** connects vertices already in one forest component.
- Deleting a tree edge creates a **cut**. Any active non-tree edge crossing that cut is a **replacement edge**.
- A **dynamic forest** supports operations such as `link`, `cut`, and component/root queries as its represented forest changes.
- A **rollback DSU** undoes unions to a saved history length; it normally avoids unlogged path compression.
- An edge's **active interval** $[a,b)$ means it is present at every operation index $t$ with $a\le t<b$.
- **Amortized update time** bounds the total cost over a sequence; it does not bound every individual deletion.
- A connectivity answer is snapshot-relative and does not itself provide a path witness.

### Central model, mechanism, or theorem

Insertion-only updates are monotone, so [disjoint-set union](./039-disjoint-sets-in-graph-algorithms.md) can merge components. Deletion is nonmonotone: removing a redundant edge changes nothing, while removing a bridge may split a component, an operation ordinary DSU cannot express.

For a known offline trace, map every edge instance to active intervals, place each interval into $O(\log T)$ canonical nodes of a segment tree over $T$ times, and depth-first traverse that tree with rollback DSU. On the root-to-leaf path for time $t$, exactly the edges active at $t$ have been unioned. Answer leaf queries, then roll back to the entry snapshot. Union by size without path compression gives $O(\log |V|)$ worst-case find; the construction costs

$$
O\bigl((I\log T+Q)\log |V|\bigr)
$$

for $I$ active intervals and $Q$ queries, plus interval construction and storage.

Online fully dynamic algorithms maintain a spanning forest and organize non-tree edges so a replacement can be found after a tree-edge deletion. Dynamic trees provide forest `link` and `cut` in logarithmic time [2]; decomposition, levels, randomization, or sparsification control replacement search [3–5].

### Critical invariants

- Vertex and edge-instance identities, parallel-edge policy, and operation ordering are unambiguous.
- At time $t$, $E_t$ contains exactly edge instances whose active intervals cover $t$.
- A maintained forest spans every current connected component and contains no cycle.
- Every active edge is classified exactly once as tree or non-tree under the algorithm's representation.
- When a tree edge is removed, components remain separate unless an active crossing replacement is installed.
- Rollback restores every parent, size, component-count, and auxiliary change made after its snapshot.
- Query results refer to a named version or linearization point, not an unspecified moving graph.

### Common failures

Using ordinary DSU after deletion; conflating an endpoint pair with an edge instance; removing all parallel edges accidentally; applying a removal at the wrong side of a time boundary; using path compression without logging rollback writes; forgetting redundant-union history; scanning only former tree edges for a replacement; claiming worst-case time from an amortized theorem; and returning a connectivity boolean when the caller requires a path or causal witness.

### Compact example

Edges `ab`, `bc`, and `ac` make a triangle. Deleting non-tree edge `ac` leaves `a` connected to `c` through `b`. If instead `ab` is a maintained tree edge, its deletion cuts the forest, but active `ac` crosses the cut and can replace it. The graph remained connected in both cases; the data-structure work differed because tree membership is representation, not graph semantics.

### Connections

[ALGE-039](./039-disjoint-sets-in-graph-algorithms.md) owns insertion-only DSU. [ALGE-072](./072-caching-and-paging-algorithms.md) provides amortized reasoning patterns. ALGE-079 next separates dynamic directed reachability and shortest-path maintenance from undirected connectivity.

## Governing Question

Given a stable vertex universe and a versioned sequence of undirected edge insertions, deletions, and queries, how should an algorithm preserve exactly the connected-component partition of each graph version while meeting an explicit online/offline and worst-case/amortized performance contract?

## Why This Matters

Networks, dependency graphs, access relationships, clusters, roads, circuits, social graphs, and infrastructure inventories change continuously. Re-running breadth-first search after every change is clear and often correct, but costs $O(|V|+|E|)$ per query. Incremental DSU is far faster when edges only arrive, yet its parent forest remembers merged equivalence classes and cannot split them when an edge disappears.

The deletion difficulty is informational. A removed edge may be redundant, may be the only bridge, or may be replaceable by a non-tree edge far from the maintained tree representation. Efficient algorithms must preserve enough organization to distinguish those cases without rescanning the entire graph each time.

Dynamic connectivity is also a semantics problem. Does `remove(u,v)` delete one edge or every parallel instance? Is a query ordered before or after a concurrent update? Does vertex deletion atomically remove incident edges? Are self-loops accepted? Is the output a boolean, component label, size, spanning forest, or actual path? A theorem for one abstract sequence does not settle these API choices.

## Prerequisites and Retrieval

Retrieve undirected paths and components from [ALGE-031](./031-breadth-first-search.md), spanning trees from [ALGE-035](./035-minimum-spanning-trees.md), DSU invariants and inverse-Ackermann amortization from [ALGE-039](./039-disjoint-sets-in-graph-algorithms.md), segment-tree interval decomposition from data structures, and amortized/randomized distinctions from ALGE-006, ALGE-068, and ALGE-071. You should be able to prove a forest invariant, represent half-open intervals, and distinguish graph state from data-structure representation.

## Learning Objectives

After this module, you should be able to:

1. specify incremental, decremental, fully dynamic, online, and offline connectivity models;
2. explain exactly why ordinary DSU cannot process arbitrary deletions;
3. derive and implement segment-tree-over-time connectivity with rollback DSU;
4. prove active-edge path coverage and rollback correctness;
5. explain spanning-forest maintenance and the replacement-edge problem;
6. interpret classic polylogarithmic upper and lower bounds under their actual models;
7. validate multigraph, time-boundary, concurrency, recovery, and adversarial cases; and
8. select a recomputation, batching, offline, or online design from workload evidence.

## Core Exposition

### Fix the dynamic graph model

Let $V$ be a finite vertex set and let operations be totally ordered at indices $0,\ldots,T-1$. This chapter treats undirected connectivity. An edge instance has a stable identity $e$ and unordered endpoints $\{u,v\}$. Stable identity matters in a multigraph: two edges with the same endpoints can have different lifetimes. A self-loop never changes connectivity but may still need accounting.

Use half-open lifetime semantics. An insertion of $e$ at index $a$ makes it available to later queries whose index is at least $a$; a removal at $b$ ends interval $[a,b)$, so a query at or after $b$ does not see it. If an API allows update and query in one transaction, define an internal order or one atomic post-update version. Reject insertion of an already active edge ID and removal of an inactive one unless reference-counted endpoint semantics are explicitly chosen.

For each query `connected(u,v)` at time $t$, the required answer is

$$
u\sim_t v
\quad\Longleftrightarrow\quad
\text{there exists an undirected path from $u$ to $v$ in }G_t.
$$

The relation $\sim_t$ is an equivalence relation for each fixed $t$, but its blocks can merge and split across time.

### Three update regimes

In the **incremental** regime, components only merge. DSU represents the partition and supports a sequence of unions and finds in near-linear total time under its standard model [1]. It does not need the graph's redundant edges to answer connectivity.

In the **decremental** regime, components only split. If the full deletion sequence is known, process time backward: the final graph is the starting state and every reversed deletion becomes an insertion. This simple reversal answers versioned connectivity offline. It does not apply directly when insertions and deletions interleave, when future operations are unknown, or when output must be emitted online.

In the **fully dynamic** regime, both changes occur. Online algorithms preserve enough forest and non-tree-edge structure to find replacements after deletion. Offline algorithms can instead exploit known lifetimes and time decomposition. These are different products: an offline batch that finishes in a minute cannot answer a request that needs a result before the next operation arrives.

### Why ordinary DSU cannot delete

Suppose DSU unions edges `ab` and `bc`. Its block is $\{a,b,c\}$. The arrays do not record whether `ac` also exists or whether `ab` was the only connection from `a` to the rest. Removing `ab` should split the block in the path graph but not in the triangle. Identical DSU partitions before removal correspond to both graphs, so no operation on the partition alone can always choose correctly.

Undoing the most recent union is narrower. A rollback DSU can restore a prior state when updates are traversed in a nested last-in-first-out schedule. Arbitrary online deletion is not generally the inverse of the last successful union: redundant edges, later unions, and crossing lifetimes break stack order. The offline segment tree creates a traversal in which rollback order is valid.

### Convert edge history to active intervals

Scan the operation trace. On `add(e,u,v)` store its start and endpoints. On `remove(e)`, emit $[a,b)$ and clear the active entry. At end time $T$, emit $[a,T)$ for every still-active edge. A query operation creates no interval.

Correct intervalization requires edge-instance IDs. With endpoint-only IDs, adding a second parallel `uv` either looks like an illegal duplicate or overwrites the first lifetime. Reference counting is possible, but then the counter and each transition between zero and positive multiplicity are part of the proof and recovery state.

### Segment tree over time

Build a segment tree whose leaves are operation indices. Decompose every interval $[a,b)$ into disjoint canonical nodes whose ranges union to exactly that interval. Any interval uses $O(\log T)$ nodes. For a leaf $t$, a stored edge appears on its root-to-leaf path exactly when its lifetime contains $t$.

Depth-first traversal maintains a rollback DSU:

1. save history length at node entry;
2. union every edge stored at that node;
3. recurse, or answer the leaf query;
4. restore the saved history length.

The traversal is an evaluation plan, not the graph's real-time order. Each branch receives the unions shared by its time range, and rollback prevents one branch's edges from leaking into its sibling.

### Rollback DSU mechanics

Use parent roots and union by size, but do not perform ordinary path compression. A successful union records the attached root, receiving root, old receiving size, and old component count or enough information to restore them. A redundant union must either record a no-op marker or leave history unchanged under a snapshot-length protocol used consistently. Rollback pops records and restores exact prior fields.

Union by size without compression gives height at most $\lfloor\log_2|V|\rfloor$: whenever a node's depth increases, its component size at least doubles. Thus `find` and `union` cost $O(\log|V|)$ worst case, and rollback is constant per successful union. Path compression can be made rollback-aware only by logging every parent rewrite and reanalyzing cost; silently enabling it corrupts snapshots.

<!-- bijux-verify: {"id":"offline-dynamic-connectivity","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"t=1 connected(a,b)=True\nt=3 connected(a,c)=True\nt=5 connected(a,c)=False\nt=7 connected(a,c)=True\nt=9 connected(b,c)=False\n","stderr":""}} -->
```python
class RollbackDSU:
    def __init__(self, vertices):
        self.parent = {v: v for v in vertices}
        self.size = {v: 1 for v in vertices}
        self.history = []

    def find(self, v):
        while self.parent[v] != v:  # deliberately no path compression
            v = self.parent[v]
        return v

    def snapshot(self):
        return len(self.history)

    def union(self, u, v):
        u, v = self.find(u), self.find(v)
        if u == v:
            return
        if self.size[u] < self.size[v]:
            u, v = v, u
        self.history.append((v, u, self.size[u]))
        self.parent[v] = u
        self.size[u] += self.size[v]

    def rollback(self, snapshot):
        while len(self.history) > snapshot:
            child, root, old_size = self.history.pop()
            self.parent[child] = child
            self.size[root] = old_size


def solve(vertices, events):
    total = len(events)
    tree = [[] for _ in range(max(1, 4 * total))]
    active = {}
    answers = []

    def cover(node, lo, hi, left, right, edge):
        if right <= lo or hi <= left:
            return
        if left <= lo and hi <= right:
            tree[node].append(edge)
            return
        mid = (lo + hi) // 2
        cover(2 * node, lo, mid, left, right, edge)
        cover(2 * node + 1, mid, hi, left, right, edge)

    for t, event in enumerate(events):
        if event[0] == "add":
            _, edge_id, u, v = event
            if edge_id in active:
                raise ValueError("edge already active")
            active[edge_id] = (t, u, v)
        elif event[0] == "remove":
            _, edge_id = event
            if edge_id not in active:
                raise ValueError("edge not active")
            start, u, v = active.pop(edge_id)
            cover(1, 0, total, start, t, (u, v))
    for start, u, v in active.values():
        cover(1, 0, total, start, total, (u, v))

    dsu = RollbackDSU(vertices)

    def visit(node, lo, hi):
        saved = dsu.snapshot()
        for u, v in tree[node]:
            dsu.union(u, v)
        if hi - lo == 1:
            event = events[lo]
            if event[0] == "query":
                _, u, v = event
                answers.append((lo, u, v, dsu.find(u) == dsu.find(v)))
        else:
            mid = (lo + hi) // 2
            visit(2 * node, lo, mid)
            visit(2 * node + 1, mid, hi)
        dsu.rollback(saved)

    if total:
        visit(1, 0, total)
    return answers


events = [
    ("add", "ab", "a", "b"),
    ("query", "a", "b"),
    ("add", "bc", "b", "c"),
    ("query", "a", "c"),
    ("remove", "ab"),
    ("query", "a", "c"),
    ("add", "ac", "a", "c"),
    ("query", "a", "c"),
    ("remove", "bc"),
    ("query", "b", "c"),
]
for t, u, v, answer in solve({"a", "b", "c"}, events):
    print(f"t={t} connected({u},{v})={answer}")
```

This implementation is a bounded offline reference, not a concurrent service or state-of-the-art online structure. It rejects malformed lifetimes, distinguishes edge IDs, and demonstrates the proof-critical no-compression rollback discipline.

### Correctness and complexity of the offline construction

Fix leaf $t$. Canonical interval decomposition places edge $e$ in exactly one node on the path to $t$ if $t$ lies in each covered piece, and in no path node otherwise. Therefore the unions active at leaf entry are exactly $E_t$. DSU connectivity equals undirected connectivity of those edges. After answering, rollback restores the parent's state, so induction on the traversal tree proves every leaf receives the correct graph.

An interval occupies $O(\log T)$ tree nodes. With $I$ intervals, there are $O(I\log T)$ union attempts. Union-by-size find costs $O(\log|V|)$; each query uses two finds. The stated time is therefore $O((I\log T+Q)\log|V|)$ for the simple implementation. Stored interval copies use $O(I\log T)$ space, the traversal stack $O(\log T)$, and DSU $O(|V|)$, apart from events and output.

### Online fully dynamic connectivity

Maintain a spanning forest $F$ of the active graph. An inserted edge whose endpoints lie in different forest trees becomes a tree edge and links them. Otherwise it becomes non-tree. Deleting a non-tree edge cannot disconnect the graph. Deleting a tree edge cuts one forest tree into two; connectivity is preserved exactly when an active non-tree edge crosses the new cut, in which case that edge becomes the replacement tree edge.

Dynamic-tree representations such as link-cut trees support link and cut on forests in $O(\log n)$ time under their model [2]. Euler-tour-tree representations offer another route for component aggregates and forest updates. Neither alone solves general graph connectivity: the hard part is organizing all non-tree edges so a crossing replacement can be found efficiently.

Henzinger and King gave randomized fully dynamic connectivity with polylogarithmic expected update cost over qualifying sequences [3]. Holm, de Lichtenberg, and Thorup gave a deterministic structure with $O(\log^2 n)$ amortized update cost for connectivity in the initially empty graph model [4]. Their level hierarchy limits how often edges are scanned or promoted. These are sophisticated complete algorithms, not permission to combine a dynamic tree with an unbounded adjacency scan and quote the same bound.

Sparsification replaces subgraphs by certificates preserving the property of interest and organizes them in a decomposition, allowing algorithms whose cost depends on sparse edge counts to extend to dense graphs [5]. It is a proof-governed reduction: a random edge sample or arbitrary spanning forest is not automatically a connectivity certificate for every required update context.

Cell-probe lower bounds show that dynamic connectivity retains logarithmic barriers under strong data-structure models and expose query/update trade-offs [6]. Such lower bounds do not predict wall-clock performance; they delimit asymptotic possibilities under word, space, randomization, amortization, and operation assumptions.

### Engineering and validation

Choose from workload evidence. Recompute with BFS when graphs or query rates are small, deletions are rare, or simplicity dominates. Use incremental DSU when deletion is prohibited by contract. Batch and solve offline when latency permits and lifetimes are known. Adopt a complete online dynamic algorithm only when its complexity and implementation risk beat measured rebuild or hybrid strategies.

Validate every result against an independent traversal oracle on bounded graphs. Exhaust all simple graphs for small $|V|$, then enumerate legal insert/remove/query traces; add multigraphs, self-loops, isolated vertices, bridges, cycles, dense cuts, repeated replacement churn, and adversarial orders. Compare every query, not just final components. For rollback, hash the complete parent/size state at every snapshot and after restoration. For online forests, independently check acyclicity, spanning, edge classification, and replacement crossing.

Production state records vertex and edge ID schemas, graph direction, multiplicity, self-loop policy, operation sequence/version, algorithm and implementation version, consistency model, persistence checkpoint, source offsets, and rebuild provenance. Metrics cover active vertices and edges, components, tree and non-tree edges, interval count, rollback depth, replacement scans/promotions, update and query latency distributions, rejected operations, lag, and oracle discrepancies.

Concurrency needs a linearization or snapshot contract. A query racing with deletion can correctly differ depending on order; returning an unversioned boolean makes the result unauditable. Persist graph updates and derived state atomically, or replay a durable log idempotently. On corruption, missing log ranges, unsupported upgrade, or invariant failure, stop serving authoritative answers and rebuild or fall back to a verified snapshot traversal.

## Definitions and Notation

- $G_t=(V,E_t)$: undirected graph at logical operation index or version $t$.
- $u\sim_t v$: $u$ and $v$ are connected in $G_t$.
- $T$: number of operations in an offline trace.
- $I$: number of maximal active edge-instance intervals.
- $Q$: number of connectivity queries.
- $[a,b)$: edge lifetime including $a$ and excluding $b$.
- $F_t$: maintained spanning forest of $G_t$.
- **Bridge:** active edge whose deletion increases the number of connected components.
- **Tree edge:** edge currently chosen in $F_t$; it need not be a bridge of $G_t$.
- **Non-tree edge:** active edge outside $F_t$.
- **Replacement edge:** non-tree edge crossing the cut created by deletion of a tree edge.
- **Rollback snapshot:** a history length identifying one exact reversible DSU state.
- **Canonical interval nodes:** disjoint segment-tree ranges whose union is one active interval.
- **Connectivity certificate:** a subgraph or structure that preserves the connectivity answers required by a stated reduction.
- **Linearization point:** one instant at which a concurrent operation is defined to take effect.

## Mechanisms, Invariants, or Proof Structure

### Offline proof layers

First prove intervalization: each edge instance is active exactly on its emitted half-open intervals. Next prove segment coverage: a leaf path contains exactly canonical nodes covering that time. Then prove rollback evaluation: node-entry state equals ancestor edges, node unions add precisely its range edges, and restoration removes precisely branch-local changes. Finally apply the DSU theorem that equal roots match connected components of unioned undirected edges. Each layer has separate boundary tests.

### Rollback representation proof

Parent pointers remain a forest because union links only distinct roots. Union by size preserves root sizes and logarithmic height. Every successful union logs the child root and receiver's old size before mutation. Reversing records in last-in-first-out order restores both roots and sizes; operations after a snapshot form a suffix of history. Omitting path compression ensures `find` creates no hidden writes outside that log.

### Online forest proof obligations

Insertion either links two forest components or adds redundancy inside one. Non-tree deletion preserves the forest. Tree deletion produces two trees; installing an active crossing edge reconnects them without forming a cycle. If no active crossing edge exists, no graph path crosses the cut, so the graph genuinely split. The difficult algorithmic obligation is finding or certifying absence of a replacement within the claimed bound.

### Complexity audit

For every bound, record preprocessing, update, query, space, initialization, and output costs; worst-case versus amortized; deterministic versus expected or high-probability; online versus offline; graph and word model; initial-state restrictions; and supported output. HLT's amortized polylogarithmic connectivity bound and Pătraşcu--Demaine's cell-probe lower bound occupy different claim types and cannot be compared as raw constants.

## Alternatives and Trade-Offs

- **Recompute by BFS/DFS:** $O(|V|+|E|)$ per relevant snapshot; simple, witness-friendly, and often the best oracle or low-rate production choice.
- **Incremental DSU:** nearly linear aggregate insertion/query cost [1]; cannot split and may discard redundant-edge evidence needed later.
- **Reverse-time decremental processing:** simple offline reduction to insertions; requires the complete deletion-only history and versioned answers.
- **Segment tree plus rollback DSU:** deterministic, auditable, fully dynamic offline processing; $O(I\log T)$ stored unions and no online answers.
- **Block or square-root decomposition:** batch updates, rebuild periodically, and answer from base plus delta; easier than polylog structures and often competitive, with tunable latency spikes.
- **Online dynamic forest plus replacement hierarchy:** supports immediate answers with polylogarithmic theoretical bounds [3,4]; substantial invariant, memory, and implementation complexity.
- **Sparsification:** reduces dense graphs to property-preserving certificates [5]; certificate construction and update integration are proof-critical.
- **Approximate or sampled connectivity:** may reduce costs for some relaxed questions, but a false connected/disconnected answer is a different contract and can be unacceptable.

The decision should use measured $|V|$, active-edge density, update/query mix, deletion fraction, burstiness, batch horizon, witness needs, consistency, memory, and recovery objectives. Asymptotic superiority may begin beyond the actual workload or lose to rebuild simplicity and cache locality.

## Failure Modes and Misconceptions

1. **“DSU supports deletion by resetting a parent.”** Parent links encode union history, not individual graph edges.
2. **“Every tree edge is a bridge.”** It is a representation edge; a non-tree replacement may exist.
3. **“Endpoint pairs identify edges.”** Parallel instances require identity or a proved multiplicity policy.
4. **“Removal at $b$ is active through $b$.”** This chapter's half-open convention excludes it; other conventions must be explicit.
5. **“Rollback DSU can compress paths normally.”** Unlogged writes survive restoration and corrupt sibling states.
6. **“Offline means slow.”** It means future operations are known; it can be efficient but cannot meet online latency semantics.
7. **“A dynamic tree solves dynamic connectivity.”** It maintains a forest; replacement search handles general non-tree edges.
8. **“Amortized $O(\log^2n)$ bounds every update.”** One update may be costlier while sequence total remains bounded.
9. **“Randomized expected time means Monte Carlo answers.”** Las Vegas algorithms can keep answers correct while runtime is random; inspect the exact theorem.
10. **“Connectivity supplies a route.”** A boolean or component label need not retain a path witness.
11. **“Concurrent answers need no version.”** Racing operations require a linearization or snapshot identifier.
12. **“Passing final-state tests is enough.”** Transient queries and rollback leaks can be wrong while final components match.

## Worked Examples

### Example 1

**Situation.** Active edges are `ab`, `bc`, and `ac`; the maintained forest uses `ab` and `bc`.

**Reasoning.** Deleting non-tree `ac` leaves the forest and connectivity unchanged. Deleting tree edge `ab` splits the forest into `{a}` and `{b,c}`, but active `ac` crosses the cut and becomes a replacement.

**Conclusion.** Graph connectivity and tree-edge classification are distinct.

### Example 2

**Situation.** DSU's only block is `{a,b,c}` after processing a path in one execution and a triangle in another.

**Reasoning.** Deleting `ab` disconnects `a` in the path but not the triangle. The DSU states can be identical because redundant `ac` never changed the partition.

**Conclusion.** The component partition lacks enough information for arbitrary deletion.

### Example 3

**Situation.** Edge `e` is added at index 2 and removed at index 6 under $[a,b)$ semantics.

**Reasoning.** It is active for leaves 2, 3, 4, and 5, but not 1 or 6. Canonical segment nodes must union exactly the range `[2,6)`; including leaf 6 makes post-removal queries stale.

**Conclusion.** One endpoint convention controls every offline answer.

### Example 4

**Situation.** Two parallel edges `e1=(u,v)` and `e2=(u,v)` are active, and `e1` is removed.

**Reasoning.** `e2` still connects the endpoints. Endpoint-only deletion that erases `(u,v)` disconnects them incorrectly; edge-ID deletion leaves one interval active.

**Conclusion.** Multigraph correctness requires edge-instance identity or explicit counts.

### Example 5

**Situation.** A rollback DSU snapshot precedes unions `ab`, redundant `ac` after `ab,bc`, and `de`.

**Reasoning.** Successful unions mutate parent and size; the redundant union mutates nothing. Rolling history back to the saved length must restore exactly the earlier roots and sizes regardless of the no-op. A protocol that pushes markers must pop them; a snapshot-length protocol may omit them consistently.

**Conclusion.** Rollback correctness is about exact mutation history, not the number of calls.

### Example 6

**Situation.** $I=10^6$ edge intervals, $T=10^6$ operations, and $|V|=2^{20}$.

**Reasoning.** The simple offline design stores on the order of $I\log_2T\approx20$ million interval-node placements in the worst decomposition scale, and each DSU find has height at most 20. Constants and memory can dominate even though both factors are logarithmic.

**Conclusion.** Complexity formulas must be translated into resource estimates before adoption.

### Example 7

**Situation.** A deletion-only trace and all future queries are available in a file.

**Reasoning.** Construct the final graph after all deletions, then traverse operations backward. Each reversed deletion inserts its edge; DSU answers the correspondingly reversed version queries. No rollback segment tree is needed.

**Conclusion.** A narrower offline regime admits a simpler reduction.

### Example 8

**Situation.** An online implementation deletes a tree edge and scans every active non-tree edge until it finds a replacement.

**Reasoning.** The forest invariant can be correct, but one deletion may scan $\Theta(|E|)$ edges and repeated adversarial deletions can repeat the cost. Quoting HLT's $O(\log^2n)$ amortized update bound is invalid without its level hierarchy and promotion analysis.

**Conclusion.** A correct mechanism does not inherit another algorithm's complexity theorem.

### Example 9

**Situation.** Query `connected(a,c)` races with removal of bridge `bc` from path `a-b-c`.

**Reasoning.** Linearizing the query before removal yields true; after removal yields false. Both are consistent outcomes under different orders. Without a returned graph version or documented consistency, neither can be audited.

**Conclusion.** Dynamic correctness includes temporal semantics.

### Example 10

**Situation.** A service detects that its durable update log skips versions 50,001 through 50,020 after recovery.

**Reasoning.** Continuing from derived forest state may omit insertions or retain deletions, so all later connectivity answers are suspect. Stop authoritative serving, rebuild from a complete snapshot plus contiguous log, validate against traversal samples, and publish the recovered version.

**Conclusion.** Recovery provenance is part of the connectivity evidence chain.

## Cross-Program Connections

- **Data Structures Engineering:** rollback DSU, segment trees, link-cut trees, Euler-tour trees, heaps, and level-indexed adjacency own the representation mechanics.
- **Distributed Systems Engineering:** version order, linearizability, snapshots, logs, replay, partition gaps, and recovery define which graph exists.
- **Database Engineering:** temporal tables and interval joins can construct active edge lifetimes for offline queries.
- **Data Engineering:** event identity, deduplication, late data, watermarks, compaction, and lineage determine update completeness.
- **Platform Engineering:** dynamic graph services need resource budgets, rebuild modes, compatibility envelopes, metrics, and degraded-state policy.
- **Security Engineering:** adversarial churn, identity spoofing, authorization changes, denial of service, and stale access edges shape threat models.
- **Operating Systems:** dynamic dependency and wait-for graphs connect to resource and deadlock monitoring, though directed cycles require other algorithms.
- **Algorithm Engineering:** [ALGE-039](./039-disjoint-sets-in-graph-algorithms.md) supplies monotone connectivity; ALGE-079 next treats reachability and shortest-path concepts under updates.

## References

1. Robert Endre Tarjan, “Efficiency of a Good But Not Linear Set Union Algorithm,” *Journal of the ACM* 22(2), 1975, 215–225. DOI: [10.1145/321879.321884](https://doi.org/10.1145/321879.321884). Primary source for amortized disjoint-set analysis; ACM-linked and Berkeley records checked 2026-09-05.
2. Daniel D. Sleator and Robert Endre Tarjan, “A Data Structure for Dynamic Trees,” *Journal of Computer and System Sciences* 26(3), 1983, 362–391. DOI: [10.1016/0022-0000(83)90006-5](https://doi.org/10.1016/0022-0000(83)90006-5). Primary source for logarithmic link and cut on dynamic forests; publisher and author records checked 2026-09-05.
3. Monika R. Henzinger and Valerie King, “Randomized Fully Dynamic Graph Algorithms with Polylogarithmic Time per Operation,” *Journal of the ACM* 46(4), 1999, 502–516. DOI: [10.1145/320211.320215](https://doi.org/10.1145/320211.320215). Primary source for randomized polylogarithmic fully dynamic connectivity; institutional and manuscript records checked 2026-09-05.
4. Jacob Holm, Kristian de Lichtenberg, and Mikkel Thorup, “Poly-Logarithmic Deterministic Fully-Dynamic Algorithms for Connectivity, Minimum Spanning Tree, 2-Edge, and Biconnectivity,” *Journal of the ACM* 48(4), 2001, 723–760. DOI: [10.1145/502090.502095](https://doi.org/10.1145/502090.502095). Primary source for deterministic level-based fully dynamic connectivity; ACM, institutional, and author records checked 2026-09-05.
5. David Eppstein, Zvi Galil, Giuseppe F. Italiano, and Amnon Nissenzweig, “Sparsification—A Technique for Speeding Up Dynamic Graph Algorithms,” *Journal of the ACM* 44(5), 1997, 669–696. DOI: [10.1145/265910.265914](https://doi.org/10.1145/265910.265914). Primary source for sparsification and dynamic connectivity certificates; author and institutional records checked 2026-09-05.
6. Mihai Pătraşcu and Erik D. Demaine, “Logarithmic Lower Bounds in the Cell-Probe Model,” *SIAM Journal on Computing* 35(4), 2006, 932–963. DOI: [10.1137/S0097539705447256](https://doi.org/10.1137/S0097539705447256). Primary source for dynamic-connectivity lower bounds and query/update trade-offs; SIAM and author records checked 2026-09-05.
7. David Eppstein, “Offline Algorithms for Dynamic Minimum Spanning Tree Problems,” *Journal of Algorithms* 17(2), 1994, 237–250. DOI: [10.1006/jagm.1994.1033](https://doi.org/10.1006/jagm.1994.1033). Primary source for exploiting known update sequences in offline dynamic graph algorithms; publisher and author records checked 2026-09-05.
8. Kathrin Hanauer, Monika Henzinger, and Christian Schulz, “Recent Advances in Fully Dynamic Graph Algorithms: A Quick Reference Guide,” *ACM Journal of Experimental Algorithmics* 27, 2022, Article 1.11, 1–45. DOI: [10.1145/3555806](https://doi.org/10.1145/3555806). Current research survey used to calibrate model, theory, and engineering distinctions; ACM-linked institutional and author records checked 2026-09-05.

## Exercises

### Exercise 1

Define incremental, decremental, fully dynamic, online, and offline connectivity. Give one workload for which each of incremental DSU, reverse-time DSU, and segment-tree rollback is the narrowest sufficient design.

### Exercise 2

Prove that root-to-leaf unions in the segment-tree-over-time algorithm equal exactly $E_t$, then derive its time and space costs with union-by-size rollback DSU.

### Exercise 3

An implementation identifies edges only by endpoints, uses path compression without logging, treats removal intervals as closed, omits history for receiving-root sizes, and tests only final components. Diagnose each defect and design focused counterexamples.

### Exercise 4

Design an online connectivity service for a graph with 50 million vertices, mostly insertions, rare deletion bursts, strict versioned queries, and a four-hour rebuild objective. Compare rebuild, batching, hybrid, and complete fully dynamic designs; specify invariants, persistence, validation, observability, and fallback.

### Exercise 5

An authorization system models active grants as undirected edges and wants connectivity to imply access. Transfer the chapter's reasoning to assess graph semantics, direction, revocation, consistency, witnesses, adversaries, fail-safe behavior, audit, and whether dynamic connectivity is even the correct primitive.

## Answers to the Exercises

### Answer 1

Incremental permits only insertion; decremental only deletion; fully dynamic permits both. Online answers before future operations are known; offline receives the whole trace. A build-time component index over an append-only edge file needs incremental DSU. A known sequence that only removes failed links can start from the final graph and process deletions backward with DSU. A historical trace with arbitrarily interleaved adds, removes, and versioned queries fits active intervals plus segment-tree rollback. If immediate answers are needed, none of the offline reductions meets the latency contract; use recomputation, batching with declared staleness, or an online structure.

### Answer 2

Intervalization emits $e$ on exactly $[a_e,b_e)$. Canonical nodes partition that interval. A leaf $t$ descends through one node containing $t$ at each depth, so it encounters one stored copy from the interval decomposition exactly when $a_e\le t<b_e$ and none otherwise. Inductively, rollback makes node-entry state contain only ancestor copies and node exit restores that state; thus leaf unions are exactly $E_t$. Each of $I$ intervals occupies $O(\log T)$ nodes, creating $O(I\log T)$ union attempts. Union by size without compression makes each find $O(\log|V|)$; $Q$ queries use two finds. Time is $O((I\log T+Q)\log|V|)$ plus interval parsing, and space is $O(|V|+I\log T+T)$ for DSU, stored copies, and the explicit tree/events, with $O(\log T)$ traversal stack.

### Answer 3

Endpoint identity cannot distinguish two parallel `uv` edges; remove one and verify the other still connects. Unlogged compression changes parents after a snapshot; traverse one branch that compresses a long path, roll back, and compare every parent/size with a deep copy. Closed removal intervals retain an edge at its removal leaf; query a sole bridge immediately after removal. Failing to restore receiver size breaks future union-by-size choices and size invariants; union unequal components, roll back, then assert every root size. Final-only testing misses all of these when later updates reconnect the graph. Enumerate and compare every intermediate query with BFS, validate complete rollback state, and include malformed add/remove traces.

### Answer 4

Measure active edges, query/update rates, deletion-burst size, acceptable staleness, and component/witness demand. Incremental DSU between deletion bursts plus a verified rebuild may win if queries can pause or use a named pre-burst snapshot; a base graph with buffered deltas can bound staleness but needs correct handling of deletions crossing the base. Offline rollback is suitable for historical and delayed batches, not strict immediate queries. A complete online fully dynamic structure is justified only if measured burst latency and four-hour rebuild risk exceed its implementation and memory cost. Define stable edge IDs, half-open version order, multigraph policy, forest and edge-class invariants, linearized queries, and no unproved bound borrowing. Durably log updates; checkpoint state at a graph version and replay contiguously. Validate continuously against BFS on sampled bounded components and shadow rebuilds, plus adversarial bridge/replacement churn. Observe log lag, active/tree/non-tree counts, component count, replacement work, latency tails, memory, rejected operations, and discrepancies. On log gaps or invariant failure, serve a labeled older snapshot if authorized or fail unavailable while rebuilding; never return unversioned guesses.

### Answer 5

Access propagation is usually directed and policy-qualified, so undirected connectivity may grant access along paths that have no legal direction or composition. Define principals, resources, grant types, direction, constraints, tenant boundaries, and whether path composition is permitted before choosing an algorithm. Revocation is a deletion requiring linearizable or otherwise explicit consistency; stale true answers should fail closed for sensitive actions. A boolean is insufficient when an authorization decision needs an explainable valid grant path, policy evaluation, and revocation version. Attackers can create churn, parallel or spoofed identities, cross-tenant edges, and race revocation. Authenticate and authorize updates, rate-limit, preserve an append-only audit log, return graph/policy version and witness, and independently recompute high-risk decisions. Missing logs, stale replicas, ambiguous identity, unsupported policy edges, invariant failure, or unavailable revocation evidence must deny or escalate. In most systems the correct primitive is versioned directed reachability plus policy evaluation, not undirected dynamic connectivity; this module supplies deletion and evidence lessons but not the authorization semantics.
