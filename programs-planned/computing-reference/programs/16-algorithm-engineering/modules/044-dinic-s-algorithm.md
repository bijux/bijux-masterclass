---
module_id: ALGE-044
program: Algorithm Engineering
level: 1
module_number: 44
title: Dinic's Algorithm
status: complete
last_verified: 2026-09-05
---

# Dinic's Algorithm

## One-Page Review

### Governing question

How can one breadth-first residual layering support many coordinated augmentations before it is rebuilt, and why does this produce a general $O(V^2E)$ maximum-flow algorithm?

### Essential definitions

- A **level** $\ell(v)$ is the shortest residual edge count from $s$ to $v$.
- The **level graph** contains positive residual directions $(u,v)$ satisfying $\ell(v)=\ell(u)+1$.
- An edge satisfying that equality is **admissible** for the current phase.
- A **blocking flow** in the level graph leaves no admissible $s$-$t$ path; every such path contains a saturated direction.
- A **phase** consists of one BFS level construction followed by one blocking-flow computation.
- A **current-arc pointer** remembers the first unexhausted outgoing adjacency position for each vertex during a phase.
- A **dead end** is a level-graph vertex from which no positive admissible path reaches $t$ under current residual state.

### Central model, mechanism, or theorem

Dinic repeats two operations: BFS builds the current residual level graph; then depth-first admissible pushes compute a blocking flow in that graph. After the blocking flow, the old shortest $s$-$t$ distance cannot remain: every path at that length was blocked, and newly created reverse residuals go from a higher level to a lower one. The next reachable sink level is therefore strictly larger. There are fewer than $V$ successful phases.

With adjacency lists and current-arc optimization, a standard general blocking-flow implementation costs $O(VE)$ per phase, so the total bound is $O(V^2E)$. Correctness still comes from feasible residual augmentation and termination with no residual $s$-$t$ path.

### Critical invariants

- BFS and blocking flow use one pinned network revision and committed starting flow.
- Admissible directions have positive residual and increase level by exactly one.
- Each push is no larger than caller demand and residual capacity.
- Paired residual updates are exact and atomic at the committed-flow boundary.
- Current-arc pointers move only forward within one level-graph phase.
- A reported blocking flow leaves no admissible $s$-$t$ path.
- The sink level strictly increases between successful phases.
- Original-edge capacity and internal conservation hold after every committed phase.
- Final optimality is claimed only after a fresh BFS cannot reach $t$ and a cut certificate validates.

### Common failures

Failures include confusing a blocking flow with a maximum flow; retaining residual edges that do not advance one level; rebuilding levels after every small push and losing the batching benefit; carrying current-arc pointers across phases; advancing a pointer before an edge is actually exhausted; omitting reverse residual updates; using recursive DFS without depth governance; treating a single failed DFS call as proof the phase is blocked; mutating capacities during a phase; and reporting cancellation as optimal completion.

### Compact example

If BFS gives levels $s:0$, $a,b:1$, $t:2$, the first level graph may contain `s-a-t` and `s-b-t`. A blocking flow can saturate one edge on each two-edge path before another BFS. It need not saturate every level edge, and it need not be maximum in the entire residual graph. Its job is to destroy every path at the current shortest length.

### Connections

