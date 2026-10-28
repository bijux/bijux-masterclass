---
module_id: ALGE-047
program: Algorithm Engineering
level: 1
module_number: 47
title: Assignment Problems
status: complete
last_verified: 2026-09-05
---

# Assignment Problems

## One-Page Review

### Governing question

How can we choose a one-to-one assignment of agents to tasks that minimizes total cost, and how can dual prices certify that no cheaper assignment exists?

### Essential definitions

- A **linear assignment problem** has agents $L$, tasks $R$, and additive pair costs $c_{ij}$.
- A **feasible square assignment** is a perfect matching, represented by binary variables $x_{ij}$ with every row and column sum equal to one.
- The **primal objective** is $\min\sum_{i,j}c_{ij}x_{ij}$.
- **Dual potentials** $u_i,v_j$ are feasible when $u_i+v_j\le c_{ij}$ for every admissible pair.
- The **reduced cost** is $r_{ij}=c_{ij}-u_i-v_j\ge0$.
- An edge is **tight** when $r_{ij}=0$.
- **Complementary slackness** says an optimal assignment can use tight edges; a perfect tight-edge matching has cost equal to the dual value.
- A **forbidden pair** is absent from the feasible graph, not merely expensive unless a defensible finite penalty has been specified.

### Central model, mechanism, or theorem

For any feasible assignment $X$ and feasible potentials $(u,v)$,

$$
\sum_{i,j}c_{ij}x_{ij}\ge\sum_i u_i+\sum_j v_j.
$$

If every selected edge is tight, equality holds and the assignment and potentials certify mutual optimality. The Hungarian method maintains dual feasibility and a matching in the tight-edge graph. When the tight graph has no perfect matching, alternating reachability identifies a potential update that preserves feasibility, increases the dual bound, and creates at least one new tight edge.

### Critical invariants

- Every required agent and task is assigned exactly once in the balanced model.
- Costs share a declared objective direction, unit, scale, and snapshot.
- Reduced costs remain nonnegative.
- Matched edges remain tight in the primal-dual method.
- Primal cost is an upper bound for minimization; dual value is a lower bound.
- Equal validated objectives prove optimality; a solver status string alone does not.
- Dummy vertices and penalties encode policy and can change the optimum.

### Common failures

Common failures include confusing assignment with cardinality matching; maximizing a cost by accident; using zero-cost dummies when nonassignment has a real penalty; substituting a large finite number for prohibition without a bound; overflowing transformed costs; accepting NaN or mixed units; assuming greedy row minima are jointly feasible; treating one optimum as unique; omitting dual feasibility from a certificate; and applying an additive model when pair choices interact.

### Compact example

For costs

$$
C=\begin{bmatrix}4&1&3\\2&0&5\\3&2&2\end{bmatrix},
$$

choose $(1,2),(2,1),(3,3)$ at cost $1+2+2=5$. Potentials $u=(1,0,1)$ and $v=(2,0,1)$ are feasible, have value five, and make all three chosen pairs tight. The equal upper and lower bounds certify optimality.

### Connections

