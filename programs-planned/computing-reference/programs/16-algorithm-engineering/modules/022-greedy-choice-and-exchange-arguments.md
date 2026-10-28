---
module_id: ALGE-022
program: Algorithm Engineering
level: 1
module_number: 22
title: Greedy Choice and Exchange Arguments
status: complete
last_verified: 2026-09-04
---

# Greedy Choice and Exchange Arguments

## One-Page Review

### Governing question

When does a locally preferred feasible choice belong to some globally optimal solution, and how can an exchange, stays-ahead, cut, or structural theorem prove that irrevocable choice safe?

### Essential definitions

- A **greedy algorithm** repeatedly makes a locally ranked feasible choice without revisiting earlier choices.
- A **feasible prefix** is a partial solution that can still satisfy the problem constraints.
- The **greedy-choice property** says some optimum is compatible with the next greedy choice.
- **Optimal substructure** says the remainder of an optimum solves the residual problem optimally.
- An **exchange argument** transforms an optimum to agree with a greedy choice without worsening its objective.
- A **stays-ahead proof** shows every greedy prefix is at least as favorable as the corresponding prefix of an optimum under a useful measure.
- A **safe edge or element** can be added to a partial solution while preserving compatibility with an optimum.
- An **independence system** is a hereditary family of feasible subsets.
- A **matroid** is an independence system satisfying augmentation; descending-weight feasible greedy is exact on matroids.
- An **approximation ratio** bounds a feasible greedy result relative to optimum even when exactness is impossible or unproved.

### Central model, mechanism, or theorem

Let $G$ be a feasible prefix and $g$ its next greedy choice. A canonical exchange proof establishes:

1. an optimal completion $O$ of the current instance exists;
2. if $g\notin O$, a named element or structure $o$ can be replaced;
3. $O'=(O-\{o\})\cup\{g\}$ remains feasible;
4. $O'$ is no worse than $O$;
5. the residual instance after fixing $g$ has the same proven structure.

For a matroid $(E,\mathcal I)$ with nonnegative weights, scan $E$ by nonincreasing weight and add $e$ exactly when $G\cup\{e\}\in\mathcal I$. Heredity and augmentation support exchanges that transform an optimum to contain each greedy prefix, so the final independent set has maximum weight.

Greedy is not synonymous with exact. For positive-cost set cover, choosing minimum cost per newly covered element yields

$$
cost(G)\le H_d\,cost(OPT),
\qquad
H_d=\sum_{i=1}^{d}\frac1i\le1+\ln d,
$$

where $d$ is the maximum input-set cardinality. That is an approximation theorem under its premises, not an optimality claim.

### Critical invariants

- The state explicitly represents a feasible partial solution and the exact residual instance.
- The ranking key is derived from the objective and proof, not intuition alone.
- Each accepted choice preserves feasibility and makes irreversible progress.
- The exchange identifies what is removed, proves feasibility, and proves objective non-worsening.
- Residual optimal substructure is proved after, not assumed before, the greedy choice.
- Ties have deterministic semantics and do not invalidate the proof.
- Ratios use exact comparison or safe cross-products rather than uncontrolled floating error.
- Priority-queue entries are validated against current marginal values when priorities can become stale.
- Exact, approximation, and heuristic claims remain visibly distinct.
- Small-instance differential tests use an independent optimizer, not the same greedy ordering.

### Common failures

Common failures include choosing the largest immediate reward; proving only feasibility; saying “take an arbitrary optimum” without exchanging it; replacing an element that makes later choices infeasible; assuming optimal substructure implies a greedy choice; reversing an exchange inequality; treating one counterexample-free benchmark as proof; applying fractional-knapsack density to indivisible items; assuming familiar coin denominations generalize; using Dijkstra with negative edges; treating interval scheduling as a matroid; comparing ratios with rounded floats; allowing stale marginal gains to choose the wrong item; changing ties across distributed workers; and calling an unbounded heuristic an approximation algorithm.

### Compact example

For half-open activities, sort by finish time and repeatedly select the next activity whose start is at least the last selected finish. If $g$ has the earliest finish and an optimum begins with $o$, then

$$
finish(g)\le finish(o).
$$

Replacing $o$ by $g$ preserves every later activity because each later start is at least $finish(o)$ and therefore at least $finish(g)$. The optimum loses no activity. Induction on the residual suffix proves maximum cardinality. On the executable instance, the deterministic result is $(B,E,H,K)$ of size four.

### Connections

[ALGE-004](./004-inductive-correctness-proofs.md) supplies induction, [ALGE-003](./003-loop-invariants-for-algorithm-correctness.md) supplies feasible-prefix invariants, [ALGE-021](./021-divide-and-conquer.md) contrasts recursive decomposition, [ALGE-023](../ROADMAP.md) contrasts dynamic-programming state design, and later graph modules apply cut and settled-prefix arguments.

## Governing Question

What theorem makes the next apparently best feasible choice irreversible, and what guarantee remains when no such theorem establishes exact optimality?

A greedy implementation is usually short. Its proof is the algorithm. The ranking must correspond to a structural property of the feasible family or objective. Earliest finish works for unweighted interval scheduling because one chosen activity consumes no more future time than the first activity it replaces. Highest value density works for fractional knapsack because divisible mass can be exchanged continuously. Neither argument transfers automatically to another constraint.

Good greedy engineering therefore starts with the proof obligation, not a priority queue. Define partial feasibility, residual state, tie order, and objective. Attempt an exchange or stays-ahead theorem. If exactness fails, search for a quantified approximation or label the method honestly as a heuristic.

## Why This Matters

Greedy methods can be fast, incremental, memory-efficient, and easy to operate. They power interval selection, minimum spanning trees, shortest paths with nonnegative weights, optimal prefix codes, scheduling orders, matroid optimization, and approximation algorithms for covering problems.