[ALGE-041](./041-flow-networks-and-residual-graphs.md) defines paired residuals, [ALGE-042](./042-ford-fulkerson-method.md) defines augmentation, and [ALGE-043](./043-edmonds-karp-algorithm.md) proves shortest residual distances do not decrease. Dinic batches the shortest-path work. [ALGE-045](../ROADMAP.md#block-05--flows-matching-and-combinatorial-optimization) develops the flow-cut theorem, and [ALGE-046](../ROADMAP.md#block-05--flows-matching-and-combinatorial-optimization) applies flows to matching.

## Governing Question

Given a finite directed capacity network, how does Dinic's phase structure compute and verify blocking flows, force progress in shortest residual distance, achieve $O(V^2E)$ general time, and remain safe under realistic numeric, memory, cancellation, and snapshot constraints?

The governing distinction is between one augmentation, one blocking flow, and the complete maximum flow. These are three different scopes. A blocking-flow phase coordinates many residual augmentations under one valid level structure; only repeated phases ending in residual exhaustion establish maximum flow.

## Why This Matters

Edmonds-Karp performs one shortest augmentation and then discards its BFS result. Dinic observes that many paths follow the same level structure. Computing a blocking flow amortizes the BFS and exposes reusable state: levels, admissible edges, and current-arc pointers. The design pattern appears beyond maximum flow whenever expensive global structure can guide a bounded batch of local operations.

The extra state creates extra proof and engineering obligations. Stale levels are allowed within a phase only because pushes use the remaining admissible subgraph and reverse edges cannot create a new forward level edge. Pointers are valid only for one phase. A recursive teaching implementation can overflow a production call stack. A checkpoint taken in the middle of blocking-flow mutation requires more state than a checkpoint between validated phases.

## Prerequisites and Retrieval

Retrieve BFS levels, DFS path search, residual capacities, reverse pairing, feasible-flow conservation, bottlenecks, asymptotic analysis, amortization, recursion limits, transactions, and snapshots. Review [ALGE-031](./031-breadth-first-search.md), [ALGE-032](./032-depth-first-search.md), and [ALGE-041](./041-flow-networks-and-residual-graphs.md) through [ALGE-043](./043-edmonds-karp-algorithm.md).

## Learning Objectives

After completing this module, you should be able to:

1. construct a residual level graph with BFS;
2. distinguish admissible edges, augmenting paths, blocking flows, and maximum flows;
3. implement blocking-flow pushes with paired residual updates;
4. explain the current-arc optimization and its lifecycle;
5. prove that a completed blocking flow eliminates the current sink distance;
6. prove fewer than $V$ successful phases occur;
7. derive the standard general $O(V^2E)$ time and $O(V+E)$ space bounds;
8. validate phase traces, feasibility, blocking, and final cut evidence;
9. handle parallel edges, deep paths, arithmetic, cancellation, and stale snapshots;
10. compare Dinic with Edmonds-Karp and push-relabel without overclaiming practice.

## Core Exposition

### Build the residual level graph

Run BFS from $s$ over exactly the positive residual directions. Set $\ell(s)=0$; each first discovery assigns its predecessor-independent shortest level. The level graph is

$$
L_f=(V,\{(u,v)\in E_f:\ell(v)=\ell(u)+1\}).
$$

It is acyclic: every admissible edge strictly raises an integer level. Every $s$-$t$ path in $L_f$ has exactly $\ell(t)$ edges and is a shortest path in the current residual graph. Edges within one level, edges going backward, and edges that skip a level are excluded even if their residual capacity is positive.

If BFS cannot reach $t$, the algorithm has exhausted residual augmenting paths. Validate the reached-set cut and return maximum. If $t$ is reachable, the phase computes a blocking flow using only admissible directions.

### Define blocking precisely

A flow added through the level graph is blocking when no positive-residual $s$-$t$ path remains in that level graph. Equivalently, every original level-graph $s$-$t$ path has at least one direction saturated by the phase's cumulative pushes. Blocking does not mean every level edge is saturated. It also does not mean the cumulative phase flow is a maximum flow of the full residual network.

A common implementation repeatedly asks for admissible flow from $s$ to $t$. A depth-first routine receives an upper bound, recursively sends through admissible children, and returns the amount delivered. Each successful push subtracts from a residual slot and adds to its paired reverse. Repeating until the source can send nothing yields a blocking flow if the routine and pointer rules are correct.

### Use current-arc pointers safely

Without memory, repeated DFS attempts can rescan exhausted outgoing edges. Maintain `next[v]`, the first adjacency index not yet proved unusable for further pushes in this phase. If an edge is nonadmissible, zero, or its head cannot accept flow, advance the pointer. If it sends some flow but retains residual capacity, do not automatically discard it; later caller demand may use it again.

Pointers are phase-local. A new BFS changes levels, and prior inadmissible edges may become admissible. Reset all pointers after every level rebuild. Stable edge identities and reciprocal reverse indices are necessary when parallel and anti-parallel edges coexist.

### Prove phase progress

Let the sink have level $k$ at the start of a phase. Every residual $s$-$t$ path of length $k$ follows increasing levels and belongs to the level graph. A blocking flow destroys all such paths.

Augmentation can create reverse residual directions only opposite used admissible edges. Those new reverses go from level $i+1$ to level $i$, so they cannot form a new length-$k$ path that moves through levels $0,1,\ldots,k$. Existing non-level residual edges also cannot form an $s$-$t$ path of length $k$; otherwise BFS would have assigned the same consecutive levels along it. Therefore, after a completed blocking flow, either $t$ is unreachable or its next BFS level exceeds $k$.

Any simple residual path has at most $V-1$ edges. The sink level starts positive and strictly rises after each successful phase, so fewer than $V$ successful phases occur.

### Derive general complexity

One BFS costs $O(V+E)$ with paired residual adjacency. A conservative standard blocking-flow analysis with DFS and current arcs costs $O(VE)$: edge scans advance monotonically, while successful path pushes have length at most $V-1$ and can be charged to saturated or exhausted admissible work. Across fewer than $V$ phases, the general bound is

$$
O(V)\cdot O(VE)=O(V^2E).
$$

Space is $O(V+E)$ for paired residual adjacency, levels, current pointers, and an explicit or implicit DFS path. Special graph classes admit stronger bounds, but those require additional hypotheses and proofs; the general bound is the contract here. Arithmetic-operation cost must still account for capacity representation when operands are not fixed-width.

### Execute a two-phase example

The following exact-integer implementation uses explicit paired residual slots. It reports how much flow each BFS phase sends, reconstructs original-edge flows, and validates the final result.

<!-- bijux-verify: {"id":"dinic-blocking-flow","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"phases=((2, 5), (3, 1))\nflows=(('ab', 1), ('at', 2), ('bt', 4), ('sa', 3), ('sb', 3))\nvalue=6\nvalid=True\nresidual_path=False\n","stderr":""}} -->
```python
from collections import deque


vertices = ("s", "a", "b", "t")
adjacency = {v: [] for v in vertices}
original = {}


def add_edge(edge_id, tail, head, capacity):
    forward_index = len(adjacency[tail])
    reverse_index = len(adjacency[head])
    adjacency[tail].append([head, reverse_index, capacity])
    adjacency[head].append([tail, forward_index, 0])
    original[edge_id] = (tail, forward_index, capacity, head)


for specification in (
    ("sa", "s", "a", 4), ("sb", "s", "b", 3),
    ("ab", "a", "b", 2), ("at", "a", "t", 2),
    ("bt", "b", "t", 4),
):
    add_edge(*specification)


def levels():
    level = {"s": 0}
    queue = deque(["s"])
    while queue:
        tail = queue.popleft()
        for head, _, residual in adjacency[tail]:
            if residual > 0 and head not in level:
                level[head] = level[tail] + 1
                queue.append(head)
    return level


def send(vertex, limit, level, current):
    if vertex == "t":
        return limit
    while current[vertex] < len(adjacency[vertex]):
        index = current[vertex]
        head, reverse, residual = adjacency[vertex][index]
        if residual > 0 and level.get(head) == level[vertex] + 1:
            delivered = send(head, min(limit, residual), level, current)
            if delivered > 0:
                adjacency[vertex][index][2] -= delivered
                adjacency[head][reverse][2] += delivered
                return delivered
        current[vertex] += 1
    return 0


def edge_flows():
    return {
        edge_id: capacity - adjacency[tail][index][2]
        for edge_id, (tail, index, capacity, _) in original.items()
    }


def validate(flow):
    balance = {v: 0 for v in vertices}
    for edge_id, (tail, _, capacity, head) in original.items():
        amount = flow[edge_id]
        if not 0 <= amount <= capacity:
            return False
        balance[tail] -= amount
        balance[head] += amount
    return balance["a"] == balance["b"] == 0 and -balance["s"] == balance["t"]


phases = []
while "t" in (level := levels()):
    current = {v: 0 for v in vertices}
    phase_flow = 0
    while (delivered := send("s", 10**9, level, current)) > 0:
        phase_flow += delivered
    phases.append((level["t"], phase_flow))

flow = edge_flows()
print(f"phases={tuple(phases)}")
print(f"flows={tuple(sorted(flow.items()))}")
print(f"value={flow['sa'] + flow['sb']}")
print(f"valid={validate(flow)}")
print(f"residual_path={'t' in levels()}")
```

The first phase sends five units across two length-two branches. The second sends one unit along `s-a-b-t`. Sink levels rise from two to three; the next BFS cannot reach $t$. The observed flow value six equals the cut capacity of `at` plus `bt`.

### Validate a phase and final result

Before a phase, independently check residual pairing and recompute BFS levels. During it, assert that every pushed direction is positive and moves from level $i$ to $i+1$, every push is within both caller limit and residual, and every pair update conserves its residual sum. At phase commit, reconstruct the original flow and validate capacity, conservation, net value, and snapshot digest.

To validate blocking, search the remaining admissible graph. The sink must be unreachable. On the next phase, check either termination or strict sink-level increase. For bounded integer graphs, compare with exhaustive flows or an independently implemented solver. Metamorphic tests include vertex renaming, canonical edge reorderings, capacity scaling, disconnected structure, and split parallel capacity with normalized output.

Final verification must not trust phase state. Re-run residual reachability, derive reached set $S$, check all outward crossing originals saturated and inward crossing originals at zero, and verify flow value equals cut capacity.

### Govern stack, memory, and arithmetic

The recursive snippet is intentionally compact. A production graph can have an admissible path with $V-1$ edges and overflow the language call stack. Use an explicit path stack or a proven safe recursion bound. Record memory for two residual slots per original edge, adjacency overhead, levels, current pointers, and work traces.

Reject negative capacity, NaN, ambiguous IDs, unknown endpoints, and totals that overflow chosen arithmetic. Exact integers preserve feasibility cleanly, but large integers have nonconstant cost. Floating implementations need declared comparison and conservation tolerances and cannot silently borrow exact proofs.

### Preserve lifecycle boundaries

Pin capacities and graph identity for the whole solve or define a restart protocol. Changing capacity mid-phase invalidates levels, blocking status, and pointers. Serialize mutations or keep candidate residual state private until validation.

The safest checkpoint is a validated phase boundary containing graph digest, original flow or complete residual pairs, algorithm version, completed phase count, last sink level, and evidence digest. Mid-phase checkpoints must additionally preserve levels, current pointers, DFS stack, pending updates, and transaction state exactly.

Cancellation returns the last committed feasible state as `feasible_incomplete`. A work or memory limit is not residual exhaustion. Publish `optimal` only after a fresh unreachable-sink search and cut equality check.

### Position the algorithm in current practice

Current Boost.Graph's maximum-flow overview lists Edmonds-Karp, push-relabel, and Boykov-Kolmogorov, rather than a named Dinic interface. Current Google OR-Tools documentation exposes a `SimpleMaxFlow` contract without promising Dinic's phase trace. These current API observations reinforce a key boundary: choosing a library maximum-flow solver is not the same as choosing or exposing Dinic's internal policy.

Use Dinic when its structure, performance on the relevant graph class, or inspectable level/blocking trace fits the requirement. Benchmark representative graphs and validate certificates. Do not infer practical superiority from one asymptotic comparison.

## Definitions and Notation

- $G_f$: residual graph of committed feasible flow $f$.
- $\ell(v)$: BFS shortest residual distance from $s$.
- $L_f$: positive residual directions that advance exactly one level.
- **admissible edge**: an edge of $L_f$.
- **blocking flow**: phase flow leaving no admissible $s$-$t$ path.
- **phase**: one level construction and one blocking-flow computation.
- `next[v]`: phase-local current-arc pointer.
- $V,E$: counts of vertices and original logical edges.
- **phase boundary**: validated committed state after a blocking flow.

## Mechanisms, Invariants, or Proof Structure

BFS creates an acyclic level graph containing every shortest residual $s$-$t$ path. Admissible DFS pushes preserve feasibility through paired residual updates. Current pointers avoid restarting scans of exhausted choices. When no admissible source-to-sink push remains, the flow blocks every path at the old shortest distance. Newly created reverses move backward in old levels, so the next sink distance strictly increases. Fewer than $V$ phases, each with $O(VE)$ conservative blocking-flow work, give $O(V^2E)$. Final residual exhaustion plus a flow-cut certificate establishes optimality.

## Alternatives and Trade-Offs

- **Edmonds-Karp:** simpler one-path phases and $O(VE^2)$; repeats BFS more often.
- **Dinic:** batches paths and has general $O(V^2E)$; needs levels, current pointers, and blocking-flow correctness.
- **Push-relabel:** uses local excess and heights instead of paths; often competitive but has different state and proofs.
- **Recursive DFS:** concise; unsafe on unbounded depth.
- **Explicit DFS stack:** controlled memory and resumability; more complex state transitions.
- **Phase-boundary checkpoint:** compact and easy to validate; may redo a long interrupted phase.
- **Mid-phase checkpoint:** less redo; must persist substantially more mutable state.
- **Full phase trace:** supports diagnosis and teaching; increases storage and exposure.
- **Certificate-only output:** compact optimality evidence; does not reproduce internal choices.

## Failure Modes and Misconceptions

- A level graph contains only positive residual edges increasing level by one.
- Blocking the level graph does not by itself finish maximum flow.
- A blocking flow need not saturate every admissible edge.
- Current-arc state must reset after each BFS.
- A partially delivered edge with residual capacity may remain usable.
- One failed path attempt is not proof that the phase is blocked.
- Reverse residual updates are necessary even though reverse edges are inadmissible in the old levels.
- Recursion depth is a production resource limit.
- $O(V^2E)$ does not include unbounded numeric-operation cost automatically.
- A phase computed across changing capacity snapshots has no valid proof.
- Cancellation, resource exhaustion, and optimal completion are distinct statuses.

## Worked Examples

### Example 1

**Situation.** Levels are $s:0$, $a,b:1$, $t:2$. Residual edge $a\to b$ stays within level one, so it is excluded although positive. **Conclusion.** Positivity alone does not make an edge admissible.

### Example 2

**Situation.** The level graph has paths `s-a-t` and `s-b-t`. Saturating `a-t` and `s-b` blocks both paths while another unrelated level edge remains positive. **Conclusion.** Blocking concerns all source-sink paths, not all edges.

### Example 3

**Situation.** A push uses admissible $u\to v$ from level three to four. Its new reverse $v\to u$ goes from four to three. **Conclusion.** The reverse cannot create a new forward path in the current level graph.

### Example 4

**Situation.** Sink levels across successful phases are $3,4,6$. Skipping level five is allowed; decreasing or repeating is not. **Conclusion.** Strict phase progress, not unit increase, bounds phase count.

### Example 5

**Situation.** DFS sends two units through an edge with residual five, limited by a downstream bottleneck. Three remain. **Conclusion.** A current pointer must not discard a still-admissible partially used edge automatically.

### Example 6

**Situation.** One DFS branch reaches a dead end. The source has another admissible branch reaching $t$. **Conclusion.** A failed call below one branch does not establish blocking; current-arc traversal must exhaust all admissible choices.

### Example 7

**Situation.** $V=1{,}000$ and $E=20{,}000$. The general expression $V^2E$ is $2\times10^{10}$ before constants. **Conclusion.** A polynomial upper bound still demands benchmarking and work limits.

### Example 8

**Situation.** A chain level graph has 100,000 vertices. Recursive DFS may exceed the runtime stack even though graph memory fits. **Conclusion.** Algorithmic space and language call-stack limits must both be governed.

### Example 9

**Situation.** Capacity revision changes after BFS but before blocking flow. An edge classified admissible is now over capacity. **Conclusion.** A phase must use one immutable revision or restart.

### Example 10

**Situation.** The last BFS cannot reach $t$; reached-set cut capacity and feasible-flow value are both 17. **Conclusion.** Residual exhaustion plus independently recomputed equality certifies optimality.

## Cross-Program Connections

- Data Structures Engineering owns paired adjacency slots, queues, explicit stacks, current pointers, and generation maps.
- Theory of Computation and Algorithm Engineering connect phase measures, amortized charging, and proof-scoped complexity.
- Operating Systems owns stack limits, cancellation, memory budgets, and atomic state transitions.
- Database Engineering owns snapshot identity, phase transactions, checkpoint recovery, and evidence provenance.
- Software Testing and Quality Engineering owns phase-property, metamorphic, differential, and certificate checks.
- Security and Platform Engineering own hostile input admission, tenant quotas, observability, trace retention, and status integrity.

## References

1. E. A. Dinic, “Algorithm for Solution of a Problem of Maximum Flow in a Network with Power Estimation,” *Soviet Mathematics Doklady* 11(5), 1277–1280, 1970. [Author-hosted primary-paper scan](https://www.cs.bgu.ac.il/~dinitz/D70.pdf), checked 2026-09-05.
2. Jack Edmonds and Richard M. Karp, “Theoretical Improvements in Algorithmic Efficiency for Network Flow Problems,” *Journal of the ACM* 19(2), 248–264, 1972, DOI [10.1145/321694.321699](https://doi.org/10.1145/321694.321699). Primary paper checked 2026-09-05.
3. Ravindra K. Ahuja, Thomas L. Magnanti, and James B. Orlin, *Network Flows: Theory, Algorithms, and Applications*, Prentice Hall, 1993. [MIT-hosted record](https://dspace.mit.edu/handle/1721.1/49424), checked 2026-09-05.
4. Thomas H. Cormen et al., *Introduction to Algorithms*, 4th ed., MIT Press, 2022, Chapter 24. [Official publisher record](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/), checked 2026-09-05.
5. Jeff Erickson, *Algorithms*, 1st ed., 2019, maximum-flow chapter. [Author-hosted book](https://jeffe.cs.illinois.edu/teaching/algorithms/), checked 2026-09-05.
6. Boost C++ Libraries, “Network Flow,” current Boost.Graph documentation. [Official documentation](https://www.boost.org/doc/libs/latest/libs/graph/doc/html/graph/algorithms/network_flow/network_flow_overview.html), checked 2026-09-05.
7. Google, “Maximum Flows,” OR-Tools documentation, updated 2026-03-18. [Official documentation](https://developers.google.com/optimization/flow/maxflow), checked 2026-09-05.

## Exercises

### Exercise 1

Given residual edges $s\to a$, $s\to b$, $a\to b$, $a\to t$, and $b\to t$, all positive, compute BFS levels and identify admissible edges. Explain why an edge can be residual but excluded from the level graph.

### Exercise 2

Prove that after a blocking flow at sink level $k$, the next BFS either cannot reach $t$ or assigns it a level greater than $k$. Derive the phase and general running-time bounds.

### Exercise 3

Diagnose a Dinic implementation that retains level arrays and current pointers across phases, advances a pointer after every partial push, updates only forward residuals, recurses on unbounded input, and checkpoints halfway through a nontransactional update.

### Exercise 4

Compare Edmonds-Karp, Dinic, and push-relabel for a teaching trace, a sparse batch workload, a dense adversarial API, and a resumable service. State what benchmarking and verification each still needs.

### Exercise 5

Design a phase-level audit record and independent verifier. Include snapshot, BFS, admissibility, pushes, blocking status, feasibility, phase progress, final cut, arithmetic, lifecycle status, and limitations.

## Answers to the Exercises

### Answer 1

BFS gives $\ell(s)=0$, $\ell(a)=\ell(b)=1$, and $\ell(t)=2$. Admissible edges are $s\to a$, $s\to b$, $a\to t$, and $b\to t$. Edge $a\to b$ is positive residual but stays from level one to level one, so it cannot belong to a shortest two-edge path and is excluded.

Residual membership asks whether an adjustment is possible. Level-graph membership additionally asks whether it advances exactly one current BFS level. The latter is a phase policy, not a statement that the excluded residual edge is invalid.

### Answer 2

Every length-$k$ residual $s$-$t$ path at phase start advances through BFS levels $0,1,\ldots,k$ and is entirely in the level graph. Blocking leaves no such path. A phase creates residual directions only as reverses of used admissible edges, so new directions go from level $i+1$ to $i$; they cannot reconstruct a forward length-$k$ path. No old non-level edge can complete such a path either, or BFS would have assigned consecutive shortest levels along it.

Thus the next sink level is greater than $k$ or infinite. A reachable simple sink level is at most $V-1$, giving fewer than $V$ successful phases. BFS is $O(V+E)$ and a standard current-arc blocking flow is conservatively $O(VE)$, so the general total is $O(V^2E)$ with $O(V+E)$ space.

### Answer 3

Recompute levels and reset every current pointer at phase start; admissibility changes when the residual graph changes. Advance a pointer only when its edge cannot send more in the current phase, not merely after a partial push with remaining residual. Update both residual slots through validated reciprocal indices so cancellation remains possible.

Replace unbounded recursion with an explicit stack or enforce a proved depth limit. Apply paired updates within a candidate or rollback transaction. The safest checkpoint is after reconstructing and validating a committed phase flow. A mid-phase checkpoint must persist exact levels, pointers, explicit DFS stack, residual pairs, pending mutation state, graph digest, and recovery protocol; otherwise discard it and resume from the last phase boundary.

### Answer 4

Edmonds-Karp is the clearest single-shortest-path trace and has $O(VE^2)$ general time. Dinic adds level graphs, blocking flows, and pointers but improves the general bound to $O(V^2E)$. Push-relabel replaces path phases with local excess and height operations; it may be a stronger implementation choice, but is less directly comparable as a teaching path trace.

For teaching, prefer explainability and small verified examples. For sparse batch graphs, benchmark Dinic and a maintained push-relabel implementation on representative size and capacity distributions. For a dense hostile API, use strict admission limits and a maintained solver with suitable worst-case and memory behavior. For resumability, compare phase-boundary Dinic checkpoints with the chosen solver's supported state. Every choice still needs snapshot validation, exact edge flows, feasibility checks, a final cut certificate, resource statuses, and versioned benchmark evidence.

### Answer 5

Record graph and capacity digest, algorithm version, phase number, starting flow digest/value, BFS level map digest, sink level, admissible-edge predicate version, current-pointer initialization, and numeric domain. For each aggregate or detailed push record residual edge-directions, bounds, delivered amount, reciprocal updates, critical edges, and transaction outcome. At phase end record resulting flow digest/value, feasibility evidence, a search showing no admissible $s$-$t$ path, and the next level or termination.

The independent verifier reconstructs original flows and residual pairs; checks capacities, conservation, terminal values, levels, admissibility, signed pushes, and blocking; and checks strict sink-level progress. At final exhaustion it recomputes residual reachability, cut crossing edges, saturation, zero inward flow, and flow-cut equality. Record toolchain, snapshot, status, cancellation/resource facts, and limitations. This verifies the recorded computation and optimum for one model snapshot, not the model's domain fitness or deployed performance.
