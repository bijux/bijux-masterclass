---
module_id: ALGE-064
program: Algorithm Engineering
level: 2
module_number: 64
title: Primal-Dual Approximation
status: complete
last_verified: 2026-09-05
---

# Primal-Dual Approximation

## One-Page Review

### Governing question

How can an algorithm construct a feasible combinatorial solution and a dual lower bound together, using tightness to decide what to buy and a charging argument to prove an approximation factor without first solving the linear program?

### Essential definitions

- The **primal** relaxation describes fractional purchases that cover demands; its **dual** prices those demands subject to resource budgets.
- **Weak duality** says every dual-feasible value is at most every primal-feasible value for a minimization primal.
- A primal constraint is **covered** when the constructed discrete solution satisfies it.
- A dual constraint is **tight** when its left side equals its budget.
- **Dual growth** raises selected demand prices while preserving every dual constraint.
- A **witness** records which tight event justified a primal choice.
- **Reverse deletion** removes choices in reverse order when feasibility survives, reducing overbuying without invalidating the lower bound.
- A **charging bound** limits how often one unit of dual value is counted in the primal cost.

### Central model, mechanism, or theorem

For weighted vertex cover, the relaxation and dual are

$$
\min\sum_{v\in V}w_vx_v\quad\text{s.t. }x_u+x_v\ge1,
\qquad
\max\sum_{e\in E}y_e\quad\text{s.t. }\sum_{e\ni v}y_e\le w_v.
$$

While an edge is uncovered, raise its $y_e$ until an endpoint budget becomes tight and select every newly tight endpoint. Dual feasibility is preserved and every processed edge becomes covered. If $C$ is the selected cover,

$$
w(C)=\sum_{v\in C}\sum_{e\ni v}y_e
\le 2\sum_{e\in E}y_e
\le 2OPT,
$$

because each edge price is counted by at most two selected endpoints and the dual is a lower bound.

### Critical invariants

- All dual variables remain nonnegative and all dual budget constraints remain feasible.
- Growth is limited by the minimum residual slack of every resource affected by the active demands.
- Every committed primal object has a tightness witness under the same dual state.
- Processed demands are covered, or remain represented in an explicitly active component.
- Cleanup removes objects only after checking original feasibility.
- The cost-to-dual charging multiplicity matches the proved factor.
- Arithmetic, event ties, and concurrent growth follow a deterministic or explicitly analyzed policy.

### Common failures

Common failures include confusing LP duality with two unrelated heuristics; raising a dual variable past a budget; buying merely almost-tight objects; counting dual value more times than the proof permits; using complementary slackness as if an integral optimum had been found; applying a set-cover frequency bound to unbounded frequency; cleaning up in an order not covered by the argument; hiding numeric slack; processing stale residuals concurrently; and reporting a dual bound that belongs to a different normalized or preprocessed model.

### Compact example

For one unit-cost edge, raise its price from zero to one. Both endpoint constraints become tight, so a simple rule may select both endpoints. The primal cost is two; the dual value is one; optimum cost is one. Weak duality and double counting prove the factor two exactly, even though the constructed cover is not optimal.

### Connections