Their simplicity is also dangerous. Many plausible rules fail on tiny instances. “Best now” may consume a resource needed by two slightly smaller choices. A ratio may be valid only when items are divisible. A settled shortest path may be invalidated by a later negative edge. A local marginal gain may change after every selection.

The right response is not to distrust greedy design. It is to demand evidence at the right level: a complete exchange for exactness, a charging or potential argument for approximation, exhaustive counterexample search for development, and production checks for the data structures and numeric comparisons that implement the proven rule.

## Prerequisites and Retrieval

Retrieve:

- sets, sequences, relations, total orders, induction, contradiction, and inequalities;
- optimization specifications, feasible regions, residual problems, and tie-breaking;
- arrays, sorting, heaps, disjoint sets, graphs, trees, cuts, paths, and prefix codes;
- fractions, cross multiplication, integer overflow, floating-point comparison, and rational arithmetic;
- exact exponential search or dynamic programming for small-instance oracles;
- property testing, adversarial generation, approximation ratios, and reproducible benchmarking.

You should be able to state what makes a partial solution feasible, compare two objective values, and distinguish an optimal solution from a maximal one.

## Learning Objectives

After completing this module, you should be able to:

1. formulate a greedy state, ranking rule, feasibility predicate, and residual problem;
2. prove termination and feasible-prefix invariants;
3. construct complete exchange and stays-ahead arguments;
4. use cut and cycle properties to justify safe graph choices;
5. explain the matroid greedy theorem and its limits;
6. prove earliest-finish interval scheduling and classic scheduling orders;
7. distinguish fractional from indivisible choices and exact from approximate greedy;
8. derive a harmonic set-cover guarantee by charging;
9. implement deterministic, overflow-safe priorities and lazy updates;
10. validate greedy claims with independent exact oracles, counterexamples, and operational evidence.

## Core Exposition

### Specify the optimization problem before the rule

Define:

- ground elements or actions $E$;
- feasible complete solutions $\mathcal F\subseteq2^E$ or feasible sequences;
- an objective $w(F)$ to maximize or minimize;
- accepted inputs and infeasibility behavior;
- whether identities, order, or only membership matter;
- deterministic tie-breaking;
- numeric and exceptional-value policy.

A partial solution $G$ needs its own invariant. “Feasible so far” may mean independent, nonoverlapping, acyclic, within capacity, connected to a settled region, or capable of completing a prefix code. State whether every feasible prefix extends to a complete solution; maximality alone does not imply optimality.

Then write the greedy rule as

$$
g=\operatorname*{arg\,best}_{e\in A(G)}priority(e,G),
$$

where $A(G)$ is the currently admissible set. If priority depends on $G$, it must be recomputed or safely maintained after state changes.

### Separate feasibility, progress, and optimality

Three proofs are required:

1. **feasibility:** adding the chosen element preserves the partial invariant;
2. **progress and termination:** a finite measure decreases or the chosen set strictly grows within finite $E$;
3. **quality:** the completed solution is exact or satisfies a declared bound.

Feasibility plus termination usually proves only that the output is maximal: no further element can be added. A maximal matching, independent set, or packing can be far from maximum. Never substitute one word for the other.

For exact greedy, prove both the greedy-choice property and optimal substructure of the residual instance. Optimal substructure alone also appears in dynamic programming and does not justify discarding alternatives.

### Build a complete exchange argument

At a state with greedy prefix $G$, choose an optimum $O$ compatible with as much of $G$ as the induction requires. If the next greedy choice $g$ is already in $O$, advance. Otherwise identify an exchange target $o$ and form

$$
O'=(O-\{o\})\cup\{g\}.
$$

Prove separately:

