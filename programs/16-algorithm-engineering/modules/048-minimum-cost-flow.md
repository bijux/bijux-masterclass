---
module_id: ALGE-048
program: Algorithm Engineering
level: 1
module_number: 48
title: Minimum-Cost Flow
status: complete
last_verified: 2026-09-05
---

# Minimum-Cost Flow

## One-Page Review

### Governing question

How can a network route required supplies to demands within arc bounds at minimum total cost, and what residual evidence certifies that no cheaper feasible routing exists?

### Essential definitions

- A **supply vector** $b$ uses the convention $\operatorname{out}_f(v)-\operatorname{in}_f(v)=b(v)$; positive values supply flow and negative values demand it.
- Arc $e$ has lower bound $\ell_e$, upper capacity $u_e$, unit cost $c_e$, and flow $f_e$ with $\ell_e\le f_e\le u_e$.
- Total cost is $c(f)=\sum_e c_ef_e$.
- A **residual forward arc** has capacity $u_e-f_e$ and cost $c_e$; a **residual reverse arc** has capacity $f_e-\ell_e$ and cost $-c_e$.
- A **negative residual cycle** is a directed residual cycle whose arc costs sum below zero.
- A vertex potential $\pi$ gives reduced cost $c_\pi(u,v)=c(u,v)+\pi(u)-\pi(v)$.
- A feasible flow and potentials with nonnegative reduced cost on every positive-capacity residual arc form an optimality certificate.

### Central model, mechanism, or theorem

A feasible flow is minimum-cost exactly when its residual graph contains no negative-cost cycle. Augmenting around a negative cycle preserves every node balance and decreases cost. Conversely, the difference between a cheaper feasible flow and the candidate decomposes into residual cycles, at least one of which must be negative.

Potentials do not change cycle costs because their terms telescope. Therefore nonnegative residual reduced costs prove that no negative cycle exists. Successive-shortest-path algorithms maintain potentials so that reduced costs are nonnegative and shortest paths can be found efficiently.

### Critical invariants

- $\sum_v b(v)=0$ is necessary for a closed balanced instance.
- Every arc satisfies its declared lower and upper bounds.
- Every vertex satisfies the same signed balance convention.
- Reverse residual cost is the negation of the original unit cost.
- Residual capacity is positive before an arc participates in a path or cycle.
- Potentials telescope on cycles and reduced costs stay nonnegative when used as a certificate.
- Costs, bounds, supplies, flows, potentials, and validation refer to one immutable snapshot.

### Common failures

Common failures include mixing demand sign conventions; optimizing before checking feasibility; omitting reverse residual arcs; assigning reverse arcs the original cost; using Dijkstra with negative reduced costs; assuming a negative original arc makes the instance unbounded; forgetting that an infinite-capacity negative cycle does make it unbounded; mishandling lower bounds; overflowing $c_ef_e$ or the total; accepting approximate balance without an error model; and treating model cost as real-world service quality.

### Compact example

A feasible flow has cost eight. Its positive-capacity residual arcs have reduced costs $0,1,2,0,0,0,0$ under supplied potentials. Any residual cycle has nonnegative reduced cost, and its potential terms cancel, so it has nonnegative original cost. No cheaper feasible flow exists; feasibility plus this reduced-cost check certifies optimality.

### Connections

