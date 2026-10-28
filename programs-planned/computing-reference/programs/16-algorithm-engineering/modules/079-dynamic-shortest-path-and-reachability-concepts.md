---
module_id: ALGE-079
program: Algorithm Engineering
level: 2
module_number: 79
title: Dynamic Shortest-Path and Reachability Concepts
status: complete
last_verified: 2026-09-05
---

# Dynamic Shortest-Path and Reachability Concepts

## One-Page Review

### Governing question

When a directed or weighted graph changes, what may be safely reused from an old reachability or shortest-path solution, what must be repaired, and which update, query, accuracy, and consistency contract makes the result meaningful?

### Essential definitions

- At version $t$, **reachability** asks whether a directed path $u\leadsto v$ exists in $G_t$; **distance** $d_t(u,v)$ is the minimum path weight, or $+\infty$ when no path exists.
- **Incremental**, **decremental**, and **fully dynamic** algorithms allow insertions, deletions, or both; a weight decrease resembles insertion of a better edge, while a weight increase resembles deletion of its former value.
- **Single-source**, **single-pair**, and **all-pairs** name the maintained query scope. **Transitive closure** represents every reachable ordered pair.
- An **exact** answer equals the static definition. An **approximate** distance must name whether its error is multiplicative, additive, one-sided, randomized, or probabilistic.
- A **witness** is a path realizing a reachability or distance answer. A scalar distance does not by itself supply one.
- **Affected vertices** are those whose correct labels or witnesses may change after an update; discovering this set is central to repair.
- A query result is meaningful only relative to a graph version or linearization point.

### Central model, mechanism, or theorem

For insertion-only, unweighted, directed single-source shortest paths, an inserted edge $(u,v)$ can improve a label only if $d(u)+1<d(v)$. Seed that improvement and propagate ordinary breadth-first relaxations from $v$. Any newly shorter path must contain the new edge; its suffix consists of old edges, so relaxation closure finds every improvement. Labels only decrease, and the algorithm remains exact.

Deletions are different. Removing one predecessor may leave an equal alternative, raise many distances, or make a region unreachable. A decremental shortest-path tree therefore needs dependency information and a repair mechanism such as the classic Even–Shiloach level structure [2]. Fully dynamic reachability and shortest paths require more elaborate combinatorial or algebraic structures [4–7], and their bounds depend sharply on directedness, weights, approximation, randomness, preprocessing, and adversary model.

### Critical invariants

- Every answer refers to one immutable version $G_t$.
- A finite label is backed by a present path; no label is smaller than the true distance.
- After repair reaches closure, every admissible edge satisfies the relevant relaxation inequality.
- Predecessor and witness data never refer to deleted edges or mixed versions.
- Unreachable means proved absence under the maintained model, not merely missing cache state.
- Complexity claims retain the theorem's exact graph, update, query, accuracy, and probability assumptions.

### Common failures

Treating directed reachability as undirected connectivity; using DSU; repairing only an edge endpoint; retaining a deleted predecessor; running Dijkstra with negative weights; confusing distance with a route; materializing an all-pairs closure without a memory budget; serving a path assembled across versions; hiding stale answers; and quoting an amortized or conditional result as a per-operation universal guarantee.

### Compact example

Suppose `s→a→b→d` gives labels $0,1,2,3$. Insert `s→b`. The new edge lowers $d(b)$ from $2$ to $1$, then relaxation lowers $d(d)$ from $3$ to $2$. Vertex `a` does not change. The affected region is discovered by propagation rather than by recomputing all labels.

### Connections

[ALGE-031](./031-breadth-first-search.md) and [ALGE-036](./036-dijkstra-s-shortest-paths.md) supply the static baselines. [ALGE-078](./078-dynamic-connectivity.md) explains update regimes and version semantics but owns only undirected connectivity. ALGE-080 next studies engineering patterns for dynamic-graph workloads.

## Governing Question

Given a stable vertex universe and a versioned stream of directed edge or weight updates, how should an algorithm maintain reachability, shortest distances, and optional path witnesses with an honest contract for scope, accuracy, latency, consistency, and failure?

## Why This Matters

Road networks, routing tables, dependency graphs, build systems, knowledge graphs, authorization relations, workflow engines, and program-analysis graphs all change. A static breadth-first search or Dijkstra run remains the clearest correctness oracle, but recomputing it after every update can waste work when a small update affects only a small region. Dynamic algorithms try to reuse unaffected state while repairing exactly what changed.

The hard part is not merely speed. Graph direction, weight domain, negative cycles, parallel edges, update ordering, and requested witnesses determine what the query even means. A service returning `reachable=true` from version 41 and a path whose final edge appeared in version 42 has returned no valid answer at all. Likewise, an approximation factor without a direction of error cannot tell a caller whether a reported route is feasible or only numerically close.