- $O'$ has the required size or completion shape;
- $O'$ is feasible;
- $w(O')$ is no worse than $w(O)$;
- $O'$ agrees with one more greedy decision;
- the operation does not disturb earlier aligned choices.

The existence of some exchange target is often the deepest step. For matroids it comes from augmentation or a basis-exchange consequence. For interval scheduling it comes from ordering by finish. For spanning trees it comes from the unique cycle created by adding a safe edge.

Avoid circular language such as “replace with the better choice, so it stays optimal.” The proof must connect the ranking inequality to feasibility and the complete objective.

### Use stays-ahead when prefixes have a useful order

Let greedy choices be $g_1,g_2,\ldots$ and an optimal sequence be $o_1,o_2,\ldots$. A stays-ahead proof establishes an invariant such as

$$
measure(g_1,\ldots,g_j)
\le
measure(o_1,\ldots,o_j)
$$

for every prefix $j$. If the measure determines how much opportunity remains, the greedy solution cannot finish with fewer or worse choices.

For interval scheduling, the finish time of greedy's $j$th chosen activity is no later than the finish time of the $j$th activity in any compatible schedule. Inductively, the optimal schedule's next activity is also available after the earlier-finishing greedy prefix. Thus any schedule with $k$ activities implies greedy selects at least $k$.

Stays-ahead is not merely comparing immediate rewards. Choose a prefix measure that controls future feasibility or the final objective.

### Prove earliest-finish interval scheduling

Each activity $a$ has half-open interval $[s_a,f_a)$ with $s_a<f_a$. Two activities are compatible when their intervals do not overlap. Sort by

$$
(f_a,s_a,id_a)
$$

for deterministic ties. Select the first activity, then every activity with $s_a\ge f_{last}$.

Let $g$ be the earliest-finishing activity and let an optimal nonempty schedule begin with $o$. Since $f_g\le f_o$, replacing $o$ by $g$ preserves compatibility with all later optimal activities. The replacement keeps cardinality. The remaining problem contains exactly activities beginning at or after $f_g$, so induction proves optimal cardinality.

The proof is specific to unweighted cardinality. Earliest finish need not maximize total activity value. Weighted interval scheduling generally requires dynamic programming because accepting one interval changes which weighted combinations remain.

### Preserve executable exchange evidence

The following implementation applies the proven earliest-finish rule and compares its cardinality with an independent exhaustive oracle. Intervals are half-open and identities break exact key ties.

<!-- bijux-verify: {"id":"earliest-finish-interval-scheduling","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"ordered_by_finish=('B', 'C', 'A', 'E', 'D', 'F', 'G', 'H', 'I', 'J', 'K')\nselected=('B', 'E', 'H', 'K')\noptimal_size=4 checked_subsets=2048\ncompatible=True maximum=True\n","stderr":""}} -->
~~~python
def compatible(activities):
    ordered = sorted(activities, key=lambda item: (item[1], item[2], item[0]))
    return all(
        ordered[index - 1][2] <= ordered[index][1]
        for index in range(1, len(ordered))
    )


def earliest_finish(activities):
    ordered = sorted(activities, key=lambda item: (item[2], item[1], item[0]))
    selected = []
    last_finish = None
    for activity in ordered:
        if last_finish is None or activity[1] >= last_finish:
            selected.append(activity)
            last_finish = activity[2]
    return tuple(ordered), tuple(selected)


def maximum_size(activities):
    best = 0
    checked = 0
    for mask in range(1 << len(activities)):
        candidate = tuple(
            activity
            for index, activity in enumerate(activities)
            if mask & (1 << index)
        )
        checked += 1
        if compatible(candidate):
            best = max(best, len(candidate))
    return best, checked


activities = (
    ("A", 0, 6),
    ("B", 1, 4),
    ("C", 3, 5),
    ("D", 3, 8),
    ("E", 5, 7),
    ("F", 5, 9),
    ("G", 6, 10),
    ("H", 8, 11),
    ("I", 8, 12),
    ("J", 2, 13),
    ("K", 12, 14),
)

ordered, selected = earliest_finish(activities)
optimum, checked = maximum_size(activities)
print(f"ordered_by_finish={tuple(activity[0] for activity in ordered)}")
print(f"selected={tuple(activity[0] for activity in selected)}")
print(f"optimal_size={optimum} checked_subsets={checked}")
print(f"compatible={compatible(selected)} maximum={len(selected) == optimum}")
~~~

This finite execution checks one activity set. It does not prove the exchange theorem, weighted scheduling, invalid-interval handling, fixed-width time arithmetic, or production scale.

### Derive scheduling orders by adjacent interchange

For jobs with processing times $p_i>0$ and due dates $d_i$, maximum lateness is

$$
L_{max}=\max_i(C_i-d_i),
$$

where $C_i$ is completion time. Earliest-due-date order minimizes $L_{max}$ on one nonpreemptive machine when all jobs are available initially.

Take adjacent jobs $i,j$ beginning at time $t$ with $d_i>d_j$. Before swapping, their completion times are $t+p_i$ and $t+p_i+p_j$. After placing $j$ first, $j$ completes earlier, while $i$ completes at the old completion time of $j$ and has the later due date. The maximum lateness of the pair does not increase. Repeatedly removing due-date inversions transforms an optimum into earliest-due-date order.

For minimizing unweighted sum of completion times, adjacent interchange instead yields shortest-processing-time order. For positive weights and objective $\sum_i w_iC_i$, compare adjacent orders:

$$
cost(i,j)-cost(j,i)=w_jp_i-w_ip_j.
$$

Thus put $i$ before $j$ when

$$
\frac{p_i}{w_i}\le\frac{p_j}{w_j},
$$

known as Smith's ratio rule. In code compare $p_iw_j$ with $p_jw_i$ using a numeric type that cannot overflow; avoid rounded floating ratios.

Release times, precedence, parallel machines, preemption, and other objectives change the theorem. Do not carry the ordering rule across models without a new proof.

### Understand fractional exchange and indivisible failure

In fractional knapsack, item $i$ has value $v_i\ge0$, weight $w_i>0$, and any fraction in $[0,1]$ may be taken. Sort by density $v_i/w_i$. If a solution takes positive mass of lower-density $j$ while leaving higher-density $i$ unused, exchange equal weight from $j$ to $i$. Feasibility remains, and value does not decrease. Repetition yields density order with at most one partial item.

In 0/1 knapsack, an item cannot be partially exchanged. With capacity 50 and $(value,weight)$ items

$$
(60,10),\quad(100,20),\quad(120,30),
$$

density greedy takes the first two for value 160, while the last two give 220. The fractional proof fails exactly where it needs to split an indivisible item.

This diagnostic is reusable: identify the exchange granularity. If the proof replaces fractions but the implementation chooses atoms, it proves a different problem.

### Treat coin systems as part of the theorem

For denominations $(1,3,4)$ and amount 6, largest-coin-first chooses

$$
4+1+1
$$

using three coins, while

$$
3+3
$$

uses two. A greedy coin rule may be exact for a particular canonical denomination system, but positivity and sorted order alone do not establish it.

Validate a fixed system with a proof specific to its denominations or a bounded theorem that reduces the amounts requiring checks. For configurable denominations, use an exact dynamic program, explicitly accept heuristic output, or verify the greedy result against an exact method within a declared range.

### Use matroids to expose the general exchange structure

An independence system $(E,\mathcal I)$ satisfies:

1. $\varnothing\in\mathcal I$;
2. if $B\in\mathcal I$ and $A\subseteq B$, then $A\in\mathcal I$.

It is a matroid when augmentation also holds:

$$
A,B\in\mathcal I
\land |A|<|B|
\Longrightarrow
\exists e\in B\setminus A:
A\cup\{e\}\in\mathcal I.
$$

For nonnegative element weights, scan in nonincreasing weight and accept an element exactly when independence remains. Augmentation supplies an exchange that aligns an optimal basis with each greedy prefix without reducing weight. Heredity and nonnegative weights let a maximum-weight independent set be extended to a basis without loss.

Forests of an undirected graph form the graphic matroid: adding an edge is allowed exactly when it creates no cycle. Kruskal's descending-benefit or ascending-cost reasoning is a matroid/cut exchange in the appropriate formulation.

Not every successful greedy problem is a matroid. Compatible activity sets are hereditary, but augmentation fails: $\{[0,4)\}$ has size one, $\{[0,2),[2,4)\}$ has size two, and neither short interval can augment the long-interval set. Earliest finish succeeds by a problem-specific ordered exchange.

### Apply cut and cycle exchange in graphs

For a connected weighted undirected graph, consider a cut $(S,V\setminus S)$ that respects a partial minimum-spanning forest: no chosen tree edge crosses it. A minimum-weight crossing edge is safe. If an optimum tree omits it, adding the edge creates a cycle. That cycle contains another crossing edge; remove one whose weight is no smaller. Connectivity and acyclicity return, and total weight does not increase.

This exchange supports Kruskal and Prim under their respective invariants. Equal weights require deterministic tie rules for reproducible identity output, though every resulting tree can still have minimum total weight.

Dijkstra's settled-prefix argument has a different premise: edge weights are nonnegative. When the minimum tentative vertex $u$ is settled, any alternative path through an unsettled vertex cannot become shorter by adding nonnegative edges. A reachable negative edge destroys that inequality; a priority queue does not repair the proof.

### Prove Huffman coding by a sibling exchange

For positive symbol frequencies $f_i$, a binary prefix-code tree has weighted path length

$$
L=\sum_i f_i d_i,
$$

where $d_i$ is leaf depth. In some optimal full tree, the two least frequent symbols can be placed as deepest siblings: exchange lower frequencies downward without increasing $L$.

Merge those two symbols into a pseudo-symbol of frequency $f_x+f_y$. Any code for the reduced alphabet expands that leaf into two children, increasing cost by exactly $f_x+f_y$. Induction proves repeatedly merging the two minimum frequencies optimal.

A heap implements the choices in $O(k\log k)$ time for $k$ symbols. Tie order changes code identities but not optimal weighted length when frequencies tie. Define zero-frequency handling, code serialization, maximum depth, integer overflow, and canonicalization separately.

### Separate exact greedy, approximation, and heuristic use

Three labels carry different obligations:

- **exact greedy:** proof that output equals the optimum under all admitted inputs;
- **approximation algorithm:** proof that output is feasible and within a stated ratio or additive bound;
- **heuristic:** no universal quality bound is claimed, though empirical quality may be measured.

For positive-cost set cover, maintain uncovered universe $U'$ and choose set $S$ minimizing

$$
\frac{c(S)}{|S\cap U'|}.
$$

Charge every newly covered element that ratio. Consider an optimum set containing $r$ elements still uncovered at some step. Greedy's ratio is no greater than that optimum set's cost divided by $r$. Ordering the moments its elements become covered bounds their total charges by

$$
c(S)\left(1+\frac12+\cdots+\frac1{|S|}\right).
$$

Summing over an optimal cover gives the $H_d$ guarantee, where $d=\max_S|S|$. The algorithm need not return an optimum. A modified priority or stopping rule needs a new bound.

### Engineer mutable priorities carefully

Some greedy priorities are static: activity finish times and Huffman frequencies of current nodes fit ordinary sorting or heaps. Others are marginal and change after every selection, as in set cover.

Safe implementations can:

- recompute every candidate exactly each round;
- update only candidates affected through an inverted index;
- use lazy heap entries tagged with state versions, recomputing the top until current;
- maintain certified upper bounds that cannot skip a better current candidate.

Never pop a stale key and treat it as the proven argmin/argmax. Record deterministic tie fields after the mathematical priority. For ratios $a/b$ and $c/d$ with positive denominators, compare $ad$ and $cb$ using checked widened arithmetic or exact rationals.

Mutable input can invalidate feasibility or priority between selection and commit. Snapshot it, hold an appropriate lock, or define optimistic validation and retry with a bound.

### Validate the theorem-to-code correspondence

For small instances, enumerate every feasible solution and compare objectives. Preserve an independent oracle: do not sort candidates with the same comparator and call that verification.

Test:

- empty, singleton, infeasible, all-tied, duplicate, and extreme numeric inputs;
- the exact exchange inequality at equality boundaries;
- deterministic output under input permutations;
- feasibility after every prefix, not only at completion;
- residual-state correctness after accept and reject;
- ratio comparison near overflow or floating-rounding boundaries;
- stale heap entries and state-version races;
- known counterexamples for nearby wrong rules;
- exact claims against exhaustive or integer-programming oracles;
- approximation ratios against optimum on bounded cases;
- time, memory, heap operations, and oracle-free production scale.

Instrumentation should count considered, accepted, rejected, recomputed, and stale candidates; feasibility checks; heap pushes/pops; numeric fallbacks; objective; bound certificate where available; and runtime/resource distributions. Finite differential tests find defects but do not replace the exchange or approximation proof.

## Definitions and Notation

- $E$: finite ground set of elements or actions.
- $\mathcal F$: family of complete feasible solutions.
- $\mathcal I$: hereditary family of independent subsets.
- $G$: current greedy prefix or selected set.
- $A(G)$: elements admissible after prefix $G$.
- $g$: next greedy choice.
- $O$ or $OPT$: an optimal solution or its objective value, as context declares.
- $O'$: an exchanged optimum aligned with an additional greedy choice.
- $w(e)$: element benefit, weight, or cost with direction stated.
- $p_i$: processing time of job $i$.
- $d_i$: due date of job $i$.
- $C_i$: completion time of job $i$.
- $L_i=C_i-d_i$: lateness; $L_{max}=\max_iL_i$.
- $s_a,f_a$: start and finish of half-open activity $a$.
- $f_i,d_i$: symbol frequency and code depth when coding context is explicit.
- $U'$: currently uncovered universe in set cover.
- $H_d=\sum_{i=1}^{d}1/i$: $d$th harmonic number.
- $\rho$: a proved approximation ratio, not an observed average.

A maximal feasible set admits no additional element. A maximum or optimal set has best objective among all feasible solutions. A safe choice preserves compatibility with at least one optimum. A deterministic tie rule selects an identity without necessarily changing objective quality.

## Mechanisms, Invariants, or Proof Structure

Use this greedy proof worksheet.

1. **Model.** State elements, complete and prefix feasibility, objective direction, ties, and numeric semantics.
2. **Rule.** Define admissible candidates and exact priority at each state.
3. **Prefix invariant.** Prove every accepted choice preserves feasibility and earlier commitments.
4. **Progress.** Prove finite termination and define infeasible-input behavior.
5. **Claim level.** Declare exact, approximation, or heuristic before presenting evidence.
6. **Comparator optimum.** Select an optimum aligned with the longest greedy prefix, or a prefix measure for stays-ahead.
7. **Exchange target.** Identify the specific element, edge, job pair, code leaves, or mass to replace.
8. **Exchange feasibility.** Prove constraints remain satisfied after replacement.
9. **Objective inequality.** Derive non-worsening from the greedy priority with the direction checked.
10. **Residual structure.** Prove the remaining instance retains the induction premises.
11. **Completion.** Show aligned optima or prefix dominance implies final quality.
12. **Approximation certificate.** If not exact, assign charges/potential and sum a stated bound.
13. **Implementation correspondence.** Check sorting/heap keys, equality, overflow, stale state, identities, and concurrency.
14. **Independent evidence.** Exhaust bounded instances, preserve counterexamples, measure structural counters, and benchmark scale.

For interval scheduling, the exchange target is the optimum's first activity and the inequality is finish time. For EDD and Smith scheduling, the target is an adjacent inverted pair. For MST, adding a safe edge identifies a removable cycle edge crossing the same cut. For Huffman, exchange places the least frequencies at deepest sibling leaves, then contraction supplies residual optimal substructure. For matroids, augmentation supplies a feasible element exchange. For set cover, no exact exchange is claimed; element charges sum the harmonic approximation.

## Alternatives and Trade-Offs

- **Greedy versus exhaustive search:** greedy can be near-linear after ordering; exhaustive search supplies a small-instance truth oracle but scales exponentially.
- **Greedy versus dynamic programming:** greedy discards alternatives using a theorem; dynamic programming retains distinct residual states when local choices cannot be exchanged safely.
- **Static sort versus priority queue:** sorting is simple for fixed priorities; heaps support newly created or changing candidates but require stale-key discipline.
- **Eager versus lazy marginal updates:** eager updates simplify argbest correctness; lazy updates reduce work but need versions and revalidation.
- **Exact rational versus floating priority:** exact comparisons preserve proof order; floating arithmetic may be faster but needs a defined error/tie policy.
- **One optimum versus deterministic identity output:** an objective may have many optima; reproducible systems need secondary keys without implying uniqueness.
- **Matroid theorem versus problem-specific exchange:** matroids give reusable weighted greedy structure; problems such as interval scheduling can be greedy without forming a matroid.
- **Exact versus approximation:** an approximation gives a universal bound where exact polynomial greedy is unavailable; it must not be marketed as optimal.
- **Approximation versus heuristic:** a heuristic can perform better empirically; without proof it lacks the approximation's worst-case certificate.
- **Online irrevocability versus offline ordering:** online arrival may prevent the exchanges available after seeing all inputs and requires competitive analysis.
- **Local recomputation versus snapshot:** live state reduces staleness windows; snapshotting supplies deterministic semantics and simpler proofs.

## Failure Modes and Misconceptions

1. **Best-now slogan:** no relationship between priority and global objective is proved.
2. **Feasible-equals-optimal:** a maximal output is mislabeled maximum.
3. **Optimal-substructure shortcut:** a property shared with dynamic programming is treated as the greedy-choice theorem.
4. **Nameless exchange:** no concrete removed element or transformed structure is identified.
5. **Broken replacement:** the exchanged solution violates capacity, compatibility, connectivity, or independence.
6. **Wrong inequality direction:** a minimization priority is justified with a maximization comparison.
7. **Disturbed prefix:** exchange removes an earlier aligned greedy choice.
8. **Residual mismatch:** the suffix problem does not retain original premises.
9. **Tie nondeterminism:** equally ranked identities vary by input, heap, hash, worker, or platform order.
10. **Fractional-to-atomic transfer:** divisible exchange is applied to 0/1 items.
11. **Coin folklore:** one familiar currency is generalized to arbitrary denominations.
12. **Weighted-interval transfer:** earliest finish is applied to value maximization.
13. **Matroid overreach:** every hereditary system is assumed to satisfy augmentation.
14. **Negative-edge settlement:** Dijkstra finalizes a distance that a later path can reduce.
15. **Huffman domain omission:** zero/negative frequencies, arity, depth limits, or serialization change the model.
16. **Approximation-as-exact:** a harmonic or constant bound is reported as optimality.
17. **Heuristic-as-approximation:** finite observed gaps are reported as a universal ratio.
18. **Rounded ratio:** floating division reverses nearly equal priorities.
19. **Cross-product overflow:** an exact-looking comparator wraps silently.
20. **Stale heap maximum:** outdated marginal gain wins a later round.
21. **Mutable feasibility:** external state changes after a choice is ranked.
22. **Oracle echo:** validation reuses the production greedy comparator.
23. **Random-only tests:** small structured counterexamples remain absent.
24. **Objective-only checking:** infeasible output happens to have an attractive score.
25. **Mean-only benchmarking:** worst priority updates, heap growth, and tail retries disappear.
26. **Unversioned rule:** production cannot identify which priority, tie, or proof assumptions produced a result.

## Worked Examples

### Example 1

**Question:** What schedule does earliest finish choose from the executable activities?

**Reasoning:** Finish ordering begins $B,C,A,E,\ldots$. Select $B=[1,4)$, reject activities starting before 4, select $E=[5,7)$, then $H=[8,11)$ and $K=[12,14)$.

**Conclusion:** The deterministic schedule is $(B,E,H,K)$ with cardinality four.

### Example 2

**Question:** Why can the first activity of an optimum be replaced by earliest-finishing $g$?

**Reasoning:** If optimum begins with $o$, then $f_g\le f_o$. Every later optimal activity starts at or after $f_o$, hence also at or after $f_g$. Replacement preserves all later activities and schedule size.

**Conclusion:** Some optimum begins with $g$, enabling induction on activities starting after $f_g$.

### Example 3

**Question:** Does largest-coin-first minimize coins for denominations $(1,3,4)$ and amount 6?

**Reasoning:** Greedy returns $4+1+1$, using three coins. The feasible representation $3+3$ uses two.

**Conclusion:** No; a tiny counterexample refutes exactness for that denomination system.

### Example 4

**Question:** Why does value density solve fractional but not 0/1 knapsack for items $(60,10),(100,20),(120,30)$ and capacity 50?

**Reasoning:** Fractionally, density order may exchange equal weight and reaches value 240 by taking the first two items plus $20/30$ of the third. In 0/1 form, density greedy gets 160, while the last two items fit exactly and yield 220.

**Conclusion:** The exchange granularity, not the priority slogan, determines whether the proof applies.

### Example 5

**Question:** What local transformation proves earliest-due-date order for maximum lateness?

**Reasoning:** Find adjacent jobs $i,j$ with $d_i>d_j$. Swap them. Job $j$ completes earlier; job $i$ takes the old later completion time but has the later due date. Neither pair lateness exceeds the prior pair maximum.

**Conclusion:** Repeated adjacent exchanges remove all due-date inversions without worsening $L_{max}$.

### Example 6

**Question:** Order jobs $(p,w)$ equal to $A=(3,5)$, $B=(2,2)$, and $C=(1,4)$ to minimize weighted completion sum.

**Reasoning:** Ratios $p/w$ are $0.6,1,0.25$, so Smith order is $C,A,B$. Completion times are $1,4,6$, giving

$$
4(1)+5(4)+2(6)=36.
$$

**Conclusion:** Compare products rather than rounded ratios in an implementation.

### Example 7

**Question:** What does the graphic-matroid exchange say when adding a chosen edge creates a cycle in an optimal spanning tree?

**Reasoning:** The cycle crosses the relevant cut at another edge. Remove a crossing edge no lighter than the chosen minimum crossing edge. The result is again a spanning tree and costs no more.

**Conclusion:** The chosen edge is safe for some minimum spanning tree.

### Example 8

**Question:** Why can Dijkstra fail with a negative edge?

**Reasoning:** Let edges be $s\to u$ of weight 2, $s\to v$ of weight 5, and $v\to u$ of weight $-10$. Settling $u$ at 2 is premature; path $s\to v\to u$ has cost $-5$.

**Conclusion:** Nonnegative edge weights are a proof premise, not an implementation detail.

### Example 9

**Question:** What weighted path length does Huffman merging produce for frequencies $(5,7,10,15,20,45)$?

**Reasoning:** Merge weights are $12,22,35,57,102$. The weighted external path length equals the sum of merge weights:

$$
12+22+35+57+102=228.
$$

**Conclusion:** Repeated minimum-frequency contraction produces an optimal prefix-code cost under the stated model.

### Example 10

**Question:** What bound does greedy set cover give when the largest set has eight elements?

**Reasoning:**

$$
H_8=1+\frac12+\cdots+\frac18\approx2.717857.
$$

The charging theorem gives $cost(G)\le H_8\,cost(OPT)$.

**Conclusion:** The bound is a worst-case approximation certificate, not a prediction that the observed gap equals 2.717857.

## Cross-Program Connections

- [Theory of Computation & Complexity](../../15-theory-of-computation-and-complexity/ROADMAP.md) owns optimization hardness, exactness, reductions, approximation and competitive guarantees, and proof quantifiers.
- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) owns heaps, disjoint sets, dynamic feasibility structures, lazy priorities, and deterministic ordered containers.
- [Statistics & Data Engineering](../../19-data-engineering/ROADMAP.md) owns production distributions, sketches, marginal updates, pipeline objectives, and evidence artifacts for large instances.
- [Programming Languages & Semantics](../../01-programming-languages-and-semantics/ROADMAP.md) owns comparator laws, numeric overflow, exact rationals, ownership, callbacks, exceptions, and reproducibility.
- [Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) owns exhaustive oracles, property/counterexample testing, benchmark design, and rollout validation.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) owns irrevocable decisions under partial information, stale state, coordination, deterministic ties, and retries.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) owns adversarial priorities, resource exhaustion, tenant-controlled numeric inputs, and quality claims exposed to attackers.