[ALGE-063](./063-linear-programming-rounding.md) rounds a solved relaxation. This chapter instead constructs primal and dual objects together. [ALGE-065](../ROADMAP.md#block-07--approximation-heuristics-and-randomized-algorithms) improves solutions through neighborhoods. Network Engineering owns deployed topology semantics; Data Architecture owns optimization-model provenance.

## Governing Question

Given a covering or network-design problem, how do we derive its dual, choose safe dual-growth events, translate tight constraints into a feasible discrete object, and bind the returned cost to a verifiable lower-bound certificate?

Primal-dual approximation is not simply “look at both LPs.” It is an algorithm-design discipline. The dual identifies scarce budgets, tightness supplies events, the primal construction restores integral feasibility, and a separate charging lemma bounds how many times dual value pays for the chosen objects.

## Why This Matters

Solving a large LP and rounding it can be expensive or operationally awkward. A combinatorial primal-dual algorithm may avoid a general solver, expose a replayable event trace, and produce its lower bound during construction. The method has classical applications in covering, facility location, network design, scheduling, and online algorithms.

The attractive implementation story can conceal proof obligations. A feasible solution alone has no approximation certificate. A feasible dual alone is only a lower bound. Tight objects can still overlap too much, causing unlimited charging multiplicity. Floating residuals, simultaneous events, preprocessing, and cleanup can sever the association between the two sides.

The durable engineering skill is to treat primal feasibility, dual feasibility, and cost charging as independently checked artifacts that are linked by stable identifiers and exact model semantics.

## Prerequisites and Retrieval

Retrieve [ALGE-061](./061-approximation-ratios-and-guarantees.md), [ALGE-062](./062-greedy-approximation.md), [ALGE-063](./063-linear-programming-rounding.md), linear-program duality, weak duality, complementary slackness, weighted vertex cover, set cover, graph cuts, and exact rational arithmetic.

This chapter derives the weighted-vertex-cover method and generalizes its design pattern to bounded-frequency cover and network growth. It distinguishes primal-dual construction from dual fitting and Lagrangian relaxation. Detailed facility-location and survivable-network algorithms remain examples of the schema rather than replacement courses on those domains.

## Learning Objectives

After completing this module, you should be able to:

1. derive a covering LP dual with correct inequality directions and signs;
2. interpret dual variables as demand prices and constraints as resource budgets;
3. prove weak-duality lower bounds used by an approximation certificate;
4. implement safe event-driven dual growth using residual slack;
5. derive the weighted-vertex-cover factor-two charging proof;
6. generalize charging to bounded-frequency covering;
7. distinguish primal-dual construction, dual fitting, and LP rounding;
8. analyze reverse deletion and other cleanup without losing feasibility;
9. preserve dual certificates through arithmetic, concurrency, and preprocessing; and
10. publish a result whose primal object, dual bound, trace, and factor can be independently checked.

## Core Exposition

### Derive the pair before designing events

Consider a covering relaxation in canonical form:

$$
\min c^Tx\quad\text{subject to }Ax\ge\mathbf1,\quad x\ge0,
$$

where $A\ge0$ and $c\ge0$. Its dual is

$$
\max \mathbf1^Ty\quad\text{subject to }A^Ty\le c,\quad y\ge0.
$$

Each primal variable buys an object of cost $c_j$. Each primal row is a demand. Dual variable $y_i$ prices demand $i$, and object $j$ can absorb total price at most $c_j$ from demands it serves. For any feasible $x,y$,

$$
\mathbf1^Ty\le y^TAx=x^TA^Ty\le c^Tx,
$$

which proves weak duality using the signs and constraint directions. A dual-feasible value is therefore a lower bound on the integer optimum because every integer solution is also primal-LP feasible.

Derive this pair from the actual model. Equality rows create unrestricted dual variables; upper bounds add dual terms; maximization reverses the certificate direction. Units are a useful check: if primal costs are currency, dual demand prices and every summed resource budget must also be currency.

### Grow duals by the next tight event

Start from $y=0$, which is feasible for nonnegative covering costs. Select one uncovered demand or an active family of demands and increase their prices uniformly or at declared rates. For each affected object, calculate residual slack

$$
s_j=c_j-\sum_i A_{ij}y_i.
$$

The next safe event is the minimum nonnegative time until some affected slack reaches zero. Advance by exactly that amount, declare the corresponding constraints tight, and make the primal choice prescribed by the algorithm. Zero-slack events must be drained before positive time advances, or the state machine may skip choices or loop.

Uniform growth is not universal. Some network algorithms grow moats around active components; facility-location algorithms combine facility and connection events. The rate vector, active-set definition, and tie handling are part of the proof. An event queue is valid only when stale predicted times are revalidated against current residuals.

### Derive weighted vertex cover

For graph $G=(V,E)$ with $w_v\ge0$, the primal buys vertices and the dual packs edge prices into endpoint budgets:

$$
\begin{aligned}
\min &\sum_vw_vx_v & x_u+x_v&\ge1 &&(uv\in E),\\
\max &\sum_ey_e & \sum_{e\ni v}y_e&\le w_v &&(v\in V).
\end{aligned}
$$

Process an uncovered edge $e=uv$. Its endpoints have residuals $r_u,r_v$. Raise $y_e$ by $\delta=\min(r_u,r_v)$. At least one endpoint becomes tight; select every endpoint that becomes tight. The edge is now covered. Prices never decrease, selected vertices remain selected, and every later processed edge is covered when its event ends. With finite edges and at least one new tight endpoint for each uncovered event, the implementation terminates.

The executable model uses integer weights, so residual arithmetic is exact. Its deterministic edge order is behavior, not a premise of the factor-two proof.

<!-- bijux-verify: {"id":"weighted-vertex-cover-primal-dual","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"single chosen=(0, 1) cost=2 dual=1 optimum=(0,) optimum_cost=1\npath chosen=(0, 1, 2, 3) cost=4 dual=2 optimum=(0, 2) optimum_cost=2\nweighted chosen=(0, 1) cost=5 dual=3 optimum=(0, 1) optimum_cost=5\n","stderr":""}} -->
```python
from itertools import combinations


def primal_dual_cover(vertices, edges, weights):
    residual = dict(weights)
    chosen = set()
    dual = {edge: 0 for edge in edges}
    for edge in edges:
        u, v = edge
        if u in chosen or v in chosen:
            continue
        delta = min(residual[u], residual[v])
        dual[edge] += delta
        residual[u] -= delta
        residual[v] -= delta
        if residual[u] == 0:
            chosen.add(u)
        if residual[v] == 0:
            chosen.add(v)
    assert all(u in chosen or v in chosen for u, v in edges)
    return tuple(sorted(chosen)), sum(weights[v] for v in chosen), sum(dual.values())


def exact_cover(vertices, edges, weights):
    candidates = []
    for size in range(len(vertices) + 1):
        for subset in combinations(vertices, size):
            if all(u in subset or v in subset for u, v in edges):
                candidates.append((sum(weights[v] for v in subset), subset))
    return min(candidates)


cases = {
    "single": ((0, 1), ((0, 1),), {0: 1, 1: 1}),
    "path": ((0, 1, 2, 3), ((0, 1), (1, 2), (2, 3)), {v: 1 for v in range(4)}),
    "weighted": ((0, 1, 2), ((0, 1), (0, 2), (1, 2)), {0: 2, 1: 3, 2: 4}),
}
for name, (vertices, edges, weights) in cases.items():
    chosen, cost, dual = primal_dual_cover(vertices, edges, weights)
    optimum_cost, optimum = exact_cover(vertices, edges, weights)
    print(
        f"{name} chosen={chosen} cost={cost} dual={dual} "
        f"optimum={optimum} optimum_cost={optimum_cost}"
    )
```

### Prove the factor by bounded charging

Every selected vertex is tight, hence $w_v=\sum_{e\ni v}y_e$. Therefore

$$
\begin{aligned}
w(C)
&=\sum_{v\in C}w_v
=\sum_{v\in C}\sum_{e\ni v}y_e\\
&=\sum_{e\in E}y_e\,|e\cap C|
\le2\sum_{e\in E}y_e
\le2OPT.
\end{aligned}
$$

The first equality consumes tightness of selected vertices. The regrouping is finite double counting. The factor two comes from an edge having two endpoints, not from weak duality. The last inequality consumes dual feasibility. This decomposition matters: if code selects a non-tight vertex, the first equality fails; if a generalized demand touches many chosen objects, the factor changes; if growth overshoots, the last inequality fails.

Complementary slackness would characterize simultaneous primal and dual LP optima under stronger conditions. Here tightness guides an integral approximation but does not prove optimality. The one-edge example deliberately selects both endpoints and realizes factor two.

### Generalize to bounded-frequency covering

For set cover, a primal variable corresponds to set $S$ of cost $c_S$ and a dual variable to element $e$:

$$
\min\sum_Sc_Sx_S,
\qquad
\max\sum_ey_e\quad\text{s.t. }\sum_{e\in S}y_e\le c_S.
$$

Raise an uncovered element price until one or more containing sets become tight, then choose according to the declared rule. If every element belongs to at most $f$ chosen tight sets, the same double count gives cost at most $f\sum_ey_e\le fOPT$. The proof needs frequency among chosen sets, not merely total input frequency if cleanup or simultaneous events change selection.

This schema can be weak: $f$ may be enormous. Set cover's logarithmic greedy guarantee from ALGE-062 can be better. A technique is selected by the formulation and structural bound, not by aesthetic preference.

### Use cleanup without erasing the proof

Straightforward growth may select redundant objects. Reverse deletion scans them in reverse selection order and removes an object when all original demands remain covered. Feasibility is checked after each deletion, so cleanup cannot increase cost and the pre-cleanup approximation inequality still upper-bounds the result.

Stronger analyses sometimes need cleanup to establish the charging factor itself—for example, to prove a forest has bounded average degree or that each active component is charged only a limited number of times. Then arbitrary order is unsafe. The proof must show which witnesses survive deletion and why the final combinatorial structure has the required sparsity.

Never delete from a cached coverage count without versioning it. Multiplicity, directed constraints, regional policy, and side constraints can make a syntactically redundant object semantically required. Verify the original model after cleanup.

### Distinguish neighboring schemas

**LP rounding** first obtains a fractional primal solution and maps it to a discrete solution. **Primal-dual construction** grows a dual and commits primal objects at events, often without finding the primal LP optimum. **Dual fitting** constructs prices that may violate the dual, then scales them into feasibility; its factor comes from the scale. **Local ratio** recursively subtracts weight components and can often be interpreted primal-dually, but its invariant is expressed through weight decomposition. **Lagrangian relaxation** moves selected constraints into the objective with multipliers and requires its own bound argument.

These views can yield equivalent algorithms, yet their certificates differ. A production result must name the actual algorithm and show the evidence its analysis requires. Calling every price-based heuristic “primal-dual” does not create a lower bound.

### Extend to network growth carefully

In network design, dual variables often correspond to violated cuts or active components. Moats grow until an edge becomes tight; the edge merges components; inactive components stop growing under a problem-specific rule. Laminarity or uncrossing may make exponentially many cut constraints manageable. A reverse-delete pass can turn the growth history into a sparse forest.

The factor proof may charge edge cost to boundaries of active components and use a degree bound in a contracted forest. This is not the vertex-cover two-endpoint argument. Directed connectivity, node weights, capacities, and higher connectivity requirements can invalidate uncrossing or change the factor. The primary generalized-Steiner results therefore specify the cut-requirement class precisely.

Facility location has different events: client budgets grow, connections become affordable, and accumulated contributions open facilities. Metricity controls reassignment. Omitting the triangle inequality or changing capacity semantics invalidates the classical factor even if the event loop still terminates.

### Preserve exactness and deterministic events

With integer or rational input, store dual values and residuals exactly when practical. If rates are rational, compare event times by cross multiplication with checked wide integers. With floating arithmetic, use conservative slack, detect negative residual beyond tolerance, and independently validate the final dual. “Nearly feasible” is not a certified lower bound unless violations are converted into an explicit safe correction.

Several resources may become tight at the same time. Choose all required events or a deterministic ordered subset covered by the proof. Stable identifiers make traces replayable. Zero-cost objects are tight initially and must be processed before growth. Negative costs violate the canonical starting assumptions and require preprocessing with a proof.

Parallel dual growth is dangerous when active demands share budgets. Workers using stale slack can jointly overshoot a constraint. Safe designs allocate disjoint budgets, use atomic reservations, or compute a synchronized global minimum event. The parallel implementation is a different state machine and needs a matching proof.

### Validate and publish the certificate

A verifiable result binds the original instance digest, normalization and formulation versions, primal object IDs, primal cost, dual variable IDs and values, every dual residual, event trace, cleanup trace, approximation factor, arithmetic mode, and completion status. A checker reconstructs original feasibility, dual feasibility, tightness for charged objects, charging multiplicity, and the final inequality.

Test empty and edgeless instances, isolated vertices, zero costs, a single factor-tight edge, stars, paths, odd cycles, parallel or duplicate demands, extreme weights, simultaneous tightness, disconnected components, overflow boundaries, malformed traces, and timeouts. For small instances, compare against exact integer and dual oracles. Finite tests support the implementation; the universal guarantee comes from the proof.

On timeout, a partial dual may still be a valid lower bound and a current primal solution may be feasible, but the advertised factor holds only if the charging relation covers that exact pair. Otherwise publish the primal as feasible-uncertified and the dual as a separate lower bound. Never infer the missing inequality from their favorable observed ratio.

## Definitions and Notation

Let $A\ge0$ be a covering matrix, $c\ge0$ object costs, $x$ primal variables, $y$ dual demand prices, $P=c^Tx$ a primal value, $D=\mathbf1^Ty$ a dual value, and $OPT$ the integer optimum.

- **Residual slack** $s_j=c_j-(A^Ty)_j$ is unused dual budget of object $j$.
- An **active demand** currently participates in dual growth.
- An **event time** is the largest safe growth increment before a relevant constraint becomes tight.
- A **moat** is a dual-growing component or cut region in a network primal-dual algorithm.
- **Dual fitting** scales a constructed infeasible price vector into a feasible dual.
- **Charging multiplicity** is the maximum number of selected-object contributions assigned to one unit of dual value.
- A **certificate checker** recomputes feasibility and inequalities independently of the constructor.

## Mechanisms, Invariants, or Proof Structure

### Four-link approximation chain

Establish (1) the integer feasible set lies inside the primal relaxation; (2) the constructed dual is feasible, so $D\le LP\le OPT$; (3) the constructed primal object is integer-feasible; and (4) charging gives $P\le\alpha D$. Then $P\le\alpha OPT$. None of these links substitutes for another.

### Event safety invariant

Before and after each growth event, $y\ge0$ and $A^Ty\le c$. The chosen increment is no greater than every affected slack divided by its growth rate. At least one event becomes tight or one active demand changes state, ensuring progress.

### Witness and cleanup invariant

Every selected object records a tight event. Cleanup preserves all original demands and never increases cost. If the factor relies on post-cleanup sparsity, the deletion order and surviving witnesses satisfy the problem-specific structural lemma.

### Certificate binding invariant

The primal, dual, model, trace, arithmetic rules, and claimed factor share one instance and algorithm digest. A checker recomputes them from canonical IDs rather than trusting displayed totals or constructor caches.

## Alternatives and Trade-Offs

| Method | Strength | Risk | Required evidence |
|---|---|---|---|
| Primal-dual growth | Combinatorial and certificate-producing | Problem-specific events and charging | Feasible primal/dual and factor proof |
| LP rounding | Uses global fractional structure | Solver and rounding cost | Certified relaxation and rounding proof |
| Dual fitting | Flexible greedy interpretation | Constructed prices initially infeasible | Safe scaling factor |
| Local ratio | Simple recursive weight reductions | Reconstruction/order complexity | Decomposition invariant |
| Exact IP | Optimal on completion | Exponential worst case | Optimality certificate or bound gap |
| Heuristic pricing | Fast operational signal | No automatic lower bound | Heuristic label and empirical evaluation |
| Parallel growth | Potential throughput | Shared-budget overshoot | Concurrency-safe event proof |

## Failure Modes and Misconceptions

- **“A dual-looking number is a lower bound.”** It must satisfy the exact dual of the exact model.
- **“Tight means selected.”** The algorithm specifies which tight objects to select and how cleanup works.
- **“Complementary slackness proves optimality.”** Partial tightness in an integral construction is insufficient.
- **“Weak duality gives the approximation factor.”** Charging multiplicity supplies the factor.
- **“All covering problems get factor two.”** Vertex cover has two endpoints; general frequency can be larger.
- **“Almost feasible is feasible enough.”** An unsafe dual cannot certify a lower bound.
- **“Event order never matters.”** It can change output, witnesses, cleanup, and reproducibility.
- **“Reverse deletion is cosmetic.”** Some analyses require the sparse final structure it creates.
- **“A timeout preserves the theorem.”** Only if the returned primal-dual pair satisfies every link.
- **“Parallel workers can spend the same slack.”** Shared budgets require synchronization or allocation.
- **“Preprocessing is invisible.”** Dual and primal certificates must reconstruct to the original model.
- **“Good observed gap proves a factor.”** Tests do not replace the universal charging proof.

## Worked Examples

### Example 1

**Situation.** One edge has endpoint costs 1 and 1.

Raise its dual price to one. Both endpoint budgets become tight and the rule selects both. Primal cost is 2, dual value is 1, and optimum selects either endpoint for cost 1.

**Conclusion.** The example realizes the factor-two charging bound.

### Example 2

**Situation.** One edge has endpoint costs 2 and 5.

Raise its price by the minimum residual, 2. The first endpoint becomes tight and is selected; the edge is covered, so growth stops. Primal cost 2 equals optimum, while dual value 2 certifies it.

**Conclusion.** Tightness can identify the cheaper endpoint without solving the primal LP.

### Example 3

**Situation.** A unit-cost path has edges $(0,1),(1,2),(2,3)$ in that order.

The first event selects 0 and 1. The middle edge is already covered. The last event selects 2 and 3. Cost is 4, dual value is 2, and optimum cost is 2.

**Conclusion.** Deterministic order may yield a factor-tight but valid cover.

### Example 4

**Situation.** A dual-growth implementation raises an edge price by 3 when one endpoint has residual slack 2.

That endpoint's dual load exceeds its cost by 1. The returned price vector is dual-infeasible, so its total cannot be used as a weak-duality lower bound.

**Conclusion.** Growth must stop at the earliest affected tight event.

### Example 5

**Situation.** Set-cover elements belong to at most three selected tight sets, and the final dual value is 40.

Double counting gives selected cost at most $3(40)=120$. If exact optimum is later found to be 90, the realized ratio is at most $4/3$, but the construction-time certificate remains 3.

**Conclusion.** Structural frequency controls the proved factor; realized quality is separate.

### Example 6

**Situation.** Growth selects sets $A,B,C$; afterward $B$ is redundant.

Reverse deletion checks $C$, then $B$, then $A$. Removing $B$ preserves coverage, so final cost decreases. The pre-cleanup inequality still holds because costs are nonnegative; if sparsity is used in charging, the proof must analyze this same order.

**Conclusion.** Cleanup is safe only with explicit feasibility and structural obligations.

### Example 7

**Situation.** Two workers see residual budget 5 on a shared object and each independently raises a dual by 4.

Combined load rises by 8 and exceeds the budget by 3. Each local check passed against stale state, but the global dual is infeasible.

**Conclusion.** Parallel growth needs atomic reservation or synchronized event computation.

### Example 8

**Situation.** A floating checker computes dual load $10.0000002$ against cost 10 and simply clips the displayed load to 10.

Display clipping does not change the dual variables or prove feasibility. Scale all duals conservatively, reconstruct exact rationals, or report no certified bound; then recompute the resulting value.

**Conclusion.** Numerical correction must transform the certificate, not its formatting.

### Example 9

**Situation.** At timeout, primal cost is 150 and a validated dual is 80.

The observed primal-to-dual ratio is 1.875. It is an instance certificate if both objects refer to the same original model and are feasible. A generic factor-two theorem is unnecessary for this stronger instance statement, but incomplete reconstruction can still invalidate it.

**Conclusion.** Valid primal-dual pairs can provide useful anytime bounds.

### Example 10

**Situation.** A facility-location variant drops the triangle inequality but keeps the classical connection-reassignment rule.

Reassignment cost can no longer be bounded by the metric path used in the analysis. The event loop may return a feasible solution, yet the classical approximation factor does not follow.

**Conclusion.** Domain assumptions belong in the certificate and deployment contract.

## Cross-Program Connections

- **Algorithm Engineering:** [ALGE-063](./063-linear-programming-rounding.md) supplies relaxation and numerical foundations; [ALGE-065](../ROADMAP.md#block-07--approximation-heuristics-and-randomized-algorithms) studies improvement neighborhoods rather than dual growth.
- **Theory of Computation:** owns hardness and inapproximability that contextualize achievable factors.
- **Data Structures Engineering:** owns event queues, stale-key validation, dynamic incidence, and exact sparse accumulators.
- **Database and Data Architecture Engineering:** own canonical model lineage, stable constraint identities, and atomic result publication.
- **Concurrent and Parallel Programming:** owns synchronization mechanisms used when active duals share resource budgets.
- **Software Testing:** owns exact small-instance oracles, trace mutation tests, certificate replay, and arithmetic boundaries.
- **Network and Systems Engineering:** own the semantic meaning of connectivity, failure domains, capacities, and deployed resource costs.

## References

1. David P. Williamson and David B. Shmoys, [“The Primal-Dual Method”](https://www.cambridge.org/core/books/abs/design-of-approximation-algorithms/primaldual-method/65C5F83E0A6EA59513F41233D5DF1E10), in *The Design of Approximation Algorithms*, Cambridge University Press, 2011/2012, Chapter 7. Publisher chapter and table of contents checked 2026-09-05.
2. Vijay V. Vazirani, [*Approximation Algorithms*](https://link.springer.com/book/10.1007/978-3-662-04565-7), Springer, 2001/2003, doi:10.1007/978-3-662-04565-7. Publisher record checked 2026-09-05; covers LP duality, set cover, and the primal-dual schema.
3. Reuven Bar-Yehuda and Shimon Even, “A Linear-Time Approximation Algorithm for the Weighted Vertex Cover Problem,” *Journal of Algorithms* 2(2), 198–203, 1981, [doi:10.1016/0196-6774(81)90020-1](https://doi.org/10.1016/0196-6774(81)90020-1). Primary weighted-cover source; DOI and DBLP records checked 2026-09-05.
4. David P. Williamson, Michel X. Goemans, Milena Mihail, and Vijay V. Vazirani, “A Primal-Dual Approximation Algorithm for Generalized Steiner Network Problems,” *Combinatorica* 15, 435–454, 1995, [doi:10.1007/BF01299747](https://doi.org/10.1007/BF01299747). Primary network-design source; Springer/IBM/author records checked 2026-09-05.
5. Michel X. Goemans and David P. Williamson, [“The Primal-Dual Method for Approximation Algorithms and Its Application to Network Design Problems”](https://math.mit.edu/~goemans/primaldual.html), in Dorit Hochbaum, ed., *Approximation Algorithms for NP-Hard Problems*, 1997. Author-maintained publication record checked 2026-09-05.
6. Reuven Bar-Yehuda, Keren Bendel, Ari Freund, and Dror Rawitz, “Local Ratio: A Unified Framework for Approximation Algorithms,” *ACM Computing Surveys* 36(4), 422–463, 2004, [doi:10.1145/1041680.1041683](https://doi.org/10.1145/1041680.1041683). Framework comparison reference.
7. Bernhard Korte and Jens Vygen, [*Combinatorial Optimization: Theory and Algorithms*](https://link.springer.com/book/10.1007/978-3-662-56039-6), 6th edition, Springer, 2018, doi:10.1007/978-3-662-56039-6. Duality, covering, network design, and approximation reference; publisher record checked 2026-09-05.

## Exercises

### Exercise 1

Derive the dual of $\min c^Tx$ subject to $Ax\ge\mathbf1$ and $x\ge0$ for $A,c\ge0$. Prove weak duality directly and state why a feasible dual lower-bounds the integer optimum.

### Exercise 2

Run the weighted-vertex-cover primal-dual algorithm on path edges $(0,1),(1,2),(2,3)$ with weights $(2,1,3,1)$. Use edge order as written. Record every residual, dual increment, selected vertex, final cost, dual value, and an exact optimum.

### Exercise 3

A concurrent implementation grows ten active demand prices against overlapping object budgets using stale event times. Design a safe execution and certificate-validation strategy that preserves dual feasibility and deterministic replay.

### Exercise 4

Compare primal-dual construction, LP rounding, dual fitting, and local ratio for a weighted covering service. Address inputs, state, certificate, approximation proof, solver dependency, cleanup, and implementation failure modes.

### Exercise 5

A regional network planner preprocesses zero-cost edges, grows cut duals, stops on timeout, reverse-deletes edges, and returns a “2-approximation.” Design the evidence needed to defend or reject that claim under disconnected inputs, floating arithmetic, and policy constraints absent from the mathematical model.

## Answers to the Exercises

### Answer 1

Assign nonnegative price $y_i$ to each covering row. Object $j$ receives total price $(A^Ty)_j$, which cannot exceed $c_j$, giving $\max\mathbf1^Ty$ subject to $A^Ty\le c$, $y\ge0$. For feasible $x,y$, $\mathbf1^Ty\le y^TAx=x^TA^Ty\le x^Tc$ because $Ax\ge\mathbf1$, $y\ge0$, $A^Ty\le c$, and $x\ge0$. Every integer feasible solution is primal-LP feasible with the same cost, so $D\le LP\le OPT$. Equality rows, signs, or a maximization primal require a new derivation.

### Answer 2

Start residuals $(2,1,3,1)$. Edge $(0,1)$ is uncovered; raise $y_{01}$ by 1, leaving $(1,0,3,1)$ and selecting vertex 1. Edge $(1,2)$ is covered and skipped. Edge $(2,3)$ is uncovered; raise $y_{23}$ by 1, leaving $(1,0,2,0)$ and selecting vertex 3. Final cover is $\{1,3\}$, cost $1+1=2$, and dual value is $1+1=2$. It covers all edges and is exact optimum: the dual proves no cover costs below 2, while the returned cover costs 2.

### Answer 3

Canonicalize active demands and affected budgets. At a barrier, aggregate each object's total growth rate and compute the global minimum safe event from current residuals using exact rationals or conservative checked arithmetic. Commit one event batch atomically, drain all zero-time tight events in stable-ID order, version residuals, and invalidate stale predictions. Alternatively allocate disjoint budget reservations before independent growth. The checker replays rates and increments, asserts nonnegative prices and every $A^Ty\le c$, verifies tight witnesses and primal feasibility, and binds trace/model digests. Local stale checks are insufficient because workers can jointly overspend one budget.

### Answer 4

Primal-dual construction starts from a feasible dual, grows prices, selects objects at proved events, and certifies through dual feasibility plus charging. LP rounding starts with a solved fractional primal and needs solver/bound evidence plus a rounding theorem. Dual fitting may create an infeasible price vector and proves a scaling that makes it feasible. Local ratio decomposes weights, solves residual instances, and proves reconstruction; it can coincide algorithmically with primal-dual but exposes different invariants. All need original feasibility and recomputed cost. Their characteristic failures are budget overshoot, solver/tolerance error, invalid scaling, and broken reconstruction respectively. Cleanup is analyzed only where the chosen proof permits it.

### Answer 5

Require the original graph and policy digest, preprocessing map and proof that zero-cost choices reconstruct, exact cut-demand semantics, active-component and dual-event trace, dual residuals, arithmetic/tolerance policy, selected and deleted edge IDs, original connectivity and policy verification, final cost, and factor derivation for the declared requirement class. On timeout, verify whether the exact returned primal and dual satisfy $P\le2D$; primal feasibility and dual feasibility alone do not imply it. Disconnected infeasible demands must be rejected, not silently omitted. Constraints absent from the model cannot be certified by its dual. If floating violations cannot be conservatively repaired or if cleanup lacks the required structural lemma, publish only a feasible-uncertified result or reject it; do not claim two-approximation.
