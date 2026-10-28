---
module_id: ALGE-042
program: Algorithm Engineering
level: 1
module_number: 42
title: Ford-Fulkerson Method
status: complete
last_verified: 2026-09-05
---

# Ford-Fulkerson Method

## One-Page Review

### Governing question

How does repeated residual-path augmentation compute a maximum flow, and which assumptions about path selection and capacity arithmetic are necessary for termination, complexity, and trustworthy implementation?

### Essential definitions

- The **Ford-Fulkerson method** starts with a feasible flow and repeatedly augments along any residual source-to-sink path.
- An **augmenting path** is a directed $s$-$t$ path in the residual graph whose every residual capacity is positive.
- The **bottleneck** $\Delta$ is the minimum residual capacity on that path.
- A **path-selection policy** chooses the next augmenting path; the method does not prescribe one.
- **Termination** means the method reaches an iteration with no augmenting path after finitely many augmentations.
- **Partial correctness** means that if the method terminates normally, its returned flow is maximum.
- **Integral preservation** means an integral starting flow and integral capacities yield integral flows after every augmentation.
- A running-time bound is **pseudo-polynomial** when it depends on numeric capacity magnitude rather than only on input encoding length.

### Central model, mechanism, or theorem

Starting from a feasible flow $f$, repeat:

1. find any residual $s$-$t$ path $P$;
2. set $\Delta=\min_{a\in P}c_f(a)$;
3. add $\Delta$ on forward residual steps and subtract it on reverse steps;
4. stop when no residual $s$-$t$ path exists.

Each iteration preserves feasibility and raises $|f|$ by exactly $\Delta$. On normal termination, residual reachability supplies a cut whose capacity equals the flow value, so the flow is maximum. With nonnegative integer capacities and zero initial flow, every $\Delta\ge1$, so at most $|f^*|$ augmentations occur. This is a termination proof and a pseudo-polynomial bound, not a strongly polynomial guarantee. Arbitrary real capacities and arbitrary path choices need not terminate.

### Critical invariants

- The original network, source, sink, capacities, and edge identities belong to one immutable snapshot.
- The current flow is feasible before and after every committed augmentation.
- Every predecessor denotes one positive residual direction and its original edge identity.
- The recovered predecessor chain is a connected, acyclic $s$-$t$ path.
- The bottleneck is positive and is recomputed against the same snapshot immediately before update.
- Every path edge changes by the same bottleneck with the correct residual sign.
- Flow value increases exactly by the bottleneck.
- Exact integral arithmetic preserves integrality and makes the finite-termination argument applicable.
- Normal exhaustion, cancellation, resource limits, arithmetic failure, and invalid input are distinct outcomes.

### Common failures

Common failures include calling Ford-Fulkerson one fixed algorithm; omitting reverse residuals; applying a stale predecessor path; choosing zero or more than the bottleneck; relying on endpoint pairs when edges are parallel; assuming DFS always has a polynomial iteration count; deriving a polynomial bound from the numeric value $|f^*|$; using floating tolerances while quoting the exact-arithmetic proof; publishing a cancelled feasible flow as maximum; mutating a path in place without rollback; and returning only a scalar without edge flows or a residual-cut certificate.

### Compact example

Suppose two available augmenting paths have bottlenecks two and five. Either is legal. Choosing the first increases flow by two; choosing the second increases it by five. Correctness on termination does not depend on which was chosen, but the iteration count and even finite termination over arbitrary real capacities can depend on that choice. Ford-Fulkerson is therefore a method parameterized by path policy.

### Connections

