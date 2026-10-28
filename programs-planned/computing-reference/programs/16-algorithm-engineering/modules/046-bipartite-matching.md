---
module_id: ALGE-046
program: Algorithm Engineering
level: 1
module_number: 46
title: Bipartite Matching
status: complete
last_verified: 2026-09-05
---

# Bipartite Matching

## One-Page Review

### Governing question

How can we pair vertices from two disjoint groups without conflicts, recognize when no larger pairing exists, and publish a compact certificate that an independent checker can trust?

### Essential definitions

- A **bipartite graph** is a graph $G=(L\mathbin{\dot\cup}R,E)$ whose edges have one endpoint in $L$ and one in $R$.
- A **matching** $M\subseteq E$ contains no two edges sharing an endpoint.
- A vertex is **matched** if it is incident to an edge in $M$ and **free** otherwise.
- A matching is **maximal** if no edge can be added; it is **maximum** if its cardinality is greatest possible.
- A **perfect matching** covers every vertex. An **$L$-perfect matching** covers every vertex in $L$.
- An **alternating path** alternates between edges outside and inside $M$.
- An **augmenting path** is an alternating path whose two endpoints are free.
- For $X\subseteq L$, its neighborhood is $N(X)=\{r\in R:\{\ell,r\}\in E\text{ for some }\ell\in X\}$.
- A **vertex cover** is a vertex set incident to every edge.

### Central model, mechanism, or theorem

Toggling membership along an augmenting path produces another matching with one more edge. Berge's lemma gives the converse: $M$ is maximum exactly when no $M$-augmenting path exists. Three equivalent views then support construction and certification:

1. unit-capacity max flow constructs a maximum bipartite matching;
2. Hall's theorem characterizes an $L$-perfect matching by $|N(X)|\ge |X|$ for every $X\subseteq L$;
3. Kőnig's theorem says maximum-matching size equals minimum-vertex-cover size in bipartite graphs.

A valid matching and valid vertex cover of equal cardinality are a lower/upper-bound certificate of optimality.

### Critical invariants

- $L$ and $R$ are disjoint, and every declared edge crosses the partition.
- Every vertex is incident to at most one matched edge.
- Alternation is relative to the current matching.
- Symmetric difference on an augmenting path preserves matching feasibility and raises cardinality by exactly one.
- A matching is a lower bound; a vertex cover is an upper bound because every matched edge needs a distinct cover endpoint.
- Cardinality matching does not encode costs, preferences, fairness, capacities greater than one, or temporal availability.
- Certificates, partitions, and edges must describe one immutable graph snapshot.

### Common failures

Common failures are confusing maximal with maximum; omitting isolated vertices from a partition; trusting endpoint labels instead of validating bipartiteness; running an augmenting search with stale visited state; traversing matched edges in the wrong direction; treating a nonunique optimum as unstable; claiming Hall's condition after checking only individual vertices; using a general-graph greedy algorithm as an exact solver; interpreting duplicate records as parallel opportunities; and claiming operational fairness from maximum cardinality alone.

### Compact example

Let $L=\{a,b,c\}$, $R=\{1,2\}$, and edges $a1,a2,b1,c2$. The matching $\{a1,c2\}$ has size two. Since $R$ itself is a vertex cover of size two, every matching has size at most two. The matching and cover therefore certify each other as optimal, even though $b$ remains free.

### Connections

