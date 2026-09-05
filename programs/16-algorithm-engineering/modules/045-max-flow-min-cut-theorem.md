---
module_id: ALGE-045
program: Algorithm Engineering
level: 1
module_number: 45
title: Max-Flow Min-Cut Theorem
status: complete
last_verified: 2026-09-05
---

# Max-Flow Min-Cut Theorem

## One-Page Review

### Governing question

Why does the largest feasible source-to-sink flow equal the smallest source-sink cut capacity, and how can that equality become an independently checkable optimality certificate?

### Essential definitions

- An **$s$-$t$ cut** is a partition $(S,T)$ of the vertices with $s\in S$ and $t\in T$.
- Its **capacity** is $c(S,T)=\sum_{e\in\delta^+(S)}c(e)$: only original edges directed from $S$ to $T$ count.
- **Weak duality** says every feasible flow satisfies $|f|\le c(S,T)$ for every $s$-$t$ cut.
- A **minimum cut** has least capacity among all $s$-$t$ cuts.
- A **maximum flow** has greatest value among all feasible flows.
- A **residual reachable set** contains exactly the vertices reachable from $s$ through positive residual directions.
- A **primal certificate** is a feasible flow; a **dual certificate** is a cut. Equal objective values prove both optimal.

### Central model, mechanism, or theorem

For every finite directed capacity network,

$$
\max_{f\text{ feasible}}|f|=\min_{(S,T)\text{ an }s\text{-}t\text{ cut}}c(S,T).
$$

For a feasible flow, the following are equivalent: it is maximum; its residual graph has no $s$-$t$ path; and some cut has capacity equal to its value. When no residual path exists, take $S$ as vertices reachable from $s$. Every original edge from $S$ to $T$ is saturated, and every original edge from $T$ to $S$ carries zero flow. Therefore $|f|=c(S,T)$. Weak duality then proves the flow maximum and the cut minimum.

### Critical invariants

- The graph is a finite directed multigraph with distinct terminals and nonnegative capacities.
- Flow satisfies every edge bound and conservation at every nonterminal.
- Flow value is net source outflow, not merely gross outgoing flow.
- Cut capacity counts original capacities leaving $S$, never residual capacities or entering edges.
- The cut sets partition the declared vertex universe and separate $s$ from $t$.
- Residual reachability includes forward unused capacity and reverse cancellable flow.
- Equality requires every outward crossing edge saturated and every inward crossing edge at zero.
- Flow, cut, capacities, and validation belong to one immutable snapshot and numeric domain.

### Common failures

Common failures include summing both directions in cut capacity; counting residual capacity; omitting parallel edges; computing gross source output; accepting a flow that violates conservation; deriving $S$ using only forward unused capacity; assuming any cut is minimum; assuming any feasible flow matching a claimed scalar is maximum; confusing maximum value with a unique edge-flow solution; using approximate equality without a declared error model; and validating a cut against a different graph revision.

### Compact example

A feasible flow has value six. Cut $S=\{s,a,b\}$ has outward edges of capacities two and four, both saturated, and no entering cut flow. Its capacity is six. Weak duality says no flow can exceed six; the feasible flow attains six. The equality, not the algorithm's reputation, certifies maximum flow and minimum cut.

### Connections

