---
module_id: ALGE-041
program: Algorithm Engineering
level: 1
module_number: 41
title: Flow Networks and Residual Graphs
status: complete
last_verified: 2026-09-05
---

# Flow Networks and Residual Graphs

## One-Page Review

### Governing question

How should a flow network represent capacity, conservation, value, and reversible residual adjustments so later maximum-flow algorithms operate on a correct, auditable state rather than on ambiguous edge mutations?

### Essential definitions

- A **flow network** is a directed graph with nonnegative arc capacities, source $s$, and distinct sink $t$.
- A **flow** assigns an amount $f(e)$ to every logical arc.
- **Capacity feasibility** requires $0\le f(e)\le c(e)$.
- **Flow conservation** requires inflow equal outflow at every vertex except $s$ and $t$.
- The **flow value** $|f|$ is net outflow from $s$, equivalently net inflow to $t$ for a feasible flow.
- A forward residual arc has capacity $c(e)-f(e)$ and can increase $f(e)$.
- A reverse residual arc has capacity $f(e)$ and can cancel previously assigned flow.
- An **augmenting path** is an $s$-to-$t$ path of positive residual arcs.
- Its **bottleneck** is the minimum residual capacity on the path.
- A **cut** $(S,V\setminus S)$ with $s\in S,t\notin S$ has capacity equal to capacities of original arcs leaving $S$.

### Central model, mechanism, or theorem

For each original edge identity $e=(u,v)$, maintain two residual directions:

$$
r_e^+=c(e)-f(e),\qquad r_e^-=f(e).
$$

Sending $\Delta$ through the forward residual increases $f(e)$; sending it through the reverse residual decreases $f(e)$. If $0<\Delta\le r$, both preserve the capacity interval. Along an internal vertex of a residual path, one residual adjustment enters and one leaves, so conservation is preserved. An $s$-$t$ residual augmentation increases flow value by $\Delta$.

Residual edges are algorithmic state, not new domain capacity. Reverse capacity exists even when the original graph has no reverse arc. If original anti-parallel arcs exist, each retains its own forward/reverse residual pair and stable identity.

### Critical invariants

- Source and sink are distinct declared vertices; the complete vertex and logical-edge universes are fixed.
- Every capacity and flow uses one compatible exact or governed numeric domain and unit.
- Every logical edge has stable identity, endpoints, capacity, flow, and paired residual directions.
- $0\le f(e)\le c(e)$ for every original edge.
- Inflow equals outflow at every nonterminal vertex.
- Net source outflow equals net sink inflow.
- Forward plus reverse residual capacity equals original capacity: $r_e^++r_e^-=c(e)$.
- A residual direction is traversable exactly when its residual capacity is strictly positive.
- Augmentation uses a connected directed residual path and one bottleneck no larger than every path residual.
- Updating all paired residual/flow state is atomic or safely rollbackable.
- Validation, search, augmentation, and publication share one network snapshot.

### Common failures

Frequent failures include treating undirected links as directed capacities without policy; allowing negative capacity; omitting parallel-edge identity; merging residual reverses with independent anti-parallel edges; computing value as gross source outflow when flow can enter the source; checking capacity but not conservation; using a path containing a zero-residual arc; choosing more than the bottleneck; updating only forward residual state; overflowing sums; accepting NaN; mixing rate and quantity units; mutating capacities during search; and exposing an intermediate update after only part of a path was changed.

### Compact example

Original arc $a\to b$ has capacity seven and current flow five. Its forward residual capacity is two and its reverse residual capacity is five. Sending two forward saturates the edge at seven; sending three in the reverse residual direction instead reduces its original flow to two. The reverse operation cancels a prior choice—it does not assert three units of original $b\to a$ capacity.

### Connections

