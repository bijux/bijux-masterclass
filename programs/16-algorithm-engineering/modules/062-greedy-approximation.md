---
module_id: ALGE-062
program: Algorithm Engineering
level: 2
module_number: 62
title: Greedy Approximation
status: complete
last_verified: 2026-09-05
---

# Greedy Approximation

## One-Page Review

### Governing question

When does repeatedly taking the locally best feasible choice yield a provable global approximation, and how should an engineer implement the marginal rule, certificate, numerical comparisons, and fallback behavior without silently weakening the theorem?

### Essential definitions

- A **greedy algorithm** commits to a locally ranked choice and does not revoke it in its core execution.
- **Marginal gain** is $f(S\cup\{x\})-f(S)$; **marginal cost-effectiveness** can be cost divided by newly covered demand.
- A set function is **monotone** when adding elements never lowers its value.
- A set function is **submodular** when marginal gain cannot increase as the selected set grows.
- **Charging** assigns algorithm cost to atomic demands so their total charge equals the returned cost and each optimum unit receives bounded charge.
- An **exchange argument** transforms an optimum to agree with greedy choices while controlling objective loss.
- A **residual argument** bounds how much unmet value remains after each choice.
- A **tie policy** is part of deterministic behavior even when every tie preserves the same theorem.

### Central model, mechanism, or theorem

For unweighted set cover on universe $U$, greedy repeatedly chooses a set covering the most uncovered elements. If $r$ elements remain and an optimum uses $k=OPT$ sets, some optimum set covers at least $r/k$ remaining elements. Greedy covers at least that many. Charging each newly covered element $1/g$ when a chosen set covers $g$ new elements bounds the total charge assigned to the elements of any optimum set by the harmonic number $H_{|U|}$, yielding at most $H_{|U|}OPT$ sets.

For monotone submodular maximization under a cardinality limit $k$, maximum-marginal greedy leaves residual at most $(1-1/k)^iOPT$ after $i$ choices and therefore returns at least $[1-(1-1/k)^k]OPT\ge(1-1/e)OPT$.

### Critical invariants

- Candidate gains and costs are computed against the current state, not stale state.
- Every committed choice preserves feasibility and makes the progress measure advance.
- Tie-breaking is deterministic or its randomization is included in the guarantee.
- Zero-cost, zero-gain, negative-gain, and infeasible residual cases are explicit.
- The proof's lower/upper bound is recomputed under weighted, capacitated, or transformed variants.
- Lazy evaluation validates stale upper bounds before selection.
- Output contains enough trace or certificate to replay choices and objective value.

### Common failures

Common failures include assuming every greedy rule has a guarantee; optimizing raw gain when costs differ; counting already-covered elements; using submodular analysis for complementary rewards; treating a maximal solution as maximum; hiding nondeterministic ties; comparing floating ratios by unsafe division; accepting zero-gain loops; using stale lazy-heap keys as exact gains; and citing a worst-case factor after timeouts, candidate pruning, or distributed races change the selection rule.

### Compact example

Universe is $\{1,2,3,4,5,6\}$. Sets are $A=\{1,2,3,4\}$, $B=\{1,2,5\}$, and $C=\{3,4,6\}$. Greedy chooses $A$ for gain four, then needs both $B$ and $C$, using three sets. Optimum uses $B,C$, so realized ratio is $3/2$. Local best first does not imply optimal, but a separate harmonic argument still bounds it.

### Connections

