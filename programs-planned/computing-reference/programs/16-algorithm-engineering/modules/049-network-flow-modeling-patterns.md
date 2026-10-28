---
module_id: ALGE-049
program: Algorithm Engineering
level: 1
module_number: 49
title: Network-Flow Modeling Patterns
status: complete
last_verified: 2026-09-05
---

# Network-Flow Modeling Patterns

## One-Page Review

### Governing question

How can a domain constraint be translated into vertices, arcs, capacities, costs, and balances so that feasible flows correspond to valid domain solutions and optimal flow values answer the intended question?

### Essential definitions

- A **reduction** maps domain instances to flow instances and maps flow solutions back, while preserving feasibility and objective meaning.
- A **sound model** maps every accepted flow solution to a valid domain solution.
- A **complete model** can represent every domain solution that the specification intends to allow.
- A **super-source** or **super-sink** combines multiple supplies or demands through explicitly bounded arcs.
- **Vertex splitting** replaces capacity-limited vertex $v$ by $v_{in}\to v_{out}$ with the vertex capacity.
- A **circulation** has balances at all vertices and no privileged source-sink pair.
- A **lower-bound transformation** subtracts required flow and adjusts incident balances.
- An **infinite-capacity arc** is a logical implication implemented with a proved finite dominating bound or a solver-supported infinity.
- A **witness projection** turns positive-flow arcs back into domain assignments, paths, selections, or shipments.

### Central model, mechanism, or theorem

A modeling pattern is correct only after two directions are proved:

1. every valid domain solution constructs a feasible flow of the same objective value or decision outcome;
2. every relevant integral feasible flow projects to a valid domain solution with the corresponding value.

Max-flow/min-cut, integrality, and minimum-cost optimality apply only after this correspondence and all transformation assumptions are established.

### Critical invariants

- Units agree on every capacity, balance, and objective coefficient.
- Conservation represents the intended conservation law, not merely graph connectivity.
- Shared resources have one shared bottleneck arc rather than duplicated capacity.
- “At most,” “exactly,” and “at least” constraints use distinct constructions.
- Logical prohibition is absence or a hard constraint, not an arbitrary large cost.
- Integrality applies to the transformed network and survives projection.
- Input, transformed graph, solution, certificate, and projection share one revision.

### Common failures

Common failures include counting a shared quota once per path; reversing supply signs; confusing edge-disjoint with vertex-disjoint paths; forgetting lower-bound balance adjustments; allowing flow to split when the domain object must remain indivisible; using a weak big-$M$ capacity; losing parallel-arc identity; extracting assignments without checking conservation; maximizing throughput when policy required serving every demand; and interpreting a mathematical cut as a causal operational diagnosis.

### Compact example

A team may accept at most two tasks across all its workers. Giving each worker capacity two permits excessive aggregate use. Instead, route source flow through one team bottleneck arc of capacity two before it reaches individual worker vertices. Every downstream unit consumes the shared quota exactly once.

### Connections