[ALGE-041](./041-flow-networks-and-residual-graphs.md) defines residuals and the cut upper bound. [ALGE-042](./042-ford-fulkerson-method.md), [ALGE-043](./043-edmonds-karp-algorithm.md), and [ALGE-044](./044-dinic-s-algorithm.md) construct flows and residual reachable sets. [ALGE-046](../ROADMAP.md#block-05--flows-matching-and-combinatorial-optimization) uses integrality and flow-cut structure for bipartite matching.

## Governing Question

Given a candidate original-edge flow and a candidate vertex cut, what assumptions and derivations prove that their equal values establish maximum flow and minimum cut, and what must an independent verifier check before accepting that conclusion?

The theorem is simultaneously an existence result, an algorithmic stopping argument, a duality statement, and a certificate design. Keeping those roles separate prevents a common mistake: treating a solver's returned number as proof when the checkable flow and cut evidence is missing.

## Why This Matters

Optimization normally raises an asymmetry: finding an optimum may be expensive, while checking feasibility alone proves only that a value is achievable. Max-flow/min-cut closes the gap. A feasible flow is a lower bound on the optimum; a cut is an upper bound. When the bounds meet, an independent verifier can certify optimality using linear scans and exact arithmetic.

The cut also explains bottlenecks. Yet mathematical capacity is not automatically causal capacity in a deployed system. A minimum cut belongs to one static model snapshot. Latency, stochastic failures, shared resources, multiple commodities, lower bounds, gains, time, and policy constraints may require different models. The theorem validates the optimization model, not the model's fidelity to reality.

## Prerequisites and Retrieval

Retrieve directed multigraphs, partitions, sums, feasible flow, conservation, residual graphs, augmenting paths, proof by contradiction, weak/strong duality, exact arithmetic, and immutable snapshots. Review [ALGE-041](./041-flow-networks-and-residual-graphs.md) for residual construction and the cut upper bound, plus [ALGE-042](./042-ford-fulkerson-method.md) for augmentation preservation.

## Learning Objectives

After completing this module, you should be able to:

1. define directed cut capacity precisely for multigraphs;
2. derive the flow-across-a-cut identity from conservation;
3. prove weak duality for every feasible flow and $s$-$t$ cut;
4. prove equivalence of maximum flow, no augmenting path, and flow-cut equality;
5. derive a minimum cut from residual reachability;
6. identify the exact saturation and zero-inward-flow equality conditions;
7. separate the theorem from the integral-flow corollary and algorithm termination;
8. implement a linear-time flow-and-cut certificate verifier;
9. handle terminal incident edges, parallel arcs, numeric domains, and snapshots;
10. interpret minimum cuts without overstating uniqueness or domain causality.

## Core Exposition

### Define the primal and dual objects

Let $G=(V,E)$ be a finite directed multigraph with distinct source $s$, sink $t$, and capacities $c(e)\ge0$. A feasible flow $f$ satisfies $0\le f(e)\le c(e)$ and conservation at every $v\notin\{s,t\}$. Define $|f|$ as net outflow from $s$.

For $S\subset V$ with $s\in S$ and $t\notin S$, write $T=V\setminus S$. Let $\delta^+(S)$ be original edges from $S$ to $T$ and $\delta^-(S)$ original edges from $T$ to $S$. The directed cut capacity is

$$
c(S,T)=\sum_{e\in\delta^+(S)}c(e).
$$

Entering capacities do not count. Parallel edges each count. Self-loops never cross a partition.

### Derive the cut-flow identity

Sum net outflow over every vertex in $S$. Each edge internal to $S$ appears once as outgoing and once as incoming, so it cancels. Because $s\in S$, $t\notin S$, and all other vertices conserve flow, the remaining vertex sum is $|f|$. Only crossing edges remain:

$$
|f|=f(S,T)-f(T,S),
$$

where $f(S,T)=\sum_{e\in\delta^+(S)}f(e)$ and analogously for $f(T,S)$. This identity remains valid when original edges enter $s$ or leave $t$ because value is net flow.

Capacity feasibility and nonnegativity give

$$
|f|=f(S,T)-f(T,S)\le f(S,T)\le c(S,T).
$$

This is weak duality. Every feasible flow value is a lower bound on the maximum; every cut capacity is an upper bound.

### Prove equality conditions

The two weak-duality inequalities become equalities exactly when

$$
f(T,S)=0
\quad\text{and}\quad
f(e)=c(e)\text{ for every }e\in\delta^+(S).
$$

Thus every entering crossing edge carries zero, and every outward crossing edge is saturated. Aggregate equality with nonnegative terms implies these edgewise facts, though an implementation should check them directly for clearer diagnostics.

If a feasible flow and valid cut have $|f|=c(S,T)$, no feasible flow can have larger value and no cut can have smaller capacity. They are a matched lower/upper-bound certificate.

### Derive the cut from residual exhaustion

Suppose the residual graph $G_f$ has no path from $s$ to $t$. Let $S$ be all vertices residually reachable from $s$; then $s\in S$ and $t\notin S$.

Take an original edge $e=(u,v)$ with $u\in S,v\in T$. If $f(e)<c(e)$, its forward residual capacity is positive, making $v$ reachable, a contradiction. Hence every outward crossing edge is saturated.

Take an original edge $e=(u,v)$ with $u\in T,v\in S$. If $f(e)>0$, its reverse residual direction runs from $v\in S$ to $u\in T$, again making $u$ reachable. Hence every entering crossing edge has zero flow. The equality conditions hold, so $|f|=c(S,T)$.

### Prove the equivalence theorem

For a feasible flow $f$, consider:

1. $f$ is maximum;
2. $G_f$ has no residual $s$-$t$ path;
3. some $s$-$t$ cut has capacity $|f|$.

If a residual path existed, augmenting by its positive bottleneck would create a feasible flow of larger value; therefore (1) implies (2). Residual exhaustion and the reachable-set argument prove (2) implies (3). Weak duality proves (3) implies (1). These implications also prove that the maximum flow value equals the minimum cut capacity.

The theorem does not say the maximum flow or minimum cut is unique. It says their optimal objective values coincide and at least one pair of optimal objects exists under the finite-network assumptions.

### Verify a flow-cut certificate

The verifier below does not run a maximum-flow algorithm. It validates a supplied flow and cut using a structurally direct formulation.

<!-- bijux-verify: {"id":"flow-cut-certificate","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"value=6 cut_capacity=6\nfeasible=True certificate=True\nmaximum=True minimum_cut=True\n","stderr":""}} -->
```python
vertices = {"s", "a", "b", "t"}
edges = {
    "sa": ("s", "a", 4), "sb": ("s", "b", 3),
    "ab": ("a", "b", 2), "at": ("a", "t", 2),
    "bt": ("b", "t", 4),
}
flow = {"sa": 3, "sb": 3, "ab": 1, "at": 2, "bt": 4}
source_side = {"s", "a", "b"}


def verify_flow(candidate):
    if set(candidate) != set(edges):
        return False, None
    balance = {vertex: 0 for vertex in vertices}
    for edge_id, (tail, head, capacity) in edges.items():
        amount = candidate[edge_id]
        if not isinstance(amount, int) or not 0 <= amount <= capacity:
            return False, None
        balance[tail] -= amount
        balance[head] += amount
    feasible = all(balance[v] == 0 for v in vertices - {"s", "t"})
    value = -balance["s"]
    feasible = feasible and balance["t"] == value
    return feasible, value


def verify_cut(candidate, source_set):
    if not source_set <= vertices or "s" not in source_set or "t" in source_set:
        return False, None
    outward = [e for e, (u, v, _) in edges.items() if u in source_set and v not in source_set]
    inward = [e for e, (u, v, _) in edges.items() if u not in source_set and v in source_set]
    capacity = sum(edges[e][2] for e in outward)
    equality_conditions = (
        all(candidate[e] == edges[e][2] for e in outward)
        and all(candidate[e] == 0 for e in inward)
    )
    return equality_conditions, capacity


feasible, value = verify_flow(flow)
cut_conditions, cut_capacity = verify_cut(flow, source_side)
certificate = feasible and cut_conditions and value == cut_capacity
print(f"value={value} cut_capacity={cut_capacity}")
print(f"feasible={feasible} certificate={certificate}")
print(f"maximum={certificate} minimum_cut={certificate}")
```

The conclusion is conditional on successful validation of this exact snapshot. The program establishes observed behavior for one certificate; the theorem justifies why the validated equality proves optimality generally.

### Separate theorem, integrality, and algorithms

Max-flow/min-cut equality does not require capacities to be integers. It is an equality for finite networks over a suitable exact nonnegative capacity domain. Integrality is a separate corollary: with integer capacities, augmenting-path algorithms starting from zero can produce an integral maximum flow because every bottleneck remains integral.

Likewise, the theorem does not prescribe Ford-Fulkerson, Edmonds-Karp, Dinic, push-relabel, or a linear program. Different algorithms may construct different optimal flows and cuts. The certificate checker should be simpler and structurally independent from the solver where practical.

### Validate numeric and representation assumptions

Use stable edge identity so parallel and anti-parallel originals are checked independently. Recompute net balances with checked wide or arbitrary-precision arithmetic. Reject missing edges, extra edges, negative capacity, out-of-range flow, NaN, ambiguous vertex membership, and a source-side set that omits $s$ or contains $t$.

Exact integers and rationals permit exact equality. Fixed-point quantities require declared units and scale. Floating certificates need a rigorous error model: a tolerance can otherwise accept infeasibility or a false equality. Interval bounds can support a qualified certificate only if the feasible lower bound and cut upper bound meet under documented rounding.

### Govern snapshots and publication

Canonicalize and hash the vertex universe, edge IDs, endpoints, capacities, units, terminals, and numeric policy. Bind both flow and cut to that digest. A cut computed before a capacity update cannot certify a flow afterward.

Publish solver status separately from certificate status. A useful result contains original-edge flows, net value, source-side set, crossing edges, cut capacity, feasibility checks, equality checks, algorithm/tool version, snapshot digest, numeric policy, and limitations. If certificate validation fails, do not downgrade silently to `optimal`; return a distinct internal or evidence failure.

Current Google OR-Tools maximum-flow documentation reports optimal flow, per-arc flows, and source- and sink-side minimum-cut sets after an optimal solve. That current interface illustrates certificate-oriented output. Callers must still bind it to their input revision and validate their own domain model.

### Interpret a minimum cut responsibly

A minimum cut identifies a capacity bottleneck in the declared static network. Multiple minimum cuts may exist, so membership in one returned cut is not proof that an edge is uniquely critical. Increasing one cut edge may not increase maximum flow because another minimum cut can remain limiting. Sensitivity analysis requires more than reading one partition.

Operational capacity may be shared, stochastic, time-varying, lossy, or coupled across commodities. A static cut can be a planning bound while observed throughput remains lower. Explain the model, units, time horizon, and exclusions before turning a theorem-backed optimization result into a production decision.

## Definitions and Notation

- $(S,T)$: vertex partition with $s\in S,t\in T$.
- $\delta^+(S)$: original edges from $S$ to $T$.
- $\delta^-(S)$: original edges from $T$ to $S$.
- $c(S,T)$: sum of original capacities on $\delta^+(S)$.
- $f(S,T)$, $f(T,S)$: crossing-flow sums by direction.
- $|f|$: net source outflow.
- $G_f$: residual graph of feasible flow $f$.
- **weak duality**: $|f|\le c(S,T)$ for every feasible flow and valid cut.
- **strong equality**: maximum flow value equals minimum cut capacity.
- **certificate pair**: feasible flow and valid cut with equal objectives.

## Mechanisms, Invariants, or Proof Structure

Summed conservation over $S$ cancels internal edges and gives $|f|=f(S,T)-f(T,S)$. Nonnegative flow and outward capacity bounds give weak duality. If no augmenting path exists, residual reachability defines a cut with saturated outward edges and zero-flow inward edges, producing equality. Conversely, an augmenting path contradicts maximality. Thus maximum flow, residual exhaustion, and an equal-capacity cut are equivalent. Independent verification checks the primal flow, dual cut, shared snapshot, and equality without replaying solver choices.

## Alternatives and Trade-Offs

- **Residual-reached cut:** obtained naturally from many solvers; requires correct reverse residual reachability.
- **Externally supplied cut:** easy to validate; provenance and snapshot binding remain necessary.
- **Full augmentation trace:** supports debugging; much larger and less direct than a final certificate.
- **Flow-cut pair:** compact linear-time optimality evidence; does not prove domain-model fitness.
- **Exact integers/rationals:** exact equality and reproducibility; range and operand cost must be governed.
- **Fixed point:** bounded operational representation; scale and rounding become model assumptions.
- **Floating point:** convenient but complicates feasibility and equality certification.
- **One minimum cut:** sufficient for optimality; insufficient for uniqueness or sensitivity conclusions.
- **Independent verifier:** reduces shared solver defects; adds implementation and maintenance cost.

## Failure Modes and Misconceptions

- Directed cut capacity counts only original edges leaving the source side.
- Residual capacity is not cut capacity.
- Gross source output is not flow value when edges enter the source.
- Equal scalar values do not certify anything unless flow and cut are independently valid.
- Outward saturation without zero inward crossing flow is insufficient for equality.
- Forward-only reachability can produce a false source-side set.
- A maximum flow need not be unique.
- A minimum cut need not be unique.
- An edge in one minimum cut is not necessarily uniquely limiting.
- Integral optimal flow is a corollary under integral capacities, not the theorem's premise.
- Solver optimality does not establish current data, correct units, or domain causality.

## Worked Examples

### Example 1

**Situation.** A cut has outward capacities four and seven and inward capacity nine. Its cut capacity is eleven, not twenty. **Reasoning.** Directed cut capacity sums only original edges leaving $S$. **Conclusion.** Entering capacity never enlarges the upper bound definition.

### Example 2

**Situation.** Across a cut, outward flow is eight and inward flow is three. **Reasoning.** Summed conservation gives value $8-3=5$. **Conclusion.** Crossing flow is directional and net.

### Example 3

**Situation.** A feasible flow has value five and a cut has capacity seven. **Reasoning.** Weak duality brackets the unknown optimum between five and seven. **Conclusion.** A two-unit gap means neither object alone proves optimality.

### Example 4

**Situation.** A feasible flow and valid cut both have value nine. **Reasoning.** No feasible flow exceeds the cut's nine, while the supplied flow achieves nine. **Conclusion.** Both are optimal regardless of how they were found.

### Example 5

**Situation.** An outward crossing edge has capacity six and flow five. **Reasoning.** Its forward residual is one, so the head would be reachable from a residually reached source side. **Conclusion.** Such an edge cannot cross the residual reachable cut.

### Example 6

**Situation.** An entering crossing edge carries two. **Reasoning.** Its reverse residual of two leaves $S$, contradicting maximal residual reachability. **Conclusion.** Inward crossing flow must be zero for the reached cut.

### Example 7

**Situation.** Two parallel outward edges have capacities two and three. **Reasoning.** Both cross and contribute separately. **Conclusion.** Cut capacity is five; endpoint deduplication would undercount.

### Example 8

**Situation.** Source sends ten and receives four. **Reasoning.** Net source outflow is six, which is the conserved flow value. **Conclusion.** Gross output ten can falsely break certificate equality.

### Example 9

**Situation.** Two different cuts each have capacity twelve. **Reasoning.** One certified flow attains twelve, making both cuts minimum. **Conclusion.** The theorem ensures equal optimal values, not unique partitions.

### Example 10

**Situation.** A certified minimum cut is computed from yesterday's capacities, while one edge capacity changed today. **Reasoning.** The upper bound belongs to the old snapshot. **Conclusion.** Without matching digests, the certificate is invalid for today's flow.

## Cross-Program Connections

- Linear Systems and Data Science connect flow conservation to incidence matrices and linear-program duality.
- Database Engineering owns immutable snapshots, digest binding, transaction boundaries, and evidence provenance.
- Software Testing and Quality Engineering owns independent certificate, mutation, boundary, and differential tests.
- Network and Distributed Systems distinguish a static capacity model from queues, failures, routing, and multiple commodities.
- Security Engineering reviews forged cuts, overflow, NaN, identity confusion, stale evidence, and status escalation.
- Software Architecture owns separation between solver, verifier, model, policy, and publication contracts.

## References

1. Lester R. Ford Jr. and Delbert R. Fulkerson, “Maximal Flow Through a Network,” *Canadian Journal of Mathematics* 8, 399–404, 1956, DOI [10.4153/CJM-1956-045-5](https://doi.org/10.4153/CJM-1956-045-5). Primary theorem source and publisher record checked 2026-09-05.
2. Lester R. Ford Jr. and Delbert R. Fulkerson, *Flows in Networks*, Princeton University Press, 1962; 2025 digital edition. [Official publisher record](https://doi.org/10.1515/9780691273457), checked 2026-09-05.
3. Ravindra K. Ahuja, Thomas L. Magnanti, and James B. Orlin, *Network Flows: Theory, Algorithms, and Applications*, Prentice Hall, 1993. [MIT-hosted record](https://dspace.mit.edu/handle/1721.1/49424), checked 2026-09-05.
4. Thomas H. Cormen et al., *Introduction to Algorithms*, 4th ed., MIT Press, 2022, Chapter 24. [Official publisher record](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/), checked 2026-09-05.
5. Jeff Erickson, *Algorithms*, 1st ed., 2019, maximum-flow chapter. [Author-hosted book](https://jeffe.cs.illinois.edu/teaching/algorithms/), checked 2026-09-05.
6. Google, “Maximum Flows,” OR-Tools documentation, updated 2026-03-18. [Official documentation](https://developers.google.com/optimization/flow/maxflow), checked 2026-09-05.

## Exercises

### Exercise 1

Define an $s$-$t$ cut and its capacity in a directed multigraph. Explain the treatment of parallel, anti-parallel, entering, and self-loop edges.

### Exercise 2

Derive $|f|=f(S,T)-f(T,S)\le c(S,T)$ from conservation and capacity constraints. State precisely when both inequalities are equalities.

### Exercise 3

Diagnose a verifier that accepts gross source output, sums crossing capacity in both directions, ignores parallel IDs, checks only outward saturation, uses unchecked 32-bit totals, and accepts a cut from another revision.

### Exercise 4

Compare an augmentation trace, a solver status, a feasible flow alone, a cut alone, and a matched flow-cut pair as evidence. Explain what each proves and does not prove.

### Exercise 5

A capacity-planning service reports one minimum cut as “the unique cause” of low throughput. Design a technically sound result and review process addressing multiple cuts, sensitivity, time-varying data, shared resources, units, certificate validation, and decision limitations.

## Answers to the Exercises

### Answer 1

Choose $S\subset V$ with $s\in S$ and $t\notin S$; let $T=V\setminus S$. Cut capacity is the sum of capacities of every original logical edge whose tail is in $S$ and head in $T$. Each parallel edge contributes separately. An anti-parallel edge from $T$ to $S$ is entering and contributes nothing to directed cut capacity. A self-loop has both endpoints on one side and never crosses.

The full declared vertex universe must be partitioned exactly; missing or unknown vertices invalidate the cut. Capacity belongs to one immutable graph snapshot and uses original, not residual, values.

### Answer 2

Sum outgoing-minus-incoming flow balances over vertices in $S$. Internal edges cancel. Conserved nonterminal balances vanish, leaving source net outflow because the sink is outside. Crossing terms yield $|f|=f(S,T)-f(T,S)$. Nonnegativity gives $f(S,T)-f(T,S)\le f(S,T)$, and edge capacity gives $f(S,T)\le c(S,T)$.

The first inequality is equality exactly when all entering crossing flow sums to zero, hence every nonnegative entering edge flow is zero. The second is equality exactly when every outward crossing edge is saturated. With both conditions, flow value equals cut capacity and weak duality certifies both optima.

### Answer 3

Compute net source outflow, including original incoming edges. Sum only original capacities from the source side outward, retaining every logical parallel edge and treating independent anti-parallel edges by direction. Check both outward saturation and zero inward crossing flow, as well as full capacity and conservation feasibility.

Use checked wider or arbitrary-precision totals and reject overflow. Canonicalize the graph, terminals, units, numeric policy, flow, and cut under one digest. A cut from another revision supplies no upper bound for the candidate snapshot and must be rejected or recomputed.

### Answer 4

An augmentation trace can support replay and diagnose invariant preservation, but is large and only as trustworthy as its checker. A solver's `optimal` status is an implementation claim tied to its contract and version. A feasible flow proves a lower bound. A valid cut proves an upper bound. Neither alone normally closes the gap.

A matched pair whose independently validated values are equal proves the flow maximum and cut minimum by weak duality, without replaying the solver. None of these artifacts proves that the input is current, units are correct, the model captures the domain, or deployment performance is adequate; provenance and model review remain separate.

### Answer 5

Publish the validated flow value, at least one source-side cut, crossing edge IDs and capacities, snapshot/time/unit digest, feasibility and equality evidence, and solver/verifier versions. Say “a minimum cut in this snapshot,” not “the unique cause.” Search or analyze alternative minimum cuts when uniqueness matters. Test sensitivity by governed capacity perturbations and recomputation; increasing one returned edge may leave another cut binding.

Review whether capacities share a time basis, whether resources are shared across modeled edges, and whether queues, stochastic failures, multiple commodities, routing policy, storage, losses, or time expansion invalidate the static model. Compare predictions with observed data without calling empirical agreement a theorem. A decision record should distinguish mathematical optimality, data currency, model adequacy, sensitivity, operational risk, acceptable alternatives, and human approval criteria.