[ALGE-045](./045-max-flow-min-cut-theorem.md) supplies flow-cut equality and integrality. [ALGE-047](../ROADMAP.md#block-05--flows-matching-and-combinatorial-optimization) adds assignment costs rather than mere cardinality. [DSE-041](../../17-data-structures-engineering/ROADMAP.md) studies graph representations, while systems scheduling and resource allocation supply applications but must state constraints beyond the matching model.

## Governing Question

Given two declared vertex classes and admissible cross-class pairs, how do we construct a conflict-free pairing, prove that it is as large as possible, diagnose why a left-perfect pairing may not exist, and separate that mathematical result from production policy?

The answer is not simply “run a library function.” It requires a model boundary, a local improvement operation, an optimality characterization, and checkable evidence. These layers let a reviewer distinguish a malformed graph, a feasible but suboptimal matching, an optimal mathematical result, and an unsuitable real-world policy.

## Why This Matters

Bipartite matching models one-to-one compatibility: applicants to positions, jobs to machines, requests to interchangeable slots, records across two data sources, and tests to execution agents. The same structure also exposes a fundamental algorithmic pattern: turn a local alternating search into a global optimality theorem.

The abstraction is deliberately narrow. A plain matching says only whether a pair is admissible and whether endpoints may be reused. It does not rank outcomes, balance groups, respect multi-unit capacities, reserve contingency capacity, or schedule across time. Those additions lead to weighted assignment, $b$-matching, flow, scheduling, or constrained optimization. Reliable engineering begins by stating which model is actually being solved.

## Prerequisites and Retrieval

Retrieve undirected graphs, paths, connected components, set cardinality, symmetric difference, induction, contradiction, breadth-first and depth-first search, asymptotic analysis, and flow networks. Review [ALGE-041](./041-flow-networks-and-residual-graphs.md) for residual directions and [ALGE-045](./045-max-flow-min-cut-theorem.md) for equal lower/upper-bound certificates.

## Learning Objectives

After completing this module, you should be able to:

1. validate a graph and its explicit bipartition;
2. distinguish feasible, maximal, maximum, perfect, and one-side-perfect matchings;
3. trace alternating and augmenting paths relative to a matching;
4. prove that augmenting-path toggling preserves feasibility and increases size;
5. prove Berge's no-augmenting-path characterization;
6. reduce bipartite matching to integral unit-capacity maximum flow;
7. apply Hall's condition and produce a deficient-set obstruction;
8. derive a minimum vertex cover from alternating reachability;
9. verify an optimality certificate independently of the solver; and
10. identify representation, lifecycle, and policy failures outside the pure model.

## Core Exposition

### Declare and validate the model

Let $G=(V,E)$ be a finite undirected graph. A bipartition is an ordered pair of disjoint sets $(L,R)$ such that $V=L\mathbin{\dot\cup}R$ and every edge has one endpoint in each set. The graph may be disconnected and may contain isolated vertices. A two-coloring can discover a bipartition when one is not supplied; it rejects an odd cycle. Once business roles matter, however, “left” and “right” are semantic data, not arbitrary colors, so callers should validate rather than silently swap them.

For cardinality matching, repeated copies of the same logical pair do not create additional compatible pairs. Normalize duplicate endpoints or retain stable edge identities while enforcing the one-endpoint rule. If repeated records represent capacity, the model is not an ordinary simple matching and must say so explicitly.

### Define feasibility and optimality

A matching $M\subseteq E$ satisfies

$$
\deg_M(v)\le 1\qquad\text{for every }v\in V.
$$

Its objective in the unweighted problem is $|M|$. A maximal matching admits no additional single edge, whereas a maximum matching has globally largest cardinality. Every maximum matching is maximal, but a maximal matching can be arbitrarily worse by a constant factor: in a four-vertex path, choosing the middle edge is maximal of size one while the two outer edges form a maximum matching of size two.

A perfect matching covers $V$, so it can exist only when $|L|=|R|$. An $L$-perfect matching covers $L$ and merely requires $|L|\le |R|$. Maximum cardinality does not imply either notion when the graph lacks enough compatible neighbors.

### Improve a matching by alternating paths

Relative to $M$, a path is alternating when its edges alternate between $E\setminus M$ and $M$. If its endpoints are free, it begins and ends with unmatched edges and is augmenting. Let $P$ denote its edge set. The symmetric difference

$$
M' = M\mathbin{\triangle}P=(M\setminus P)\cup(P\setminus M)
$$

removes every matched path edge and inserts every unmatched path edge. Internal path vertices lose one matched edge and gain one; the free endpoints each gain one. No outside incidence changes. An augmenting path contains one more unmatched edge than matched edge, hence $|M'|=|M|+1$.

Search must respect direction in an implicit alternating graph: from a left vertex traverse only unmatched edges to the right; from a right vertex traverse its unique matched edge back to the left. Reusing a visited set across separate augmentation attempts can hide valid paths. Layering many shortest augmenting paths, rather than finding one at a time, leads to Hopcroft–Karp.

### Prove Berge's lemma

**Theorem.** A matching $M$ is maximum if and only if no $M$-augmenting path exists.

If an augmenting path exists, toggling it produces a larger matching, so $M$ cannot be maximum.

For the converse, suppose a larger matching $M^*$ exists. Consider the graph formed by the symmetric difference $M\triangle M^*$. At each vertex, at most one edge comes from each matching, so every component is an isolated vertex, an alternating cycle, or an alternating path. Cycles contain equally many edges from both matchings. Paths whose endpoints have different matching incidences also have equal counts. Because $|M^*|>|M|$, at least one path component has one more $M^*$ edge than $M$ edge. It begins and ends with edges outside $M$, so both endpoints are free in $M$: it is an $M$-augmenting path, contradicting the premise. Therefore no larger matching exists.

The proof applies to every finite graph, not just bipartite graphs. Bipartiteness makes augmenting paths easier to find and connects them to flow and vertex-cover duality.

### Reduce matching to maximum flow

Construct a directed network with source $s$ and sink $t$:

- add $s\to \ell$ of capacity one for each $\ell\in L$;
- orient every bipartite edge as $\ell\to r$ with capacity one;
- add $r\to t$ of capacity one for each $r\in R$.

Every matching yields a flow of the same value by sending one unit along $s\to\ell\to r\to t$ for each matched pair. Conversely, every integral flow selects the middle edges carrying one. Unit source and sink arcs ensure no endpoint is selected twice. Integral capacities admit an integral maximum flow, so maximum flow value equals maximum matching size.

This is an exact reduction, not a claim that a generic flow implementation is always fastest. It transfers correctness, integrality, and cut certificates. A specialized augmenting-path or Hopcroft–Karp implementation can exploit the graph's structure with less representation overhead.

### Characterize one-side-perfect matchings with Hall's theorem

**Hall's theorem.** A finite bipartite graph has a matching covering every vertex of $L$ if and only if

$$
|N(X)|\ge |X|\qquad\text{for every }X\subseteq L.
$$

Necessity is immediate: if every $\ell\in X$ has a distinct matched neighbor, those $|X|$ vertices lie in $N(X)$.

For sufficiency, use the flow network but give each middle arc capacity $B=|L|+1$; source and sink arcs retain capacity one. A cut of capacity $|L|$ exists immediately before the left vertices, so a minimum cut never crosses a middle arc of capacity $B$. Let $S$ be its source side, $X=L\cap S$, and $Y=R\cap S$. Avoiding middle arcs forces $N(X)\subseteq Y$. Its capacity is

$$
|L\setminus X|+|Y|
\ge |L|-|X|+|N(X)|
\ge |L|.
$$

The first term counts source arcs entering $L\setminus X$; the second counts sink arcs leaving $Y$. Hall's inequality supplies the last step. Therefore every cut has capacity at least $|L|$, while the trivial cut has exactly $|L|$. Max-flow/min-cut gives a flow of value $|L|$, and integrality selects distinct middle edges covering every left vertex. This proves sufficiency.

Hall's theorem quantifies over all subsets, not just single vertices. Every left vertex may have several neighbors while a group still competes for too small a combined neighborhood. A returned deficient set $X$ with $|N(X)|<|X|$ is useful impossibility evidence.

### Derive Kőnig's equality and a certificate

Every vertex cover $C$ satisfies $|M|\le |C|$ for every matching $M$: each matched edge needs a cover endpoint, and distinct matched edges cannot charge the same endpoint. This is weak duality.

Given a maximum matching $M$, begin at all free vertices in $L$ and compute $Z$, the vertices reachable by alternating paths: unmatched edges go $L\to R$, and matched edges go $R\to L$. Define

$$
C=(L\setminus Z)\cup(R\cap Z).
$$

To see that $C$ covers every edge, suppose an edge $\ell r$ has neither endpoint in $C$. Then $\ell\in Z$ and $r\notin Z$. If $\ell r\notin M$, alternating reachability would put $r$ in $Z$. If $\ell r\in M$, a reached matched left vertex either was reached through that matched edge or is a free start; the latter cannot have a matched edge. Again $r\in Z$, a contradiction.

No alternating search from a free left vertex reaches a free right vertex, because that would be an augmenting path. Each reached right vertex is therefore matched to a reached left vertex. Counting matched edges shows $|C|=|M|$. Thus a valid maximum matching and the constructed minimum vertex cover have equal size. Publishing both lets an independent verifier check feasibility, coverage, and equality without trusting the solver's search trace.

### Execute and verify a small instance

The program below uses deterministic augmenting searches to find a matching, independently checks its feasibility, searches for any remaining augmenting path, and validates an equal-size cover. It uses only the CPython standard library.

<!-- bijux-verify: {"id":"bipartite-matching-certificate","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"matching=(('A', '2'), ('B', '3'), ('C', '1'))\nunmatched_left=('D',)\ncardinality=3 augmenting_path=False\ncover=('1', '2', '3') valid=True equality=True\n","stderr":""}} -->
```python
left = ("A", "B", "C", "D")
right = ("1", "2", "3")
adjacency = {
    "A": ("1", "2"),
    "B": ("2", "3"),
    "C": ("1",),
    "D": ("3",),
}

mate_right = {}


def augment(left_vertex, seen_right):
    for right_vertex in adjacency[left_vertex]:
        if right_vertex in seen_right:
            continue
        seen_right.add(right_vertex)
        if right_vertex not in mate_right or augment(
            mate_right[right_vertex], seen_right
        ):
            mate_right[right_vertex] = left_vertex
            return True
    return False


for vertex in left:
    augment(vertex, set())

mate_left = {left_vertex: right_vertex for right_vertex, left_vertex in mate_right.items()}
matching = tuple(sorted(mate_left.items()))
unmatched_left = tuple(vertex for vertex in left if vertex not in mate_left)


def has_augmenting_path():
    frontier = list(unmatched_left)
    seen_left = set(frontier)
    seen_right = set()
    while frontier:
        left_vertex = frontier.pop()
        for right_vertex in adjacency[left_vertex]:
            if mate_left.get(left_vertex) == right_vertex or right_vertex in seen_right:
                continue
            seen_right.add(right_vertex)
            if right_vertex not in mate_right:
                return True
            next_left = mate_right[right_vertex]
            if next_left not in seen_left:
                seen_left.add(next_left)
                frontier.append(next_left)
    return False


valid_matching = (
    len(mate_left) == len(mate_right)
    and all(right_vertex in adjacency[left_vertex] for left_vertex, right_vertex in matching)
    and len(set(mate_left)) == len(mate_left)
    and len(set(mate_right)) == len(mate_right)
)
cover = set(right)
valid_cover = all(
    left_vertex in cover or right_vertex in cover
    for left_vertex, neighbors in adjacency.items()
    for right_vertex in neighbors
)

print(f"matching={matching}")
print(f"unmatched_left={unmatched_left}")
print(f"cardinality={len(matching)} augmenting_path={has_augmenting_path()}")
print(
    f"cover={tuple(sorted(cover))} valid={valid_cover} "
    f"equality={valid_matching and len(matching) == len(cover)}"
)
```

The solver and verifier share data structures for compactness, so this is reproduction evidence rather than independent implementation assurance. A production verifier should parse an immutable certificate separately, reject undeclared vertices and edges, and use a simpler code path than the optimizer.

### Understand complexity and current interfaces

A straightforward algorithm searches for one augmenting path for each successful augmentation. With at most $O(V)$ augmentations and $O(E)$ work per search, its worst-case time is $O(VE)$. Hopcroft and Karp's 1973 algorithm finds a maximal set of shortest vertex-disjoint augmenting paths per phase and runs in $O(E\sqrt V)$ time in modern notation.

As retrieved on 2026-09-05, NetworkX 3.6.1 exposes `hopcroft_karp_matching` and aliases it as bipartite `maximum_matching`. Its documentation says the returned dictionary maps both directions and explains that disconnected graphs may require callers to supply the `top_nodes` partition. NetworkX represents bipartite graphs with ordinary graph classes and a node convention rather than a distinct enforcing type. These are version-scoped interface facts, not mathematical guarantees; validate inputs and normalize output at the application boundary.

### Govern production use

Persist stable vertex identities, semantic partition membership, logical edge identity, provenance, and a graph revision. Validate that sets are disjoint and exhaustive and that every edge crosses them. Reject or explicitly normalize duplicates, self-loops, undeclared endpoints, inconsistent role labels, and stale certificates.

Return more than a list of pairs: solver status, matching, cardinality, unmatched vertices, a minimum vertex cover or deficient Hall set where available, graph digest, deterministic tie-breaking policy, algorithm and version, resource limits, and limitations. Multiple maximum matchings are normal. If downstream behavior requires repeatability, define a secondary deterministic objective without falsely calling it part of maximum cardinality.

Real allocation often adds eligibility changes, quotas, priorities, fairness constraints, preferences, capacities, cancellation, or time windows. Maximum cardinality can concentrate undesirable outcomes even while matching the most vertices. Treat those constraints as policy inputs to a richer model and audit them explicitly; the pure matching theorem cannot certify them.

## Definitions and Notation

- $G=(L\mathbin{\dot\cup}R,E)$: finite bipartite graph with declared left and right classes.
- $M\subseteq E$: matching; $|M|$ is its cardinality.
- $\deg_M(v)$: number of matched edges incident to $v$, at most one.
- **free vertex**: vertex with $\deg_M(v)=0$.
- **maximal matching**: feasible matching to which no edge can be added.
- **maximum matching**: feasible matching of greatest cardinality.
- **perfect / $L$-perfect matching**: covers all vertices / all vertices of $L$.
- $M\triangle P$: symmetric difference of matching edges and path edges.
- $N(X)$: right-side neighbors of $X\subseteq L$.
- $C$: vertex cover, incident to every edge.
- $Z$: vertices reachable from free left vertices by alternating paths.
- **deficiency** of $X$: $|X|-|N(X)|$; a positive value obstructs an $L$-perfect matching.

## Mechanisms, Invariants, or Proof Structure

An augmenting path begins and ends outside $M$, so toggling its edges preserves the degree-at-most-one invariant and adds exactly one match. Berge's symmetric-difference proof shows that if a larger matching existed, at least one component of $M\triangle M^*$ would be an augmenting path. Unit-capacity flow transfers construction, integrality, and cut bounds. Hall's theorem characterizes the absence of a deficient left subset. Kőnig's alternating-reachability construction converts a maximum matching into a vertex cover of the same size. The matching and cover are equal lower and upper bounds, forming a compact optimality certificate.

## Alternatives and Trade-Offs

- **Greedy maximal matching:** simple and often fast; not exact for maximum cardinality.
- **One-path-at-a-time augmentation:** elementary and easy to inspect; $O(VE)$ worst case.
- **Hopcroft–Karp:** $O(E\sqrt V)$ and specialized for unweighted bipartite matching; more subtle layering invariants.
- **Unit-capacity maximum flow:** reuses mature flow infrastructure and certificates; introduces extra vertices/arcs and generic overhead.
- **Matching plus minimum cover:** compact independently checkable optimum evidence; does not prove a preferred optimum among ties.
- **Hall deficient set:** explains failure of one-side perfection; finding a useful minimal explanation may require additional policy.
- **Weighted assignment:** optimizes costs or preferences; answers a different question developed in ALGE-047.
- **$b$-matching or capacitated flow:** permits multiple incidences; requires different feasibility constraints.
- **Offline recomputation:** simple and globally coherent; may be too slow or unstable for rapid updates.
- **Incremental maintenance:** can reuse prior structure; complicates snapshot, deletion, and certificate correctness.

## Failure Modes and Misconceptions

- Maximal means locally unextendable, not maximum.
- A maximum matching need not be perfect.
- Checking $|N(\{\ell\})|\ge1$ for each left vertex does not establish Hall's condition.
- An alternating path is defined relative to a specific current matching.
- An augmenting search must traverse unmatched and matched edges in their proper alternating directions.
- Persistent visited state across roots can suppress legitimate augmentations.
- Greedy tie-breaking can change the returned matching and its size.
- Duplicate rows do not create distinct endpoint capacity in ordinary matching.
- A library's bipartite convention may not validate the caller's semantic partition.
- Equal cardinality proves optimality only after both matching and cover validate on the same snapshot.
- Kőnig's equality is specific to bipartite graphs; odd-cycle general graphs need different theory.
- Maximum cardinality does not imply fairness, stability, minimum cost, or schedule feasibility.

## Worked Examples

### Example 1

**Situation.** In the path $a-1-b-2$, choose the middle edge $1b$. **Reasoning.** No other edge can be added because each remaining edge touches $1$ or $b$, so the matching is maximal. Yet $\{a1,b2\}$ is a matching of size two. **Conclusion.** A maximal matching can be strictly smaller than a maximum matching.

### Example 2

**Situation.** Let $M=\{a1,b2\}$ and suppose edges $c1,a3$ also exist, with $c$ and $3$ free. **Reasoning.** The path $c-1-a-3$ alternates unmatched, matched, unmatched. Toggling replaces $a1$ by $c1$ and $a3$, while $b2$ remains. The size rises from two to three. **Conclusion.** Reassignment along an augmenting path can free capacity that a one-edge greedy test misses.

### Example 3

**Situation.** Two matchings have sizes four and six. **Reasoning.** In their symmetric difference, cycles and balanced paths contribute equal counts. The total two-edge advantage of the larger matching forces at least one component with one more larger-matching edge; that component is augmenting relative to the smaller matching. **Conclusion.** Global suboptimality implies a local augmenting witness.

### Example 4

**Situation.** $L=\{a,b,c\}$ and all three vertices have the sole neighbor $1$. **Reasoning.** Individual non-isolation holds, but for $X=L$, $N(X)=\{1\}$ and $1<3$. Hall's condition fails with deficiency two. **Conclusion.** Per-vertex degree checks cannot replace subset congestion checks.

### Example 5

**Situation.** $L=\{a,b\}$, $R=\{1,2,3\}$, and edges are $a1,a2,b2,b3$. **Reasoning.** Every singleton has at least one neighbor, and $N(L)=R$ has size three at least two. These are all left subsets, so Hall holds. Matching $\{a1,b2\}$ covers $L$. **Conclusion.** One-side perfection does not require equal partition sizes.

### Example 6

**Situation.** A matching contains $a1,b2,c3$ and a proposed cover is $\{1,2,3\}$. **Reasoning.** If the cover is validated against every edge, its size three upper-bounds all matchings. The supplied matching is feasible with size three. **Conclusion.** Equal valid lower and upper bounds certify maximum cardinality without replaying the solver.

### Example 7

**Situation.** A graph includes an edge between two declared left vertices. **Reasoning.** The unit-flow reduction assumes every middle arc goes from $L$ to $R$. Silently orienting the invalid edge changes the model and can reuse a semantic role incorrectly. **Conclusion.** Reject the input or repair its authoritative partition before optimization.

### Example 8

**Situation.** Two identical eligibility records say applicant $a$ may take slot $1$. **Reasoning.** Both records share endpoints, so choosing both would violate degree constraints. Deduplicating preserves cardinality; retaining provenance may still be necessary for audit. **Conclusion.** Record multiplicity and endpoint capacity are different concepts.

### Example 9

**Situation.** A deployment upgrades a library and the matching dictionary now appears in a different iteration order. **Reasoning.** Mathematical equality of matchings does not promise serialization order or a unique optimum. Normalize pairs and define a secondary tie-break if reproducible output is required. **Conclusion.** Determinism is an application policy layered on optimal cardinality.

### Example 10

**Situation.** Maximum cardinality assigns every available shift but repeatedly gives undesirable shifts to the same group. **Reasoning.** The binary eligibility graph and cardinality objective contain no distributional criterion. The solver can be exactly correct for the wrong policy objective. **Conclusion.** Encode and audit fairness or preference constraints explicitly; matching optimality alone cannot establish them.

## Cross-Program Connections

- **Data Structures Engineering:** adjacency layout, identity maps, and traversal state determine performance and auditability.
- **Operating Systems:** matching can model one-shot resource assignment, but preemption, duration, and capacity require scheduling models.
- **Database Engineering:** deduplication, stable identifiers, snapshot isolation, and provenance protect graph correctness.
- **Software Architecture:** solver and independent verifier are separate trust boundaries with versioned certificate schemas.
- **Systems Engineering:** eligibility, fairness, safety, and contingency rules belong to requirements and policy, not to the bare theorem.
- **API and Service Engineering:** published results need explicit status, graph revision, deterministic serialization, and limitation fields.

## References

1. J. E. Hopcroft and R. M. Karp, “An $n^{5/2}$ Algorithm for Maximum Matchings in Bipartite Graphs,” *SIAM Journal on Computing* 2(4), 1973, pp. 225–231, [doi:10.1137/0202019](https://doi.org/10.1137/0202019). Primary algorithm paper; retrieved 2026-09-05.
2. P. Hall, “On Representatives of Subsets,” *Journal of the London Mathematical Society* s1-10(1), 1935, pp. 26–30, [doi:10.1112/jlms/s1-10.37.26](https://doi.org/10.1112/jlms/s1-10.37.26). Primary theorem paper; retrieved 2026-09-05.
3. T. H. Cormen, C. E. Leiserson, R. L. Rivest, and C. Stein, *Introduction to Algorithms*, 4th ed., MIT Press, 2022, [publisher record](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/). Chapters on maximum flow and matching.
4. R. K. Ahuja, T. L. Magnanti, and J. B. Orlin, *Network Flows: Theory, Algorithms, and Applications*, Prentice Hall, 1993, [MIT record](https://dspace.mit.edu/handle/1721.1/49424). Matching and network-flow reductions.
5. J. Erickson, *Algorithms*, 1st ed., 2019, [author-hosted text](https://jeffe.cs.illinois.edu/teaching/algorithms/). Matching, augmenting paths, and flow foundations; retrieved 2026-09-05.
6. NetworkX Developers, “Bipartite algorithms,” NetworkX 3.6.1 documentation, [official documentation](https://networkx.org/documentation/stable/reference/algorithms/bipartite.html). Current interface and partition conventions; retrieved 2026-09-05.
7. NetworkX Developers, “Matching,” NetworkX 3.6.1 documentation, [official documentation](https://networkx.org/documentation/stable/reference/algorithms/matching.html). General matching terminology and interfaces; retrieved 2026-09-05.

## Exercises

### Exercise 1

Define maximal, maximum, perfect, and $L$-perfect matching. State every logical implication among these notions that holds without additional assumptions.

### Exercise 2

Let $L=\{a,b,c\}$, $R=\{1,2,3\}$, edges $a1,a2,b2,b3,c1$, and $M=\{a1,b2\}$. Find an augmenting path, toggle it, and verify the matching invariant and size change.

### Exercise 3

A service returns pairs $\{a1,b2,c3\}$ and cover $\{1,2,3\}$ for a declared bipartite graph. Design a verifier that can accept or reject the optimality claim. Include malformed-input and snapshot checks.

### Exercise 4

Compare one-at-a-time augmenting search, Hopcroft–Karp, and the unit-capacity flow reduction for a sparse graph used by an organization that already operates a verified max-flow library.

### Exercise 5

A volunteer platform must assign people to shifts. Each shift accepts one person, but volunteers have ranked preferences, weekly limits, and a rule that critical skills must retain one unassigned backup. Explain why maximum cardinality matching is insufficient and propose a bounded richer model and certificate strategy.

## Answers to the Exercises

### Answer 1

A matching is maximal when no single edge can be added while preserving feasibility; maximum when no matching has larger cardinality; perfect when it covers every vertex; and $L$-perfect when it covers every left vertex. Every perfect matching is $L$-perfect and maximum. Every $L$-perfect matching is maximum because no matching can use more than $|L|$ edges, but it need not be perfect when $|R|>|L|$. Every maximum matching is maximal. The converses fail in general: a maximal matching may be suboptimal; a maximum matching may leave vertices unmatched; and an $L$-perfect matching need not cover $R$. If $|L|=|R|$, $L$-perfect also implies perfect.

### Answer 2

The path $c-1-a-2-b-3$ uses edges $c1\notin M$, $a1\in M$, $a2\notin M$, $b2\in M$, and $b3\notin M$. Its endpoints $c$ and $3$ are free. Toggling gives $M'=\{c1,a2,b3\}$. Every endpoint occurs once, so the degree-at-most-one invariant holds. The path contained three unmatched and two matched edges, hence the cardinality rose from two to three. Since all three left vertices are now covered, the result is maximum and $L$-perfect.

### Answer 3

Parse a canonical graph snapshot containing disjoint exhaustive partitions, stable vertex and edge identities, and a digest. Reject self-loops, undeclared endpoints, same-side edges, ambiguous duplicates, or a certificate for another digest. For every proposed pair, require an existing cross edge and count each endpoint once; this proves matching feasibility and yields the lower bound three. For every graph edge, require at least one endpoint in the proposed cover; reject duplicate or undeclared cover vertices and compute its cardinality three. The universal inequality $|M|\le|C|$, plus equality, proves the matching maximum and cover minimum. Report validation separately from solver status. Acceptable implementations may also validate an equivalent flow-cut certificate, but the evaluation criteria are full graph validation, matching feasibility, cover coverage, shared snapshot identity, and exact equality.

### Answer 4

One-at-a-time augmentation is the smallest implementation and is suitable for small graphs, teaching, and a simple verifier, but costs $O(VE)$ in the worst case. Hopcroft–Karp exploits batches of shortest augmenting paths for $O(E\sqrt V)$ time and is the natural specialized choice for large sparse unweighted bipartite instances, at the cost of subtler BFS/DFS layer invariants. A unit-capacity flow reduction expands the graph and may lose constant factors, but it reuses the organization's tested flow parser, resource controls, and flow-cut certificate path. A sound design could use Hopcroft–Karp for production speed and independently emit/check a minimum vertex cover, or reuse max flow when operational assurance dominates performance. Benchmark on representative snapshots; do not infer the choice from asymptotics alone.

### Answer 5

Plain maximum cardinality sees only eligibility and one-use endpoints. It cannot optimize rankings, enforce weekly multi-shift limits, or reserve skilled backup capacity. A bounded model can use min-cost capacitated flow: source-to-volunteer capacity equals the weekly limit; volunteer-to-shift arcs encode eligibility and preference cost; shift-to-sink capacity is one. Backup protection can reserve one qualified volunteer outside the assigned set through an explicit skill-group constraint; if that coupling is not representable in ordinary flow, use an integer program with binary assignment and backup variables. First maximize policy-feasible coverage, then minimize preference cost lexicographically. Publish the input digest, assignments, unmatched demand, objective vector, constraint residuals, and solver bound/status. Independently validate every hard constraint and recompute objectives; for an integer program, a solver optimality gap is evidence with stated limits, not the matching-plus-cover theorem. Alternative policies are acceptable only if they formalize preferences, workload, and backup preservation and specify how feasibility and optimality are checked.