[ALGE-041](./041-flow-networks-and-residual-graphs.md) defines feasible flows and paired residual state. [ALGE-031](./031-breadth-first-search.md) and [ALGE-032](./032-depth-first-search.md) supply path searches. [ALGE-043](../ROADMAP.md#block-05--flows-matching-and-combinatorial-optimization) fixes breadth-first selection to obtain the Edmonds-Karp bound, while [ALGE-045](../ROADMAP.md#block-05--flows-matching-and-combinatorial-optimization) develops the max-flow/min-cut theorem in full.

## Governing Question

Given a finite directed capacity network and a feasible initial flow, how can an implementation repeatedly find, validate, and atomically apply residual augmentations, and what can it honestly claim about feasibility, integrality, termination, maximum value, complexity, and operational status?

Ford-Fulkerson is best understood as a proof-guided family of algorithms. Its invariant and stopping argument are general; its progress rate depends on capacity arithmetic and the chosen augmenting paths. Conflating these layers produces both mathematical errors and production defects.

## Why This Matters

The method reveals the central idea behind maximum flow: a current decision is not permanent because residual reverse arcs permit cancellation and rerouting. This idea recurs in matching, circulation, assignment, min-cost flow, and many primal-dual algorithms. It also provides a clean example of how an invariant, a progress measure, a stopping certificate, and a representation cooperate.

The familiar instruction “choose any augmenting path” hides important engineering questions. Which deterministic order is used? Can arithmetic represent the bottleneck exactly? Can an adversary force many tiny augmentations? What happens if capacity data changes during a search? Is a time-limited result merely feasible or certified maximum? Does a restored checkpoint use the identical graph snapshot? A robust implementation answers these before exposing a `solve` operation.

## Prerequisites and Retrieval

Retrieve directed graphs, paths, reachability, asymptotic analysis, binary encoding length, loop invariants, exact arithmetic, cuts, snapshots, transactions, and cancellation semantics. Review [ALGE-041](./041-flow-networks-and-residual-graphs.md) for $r_e^+=c(e)-f(e)$, $r_e^-=f(e)$, augmentation preservation, net flow value, and stable residual edge identity. Review [ALGE-032](./032-depth-first-search.md) for iterative DFS and predecessor reconstruction.

## Learning Objectives

After completing this module, you should be able to:

1. state Ford-Fulkerson as a method parameterized by augmenting-path policy;
2. prove feasibility and exact value increase for every committed augmentation;
3. prove partial correctness from residual exhaustion and a cut certificate;
4. prove finite termination and integral preservation for integer capacities;
5. distinguish pseudo-polynomial $O(E|f^*|)$ behavior from a polynomial input-size bound;
6. explain why rational scaling can terminate yet be computationally poor;
7. explain why arbitrary real capacities invalidate unconditional termination;
8. implement deterministic DFS path selection with stable edge identities;
9. validate paths, arithmetic, snapshots, transactions, cancellation, and output evidence;
10. choose a safer bounded policy when input or service guarantees require one.

## Core Exposition

### Separate the method from its policy

Let $G=(V,E)$ be a finite directed multigraph with source $s$, sink $t$, nonnegative capacities $c$, and feasible starting flow $f_0$. The zero flow is the usual start. At iteration $i$, construct the residual graph $G_{f_i}$. If $t$ is reachable from $s$, recover one residual path $P_i$, compute

$$
\Delta_i=\min_{a\in P_i}c_{f_i}(a),
$$

and augment by $\Delta_i$. Otherwise, return $f_i$ as maximum.

“Find one path” is an interface, not a completed algorithm specification. DFS, BFS, widest-path selection, capacity scaling, and other rules instantiate different algorithms with different traces and bounds. Neighbor order is part of determinism. Two conforming implementations may return different edge-level maximum flows even when the maximum value is unique.

### Maintain feasibility and strict progress

Assume $f_i$ is feasible and $P_i$ is a positive residual path. A forward step changes $f(e)$ to $f(e)+\Delta_i$; because $\Delta_i\le c(e)-f(e)$, the result does not exceed capacity. A reverse step changes it to $f(e)-\Delta_i$; because $\Delta_i\le f(e)$, the result remains nonnegative.

At each internal path vertex, one residual adjustment enters and one leaves with the same amount. Their signed effects cancel in the conservation balance. At $s$, net outflow rises by $\Delta_i$; at $t$, net inflow rises by the same amount. Therefore

$$
|f_{i+1}|=|f_i|+\Delta_i>|f_i|.
$$

Strict progress alone does not imply finitely many iterations: a strictly increasing bounded real sequence may have infinitely many terms. The numeric domain matters.

### Prove correctness when the loop stops

Suppose a search finds no residual $s$-$t$ path. Let $S$ be the vertices reachable from $s$ in $G_f$. Then $s\in S$ and $t\notin S$. Every original edge from $S$ to $V\setminus S$ must be saturated; otherwise its positive forward residual would cross the boundary. Every original edge entering $S$ must carry zero flow; otherwise its positive reverse residual would cross from $S$ outward.

Summed flow conservation gives

$$
|f|=f(\delta^+(S))-f(\delta^-(S))
=c(\delta^+(S))-0=c(S,V\setminus S).
$$

Every feasible flow is at most every cut capacity, so equality proves this flow maximum and this cut minimum. This establishes partial correctness of the method: if it reaches normal residual exhaustion with preserved invariants, its result is optimal. ALGE-045 develops the theorem and equivalent formulations more broadly.

### Establish integer termination

Assume capacities and the initial flow are integers. Forward and reverse residual capacities are integers, so every bottleneck is a positive integer. Augmentation adds or subtracts that integer, preserving integral flow. Since each iteration raises value by at least one and every flow value is bounded above by the total capacity leaving $s$, only finitely many iterations are possible.

Starting from zero, the number of augmentations is at most $|f^*|$, the value of a maximum flow. If a path search and update take $O(V+E)$ with adjacency lists, a safe elementary bound is $O((V+E)|f^*|)$; conventions that charge $O(E)$ per iteration state $O(E|f^*|)$. Both depend on numeric value.

If one edge capacity is $2^k$, its binary encoding uses $O(k)$ bits, while $|f^*|$ may be $2^k$. A bound linear in $|f^*|$ can therefore be exponential in input bit length. That is why this is pseudo-polynomial, not a general polynomial-time guarantee.

### Treat rational and real capacities precisely

For finitely represented rational capacities, multiplying by a common positive denominator converts the instance to integers without changing which flows are feasible after rescaling. This proves finite termination under exact rational arithmetic. It does not promise practicality: a common denominator can be enormous, and the resulting numeric bound can dwarf the encoded graph size.

For arbitrary real, including irrational, capacities, arbitrary augmenting-path choices can produce an infinite sequence of ever-smaller bottlenecks. Classical counterexamples can even converge below the maximum value. Consequently, “any path always terminates” is false without a discrete-domain assumption or a stronger selection rule. Edmonds-Karp restores a capacity-independent finite bound by always selecting a shortest residual path in edge count.

Floating-point arithmetic is neither exact real arithmetic nor exact rational arithmetic. Rounding can create tiny positive residuals, erase legitimate residuals, violate conservation, or make a tolerance-dependent stopping condition. If measurements require decimals, declare quantization, units, range, rounding, conservation tolerance, and what status a tolerance-based result receives. Do not cite the integral proof for a float implementation.

### Run a deterministic DFS instantiation

The following implementation deliberately exposes the policy. It stores logical flows, derives stable residual steps, performs deterministic iterative DFS, reconstructs an edge-identity path, applies to a copy, and validates before commit.

<!-- bijux-verify: {"id":"ford-fulkerson-dfs","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"augmentations=((('sa:f', 'ab:f', 'bt:f'), 2), (('sa:f', 'at:f'), 2), (('sb:f', 'bt:f'), 2))\nflows=(('ab', 2), ('at', 2), ('bt', 4), ('sa', 4), ('sb', 2))\nvalue=6\nvalid=True\nresidual_path=False\n","stderr":""}} -->
```python
edges = {
    "sa": ("s", "a", 4), "sb": ("s", "b", 3),
    "ab": ("a", "b", 2), "at": ("a", "t", 2),
    "bt": ("b", "t", 4),
}
vertices = {"s", "a", "b", "t"}


def residual_steps(flow):
    adjacency = {vertex: [] for vertex in vertices}
    for edge_id, (tail, head, capacity) in sorted(edges.items()):
        if capacity > flow[edge_id]:
            adjacency[tail].append((head, edge_id, "f", capacity - flow[edge_id]))
        if flow[edge_id] > 0:
            adjacency[head].append((tail, edge_id, "r", flow[edge_id]))
    for steps in adjacency.values():
        steps.sort(key=lambda step: (step[0], step[1], step[2]))
    return adjacency


def find_path(flow):
    adjacency = residual_steps(flow)
    seen = {"s"}
    predecessor = {}
    stack = [("s", 0)]
    while stack:
        vertex, index = stack[-1]
        if vertex == "t":
            break
        if index == len(adjacency[vertex]):
            stack.pop()
            continue
        stack[-1] = (vertex, index + 1)
        head, edge_id, direction, residual = adjacency[vertex][index]
        if head not in seen:
            seen.add(head)
            predecessor[head] = (vertex, edge_id, direction, residual)
            stack.append((head, 0))
    if "t" not in seen:
        return None
    path = []
    cursor = "t"
    while cursor != "s":
        prior, edge_id, direction, residual = predecessor[cursor]
        path.append((edge_id, direction, residual))
        cursor = prior
    return tuple(reversed(path))


def validate(flow):
    balance = {vertex: 0 for vertex in vertices}
    if set(flow) != set(edges):
        return False
    for edge_id, (tail, head, capacity) in edges.items():
        amount = flow[edge_id]
        if not isinstance(amount, int) or not 0 <= amount <= capacity:
            return False
        balance[tail] -= amount
        balance[head] += amount
    return balance["a"] == balance["b"] == 0 and -balance["s"] == balance["t"]


def value(flow):
    return sum(flow[e] for e, (u, _, _) in edges.items() if u == "s")


def solve():
    flow = {edge_id: 0 for edge_id in edges}
    trace = []
    while (path := find_path(flow)) is not None:
        delta = min(residual for _, _, residual in path)
        candidate = dict(flow)
        for edge_id, direction, _ in path:
            candidate[edge_id] += delta if direction == "f" else -delta
        if not validate(candidate):
            raise AssertionError("candidate flow is infeasible")
        flow = candidate
        trace.append((tuple(f"{edge_id}:{direction}" for edge_id, direction, _ in path), delta))
    return flow, tuple(trace)


flow, trace = solve()
print(f"augmentations={trace}")
print(f"flows={tuple(sorted(flow.items()))}")
print(f"value={value(flow)}")
print(f"valid={validate(flow)}")
print(f"residual_path={find_path(flow) is not None}")
```

The observed three-augmentation trace is a consequence of this graph and ordering. The final value six also equals the capacity of the cut $S=\{s,a,b\}$, whose crossing edges `at` and `bt` have capacities two and four. The local execution checks this implementation on one instance; the invariant and cut arguments support the general claim under their assumptions.

### Preserve edge identity and reverse choices

An augmenting path is a sequence of residual edge identities, not merely vertices. With parallel edges, a vertex predecessor does not reveal which original edge to change unless the predecessor record stores the residual slot or logical edge plus direction. With anti-parallel original edges, a residual step $v\to u$ could mean increasing an original $v\to u$ edge or cancelling an original $u\to v$ edge. Those operations are not interchangeable in edge-level output.

At least one reverse residual may appear in an augmenting path. Its role is not optional optimization; it is how the method corrects an earlier route. Tests should force cancellation, parallel identities, anti-parallel identities, saturated edges, zero-capacity edges, and terminal incident edges.

### Validate iteration boundaries

Before search, validate the graph revision and the complete feasible flow. During search, store predecessor residual identity and snapshot revision. Before update, reconstruct a simple connected $s$-$t$ path, recompute every positive residual and the bottleneck from the same committed state, and reject repeated inconsistent edge-directions.

Apply changes to a copy or transaction. Use checked arithmetic. Revalidate capacity, internal conservation, source/sink value equality, value increase by exactly $\Delta$, and residual pairing. Only then publish the candidate as the next committed flow. A failure cannot expose a half-augmented path.

At normal exhaustion, persist the reached set $S$ and independently recompute: $t\notin S$; all outgoing crossing originals are saturated; all incoming crossing originals carry zero; flow value equals cut capacity. This certificate is much cheaper to verify than replaying every search choice.

### Bound resources and describe statuses

A service must not promise prompt completion from the integer termination theorem alone. Validate capacity bit widths and total source capacity, estimate the pseudo-polynomial bound, and use a path policy with a suitable capacity-independent guarantee when latency matters. Limit graph size, work, memory, trace volume, and checkpoint frequency.

Return distinct statuses such as `optimal`, `feasible_incomplete`, `invalid_input`, `arithmetic_failure`, `resource_limit`, and `internal_error`. Cancellation or a work limit may leave the last committed flow feasible, but no residual-exhaustion certificate exists. Label it incomplete and retain a resumable snapshot if supported.

### Place current libraries in context

Current Boost.Graph documentation exposes named maximum-flow algorithms such as Edmonds-Karp and requires explicit capacity, residual-capacity, and reverse-edge maps. Current Google OR-Tools documentation exposes `SimpleMaxFlow`, directed arcs with integer capacities, solver status, optimal value, per-arc flow, and source/sink sides of a cut. These are current interface observations, not evidence that an arbitrary hand-written Ford-Fulkerson loop has their termination or performance properties.

For production, prefer a maintained bounded implementation unless the educational or domain purpose specifically requires Ford-Fulkerson path control. Even then, wrap the method in input validation, deterministic policy, resource governance, independent result checks, and explicit evidence.

## Definitions and Notation

- $G=(V,E)$: finite directed capacity multigraph.
- $c(e)$: nonnegative original capacity of edge $e$.
- $f_i$: feasible original-edge flow before iteration $i$.
- $G_{f_i}$: residual graph of $f_i$.
- $c_{f_i}(a)$: capacity of residual direction $a$.
- $P_i$: selected residual $s$-$t$ path.
- $\Delta_i$: minimum residual capacity on $P_i$.
- $f^*$: a maximum flow.
- $|f|$: net source outflow.
- $S$: vertices reachable from $s$ after residual exhaustion.
- $c(S,V\setminus S)$: capacity of original edges crossing from $S$ outward.
- **Policy**: deterministic or nondeterministic rule selecting $P_i$.
- **Certificate**: independently checkable evidence supporting an output claim.

## Mechanisms, Invariants, or Proof Structure

Initialization supplies a feasible flow, usually zero. Residual search either finds a path or produces the reached set. A found path has a positive bottleneck; atomic signed updates preserve edge bounds and conservation, preserve integrality in an exact integral domain, and raise value exactly by the bottleneck. Under integral capacities, the integer-valued progress measure and finite upper bound prove termination. On normal exhaustion, residual reachability identifies a cut saturated outward and empty inward; its capacity equals the current value and certifies optimality. The path-selection policy controls the trace and complexity without changing these invariant arguments.

## Alternatives and Trade-Offs

- **DFS selection:** simple and memory-efficient; arbitrary choices expose pseudo-polynomial behavior and poor predictability.
- **BFS selection (Edmonds-Karp):** adds a capacity-independent polynomial bound; repeated breadth-first scans can still be costly.
- **Widest augmenting path:** seeks a large bottleneck; needs priority machinery and a separate bound analysis.
- **Capacity scaling:** ignores small residuals until later scales; improves control for integer capacities but adds policy state.
- **Push-relabel:** abandons whole $s$-$t$ path selection and performs local pushes under a different invariant; often preferable in general-purpose implementations.
- **Exact integer arithmetic:** supports integral proofs and reproducibility; requires bounded inputs or big-integer cost control.
- **Exact rational arithmetic:** preserves exactness; denominator growth and comparison cost can be severe.
- **Quantized fixed point:** operationally bounded and reproducible; introduces declared approximation/model error.
- **Floating point:** convenient for measured inputs; invalidates exact feasibility and termination reasoning unless carefully reformulated.
- **Full trace:** strong replay evidence; can be much larger than the input. Final flow plus cut is compact but does not reproduce the route choices.

## Failure Modes and Misconceptions

- Ford-Fulkerson is a method, not a unique path-selection algorithm.
- Strictly increasing bounded flow values do not prove finite termination over arbitrary reals.
- An $O(E|f^*|)$ bound is pseudo-polynomial because $|f^*|$ is a numeric value.
- Scaling rationals proves termination under exact arithmetic, not efficient denominator handling.
- Floating-point values do not inherit exact integer or rational proofs.
- Reverse residual edges are required to undo earlier choices.
- A predecessor must name the residual edge and direction, not only its endpoint.
- Search and augmentation over different graph revisions are invalid.
- A cancelled or resource-limited feasible flow is not certified maximum.
- A maximum value alone does not establish per-edge feasibility or identify the input snapshot.
- Different legal policies can return different maximum edge flows.
- Solver success does not validate units, domain assumptions, or static single-commodity modeling.

## Worked Examples

### Example 1

**Situation.** Zero flow has augmenting path residual capacities $(5,3,7)$. The bottleneck is three, so all three path edges receive three and the middle edge saturates. Flow value rises from zero to three. **Conclusion.** One common bottleneck preserves conservation and guarantees strict progress.

### Example 2

**Situation.** A current flow uses two units on $a\to b$. A later residual path contains the reverse $b\to a$ with bottleneck one. Updating that step subtracts one from the original edge, while other path steps reroute the unit toward $t$. **Conclusion.** Reverse residual traversal corrects a prior routing decision; it is not negative shipment.

### Example 3

**Situation.** Integral maximum value is eleven and current value is seven. Every later augmentation has integral bottleneck at least one, so no more than four additional augmentations can occur. **Conclusion.** Integrality turns value into a discrete decreasing gap.

### Example 4

**Situation.** A capacity $2^{80}$ occupies only 81 binary bits. A hypothetical policy taking unit bottlenecks could require $2^{80}$ augmentations. **Conclusion.** A bound linear in flow magnitude is not polynomial in encoded input length.

### Example 5

**Situation.** Capacities are $1/6$ and $1/10$. Scaling by the least common denominator 30 yields capacities five and three, so exact integral termination applies and results rescale by $1/30$. **Conclusion.** Rational scaling is mathematically valid, though large denominators may be impractical.

### Example 6

**Situation.** A floating computation leaves residual $1.1\times10^{-16}$ on an edge intended to be saturated. Testing `residual > 0` admits a meaningless tiny augmentation; using an undocumented epsilon may instead remove a real small capacity. **Conclusion.** Floating stopping is a modeling policy, not the exact theorem.

### Example 7

**Situation.** After normal exhaustion, reached set $S$ has outgoing capacity nine, all outgoing crossing edges carry nine total, and entering crossing flow is zero. Current value is nine. **Conclusion.** Flow-cut equality supplies an independently checkable optimality certificate.

### Example 8

**Situation.** Search records path edge IDs under revision 17. Before update, revision 18 lowers one capacity below its current flow. Applying the old bottleneck corrupts feasibility. **Conclusion.** Search, bottleneck, update, and validation must use one pinned revision.

### Example 9

**Situation.** A work limit fires after 400 augmentations. The last committed flow validates at value 73, but a residual path remains. **Conclusion.** The result may be published only as feasible and incomplete, with no maximum claim.

### Example 10

**Situation.** Two parallel $u\to v$ edges have capacities four and six. A predecessor storing only `(u,v)` cannot tell which flow to raise. Storing `edge-7:f` identifies the exact residual operation. **Conclusion.** Stable edge-direction identity is part of correctness.

## Cross-Program Connections

- Data Structures Engineering owns adjacency layout, predecessor identity, stacks, queues, and paired-edge representations.
- Theory of Computation and Algorithm Engineering distinguish termination, partial correctness, numeric measures, and input encoding.
- Database Engineering owns snapshot isolation, transactions, checkpoints, and atomic publication of validated states.
- Systems and Platform Engineering own cancellation, resource budgets, observability, reproducibility, and multi-tenant safeguards.
- Security Engineering reviews adversarial capacities, numeric overflow, denial-of-service traces, corrupted checkpoints, and ambiguous identifiers.
- Distributed Systems and Network Engineering determine whether a static, centrally known, single-commodity model represents the operating domain.

## References

1. Lester R. Ford Jr. and Delbert R. Fulkerson, “Maximal Flow Through a Network,” *Canadian Journal of Mathematics* 8, 399–404, 1956, DOI [10.4153/CJM-1956-045-5](https://doi.org/10.4153/CJM-1956-045-5). Primary source and publisher record checked 2026-09-05.
2. Lester R. Ford Jr. and Delbert R. Fulkerson, “A Simple Algorithm for Finding Maximal Network Flows and an Application to the Hitchcock Problem,” *Canadian Journal of Mathematics* 9, 210–218, 1957, DOI [10.4153/CJM-1957-024-0](https://doi.org/10.4153/CJM-1957-024-0). Primary source checked 2026-09-05.
3. Lester R. Ford Jr. and Delbert R. Fulkerson, *Flows in Networks*, Princeton University Press, 1962; 2025 digital edition. [Official publisher record](https://doi.org/10.1515/9780691273457), checked 2026-09-05.
4. Ravindra K. Ahuja, Thomas L. Magnanti, and James B. Orlin, *Network Flows: Theory, Algorithms, and Applications*, Prentice Hall, 1993, Chapters 4–6. [MIT-hosted record](https://dspace.mit.edu/handle/1721.1/49424), checked 2026-09-05.
5. Thomas H. Cormen et al., *Introduction to Algorithms*, 4th ed., MIT Press, 2022, Chapter 24. [Official publisher record](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/), checked 2026-09-05.
6. Jeff Erickson, *Algorithms*, 1st ed., 2019, maximum-flow chapter. [Author-hosted book](https://jeffe.cs.illinois.edu/teaching/algorithms/), checked 2026-09-05.
7. Boost C++ Libraries, “Network Flow” and “Edmonds-Karp Maximum Flow,” current Boost.Graph documentation. [Official documentation](https://www.boost.org/doc/libs/latest/libs/graph/doc/html/graph/algorithms/network_flow/network_flow_overview.html), checked 2026-09-05.
8. Google, “Maximum Flows,” OR-Tools documentation, updated 2026-03-18. [Official documentation](https://developers.google.com/optimization/flow/maxflow), checked 2026-09-05.

## Exercises

### Exercise 1

State the Ford-Fulkerson loop precisely for an initially feasible flow. Identify the path-selection policy, loop invariant, progress measure, normal stopping condition, and returned optimality evidence.

### Exercise 2

Assume integral capacities, zero initial flow, and maximum value 23. After six augmentations the value is 15. Prove integrality is preserved and bound the remaining augmentations. Then explain why the resulting total bound is pseudo-polynomial.

### Exercise 3

Diagnose an implementation that stores vertex-only predecessors, searches revision 12, augments revision 13 in place, uses unchecked 32-bit sums, accepts floating capacities, stops at an undocumented epsilon, and reports `optimal` after cancellation.

### Exercise 4

Compare arbitrary DFS, Edmonds-Karp BFS, capacity scaling, and push-relabel for a classroom trace tool, an adversarial public API, and a large internal batch solver. State which evidence remains necessary regardless of algorithm.

### Exercise 5

Design a resumable maximum-flow operation for exact integer capacity uploads. Specify input bounds, deterministic policy, iteration transaction, checkpoint, cancellation and resource-limit semantics, optimality certificate, independent validation, and published provenance.

## Answers to the Exercises

### Answer 1

Given one immutable finite network and feasible $f$, construct $G_f$. The policy selects a positive residual $s$-$t$ path $P$ if one exists. Compute $\Delta=\min_{a\in P}c_f(a)$, apply signed original-edge updates on a candidate state, validate, and commit. Repeat; if no path exists, stop normally.

The loop invariant is that the committed flow is feasible and corresponds exactly to its residual graph and snapshot. Value is the progress measure and rises by positive $\Delta$. Normal stopping is residual exhaustion, not timeout or cancellation. Return original-edge flows, value, reached set $S$, and recomputed evidence that outward crossing edges are saturated, inward crossing flow is zero, and $|f|=c(S,V\setminus S)$.

### Answer 2

Initially every flow is integer. If current flows and capacities are integers, every forward residual $c(e)-f(e)$ and reverse residual $f(e)$ is integer. The minimum positive path residual is therefore a positive integer. Adding or subtracting it preserves integrality, completing induction over iterations.

The remaining value gap is $23-15=8$. Each augmentation raises value by at least one without exceeding 23, so at most eight further augmentations occur. From zero, at most 23 occur. This uses the numeric value 23; in general a value $2^k$ needs only $O(k)$ bits to encode, so $O(E|f^*|)$ can be exponential in input bit length and is pseudo-polynomial.

### Answer 3

Predecessors must retain the exact residual slot or original edge ID plus direction, especially for parallel and anti-parallel edges. Pin one revision through search, bottleneck recomputation, update, validation, and publication; revision 12 evidence cannot authorize revision 13 mutation. Apply to a copy or rollback-capable transaction, then atomically commit.

Use checked sufficiently wide integers or exact governed arithmetic for balances, value, and residuals. Floating capacities require a separately specified quantized/tolerance model and cannot inherit the integral proof. Documented tolerance must be part of input/output semantics and evidence. Cancellation returns the last validated state as `feasible_incomplete`, never `optimal`, unless an independently verified exhaustion certificate already exists.

### Answer 4

Arbitrary DFS is excellent for exposing residual mechanics in a classroom trace tool, provided examples also teach its weak bound. Edmonds-Karp is safer for an adversarial API because its BFS rule supplies a capacity-independent polynomial bound, though graph-size and work limits remain necessary. Capacity scaling is attractive for bounded exact integer instances and can control small augmentations, but introduces scale-state and numeric assumptions. Push-relabel is often a stronger production candidate for a large batch solver because it uses local preflow operations and robust polynomial analysis, at the cost of different invariants and more complex traces.

All choices still require input and snapshot validation, stable edge identity, checked arithmetic, feasible edge-flow output, deterministic/versioned policy, explicit statuses, resource governance, and an independently recomputed flow-cut certificate before an optimal claim.

### Answer 5

Accept a complete vertex/edge universe, distinct terminals, stable unique edge IDs, common units, and nonnegative integer capacities within declared per-edge bit width, total source-capacity bound, vertex/edge limits, and trace budget. Hash the canonical network revision. Select a deterministic versioned path policy; if using arbitrary DFS, calculate an admissible worst-case work bound or reject inputs that cannot meet the service objective.

Each iteration checkpoints the last committed feasible flow and policy state, searches the pinned revision, records residual edge-directions, recomputes positive residuals and checked bottleneck, updates a candidate, and verifies capacity, conservation, value increase, pairing, and revision before atomic commit. A checkpoint contains network digest, algorithm/policy version, exact flow, iteration count, validated value, optional frontier state, evidence version, and transaction status. Resume only after full checkpoint validation.

Cancellation and work limits return the last committed flow as `feasible_incomplete` with reason and remaining resumability; invalid data, overflow, and internal invariant failure receive distinct statuses. Normal exhaustion publishes edge flows, value, reached set, cut capacity, saturation/zero-inward checks, toolchain and algorithm versions, input digest, resource use, and limitations. A structurally separate verifier recomputes feasibility and the flow-cut equality. This evidence supports the recorded snapshot only; it does not validate the uploader's domain model or predict real throughput.
