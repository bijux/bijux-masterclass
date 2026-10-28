---
module_id: ALGE-063
program: Algorithm Engineering
level: 2
module_number: 63
title: Linear-Programming Rounding
status: complete
last_verified: 2026-09-05
---

# Linear-Programming Rounding

## One-Page Review

### Governing question

How can a fractional solution of a linear-programming relaxation be converted into a feasible discrete solution while bounding objective loss, constraint violation, numerical error, and the gap between mathematical and production solver evidence?

### Essential definitions

- An **integer program (IP)** constrains selected variables to integers; its **LP relaxation** removes or weakens integrality.
- For minimization, a valid relaxation has $LP(I)\le OPT(I)$.
- **Deterministic rounding** maps a fractional point to a discrete point without randomness.
- **Randomized rounding** samples discrete choices using fractional values as probabilities or parameters.
- **Alteration** repairs violations after an initial randomized or deterministic rounding.
- **Dependent rounding** correlates choices to preserve totals or improve concentration.
- The **integrality gap** is the worst ratio between integer and relaxation optima under a fixed formulation.
- A **certified bound** is a solver result whose feasibility and rounding direction have been checked for the inequality claimed.

### Central model, mechanism, or theorem

The standard LP for weighted vertex cover minimizes $\sum_v w_vx_v$ subject to $x_u+x_v\ge1$ for every edge and $0\le x_v\le1$. Select $C=\{v:x_v\ge1/2\}$. Every edge has an endpoint in $C$, and $\mathbf1[v\in C]\le2x_v$, so

$$
w(C)\le2\sum_vw_vx_v=2LP\le2OPT.
$$

The proof contains three separate facts: relaxation direction, rounded feasibility, and coordinate-wise cost domination. Thresholding is not generally valid when constraints or coefficients differ.

### Critical invariants

- Every integer solution embeds into the relaxation with the same declared objective.
- Solver status is optimal and the bound direction is safe before it is used as a certificate.
- Rounded variables satisfy the original constraints, not merely relaxed constraints within tolerance.
- Thresholds, sampling probabilities, and repair rules match the proof.
- Objective and constraints are recomputed from exported values with checked arithmetic.
- Randomized claims state expectation, tail probability, independence, and repetition.
- Infeasible, unbounded, approximate, timed-out, and numerically suspect solves do not inherit the theorem.

### Common failures

Common failures include writing a relaxation that excludes valid integer solutions; assuming componentwise nearest rounding preserves coupling constraints; proving expected cost but not feasibility; using independent rounding where cardinality must be exact; treating a solver's rounded display as exact; accepting constraint tolerance as business feasibility; dividing by an unverified LP value; ignoring integrality gaps; and reporting the best randomized trial without a valid probability and selection argument.

### Compact example

For one edge $(u,v)$, the LP constraint $x_u+x_v\ge1$ ensures at least one endpoint is at least $1/2$. Rounding both values by the threshold covers the edge. If both are $1/2$, both are selected: cost can double the fractional cost locally, exactly matching the proof's factor.

### Connections

