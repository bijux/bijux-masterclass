---
module_id: ALGE-061
program: Algorithm Engineering
level: 2
module_number: 61
title: Approximation Ratios and Guarantees
status: complete
last_verified: 2026-09-05
---

# Approximation Ratios and Guarantees

## One-Page Review

### Governing question

When exact optimization is computationally impractical, how can we specify, prove, test, and operationalize a polynomial-time guarantee that bounds solution quality for every admissible instance without confusing it with typical empirical performance?

### Essential definitions

- An **optimization problem** defines admissible instances, feasible solutions, an objective, and minimization or maximization direction.
- $OPT(I)$ is the objective value of an optimal feasible solution for instance $I$.
- An **$\alpha$-approximation** for positive objectives has $A(I)\le\alpha OPT(I)$ for minimization or $A(I)\ge OPT(I)/\alpha$ for maximization, with $\alpha\ge1$.
- An **absolute guarantee** holds for every admissible instance; an **asymptotic guarantee** may include an additive term or apply as $OPT$ grows.
- An **additive guarantee** bounds $|A(I)-OPT(I)|$ rather than a ratio.
- A **PTAS** gives a $(1+\varepsilon)$ minimization approximation for every fixed $\varepsilon>0$ in time polynomial in input size; an **FPTAS** is also polynomial in $1/\varepsilon$.
- A **lower bound** $L(I)\le OPT(I)$ for minimization lets a feasible solution $A(I)$ prove $A(I)\le\alpha L(I)\le\alpha OPT(I)$.
- An **integrality gap** compares an integer optimum with a relaxation optimum and can limit analyses based on that relaxation.

### Central model, mechanism, or theorem

For minimum vertex cover, take both endpoints of every edge in any maximal matching $M$. Maximality implies the chosen endpoints cover every edge. Every vertex cover must include at least one endpoint from each edge of $M$; matching edges are disjoint, so $OPT\ge|M|$. The algorithm returns $|C|=2|M|\le2OPT$. The matching is a checkable lower-bound certificate.

The factor depends on problem direction, objective sign, feasibility, and instance class. A ratio is meaningless when its denominator can be zero or negative unless the definition handles those cases explicitly.

### Critical invariants

- Input validation establishes the exact instance class assumed by the theorem.
- The returned solution is feasible before its objective is compared with $OPT$ or a bound.
- Objective arithmetic uses exact or conservatively rounded values.
- Every inequality states its direction and premises.
- Lower bounds for minimization and upper bounds for maximization are independently checkable where possible.
- Randomized guarantees state expectation, probability, adversary, and repetition assumptions.
- Timeout, infeasibility, heuristic fallback, and numerical failure cannot inherit the proved ratio silently.

### Common failures

Common failures include reversing minimization and maximization ratios; dividing by zero; proving only feasibility; comparing with an unknown optimum without a bound; using an inadmissible relaxation value; assuming one benchmark establishes a worst-case guarantee; hiding additive terms in a factor; calling pseudopolynomial time polynomial; omitting $\varepsilon$ dependence; applying a metric-TSP result to nonmetric costs; and reporting the best of repeated randomized runs without accounting for selection and failure probability.

### Compact example

A minimization algorithm returns cost 120 and a certified lower bound is 80. The instance-specific certificate is $120/80=1.5$, so $120\le1.5OPT$ because $80\le OPT$. If the true optimum later proves to be 100, realized ratio is 1.2; that better observation does not change the algorithm's general worst-case theorem.

### Connections