[ALGE-046](./046-bipartite-matching.md) supplies matching feasibility and alternating paths. [ALGE-048](../ROADMAP.md#block-05--flows-matching-and-combinatorial-optimization) generalizes costs to capacitated minimum-cost flow. Linear programming explains dual potentials and integrality; production allocation adds policy beyond the mathematical objective.

## Governing Question

Given additive costs for pairing two sets one-to-one, what mathematical model captures feasibility, what primal-dual mechanism finds an optimum, and what evidence lets a separate checker distinguish an optimal result from a merely plausible one?

The core assignment problem is polynomially solvable because its constraints have special structure. That favorable result does not transfer automatically to quadratic interactions, arbitrary side constraints, or uncertain future costs. Modeling discipline is therefore as important as the algorithm.

## Why This Matters

Assignment appears in workforce allocation, machine scheduling, object tracking, record linkage, test placement, and resource brokerage. Cardinality matching asks how many pairs can be made; assignment asks which full pairing has least additive cost or greatest additive score. A locally attractive choice can block a much better global combination.

The dual variables have practical value beyond optimization. They provide a lower bound, expose scarce rows or columns as implicit prices, and support a compact optimality certificate. Yet dual prices are properties of the declared matrix, not causal market prices or fairness guarantees.

## Prerequisites and Retrieval

Retrieve matrices, permutations, bipartite perfect matching, alternating paths, linear inequalities, weak and strong duality, and exact arithmetic. Review [ALGE-046](./046-bipartite-matching.md) for matching and equal matching-cover certificates. Familiarity with shortest paths and residual reasoning helps interpret reduced costs.

## Learning Objectives

After completing this module, you should be able to:

1. formulate balanced and rectangular linear assignment problems;
2. distinguish absent pairs, finite penalties, dummy vertices, and genuine zero costs;
3. derive the primal linear program and its dual;
4. prove weak duality directly from row and column constraints;
5. use reduced costs and complementary slackness as an optimality certificate;
6. trace the primal-dual logic of the Hungarian method;
7. explain why the linear relaxation admits an integral optimum;
8. recompute and validate a result independently;
9. handle numeric, representation, and lifecycle hazards; and
10. recognize when interactions or side constraints require a richer model.

## Core Exposition

### State the balanced model

Let $L=\{1,\ldots,n\}$ be agents and $R=\{1,\ldots,n\}$ tasks. Pair $(i,j)$ has finite cost $c_{ij}$. Binary variable $x_{ij}$ is one exactly when agent $i$ receives task $j$:

$$
\begin{aligned}
\text{minimize}\quad &\sum_{i=1}^n\sum_{j=1}^n c_{ij}x_{ij}\\
\text{subject to}\quad &\sum_jx_{ij}=1 &&\text{for every }i,\\
&\sum_ix_{ij}=1 &&\text{for every }j,\\
&x_{ij}\in\{0,1\}.
\end{aligned}
$$

Feasible solutions are permutation matrices and perfect matchings. Additivity is a substantive assumption: the cost of $i$ receiving $j$ cannot depend on other chosen pairs. If it does, this is not the linear assignment problem.

For maximum score, either formulate a maximization explicitly or transform scores with proved numeric bounds. Negating signed values is conceptually simple but can overflow a fixed-width minimum integer. Subtracting from a constant preserves optimizers only when every feasible assignment selects the same number of edges.

### Derive the LP dual and weak duality

Relax $x_{ij}\in\{0,1\}$ to $x_{ij}\ge0$. Associate unrestricted potentials $u_i$ with row equalities and $v_j$ with column equalities. The dual is

$$
\begin{aligned}
\text{maximize}\quad &\sum_i u_i+\sum_jv_j\\
\text{subject to}\quad &u_i+v_j\le c_{ij}\quad\text{for every pair }(i,j).
\end{aligned}
$$

For any primal-feasible $x$ and dual-feasible $(u,v)$,

$$
\begin{aligned}
\sum_{i,j}c_{ij}x_{ij}
&\ge\sum_{i,j}(u_i+v_j)x_{ij}\\
&=\sum_i u_i\left(\sum_jx_{ij}\right)
+\sum_jv_j\left(\sum_ix_{ij}\right)\\
&=\sum_i u_i+\sum_jv_j.
\end{aligned}
$$

This is weak duality: every feasible assignment gives an upper bound on the minimum, and every feasible potential vector gives a lower bound.

### Turn equality into a certificate

Define reduced cost $r_{ij}=c_{ij}-u_i-v_j$. Dual feasibility is exactly $r_{ij}\ge0$. If an assignment selects only tight edges, then

$$
\sum_{i,j}c_{ij}x_{ij}
=\sum_{i,j}(u_i+v_j)x_{ij}
=\sum_i u_i+\sum_jv_j.
$$

Weak duality then proves both objects optimal. A checker needs the cost matrix or its digest, the selected pairs, potentials, numeric domain, and objective direction. It verifies every row and column once, recomputes the primal value, tests every dual inequality, recomputes the dual value, and checks equality. It need not replay the Hungarian algorithm.

### Understand the Hungarian primal-dual mechanism

Begin with any dual-feasible potentials, for example row minima as $u_i$ and zero column potentials $v_j$. Construct the equality graph containing edges with $r_{ij}=0$, then find a maximum matching in it. If the matching is perfect, tightness yields an optimality certificate.

Otherwise start an alternating search from unmatched left vertices in the equality graph. Let $Z_L$ and $Z_R$ be reached left and right vertices. No free right vertex is reached, or an augmenting path would enlarge the matching. The minimum vertex cover of the equality graph is $(L\setminus Z_L)\cup Z_R$, so $|Z_L|>|Z_R|$ while the tight graph lacks a perfect matching.

Choose


$$
\delta=\min\{r_{ij}:i\in Z_L,\ j\notin Z_R\}.
$$

Update $u_i\leftarrow u_i+\delta$ for $i\in Z_L$ and $v_j\leftarrow v_j-\delta$ for $j\in Z_R$. Reduced costs on $Z_L\times Z_R$ do not change; those leaving $Z_L$ decrease by at most $\delta$; those entering $Z_R$ increase; all others stay fixed. Thus dual feasibility is preserved, old matched tight edges stay tight, and at least one new tight edge appears. The dual objective rises by $\delta(|Z_L|-|Z_R|)>0$. Repeating tight-edge augmentation and potential updates eventually yields a perfect matching. Standard dense implementations run in $O(n^3)$ time.

### Explain integrality without hand-waving

The relaxed feasible region is the set of doubly stochastic matrices. Its extreme points are permutation matrices, equivalently by the Birkhoff-von Neumann theorem. A linear objective has an optimum at an extreme point when the feasible polytope is nonempty and bounded, so an integral optimum exists without declaring $x_{ij}$ binary to the LP solver.

The same fact follows from total unimodularity of the bipartite incidence constraint matrix after removing one redundant equality. Integrality depends on this special structure and integral right-hand sides. Adding arbitrary side constraints can destroy it, so a fractional LP optimum may then cease to describe an assignment.

### Handle rectangular and incomplete instances

If there are $m$ agents and $n$ tasks, decide which side must be fully assigned. A rectangular solver commonly returns $\min(m,n)$ pairs for a complete finite matrix, leaving vertices on the larger side unmatched. Padding to a square matrix is correct only when each dummy cost represents the intended consequence of nonassignment. A zero dummy cost says nonassignment is free; a penalty says it has that exact modeled cost.

For incomplete eligibility, maintain an explicit admissible-edge set. A sentinel such as infinity is safe only if the solver supports and documents it. A finite big-$M$ value can be selected if its bound dominates every possible feasible objective difference without overflow, but a mistaken bound can make a forbidden assignment appear optimal. Prefer sparse matching/min-cost-flow interfaces that represent absence directly when appropriate.

### Reproduce a primal-dual certificate

This dependency-free program enumerates a three-by-three instance to obtain the primal optimum, then validates supplied dual potentials and complementary tightness. Enumeration is used only as an independently transparent small-instance oracle.

<!-- bijux-verify: {"id":"assignment-primal-dual-certificate","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"assignment=((0, 1), (1, 0), (2, 2))\ncost=5\ndual_feasible=True dual_value=5\ntight=True certificate=True\n","stderr":""}} -->
```python
from itertools import permutations

cost = (
    (4, 1, 3),
    (2, 0, 5),
    (3, 2, 2),
)

candidates = []
for columns in permutations(range(len(cost))):
    pairs = tuple(enumerate(columns))
    value = sum(cost[row][column] for row, column in pairs)
    candidates.append((value, pairs))

primal_value, assignment = min(candidates)
u = (1, 0, 1)
v = (2, 0, 1)

dual_feasible = all(
    u[row] + v[column] <= cost[row][column]
    for row in range(len(cost))
    for column in range(len(cost[row]))
)
dual_value = sum(u) + sum(v)
tight = all(u[row] + v[column] == cost[row][column] for row, column in assignment)
certificate = dual_feasible and tight and primal_value == dual_value

print(f"assignment={assignment}")
print(f"cost={primal_value}")
print(f"dual_feasible={dual_feasible} dual_value={dual_value}")
print(f"tight={tight} certificate={certificate}")
```

The run checks one exact integer instance under CPython. The direct weak-duality derivation, not exhaustive search, establishes the general certificate rule.

### Treat numeric semantics as part of the model

Declare whether costs are money, latency, distance, risk points, or a lexicographic encoding. Convert to one scale before addition. Binary floating-point may make a mathematically zero reduced cost appear slightly nonzero; arbitrary tolerances can in turn accept a negative reduced cost. Prefer checked integers or exact fixed-point values when units permit. Otherwise state feasibility and equality tolerances, rounding direction, and a bound on accumulated error.

Potential values may be negative and are not unique: adding a constant to every $u_i$ and subtracting it from every $v_j$ preserves reduced costs and dual value. Validate their inequalities and sum, not a preferred normalization.

### Understand current library boundaries

As retrieved on 2026-09-05, SciPy 1.18.0 documents `scipy.optimize.linear_sum_assignment` for dense linear sum assignment, minimization by default, a `maximize` option, and rectangular matrices. It returns row and column index arrays from which the objective can be recomputed. Its documentation points to a separate sparse full-matching routine. These are version-scoped interface properties; callers still own forbidden-edge semantics, units, data freshness, and certificate policy.

### Govern deployed assignment

Canonicalize row and column IDs, costs, units, admissibility, dummy semantics, objective direction, tie-breaking, and revision into a digest. Return selected pairs, unmatched entities, primal cost, dual potentials or another lower bound, validation result, algorithm/version, limits, and the digest. Multiple optimal permutations are legitimate. If stable output matters, add a documented secondary objective rather than relying on iteration order.

Assignment optimizes the stated additive objective. It does not ensure stable preferences, fairness, explainability, privacy, temporal feasibility, or resilience. Interacting pair costs produce quadratic assignment; multi-unit supply leads toward transportation or minimum-cost flow; complex logical constraints may require integer programming. Publish the model boundary with the result.

## Definitions and Notation

- $L,R$: agent and task vertex sets.
- $c_{ij}$: additive cost of assigning $i$ to $j$.
- $x_{ij}$: primal selection variable.
- $u_i,v_j$: unrestricted dual potentials for row and column equalities.
- $r_{ij}=c_{ij}-u_i-v_j$: reduced cost.
- **tight edge:** admissible pair with $r_{ij}=0$.
- **equality graph:** bipartite graph containing the tight edges.
- $Z_L,Z_R$: vertices reached in an alternating equality-graph search.
- **dummy vertex:** explicit representation of an unused entity, with policy-defined costs.
- **primal-dual certificate:** feasible assignment and feasible potentials with equal objective values.

## Mechanisms, Invariants, or Proof Structure

The assignment LP yields dual row and column potentials. Weak duality follows by multiplying every dual constraint by nonnegative $x_{ij}$ and using row and column sums. Tight selected edges make the inequality an equality and certify optimality. The Hungarian method maintains nonnegative reduced costs and tight matched edges; alternating reachability finds either an augmentation or a positive dual update that introduces a new tight edge. Birkhoff-von Neumann or total unimodularity explains why the LP relaxation has an integral optimum. Independent verification recomputes both feasible objectives on one immutable matrix.

## Alternatives and Trade-Offs

- **Greedy row minima:** cheap heuristic; collisions and future blocking make it unreliable.
- **Exhaustive permutations:** transparent for tiny test oracles; factorial and unusable at scale.
- **Hungarian method:** strongly structured $O(n^3)$ dense algorithm with dual evidence.
- **Sparse weighted bipartite matching:** avoids materializing forbidden pairs; behavior depends on required coverage.
- **Minimum-cost flow:** handles capacities and partial flow naturally; broader machinery belongs to ALGE-048.
- **Linear programming:** flexible and exposes duals; arbitrary added constraints may destroy integrality.
- **Dummy padding:** reuses balanced solvers; correctness depends entirely on dummy-cost policy.
- **Exact integer/fixed-point costs:** reproducible certificate equality; require scale and overflow control.
- **Floating costs:** convenient for measured values; require error-aware comparisons.
- **Secondary tie-break objective:** deterministic among equal optima; changes the declared optimization policy.

## Failure Modes and Misconceptions

- A cheapest edge need not belong to any globally cheapest assignment.
- Maximum-cardinality matching ignores costs among full matchings.
- Row reduction preserves all assignment objective differences; arbitrary per-edge changes do not.
- Dual potentials are unrestricted even though reduced costs must be nonnegative.
- A tight edge is eligible for an optimum but need not appear in every optimum.
- Selected tight edges prove optimality only with primal and dual feasibility.
- Zero-cost dummy assignments assert that nonassignment has no cost.
- Big-$M$ is a model value requiring a proved bound, not a synonym for infinity.
- Rectangular output does not automatically identify which side policy required covering.
- LP integrality can disappear after adding side constraints.
- Floating tolerance is not a substitute for an error analysis.
- Linear assignment cannot represent pairwise interactions between assignments.

## Worked Examples

### Example 1

**Situation.** Agent A costs one on task 1 and two on task 2; B costs two and one. **Reasoning.** Choosing both row minima gives A-1 and B-2 with total two and no collision. **Conclusion.** Greedy happens to succeed, but feasibility—not row-local optimality—makes this instance easy.

### Example 2

**Situation.** Costs are A: $(1,2)$ and B: $(1,100)$. **Reasoning.** Both row minima select task 1. If A takes 1, B must take 2 for total 101; assigning A-2 and B-1 costs three. **Conclusion.** Resolving a collision locally can require sacrificing the cheapest edge.

### Example 3

**Situation.** A feasible assignment costs 14 and feasible dual potentials sum to 11. **Reasoning.** Weak duality places the optimum in $[11,14]$. **Conclusion.** The three-unit gap means neither object proves optimality.

### Example 4

**Situation.** An assignment costs nine, dual potentials sum to nine, and every dual inequality holds. **Reasoning.** The assignment is an upper bound and the dual is a lower bound; equality closes the gap. **Conclusion.** Both are optimal even if found by unrelated algorithms.

### Example 5

**Situation.** Potentials give $u_2+v_3=7$ where $c_{23}=6$. **Reasoning.** Reduced cost is $-1$, so dual feasibility fails. Its claimed value is not a lower bound. **Conclusion.** Equal reported totals cannot rescue an invalid certificate.

### Example 6

**Situation.** Three agents and two tasks use a zero-cost dummy task. **Reasoning.** Every solution leaves one agent on the dummy, and zero says all choices of the unassigned agent are cost-neutral except for displaced real costs. **Conclusion.** If nonassignment harms different agents differently, dummy costs must encode those penalties.

### Example 7

**Situation.** A forbidden pair receives big-$M=100$, while all-feasible assignments can cost 500. **Reasoning.** A solution using the “forbidden” edge may still be cheaper than legitimate alternatives. **Conclusion.** The sentinel did not enforce prohibition because its dominance bound was false.

### Example 8

**Situation.** Two assignments both cost 20. **Reasoning.** The optimization model regards both as optimal. A library may return either after a version or ordering change. **Conclusion.** Uniqueness and deterministic choice require separate evidence or a secondary objective.

### Example 9

**Situation.** Monetary costs in cents are added to latency measured in milliseconds. **Reasoning.** The sum has no defined interpretation without a conversion or explicit multiobjective rule. **Conclusion.** Numeric validity cannot repair incompatible semantics.

### Example 10

**Situation.** Assigning A to task 1 makes B's cost for task 2 increase because they share equipment. **Reasoning.** The total is no longer $\sum c_{ij}x_{ij}$ with fixed independent coefficients. **Conclusion.** This interaction lies outside linear assignment and may require quadratic or scheduling constraints.

## Cross-Program Connections

- **Database Engineering:** matrix snapshots need stable identities, deduplication, units, and provenance.
- **Software Architecture:** optimizer and verifier should be separable components with a versioned certificate contract.
- **Systems Engineering:** dummy penalties and forbidden pairs encode requirements whose ownership must be explicit.
- **Data Engineering:** feature-derived costs require reproducible transformations and freshness controls.
- **API Engineering:** objective direction, unmatched semantics, tie policy, and evidence status belong in the response schema.
- **Security Engineering:** adversarial NaN, overflow, oversized matrices, and stale identifiers are input-validation concerns.

## References

1. H. W. Kuhn, “The Hungarian Method for the Assignment Problem,” *Naval Research Logistics Quarterly* 2(1–2), 1955, pp. 83–97, [doi:10.1002/nav.3800020109](https://doi.org/10.1002/nav.3800020109). Primary method paper; retrieved 2026-09-05.
2. J. Munkres, “Algorithms for the Assignment and Transportation Problems,” *Journal of the Society for Industrial and Applied Mathematics* 5(1), 1957, pp. 32–38, [doi:10.1137/0105003](https://doi.org/10.1137/0105003). Primary algorithm and correctness treatment; retrieved 2026-09-05.
3. A. Schrijver, *Combinatorial Optimization: Polyhedra and Efficiency*, Springer, 2003, [publisher record](https://link.springer.com/book/9783540443896). Assignment polytopes, matchings, and combinatorial optimization.
4. R. K. Ahuja, T. L. Magnanti, and J. B. Orlin, *Network Flows: Theory, Algorithms, and Applications*, Prentice Hall, 1993, [MIT record](https://dspace.mit.edu/handle/1721.1/49424). Assignment and minimum-cost network models.
5. T. H. Cormen, C. E. Leiserson, R. L. Rivest, and C. Stein, *Introduction to Algorithms*, 4th ed., MIT Press, 2022, [publisher record](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/). Matching, flow, and linear-programming foundations.
6. SciPy Developers, “`linear_sum_assignment`,” SciPy 1.18.0 documentation, [official documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linear_sum_assignment.html). Dense rectangular interface and objective behavior; retrieved 2026-09-05.

## Exercises

### Exercise 1

Write the balanced minimization assignment primal and dual. Define reduced cost and state a complete primal-dual optimality certificate.

### Exercise 2

For $C=\begin{bmatrix}4&1&3\\2&0&5\\3&2&2\end{bmatrix}$, verify assignment $(1,2),(2,1),(3,3)$ and potentials $u=(1,0,1)$, $v=(2,0,1)$ edge by edge.

### Exercise 3

A service pads 1,000 workers and 900 tasks with 100 zero-cost dummy tasks, uses floating costs, and returns only pairs plus “optimal.” Diagnose the evidence and modeling defects and specify a safer result contract.

### Exercise 4

Compare Hungarian, sparse weighted matching, minimum-cost flow, and a generic LP for a matrix with ten million possible pairs but only fifty thousand admissible pairs and one-unit endpoints.

### Exercise 5

A mentorship program wants one mentor per student, permits mentors to take up to three students, ranks preferences, forbids conflicts of interest, and requires distribution across departments. Formulate the closest sound model, identify which assignment assumptions fail, and define validation evidence.

## Answers to the Exercises

### Answer 1

The primal minimizes $\sum_{ij}c_{ij}x_{ij}$ subject to every row sum and column sum equal to one and $x_{ij}\ge0$; integrality follows from assignment-polytope structure. Its dual maximizes $\sum_i u_i+\sum_jv_j$ subject to $u_i+v_j\le c_{ij}$, with unrestricted potentials. Reduced cost is $r_{ij}=c_{ij}-u_i-v_j$. A certificate contains one selected edge per row and column, feasible potentials, and a shared matrix digest. Verify all primal constraints, all dual inequalities, the recomputed objectives, and equality; equivalently selected edges must be tight. Those checks prove both optimal by weak duality.

### Answer 2

The chosen costs are $c_{12}=1$, $c_{21}=2$, and $c_{33}=2$, totaling five. The nine potential sums by row are $(3,1,2)$, $(2,0,1)$, and $(3,1,2)$; each is at most the corresponding cost row $(4,1,3)$, $(2,0,5)$, and $(3,2,2)$. Thus the dual is feasible. Its value is $(1+0+1)+(2+0+1)=5$. Each selected edge has equality: $1+0=1$, $0+2=2$, and $1+1=2$. The assignment and dual values meet at five, certifying optimality.

### Answer 3

Zero dummy costs assert that leaving any worker unassigned has no direct penalty; that may be wrong or may make tie behavior consequential. Floating arithmetic needs units, finite-value checks, accumulation rules, and an error bound. “Optimal” without the matrix revision, objective, and lower-bound evidence is not independently checkable. The result should include canonical worker/task IDs, real and dummy pair semantics, selected and unmatched entities, exact fixed-point costs where possible, objective direction/value, dual potentials or solver lower bound, primal/dual residuals, graph digest, algorithm/version, tie policy, and limitations. A separate checker validates admissibility, capacities, dummy policy, cost reconstruction, dual feasibility, and the bounded equality or gap.

### Answer 4

A dense Hungarian representation is unattractive because materializing ten million entries wastes memory and invites big-$M$ mistakes. Sparse weighted bipartite matching is the most direct specialized model if it supports the required coverage and certificate needs. Unit-capacity minimum-cost flow represents only fifty thousand admissible arcs, naturally handles partial feasibility, and can expose potentials/residual optimality, though it carries generic overhead. A sparse LP is flexible and can return duals, but generic solver overhead may be higher. Benchmark the two sparse combinatorial routes; select based on coverage semantics, certificate availability, limits, and operational maturity. Dense asymptotics alone do not decide it.

### Answer 5

One-to-one assignment fails because mentors have capacity three and departmental distribution couples multiple choices. Use minimum-cost capacitated flow if distribution requirements can be represented by department aggregation nodes: source-to-mentor capacity three, admissible mentor-student arcs with preference costs, student-to-department or sink arcs enforcing one mentor, and lower/upper departmental bounds where supported. Conflicts are absent arcs. If distribution rules are nonlaminar or logical, use an integer program with binary pair variables, mentor capacities, exactly-one student constraints, forbidden variables fixed to zero, and explicit department inequalities. Validate all identities, conflicts, capacities, coverage, and distribution counts; recompute preference cost; record snapshot and numeric policy; and publish a dual certificate for the flow case or solver bound/gap plus independently checked feasibility for the integer case. A model answer must not force this into a square dummy matrix that loses capacity and distribution semantics.