There is no single “dynamic shortest-path algorithm.” An insertion-only single-source problem with nonnegative integral weights, a fully dynamic all-pairs problem with real weights, and decremental reachability in a directed acyclic graph have different structures and theorems. Good engineering starts with that model matrix, then measures whether specialized maintenance actually beats a simple recomputation baseline.

## Prerequisites and Retrieval

Retrieve directed paths and BFS from [ALGE-031](./031-breadth-first-search.md), nonnegative weighted shortest paths from [ALGE-036](./036-dijkstra-s-shortest-paths.md), negative-edge and cycle reasoning from [ALGE-037](./037-bellman-ford-and-negative-weights.md), all-pairs scope from [ALGE-038](./038-all-pairs-shortest-paths.md), and update/version distinctions from [ALGE-078](./078-dynamic-connectivity.md). You should be able to prove a relaxation invariant, trace a queue, distinguish a path from a walk, and state whether a complexity bound is worst-case, amortized, expected, or total.

## Learning Objectives

After this module, you should be able to:

1. specify dynamic reachability and shortest-path problems along every material model dimension;
2. derive an exact insertion-only BFS repair algorithm and prove its closure property;
3. explain why deletions, weight increases, witnesses, and negative cycles require different evidence;
4. distinguish single-source, single-pair, all-pairs, and transitive-closure costs;
5. interpret classic decremental, fully dynamic, algebraic, and conditional-lower-bound results narrowly;
6. design version, edge-identity, consistency, recovery, and observability contracts;
7. test repair algorithms against static oracles on exhaustive small graphs and adversarial traces; and
8. decide when recomputation, batching, caching, or specialized dynamic maintenance is justified.

## Core Exposition

### Specify the graph and the answer

Let $G_t=(V,E_t,w_t)$ be a directed graph at committed version $t$. An edge instance $e$ has stable identity, ordered endpoints $(u_e,v_e)$, and weight $w_t(e)$ while active. Stable identity distinguishes parallel edges. A self-loop of nonnegative weight does not improve a shortest distance but can matter to reachability, negative-cycle detection, update accounting, and audit.

A directed path from $x$ to $y$ follows edge orientation. Reachability is

$$
R_t(x,y)\iff \text{a directed path }x\leadsto y\text{ exists in }G_t.
$$

For path weights defined by addition,

$$
d_t(x,y)=\min_{P:x\leadsto y}\sum_{e\in P}w_t(e),
$$

with $d_t(x,y)=+\infty$ when no path exists. If a reachable negative cycle can lie on a walk from $x$ to $y$, the minimum walk cost is unbounded below rather than a finite shortest-path value. An API must represent that state separately from unreachable.

The maintained scope matters. Single-source shortest paths store $d_t(s,v)$ for a fixed source. Single-pair maintenance focuses on one $(s,z)$. All-pairs shortest paths conceptually exposes $n^2$ distances. Transitive closure exposes $R_t(x,y)$ for every ordered pair. Output size alone can dominate: a dense Boolean closure needs $n^2$ bits even before indexes, versions, and witnesses.

### Classify every update

Incremental algorithms accept edge insertions; decremental algorithms accept deletions; fully dynamic algorithms accept both. Weight updates have analogous polarity. Decreasing an edge weight can create better paths and behaves like inserting a better alternative. Increasing it can invalidate paths that used the former value and behaves like deleting that alternative. Replacing a weight is safest to model as removal of one versioned edge value followed by insertion of another.

Monotonicity gives useful checks. Under edge insertion alone with unchanged weights, reachability can only change from false to true. With nonnegative fixed weights, distances can only stay equal or decrease. Under deletion alone, reachability can only change from true to false and distances can only stay equal or increase. A result violating the appropriate direction proves a bug or a mismatched version.

These checks do not solve the problem. An insertion can improve the entire downstream region. A deletion can break a high-level dominator or shortest-path-tree edge and affect many vertices. “One edge changed” does not imply “constant repair.”

### Keep static recomputation as an oracle

For unweighted single-source queries, recompute BFS in $O(n+m)$. For nonnegative weights, recompute Dijkstra using a suitable priority queue. For negative edges without a relevant negative cycle, use a compatible static algorithm. These baselines are valuable even when asymptotically slower:

- they are compact enough to review;
- they define expected results for differential tests;
- their latency may be acceptable when updates are rare;
- they recover from a suspect incremental state; and
- they reveal whether a specialized structure pays for its complexity.

A dynamic design should therefore be evaluated against measured recomputation, not against an imagined full scan. Sparse bounded components, batching, hardware locality, and low query rate often change the practical choice.

### Exact incremental BFS repair

Consider a fixed source $s$, unit-weight directed edges, insertion-only updates, and exact distance queries. Store adjacency lists and labels $d[v]$, initially $0$ for $s$ and $+\infty$ otherwise. Insert $(u,v)$ into adjacency. If $d[u]+1<d[v]$, set $d[v]=d[u]+1$ and enqueue $v$. While the queue is nonempty, relax every outgoing old edge from its vertex; enqueue a neighbor whenever its label strictly decreases.