[ALGE-047](./047-assignment-problems.md) is a unit-capacity special case with row and column potentials. [ALGE-041](./041-flow-networks-and-residual-graphs.md) defines residual cancellation, and [ALGE-045](./045-max-flow-min-cut-theorem.md) develops lower/upper-bound certificates. [ALGE-049](../ROADMAP.md#block-05--flows-matching-and-combinatorial-optimization) applies flow models to domain constraints.

## Governing Question

Given a directed network with supplies, demands, lower and upper arc bounds, and additive unit costs, how do we distinguish feasibility from optimality, improve a feasible routing safely, and validate a compact certificate without trusting the solver implementation?

Minimum-cost flow unifies transportation, transshipment, assignment, inventory movement, and many scheduling relaxations. Its guarantees are strong precisely because the model is specific: a single conserved commodity, linear separable costs, fixed bounds, and a static snapshot.

## Why This Matters

Maximum flow values quantity but ignores which feasible routing is preferable. Minimum-cost flow fixes an amount or a supply-demand vector and chooses the cheapest routing. Negative unit costs, cancellations, multiple sources, lower commitments, and competing routes make naive shortest-path reasoning insufficient.

The residual graph supplies both an algorithm and an audit language. It describes every allowed local change to the current flow. A negative residual cycle is a concrete improvement; nonnegative reduced costs are concise evidence that no such improvement exists. Production systems can validate this evidence separately from a large solver.

## Prerequisites and Retrieval

Retrieve directed multigraphs, feasible flow, conservation, residual forward and reverse directions, shortest paths with negative edges, cycle decomposition, linear objectives, and integer arithmetic. Review [ALGE-041](./041-flow-networks-and-residual-graphs.md), [ALGE-045](./045-max-flow-min-cut-theorem.md), and the primal-dual certificate in [ALGE-047](./047-assignment-problems.md).

## Learning Objectives

After completing this module, you should be able to:

1. formulate supplies, demands, lower bounds, capacities, and linear arc costs;
2. separate feasibility, boundedness, and optimality statuses;
3. construct the costed residual graph correctly;
4. prove that negative-cycle augmentation preserves feasibility and lowers cost;
5. prove the no-negative-cycle optimality characterization;
6. use potentials and reduced costs as an independently checkable certificate;
7. trace successive shortest augmentations with valid potential updates;
8. transform lower bounds and fixed-value source-sink variants coherently;
9. validate numeric, identity, and snapshot assumptions; and
10. identify problems that violate single-commodity linear-cost assumptions.

## Core Exposition

### Formulate the transshipment model

Let $G=(V,E)$ be a finite directed multigraph. Each arc $e=(u,v)$ has lower bound $\ell_e$, upper bound $u_e$, and unit cost $c_e$, where $0\le\ell_e\le u_e$. Each vertex has supply $b(v)$. Use one explicit convention:

$$
\sum_{e\in\delta^+(v)}f_e-\sum_{e\in\delta^-(v)}f_e=b(v).
$$

Positive $b(v)$ is net production; negative $b(v)$ is net consumption. A feasible flow satisfies all arc bounds and balances. Summing balances over all vertices cancels every arc, so $\sum_vb(v)=0$ is necessary. It is not sufficient: cuts and capacities may still prevent supply from reaching demand.

The optimization problem is

$$
\min_f\sum_{e\in E}c_ef_e
\quad\text{subject to balances and }\ell_e\le f_e\le u_e.
$$

Costs may be negative. Finite capacities can still bound the objective; negativity alone does not imply unboundedness.

### Construct the costed residual graph

For original arc $e=(u,v)$ under feasible $f$:

- if $f_e<u_e$, add residual $u\to v$ with capacity $u_e-f_e$ and cost $c_e$;
- if $f_e>\ell_e$, add residual $v\to u$ with capacity $f_e-\ell_e$ and cost $-c_e$.

Sending $\Delta$ units on a forward residual arc increases $f_e$; sending it on a reverse residual arc decreases $f_e$. The cost signs follow from the objective change. Stable original-arc identity is essential when parallel or anti-parallel arcs cause several residual arcs to share endpoints.

An augmentation around a directed residual cycle changes one incoming and one outgoing residual amount at every visited vertex, so balances are preserved. Choosing no more than the minimum residual capacity preserves bounds. The objective changes by $\Delta$ times the cycle's residual cost.

### Characterize optimality by negative cycles

**Theorem.** A feasible flow $f$ is minimum-cost if and only if its positive-capacity residual graph contains no negative-cost directed cycle.

If a negative cycle exists, augment by its positive bottleneck. Feasibility is preserved and the objective strictly decreases, so $f$ was not optimal.

Conversely, suppose a cheaper feasible flow $g$ exists. The difference $g-f$ respects zero net balance at every vertex. Positive differences use forward residual directions and negative differences use reverse residual directions; feasibility of $g$ ensures enough residual capacity. This nonzero residual circulation decomposes into directed cycles. Its total residual cost equals $c(g)-c(f)<0$. If every cycle in the decomposition had nonnegative cost, their capacity-weighted sum could not be negative. Therefore at least one negative residual cycle exists. The contradiction proves optimality when none exists.

This argument assumes both flows meet the same supply vector and bounds. A path, rather than a cycle, can improve an infeasible intermediate state because its endpoints may carry excess and deficit.

### Turn potentials into a compact certificate

For residual arc $a=(u,v)$ with cost $c(a)$, define

$$
c_\pi(a)=c(a)+\pi(u)-\pi(v).
$$

Around any directed cycle, every potential occurs once positively and once negatively, so the reduced cycle cost equals its original cost. If every positive-capacity residual arc has $c_\pi(a)\ge0$, every residual cycle is nonnegative and the feasible flow is optimal.

The converse also holds: if the residual graph has no negative cycle, add a super-source with zero-cost arcs to all vertices and let $d(v)$ be shortest-path distances. The triangle inequality $d(v)\le d(u)+c(u,v)$ yields $c(u,v)+d(u)-d(v)\ge0$. Thus $\pi=d$ supplies feasible potentials.

A certificate checker validates the original graph, bounds, balances, cost, residual construction, every reduced-cost inequality, and shared snapshot digest. It need not find shortest paths or replay solver pivots.

### Trace successive shortest augmenting paths

For zero lower bounds and a balanced integral supply vector, start with zero flow and vertex excess $e(v)=b(v)-\operatorname{out}_f(v)+\operatorname{in}_f(v)$. Select a vertex with positive excess and a reachable vertex with negative excess. Send the minimum of source excess, destination deficit, and path bottleneck along a cheapest residual path.

If original residual costs can be negative, initialize valid potentials with Bellman-Ford or another negative-edge-capable method. With nonnegative reduced costs, use Dijkstra. If $d_\pi(v)$ are reduced-cost shortest distances from the selected source, update reached potentials by $\pi(v)\leftarrow\pi(v)+d_\pi(v)$. For residual edge $u\to v$, shortest-path inequality gives

$$
c_{\pi'}(u,v)=c_\pi(u,v)+d_\pi(u)-d_\pi(v)\ge0.
$$

After augmentation, newly created reverse arcs of used path edges have zero reduced cost. The invariant is preserved. Integral supplies, bounds, and augmentations produce integral flows. Complexity depends on the variant, data structures, numeric ranges, and how many augmentations occur; “uses Dijkstra” is not by itself a complete bound.

### Transform lower bounds correctly

Set $x_e=f_e-\ell_e$, so $0\le x_e\le u_e-\ell_e$. Substituting into the balance equations gives adjusted supply

$$
b'(v)=b(v)-\left(\sum_{e\in\delta^+(v)}\ell_e-\sum_{e\in\delta^-(v)}\ell_e\right).
$$

Solve for $x$ under $b'$, then recover $f=x+\ell$. The objective becomes $\sum_ec_ex_e+\sum_ec_e\ell_e$; the second term is constant, so minimizers are preserved. Sign errors in the adjusted supplies are a frequent source of infeasible or falsely feasible instances.

A fixed-value $s$-$t$ minimum-cost flow can be expressed with $b(s)=F$, $b(t)=-F$, and zero elsewhere. A maximum flow of minimum cost is lexicographic: first determine maximum value, then minimize cost at that value, or use a solver whose API explicitly implements that combined objective.

### Reproduce feasibility and optimality evidence

The following dependency-free program verifies a candidate flow and potential certificate, then exhaustively recomputes the integral optimum for this small instance. Enumeration is a test oracle, not a scalable algorithm.

<!-- bijux-verify: {"id":"min-cost-flow-certificate","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"feasible=True cost=8\nresidual_arcs=7\ndual_feasible=True min_reduced_cost=0\ncertificate=True enumerated_optimum=8 agrees=True\n","stderr":""}} -->
```python
from itertools import product

vertices = ("s", "a", "b", "t")
supply = {"s": 3, "a": 0, "b": 0, "t": -3}
arcs = {
    "sa": ("s", "a", 3, 2),
    "sb": ("s", "b", 2, 4),
    "ab": ("a", "b", 2, -1),
    "at": ("a", "t", 2, 2),
    "bt": ("b", "t", 3, 1),
}
flow = {"sa": 3, "sb": 0, "ab": 2, "at": 1, "bt": 2}
potential = {"s": 0, "a": 2, "b": 3, "t": 4}


def balances(candidate):
    net = {vertex: 0 for vertex in vertices}
    for edge_id, (tail, head, capacity, _) in arcs.items():
        amount = candidate[edge_id]
        if not 0 <= amount <= capacity:
            return None
        net[tail] += amount
        net[head] -= amount
    return net


def cost_of(candidate):
    return sum(candidate[e] * arcs[e][3] for e in arcs)


def residual(candidate):
    result = []
    for edge_id, (tail, head, capacity, unit_cost) in arcs.items():
        amount = candidate[edge_id]
        if amount < capacity:
            result.append((edge_id, tail, head, capacity - amount, unit_cost))
        if amount > 0:
            result.append((edge_id, head, tail, amount, -unit_cost))
    return result


net = balances(flow)
feasible = net == supply
residual_arcs = residual(flow)
reduced = [
    unit_cost + potential[tail] - potential[head]
    for _, tail, head, _, unit_cost in residual_arcs
]
dual_feasible = all(value >= 0 for value in reduced)

feasible_costs = []
capacities = [arcs[edge_id][2] for edge_id in arcs]
for amounts in product(*(range(capacity + 1) for capacity in capacities)):
    candidate = dict(zip(arcs, amounts))
    if balances(candidate) == supply:
        feasible_costs.append(cost_of(candidate))
optimum = min(feasible_costs)

print(f"feasible={feasible} cost={cost_of(flow)}")
print(f"residual_arcs={len(residual_arcs)}")
print(f"dual_feasible={dual_feasible} min_reduced_cost={min(reduced)}")
print(
    f"certificate={feasible and dual_feasible} "
    f"enumerated_optimum={optimum} agrees={cost_of(flow) == optimum}"
)
```

The candidate's objective is eight. Nonnegative reduced costs prove optimality generally for this snapshot; enumeration independently agrees only for this bounded example.

### Distinguish infeasible, optimal, and unbounded

An implementation needs separate outcomes. `INFEASIBLE` means no flow meets all balances and bounds. `OPTIMAL` requires feasible flow plus an algorithmic or certificate-backed optimality conclusion. `UNBOUNDED` means feasible costs decrease without limit, such as a reachable residual negative cycle with unbounded augmenting capacity in a formulation that permits arbitrary circulation. A time limit or numeric error is none of these.

Before optimization, check vertex and arc identities, bound order, supply sum, numeric range, and obvious reachability. A feasibility reduction can add a super-source to supply vertices and a super-sink from demand vertices and require a saturating flow. Keep this feasibility certificate distinct from the cost-optimality certificate.

### Govern numeric semantics and current interfaces

Use checked wide integers or exact fixed-point units where possible. Multiplication $c_ef_e$, summation over many arcs, distance addition, and potential updates can overflow even when individual inputs fit. Floating arithmetic requires a declared error model for balances, bounds, reduced costs, and objective comparison; an arbitrary epsilon can accept a negative cycle or reject a valid optimum.

Google's OR-Tools minimum-cost-flow documentation, current as retrieved 2026-09-05 and marked updated 2026-03-18, describes `SimpleMinCostFlow` with arc capacities, unit costs, and signed node supplies and exposes distinct solve status, arc flows, and optimal cost. The documented sign convention is net outflow equals supply. That current interface illustrates explicit status and evidence, but callers still must validate units, input revision, overflow bounds, and model fidelity.

### Interpret results without overstating them

The optimum belongs to a static, single-commodity, linear, separable model. Congestion-dependent costs, shared capacity across products, losses or gains, time-expanded behavior, fixed charges, logical dependencies, risk limits, and fairness policies may require convex cost flow, multi-commodity flow, time expansion, or integer optimization.

Publish arc flows including zeros when auditability matters, total cost recomputed from original arcs, unmet supply if the model allows it, potentials or another certificate, snapshot digest, algorithm and version, status, limits, and caveats. A low modeled cost does not prove low latency, ethical allocation, resilience, or causality outside the declared assumptions.

## Definitions and Notation

- $b(v)$: net supply under the convention outflow minus inflow.
- $\ell_e,u_e$: lower and upper flow bounds.
- $c_e$: additive unit cost on original arc $e$.
- $f_e$: flow on arc $e$.
- $c(f)=\sum_ec_ef_e$: total linear cost.
- **residual arc:** permitted incremental increase or decrease of original flow.
- **negative residual cycle:** feasible circulation change with negative unit objective change.
- $\pi(v)$: vertex potential.
- $c_\pi(u,v)=c(u,v)+\pi(u)-\pi(v)$: reduced cost.
- **excess / deficit:** remaining positive / negative imbalance during construction.
- **optimality certificate:** feasible flow plus potentials making every positive-capacity residual reduced cost nonnegative.

## Mechanisms, Invariants, or Proof Structure

Residual arcs encode every bound-respecting change, with reverse cost negated. Cycle augmentation preserves balances, and a negative cycle lowers cost. The difference of two equally balanced feasible flows is a residual circulation; cycle decomposition proves that any cheaper flow implies a negative residual cycle. Potentials telescope around cycles, so nonnegative residual reduced costs rule out every negative cycle. Successive shortest paths move excess to deficit while potential updates preserve nonnegative reduced costs. Lower-bound elimination shifts supplies and adds only a constant to the objective.

## Alternatives and Trade-Offs

- **Successive shortest paths:** intuitive, integral, and effective for modest shipped amounts; augmentation count may depend on numeric supply.
- **Cycle canceling:** mirrors the optimality theorem directly; naive negative-cycle selection can be slow.
- **Capacity or cost scaling:** improves worst-case behavior; requires more complex invariants and numeric care.
- **Network simplex:** often practical and exposes basis structure; worst-case and degeneracy behavior require attention.
- **Generic linear programming:** flexible and provides duals; may ignore exploitable network structure.
- **Exact integer/fixed-point arithmetic:** reproducible balances and certificates; requires scale and overflow proofs.
- **Floating arithmetic:** represents measured costs directly; weakens exact feasibility and reduced-cost tests.
- **Potentials certificate:** compact and linear-time to check after residual construction; does not prove model adequacy.
- **Full solver trace:** useful for diagnosis; larger and more coupled to implementation than final evidence.
- **Richer optimization model:** captures interactions and policies; may lose flow integrality and specialized algorithms.

## Failure Modes and Misconceptions

- Balanced total supply is necessary but not sufficient for feasibility.
- A negative original arc is not automatically an improving residual direction.
- Reverse residual cost must negate the original cost.
- Residual arcs with zero capacity cannot be used.
- A negative path does not preserve all balances; a residual cycle does.
- Dijkstra requires nonnegative reduced costs, not merely nonnegative original costs somewhere.
- Potentials are certificates only after every residual inequality is checked.
- Lower bounds change node supplies when shifted away.
- Integral data admits an integral optimum under the network model; arbitrary side constraints can destroy this property.
- Minimum cost at a fixed flow value differs from unconstrained minimum cost and from maximum flow.
- Infinite-capacity negative cycles can make cost unbounded; finite negative cycles merely invite bounded augmentation.
- Solver success does not validate units, snapshots, fairness, or real-system performance.

## Worked Examples

### Example 1

**Situation.** Supplies are $b(s)=5$, $b(t)=-4$, and all others zero. **Reasoning.** Their sum is one, but summing all balance equations must yield zero. **Conclusion.** The instance is infeasible before capacities or costs are considered.

### Example 2

**Situation.** Arc $a\to b$ has bounds $1\le f\le5$, cost three, and current flow four. **Reasoning.** Its forward residual has capacity one and cost three; its reverse has capacity three and cost negative three. **Conclusion.** The residual graph describes both the remaining increase and permissible cancellation above the lower bound.

### Example 3

**Situation.** A residual cycle costs $2-5+1=-2$ and has capacities $4,3,7$. **Reasoning.** Its bottleneck is three. Augmenting three units preserves balances and changes cost by $3(-2)=-6$. **Conclusion.** The feasible candidate was not optimal.

### Example 4

**Situation.** A residual graph has negative edges but supplied potentials make every reduced cost nonnegative. **Reasoning.** Potential terms telescope on cycles, so every cycle has the same nonnegative reduced and original total. **Conclusion.** Individual negative arcs do not contradict optimality.

### Example 5

**Situation.** A candidate flow costs 20, is feasible, and its smallest residual reduced cost is negative one. **Reasoning.** The potentials are not a valid certificate; the negative arc alone need not form a cycle. **Conclusion.** Reject the certificate, not necessarily the flow's optimality.

### Example 6

**Situation.** Lower bound two on $u\to v$ is removed. **Reasoning.** The fixed lower flow contributes net outflow two at $u$ and net inflow two at $v$. Adjust $b'(u)=b(u)-2$ and $b'(v)=b(v)+2$. **Conclusion.** Shifting capacity without shifting balances changes the feasible set.

### Example 7

**Situation.** A negative-cost cycle has total cost negative four and every arc capacity at most ten. **Reasoning.** At most the bottleneck can circulate before the residual structure changes. **Conclusion.** Negative cost implies improvement, not unboundedness, when capacity is finite.

### Example 8

**Situation.** Unit cost and capacity each fit signed 64-bit integers, but their product does not. **Reasoning.** Objective accumulation happens after multiplication; input-range checks on fields alone miss overflow. **Conclusion.** Prove bounds for products, path distances, potentials, and total sums or use wider arithmetic.

### Example 9

**Situation.** Two parallel arcs share endpoints but have costs one and five. **Reasoning.** Aggregating them into one capacity without a piecewise cost changes which units are cheap. Residual reverse arcs also need their originating identities. **Conclusion.** Endpoint pairs are not sufficient arc identity.

### Example 10

**Situation.** Shipping one extra unit increases congestion cost on every other unit. **Reasoning.** The objective is not a fixed sum $\sum c_ef_e$. **Conclusion.** Use a justified convex-cost or other richer model; linear minimum-cost-flow optimality does not apply unchanged.

## Cross-Program Connections

- **Data Structures Engineering:** residual multiarcs, priority queues, and stable identities determine performance and correctness.
- **Database Engineering:** snapshot isolation and checked units prevent certificates from validating stale or mixed data.
- **Systems Engineering:** supplies, lower commitments, penalties, and unserved-demand policy are requirements, not solver defaults.
- **Software Architecture:** separate feasibility, optimizer, certificate verifier, and publication boundaries.
- **Platform Engineering:** quotas and placement can resemble flow but often add failure domains and discrete policy constraints.
- **Security Engineering:** resource limits, overflow, NaN, oversized inputs, and certificate parsing are adversarial surfaces.

## References

1. R. K. Ahuja, T. L. Magnanti, and J. B. Orlin, *Network Flows: Theory, Algorithms, and Applications*, Prentice Hall, 1993, [MIT record](https://dspace.mit.edu/handle/1721.1/49424). Minimum-cost flow models, optimality, and algorithms.
2. A. V. Goldberg and R. E. Tarjan, “Finding Minimum-Cost Circulations by Canceling Negative Cycles,” *Journal of the ACM* 36(4), 1989, pp. 873–886, [doi:10.1145/76359.76368](https://doi.org/10.1145/76359.76368). Primary negative-cycle algorithm paper; retrieved 2026-09-05.
3. J. B. Orlin, “A Faster Strongly Polynomial Minimum Cost Flow Algorithm,” *Operations Research* 41(2), 1993, pp. 338–350, [doi:10.1287/opre.41.2.338](https://doi.org/10.1287/opre.41.2.338). Primary strongly polynomial algorithm paper; retrieved 2026-09-05.
4. A. Schrijver, *Combinatorial Optimization: Polyhedra and Efficiency*, Springer, 2003, [publisher record](https://link.springer.com/book/9783540443896). Flows, circulations, duality, and integrality.
5. J. Erickson, *Algorithms*, 1st ed., 2019, [author-hosted text](https://jeffe.cs.illinois.edu/teaching/algorithms/). Flow and shortest-path foundations; retrieved 2026-09-05.
6. Google, “Minimum Cost Flows,” OR-Tools documentation, updated 2026-03-18, [official documentation](https://developers.google.com/optimization/flow/mincostflow). Current interface, status, supply, capacity, cost, and result behavior; retrieved 2026-09-05.

## Exercises

### Exercise 1

State the minimum-cost transshipment model using net-outflow supply convention. Give all feasibility conditions and the linear objective.

### Exercise 2

An original arc $u\to v$ has lower bound two, capacity nine, cost negative three, and current flow six. Derive every residual arc. Then compute reduced costs using $\pi(u)=4$ and $\pi(v)=1$.

### Exercise 3

A service returns an “optimal” flow and total cost but no potentials. Design an independent verifier and distinguish what it can conclude about feasibility, objective accuracy, and optimality.

### Exercise 4

Compare successive shortest paths, cycle canceling, network simplex, and generic linear programming for an integral sparse network with large supplies and a requirement for independently checkable evidence.

### Exercise 5

A relief network moves two commodities that share vehicle capacity, has travel-time congestion, uncertain road availability, and priorities for underserved regions. Explain which minimum-cost-flow assumptions fail and propose a bounded model and evidence plan.

## Answers to the Exercises

### Answer 1

For each arc $e$, require $\ell_e\le f_e\le u_e$. For each vertex, require $\sum_{\delta^+(v)}f_e-\sum_{\delta^-(v)}f_e=b(v)$, where positive $b$ supplies and negative $b$ demands. Require finite declared vertices and arcs, coherent numeric units, $\ell_e\le u_e$, and $\sum_vb(v)=0$; the last is necessary but capacity cuts still determine actual feasibility. Minimize $\sum_ec_ef_e$. If values are integral, the standard network structure supports an integral optimum when feasible and bounded. Feasibility, boundedness, and optimality remain separate outcomes.

### Answer 2

Forward residual capacity is $9-6=3$ with cost $-3$. Reverse residual capacity is $6-2=4$ with cost $3$. Using $c_\pi(x,y)=c(x,y)+\pi(x)-\pi(y)$, the forward reduced cost is $-3+4-1=0$. The reverse reduced cost is $3+1-4=0$. Both directions being tight is expected for an original arc strictly between its lower and upper bounds. Stable identity must link the reverse residual arc to this original arc.

### Answer 3

Validate the snapshot schema, stable arc identities, endpoints, bounds, costs, supplies, and numeric domain. Recompute every arc-bound check and vertex balance; if they pass, the returned flow is feasible. Recompute $\sum c_ef_e$ with checked arithmetic; if it matches, the reported objective is accurate for that flow. Neither result proves optimality. To establish optimality, independently search the residual graph for a negative cycle or request potentials and check every positive-capacity residual reduced cost. A trusted solver status is operational evidence but not an independently checkable mathematical certificate. The result contract should carry the graph digest, flow, cost, potentials or explicit evidence gap, algorithm/version, status, and limitations.

### Answer 4

Successive shortest paths preserves integrality and has clear potential certificates, but large supplies can mean many augmentations unless scaling or larger bottleneck sends help. Cycle canceling matches the negative-cycle theorem and is easy to reason about, though naive cycle choice is slow. Network simplex is often effective on practical sparse networks and can expose dual potentials, but degeneracy and implementation behavior deserve measurement. Generic LP supplies mature status and dual facilities but may use more memory and ignore network-specialized speed. A sound choice benchmarks network simplex and a scaling shortest-path implementation, requires the final feasible-flow plus residual-potential certificate regardless of solver, and treats performance results as environment-specific.

### Answer 5

Two commodities violate single-commodity conservation because their arc usages couple through vehicle capacity. Congestion violates fixed linear separable unit costs. Road uncertainty violates the static deterministic snapshot, and regional priority adds policy or multiple objectives. A bounded plan can use a time-expanded multi-commodity linear or mixed-integer model over a finite scenario set, explicit shared-capacity constraints, piecewise-linear congestion approximations, and lexicographic objectives that first meet critical regional service floors and then minimize expected cost. Validate every scenario's conservation, shared capacities, service floors, and objective recomputation. Publish scenario/version digests, feasible routes, constraint residuals, solver bound and optimality gap, sensitivity cases, and excluded uncertainties. Do not present ordinary residual potentials as a certificate for the coupled integer model; use solver bounds plus independent feasibility checking and state the evidence limit.