[ALGE-062](./062-greedy-approximation.md) proves factors from local progress. [ALGE-064](../ROADMAP.md#block-07--approximation-heuristics-and-randomized-algorithms) constructs solutions together with dual bounds. Database and Data Engineering own model provenance; Testing owns finite solver and rounding evidence.

## Governing Question

Given an IP formulation, an LP solver result, and a rounding rule, how do we prove the relaxation is valid, restore integrality and feasibility, bound the rounded objective, and make the implementation's status, tolerances, and random choices auditable?

Rounding is not a generic final call to `round()`. It is an algorithm designed around the geometry of one relaxation and one problem. The same fractional vector can support a strong theorem, no theorem, or an infeasible result depending on the rounding rule.

## Why This Matters

Linear programming supplies both an efficiently solvable fractional model and an optimum-relative bound. Fractional variables expose where combinatorial decisions can share responsibility. Rounding converts that structure into an implementable solution while measuring the price of integrality.

The method also exposes formulation quality. A weak relaxation may have a large integrality gap even when solved exactly. Adding valid inequalities can strengthen it but increase solve cost. Randomized rounding can preserve expectations elegantly, yet constraints may fail unless concentration or repair is proved.

In production, solver statuses and floating tolerances are part of correctness. A numerical value called “optimal” in logs is not automatically a rigorous lower bound, and a near-feasible vector may violate a hard capacity after rounding.

## Prerequisites and Retrieval

Retrieve [ALGE-061](./061-approximation-ratios-and-guarantees.md), [ALGE-062](./062-greedy-approximation.md), linear programs and duality, integer formulations, convexity, expectation, union and Chernoff bounds, exact rational arithmetic, and graph vertex cover.

This chapter covers LP relaxation, deterministic thresholding, randomized rounding, alteration, dependence, formulation gaps, and solver evidence. ALGE-064 owns primal-dual algorithms; semidefinite rounding is mentioned only as a distinct stronger relaxation.

## Learning Objectives

After completing this module, you should be able to:

1. prove that an LP is a relaxation of an IP;
2. identify the correct bound direction for minimization and maximization;
3. derive deterministic threshold-rounding feasibility and cost bounds;
4. analyze randomized cost by linearity of expectation;
5. use probability bounds to control constraint failure;
6. explain when alteration or dependent rounding is required;
7. measure and interpret an integrality gap;
8. preserve guarantees through preprocessing and numerical solving;
9. verify exported solutions and certificates independently; and
10. report solver, rounding, randomness, and fallback evidence honestly.

## Core Exposition

### Build a relaxation before rounding

For a minimization IP with feasible set $F_{IP}$, an LP is a relaxation when every integer feasible point is LP-feasible and objectives agree on those points. Thus $F_{IP}\subseteq F_{LP}$ and

$$
LP=\min_{x\in F_{LP}}c^Tx\le\min_{x\in F_{IP}}c^Tx=OPT.
$$

For maximization, enlarging the feasible set gives $LP\ge OPT$. Reversing this direction destroys the certificate chain. Valid inequalities may shrink $F_{LP}$ while retaining every integer point, strengthening the bound.

The formulation includes scaling, units, index sets, omitted variables, and big-$M$ constants. An apparently harmless overly small $M$ can exclude valid integer solutions; an enormous $M$ can weaken bounds and numerical conditioning.

### Round vertex cover at one half

For graph $G=(V,E)$ and nonnegative weights $w_v$, the integer model uses $x_v\in\{0,1\}$ and constraints $x_u+x_v\ge1$. Relax to $0\le x_v\le1$, solve, and choose every $v$ with $x_v\ge1/2$.

For any edge, both endpoints cannot be below $1/2$, so the rounded set covers it. For each vertex, rounded indicator $y_v\le2x_v$. Multiplying by $w_v\ge0$ and summing gives $w^Ty\le2w^Tx$. When $x$ is LP-optimal, $w^Tx=LP\le OPT$.

Nonnegative weights are used in the summation inequality. A threshold other than one half changes feasibility or factor. Constraints involving three variables, capacities, or equality are not covered by this edge proof.

This teaching implementation enumerates half-integral points as a finite oracle. The half-integrality of the vertex-cover LP is structural; enumeration is not a general LP solver.

<!-- bijux-verify: {"id":"vertex-cover-lp-threshold-rounding","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"path fractional=(0.5, 0.5, 0.5, 0.5) lp=2.0 rounded=(0, 1, 2, 3) optimum=(0, 2)\ntriangle fractional=(0.5, 0.5, 0.5) lp=1.5 rounded=(0, 1, 2) optimum=(0, 1)\nstar fractional=(1.0, 0.0, 0.0, 0.0) lp=1.0 rounded=(0,) optimum=(0,)\n","stderr":""}} -->
```python
from itertools import combinations, product


def fractional_optimum(vertices, edges):
    best = None
    for values in product((0.0, 0.5, 1.0), repeat=len(vertices)):
        x = dict(zip(vertices, values))
        if all(x[u] + x[v] >= 1.0 for u, v in edges):
            # Among equal optima, prefer the point with more fractional
            # coordinates so this example exercises threshold rounding.
            candidate = (sum(values), -values.count(0.5), values)
            if best is None or candidate < best:
                best = candidate
    return best[2]


def integer_optimum(vertices, edges):
    for size in range(len(vertices) + 1):
        for chosen in combinations(vertices, size):
            if all(u in chosen or v in chosen for u, v in edges):
                return chosen


cases = {
    "path": ((0, 1, 2, 3), ((0, 1), (1, 2), (2, 3))),
    "triangle": ((0, 1, 2), ((0, 1), (1, 2), (0, 2))),
    "star": ((0, 1, 2, 3), ((0, 1), (0, 2), (0, 3))),
}
for name, (vertices, edges) in cases.items():
    fractional = fractional_optimum(vertices, edges)
    rounded = tuple(v for v, value in zip(vertices, fractional) if value >= 0.5)
    optimum = integer_optimum(vertices, edges)
    print(
        f"{name} fractional={fractional} lp={sum(fractional)} "
        f"rounded={rounded} optimum={optimum}"
    )
```

### Diagnose the integrality gap

For minimization, the instance gap is $OPT/LP$ when $LP>0$. The formulation's gap is the supremum over its instance class. Threshold rounding proves both an algorithmic factor and an upper bound of two on the vertex-cover LP gap. Odd cycles show a nontrivial gap: a triangle has LP value $3/2$ and integer optimum 2.

An integrality gap limits proofs that compare only to that LP. It does not prove hardness for all algorithms. Stronger inequalities, hierarchies, extended formulations, or a different relaxation may tighten it at additional computational cost.

If $LP=0$, ratio is undefined; handle zero separately. A negative objective or free variables may make multiplicative gaps inappropriate.

### Analyze independent randomized rounding

Suppose a fractional solution has $x_i\in[0,1]$. Independently select item $i$ with probability $p_i=\min\{1,\alpha x_i\}$. For nonnegative costs,

$$
\mathbb E[c^Ty]=\sum_i c_i\Pr[y_i=1]\le\alpha c^Tx
$$

by linearity of expectation; independence is not needed for this equality. Independence matters for many concentration and constraint-failure bounds.

For a covering constraint, scale probabilities enough that the probability all useful items fail is small, then union-bound across constraints. For packing, independent selection can exceed capacities; scale down, use concentration, reject and repeat, or alter the selection. The final theorem must account for both objective and every feasibility event.

Expected cost alone does not guarantee one run is feasible or cheap. Markov's inequality, Chernoff bounds, conditional expectation, repetition, or repair may turn expectation into a usable probability statement, each with explicit premises.

### Repair by alteration

Alteration first rounds, then repairs violated constraints or removes conflicting items. Its analysis charges expected repair cost or lost value to fractional structure. The repair must terminate and produce original feasibility.

For covering, add a deterministic fallback set for each uncovered demand. For packing, discard items contributing to overload. Naive repair can destroy the approximation: one expensive fallback or many correlated deletions may dominate. Analyze the distribution of violations and repair multiplicity.

Record both sampled and repaired solutions. A verifier checks only the final object's feasibility and value, while the proof also relies on the generation process to establish expected quality.

### Preserve totals with dependent rounding

Independent Bernoulli choices fluctuate around $\sum_i x_i$. When a cardinality or assignment total must be exact, dependent rounding correlates choices while preserving marginal probabilities and selected sums, often with useful negative-correlation properties.

Correlation is not an implementation nuisance. It is the mechanism satisfying coupled constraints. Sampling each variable independently and clipping excess choices changes marginals and can bias value. Use a proved dependent-rounding algorithm for the relevant polytope.

Derandomization by conditional expectations fixes random choices one at a time while keeping a pessimistic estimator or conditional expected objective within its bound. The estimator must upper-bound failure or lower-bound value after every fixing decision and be computable efficiently.

### Treat solver numerics as evidence, not axioms

LP solvers generally use floating arithmetic and feasibility tolerances. Export status, primal values, objective, dual bound, residuals, tolerances, scaling, solver/version, and termination reason. Independently recompute original constraints and the rounded objective.

A minimization value rounded upward is not necessarily a lower bound. A validated dual feasible solution gives a lower bound; use exact rational reconstruction or conservative outward rounding when a rigorous certificate is required. “Optimal within tolerance” must be translated into the approximation inequality with a proved numerical slack.

Threshold comparisons near $1/2$ need policy. Rounding $0.4999999999$ down may uncover an edge when residual tolerance allowed both endpoints below half. Repair feasibility and include its cost in analysis, or compute with certified values. Never quietly change threshold to make tests pass.

### Preserve the proof across engineering choices

Preprocessing may fix variables, remove dominated constraints, scale coefficients, or decompose components. Prove reconstruction feasibility and objective correspondence. Warm starts affect search, not the relaxation's mathematical optimum, but early termination changes the bound available.

Large LPs may use separation or column generation. A restricted master solution can have the wrong bound direction unless missing columns/constraints and dual pricing conditions are handled. A heuristic fractional solution is not LP-optimal; rounding it may remain feasible but lose the $LP\le OPT$ certificate chain.

Parallel sampling must reproduce the specified random variables. Counter-based generators keyed by instance, trial, and variable give replayable draws without order dependence. Do not reuse seeds across security-sensitive contexts or infer independence merely from different thread IDs.

### Validate and publish the rounded result

For every result, bind instance/model digest, formulation/version, solver/version and status, primal and certified bound, residuals and tolerances, rounding algorithm/version, threshold or probability scale, seed/trial, alteration, final feasibility, recomputed objective, and guarantee status.

Test tiny instances against exact IP and rational LP oracles; include gap witnesses, threshold boundaries, redundant constraints, zero weights, skewed coefficients, infeasible/unbounded models, and repair-heavy random trials. Statistical tests can catch distribution defects but do not prove tail inequalities.

On timeout, return a rounded feasible solution with an instance-specific certified gap only if a valid bound exists and the rounding/repair completed. Otherwise label it feasible-uncertified, partial, numerical failure, infeasible, or unknown as appropriate.

## Definitions and Notation

Let $F_{IP}\subseteq F_{LP}$ be integer and relaxed feasible regions, $c$ the objective vector, $x$ a fractional solution, $y$ its discrete rounding, and $LP$, $OPT$, and $A$ the relaxation, integer optimum, and rounded objective values.

- A **valid inequality** holds for every integer feasible solution.
- A **rounding threshold** maps fractional coordinates to discrete choices under a proved rule.
- A **marginal probability** is the probability one coordinate is selected, regardless of dependence.
- A **tail bound** controls deviation probability beyond a threshold.
- A **pessimistic estimator** is a tractable bound maintained during derandomization.
- A **primal residual** measures constraint violation; a **dual certificate** supports an objective bound.
- **Outward rounding** directs numeric error so a claimed bound remains conservative.

## Mechanisms, Invariants, or Proof Structure

### Three-link proof chain

For minimization, prove (1) $LP\le OPT$ because every integer solution is relaxation-feasible; (2) rounded $y\in F_{IP}$; and (3) $c^Ty\le\alpha c^Tx=\alpha LP$. Chaining yields $A\le\alpha OPT$. Each link can fail independently.

### Threshold-cover invariant

Every edge constraint has at least one endpoint at or above half. Selecting all such endpoints covers every edge. Nonnegative coordinate costs allow $y_v\le2x_v$ to be summed. The final verifier directly checks every edge and recomputes weights.

### Randomized-rounding obligations

Define the probability space, marginals, dependence, expected objective, per-constraint failure event, simultaneous feasibility probability, repair, and repetition/selection. Show polynomial sampling and verification. One expected-value line is not a full approximation proof.

### Numerical certificate invariant

The bound used in a ratio is conservative for the exact modeled problem; exported values satisfy stated residual limits; final integer feasibility is checked under business rules; and numerical slack is included in the reported factor rather than hidden.

## Alternatives and Trade-Offs

| Method | Benefit | Risk | Evidence |
|---|---|---|---|
| Threshold rounding | Deterministic and transparent | Problem-specific feasibility threshold | Coordinate inequality proof |
| Independent rounding | Simple expectations and concentration | Coupled constraints can fail | Tail and union-bound analysis |
| Alteration | Restores feasibility | Repair may dominate cost/value | Repair charging proof |
| Dependent rounding | Preserves totals/correlation properties | More complex sampler | Marginal and dependence proof |
| Conditional expectation | Deterministic guarantee | Needs computable estimator | Per-decision invariant |
| Stronger LP | Better bound/gap | Larger solve cost | Validity and solver evidence |
| SDP rounding | Captures quadratic geometry | Different solver and analysis | SDP-specific theorem |
| Heuristic rounding | Often fast | No inherited factor | Explicit heuristic label and oracle tests |

## Failure Modes and Misconceptions

- **“Relaxing integrality always gives the right bound.”** Only if every integer feasible point remains feasible with the same objective.
- **“Round to nearest.”** Coupled constraints can become infeasible.
- **“Expected cost proves an approximation.”** Simultaneous feasibility and probability of quality remain.
- **“Independence is always desirable.”** It can violate exact totals that dependence preserves.
- **“Repair is free.”** Alteration cost or lost value belongs in the factor.
- **“The integrality gap is NP-hardness.”** It describes one formulation.
- **“Solver optimal means exact lower bound.”** Status, tolerance, and rounding direction matter.
- **“0.499999 is one half.”** Business feasibility and theorem thresholds cannot be inferred from display rounding.
- **“A restricted LP is a relaxation bound.”** Missing columns or constraints can reverse usefulness.
- **“More trials guarantee success.”** Repetition needs probability and dependence analysis.
- **“A feasible rounded solution keeps the theorem after timeout.”** It needs a valid bound and completed proof path.
- **“Random seed is the evidence.”** It enables replay; it does not prove the distribution theorem.

## Worked Examples

### Example 1

**Situation.** One vertex-cover edge has $x_u=0.4$, $x_v=0.6$.

The LP constraint holds with equality. Half-threshold rounding selects $v$ and covers the edge. Indicators satisfy $y_u=0\le0.8$ and $y_v=1\le1.2$.

**Conclusion.** The threshold proves both edge feasibility and coordinate cost domination.

### Example 2

**Situation.** Triangle vertices all have $x=1/2$.

Fractional cost is $3/2$. Threshold rounding selects all three, cost 3, while an integer optimum chooses two. Rounded-to-LP ratio is 2; realized integer ratio is $3/2$.

**Conclusion.** LP and integer comparisons answer different gap questions.

### Example 3

**Situation.** A minimization IP optimum is 100 and a valid LP optimum is 70.

The instance integrality gap is $100/70=10/7$. A rounded solution costing 130 has certificate $130/70=13/7$, even though its realized ratio is 1.3.

**Conclusion.** A weak relaxation makes the available certificate looser than realized quality.

### Example 4

**Situation.** Independent rounding selects items with costs 2, 5, 7 at probabilities 0.2, 0.5, 1.

Expected cost is $2(0.2)+5(0.5)+7(1)=9.9$ by linearity. This calculation does not say that every sample costs at most 9.9 or satisfies constraints.

**Conclusion.** Expected objective is one proof component, not a deterministic outcome.

### Example 5

**Situation.** Ten constraints each fail with probability at most 0.01.

The union bound gives probability of any failure at most 0.10, without independence. Thus simultaneous feasibility is at least 0.90. This may be too weak for production and says nothing about repair cost.

**Conclusion.** Per-constraint probability must be lifted to a whole-solution statement.

### Example 6

**Situation.** Fractional assignments sum exactly to 20, but independent Bernoulli rounding produces 24 selections.

If exactly 20 is hard, the sample is infeasible. Dropping four arbitrary items changes marginals and value. Use dependent rounding that preserves the sum, or analyze a specified repair.

**Conclusion.** Coupled totals require more than independent marginal preservation.

### Example 7

**Situation.** A solver prints $x_u=x_v=0.4999999998$ for an edge and reports feasibility tolerance $10^{-6}$.

Both round down under the exact half threshold, leaving the edge uncovered. Direct feasibility verification catches this. Certified reconstruction, tightened solve, or analyzed repair is required; formatting both as 0.5 is not evidence.

**Conclusion.** Solver tolerance does not relax the output contract automatically.

### Example 8

**Situation.** A minimization solver reports primal 125 and dual bound 100 at timeout.

If the dual is validated and a rounded feasible solution costs 140, the instance certificate is $140/100=1.4$. The primal fractional 125 is not a lower bound merely because it is feasible; for minimization it is an upper bound on LP optimum.

**Conclusion.** Use the correct certified bound and distinguish solver incumbents.

### Example 9

**Situation.** Random rounding succeeds per independent trial with probability at least 0.8.

Three trials all fail with probability at most $0.2^3=0.008$. Selecting the cheapest verified feasible result preserves feasibility and improves minimization cost among successes. Correlated seeds invalidate this multiplication.

**Conclusion.** Repetition needs independence and direction-correct selection.

### Example 10

**Situation.** Adding a valid inequality raises a minimization LP bound from 50 to 80; rounded solution remains cost 100.

Certificate improves from $100/50=2$ to $100/80=1.25$. The solution did not change; formulation strength improved its proof. Solve time and numeric conditioning must still be measured.

**Conclusion.** Stronger relaxations can improve guarantees without changing rounding output.

## Cross-Program Connections

- **Algorithms:** [ALGE-061](./061-approximation-ratios-and-guarantees.md) defines factors; [ALGE-064](../ROADMAP.md#block-07--approximation-heuristics-and-randomized-algorithms) builds primal and dual certificates together.
- **Theory of Computation:** owns hardness and formulation-complexity limits.
- **Data Structures:** owns sparse matrices, separation structures, and reproducible samplers.
- **Database Engineering:** owns declarative constraint modeling, solver-input provenance, and transactionally published decisions.
- **Software Testing:** owns exact small oracles, constraint replay, numerical boundary cases, and distribution checks.
- **Platform Engineering:** owns solver versions, resources, seeds, timeout semantics, and certificate telemetry.

## References

1. David P. Williamson and David B. Shmoys, [“Deterministic Rounding of Linear Programs”](https://www.cambridge.org/core/books/abs/design-of-approximation-algorithms/deterministic-rounding-of-linear-programs/D4F4FE47718887B638C0C00FDC1D9486), in *The Design of Approximation Algorithms*, Cambridge University Press, 2011, doi:10.1017/CBO9780511921735.005. Graduate treatment; publisher record checked 2026-09-05.
2. Vijay V. Vazirani, [*Approximation Algorithms*](https://link.springer.com/book/10.1007/978-3-662-04565-7), Springer, 2001/2003, doi:10.1007/978-3-662-04565-7. LP relaxation, rounding, and integrality-gap reference.
3. George L. Nemhauser and Leslie E. Trotter, “Vertex Packings: Structural Properties and Algorithms,” *Mathematical Programming* 8, 232–248, 1975, [doi:10.1007/BF01580444](https://doi.org/10.1007/BF01580444). Primary half-integral vertex-packing structure source; bibliographic record checked 2026-09-05.
4. Prabhakar Raghavan and Clark D. Thompson, “Randomized Rounding: A Technique for Provably Good Algorithms and Algorithmic Proofs,” *Combinatorica* 7, 365–374, 1987, [doi:10.1007/BF02579324](https://doi.org/10.1007/BF02579324). Primary randomized-rounding source; archival record checked 2026-09-05.
5. Michel X. Goemans and David P. Williamson, “Improved Approximation Algorithms for Maximum Cut and Satisfiability Problems Using Semidefinite Programming,” *Journal of the ACM* 42(6), 1115–1145, 1995, [doi:10.1145/227683.227684](https://doi.org/10.1145/227683.227684). Primary SDP-rounding source; author and DOI records checked 2026-09-05.
6. Alexander Schrijver, *Theory of Linear and Integer Programming*, Wiley, 1986, ISBN 978-0471908548. Linear/integer formulation, duality, and polyhedral reference.
7. Rajeev Motwani and Prabhakar Raghavan, *Randomized Algorithms*, Cambridge University Press, 1995, [doi:10.1017/CBO9780511814075](https://doi.org/10.1017/CBO9780511814075). Probability, concentration, derandomization, and randomized algorithms reference.

## Exercises

### Exercise 1

Prove the bound direction of an LP relaxation for minimization and maximization. State the two facts needed beyond that direction to obtain an approximation theorem by rounding.

### Exercise 2

For a four-cycle with every $x_v=1/2$ and unit weights, perform threshold rounding, verify every edge, compute LP and rounded costs, and compare with integer optimum.

### Exercise 3

A solver returns `optimal_inaccurate`, values within $10^{-5}$ of constraints, and a printed minimization objective 200. Code rounds near-half values to nearest integer and claims factor two. Diagnose the evidence gaps and design a safe verification path.

### Exercise 4

Compare independent rounding with dependent rounding for selecting exactly 100 items from fractional variables summing to 100. Address marginals, objective expectation, feasibility, concentration, implementation, and replay.

### Exercise 5

A cloud-placement IP uses capacities, regional redundancy, and latency penalties. Its LP is rounded independently, then overloaded regions are repaired by dropping arbitrary replicas. Design an honest analysis and production result contract, or explain why the output remains heuristic.

## Answers to the Exercises

### Answer 1

Relaxation means every integer feasible solution is LP-feasible with the same objective. Enlarging a minimization feasible set can only lower its optimum, so $LP\le OPT$; enlarging a maximization set can only raise it, so $LP\ge OPT$. Rounding must additionally prove that its discrete output is feasible for the original problem and that its objective is within the claimed factor of the relaxation bound. Termination and polynomial runtime complete the algorithmic claim.

### Answer 2

Every vertex is at one half, so threshold rounding selects all four. Each cycle edge has both endpoints selected and is covered. LP cost is $4(1/2)=2$; rounded cost is 4. The integer optimum is 2, obtained by alternating vertices, so rounded-to-LP factor is 2 and realized ratio is also 2. This is valid despite another LP optimum corresponding to the alternating integer cover.

### Answer 3

`optimal_inaccurate` does not itself supply an exact LP optimum or certified lower bound. Near-feasibility may put both endpoints below half, and nearest rounding has no vertex-cover feasibility proof. Export full precision, status, residuals, tolerances, and a validated dual; reconstruct or conservatively round a lower bound. Apply the proved half-threshold rule to certified values, then directly verify every original edge and recompute cost. If repair is needed, analyze its cost or report the result feasible-uncertified. Distinguish numerical failure, timeout, and certified completion.

### Answer 4

Independent rounding preserves each marginal and hence expected linear objective, but selected count fluctuates and violates the exact-100 constraint in most samples. Dependent rounding can preserve the sum exactly while retaining marginals and often negative-correlation concentration, but requires a problem-specific sampler and proof. Validate the final count, eligibility, and objective; test empirical marginals across many seeds without treating that as proof. Use counter-based or recorded random streams for replay, record algorithm/version and seed, and select only by a rule covered by the analysis.

### Answer 5

Independent placement can violate capacities and redundancy simultaneously. Arbitrary dropping may remove the only cross-region replica, distort marginals, and make latency or durability arbitrarily poor, so no LP-derived factor follows. A valid design needs a relaxation and dependent/iterative rounding or alteration theorem covering capacity, redundancy, and objective, plus a repair whose loss is bounded. The service records model digest, solver bound/status, rounding seed, violations, repair, final hard-constraint verification, recomputed objective, and certificate. Without that proof, label the output heuristic, reject hard-constraint violations, and evaluate against exact/strong-bound small instances and adversarial regional failures.