## References

1. Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein. [*Introduction to Algorithms*, fourth edition](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/), MIT Press, 2022. Greedy design, activity selection, Huffman coding, matroids, scheduling, graph algorithms, and approximation foundations.
2. Jack Edmonds. [“Matroids and the Greedy Algorithm”](https://doi.org/10.1007/BF01584082), *Mathematical Programming* 1, 1971, pp. 127–136. Primary structural treatment of matroids and greedy optimization.
3. David A. Huffman. [“A Method for the Construction of Minimum-Redundancy Codes”](https://doi.org/10.1109/JRPROC.1952.273898), *Proceedings of the IRE* 40(9), 1952, pp. 1098–1101. Primary optimal prefix-code construction.
4. Edsger W. Dijkstra. [“A Note on Two Problems in Connexion with Graphs”](https://doi.org/10.1007/BF01386390), *Numerische Mathematik* 1, 1959, pp. 269–271. Primary minimum-tree and nonnegative shortest-path greedy constructions.
5. Vašek Chvátal. [“A Greedy Heuristic for the Set-Covering Problem”](https://doi.org/10.1287/moor.4.3.233), *Mathematics of Operations Research* 4(3), 1979, pp. 233–235. Primary harmonic approximation analysis for positive-cost set cover.
6. Wayne E. Smith. [“Various Optimizers for Single-Stage Production”](https://doi.org/10.1002/nav.3800030106), *Naval Research Logistics Quarterly* 3(1–2), 1956, pp. 59–66. Primary single-machine weighted-completion scheduling result.
7. Jon Kleinberg and Éva Tardos. [*Algorithm Design*](https://www.pearson.com/en-us/subject-catalog/p/algorithm-design/P200000003259), Addison-Wesley, 2005. Exchange, stays-ahead, interval scheduling, and greedy-versus-dynamic-programming design patterns.
8. ACM, IEEE Computer Society, and AAAI. [*Computer Science Curricula 2023: Algorithmic Foundations*](https://csed.acm.org/al-cs-core/), endorsed 2024; consulted 2026-09-04. Current curricular scope for greedy strategies, graphs, correctness, optimization, and approximation.

## Exercises

### Exercise 1

Run earliest-finish scheduling on $A=[0,3)$, $B=[1,2)$, $C=[2,4)$, $D=[3,5)$, $E=[4,7)$, $F=[5,6)$, and $G=[6,8)$. Use key $(finish,start,id)$. Give the selected identities, prove optimality by exchange or stays-ahead, and give time/space bounds for sorting plus scanning.

### Exercise 2

Jobs available at time zero are $A:(p=3,d=4)$, $B:(p=2,d=100)$, $C:(p=4,d=7)$, and $D:(p=1,d=5)$. Produce earliest-due-date order, compute every completion, lateness, and $L_{max}$, then give the adjacent-interchange proof and state two model changes that invalidate transferring the result unchanged.

### Exercise 3

Prove descending-weight feasible greedy returns a maximum-weight independent set for a matroid with nonnegative weights. Cover extension to bases, prefix alignment, augmentation/exchange, tied weights, and why heredity without augmentation is insufficient.

### Exercise 4

Construct a Huffman tree for frequencies $(2,3,7,9,18)$. Give every merge weight, one deterministic code using left child before right and symbol order for ties, verify prefix-freeness, compute weighted path length two ways, and summarize the sibling-exchange induction.

### Exercise 5

Engineer positive-cost greedy set cover for a multitenant service-placement system. Specify the contract, exact mutable priority, harmonic guarantee, deterministic and overflow-safe comparison, lazy-heap validation, infeasibility, independent quality checks, adversarial tests, resource bounds, telemetry, and rollout safeguards.

## Answers to the Exercises

### Answer 1

Finish order is

$$
B(2),A(3),C(4),D(5),F(6),E(7),G(8),
$$

where parentheses show finish times. Select $B=[1,2)$, then $C=[2,4)$, then $F=[5,6)$, then $G=[6,8)$. The result is

$$
(B,C,F,G)
$$

of size four.

For exchange, let $g$ be the first greedy activity and $o$ the first activity of an optimal schedule. Because $g$ has minimum finish, $f_g\le f_o$. Replace $o$ with $g$. Every later activity starts at or after $f_o$, hence after $f_g$, so feasibility and cardinality remain. Apply the same argument to the residual activities beginning at or after $f_g$. Induction produces an optimum agreeing with every greedy choice.

Equivalently, prove greedy's $j$th finish is no later than the $j$th finish of any compatible schedule. Then a schedule cannot have an additional activity after greedy stops.

Sorting costs $O(n\log n)$ comparisons and the scan costs $O(n)$. Storing the sorted copy and output uses $O(n)$ auxiliary references; in-place sorting plus streamed output can change the storage accounting. Pre-sorted input permits an $O(n)$ scan.

### Answer 2

Due-date order is

$$
A(d=4),D(d=5),C(d=7),B(d=100).
$$

The ledger is:

- $A$: $C_A=3$, $L_A=3-4=-1$;
- $D$: $C_D=4$, $L_D=4-5=-1$;
- $C$: $C_C=8$, $L_C=8-7=1$;
- $B$: $C_B=10$, $L_B=10-100=-90$.

Thus

$$
L_{max}=1.
$$

Consider adjacent due-date inversion $i,j$ starting at $t$, where $d_i>d_j$. Before swap, completion times are $t+p_i$ and $t+p_i+p_j$. After swap, $j$ completes at $t+p_j$, no later than the pair's old final completion, and $i$ completes at the unchanged pair final time but has the later due date. More directly, both new latenesses are bounded by the maximum of the two old latenesses. Swapping removes one inversion without increasing $L_{max}$. Repetition transforms some optimum into EDD order.

Release times can make the next due job unavailable, and precedence constraints can forbid the exchange. Parallel machines, preemption, weighted tardiness, or minimizing the number of late jobs also require different theorems.

### Answer 3

Let $(E,\mathcal I)$ be a matroid and weights be nonnegative. Heredity implies the greedy prefix remains independent because an element is added only after the oracle accepts it. Augmentation implies every independent set can extend to a basis. Nonnegative weights mean extending a maximum-weight independent set cannot decrease its weight, so compare greedy with an optimal basis of the same rank.

Order elements $g_1,\ldots,g_m$ by nonincreasing weight, including deterministic secondary ties. Inductively maintain an optimal basis $O_i$ containing greedy prefix $G_i=\{g_1,\ldots,g_i\}$. Initially choose any optimal basis.

If $g_i\in O_{i-1}$, take $O_i=O_{i-1}$. Otherwise, because $G_{i-1}\cup\{g_i\}$ is independent and $O_{i-1}$ is a basis containing $G_{i-1}$, basis exchange supplies some

$$
o\in O_{i-1}\setminus G_{i-1}
$$

such that

$$
O_i=(O_{i-1}-\{o\})\cup\{g_i\}
$$

is a basis. No element of $O_{i-1}\setminus G_{i-1}$ can precede $g_i$ in the scan: when such an element was encountered, the then-current greedy prefix was a subset of the independent set $O_{i-1}$, so it would have been accepted and would now belong to $G_{i-1}$. Therefore the exchanged $o$ occurs no earlier than $g_i$, and $w(g_i)\ge w(o)$. Thus $w(O_i)\ge w(O_{i-1})$. Since $O_{i-1}$ was optimal, $O_i$ is also optimal. At termination an optimal basis contains the complete greedy basis, so they coincide in weight.

Equal weights make the exchange non-worsening; the secondary order chooses one of possibly many optimal bases. Heredity alone does not supply the exchange. Compatible intervals show the failure: $\{[0,4)\}$ is independent, as is $\{[0,2),[2,4)\}$, but neither element of the larger set augments the smaller.

### Answer 4

Merge the two least frequencies repeatedly:

$$
2+3=5,
\quad
5+7=12,
\quad
9+12=21,
\quad
18+21=39.
$$

Put the smaller-weight child on the left at each merge. One code is:

- frequency 18: `0`;
- frequency 9: `10`;
- frequency 2: `1100`;
- frequency 3: `1101`;
- frequency 7: `111`.

No codeword is a prefix of another because symbols label leaves of a full binary tree. The weighted path length from depths is

$$
18(1)+9(2)+2(4)+3(4)+7(3)
=18+18+8+12+21
=77.
$$

It also equals the sum of merge weights:

$$
5+12+21+39=77.
$$

In an optimal full prefix tree, two deepest sibling leaves exist. Exchanging the two smallest frequencies with those leaves cannot increase weighted depth. Contract the sibling pair into frequency sum 5. If the contracted tree were not optimal for the reduced alphabet, replacing it with a better reduced tree and expanding the pair would improve the original. Induction therefore validates repeated minimum merging.

### Answer 5

Accept a finite universe $U$, a versioned family of sets with stable identities, and strictly positive exact costs. Require that every universe element be coverable or return a declared infeasibility certificate listing uncovered identities. Output selected set identities, total cost under checked arithmetic, and a coverage certificate. Define whether duplicate elements/sets are normalized and how ties are resolved.

At state $U'$, candidate $S$ has new coverage $k_S=|S\cap U'|$. Ignore $k_S=0$ and minimize exact ratio $c(S)/k_S$, then stable set identity. Compare candidates $A,B$ using

$$
c(A)k_B<c(B)k_A
$$

with widened checked integers or exact rationals; equality uses the secondary key. After selecting $S$, remove $S\cap U'$ and update affected sets through an inverted element-to-set index.

For a lazy heap, store cost, cached new-count, state version, and identity. On pop, recompute the candidate against current $U'$. If its key changed, push the new version and continue; accept only a current top after proving no stored bound can hide a better ratio. Simpler full recomputation is the correctness baseline. Bound heap entries and compact obsolete versions.

Charge each newly covered element $c(S)/k_S$. For any optimum set $T$, when $r$ of its elements remain uncovered, greedy's chosen ratio is at most $c(T)/r$. The charges to elements of $T$ sum to at most $H_{|T|}c(T)$. Assigning every charge through an optimal cover yields

$$
cost(G)\le H_d\,cost(OPT),
\qquad d=\max_S|S|.
$$

This proves an approximation, not exactness.

For bounded fixtures, enumerate all set subsets or use an independently modeled integer program to verify feasibility, optimum, observed ratio, and certificate. Include empty universe, uncovered elements, duplicate sets, dominated sets, all ties, one giant set, singleton sets, highly overlapping sets, extreme costs, cross-product overflow, stale-entry storms, concurrent input mutation, cancellation, and tenant resource exhaustion. Preserve known near-worst cases.

Bound universe/set incidences, heap entries, recomputations, arithmetic width, CPU, memory, and cancellation latency. Emit privacy-safe counts: input sizes, chosen count/cost, coverage progress, stale pops, recomputations, maximum heap, certificate ratio against a lower bound when available, failures, and latency/resource quantiles. Do not log sensitive element identities by default.

Version normalization, ratio comparison, tie order, update scheme, and proof assumptions. Canary lazy updates against the full-recompute implementation, compare outputs and costs on sampled requests, and roll back on coverage mismatch, comparator inconsistency, heap/resource spikes, or quality regression. Keep the exact key recomputation path as the safety fallback.