<!-- bijux-verify: {"id":"incremental-directed-bfs","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"add s->a: [('a', 1)]\nadd a->b: [('b', 2)]\nadd b->d: [('d', 3)]\nadd s->c: [('c', 1)]\nadd c->b: []\nadd s->b: [('b', 1), ('d', 2)]\nfinal: [('a', 1), ('b', 1), ('c', 1), ('d', 2), ('s', 0)]\n","stderr":""}} -->
```python
from collections import deque
from math import inf


class IncrementalBFS:
    def __init__(self, vertices, source):
        self.adj = {v: [] for v in vertices}
        self.distance = {v: inf for v in vertices}
        self.distance[source] = 0

    def add_edge(self, u, v):
        self.adj[u].append(v)
        changed = []
        queue = deque()
        if self.distance[u] + 1 < self.distance[v]:
            self.distance[v] = self.distance[u] + 1
            queue.append(v)
        while queue:
            x = queue.popleft()
            changed.append((x, self.distance[x]))
            for y in self.adj[x]:
                candidate = self.distance[x] + 1
                if candidate < self.distance[y]:
                    self.distance[y] = candidate
                    queue.append(y)
        return changed


graph = IncrementalBFS(["s", "a", "b", "c", "d"], "s")
for u, v in [("s", "a"), ("a", "b"), ("b", "d"),
             ("s", "c"), ("c", "b"), ("s", "b")]:
    print(f"add {u}->{v}: {graph.add_edge(u, v)}")
print("final:", sorted(graph.distance.items()))
```

Why is this exact? Before insertion, all labels equal old distances. Any newly shorter path must use the new edge; otherwise it already existed. Choose such a path with prefix $s\leadsto u$, new edge $(u,v)$, and an old-edge suffix. Its prefix to $u$ cannot become shorter because the new edge is directed out of $u$ on this chosen first use; removing cycles yields a path whose improvement is seeded at $v$. Successive relaxations follow the suffix. Conversely, every assigned value is the length of a present path: the seed appends $(u,v)$ to a witnessed path to $u$, and propagation appends one present edge. At closure every edge satisfies $d[y]\le d[x]+1$, so no present path can be shorter than its endpoint label. Sound upper bounds and relaxation closure establish equality.

The algorithm demonstrates a mechanism, not a universal performance theorem. One insertion may lower $\Theta(n)$ labels, and repeated insertions may cause many repairs. Deduplicate or define parallel-edge policy, and maintain predecessor evidence separately if paths are requested.

### Deletions expose dependency

Suppose a shortest-path tree uses $(p,v)$. Deleting it does not immediately prove that $v$ is farther: another predecessor $q$ may satisfy $d[q]+w(q,v)=d[v]$. If no equal predecessor exists, $v$ rises; then descendants whose only shortest predecessors depend on $v$ may rise too. Repair must distinguish witness invalidation from value invalidation and must find alternative incoming support.

For decremental unweighted graphs, the Even–Shiloach approach maintains distance levels and scans incident edges as vertices lose valid parents. Its classic total update bound is $O(mn)$ for the stated decremental setting, with constant-time queries in the original connectivity formulation [2]. The result is historically foundational, but its exact direction, weight, query, and total-time assumptions must be checked before reuse. Modern results refine many regimes; the conceptual lesson remains that monotone level increases can charge repeated scans to bounded label changes.

A deleted edge outside the maintained witness can still matter later, so retaining only one tree is insufficient for arbitrary repair. Conversely, storing every shortest path can be enormous. Dynamic structures trade time, space, preprocessing, randomization, and approximation to preserve enough alternative support.

### Reachability is not connectivity

In an undirected graph, connectedness is an equivalence relation. Directed reachability is reflexive and transitive but not symmetric: $u\leadsto v$ does not imply $v\leadsto u$. DSU therefore cannot represent it. Strongly connected components compress mutual reachability at one static version, but an update may split or merge components and alter the condensation DAG.

Transitive closure materializes or implicitly supports all ordered reachability pairs. Combinatorial algorithms organize witnesses, paths, or graph decompositions; algebraic algorithms reduce reachability-related maintenance to dynamic matrix operations. Sankowski's dynamic-matrix-inverse method is an important example [6]. Algebraic bounds may count field operations, use randomization, or assume a computational model unlike production integer arithmetic. They establish possibilities under those assumptions, not a drop-in service design.

### Fully dynamic shortest paths

Fully dynamic all-pairs shortest paths must process both improvements and invalidations. Classic work includes deterministic and randomized structures with carefully bounded weight domains, update forms, and query guarantees [4,5]. Later work handles real weights under explicit restrictions [7]. These results show that reuse can beat naive recomputation in important models, but comparing bounds requires normalizing:

- directed versus undirected graphs;
- positive integers, nonnegative reals, or arbitrary real weights;
- exact versus $(1+\varepsilon)$ or additive approximation;
- distance-only versus path-reporting queries;
- single-edge versus batched incident-edge updates;
- worst-case, amortized, expected, or high-probability time;
- preprocessing and space; and
- adaptive versus oblivious adversaries.

Omitting any one of these can turn a true theorem into a false product promise.

### Conditional lower bounds guide expectations

Some dynamic-problem lower bounds are conditional: a hypothetical combination of preprocessing, update time, and query time would imply a faster algorithm for a conjecturally hard problem. The Online Matrix–Vector multiplication conjecture provides a framework unifying such hardness results [8]. A conditional lower bound is an implication under a named conjecture and parameter regime. It is not an unconditional proof that every instance is slow, nor a reason to avoid workload-specific engineering.

Use lower bounds to reject impossible-looking universal targets and to identify which concession may help: restrict graph classes, accept approximation, batch updates, answer fewer pairs, tolerate staleness, or exploit offline knowledge. Then measure the chosen workload.

### Witnesses, versions, and concurrency

A reachability Boolean, scalar distance, and actual path are different outputs. If a service promises a path, every consecutive edge must be active in the same version and the sum must equal the reported distance under that version's weights. Predecessor chains need cycle guards and version binding. When an update invalidates a witness but not the scalar answer, the service must repair the witness or explicitly return distance-only.

Concurrent updates require a linearization contract. One safe design commits an immutable edge-set version, runs or publishes repair for that version, and labels every query result with the version it read. Another serves an older complete snapshot while a new one builds, but then staleness is explicit. Mutating adjacency, distance, and predecessor arrays independently while queries read them can create an answer that belongs to no graph.

Durability also matters. Log edge identity, endpoints, old and new weight, operation kind, sequence number, and commit checksum. A checkpoint names the last included operation. Recovery loads the checkpoint and replays a contiguous suffix; gaps, duplicates, and out-of-order operations fail closed. Recompute or shadow validation can certify selected versions against a static oracle.

### Engineering decision procedure

Start with workload evidence: $n$, active $m$, component sizes, directionality, weight distribution, update mix, source/pair popularity, burstiness, path-output rate, latency percentiles, memory, and staleness tolerance. Implement the static oracle and time it. Then consider progressively more state:

1. cache results by immutable graph version;
2. batch updates and recompute named snapshots;
3. repair only hot sources while cold sources recompute;
4. specialize for insertion-only or deletion-only epochs;
5. use a fully dynamic structure only when its measured benefit covers implementation and audit cost.

Observe updates accepted/rejected, versions committed/published, repair queue size, affected labels, scanned edges, recomputation time, query latency, stale-version age, witness failures, oracle discrepancies, memory, and recovery lag. A fallback should return a named older version or unavailable status, never an unversioned guess.

## Definitions and Notation

Let $n=|V|$ and $m_t=|E_t|$. Write $x\leadsto_t y$ for a directed path in version $t$, $R_t(x,y)$ for its existence, and $d_t(x,y)$ for shortest distance. Infinity denotes unreachable, while negative infinity denotes an unbounded-below walk cost when a relevant negative cycle exists. For a fixed source $s$, abbreviate $d_t(v)=d_t(s,v)$.

An edge relaxation tests $d(v)>d(u)+w(u,v)$ and, if true, lowers $d(v)$. A feasible potential or distance labeling satisfies $d(v)\le d(u)+w(u,v)$ on every applicable edge. An affected set contains vertices whose correct distance, reachability, or requested witness changes. A predecessor relation records support for a path label; it is representation, not graph truth.

An approximation statement must specify its inequality. For nonnegative true distance $d$, a one-sided multiplicative estimate might promise

$$
d\le \widehat d\le (1+\varepsilon)d.
$$

This differs from two-sided error and becomes delicate when $d=0$, $d=+\infty$, or negative weights are allowed. Define these cases rather than importing notation silently.

## Mechanisms, Invariants, or Proof Structure

### Static and dynamic correctness obligations

For exact finite distances, maintain two complementary obligations. **Witness soundness** gives a present source-to-vertex path of weight $d(v)$, proving true distance is at most the label. **Lower-bound closure** ensures no path is cheaper, usually through relaxation inequalities and source initialization. Reachability uses the analogous present-witness and no-missed-path obligations.

Incremental BFS preserves witness soundness on every assignment and restores closure by queue propagation. Its termination follows because integral labels strictly decrease and are bounded below by zero. The proof is version-local: adjacency and labels must not change concurrently outside the update transaction.

Deletion repair must prove that every retained label still has present support, that every raised or unreachable label lacks a cheaper present alternative, and that dependency propagation reaches closure. Checking only the deleted endpoint is insufficient because a shortest-path DAG can fan out arbitrarily.

### Validation strategy

Use differential testing against static BFS, Dijkstra, Bellman–Ford, or closure computation at every committed prefix. Exhaust all small graphs where feasible, not merely random large graphs. Include every insertion ordering on very small universes, ties, parallel edges, self-loops, unreachable sources, deletion of used and unused edges, repeated weight changes, zero weights, and negative-cycle transitions under models that allow them.

For witnesses, independently verify edge presence, orientation, version, endpoint sequence, total weight, and absence of illegal predecessor cycles. For approximate answers, test the declared inequality, including $0$ and infinity. For persistence, restore checkpoints at many prefixes and compare replayed state with a fresh build.

Performance validation needs adversarial traces: insert a shortcut near the source that improves a long chain; delete the only incoming support of a large downstream region; alternate two weights; churn a central edge; and issue queries during publication. Report latency distributions and affected work, not only average throughput.

### Complexity discipline

Separate preprocessing $P(n,m)$, update $U$, query $Q$, path-reporting cost, and space $S$. State whether $U$ is per update, amortized over a legal sequence, expected, high probability, or total over a decremental lifetime. Include output cost: reporting a path of $k$ edges needs $\Omega(k)$ time. A constant-time distance query does not imply constant-time path recovery.

## Alternatives and Trade-Offs

**Recompute per query** minimizes mutable state and is easy to certify, but repeats work for hot sources. **Recompute per update** makes subsequent queries cheap but wastes effort when queries are rare. **Version cache** reuses immutable answers safely but consumes memory and does not repair a new version.

**Incremental or decremental specialization** exploits monotonicity and is often simpler than full dynamism, but only if forbidden operations are rejected or force a rebuild. Epoch designs can rebuild between monotone windows. **Affected-region repair** performs well on local changes but can degrade to whole-graph work and needs complete dependency discovery.

**All-pairs materialization** gives fast distance or reachability lookups at quadratic space. **Hot-source maintenance** scales state with actual query demand but gives heterogeneous latency. **Approximation** may reduce update cost, yet path feasibility, infinity, zero distance, and business tolerance must be explicit.

**Combinatorial structures** often map more directly to discrete witnesses and integer implementations. **Algebraic structures** can yield strong asymptotic bounds but may involve field arithmetic, randomized correctness, dense state, or large constants. **Offline batching** may reorder or preprocess a known trace, but cannot satisfy an online answer-before-future-input requirement.

## Failure Modes and Misconceptions

- **“Connectivity answers reachability.”** Direction destroys symmetry; DSU is the wrong abstraction.
- **“Only the changed endpoints are affected.”** Improvements and invalidations can propagate through an entire downstream region.
- **“Deleting the chosen parent raises the distance.”** An equal alternative predecessor may preserve the value while only the witness changes.
- **“A stored distance proves a path.”** It may be stale, corrupted, or unsupported; retain or reconstruct version-valid evidence.
- **“Dijkstra handles dynamic weights.”** Dijkstra is a static method requiring nonnegative weights; rerunning it after each update is a baseline, not a dynamic repair proof.
- **“An all-pairs Boolean table is small.”** It is quadratic before metadata, versioning, and indexes.
- **“Approximate means close.”** The inequality, direction, probability, and exceptional values are part of correctness.
- **“Amortized means every update is fast.”** One operation may be expensive even when sequence-average cost is bounded.
- **“A conditional lower bound forbids optimization.”** It constrains a named combination under a conjecture; restrictions and workload structure still matter.
- **“Eventually consistent is self-explanatory.”** State maximum staleness, version exposure, monotonic-read behavior, and fail-safe policy.
- **“Replay restores the graph.”** It restores only if identity, order, weight transitions, checkpoint boundary, and integrity are correct.
- **“Passing random tests proves the repair.”** Exhaustive small-state comparison and adversarial traces find different defect classes.

## Worked Examples

### Example 1

**Situation.** Edges are $a\to b$ and $b\to c$. Is `a` connected to `c`, and can DSU answer whether `c` reaches `a`?

**Reasoning.** Ignoring direction, all three vertices are in one weakly connected component. Directed reachability gives $a\leadsto c$, but neither $c\leadsto b$ nor $c\leadsto a$. A DSU block is symmetric and cannot encode those two different ordered answers.

**Conclusion.** Weak connectivity and directed reachability are different predicates; use a directed reachability mechanism.

### Example 2

**Situation.** The path `s→a→b→d` has distances $0,1,2,3$. Insert `s→b`.

**Reasoning.** The seed test finds $d(s)+1=1<2=d(b)$, so $b$ becomes $1$. Its outgoing edge then gives $d(d)\le2<3$, so $d$ becomes $2$. No outgoing relaxation from those vertices improves $a$.

**Conclusion.** One insertion affects a downstream closure, not just endpoint `b`; queue propagation obtains exact labels $d(b)=1,d(d)=2$.

### Example 3

**Situation.** With `s→c`, `c→b`, and $d(b)=2$ already established through `s→a→b`, insert `c→b` or another equal-length route.

**Reasoning.** The candidate $d(c)+1=2$ equals $d(b)$. A strict-distance repair enqueues nothing because no scalar improves. If the product counts witnesses or needs redundancy for future deletion, it may still need to record the alternative predecessor.

**Conclusion.** A no-op for distance can be a meaningful update for witness and resilience state.

### Example 4

**Situation.** Paths `s→a→v` and `s→b→v` both have length two. The chosen predecessor of `v` is edge `a→v`, which is deleted.

**Reasoning.** The stored witness is invalid immediately, but incoming edge `b→v` still supports distance two. Raising $d(v)$ would be incorrect. Repair must remove the dead predecessor, discover the equal alternative, and either publish a repaired path or declare that only the distance is currently available.

**Conclusion.** Witness invalidation does not necessarily imply value invalidation.

### Example 5

**Situation.** Edges `s→a` of weight 4, `s→b` of weight 1, and `b→a` of weight 5 give $d(a)=4$. Change `b→a` from 5 to 2, then change `s→b` from 1 to 10.

**Reasoning.** The decrease creates path cost $1+2=3$, lowering $a$. The later increase invalidates that support: the route through `b` costs $12$, while direct `s→a` costs $4$, so $a$ rises to $4$. Treating both changes as decrease-style relaxations would leave stale value $3$.

**Conclusion.** Weight decreases and increases have opposite repair polarity.

### Example 6

**Situation.** Estimate the bare memory for a bit-packed transitive closure of $n=100{,}000$ vertices.

**Reasoning.** There are $n^2=10^{10}$ ordered pairs. At one bit per pair, storage is $10^{10}/8=1.25\times10^9$ bytes, or $1.25$ GB in decimal units, before row alignment, indexes, versions, allocator overhead, witnesses, or concurrency copies. A byte per pair would be 10 GB.

**Conclusion.** “Constant-time all-pairs lookup” carries a material quadratic-space contract.

### Example 7

**Situation.** A graph has 2 million active edges. Static recomputation takes 180 ms. Updates arrive twice per minute, queries 5,000 times per second, and a named snapshot may lag by one second.

**Reasoning.** Recomputing per query is impossible at the offered rate. Recomputing once after each update costs about 360 ms of compute per minute and can publish a new immutable snapshot well within the one-second budget. A sophisticated fully dynamic structure would need to beat this simple design after including validation and recovery cost.

**Conclusion.** High query rate alone does not imply dynamic repair; update frequency and staleness tolerance can make snapshot recomputation superior.

### Example 8

**Situation.** A query reads distance 7 from version 20, then follows a predecessor pointer installed for version 21 after a concurrent edge insertion.

**Reasoning.** The scalar and path belong to different snapshots. The new predecessor chain may have weight below 7, may contain an edge absent from version 20, or may loop while fields are being updated. Even if each field was valid when written, their composition is not a valid answer.

**Conclusion.** Publish graph, labels, and witnesses atomically by version or guard them with a proven concurrency protocol.

### Example 9

**Situation.** Edges are `s→a` weight 2, `s→b` weight 5, and `b→a` weight -10. Can Dijkstra settle `a` at 2?

**Reasoning.** Settling `a` before `b` assumes no later path can lower it. Yet `s→b→a` costs $5-10=-5$. The negative edge violates the theorem's nonnegative-weight premise; dynamic maintenance derived from Dijkstra relaxations inherits the same problem unless its own theorem explicitly handles negative weights.

**Conclusion.** A locally executable algorithm is not evidence outside its weight model.

### Example 10

**Situation.** A paper shows that update time $n^{0.4}$ and query time $n^{0.4}$ together would refute a named conjecture for a particular dynamic reachability model. A team concludes that no production optimization is worthwhile.

**Reasoning.** The result is conditional and constrains a joint asymptotic target under specified preprocessing, error, adversary, and graph assumptions. The service may query one source, use a DAG, accept batching, exploit small affected components, or tolerate approximation. Even within the hard model, constants and actual $n$ remain empirical questions.

**Conclusion.** Conditional hardness calibrates universal promises; it does not replace workload-specific design and measurement.

## Cross-Program Connections

- **Data Structures Engineering:** queues, heaps, dependency indexes, persistent versions, and compact bit matrices determine whether repair is practical.
- **Operating Systems:** snapshot publication, readers concurrent with repair, crash recovery, and memory reclamation are systems correctness obligations.
- **Database Engineering:** graph versions resemble transaction snapshots; log sequence, atomic commit, and replay boundaries prevent mixed-version answers.
- **Systems Engineering:** service-level objectives must cover update lag, query tails, recovery point, recovery time, and degraded-mode behavior.
- **Security Engineering:** authorization reachability needs direction, policy semantics, revocation consistency, witnesses, and fail-closed behavior beyond graph mechanics.
- **Platform Engineering:** shared dynamic-graph services need quotas, tenant isolation, observability, and explicit model/accuracy contracts.

## References

1. Edsger W. Dijkstra, “A Note on Two Problems in Connexion with Graphs,” *Numerische Mathematik* 1, 1959, 269–271. DOI: [10.1007/BF01386390](https://doi.org/10.1007/BF01386390). Primary source for the nonnegative shortest-path baseline; publisher record checked 2026-09-05.
2. Shimon Even and Yossi Shiloach, “An On-Line Edge-Deletion Problem,” *Journal of the ACM* 28(1), 1981, 1–4. DOI: [10.1145/322234.322235](https://doi.org/10.1145/322234.322235). Primary source for classic decremental level maintenance and total-time analysis; ACM-linked and IBM records checked 2026-09-05.
3. G. Ramalingam and Thomas W. Reps, “An Incremental Algorithm for a Generalization of the Shortest-Path Problem,” *Journal of Algorithms* 21(2), 1996, 267–305. DOI: [10.1006/jagm.1996.0046](https://doi.org/10.1006/jagm.1996.0046). Primary source for incremental shortest-path repair beyond the unit-weight mechanism developed here; publisher, author, and DBLP records checked 2026-09-05.
4. Valerie King, “Fully Dynamic Algorithms for Maintaining All-Pairs Shortest Paths and Transitive Closure in Digraphs,” *40th Annual Symposium on Foundations of Computer Science*, 1999, 81–89. DOI: [10.1109/SFFCS.1999.814580](https://doi.org/10.1109/SFFCS.1999.814580). Primary source for exact and approximate fully dynamic directed results under bounded positive integer weights; proceedings and author manuscript records checked 2026-09-05.
5. Camil Demetrescu and Giuseppe F. Italiano, “A New Approach to Dynamic All Pairs Shortest Paths,” *Journal of the ACM* 51(6), 2004, 968–992. DOI: [10.1145/1039488.1039492](https://doi.org/10.1145/1039488.1039492). Primary source for fully dynamic all-pairs shortest paths with nonnegative real weights; ACM-linked bibliographic records checked 2026-09-05.
6. Piotr Sankowski, “Dynamic Transitive Closure via Dynamic Matrix Inverse,” *45th Annual IEEE Symposium on Foundations of Computer Science*, 2004, 509–517. DOI: [10.1109/FOCS.2004.25](https://doi.org/10.1109/FOCS.2004.25). Primary source for the algebraic dynamic-reachability approach; IEEE-linked publication records checked 2026-09-05.
7. Camil Demetrescu and Giuseppe F. Italiano, “Fully Dynamic All Pairs Shortest Paths with Real Edge Weights,” *Journal of Computer and System Sciences* 72(5), 2006, 813–837. DOI: [10.1016/j.jcss.2005.05.005](https://doi.org/10.1016/j.jcss.2005.05.005). Primary source illustrating explicit weight and update assumptions in fully dynamic APSP; publisher record checked 2026-09-05.
8. Monika Henzinger, Sebastian Krinninger, Danupon Nanongkai, and Thatchaphol Saranurak, “Unifying and Strengthening Hardness for Dynamic Problems via the Online Matrix-Vector Multiplication Conjecture,” *47th Annual ACM Symposium on Theory of Computing*, 2015, 21–30. DOI: [10.1145/2746539.2746609](https://doi.org/10.1145/2746539.2746609). Primary source for conditional dynamic-problem lower-bound methodology; ACM-linked and author records checked 2026-09-05.
9. Kathrin Hanauer, Monika Henzinger, and Christian Schulz, “Recent Advances in Fully Dynamic Graph Algorithms: A Quick Reference Guide,” *ACM Journal of Experimental Algorithmics* 27, 2022, Article 1.11, 1–45. DOI: [10.1145/3555806](https://doi.org/10.1145/3555806). Current survey used to calibrate modern model and engineering distinctions; ACM-linked institutional records checked 2026-09-05.

## Exercises

### Exercise 1

Define incremental, decremental, and fully dynamic graph algorithms; directed reachability; exact distance; transitive closure; and a path witness. Explain why edge insertion is monotone for reachability but not for a stored predecessor.

### Exercise 2

Prove the insertion-only directed BFS repair algorithm correct. State the model precisely, establish witness soundness and relaxation closure, prove termination, and construct one insertion that changes $\Theta(n)$ labels.

### Exercise 3

A service uses endpoint pairs as edge identity, runs Dijkstra despite negative weights, repairs only the changed endpoint, publishes distance before predecessor state, and tests only final answers. Diagnose every defect and design a focused counterexample or check for each.

### Exercise 4

Design a versioned shortest-path service for a directed graph with 30 million edges, 20 hot sources, rare update bursts, a two-second staleness allowance, occasional path requests, and a 15-minute recovery objective. Compare per-query recomputation, snapshot recomputation, hot-source repair, and fully dynamic all-pairs maintenance. Specify evidence, observability, and fallback.

### Exercise 5

An authorization platform wants to maintain whether a principal can reach a resource through delegated grants. Transfer this chapter's concepts to define the graph semantics, revocation behavior, consistency, witnesses, adversarial cases, and algorithm choice. Explain why ordinary dynamic connectivity is insufficient.

## Answers to the Exercises

### Answer 1

Incremental permits insertion only, decremental deletion only, and fully dynamic both. Directed reachability $R_t(u,v)$ means a direction-respecting path exists in version $t$. Exact distance is the minimum valid path weight, infinity if unreachable, with a separate unbounded-below state when relevant negative cycles are admitted. Transitive closure represents all reachable ordered pairs. A witness is a concrete version-valid path supporting an answer. Insertion cannot destroy a present path, so true reachability only grows. It can, however, make a different path shorter or preferred under tie-breaking, so a stored predecessor may change even though reachability was already true. If resilience metadata records alternative predecessors, even a scalar no-op may change representation state.

### Answer 2

Assume a fixed source, stable vertices, directed unit-weight edges, insertion only, and a committed serial update order. Before an insertion labels equal BFS distances. Any newly shorter path must contain the new edge; otherwise the old graph already contained it. Choosing its first useful occurrence gives an old reachable prefix to the tail, the new edge, and an old-edge suffix. The seed assigns the path length to the head when it improves, and queue relaxation follows every suffix edge. Every assignment appends a present edge to a witnessed path, so labels never understate true distance. At termination every present edge satisfies $d(v)\le d(u)+1$; induction along any source path shows its length is at least the endpoint label. Thus labels equal true distances. Labels are nonnegative integers and strictly decrease on enqueue, so a finite graph admits only finitely many changes. For a worst affected set, begin with chain $s\to v_1\to\cdots\to v_{n-1}$ and then insert $s\to v_1$ only after arranging a much longer reachable route to $v_1$, or more simply use a long chain from $v_1$ downstream and insert the first source edge: every downstream label changes from infinity to finite, totaling $\Theta(n)$.

### Answer 3

Endpoint identity conflates parallel edge instances; add two `u→v` edges with different weights, delete one ID, and verify the other remains. Negative weights violate Dijkstra's settling proof; use `s→a=2`, `s→b=5`, `b→a=-10` and require $d(a)=-5$. Endpoint-only repair misses propagation; insert a shortcut to the first vertex of a long chain and compare every label with BFS. Publishing scalar and predecessor separately allows a mixed snapshot; pause a reader between writes and verify that every returned path uses one named version and sums to its scalar. Final-only tests miss transient faults that later updates mask; compare with a fresh static oracle after every prefix, validate witnesses, and enumerate small insertion orders. The service must also reject a model it cannot support rather than silently returning plausible values.

### Answer 4

Measure update frequency and burst size, graph locality, path lengths, source popularity, and static runtime first. Per-query recomputation is simple but repeats work at hot-source volume. Recomputing one immutable snapshot after a burst is attractive if it completes within two seconds; it gives homogeneous, auditable versions. Maintaining only 20 hot sources bounds mutable state and lets cold sources recompute on demand, but repair may still touch large regions. Fully dynamic all-pairs state is likely unjustified without a very high all-pairs query rate and a proven memory/update advantage. A sound design logs stable edge IDs and weight transitions, commits graph version $t$, builds or repairs source states bound to $t$, validates sampled sources against static algorithms, and atomically publishes a complete snapshot. Path requests validate orientation, edge presence, sum, and version. Observe accepted sequence, lag, affected labels, scanned edges, build/repair latency, query tails, witness failures, oracle discrepancies, memory, checkpoint age, and replay time. Checkpoint often enough to meet 15 minutes and test restores. On invariant failure or excessive lag, serve the last complete version with explicit age if policy permits; otherwise fail unavailable and rebuild.

### Answer 5

Model principals and resources as distinct typed vertices and grants as authenticated, directed, stable-ID edges. Define which grant types compose, maximum delegation depth, tenant and policy boundaries, expiration, deny precedence, and whether cycles are legal. Revocation is a deletion and must have a named visibility point; sensitive decisions should not accept an unlabeled stale true result. A Boolean needs a version-valid grant path and policy evaluation for explanation and audit. Test parallel grants, expired edges, cross-tenant attempts, cycles, rapid grant/revoke churn, concurrent reads, compromised writers, replay gaps, and deletion of one among several supporting paths. Ordinary dynamic connectivity is undirected and would authorize against edge direction, so it cannot represent the predicate. A versioned directed-reachability service with fail-closed recovery may fit; if the graph is small or updates rare, snapshot closure or per-request search may be safer than complex fully dynamic maintenance. Evaluate algorithms only after semantics and revocation SLOs are fixed.