[ALGE-060](./060-engineering-search-over-large-text-and-sequence-collections.md) distinguishes heuristic search from completeness. [ALGE-062](../ROADMAP.md#block-07--approximation-heuristics-and-randomized-algorithms) develops greedy approximation analyses. Theory of Computation owns hardness assumptions; Software Testing owns finite implementation evidence, not universal approximation proofs.

## Governing Question

Given an optimization problem, an efficient algorithm, and a claimed factor, how do we define the comparison so it survives zero values and numerical representation, prove feasibility and the factor for the stated instance domain, and communicate exactly what the theorem and experiments do—and do not—establish?

An approximation guarantee is a quantified mathematical contract. It says more than “usually close” and less than “optimal.” Its strength comes from covering every admissible instance, so unstated restrictions or fallback behavior can invalidate it.

## Why This Matters

Many useful optimization problems are NP-hard. Approximation algorithms keep polynomial running time and feasibility while relaxing exact optimality in a controlled way. The theory gives an engineer a portable quality floor independent of a benchmark distribution.

Yet production software adds failure modes absent from a clean theorem: invalid or oversized inputs, finite precision, time limits, nondeterministic parallel execution, incomplete lower bounds, and evolving business objectives. A robust interface attaches the guarantee to a verified execution path and reports when that path was not followed.

Approximation is also a design language. Lower bounds identify what any solution must pay. Relaxations expose structure. Charging, exchange, rounding, primal-dual, local-search, and randomized arguments connect an implementable solution to those bounds. Later modules develop those techniques; this chapter establishes the contract they must satisfy.

## Prerequisites and Retrieval

Retrieve reductions and NP-hardness, asymptotic analysis, graph matching and vertex cover, linear programming and relaxations, probability, exact arithmetic, and [ALGE-041](./041-flow-networks-and-residual-graphs.md) through [ALGE-050](./050-turning-a-domain-problem-into-a-graph-optimization-problem.md) for certificates and modeling discipline.

This chapter defines ratios, schemes, certificates, proof structure, and engineering evidence. [ALGE-062](../ROADMAP.md#block-07--approximation-heuristics-and-randomized-algorithms) through ALGE-068 own specific greedy, rounding, primal-dual, local-search, and randomized methods.

## Learning Objectives

After completing this module, you should be able to:

1. formalize an optimization problem and admissible instance class;
2. state minimization and maximization approximation factors correctly;
3. handle zero, negative, additive, and asymptotic objectives explicitly;
4. prove a factor through feasibility and a certified bound;
5. distinguish absolute, expected, high-probability, bicriteria, and empirical claims;
6. distinguish a fixed-factor algorithm, PTAS, EPTAS, FPTAS, and pseudopolynomial method;
7. explain how relaxations and integrality gaps affect possible analyses;
8. validate transformations and reductions that transfer guarantees;
9. bind a production result to the verified algorithm path and parameters; and
10. combine theorem-based guarantees with honest finite benchmarking.

## Core Exposition

### Formalize the optimization problem

An optimization problem supplies an instance set $\mathcal I$. Each $I\in\mathcal I$ has feasible solutions $F(I)$ and objective $f_I:F(I)\to\mathbb R$. For minimization,

$$
OPT(I)=\min_{x\in F(I)} f_I(x),
$$

and maximization uses $\max$. An algorithm must either return $x_A\in F(I)$ or a separately specified non-success outcome. Write $A(I)=f_I(x_A)$ only after feasibility is established.

The instance class carries theorem premises: nonnegative weights, triangle inequality, undirected graph, fixed dimension, integral demands, or bounded capacities. Parsing a file is not proof that those premises hold. Validation must reject, transform with proof, or use a different contract.

Objective identity includes units and aggregation. Adding a constant preserves exact minimizers but can change multiplicative ratios. Negating a maximization objective reverses ordering but does not automatically preserve a positive-factor definition. Model transformations therefore need ratio analysis, not merely optimizer equivalence.

### Define multiplicative guarantees by direction

Assume $OPT(I)>0$ and $A(I)>0$. For minimization, feasibility gives $A(I)\ge OPT(I)$ and an $\alpha$-approximation additionally satisfies

$$
1\le \frac{A(I)}{OPT(I)}\le\alpha.
$$

For maximization, $A(I)\le OPT(I)$ and the same $\alpha\ge1$ convention uses

$$
1\le \frac{OPT(I)}{A(I)}\le\alpha,
$$

equivalently $A(I)\ge OPT(I)/\alpha$. Some literature reports a maximization performance ratio $A/OPT\in[0,1]$. Both are valid conventions; never mix their numbers.

If $OPT=0$, direct division fails. A theorem may prove $A=0$ for those instances and state the factor only for positive optima. Negative objectives need a shift-independent alternative, an additive bound, or a problem-specific definition. Arbitrarily adding constants to make values positive can make any multiplicative ratio appear close to one.

### Prove feasibility and comparison separately

Most approximation proofs have two obligations:

1. **Feasibility:** the constructed object belongs to $F(I)$.
2. **Quality:** its objective relates to a valid bound on $OPT(I)$.

For minimization, find $L(I)\le OPT(I)$ and show $A(I)\le\alpha L(I)$. For maximization, find $U(I)\ge OPT(I)$ and show $A(I)\ge U(I)/\alpha$. The bound may come from a relaxation, packing, matching, dual solution, averaging, or decomposition.

An instance-specific certificate can be stronger than the general theorem. If a solver returns feasible cost $A$ and verified lower bound $L>0$, then $A/L$ certifies that instance, even when the algorithm's worst-case factor is larger. A weak bound does not mean the solution is poor; it means the available certificate is weak.

### Derive a two-approximation for vertex cover

For an undirected graph $G=(V,E)$, a vertex cover $C\subseteq V$ touches every edge. Find any **maximal matching** $M$: disjoint edges to which no further edge can be added. Return every endpoint of every edge in $M$.

Feasibility follows from maximality. If an uncovered edge had neither endpoint in $C$, it would be disjoint from every matched edge and could be added to $M$, contradicting maximality.

For quality, every vertex cover must choose at least one endpoint from each matching edge. Because matching edges share no endpoints, these requirements are distinct, so $OPT\ge|M|$. The returned set has $|C|=2|M|$, hence $|C|\le2OPT$.

The implementation below uses exhaustive optimum search only as a small-instance oracle. The approximation algorithm itself does not use the optimum.

<!-- bijux-verify: {"id":"maximal-matching-vertex-cover","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"path matching=((0, 1), (2, 3)) cover=(0, 1, 2, 3) optimum=(0, 2) ratio=2.0\ntriangle matching=((0, 1),) cover=(0, 1) optimum=(0, 1) ratio=1.0\nstar matching=((0, 1),) cover=(0, 1) optimum=(0,) ratio=2.0\nempty matching=() cover=() optimum=() ratio=1.0\n","stderr":""}} -->
```python
from itertools import combinations


def approximate_cover(vertices, edges):
    remaining = {tuple(sorted(edge)) for edge in edges}
    matching = []
    while remaining:
        edge = min(remaining)
        matching.append(edge)
        left, right = edge
        remaining = {e for e in remaining if left not in e and right not in e}
    cover = tuple(sorted({vertex for edge in matching for vertex in edge}))
    assert all(left in cover or right in cover for left, right in edges)
    return tuple(matching), cover


def optimum_cover(vertices, edges):
    for size in range(len(vertices) + 1):
        for chosen in combinations(vertices, size):
            if all(left in chosen or right in chosen for left, right in edges):
                return chosen
    raise AssertionError("finite graph always has a vertex cover")


cases = {
    "path": ((0, 1, 2, 3), ((0, 1), (1, 2), (2, 3))),
    "triangle": ((0, 1, 2), ((0, 1), (1, 2), (0, 2))),
    "star": ((0, 1, 2, 3), ((0, 1), (0, 2), (0, 3))),
    "empty": ((0, 1), ()),
}
for name, (vertices, edges) in cases.items():
    matching, cover = approximate_cover(vertices, edges)
    optimum = optimum_cover(vertices, edges)
    ratio = len(cover) / len(optimum) if optimum else 1.0
    print(f"{name} matching={matching} cover={cover} optimum={optimum} ratio={ratio}")
```

### Distinguish guarantees from observed quality

A worst-case factor is a supremum over admissible instances, not a forecast for a workload. An algorithm with factor two may be optimal on most measured inputs. Conversely, excellent benchmark averages do not prove any finite worst-case factor.

Report both layers. The theorem record identifies problem version, algorithm, factor, premises, proof or citation, arithmetic model, and complexity. The empirical record identifies corpus, optimum or bound oracle, hardware, implementation version, timeouts, and distribution of realized gaps.

If exact optimum is unavailable, $A/L$ is an upper bound on a minimization solution's ratio, not the realized ratio. Comparing two feasible costs identifies which is cheaper but not how close either is to optimum. Small exact instances can test code and find counterexamples; they cannot prove the universal theorem.

### Define approximation schemes with runtime dependence

A PTAS accepts accuracy parameter $\varepsilon>0$ and, for minimization, returns a $(1+\varepsilon)$-approximation. For every fixed $\varepsilon$, runtime is polynomial in input size $n$, but its dependence on $1/\varepsilon$ may be exponential, such as $n^{1/\varepsilon}$.

An EPTAS has runtime $f(1/\varepsilon)n^{O(1)}$, separating the polynomial exponent from accuracy. An FPTAS has runtime polynomial in both $n$ and $1/\varepsilon$. A pseudopolynomial algorithm polynomial in numeric magnitudes is not polynomial in their bit-length; scaling such an algorithm may yield an FPTAS only after a complete error and runtime proof.

The input contract restricts $\varepsilon$ to a representable valid range. Very small $\varepsilon$ can create enormous work even for an FPTAS. Production policy may reject it, but rejection is not a lower-quality approximate answer.

### Use additive, asymptotic, and bicriteria bounds deliberately

An additive guarantee may state $A\le OPT+\beta$ for minimization. It can be strong when objectives are large and weak when they are small. An asymptotic factor may state $A\le\alpha OPT+\beta$; omitting $\beta$ falsely upgrades it to an absolute factor.

Bicriteria approximation relaxes more than the objective. A solution might cost at most $\alpha OPT$ while violating capacity by at most factor $\beta$. Write the pair $(\alpha,\beta)$ and identify which constraint is relaxed. A formally excellent cost is unusable when the relaxed constraint is legally or physically hard.

Resource augmentation compares an algorithm given extra capacity with an optimum lacking it. Online competitive ratios compare against an offline optimum under an arrival model. These are useful but not interchangeable with an ordinary offline approximation ratio.

### State randomized guarantees completely

A randomized approximation can guarantee an expected objective, a factor with probability at least $1-\delta$, or both. State whether probability is over algorithm randomness for each fixed input, whether the adversary sees random choices, and whether runtime is deterministic, expected, or high probability.

Repetition changes claims only with justified independence or martingale reasoning. For a maximization algorithm that succeeds with probability $p$, $r$ independent runs and the best feasible result fail together with probability $(1-p)^r$. For minimization choose the cheapest feasible result. Selection never repairs infeasibility, biased verification, or correlated runs.

Seed, run count, and selection rule belong in evidence. A fixed seed aids replay but does not demonstrate the probability theorem. An empirical success frequency estimates behavior on sampled runs; it is not the analytical lower bound $p$ without statistical assumptions.

### Understand relaxations and gaps

A minimization relaxation enlarges the feasible set, so its optimum $LP(I)\le OPT(I)$. Rounding a relaxation solution and proving $A(I)\le\alpha LP(I)$ gives an $\alpha$-approximation. If a family has $OPT/LP$ approaching $g$, no analysis that compares only to this relaxation can certify a factor below $g$ on that family without additional information.

The integrality gap is a property of a formulation and instance family, not proof that no algorithm can do better. Hardness of approximation requires a complexity reduction. Conversely, NP-hardness of exact optimization alone does not imply that a good approximation is impossible.

Relaxation arithmetic needs care. A floating solver value slightly above or below the true relaxation optimum may not be a certified lower bound. Use exact arithmetic, validated dual bounds, or conservative outward rounding appropriate to the claim.

### Preserve ratios through transformations

An implementation often preprocesses, decomposes, or reduces an instance. Exact equivalence of optima is ideal but not necessary; what matters is a proved relationship among original and transformed objectives and the reconstruction cost.

Suppose transformation yields $I'$ and reconstruction maps solution $x'$ to $x$. To transfer a factor, bound both $OPT(I')$ relative to $OPT(I)$ and $f_I(x)$ relative to $f_{I'}(x')$, including additive constants. A reduction preserving decision yes/no answers may fail to preserve approximation ratios.

Kernelization, removal of forced elements, zero-weight handling, connected-component decomposition, and rounding inputs all require proof. Record preprocessing decisions so a certificate can be replayed against the original instance.

### Bind guarantees to production outcomes

Tag each successful result with algorithm/version, model/version, approximation contract, validated premises, parameters, arithmetic mode, certificate or bound, and completion status. A heuristic warm start is compatible if the certified algorithm still completes and the final proof applies.

Timeout complicates guarantees. Returning the best feasible incumbent with an unverified theorem path is a feasible heuristic result, not automatically an $\alpha$-approximation. If a live lower bound $L$ gives $A/L\le\rho$, the system can return the instance-specific certificate $\rho$. Otherwise report “feasible, uncertified.”

Monitor feasibility failures, certificate failures, realized bound gaps, time, memory, fallback rate, numeric warnings, and premise rejections. Recompute the objective independently from the returned solution; never trust a cached objective field as the sole evidence.

## Definitions and Notation

Let $I\in\mathcal I$ be an admissible instance, $F(I)$ its feasible set, $f_I$ its objective, $x_A$ the returned solution, and $A(I)=f_I(x_A)$. Let $OPT(I)$ be the optimum, $L(I)$ a certified minimization lower bound, $U(I)$ a certified maximization upper bound, $\alpha\ge1$ a multiplicative factor, $\beta\ge0$ an additive error, and $\varepsilon>0$ a scheme parameter.

- **Approximation factor:** a universal objective inequality over the stated instance class.
- **Realized ratio:** comparison with an exact optimum known for a particular instance.
- **Certified gap:** comparison with a valid bound, such as $A/L$ for minimization.
- **Relaxation:** an optimization problem whose feasible set contains the original set for minimization.
- **Integrality gap:** worst-case ratio between integer and relaxation optima under a fixed formulation and convention.
- **Hardness of approximation:** conditional evidence that no efficient algorithm achieves a factor unless a complexity assumption fails.
- **Heuristic:** a method without the claimed universal guarantee, regardless of empirical quality.

## Mechanisms, Invariants, or Proof Structure

### Approximation-proof checklist

1. Define instances, feasibility, objective direction, and value domain.
2. Validate every theorem premise.
3. Prove the algorithm terminates in the claimed time model.
4. Prove the returned object is feasible.
5. Construct or invoke a valid bound on $OPT$.
6. Relate algorithm value to that bound with every inequality shown.
7. Treat zero/negative optima and empty instances separately.
8. Account for randomization, numerical error, preprocessing, and fallback paths.

### Vertex-cover proof invariant

During matching construction, edges in $M$ are pairwise vertex-disjoint. At termination, maximality says every edge shares an endpoint with some edge in $M$. Selecting all matched endpoints therefore covers $E$. Any cover assigns at least one distinct selected vertex to each disjoint matching edge, proving $|M|\le OPT$. These premises yield the factor even though $M$ need not be a maximum matching.

### Certificate verification

A verifier independently checks input digest, solution feasibility, objective recomputation, bound feasibility, and inequality. For the vertex-cover example it verifies that $M$ is a matching, $C$ contains both endpoints of $M$, $C$ covers all edges, and $|C|=2|M|$. Maximality supports feasibility for construction, but direct cover verification is simpler for an external checker.

### Evidence boundary

Proof establishes the mathematical algorithm under its model. Formal verification can connect code to that model under its assumptions. Tests cover selected executions. Benchmarks characterize sampled workloads and machines. Production monitoring observes deployed paths. Strong assurance layers these rather than translating one into another.

## Alternatives and Trade-Offs

| Claim or method | Strength | Limitation | Evidence needed |
|---|---|---|---|
| Fixed $\alpha$ factor | Uniform, simple contract | May be conservative | Feasibility and universal bound proof |
| Instance certificate $A/L$ | Can be much tighter | Depends on bound quality | Independently verified solution and bound |
| Additive bound | Handles zero and signed values | Scale-sensitive | Unit and absolute-error proof |
| PTAS | Arbitrarily close for fixed $\varepsilon$ | Accuracy dependence may be severe | Factor and fixed-$\varepsilon$ polynomial proof |
| FPTAS | Polynomial in input and $1/\varepsilon$ | Often problem-specific; numeric scaling | Bit-complexity and error proof |
| Randomized factor | Can beat deterministic method | Failure probability and replay complexity | Probability and runtime analysis |
| Bicriteria result | Makes constrained problems tractable | Relaxes a second promise | Both factors and hard-constraint review |
| Empirical heuristic | May excel on target workloads | No universal floor | Representative oracle-based evaluation |

## Failure Modes and Misconceptions

- **“Within 20%” is unambiguous.** For minimization it may mean $A\le1.2OPT$; state formula and direction.
- **“Feasible implies approximate.”** A feasible value may be arbitrarily worse than optimum.
- **“The relaxation solved, so the ratio holds.”** The relaxation direction and rounded feasibility still need proof.
- **“Average gap proves a factor.”** A worst-case guarantee quantifies over every admissible instance.
- **“$OPT=0$ gives ratio zero.”** Division is undefined; handle the case separately.
- **“Adding a constant is harmless.”** It can arbitrarily alter multiplicative ratios.
- **“A PTAS is practical for tiny $\varepsilon$.”** Polynomial-for-fixed-$\varepsilon$ says nothing about a manageable constant.
- **“Pseudopolynomial is polynomial.”** Numeric magnitude can be exponential in its encoded bit length.
- **“An integrality gap is hardness.”** It limits one formulation's analysis, not every algorithm.
- **“NP-hard means inapproximable.”** Approximation hardness requires additional reductions and assumptions.
- **“A timeout keeps the theorem.”** Only a proved anytime certificate or completed guaranteed path does.
- **“Floating output is a lower bound.”** Rounding direction must preserve validity.

## Worked Examples

### Example 1

**Situation.** A minimization algorithm costs 75 and $OPT=60$.

The realized ratio is $75/60=1.25$. It satisfies a 1.3 guarantee because $75\le1.3\cdot60=78$, and also satisfies any weaker factor such as 2. The same arithmetic does not define a maximization factor.

**Conclusion.** State direction before interpreting a ratio.

### Example 2

**Situation.** A maximization algorithm returns 80 while $OPT=100$.

Under the $\alpha\ge1$ convention, ratio is $OPT/A=100/80=1.25$, equivalently $A=0.8OPT=OPT/1.25$. Calling it “0.8-approximate” uses the alternative performance convention and must be labeled.

**Conclusion.** Reciprocal conventions describe the same result but cannot be compared numerically without conversion.

### Example 3

**Situation.** A minimum-cost instance has $OPT=0$ and the algorithm returns cost 0.

The solution is optimal, but $A/OPT=0/0$ is undefined. State exact optimality for the zero case and the multiplicative theorem for positive optima. If the algorithm returned 1, no finite pure multiplicative factor could justify it against zero.

**Conclusion.** Zero optima require an explicit branch in definition and implementation.

### Example 4

**Situation.** A feasible schedule costs 120; a relaxation supplies verified lower bound 80.

Because $80\le OPT\le120$, the certificate is $120/80=1.5$. If a stronger bound 100 is later proved, the certificate tightens to 1.2 without changing the schedule.

**Conclusion.** Bound quality controls certificate strength, not solution feasibility.

### Example 5

**Situation.** A path on four vertices has edges $(0,1),(1,2),(2,3)$.

The deterministic maximal matching may choose $(0,1)$ and $(2,3)$, returning all four vertices. The optimum cover has two vertices, such as $\{0,2\}$ or $\{1,2\}$. The ratio is exactly two, showing the proof's factor can be tight for this algorithm.

**Conclusion.** A matching certificate proves the bound even when the constructed cover is not optimal.

### Example 6

**Situation.** A minimization result satisfies $A\le1.1OPT+50$ and $OPT=20$.

The bound permits $A\le72$, a ratio as high as 3.6. When $OPT=10,000$, it permits ratio at most $1.105$. Advertising a pure 1.1 approximation would hide the additive term.

**Conclusion.** Asymptotic factors can be weak on small optima.

### Example 7

**Situation.** Two schemes run in $n^{1/\varepsilon}$ and $n^3/\varepsilon^4$ time.

For every fixed $\varepsilon$, both are polynomial in $n$, so both meet the PTAS runtime form if their quality proofs hold. Only the second is polynomial jointly in $n$ and $1/\varepsilon$, so it meets the FPTAS runtime form. Practical crossover still requires measurement.

**Conclusion.** Scheme classification depends on symbolic parameter complexity, not the word “polynomial” alone.

### Example 8

**Situation.** A randomized maximization algorithm achieves its factor with probability at least $0.75$ per independent run.

Run it four independently seeded times and select the highest feasible value. All runs fail with probability at most $(1-0.75)^4=1/256$, so success probability is at least $255/256$. Shared randomness or adaptive adversarial inputs would require a different argument.

**Conclusion.** Amplification needs independence and a direction-correct selection rule.

### Example 9

**Situation.** A capacity algorithm returns cost at most $1.05OPT$ while using up to $1.2$ times each capacity.

This is a $(1.05,1.2)$ bicriteria statement, not an ordinary 1.05 approximation to the original feasible problem. If capacity is a hard safety limit, the output is infeasible regardless of cost quality.

**Conclusion.** Relaxed constraints must be visible beside objective guarantees.

### Example 10

**Situation.** Production times out before a certified two-approximation completes but has a feasible incumbent of cost 900 and verified lower bound 600.

The incomplete general path cannot claim its two-factor theorem. The live certificate does establish $900/600=1.5$ for this instance, assuming bound and objective checks pass. Without that bound the honest status is feasible but uncertified.

**Conclusion.** Bind the returned guarantee to evidence available on the actual execution path.

## Cross-Program Connections

- **Algorithms:** [ALGE-062](../ROADMAP.md#block-07--approximation-heuristics-and-randomized-algorithms) through ALGE-068 instantiate greedy, rounding, primal-dual, local-search, and randomized proof methods.
- **Theory of Computation:** owns NP-hardness, gap reductions, PCP-based hardness, and complexity assumptions underlying inapproximability.
- **Data Structures:** owns efficient representations needed to realize the promised polynomial runtime.
- **Software Testing:** owns bounded exact oracles, property tests, differential checks, and regression evidence without converting samples into proofs.
- **Software Architecture:** owns the separation between certified and heuristic execution paths and versioned result contracts.
- **Data Engineering:** owns representative instance corpora, objective lineage, and benchmark reproducibility.
- **Platform Engineering:** owns quotas, timeouts, telemetry, deterministic replay, and safe rollout of approximation policies.

## References

1. Vijay V. Vazirani, [*Approximation Algorithms*](https://link.springer.com/book/10.1007/978-3-662-04565-7), Springer, 2001/2003, doi:10.1007/978-3-662-04565-7. Graduate reference on approximation definitions, techniques, and approximability; publisher record checked 2026-09-05.
2. David P. Williamson and David B. Shmoys, [*The Design of Approximation Algorithms*](https://www.cambridge.org/core/books/the-design-of-approximation-algorithms/88E0AEAEFF2382681A103EEA572B83C6), Cambridge University Press, 2011, doi:10.1017/CBO9780511921735. Graduate text; definitions and design-technique scope checked 2026-09-05.
3. David S. Johnson, “Approximation Algorithms for Combinatorial Problems,” *Journal of Computer and System Sciences* 9(3), 256–278, 1974, [doi:10.1016/S0022-0000(74)80044-9](https://doi.org/10.1016/S0022-0000(74)80044-9). Primary early worst-case ratio analysis; publisher record checked 2026-09-05.
4. Oscar H. Ibarra and Chul E. Kim, “Fast Approximation Algorithms for the Knapsack and Sum of Subset Problems,” *Journal of the ACM* 22(4), 463–468, 1975, [doi:10.1145/321906.321909](https://doi.org/10.1145/321906.321909). Primary approximation-scheme source; bibliographic record checked 2026-09-05.
5. Brenda S. Baker, “Approximation Algorithms for NP-Complete Problems on Planar Graphs,” *Journal of the ACM* 41(1), 153–180, 1994, [doi:10.1145/174644.174650](https://doi.org/10.1145/174644.174650). Primary structural approximation-scheme source; publisher DOI record checked 2026-09-05.
6. Sanjeev Arora, “Polynomial Time Approximation Schemes for Euclidean Traveling Salesman and Other Geometric Problems,” *Journal of the ACM* 45(5), 753–782, 1998, [doi:10.1145/290179.290180](https://doi.org/10.1145/290179.290180). Primary geometric PTAS source.
7. Michael R. Garey and David S. Johnson, *Computers and Intractability: A Guide to the Theory of NP-Completeness*, W. H. Freeman, 1979, ISBN 978-0716710455. Complexity and reduction reference.
8. Rajeev Motwani and Prabhakar Raghavan, *Randomized Algorithms*, Cambridge University Press, 1995, [doi:10.1017/CBO9780511814075](https://doi.org/10.1017/CBO9780511814075). Randomized guarantees, amplification, and probabilistic analysis reference.

## Exercises

### Exercise 1

State a 1.4-approximation guarantee for a positive-objective minimization problem and for a positive-objective maximization problem. Then explain how each definition handles an optimal value of zero.

### Exercise 2

For graph edges $(a,b),(b,c),(c,d),(d,a),(a,c)$, build any maximal matching, construct the endpoint vertex cover, verify feasibility, derive the matching lower bound, and calculate the certified factor.

### Exercise 3

A service advertises a PTAS but runs in $2^{1/\varepsilon}n^4$, rounds floating lower bounds upward, and returns its current incumbent on timeout with the requested factor. Diagnose each claim and specify correct result statuses.

### Exercise 4

Compare a certified three-approximation with an uncertified heuristic on a workload where the heuristic's mean realized ratio is 1.08 and maximum observed ratio is 1.4. Design an evaluation and deployment policy that uses both without weakening the contract.

### Exercise 5

A resource-allocation problem permits signed utility and hard capacity. A proposal adds a large constant to every objective, reports a 1.01 ratio, and allows 10% capacity violation. Redesign the guarantee so it is invariant to harmless objective representation and honest about feasibility.

## Answers to the Exercises

### Answer 1

For minimization and $OPT>0$, require a feasible result with $A(I)\le1.4OPT(I)$. For maximization and $A>0$, require $A(I)\ge OPT(I)/1.4$, equivalently $OPT/A\le1.4$. When $OPT=0$, division is undefined. A nonnegative minimization contract can require $A=0$ and call it optimal; a nonnegative maximization instance with $OPT=0$ also has every feasible value at most zero, but the treatment depends on its allowed values. State zero cases separately rather than inventing a ratio.

### Answer 2

Choose matching $M=\{(a,b),(c,d)\}$. It is a matching and is maximal. Taking all endpoints yields $C=\{a,b,c,d\}$, which touches every listed edge. Every cover must choose at least one endpoint from each of the two disjoint matching edges, so $OPT\ge2$. Thus $|C|=4=2|M|\le2OPT$, certifying factor two. The actual optimum is two, for example $\{a,c\}$, so this chosen matching realizes ratio two. A different maximal matching may return two vertices and is also valid.

### Answer 3

Runtime $2^{1/\varepsilon}n^4$ is polynomial in $n$ for fixed $\varepsilon$, so it can be a PTAS but not an FPTAS; quality still needs proof. Rounding a minimization lower bound upward can exceed the true bound and invalidate a certificate; use a validated dual bound or conservative downward rounding. An incumbent returned before the guaranteed path completes keeps its factor only if an independently verified bound certifies it. Return `certified` with the measured certificate, `feasible_uncertified` without one, `resource_limit` if no acceptable result contract permits incumbents, and distinct invalid-input or numerical-failure statuses.

### Answer 4

Keep the certified algorithm as the correctness floor. Run the heuristic as a warm start and return its solution if the certified verifier completes and proves the three-factor bound; otherwise use the certified solution. On a latency-bound endpoint, return the heuristic as explicitly uncertified or with an instance-specific bound, never under the unconditional factor. Evaluate both on frozen representative and adversarial sets with exact optima or validated bounds, reporting distributions, maximum observed gaps, feasibility, time, memory, fallback, and certificate rates. The heuristic's observed maximum 1.4 is evidence only for that sample.

### Answer 5

Multiplicative ratios are not invariant under adding constants, so use an additive utility loss $OPT-A\le\beta$, a normalized domain-specific regret with a defensible fixed scale, or transform to a nonnegative cost whose relationship to original utility is proved independently of arbitrary offsets. Hard capacity must not be relaxed: require exact capacity feasibility and reject over-capacity output. If the business permits augmentation, report a bicriteria pair such as utility loss plus capacity factor 1.1 and stop calling it feasible for the original problem. The contract must name units, reference point, feasibility rule, and certificate.