[ALGE-041](./041-flow-networks-and-residual-graphs.md) defines the mechanism, [ALGE-045](./045-max-flow-min-cut-theorem.md) supplies certificates, and [ALGE-048](./048-minimum-cost-flow.md) adds balances and costs. [ALGE-050](../ROADMAP.md#block-05--flows-matching-and-combinatorial-optimization) develops the broader process of turning a domain problem into a graph optimization problem.

## Governing Question

For a proposed network-flow encoding, what must be proved and validated so that a feasible or optimal graph solution is genuinely a solution to the original domain problem rather than an artifact of missing constraints, duplicated capacity, or incorrect units?

Flow algorithms are reusable because many constraints share conservation and capacity structure. That reuse is safe only when the transformation is treated as a proof obligation. A solver can be perfectly correct on a graph that answers the wrong question.

## Why This Matters

Real applications rarely arrive already labeled with $s$, $t$, and capacities. They mention people, machines, quotas, routes, dependencies, commitments, and penalties. Modeling translates those nouns and rules into mathematical structure. Most severe optimization failures occur here: the result passes algorithmic checks but violates an unstated or mistranslated requirement.

Patterns help because they package known correspondences. They do not eliminate judgment. Each use must state domain identities, units, multiplicities, time semantics, objective priority, and excluded effects. A certificate validates the encoded instance, while a separate projection audit validates its connection to the domain.

## Prerequisites and Retrieval

Retrieve directed multigraphs, conservation, integral flows, cuts, residual graphs, bipartite matching, lower bounds, supplies and demands, additive costs, and proof by two-way construction. Review [ALGE-045](./045-max-flow-min-cut-theorem.md), [ALGE-046](./046-bipartite-matching.md), and [ALGE-048](./048-minimum-cost-flow.md).

## Learning Objectives

After completing this module, you should be able to:

1. state soundness, completeness, and objective-preservation obligations;
2. combine multiple sources and sinks without inventing capacity;
3. encode shared quotas and vertex capacities;
4. model bipartite allocation, disjoint paths, circulation, and lower bounds;
5. choose between hard constraints, penalties, and lexicographic objectives;
6. derive safe finite substitutes for logical infinity;
7. project integral flow back to auditable domain objects;
8. validate transformation and projection independently;
9. identify violated flow assumptions; and
10. publish model, solver, certificate, and policy evidence separately.

## Core Exposition

### Treat a reduction as a contract

Let domain instance $I$ map to network $N(I)$. A complete reduction specifies:

- which domain entity owns each vertex and arc;
- what one unit of flow means;
- what capacities, lower bounds, balances, and costs mean;
- how a domain solution maps to flow;
- how an integral flow maps back to a domain witness;
- how objective values or yes/no decisions correspond;
- which assumptions make the correspondence valid.

**Soundness** forbids false positives: every projected accepted flow obeys the domain rules. **Completeness** forbids false negatives: every intended valid domain solution has a corresponding flow. **Objective preservation** ensures that comparing flow solutions compares the intended domain quantity. Prove all applicable directions before invoking an algorithm theorem.

### Combine multiple sources and sinks

For source vertices $s_i$ with maximum supplies $a_i$, introduce super-source $S$ and arcs $S\to s_i$ of capacity $a_i$. For sinks $t_j$ with maximum intake $d_j$, add $t_j\to T$ of capacity $d_j$. A maximum $S$-$T$ flow then respects each local limit.

An unbounded connector silently changes the model if the domain source has finite supply. Conversely, using current expected volume rather than maximum capacity may reject legitimate solutions. If every demand must be satisfied exactly, max flow alone is insufficient: require total value $\sum_jd_j$, use balances, or validate saturation of every demand arc.

Super nodes are transformations, not domain facilities. Exclude their artificial arcs when publishing physical bottlenecks, or clearly label them as supply/demand constraints.

### Encode vertex and shared-resource capacity

Ordinary flow capacity belongs to arcs. To limit total flow through vertex $v$ to $k$, replace it with $v_{in}$ and $v_{out}$, redirect incoming arcs to $v_{in}$, redirect outgoing arcs from $v_{out}$, and add $v_{in}\to v_{out}$ of capacity $k$. Every traversal consumes the bottleneck once.

The same pattern handles a quota shared by many choices. Route all relevant units through one quota arc. Do not copy the quota onto each choice: that permits the aggregate to exceed it. If a resource is consumed only by certain transitions or time intervals, place the bottleneck at the narrowest structure traversed exactly once by each consumption.

Vertex splitting changes path representation. Projection must collapse the pair and reject flows that use internal transformation arcs without a valid original traversal.

### Model one-to-one and capacitated allocation

For one-to-one assignment, add source-to-agent capacity one, admissible agent-to-task capacity one, and task-to-sink capacity one. Integral maximum flow projects to a matching. Agent or task capacities greater than one produce a capacitated bipartite allocation, provided each unit is interchangeable and splitting an entity's allocation is allowed.

Add costs to admissible arcs for additive preferences and solve minimum-cost flow at a required cardinality. If maximizing served count has priority over cost, use a lexicographic process: first determine maximum flow $F$, then minimize cost subject to value $F$. A single blended penalty preserves that priority only with a proved dominance bound and safe arithmetic.

### Represent path-disjointness precisely

With unit arc capacities, an integral $s$-$t$ flow of value $k$ decomposes into $k$ edge-disjoint paths plus possible cycles; remove cycles during projection. This represents edge-disjointness, not vertex-disjointness. For internally vertex-disjoint paths, split each nonterminal vertex with capacity one.

If physical links are undirected but capacity is shared across both directions, replacing each link with two independent directed arcs can double usable capacity. Use a gadget or a solver model that enforces one shared bidirectional bound. State whether opposite directions may simultaneously consume separate capacity.

### Use circulation for balances and commitments

A circulation model assigns balances $b(v)$ and arc bounds. It naturally represents multiple producers and consumers. Lower bounds encode mandatory commitments, but shifting them away changes balances:

$$
b'(v)=b(v)-\left(\sum_{\delta^+(v)}\ell_e-\sum_{\delta^-(v)}\ell_e\right).
$$

Feasibility can be reduced to max flow with a super-source connected to deficit/excess nodes under one consistent sign convention. A saturating auxiliary flow proves the transformed balances can be met. Recover the lower-bound flow before projection and validate the original equations, not only the transformed ones.

To turn a required $s$-$t$ flow into a circulation, one common construction adds $t\to s$ with an appropriate lower bound or fixes source and sink balances. The exact choice depends on whether value is fixed, bounded, or optimized; do not treat these formulations as interchangeable.

### Encode implications with dominating capacity

Maximum-closure-style models use a source arc for positive benefit, a sink arc for negative benefit, and an implication arc $u\to v$ meaning selecting $u$ requires selecting $v$. The implication arc must be too expensive for a minimum cut to cross. A finite value $M$ is safe only when it strictly exceeds a proved upper bound on every finite cut of interest, such as one plus the sum of all finite nonnegative capacities, with overflow checked.

This is a hard logical constraint expressed through cut capacity, not a penalty preference. If no safe representable $M$ exists, use explicit solver infinity or another formulation. Document the bound derivation so later cost growth cannot silently invalidate it.

### Separate hard constraints and soft costs

A forbidden action should be absent or structurally impossible. A soft undesirable action may receive a cost reflecting an explicit trade-off. Turning a hard rule into a large penalty permits violation whenever competing costs become larger. Turning a preference into a prohibition can make a useful instance infeasible.

Multiple objectives need an ordering. Lexicographic optimization solves and freezes higher-priority optima before optimizing the next criterion. A weighted sum matches that order only if weight bounds dominate all lower-priority variation. Costs also need coherent units; dollars, milliseconds, risk points, and fairness scores do not add themselves.

### Project flows into domain witnesses

Integral flow can still contain circulations unrelated to delivered value. Decompose positive flow into source-sink paths and cycles, discard zero-cost or nonbeneficial cycles only when doing so preserves the intended objective and constraints, and map every path through transformation gadgets back to a domain object.

Projection should be deterministic where possible and should retain provenance: original vertex/arc IDs, quantity, cost contribution, and transformation path. After projection, revalidate domain rules directly. Do not infer them merely because the transformed graph was feasible.

### Reproduce a shared-quota model

The following program constructs a bipartite allocation with two group bottlenecks. Group 1 contains workers A and B but may accept at most one task; group 2 contains C and may accept one. A deterministic augmenting-flow routine finds two assignments and verifies an equal-capacity cut.

<!-- bijux-verify: {"id":"shared-quota-flow-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"max_flow=2\nassignments=(('A', 'X'), ('C', 'Y'))\nquota_usage={'g1': 1, 'g2': 1}\ncut_capacity=2 certificate=True\n","stderr":""}} -->
```python
from collections import deque

capacities = {}


def add_arc(u, v, capacity):
    capacities[(u, v)] = capacity
    capacities.setdefault((v, u), 0)


add_arc("s", "g1", 1)
add_arc("s", "g2", 1)
for group, worker in (("g1", "A"), ("g1", "B"), ("g2", "C")):
    add_arc(group, worker, 1)
for worker, task in (("A", "X"), ("A", "Y"), ("B", "X"), ("C", "Y")):
    add_arc(worker, task, 1)
for task in ("X", "Y"):
    add_arc(task, "t", 1)

flow = {edge: 0 for edge in capacities}


def augment():
    parent = {"s": None}
    queue = deque(["s"])
    while queue and "t" not in parent:
        u = queue.popleft()
        for a, v in capacities:
            if a == u and v not in parent and flow[(a, v)] < capacities[(a, v)]:
                parent[v] = u
                queue.append(v)
    if "t" not in parent:
        return 0
    v = "t"
    while parent[v] is not None:
        u = parent[v]
        flow[(u, v)] += 1
        flow[(v, u)] -= 1
        v = u
    return 1


value = 0
while augment():
    value += 1

assignments = tuple(
    (worker, task)
    for worker, task in (("A", "X"), ("A", "Y"), ("B", "X"), ("C", "Y"))
    if flow[(worker, task)] == 1
)
quota_usage = {group: flow[("s", group)] for group in ("g1", "g2")}
source_side = {"s"}
cut_capacity = sum(
    capacity
    for (u, v), capacity in capacities.items()
    if u in source_side and v not in source_side
)

print(f"max_flow={value}")
print(f"assignments={assignments}")
print(f"quota_usage={quota_usage}")
print(f"cut_capacity={cut_capacity} certificate={value == cut_capacity}")
```

The cut containing only the source crosses both group-quota arcs and upper-bounds throughput by two. The feasible integral assignment attains two. This certifies the transformed graph; direct projection checks still establish worker/task uniqueness and group ownership.

### Validate the transformation as a separate layer

Use three schemas: canonical domain input, normalized network, and projected result. Bind them with digests and version the transformation. Validate:

1. all domain entities and rules were represented;
2. all generated vertices/arcs have traceable ownership;
3. units, signs, bounds, costs, and dominating constants are valid;
4. the solver result and mathematical certificate validate on the network;
5. the projected witness validates directly against the original domain snapshot.

Property-based tests can enumerate tiny domain instances, compare a direct oracle with the flow model, and shrink counterexamples. Metamorphic tests can permute IDs, add irrelevant zero-capacity arcs, or scale all compatible units and check expected invariance. These tests support the reduction proof but do not replace it.

### Know when flow is the wrong abstraction

Ordinary flow permits divisible units and uses local conservation plus separable arc bounds/costs. It is unsuitable without extension when objects are indivisible but capacities exceed one, commodities share arcs, choices have fixed activation costs, costs depend on combinations, resources persist across time, or uncertainty and fairness create global constraints.

Some cases admit flow gadgets or time-expanded networks, but expansion size and proof burden may become unacceptable. Choose integer programming, constraint programming, dynamic programming, or a specialized algorithm when it matches the domain more honestly.

## Definitions and Notation

- **domain instance:** authoritative entities, constraints, units, and objective.
- **network instance:** generated vertices, arcs, bounds, balances, and costs.
- **soundness:** every accepted network witness projects to a valid domain witness.
- **completeness:** every intended domain witness has a network representation.
- **objective preservation:** mapped solutions retain the intended ordering or value.
- **gadget:** bounded subnetwork implementing one domain constraint.
- **super-source / super-sink:** artificial aggregation terminal.
- **vertex splitting:** in/out pair joined by a capacity arc.
- **projection:** reconstruction of domain objects from flow.
- **dominating bound:** proved finite value that makes crossing a logical arc suboptimal.

## Mechanisms, Invariants, or Proof Structure

A correct model starts with units and conservation, encodes every shared resource exactly once, and proves soundness, completeness, and objective preservation by two-way construction. Super terminals aggregate bounded supply and demand; vertex splitting turns node limits into arc limits; unit capacities plus integrality yield discrete assignments or paths; circulations express balances and lower commitments; dominating arcs encode implications only under proved bounds. Solver certificates validate the network, while projection validation independently checks the original domain rules.

## Alternatives and Trade-Offs

- **Direct domain algorithm:** avoids transformation overhead; may lack mature certificates or reusable infrastructure.
- **Flow reduction:** inherits polynomial algorithms and integrality; requires a rigorous correspondence proof.
- **Super terminals:** simplify multiple endpoints; can obscure physical versus artificial bottlenecks.
- **Vertex splitting:** exact for throughput limits; expands the graph and complicates projection.
- **Hard structural exclusion:** preserves policy; may create infeasibility that must be reported honestly.
- **Soft penalty:** supports trade-offs; cannot enforce a hard rule without a dominance proof.
- **Lexicographic solves:** preserve priority exactly; require multiple solves or specialized support.
- **Weighted objective:** one solve; weights and overflow bounds become proof obligations.
- **Time expansion:** restores local conservation across time; graph size can grow prohibitively.
- **Integer programming:** represents global logical constraints; may sacrifice flow integrality and compact optimality certificates.

## Failure Modes and Misconceptions

- A solver theorem proves properties of the generated graph, not correctness of its generation.
- Super-source arcs need real supply bounds.
- Max flow does not require each demand to be satisfied unless value or saturation is checked.
- Per-choice copies of a shared quota do not enforce an aggregate limit.
- Unit edge capacities encode edge-disjointness, not vertex-disjointness.
- Two directed arcs may double an undirected shared capacity.
- Lower-bound elimination must adjust balances and restore flows before projection.
- Big-$M$ requires a strict, overflow-safe dominance proof.
- Integral flow does not make a divisible domain object indivisible automatically.
- Positive flow can include cycles that are not domain paths.
- Minimum cut membership does not establish unique real-world causality.
- Penalties, fairness, and objective priorities are policy, not incidental solver parameters.

## Worked Examples

### Example 1

**Situation.** Two warehouses supply three and five units. **Reasoning.** Super-source arcs with capacities three and five cap total injected flow at eight and preserve each warehouse limit. **Conclusion.** An infinite connector would invent supply.

### Example 2

**Situation.** Three machines share a power feed of capacity four. **Reasoning.** Routing every machine path through one feed arc of capacity four enforces the aggregate. Giving each machine capacity four permits twelve. **Conclusion.** Shared resources require a shared bottleneck.

### Example 3

**Situation.** Two routes must share no intermediate location. **Reasoning.** Unit road capacities prevent edge reuse but allow both paths through different roads at one vertex. Split every nonterminal location with an internal capacity-one arc. **Conclusion.** Vertex-disjointness needs vertex capacity.

### Example 4

**Situation.** Every customer arc to the super-sink has capacity one and max flow equals the number of customers. **Reasoning.** The total value forces all those arcs to saturate. **Conclusion.** This equality certifies complete service; merely computing an unspecified max flow does not.

### Example 5

**Situation.** A contract requires two units on $u\to v$. **Reasoning.** Subtract the lower flow, reduce residual capacity, and shift $u$'s adjusted supply down two and $v$'s up two. **Conclusion.** A lower bound is both an arc and a balance transformation.

### Example 6

**Situation.** Finite cut capacities sum to at most 900 and an implication arc receives capacity 901. **Reasoning.** Any cut crossing the implication costs more than a finite alternative, so an optimum respects it, assuming checked exact arithmetic. **Conclusion.** The logical arc is safe because its dominance bound is proved.

### Example 7

**Situation.** Throughput is worth priority over every cost improvement, but the model minimizes `cost - 100*flow`. **Reasoning.** If total cost variation can exceed 100, the solver may sacrifice a unit of throughput. **Conclusion.** Use lexicographic optimization or prove a larger safe weight.

### Example 8

**Situation.** An integral flow of value two includes a positive-flow cycle. **Reasoning.** Flow decomposition separates two source-sink paths and the circulation. Removing the cycle preserves value but may change cost if it is nonzero. **Conclusion.** Projection must handle cycles with objective awareness.

### Example 9

**Situation.** An undirected cable carries ten total, but the model uses two directed capacity-ten arcs. **Reasoning.** It permits ten in each direction simultaneously. **Conclusion.** Direction expansion duplicated a shared physical limit.

### Example 10

**Situation.** A placement flow satisfies capacities but assigns replicas to one failure domain. **Reasoning.** Ordinary conservation contains no anti-affinity or correlated-failure rule. **Conclusion.** Add a proven failure-domain gadget or use a richer constraint model.

## Cross-Program Connections

- **Systems Engineering:** requirements decide hard rules, allowed trade-offs, units, and acceptance evidence.
- **Software Architecture:** domain compiler, solver, certificate checker, and projector are distinct responsibilities.
- **Database Engineering:** immutable snapshots and provenance bind domain rows to generated arcs.
- **Platform Engineering:** quotas, placement, failure domains, and temporal reservations test flow-model boundaries.
- **Security Engineering:** dominating constants, overflow, untrusted identifiers, and resource exhaustion require validation.
- **API Engineering:** result schemas should separate domain witness, network certificate, status, and limitations.

## References

1. R. K. Ahuja, T. L. Magnanti, and J. B. Orlin, *Network Flows: Theory, Algorithms, and Applications*, Prentice Hall, 1993, [MIT record](https://dspace.mit.edu/handle/1721.1/49424). Network transformations, circulations, costs, and applications.
2. L. R. Ford Jr. and D. R. Fulkerson, “Maximal Flow Through a Network,” *Canadian Journal of Mathematics* 8, 1956, pp. 399–404, [doi:10.4153/CJM-1956-045-5](https://doi.org/10.4153/CJM-1956-045-5). Primary flow and cut result; retrieved 2026-09-05.
3. T. H. Cormen, C. E. Leiserson, R. L. Rivest, and C. Stein, *Introduction to Algorithms*, 4th ed., MIT Press, 2022, [publisher record](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/). Flow algorithms and standard reductions.
4. A. Schrijver, *Combinatorial Optimization: Polyhedra and Efficiency*, Springer, 2003, [publisher record](https://link.springer.com/book/9783540443896). Flow, matching, integrality, and reductions.
5. J. Erickson, *Algorithms*, 1st ed., 2019, [author-hosted text](https://jeffe.cs.illinois.edu/teaching/algorithms/). Reductions, flows, cuts, and modeling examples; retrieved 2026-09-05.
6. Google, “Network Flows” and “Minimum Cost Flows,” OR-Tools documentation, updated 2026-03-18, [official documentation](https://developers.google.com/optimization/flow). Current solver-family boundaries and examples; retrieved 2026-09-05.

## Exercises

### Exercise 1

Define soundness, completeness, and objective preservation for a reduction. Explain why solver correctness establishes none of them by itself.

### Exercise 2

Model two internally vertex-disjoint paths from $s$ to $t$ in a directed graph. State the construction, flow target, projection, and proof obligations.

### Exercise 3

A model gives every worker an arc of capacity three although workers share a team quota of three. Diagnose the defect, correct the network, and specify direct projection checks.

### Exercise 4

Compare hard exclusion, big-$M$ implication arcs, soft penalties, and lexicographic objectives for representing policy rules.

### Exercise 5

A cloud placement service has replica demand, host capacities, rack anti-affinity, time-varying reservations, and a cost for cross-zone traffic. Propose the closest bounded flow-based model, state what cannot be represented honestly, and define evidence for deployment.

## Answers to the Exercises

### Answer 1

Soundness means every accepted feasible or optimal flow projects to a domain solution satisfying all authoritative rules. Completeness means every domain solution intended to be allowed maps to a feasible flow. Objective preservation means mapped solutions retain the intended value or ordering. A correct solver proves feasibility or optimality only for the generated vertices, arcs, bounds, balances, and costs. It cannot show that generation omitted no rule, invented no solution, used correct units, or projected correctly. Those claims need two-way construction proofs, transformation tests, traceable identities, and direct domain validation.

### Answer 2

For every nonterminal vertex $v$, create $v_{in}\to v_{out}$ with capacity one. Redirect each original incoming edge to $v_{in}$ and each outgoing edge from $v_{out}$; give transformed original arcs capacity one or a sufficient bound. Leave $s,t$ unsplit, then seek integral max flow of value at least two. Decompose the flow into two $s$-$t$ paths, remove cycles, and collapse in/out pairs. Soundness follows because both paths would have to use the same internal capacity-one arc to share a vertex. Completeness follows by mapping two domain-disjoint paths through distinct internal arcs. Validate original edge existence, path continuity, distinct internal vertices, value two, and the flow/cut certificate.

### Answer 3

Per-worker capacity three permits each worker to use three units, so aggregate use can exceed the team quota. Add one team bottleneck: source to team with capacity three, then team to each worker with capacity no greater than the worker's own limit. Every assignment path must traverse the team arc exactly once. Projection extracts positive worker-to-task arcs, then directly checks task uniqueness or capacity, worker limits, worker-team ownership, and total assignments per team at most three. The certificate proves transformed maximum flow; these direct checks prove projection soundness for the snapshot.

### Answer 4

Hard exclusion removes an arc or otherwise makes a choice infeasible; use it for rules that may never be violated. A big-$M$ implication arc also encodes a hard rule through cut cost, but only when $M$ strictly dominates every relevant finite cut under checked arithmetic and future bounds. A soft penalty permits violation at an explicit trade-off and must use meaningful units. Lexicographic optimization first fixes a higher-priority optimum, then optimizes lower priorities, preserving ordering without delicate weights. Choose from requirement semantics: never silently replace a hard rule with a penalty or a preference with a prohibition.

### Answer 5

For one static interval, a flow model can send one unit per replica through service, optional rack-quota, host, and sink layers; host arcs encode capacity and admissible arcs encode compatibility. Cross-zone cost can be additive on placement arcs. Rack anti-affinity for each service requires service-specific rack bottlenecks, which can greatly expand the graph. Time-varying reservations require a finite time-expanded network with carryover and interval capacities. If replicas are indivisible with heterogeneous resource vectors, or anti-affinity and reservations couple arbitrary choices, ordinary scalar flow is not honest; use integer or constraint programming. Before deployment validate every replica, resource dimension, host and rack rule, time interval, and cost directly; bind input/network/projection digests; report feasible placement, unmet demand, objective, certificate or solver bound/gap, version, limits, scenario tests, and excluded failure correlations.