[ALGE-031](./031-breadth-first-search.md) supplies residual reachability, [ALGE-040](./040-engineering-graph-traversal-for-sparse-and-dense-inputs.md) supplies representation and paired-edge engineering, and [ALGE-045](../ROADMAP.md#block-05--flows-matching-and-combinatorial-optimization) will connect absence of residual paths to cuts. [ALGE-042](../ROADMAP.md#block-05--flows-matching-and-combinatorial-optimization) next turns residual augmentation into the Ford-Fulkerson method.

## Governing Question

Given directed capacity arcs and a candidate flow, what representation and invariants make feasibility, residual reachability, augmentation, reversal, validation, numeric behavior, and lifecycle state precise enough for subsequent maximum-flow algorithms and production use?

The residual graph is the essential mechanism. A forward residual arc represents unused capacity; a reverse residual arc represents permission to undo existing flow. Without reverse residuals, a locally plausible path choice can permanently block a better solution. Without stable edge identity, anti-parallel and parallel arcs become ambiguous.

## Why This Matters

Flow networks model throughput, assignment, matching, circulation, segmentation, routing, scheduling, and resource allocation. Later algorithms differ in how they select and organize residual work, but they share the same feasibility and paired-update foundation.

The abstraction is narrower than physical flow. It assumes one additive conserved scalar over a snapshot. Losses, gains, storage, time, multiple commodities, lower bounds, costs, and nonlinear capacities require transformations or different models. A solver can be perfectly correct for its network while the network is inadequate for the domain.

Production correctness depends on details often absent from textbook diagrams: exact edge IDs, parallel arcs, incoming source edges, outgoing sink edges, numeric overflow, partial mutation, checkpoint consistency, and output certificates. This chapter establishes those foundations before choosing an augmenting-path policy.

## Prerequisites and Retrieval

Retrieve directed graphs, paths, cuts, BFS/DFS reachability, adjacency with reverse-edge pairing, exact arithmetic and infinity, sums and conservation equations, loop invariants, snapshots, transactions, and atomic publication. Review [ALGE-031](./031-breadth-first-search.md) and [ALGE-040](./040-engineering-graph-traversal-for-sparse-and-dense-inputs.md).

## Learning Objectives

After completing this module, you should be able to:

1. specify a directed capacitated multigraph and feasible source-sink flow;
2. derive equality of source and sink flow values from conservation;
3. construct forward and reverse residual arcs per original edge identity;
4. prove residual augmentation preserves capacity and conservation;
5. implement and validate atomic augmentation over a residual path;
6. distinguish residual reverses from original anti-parallel arcs;
7. compute cuts and explain their upper-bound role without preempting the full theorem;
8. handle parallel edges, self-loops, terminal incident edges, numeric bounds, and units;
9. govern snapshots, cancellation, checkpoints, rollback, and publication;
10. recognize lower-bound, circulation, min-cost, multi-commodity, dynamic, and lossy-flow boundaries.

## Core Exposition

### Specify the network

Let $G=(V,E)$ be a finite directed multigraph. Each logical edge $e$ has stable identity, tail $u$, head $v$, and capacity $c(e)\ge0$. Source $s$ and sink $t$ are distinct vertices. Parallel and anti-parallel edges remain distinct unless a proved normalization preserves every required output.

A flow $f:E\to\mathbb R$ or an exact discrete domain satisfies capacity feasibility and, for every $v\in V\setminus\{s,t\}$,

$$
\sum_{e:\operatorname{head}(e)=v}f(e)
=\sum_{e:\operatorname{tail}(e)=v}f(e).
$$

Define net outflow at vertex $v$ as outgoing minus incoming flow. Then $|f|$ is net outflow at $s$. Summing net outflow over all vertices cancels every edge once positive and once negative, yielding zero. Internal terms vanish by conservation, so source net outflow equals sink net inflow.

This net definition remains correct when original arcs enter $s$ or leave $t$. Gross outgoing flow alone does not.

### Derive the residual representation

For original edge $e=(u,v)$, unused capacity permits an adjustment from $u$ to $v$ of at most $c(e)-f(e)$. Existing flow permits cancellation from $v$ to $u$ of at most $f(e)$. Represent both with a pointer to $e$ and a direction bit rather than inventing domain edges.

If an original $v\to u$ edge also exists, it contributes its own forward residual direction in addition to the reverse residual of $e$. Aggregating them may preserve only total reachability/capacity; it loses which original flows an update should change. Stable paired identities avoid this bug.

Zero residual capacity means absence from traversal even if a stored slot remains. A self-loop has paired residual state but contributes equally to inflow and outflow; it cannot advance an $s$-$t$ simple residual path and should follow a declared retention policy.

### Prove augmentation preservation

Let residual path $P$ run from $s$ to $t$, and let

$$
\Delta=\min_{a\in P}c_f(a)>0.
$$

For each forward residual step, set $f(e)\leftarrow f(e)+\Delta$; for each reverse step, subtract $\Delta$. The bottleneck ensures forward flow never exceeds capacity and reverse flow never becomes negative.

At an internal path vertex, exactly one path adjustment enters and one leaves in residual orientation. Both add the same $\Delta$ to the conservation equation, even when either corresponds to cancellation of an original edge. Thus internal net flow stays zero. Source net outflow and sink net inflow each increase by $\Delta$.

The proof assumes a directed connected residual path with no inconsistent repeated edge-direction update. General residual walks can be simplified or accumulated carefully; implementations normally use predecessor paths from a search.

### Execute and validate one augmentation

The implementation below holds original flows separately, computes residual directions on demand, checks a declared path, applies updates to a copy, and validates the candidate before commit.

<!-- bijux-verify: {"id":"residual-augmentation","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"before_value=5 before_valid=True\naugmenting_path=('sa:f', 'ab:f', 'bt:f') bottleneck=1\nafter_flows=(('ab', 2), ('at', 2), ('bt', 4), ('sa', 4), ('sb', 2))\nafter_value=6 after_valid=True\nresidual_path_after=False\n","stderr":""}} -->
```python
from collections import deque


edges = {
    "sa": ("s", "a", 4), "sb": ("s", "b", 3),
    "ab": ("a", "b", 2), "at": ("a", "t", 2),
    "bt": ("b", "t", 4),
}
vertices = {"s", "a", "b", "t"}


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


def value(flow):
    outgoing = sum(flow[e] for e, (u, _, _) in edges.items() if u == "s")
    incoming = sum(flow[e] for e, (_, v, _) in edges.items() if v == "s")
    return outgoing - incoming


def residual_steps(flow):
    steps = []
    for edge_id, (tail, head, capacity) in sorted(edges.items()):
        if capacity - flow[edge_id] > 0:
            steps.append((tail, head, edge_id, "f", capacity - flow[edge_id]))
        if flow[edge_id] > 0:
            steps.append((head, tail, edge_id, "r", flow[edge_id]))
    return steps


def augment(flow, path):
    steps = {(edge_id, direction): (tail, head, residual)
             for tail, head, edge_id, direction, residual in residual_steps(flow)}
    cursor = "s"
    residuals = []
    for edge_id, direction in path:
        if (edge_id, direction) not in steps:
            raise ValueError("nonpositive or unknown residual step")
        tail, head, residual = steps[edge_id, direction]
        if tail != cursor:
            raise ValueError("disconnected residual path")
        cursor = head
        residuals.append(residual)
    if cursor != "t" or not residuals:
        raise ValueError("path must connect source to sink")
    delta = min(residuals)
    candidate = dict(flow)
    for edge_id, direction in path:
        candidate[edge_id] += delta if direction == "f" else -delta
    if not validate(candidate):
        raise AssertionError("augmentation violated feasibility")
    return candidate, delta


def has_residual_path(flow):
    adjacency = {vertex: [] for vertex in vertices}
    for tail, head, _, _, _ in residual_steps(flow):
        adjacency[tail].append(head)
    seen, queue = {"s"}, deque(["s"])
    while queue:
        vertex = queue.popleft()
        for neighbor in adjacency[vertex]:
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)
    return "t" in seen


flow = {"sa": 3, "sb": 2, "ab": 1, "at": 2, "bt": 3}
print(f"before_value={value(flow)} before_valid={validate(flow)}")
path = (("sa", "f"), ("ab", "f"), ("bt", "f"))
updated, delta = augment(flow, path)
print(f"augmenting_path={tuple(e + ':' + d for e, d in path)} bottleneck={delta}")
print(f"after_flows={tuple(sorted(updated.items()))}")
print(f"after_value={value(updated)} after_valid={validate(updated)}")
print(f"residual_path_after={has_residual_path(updated)}")
```

The final absence of an augmenting path is observed for this network. Proving it implies maximum flow requires the cut theorem developed in ALGE-045; later algorithm chapters supply systematic path policies.

### Understand reversal through a counterexample

Suppose an early path sends flow through $a\to b$, but a later solution needs capacity leaving $a$ and entering $b$ along different routes. The residual reverse $b\to a$ allows a new augmenting path to cancel some $a\to b$ flow while simultaneously rerouting it. A representation containing only unused forward capacities can become stuck at a nonmaximum feasible flow.

Cancellation changes the original edge flow. It is not a negative physical shipment and not necessarily an original reverse edge. Audit logs should record original edge ID, residual direction, previous amount, delta, and new amount.

### Define cut capacity and the upper bound

For $S\subset V$ with $s\in S$ and $t\notin S$, let $\delta^+(S)$ be original edges leaving $S$ and $\delta^-(S)$ entering it. Summed conservation gives

$$
|f|=f(\delta^+(S))-f(\delta^-(S))
\le c(\delta^+(S)).
$$

Every cut capacity is therefore an upper bound on every feasible flow value. If residual search cannot reach $t$, the reached set suggests a cut; the equality proof and maximum theorem are reserved for ALGE-045. Keep original capacities, not residual capacities, in the cut definition.

### Validate independently

Validate vertex/source/sink membership, unique edge IDs, endpoints, capacity domain, and flow domain. Recompute every capacity inequality, every internal conservation equation, source and sink net values, and their equality. Recompute paired residual capacities and verify they are nonnegative and sum to original capacity.

For a proposed residual path, check source, sink, continuity, each original edge/direction identity, positive residual capacity, bottleneck minimum, and candidate updates. Revalidate the entire flow after applying to a copy. For bounded networks, compare with an independent linear program or enumerated integer flows; agreement is evidence within that bound.

Metamorphic checks include vertex renaming, edge-record permutation, adding zero-capacity edges, splitting a capacity into parallel edges when edge-level output is normalized, and adding disconnected components. Scaling exact capacities and a feasible flow by a positive integer scales values and residuals.

### Govern arithmetic and units

Capacities may be exact integers, rationals, decimals, or carefully governed floating values. Reject negative values and NaN. Check additions for overflow in conservation, value, cut, and total-capacity calculations. A capacity sentinel is usually unnecessary; “unbounded” needs a proved finite replacement or a separate model.

All capacities must share a conserved unit over a common time basis. Combining requests per second with storage bytes or weekday capacity with hourly demand is invalid without transformation. Floating tolerances can accept conservation leakage or negative residuals; specify tolerances relative to model and audit cumulative error.

Integral capacities matter later: augmenting by integral bottlenecks preserves integrality. This is a theorem about exact arithmetic, not about rounded floating implementations.

### Engineer paired residual edges safely

Array-based implementations often create two stored slots together and store reciprocal indices. For original edge ID `e`, forward slot holds capacity and flow; reverse slot may have zero original capacity but shares the pair. Updating slot residuals must preserve reverse pairing even with parallel and anti-parallel originals.

Never infer the reverse slot solely by endpoints: several edges can share them. Validate `reverse[reverse[i]]=i`, swapped endpoints, distinct or explicitly self-loop slots, same original ID, complementary directions, and residual sum. A partial pair insertion must roll back.

Current [Boost.Graph 1.92.0 maximum-flow documentation](https://www.boost.org/doc/libs/latest/libs/graph/doc/html/graph/algorithms/network_flow/boykov_kolmogorov_max_flow.html) explicitly requires each edge to have a reverse edge and accepts capacity, residual-capacity, and reverse-edge maps. Current [Google OR-Tools maximum-flow guidance](https://developers.google.com/optimization/flow/maxflow) exposes directed arcs with capacities and reports per-arc flows. These interfaces illustrate current practice; callers must still validate their own modeling and lifecycle assumptions.

### Preserve snapshots and atomicity

Bind capacities, source/sink, edge IDs, residual pairing, current flow, search predecessors, bottleneck, validation, and output to one immutable revision. Changing capacity during search invalidates residual reachability and the bottleneck. Concurrent augmentations can oversubscribe the same residual arc unless serialized or coordinated by a proved algorithm.

A checkpoint records graph digest, current validated flow, residual representation version, algorithm/policy version, search state, predecessor edge-directions, pending delta, and transaction state. Resume only from a validated committed flow, or prove how an in-progress path update is rolled forward/back.

Cancellation yields incomplete optimization, though the last committed flow may remain feasible. Publish it only as a feasible partial result with value and snapshot, not as maximum. Atomic output includes status, original edge flows/capacities, value, conservation evidence, residual/cut evidence when applicable, and limitations.

### Respect model boundaries

Lower bounds require a circulation transformation and feasibility phase. Supplies/demands generalize conservation. Costs lead to minimum-cost flow and residual costs. Multiple commodities share capacities but break the single conserved-scalar structure. Gains/losses change conservation coefficients. Time-expanded networks discretize time with potentially huge graphs. Dynamic capacities require versioned recomputation or specialized algorithms.

Do not translate “maximum throughput” automatically. Queues, stochastic arrivals, latency, fairness, priorities, failures, indivisible tasks, and multi-period storage may make a static maximum flow only an upper bound or planning subproblem.

## Definitions and Notation

- $G=(V,E)$: finite directed multigraph.
- $s,t$: distinct source and sink.
- $c(e)$: nonnegative original capacity.
- $f(e)$: current original-edge flow.
- $|f|$: net source outflow, equal to net sink inflow for feasible flow.
- $r_e^+=c(e)-f(e)$: forward residual capacity.
- $r_e^-=f(e)$: reverse residual capacity.
- $G_f$: residual graph containing positive residual directions.
- $P$: residual source-to-sink path.
- $\Delta$: path bottleneck.
- $(S,V\setminus S)$: source-sink cut.
- $\delta^+(S)$, $\delta^-(S)$: original edges leaving/entering $S$.

## Mechanisms, Invariants, or Proof Structure

Initialization at zero flow satisfies capacity and conservation; each forward residual equals capacity and reverse residual is zero. Residual construction exposes every feasible one-edge increase or cancellation. Bottleneck augmentation preserves edge intervals and internal conservation and increases value by the bottleneck. Paired residual sums remain equal to original capacities. Cut conservation provides an upper bound. Independent validation recomputes feasibility and residual correspondence from original edge identities.

## Alternatives and Trade-Offs

- **Explicit residual slots:** fast traversal and updates; pairing invariants require care.
- **Residuals computed from original flow:** simpler source of truth; repeated calculation and adjacency construction cost more.
- **Aggregated parallel capacity:** smaller graph; loses per-edge flow/provenance unless reconstruction is defined.
- **Exact integer/rational arithmetic:** strong invariants; range or performance costs.
- **Floating arithmetic:** models measured values; tolerance and reproducibility risks.
- **Copy-validate-commit augmentation:** strong failure isolation; extra memory/write cost.
- **In-place transactional update:** efficient; needs undo logging or atomicity discipline.
- **Linear-programming representation:** general and independently checkable; may obscure graph-specific mechanisms.

## Failure Modes and Misconceptions

- Residual reverse capacity is not original reverse transport capacity.
- Feasible does not mean maximum.
- Capacity constraints alone do not establish conservation.
- Gross source output may differ from flow value when source has incoming arcs.
- A residual path must use strictly positive residual capacity in its directed orientation.
- Updating one side of a residual pair corrupts future reversals.
- Endpoint matching cannot identify a reverse when parallel edges exist.
- Zero-capacity arcs may remain stored but are absent from residual traversal.
- Cancellation preserves the last committed feasible flow; it does not certify optimality.
- A mathematically maximum static flow does not guarantee real system throughput.

## Worked Examples

### Example 1

**Situation.** Edge capacity is ten and flow six. Forward residual is four; reverse residual is six. Augmenting forward by three produces flow nine and residuals one/nine. **Conclusion.** Paired residual sum remains ten.

### Example 2

**Situation.** Internal vertex receives flows four and two and sends five and one. Inflow and outflow both equal six. Increasing one incoming and one outgoing residual step by three preserves equality at nine. **Conclusion.** Path augmentation preserves internal conservation.

### Example 3

**Situation.** Residual path capacities are $(7,2,5)$. Bottleneck is two. Sending three would violate the middle edge; sending two saturates it. **Conclusion.** The minimum residual determines the feasible uniform delta.

### Example 4

**Situation.** Original arcs $u\to v$ and $v\to u$ both exist. Flow on the first also creates a residual reverse $v\to u$. **Conclusion.** Two same-endpoint residual directions may update different original edge identities and cannot be merged blindly.

### Example 5

**Situation.** Source sends eight and receives three. Gross output is eight, but net flow value is five. Conservation implies sink net input five. **Conclusion.** Terminal incident edges require net definitions.

### Example 6

**Situation.** Cut leaving edges have capacities four and seven; an entering edge carries two. Any feasible flow has value at most eleven, while its current cut equation subtracts entering flow. **Conclusion.** Original leaving capacity supplies an upper bound.

### Example 7

**Situation.** Two parallel edges each have capacity three. A total flow four can split $(3,1)$ or $(2,2)$. **Conclusion.** Aggregation preserves total capacity but not edge-level output or provenance.

### Example 8

**Situation.** Signed 32-bit conservation sum adds two inflows of 1.5 billion. The true three billion exceeds range and can wrap. **Conclusion.** Validation arithmetic needs checked wider accumulation.

### Example 9

**Situation.** A path update commits its first two edges, then an exception occurs. Internal conservation is broken. **Conclusion.** Apply to a copy or use transactional rollback before publishing.

### Example 10

**Situation.** A data-center link has 10 Gb/s capacity, but the model mixes it with a queue capacity in gigabytes. **Conclusion.** Units and time basis must be transformed before conservation has meaning.

## Cross-Program Connections

- Data Structures Engineering owns paired adjacency slots, maps, queues, and mutation invariants.
- Database Engineering owns snapshot isolation, transactions, recovery, and durable evidence.
- Distributed Systems and Network Engineering own dynamic capacity, queues, failures, routing policy, and multi-path operation.
- Software Architecture owns domain boundaries, unit contracts, API statuses, and idempotent publication.
- Security Engineering reviews hostile capacities, overflow, edge-ID confusion, resource exhaustion, and corrupted checkpoints.
- Optimization and linear algebra connect feasible flows, incidence matrices, dual cuts, and later min-cost models.

## References

1. Lester R. Ford Jr. and Delbert R. Fulkerson, “Maximal Flow Through a Network,” *Canadian Journal of Mathematics* 8, 399–404, 1956, DOI [10.4153/CJM-1956-045-5](https://doi.org/10.4153/CJM-1956-045-5). Primary source checked 2026-09-05.
2. Lester R. Ford Jr. and Delbert R. Fulkerson, *Flows in Networks*, Princeton University Press, 1962; 2025 digital edition. [Official publisher record](https://doi.org/10.1515/9780691273457), checked 2026-09-05.
3. Ravindra K. Ahuja, Thomas L. Magnanti, and James B. Orlin, *Network Flows: Theory, Algorithms, and Applications*, Prentice Hall, 1993, Chapters 1–4. [MIT-hosted record](https://dspace.mit.edu/handle/1721.1/49424), checked 2026-09-05.
4. Thomas H. Cormen et al., *Introduction to Algorithms*, 4th ed., MIT Press, 2022, Chapter 24. [Official publisher record](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/), checked 2026-09-05.
5. Jeff Erickson, *Algorithms*, 1st ed., 2019, maximum-flow chapter. [Author-hosted book](https://jeffe.cs.illinois.edu/teaching/algorithms/), checked 2026-09-05.
6. Boost C++ Libraries, “Boykov-Kolmogorov Maximum Flow,” Boost.Graph 1.92.0 documentation. [Official documentation](https://www.boost.org/doc/libs/latest/libs/graph/doc/html/graph/algorithms/network_flow/boykov_kolmogorov_max_flow.html), checked 2026-09-05.
7. Google, “Maximum Flows,” OR-Tools documentation, updated 2026-03-18. [Official documentation](https://developers.google.com/optimization/flow/maxflow), checked 2026-09-05.

## Exercises

### Exercise 1

For edges $s\to a$ capacity five, $s\to b$ four, $a\to b$ two, $a\to t$ three, and $b\to t$ six, validate flow $(4,2,1,3,3)$ in that order, compute value, and list every positive residual direction and capacity.

### Exercise 2

Prove that augmenting a feasible flow by the bottleneck of a simple residual $s$-$t$ path preserves capacity constraints and conservation and increases value by exactly the bottleneck.

### Exercise 3

Diagnose a representation that merges parallel arcs, identifies reverse edges only by swapped endpoints, stores unsigned residuals with unchecked subtraction, computes gross source output, and mutates a path edge-by-edge without rollback.

### Exercise 4

Compare explicit paired residual slots, on-demand residual construction, and a linear-programming model for a high-throughput solver, an audit-oriented teaching system, and an independently implemented verifier.

### Exercise 5

Design a resumable flow-state service for untrusted capacity uploads. Specify validation, identity, arithmetic, snapshots, path transactions, checkpoints, cancellation, and evidence boundaries before any maximum-flow algorithm is selected.

## Answers to the Exercises

### Answer 1

Flows are $f(sa)=4,f(sb)=2,f(ab)=1,f(at)=3,f(bt)=3$. At $a$, inflow four equals outflow $1+3=4$. At $b$, inflow $2+1=3$ equals outflow three. Every amount lies within capacity. Value is source net outflow $4+2=6$, equal to sink input $3+3=6$.

Positive residuals are forward/reverse pairs: `sa:f=1`, `sa:r=4`; `sb:f=2`, `sb:r=2`; `ab:f=1`, `ab:r=1`; `at:r=3` with no positive forward residual; `bt:f=3`, `bt:r=3`. Each pair sums to its original capacity.

### Answer 2

For every forward step, $\Delta\le c(e)-f(e)$ gives $f(e)+\Delta\le c(e)$ and nonnegativity remains. For every reverse step, $\Delta\le f(e)$ gives $f(e)-\Delta\ge0$ and the upper bound remains. Edges outside the path do not change.

At each internal path vertex, the residual path brings one adjustment in and takes one out. Whether a step adds forward flow or cancels opposite flow, its residual orientation changes net balance by $+\Delta$ on entry and $-\Delta$ on exit, so conservation remains. At $s$ only the outgoing residual adjustment remains, raising net outflow by $\Delta$; at $t$ net inflow rises by $\Delta$.

### Answer 3

Retain stable identity and state for every parallel original edge or define a reversible aggregation with output reconstruction. Endpoint swapping cannot select a unique reverse with parallel or anti-parallel arcs; store reciprocal slot indices and original-edge/direction metadata.

Checked signed or tagged arithmetic must reject subtraction below zero and addition above range. Compute value as outgoing minus incoming source flow. Apply all path changes to a candidate copy or transaction with undo logging, validate capacity/conservation/pairing, then commit atomically. Bind every step to one snapshot.

### Answer 4

Explicit paired slots suit a high-throughput graph solver: traversal and updates are direct, at the cost of strict reverse-index and atomic-update invariants. On-demand residual construction suits an audit-oriented system with original flow as the single source of truth; it is easier to explain and recompute but adds search overhead.

An independent verifier benefits from a structurally different formulation such as incidence-matrix conservation plus direct capacity inequalities, optionally a linear program for bounded instances. Independence reduces shared representation defects. No option alone validates domain modeling, units, or snapshot provenance.

### Answer 5

Parse a complete stable vertex universe, distinct source/sink, unique logical edge IDs, endpoints, nonnegative capacities, units, and numeric limits into an immutable digest. Reject NaN, overflow-risk bounds, unknown endpoints, and ambiguous duplicate IDs. Store original flow plus explicit paired residual metadata or recompute residuals from flow; validate zero-flow initialization and every restored state.

For a residual adjustment, record connected edge/direction identities, positive residuals, checked bottleneck, previous flow values, and revision. Apply to a copy or transaction, recompute capacity, conservation, terminal values, and residual-pair sums, then commit atomically. A checkpoint contains graph digest, validated flow, representation/algorithm version, search/frontier and predecessor state, pending transaction state, and output cursor.

Cancellation preserves only the last committed feasible state and returns incomplete; it does not claim maximum. Publish graph revision, capacities/flows, net value, feasibility evidence, residual representation version, status, and limitations. Later path-selection and maximum/cut proofs remain separate algorithm evidence.