[ALGE-061](./061-approximation-ratios-and-guarantees.md) defines the contract proved here. [ALGE-063](../ROADMAP.md#block-07--approximation-heuristics-and-randomized-algorithms) derives guarantees by rounding linear programs. Data Structures owns priority and lazy-gain structures; Software Testing owns bounded exact oracles and trace replay.

## Governing Question

Given a discrete optimization problem and a proposed local scoring rule, how can we determine whether greedy choices preserve feasibility, force measurable progress, relate to an optimum through charging, exchange, or residual decay, and remain faithful under implementation optimizations?

“Choose the best next item” is an algorithm only after best, candidate, state, feasibility, stopping, and ties are defined. It is an approximation algorithm only after a universal quality proof covers the declared instance class.

## Why This Matters

Greedy algorithms are attractive because they are incremental, explainable, and often fast. They can stream over candidates, produce usable prefixes, and expose a trace of decisions. In set cover, scheduling, facility placement, and submodular selection, carefully chosen local rules have rigorous bounds.

The same simplicity invites overclaiming. A natural-looking score can be arbitrarily bad when costs, interactions, precedence, or complementarity violate the proof. Production shortcuts—cached gains, batching, approximate nearest neighbors, parallel winners—may define a different algorithm.

The durable skill is not memorizing greedy recipes. It is identifying a progress measure and an optimum-relative lemma, then preserving their premises through data representation, arithmetic, and execution.

## Prerequisites and Retrieval

Retrieve [ALGE-061](./061-approximation-ratios-and-guarantees.md), set cover, matchings and matroids, harmonic sums, recurrence solving, conditional expectation, exact rational comparison, and priority queues. Understand the difference between feasibility, maximality, local optimality, and global optimality.

This chapter derives greedy set-cover and monotone-submodular guarantees and surveys exchange and scheduling arguments. Linear-program rounding, primal-dual construction, general local search, and randomized algorithms are owned by ALGE-063 through ALGE-068.

## Learning Objectives

After completing this module, you should be able to:

1. specify a greedy state, candidate rule, tie policy, and stop condition;
2. distinguish greedy construction from arbitrary heuristics and local search;
3. derive the harmonic set-cover bound by charging;
4. derive residual decay for monotone submodular maximization;
5. recognize when an exchange argument proves exactness or approximation;
6. select cost-effectiveness rather than raw gain for weighted cover;
7. preserve guarantees under lazy evaluation and deterministic parallelism;
8. compare marginal ratios without overflow or unstable division;
9. verify feasibility, trace, objective, and certificates independently; and
10. combine worst-case analysis with adversarial and workload evaluation.

## Core Exposition

### Define the greedy state machine

Let $S_i$ be the partial solution after $i$ commitments. A complete specification defines candidate set $X(S_i)$, feasibility predicate, score $g(x\mid S_i)$, deterministic or randomized tie rule, update $S_{i+1}=S_i\cup\{x_i\}$, and stop condition.

Termination usually follows from a finite ground set and strict progress: every step adds an unselected element, covers at least one new demand, or decreases a nonnegative integer residual. If no candidate makes progress while requirements remain, the instance is infeasible under the represented candidates or the implementation has lost information. It must not loop or return “complete.”

Greedy is different from local search. Greedy constructs forward without revocation; local search starts from a feasible solution and replaces parts. Hybrid algorithms are legitimate, but the proof must analyze the actual composition.

### Derive greedy set cover

In unweighted set cover, universe $U$ must be covered by selected subsets from family $\mathcal S$. At each step choose a set maximizing the number of uncovered elements it contains.

Let $k=OPT$. When $r$ elements remain, the $k$ optimum sets collectively cover them, so at least one covers $r/k$ by averaging. Greedy covers $g\ge r/k$ and leaves at most

$$
r'\le r\left(1-\frac1k\right).
$$

This recurrence gives a logarithmic stopping intuition. A sharper charging proof charges $1/g$ to every element newly covered by a chosen set. Total charge equals one per selected set. Order the elements of any optimum set by when greedy covers them. When its $j$th still-uncovered element is charged, at least the remaining elements of that optimum set were available together, so its charge is at most the reciprocal of that remaining count. Charges to that optimum set total at most $H_d=\sum_{i=1}^d1/i$, where $d$ is its size; summing over optimum sets gives an $H_{|U|}$ bound. Tighter statements use maximum set size.

The executable implementation shows a nonoptimal result and emits its choices. Its representation is a teaching model, not a compressed industrial set system.

<!-- bijux-verify: {"id":"greedy-unweighted-set-cover","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"chosen=('A', 'B', 'C')\ncovered=(1, 2, 3, 4, 5, 6)\noptimum=('B', 'C')\nrealized_ratio=1.5\ninfeasible=rejected\n","stderr":""}} -->
```python
from itertools import combinations


def greedy_cover(universe, subsets):
    uncovered = set(universe)
    chosen = []
    while uncovered:
        name, members = min(
            subsets.items(),
            key=lambda item: (-len(uncovered & item[1]), item[0]),
        )
        gain = uncovered & members
        if not gain:
            raise ValueError("universe is not coverable")
        chosen.append(name)
        uncovered -= gain
    return tuple(chosen)


def optimum_cover(universe, subsets):
    names = tuple(sorted(subsets))
    for size in range(len(names) + 1):
        for chosen in combinations(names, size):
            if set().union(*(subsets[name] for name in chosen)) >= set(universe):
                return chosen
    raise ValueError("universe is not coverable")


universe = set(range(1, 7))
subsets = {
    "A": {1, 2, 3, 4},
    "B": {1, 2, 5},
    "C": {3, 4, 6},
}
chosen = greedy_cover(universe, subsets)
optimum = optimum_cover(universe, subsets)
covered = set().union(*(subsets[name] for name in chosen))
print(f"chosen={chosen}")
print(f"covered={tuple(sorted(covered))}")
print(f"optimum={optimum}")
print(f"realized_ratio={len(chosen) / len(optimum)}")
try:
    greedy_cover({1, 2}, {"only-one": {1}})
except ValueError:
    print("infeasible=rejected")
```

### Generalize to weighted cover safely

When set $S$ costs $c(S)>0$, maximizing raw new coverage ignores cost. Choose minimum density

$$
\frac{c(S)}{|S\cap R|},
$$

where $R$ is uncovered demand. Charge that density to every newly covered element. The weighted charging proof yields a harmonic factor under the stated positive-cost model.

Compare $c_1/g_1<c_2/g_2$ by cross multiplication $c_1g_2<c_2g_1$ with exact integers or checked wide arithmetic. Floating division can invert nearly equal choices, produce NaN for zero gain, or violate deterministic ties. Exclude zero-gain candidates before comparison. Zero-cost positive-gain sets should be selected under a specified tie rule; negative costs change the model and proof.

Weighted elements or partial-cover targets need a corresponding residual measure. Reusing the unweighted denominator without re-deriving charges is not a harmless implementation detail.

### Use exchange arguments when choices can be reconciled

An exchange proof compares greedy solution $G$ with an optimum $O$. At each greedy choice, transform $O$ to include that choice by removing or replacing bounded structure, showing feasibility remains and objective degrades by at most a controlled amount.

For maximum-weight independent sets in a matroid, choosing the heaviest feasible element is exact: the matroid exchange property lets an optimum be transformed to include each greedy choice without losing total weight. In general independence systems that exchange property fails; the same code can be arbitrarily bad.

For approximation, one greedy choice may displace at most $b$ optimum objects of no greater value, yielding a $b$-style charging bound. The map from optimum objects to greedy choices must bound multiplicity. Saying “charge optimum to greedy” without defining the map and its congestion is not a proof.

### Derive submodular residual decay

A set function $f:2^V\to\mathbb R_{\ge0}$ is normalized if $f(\varnothing)=0$, monotone if $f(A)\le f(B)$ for $A\subseteq B$, and submodular if for $A\subseteq B$ and $x\notin B$,

$$
f(A\cup\{x\})-f(A)\ge f(B\cup\{x\})-f(B).
$$

Under cardinality limit $k$, greedy selects maximum marginal gain. Let $S_i$ be its first $i$ elements and $O$ an optimum of size at most $k$. Monotonicity and submodularity imply the remaining optimum elements' marginals from $S_i$ sum to at least $OPT-f(S_i)$. One has marginal at least that residual divided by $k$, and greedy is no worse. Thus


$$
OPT-f(S_{i+1})\le\left(1-\frac1k\right)(OPT-f(S_i)).
$$

After $k$ steps, $f(S_k)\ge[1-(1-1/k)^k]OPT\ge(1-1/e)OPT$. Normalization, monotonicity, submodularity, exact marginal choice, and a pure cardinality constraint are premises. Costs, matroid constraints, nonmonotonicity, approximate value oracles, and noisy gains require altered algorithms and bounds.

### Recognize scheduling's lower bounds

For $m$ identical machines and jobs with processing times $p_j$, list scheduling assigns each next job to a least-loaded machine. Let $C$ be its makespan and job $j$ finish last. Its start time is at most total earlier work divided by $m$. Therefore

$$
C\le\frac{\sum_i p_i-p_j}{m}+p_j
\le OPT+\left(1-\frac1m\right)OPT
=\left(2-\frac1m\right)OPT,
$$

using lower bounds $OPT\ge\sum_i p_i/m$ and $OPT\ge p_j$. Ordering jobs by decreasing processing time yields a stronger theorem, but only under its own premises. Release times, related machines, setup costs, precedence, or migration change the problem.

### Optimize greedy execution without changing selection

Naively recomputing every marginal each round can be expensive. For monotone submodular functions, marginal gains only decrease, enabling **lazy greedy**: keep upper bounds in a max-heap, recompute the current leader, and select it only when its refreshed gain remains at least every other valid upper bound.

The heap key is not necessarily the current gain. Failing to refresh before commitment changes the algorithm and can invalidate the proof. Version state and use deterministic comparison for ties. If gain evaluation is approximate within a proved tolerance, carry that error through the residual recurrence.

Batch and parallel variants may select several items from the same stale state. Their combined gain can be far below the sum of individual gains because of overlap. Either serialize commits, recompute conflicts, or use a parallel approximation theorem that analyzes stale batches.

### Test greedy algorithms against the proof

Test three layers. Structural tests replay feasibility, progress, and stopping. Bounded exact tests enumerate small instances and compare with optimum to find ratio counterexamples. Metamorphic tests permute input order under deterministic canonical ties, duplicate dominated candidates, add irrelevant elements, and scale positive costs where the theorem predicts invariance.

Property tests should seek the worst observed ratio, not merely average cost. Generate skew, nested sets, identical gains, zero gain, rare residual elements, complements, overflow-sized costs, and infeasible universes. Preserve any failing instance as a regression case.

The proof still carries the universal guarantee; enumeration validates implementation consistency only over its finite domain. Conversely, a sound proof of pseudocode does not show that stale caches, overflow, timeouts, or distributed arbitration implement it.

### Publish guarantees with execution evidence

Return solution, objective, feasibility result, algorithm/version, local rule, tie policy, premise checks, parameters, trace or certificate, factor, and completion status. Recompute objective independently. For set cover, a trace records residual size, selected set, new elements, and density at each step.

If a time budget stops greedy before feasibility, there is no cover result. If it stops after a feasible prefix but before an optional improvement stage, the original greedy factor may remain if the factor-bearing construction completed. Approximate candidate search preserves the theorem only when it provably returns a sufficiently good marginal; otherwise label the result heuristic or weaken the factor by a derived amount.

Monitor gain-evaluation count, stale-key refreshes, selected count, certificate bound, realized bound ratio, time, memory, infeasibility, overflow rejection, and fallback rate. Avoid logging sensitive element membership without policy.

## Definitions and Notation

Let ground set be $V$, partial solution $S_i$, candidate $x$, residual demand $R_i$, marginal $\Delta(x\mid S)=f(S\cup\{x\})-f(S)$, optimum solution $O$, and optimum value $OPT$. Let $H_n=\sum_{j=1}^n1/j$.

- **Maximal:** no single admissible object can be added; not necessarily maximum objective.
- **Density:** cost per unit of current progress, with progress measured under the proof.
- **Charging scheme:** an accounting map whose total equals or bounds algorithm cost.
- **Exchange property:** a structural rule permitting one feasible solution to trade elements with another.
- **Value oracle:** an interface returning $f(S)$; exactness and cost are assumptions.
- **Lazy key:** an upper bound on a current marginal, not automatically its present value.
- **Greedy trace:** replayable sequence of states, candidates, scores, ties, and commits.

## Mechanisms, Invariants, or Proof Structure

### Greedy proof template

1. Define state and strict progress.
2. Show every choice preserves feasibility or can be extended to feasibility.
3. Identify an optimum-relative averaging, exchange, charging, or residual lemma.
4. Apply the lemma at every state reachable by the algorithm.
5. Sum charges or solve the recurrence.
6. Handle empty, zero, tie, and infeasible cases.
7. prove polynomial runtime including score evaluation and representation costs.

### Set-cover charging invariant

When a chosen set covers $g$ new elements at cost one, give each charge $1/g$. Charges across all elements sum to the number of chosen sets. At the moment an element in optimum set $O_j$ is covered, greedy's gain is at least the number of uncovered elements of $O_j$ because $O_j$ was a candidate. Its charge is therefore at most the reciprocal of that count. Summing gives at most $H_{|O_j|}$ per optimum set.

### Submodular residual invariant

At state $S_i$, submodularity upper-bounds the benefit of adding all optimum elements by the sum of their individual marginals from $S_i$. Therefore at least one has marginal at least residual divided by $k$. Greedy's selected marginal meets that value, contracting residual. If cached or approximate gains break this inequality, the stated recurrence no longer follows.

### Implementation invariants

Every recorded gain equals progress from the pre-commit state; every selected item was feasible; every unselected candidate's comparison key was valid at selection; each commit advances; cumulative objective equals independent recomputation; and the reported guarantee names the exact completed path.

## Alternatives and Trade-Offs

| Greedy design | Advantage | Risk | Proof obligation |
|---|---|---|---|
| Maximum uncovered count | Simple unweighted cover | Ignores costs | Harmonic charging |
| Minimum cost/new gain | Weighted cover | Division, zero gain, changing density | Weighted charging |
| Maximum submodular marginal | Strong cardinality result | Oracle cost and overlap | Residual contraction |
| Heaviest feasible matroid element | Exact under matroid axioms | Fails for general systems | Exchange property |
| Least-loaded scheduling | Online simplicity | Weaker than reordered rules | Load and longest-job bounds |
| Lazy greedy | Fewer oracle calls | Stale-key misuse | Upper-bound refresh correctness |
| Batched parallel choices | Throughput | Redundant stale gains | Parallel-specific factor |
| Empirical learned score | Workload adaptation | No inherited theorem | New proof or heuristic label |

## Failure Modes and Misconceptions

- **“Greedy is always within a constant.”** Set cover's standard guarantee grows harmonically.
- **“Largest set is weighted greedy.”** The correct local ratio depends on cost per new coverage.
- **“Submodular means additive.”** It permits interactions, specifically diminishing returns.
- **“Monotone submodular proof covers negative gains.”** Nonmonotone objectives need different methods.
- **“Maximal means maximum.”** A maximal matching can be much smaller than a maximum matching.
- **“Any tie is harmless.”** The factor may survive while reproducibility and realized quality differ.
- **“A heap makes greedy faster without change.”** Only validated upper-bound laziness preserves selection.
- **“Parallel top gains equal sequential gains.”** Their covered value can overlap.
- **“Exact small tests prove the theorem.”** They test a bounded implementation domain.
- **“The theorem proves the code.”** Overflow, stale state, and fallback paths can violate premises.
- **“Better observed ratio strengthens the worst case.”** It characterizes only observed instances.
- **“Feasible prefix keeps the factor.”** The factor applies only at the proof's completion point.

## Worked Examples

### Example 1

**Situation.** Universe has six elements and sets $A=\{1,2,3,4\}$, $B=\{1,2,5\}$, $C=\{3,4,6\}$.

Greedy selects $A$ with gain four. Both remaining sets gain one, so deterministic name order selects $B$, then $C$: three sets. $B\cup C=U$, so optimum is two. Realized ratio is $3/2$.

**Conclusion.** Greedy can be nonoptimal even on a small unweighted cover.

### Example 2

**Situation.** With four uncovered elements, candidate X covers three at cost 12 and Y covers two at cost 3.

Raw gain chooses X. Density is $12/3=4$ for X and $3/2=1.5$ for Y, so weighted greedy chooses Y. Previously covered members must be excluded from each denominator.

**Conclusion.** Weighted cover ranks current cost-effectiveness, not set size.

### Example 3

**Situation.** A chosen unweighted set covers four new elements.

Charge each $1/4$. The charges total one, exactly the cost of selecting the set. If an optimum set had four of its elements still uncovered, greedy gain was at least four, so none of those elements receives more than $1/4$ at that moment.

**Conclusion.** Local charges convert selected-set count into an optimum-relative harmonic sum.

### Example 4

**Situation.** A coverage function counts distinct users reached. Current campaigns reach $\{a,b\}$. Candidate X reaches $\{b,c,d\}$.

Marginal gain is two, not three, because `b` is already reached. From a larger current set containing `c`, X's gain drops to one, demonstrating diminishing returns. Summing static campaign sizes would double-count.

**Conclusion.** Marginals are state-dependent and submodular coverage penalizes overlap.

### Example 5

**Situation.** For cardinality $k=4$, current value is 40 and $OPT=100$.

The residual is 60. The submodular averaging lemma guarantees some optimum element has marginal at least $60/4=15$, so exact greedy gains at least 15 and reaches at least 55. Residual contracts to at most 45.

**Conclusion.** One-step residual contraction is the engine of the $1-1/e$ bound.

### Example 6

**Situation.** Lazy heap keys are X:10 and Y:9. Refreshing X gives current gain 6.

X cannot be selected yet because Y's unrefreshed key remains a valid upper bound of 9. Reinsert X with 6 and refresh Y. If Y evaluates to 7, select Y; taking X at its stale 10 would not implement maximum-marginal greedy.

**Conclusion.** Lazy evaluation saves oracle calls only while preserving the comparison invariant.

### Example 7

**Situation.** Ratios are $c_X/g_X=(2^{62}+1)/3$ and $c_Y/g_Y=2^{62}/3$ in signed 64-bit arithmetic.

Floating conversion may erase the difference. Cross multiplication also overflows 64 bits. Use arbitrary-precision integers, checked 128-bit arithmetic if proven sufficient, or exact rationals; Y is cheaper because its numerator is smaller with equal denominator.

**Conclusion.** Numerical comparison is part of the greedy selection proof.

### Example 8

**Situation.** Four equal-gain candidates are stored in a hash table whose iteration order varies.

The approximation factor may hold for every tie, yet output, trace, cache key, and downstream load can change. Canonically compare `(negative gain, stable ID)`, or record random seed and prove the randomized policy.

**Conclusion.** Tie policy supports reproducibility even when quality theory is tie-robust.

### Example 9

**Situation.** Two workers simultaneously choose sets with gains 100 and 95 from the same residual, but 90 newly covered elements overlap.

Their joint gain is only 105, not 195. Sequential greedy would recompute the second marginal as at most five and might choose another set. A batch based on stale gains is a different algorithm needing its own bound.

**Conclusion.** Parallel selection cannot sum stale marginal values under overlap.

### Example 10

**Situation.** A service has selected sets covering 99% of required elements when its deadline expires.

Set cover requires all elements, so the prefix is infeasible and has no set-cover approximation ratio. Return timeout with residual demands. If the product instead permits partial cover, define a budgeted maximum-coverage problem and analyze that distinct objective.

**Conclusion.** A near-complete greedy prefix does not inherit a guarantee for a different feasible set.

## Cross-Program Connections

- **Algorithms:** [ALGE-061](./061-approximation-ratios-and-guarantees.md) supplies factor semantics; ALGE-063 through ALGE-068 provide alternative proof and search paradigms.
- **Data Structures:** owns indexed residual sets, exact ratio keys, heaps, lazy versions, and deterministic iteration.
- **Software Testing:** owns exhaustive small-instance oracles, metamorphic checks, trace replay, and adversarial regression corpora.
- **Concurrent Programming:** owns synchronization and deterministic reduction when gains are evaluated or committed in parallel.
- **Data Engineering:** owns representative instance distributions and stable cost/value lineage.
- **Platform Engineering:** owns resource budgets, timeout semantics, telemetry, replay, and safe fallback routing.

## References

1. David P. Williamson and David B. Shmoys, [“Greedy Algorithms and Local Search”](https://www.cambridge.org/core/books/abs/design-of-approximation-algorithms/greedy-algorithms-and-local-search/5CB0128EBCA19A51353C64A425B57FFE), in *The Design of Approximation Algorithms*, Cambridge University Press, 2011, doi:10.1017/CBO9780511921735.003. Graduate treatment; publisher record checked 2026-09-05.
2. Vijay V. Vazirani, [*Approximation Algorithms*](https://link.springer.com/book/10.1007/978-3-662-04565-7), Springer, 2001/2003, doi:10.1007/978-3-662-04565-7. Set cover and combinatorial approximation reference; publisher record checked 2026-09-05.
3. Václav Chvátal, “A Greedy Heuristic for the Set-Covering Problem,” *Mathematics of Operations Research* 4(3), 233–235, 1979, [doi:10.1287/moor.4.3.233](https://doi.org/10.1287/moor.4.3.233). Primary weighted set-cover analysis; publisher record checked 2026-09-05.
4. David S. Johnson, “Approximation Algorithms for Combinatorial Problems,” *Journal of Computer and System Sciences* 9(3), 256–278, 1974, [doi:10.1016/S0022-0000(74)80044-9](https://doi.org/10.1016/S0022-0000(74)80044-9). Primary early greedy worst-case analysis.
5. George L. Nemhauser, Laurence A. Wolsey, and Marshall L. Fisher, “An Analysis of Approximations for Maximizing Submodular Set Functions—I,” *Mathematical Programming* 14, 265–294, 1978, [doi:10.1007/BF01588971](https://doi.org/10.1007/BF01588971). Primary submodular-greedy analysis; bibliographic record checked 2026-09-05.
6. Ronald L. Graham, “Bounds for Certain Multiprocessing Anomalies,” *Bell System Technical Journal* 45(9), 1563–1581, 1966, [doi:10.1002/j.1538-7305.1966.tb01709.x](https://doi.org/10.1002/j.1538-7305.1966.tb01709.x). Primary list-scheduling bounds; publisher record checked 2026-09-05.
7. Bernhard Korte and Jens Vygen, *Combinatorial Optimization: Theory and Algorithms*, 6th ed., Springer, 2018, [doi:10.1007/978-3-662-56039-6](https://doi.org/10.1007/978-3-662-56039-6). Greedy, matroid, and approximation foundations.

## Exercises

### Exercise 1

Specify the state, candidates, score, tie rule, progress measure, and stop condition for deterministic unweighted greedy set cover. Explain what happens when the universe is empty or not coverable.

### Exercise 2

Universe is $\{1,2,3,4,5\}$. Sets are $A=\{1,2,3\}$, $B=\{2,4\}$, $C=\{3,4,5\}$, and $D=\{1,5\}$. Trace maximum-new-coverage greedy with alphabetical ties, assign charges, and compare with an optimum.

### Exercise 3

A lazy submodular implementation pops the largest cached gain and commits it without recomputation; ties depend on thread completion; gain counters use signed 32-bit integers. Diagnose each proof-to-code gap and give a correction.

### Exercise 4

Compare greedy weighted set cover and cardinality-constrained monotone submodular maximization. Identify the local rule, direction, bound form, proof technique, and assumptions that cannot be transferred between them.

### Exercise 5

A recommendation service selects a batch of ten items in parallel using predicted marginal engagement. Engagement has complements, predictions have bounded absolute error $\eta$, and policy requires category quotas. Design an honest algorithm/evidence contract; state why the standard $1-1/e$ theorem does or does not apply.

## Answers to the Exercises

### Answer 1

State is selected sets plus uncovered universe $R$. Candidates are unselected sets with positive $|S\cap R|$; score is that gain, ties break by stable set ID, and update removes newly covered elements. Progress is $|R|$, which strictly decreases; stop successfully when $R=\varnothing$. Empty universe returns the empty cover with cost zero. If $R$ remains but every candidate has zero gain, return infeasible with residual elements. The deterministic trace records pre-state, gains, winner, newly covered elements, and post-state.

### Answer 2

Initially A and C each gain three, so choose A. Charge elements 1,2,3 each $1/3$. Residual is $\{4,5\}$; C gains two, so choose C and charge 4,5 each $1/2$. Result is `(A,C)` of size two and covers all elements. No single set covers all five, so optimum is at least two; A and C witness two, hence greedy is optimal here. Total charges are $3(1/3)+2(1/2)=2$, equal to selected count.

### Answer 3

Cached submodular gains are only upper bounds after state grows; recompute the leader and select only when refreshed gain dominates every remaining valid bound. Thread-completion ties make the trace nondeterministic; compare exact refreshed gains then stable IDs, or define recorded randomness with an applicable proof. A 32-bit counter can overflow and invert ranking; prove a safe wider bound, use checked arithmetic, or arbitrary precision. Also version heap entries by state, verify selected feasibility and marginal against the pre-commit snapshot, and reject numerical failure rather than continuing under the factor.

### Answer 4

Weighted set cover minimizes total positive cost and chooses minimum cost divided by current uncovered gain; charging yields a harmonic multiplicative upper bound under full-cover feasibility. Monotone submodular cardinality maximization chooses maximum marginal value and uses residual contraction to guarantee at least $1-1/e$ of optimum under normalization, monotonicity, submodularity, exact oracle values, and at most $k$ items. Cover density, harmonic charges, and full-demand stopping do not prove the submodular result; diminishing returns and cardinality residual reasoning do not establish weighted-cover feasibility or its factor.

### Answer 5

The standard theorem does not apply directly: complements violate submodularity, parallel stale batches need not match sequential maximum marginal, prediction error alters comparisons, and category quotas are not a pure cardinality constraint. Define exact policy feasibility first, a measured or conservatively bounded value oracle, batch conflict handling, deterministic ties, and timeout status. Either choose a formulation and algorithm with a proof for complementary value plus quota constraints, or label selection heuristic and evaluate against exact/strong-bound small instances and an offline policy-compliant baseline. Report feasibility, prediction calibration, realized value, worst sampled gaps, batch overlap, latency, and drift. If a restricted submodular quota model is defensible, cite and implement its specific constrained-submodular algorithm rather than borrowing $1-1/e$.
