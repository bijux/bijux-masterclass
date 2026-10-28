---
module_id: ALGE-065
program: Algorithm Engineering
level: 2
module_number: 65
title: Local Search
status: complete
last_verified: 2026-09-05
---

# Local Search

## One-Page Review

### Governing question

How can an engineer define, analyze, implement, and evaluate a neighborhood-based improvement algorithm without confusing local optimality, termination, empirical quality, and a proved global approximation guarantee?

### Essential definitions

- A **solution space** is the set of feasible states the search may visit.
- A **neighborhood** $N(S)$ maps state $S$ to candidate states reachable by one allowed move.
- A **local optimum** has no strictly improving neighbor under the declared neighborhood.
- **First improvement** accepts the first improving move; **best improvement** selects the largest improvement found.
- A **locality gap** is the worst ratio between a neighborhood-local optimum and global optimum over an instance class.
- A **plateau** contains equal-objective states; a **strict** search does not traverse it.
- A **restart** begins from another initial state under a declared sampling or construction policy.
- A **move delta** computes objective change without evaluating the whole candidate from scratch.
- A **tabu rule**, annealing acceptance, or perturbation changes local search into a metaheuristic with a different evidence contract.

### Central model, mechanism, or theorem

For nonnegative weighted Max-Cut, let $S$ be locally optimal under single-vertex flips. For every vertex $v$, the weight $c_v$ of incident cut edges is at least the weight $u_v$ of incident uncut edges; otherwise flipping $v$ improves the cut. Summing over vertices counts every edge twice:

$$
2w(\delta(S))=\sum_vc_v\ge\sum_vu_v=2(W-w(\delta(S))).
$$

Therefore $w(\delta(S))\ge W/2\ge OPT/2$. The guarantee comes from this neighborhood-specific inequality. A different move, negative edge weights, approximate deltas, or premature stopping needs a new proof.

### Critical invariants

- Every current state and accepted neighbor is feasible under the original constraints.
- An accepted strict move changes the objective in the promised direction under exact semantics.
- Candidate deltas, caches, and committed objective remain consistent.
- Tie order, scan order, restart seed, and stop conditions are explicit.
- Termination follows from finite states, quantized progress, or a proved potential bound.
- Approximation claims apply to the actual terminal condition and neighborhood.
- Best-of-run selection uses a held-out or predeclared evaluation rule and retains every run's evidence.

### Common failures

Common failures include calling a local optimum globally optimal; changing the neighborhood without redoing the proof; accepting equal moves and cycling; assuming integer objectives imply polynomial runtime; using stale deltas after a move; allowing infeasible intermediate states without a repair theorem; terminating after a sample of neighbors yet claiming full local optimality; tuning restart counts on the benchmark test set; comparing stochastic variants without paired seeds or uncertainty; and hiding that parallel races choose a different move sequence.

### Compact example

On a four-cycle, partition $S=\{0,1\}$ cuts two of four edges. Each vertex has one cut and one uncut incident edge, so no single flip strictly improves it. The global alternating partition cuts all four. The state is a valid one-flip local optimum with value exactly half of optimum, witnessing tightness of the general factor.

### Connections

[ALGE-064](./064-primal-dual-approximation.md) constructs certificates through dual growth. This chapter uses neighborhoods and potential improvement. [ALGE-066](../ROADMAP.md#block-07--approximation-heuristics-and-randomized-algorithms) owns randomized selection and sampling. Testing owns oracle comparison and experimental design; Software Delivery owns bounded execution and rollback.

## Governing Question

Given a combinatorial objective and feasible solution, how do we specify a neighborhood, find and commit improving moves, prove what terminal states mean, control runtime and numerical behavior, and distinguish theorem-backed quality from empirical heuristic performance?

Local search is a framework, not one algorithm. The solution representation, neighborhood, move enumeration, acceptance, ties, plateaus, initialization, stopping, and restarts jointly define behavior. “We used local search” is too incomplete to reproduce, analyze, or deploy.

## Why This Matters

Many production optimization problems are too large, dynamic, or richly constrained for exact search on every request. Local search can start from an existing feasible plan, deliver monotone improvements, exploit problem-specific deltas, and stop at a deadline with a usable incumbent. It underlies routing, placement, clustering, scheduling, partitioning, and assignment systems.

Its apparent simplicity is deceptive. A larger neighborhood can improve terminal quality but make move search expensive. Strict improvements guarantee eventual termination in a finite state space, not polynomial time. Practical shortcuts such as candidate lists, approximate nearest neighbors, parallel batches, and floating acceptance thresholds alter the neighborhood or terminal condition.

Rigorous use therefore has two tracks: prove properties for the precisely declared algorithm where possible, and evaluate unproved enhancements with reproducible, bias-resistant experiments.

## Prerequisites and Retrieval

Retrieve [ALGE-061](./061-approximation-ratios-and-guarantees.md), [ALGE-062](./062-greedy-approximation.md), graph cuts, exchange arguments, potential functions, exact arithmetic, amortized analysis, randomized experiments, and statistical uncertainty.

This chapter derives single-flip Max-Cut, then develops neighborhood strength, move policies, plateaus, restarts, deltas, acceleration, concurrency, and evidence. ALGE-069 owns broad metaheuristic evidence requirements; ALGE-095 and ALGE-096 own parameter tuning and statistical implementation comparison in depth.

## Learning Objectives

After completing this module, you should be able to:

1. specify a complete local-search state machine;
2. prove feasibility and strict potential improvement for accepted moves;
3. distinguish local optimum, maximal solution, global optimum, and approximation;
4. derive the one-flip Max-Cut factor-two guarantee;
5. analyze how neighborhood size changes quality and move cost;
6. identify when strict termination does not imply polynomial runtime;
7. implement and validate incremental move deltas;
8. design honest restart, plateau, and deadline policies;
9. preserve semantics under candidate pruning and parallel evaluation; and
10. report proofs, certificates, traces, and empirical results at their actual strength.

## Core Exposition

### Specify the state machine

For minimization, define feasible states $F$, objective $f:F\to\mathbb R$, neighborhood $N(S)\subseteq F$, initialization $S_0$, candidate enumeration, move selection, acceptance, tie rule, and stop condition. A strict descent step requires $f(S')<f(S)$. Maximization reverses the inequality.

First improvement depends on enumeration order. Best improvement needs every eligible delta or a data structure that proves no omitted candidate is better. Random choice among improving moves defines a probability distribution. A sampled neighborhood can be useful, but stopping after a sample establishes only “no sampled improvement,” not local optimality in $N(S)$.

Representation matters. Two encodings of the same mathematical solution can appear as different states and create zero-cost cycles. Canonicalize symmetric labels or incorporate symmetry into visited-state and tie semantics.

### Establish feasibility before quality

The cleanest local search moves only between feasible states. A $k$-median swap closes and opens equal numbers of facilities so cardinality remains $k$. A TSP 2-opt move reconnects two tour edges so one Hamiltonian cycle remains. A Max-Cut flip moves one vertex and cannot violate partition feasibility.

Some methods traverse infeasible states using penalties or repair. Then the optimized penalized objective is not automatically the original objective. A fixed penalty may prefer constraint violation; dynamic penalties can make accepted objective values incomparable across time. Prove exactness of the penalty, analyze repair, or label the method heuristic and verify final feasibility independently.

Assertions on the final state are necessary but not sufficient. Move generators should preserve representation invariants, and mutation should be transactional: calculate and validate a candidate, then commit all state and cache changes atomically.

### Prove termination at the right strength

In a finite solution space, accepting only strict objective improvements prevents revisiting a state and guarantees eventual termination. This says nothing about a polynomial number of moves when objective values have fine precision or the state space is exponential.

If objectives are nonnegative integers bounded by polynomial $B$ and every move improves by at least one, there are at most $B$ moves. If improvement must be at least $\epsilon f(S)$ for minimization, then geometric decrease can bound iterations once a positive lower scale is known. Scaling or accepting only sufficiently large improvements may make runtime polynomial while weakening local optimality and approximation by an explicit additive or multiplicative slack.

Equal moves break the strict-potential proof. Plateau traversal requires a secondary acyclic potential, a visited-state rule with bounded memory, or a finite move budget. Floating comparisons require a tolerance policy connected to recomputed objective; `new < old - eps` is a different acceptance rule from exact descent.

### Derive one-flip Max-Cut

Let undirected edge weights be nonnegative and total weight be $W$. For partition $S,V\setminus S$, write $C=w(\delta(S))$. At a one-flip local optimum, every vertex $v$ has crossing incident weight $c_v$ at least uncut incident weight $u_v$, because flipping changes the objective by $u_v-c_v$.

Summing $c_v\ge u_v$ gives $2C\ge2(W-C)$: every cut and uncut edge is incident to two vertices. Hence $C\ge W/2$. Since no cut can exceed total edge weight, $OPT\le W$, so $C\ge OPT/2$.

Nonnegative weights are essential to $OPT\le W$ and to the interpretation of incident totals. The theorem applies only when all one-vertex flips have been checked under exact weights. It does not claim every intermediate state has factor two, although the algorithm can begin with any feasible partition and strict improvement never reduces value.

This implementation uses best improvement and stable vertex ties. Brute force supplies an oracle for examples, not a subroutine of local search.

<!-- bijux-verify: {"id":"max-cut-one-flip-local-search","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"triangle side=(0,) cut=2 optimum=2 moves=((0, 2),)\ntrap side=(0, 1) cut=4 optimum=5 moves=((0, 3), (1, 1))\ncycle-local side=(0, 1) cut=2 optimum=4 moves=()\n","stderr":""}} -->
```python
def cut_value(edges, side):
    return sum(weight for u, v, weight in edges if (u in side) != (v in side))


def one_flip(vertices, edges, initial=()):
    side = set(initial)
    moves = []
    while True:
        current = cut_value(edges, side)
        improving = []
        for vertex in vertices:
            candidate = side ^ {vertex}
            gain = cut_value(edges, candidate) - current
            if gain > 0:
                improving.append((-gain, vertex, candidate))
        if not improving:
            return tuple(sorted(side)), current, tuple(moves)
        negative_gain, vertex, side = min(improving)
        moves.append((vertex, -negative_gain))


def exact_max_cut(vertices, edges):
    return max(
        cut_value(edges, {v for i, v in enumerate(vertices) if mask >> i & 1})
        for mask in range(1 << len(vertices))
    )


cases = {
    "triangle": ((0, 1, 2), ((0, 1, 1), (0, 2, 1), (1, 2, 1)), ()),
    "trap": (
        (0, 1, 2, 3, 4),
        ((0, 1, 1), (0, 2, 1), (0, 3, 1), (1, 2, 1), (1, 4, 1), (2, 3, 1)),
        (),
    ),
    "cycle-local": (
        (0, 1, 2, 3),
        ((0, 1, 1), (1, 2, 1), (2, 3, 1), (0, 3, 1)),
        (0, 1),
    ),
}
for name, (vertices, edges, initial) in cases.items():
    side, value, moves = one_flip(vertices, edges, initial)
    optimum = exact_max_cut(vertices, edges)
    print(f"{name} side={side} cut={value} optimum={optimum} moves={moves}")
```

### Understand the locality gap

For maximization, the locality gap can be expressed as $\sup OPT/L$ over positive-valued local optima $L$; for minimization, use $\sup L/OPT$ under positive denominators. The neighborhood and instance class are part of the definition. The four-cycle partition in the review has $OPT/L=2$, so the one-flip Max-Cut analysis is tight.

A locality-gap proof typically maps optimum components to local moves and sums the non-improvement inequalities. In metric $k$-median, multi-swaps and metric reassignment produce bounds that improve as swap size grows. This is a problem-specific structural argument; the fact that larger neighborhoods contain smaller ones only says terminal solutions cannot be worse under exact exhaustive search, not what factor they achieve.

Gap witnesses are valuable regression fixtures. Store the instance, initial state, terminal state, all checked deltas, optimum or certified bound, and neighborhood version. A claimed improvement in a heuristic should not silently remove adversarial cases from evaluation.

### Choose neighborhood strength and search policy

A larger neighborhood may escape shallow local optima but can contain $\Theta(n^k)$ or more moves. Variable-neighborhood search expands move types after smaller moves fail. Ejection chains compose dependent changes. Lin-Kernighan-style routing search varies exchange depth using gain criteria. These can be highly effective without a universal factor for every implementation variant.

Best improvement performs more candidate work per accepted move and may take fewer moves; first improvement can exploit early exits and locality but is order-sensitive. Neither dominates universally. Candidate lists restrict search to promising moves and improve speed, but a terminal state is local only with respect to that restricted neighborhood unless a completeness argument recovers the full one.

Tie policies affect trajectories even when objective remains monotone. Use stable object IDs for deterministic service behavior, or record random streams. Avoid address, hash-table, worker-completion, or wall-clock order as implicit tie breakers.

### Maintain deltas as derived state

Recomputing every candidate objective may be too slow. Delta evaluation updates only affected terms: a vertex flip changes incident cut edges; a facility swap changes client assignments; a 2-opt route move replaces a small edge set. A delta cache is derived state and must be invalidated for every move whose affected region overlaps it.

Use checked arithmetic. Subtracting large nearly equal unsigned totals can underflow; floating cancellation can reverse a tiny gain. Periodically recompute the entire objective from canonical state and compare it with accumulated deltas. On mismatch, fail closed or rebuild caches; do not keep optimizing a fictional objective.

Property tests should compare every incremental delta with full recomputation on small random and exhaustive states. Mutation tests can corrupt one dependency edge or cache version to ensure the checker detects stale data.

### Handle plateaus, cycling, and diversification

Strict search stops on plateaus, possibly at a poor basin boundary. Allowing equal or worsening moves can escape but removes monotonicity and may cycle. Tabu tenure forbids recent reversals; simulated annealing accepts worsening moves probabilistically; iterated local search applies perturbations; restarts change initialization. Each adds parameters and stochastic evidence requirements.

Do not report “locally optimal” after an accepted worsening move until the algorithm again exhausts the declared neighborhood. Aspiration rules and tabu restrictions mean a tabu terminal state may still have an improving forbidden neighbor. State the exact terminal predicate.

Restart performance depends on the distribution of initial states and correlations among runs. Best of $r$ trials is selected data and will improve mechanically with $r$. Compare methods under equal declared budgets, retain all trial outcomes, report distributions and uncertainty, and keep tuning separate from final evaluation.

### Bound execution and anytime behavior

Production search needs time, move, memory, and cancellation limits. Check cancellation at stable points; leave the last fully committed feasible state publishable. A deadline may interrupt neighborhood enumeration, so the result is an incumbent, not a certified local optimum. Record evaluated candidates, neighborhood coverage, last full sweep, and termination reason.

An anytime trace contains timestamp or deterministic work count, objective, certified bound if any, and state digest. Wall-clock comparisons require controlled environments; candidate evaluations are often a more portable effort measure. Warm starts should be identified because they can dominate outcome quality.

If a proof requires exact local optimality, an approximate terminal rule may support a degraded theorem. Derive the slack explicitly. Otherwise retain only the feasibility and empirical claims supported by evidence.

### Parallelize without changing the algorithm accidentally

Candidate evaluation from one immutable snapshot is embarrassingly parallel. Reduce results by objective delta and stable move ID, then atomically commit one winner. This reproduces deterministic best improvement. Committing several individually improving moves concurrently is safe only when they are independent and their combined delta equals the sum.

Conflicting moves can make each other infeasible or jointly worsening. Optimistic execution must validate versions and recompute combined feasibility and objective before commit. Asynchronous local search is a legitimate different heuristic, but single-thread approximation or local-optimum proofs do not transfer automatically.

Distributed replicas also need one canonical incumbent sequence or clearly independent restart identities. Merging “best state” is easy; merging partially applied move traces is not.

### Design proof-aware experiments

First verify feasibility, objective recomputation, terminal predicate, and trace replay. Use exhaustive small instances to compare against optimum and enumerate every neighbor. Include known locality-gap witnesses, symmetric ties, plateaus, overflow boundaries, and cache invalidation adversaries.

For empirical quality, define workload strata, initializers, move budget, restart budget, seed schedule, baselines, hardware, implementation version, and metrics before examining results. Report objective gaps against exact optima or valid bounds when available, not against an undocumented “best known.” Pair seeds or instances for comparisons and report uncertainty rather than only the best run.

Observed success does not prove a locality bound or convergence to global optimum. Conversely, a worst-case bound does not establish latency or typical quality. Maintain both proof evidence and experimental evidence without blending their claims.

## Definitions and Notation

Let $F$ be feasible states, $f(S)$ the objective, $N(S)$ a neighborhood, $\Delta(S,S')=f(S')-f(S)$ for maximization, $L$ a terminal local value, and $OPT$ the global value.

- A **move operator** constructs a neighboring state and its affected region.
- A **terminal predicate** states exactly which candidates have no accepted improvement.
- A **basin of attraction** is the set of starts reaching a terminal state under fixed policy.
- A **candidate list** is a restricted subset of the conceptual neighborhood.
- A **full sweep** evaluates every eligible move in the declared neighborhood from one state.
- **Diversification** deliberately changes trajectory to explore another basin.
- **Intensification** spends more search near promising states.
- An **incumbent** is the best verified feasible state retained so far.

## Mechanisms, Invariants, or Proof Structure

### Feasible monotone transition invariant

Every committed state belongs to $F$. Each strict accepted move improves the exact original objective. State, objective, auxiliary indexes, and delta caches commit atomically or roll back together.

### Terminal-scope invariant

“Local optimum” names the neighborhood, acceptance tolerance, and coverage actually exhausted. Candidate-pruned, sampled, tabu-restricted, timed-out, or approximate searches use narrower terminal labels.

### Max-Cut charging invariant

At one-flip local optimality, each vertex's crossing incident weight dominates uncut incident weight. Summing counts both classes twice and produces $C\ge W/2\ge OPT/2$ under nonnegative weights.

### Evidence-separation invariant

Universal proof, exact finite oracle results, benchmark distributions, and operational traces retain distinct labels. No number of successful trials is promoted into a theorem.

## Alternatives and Trade-Offs

| Choice | Benefit | Risk | Evidence |
|---|---|---|---|
| First improvement | Early exit, cheap sweeps | Order-sensitive trajectory | Stable enumeration and trace |
| Best improvement | Strongest scanned step | Expensive full neighborhood | Complete delta reduction |
| Larger neighborhood | Better exact local optimum | Combinatorial move cost | Locality proof and coverage |
| Candidate lists | Faster search | Missed improving moves | Restricted-neighborhood label |
| Equal/worse moves | Escapes plateaus | Cycling and lost monotonicity | Secondary rule and budget |
| Restarts | Explore multiple basins | Selection bias and cost | Seeded trial distribution |
| Parallel evaluation | Higher throughput | Stale/conflicting commits | Snapshot and deterministic reduction |
| Exact optimization | Global certificate | Potentially high runtime | Bound/optimality evidence |

## Failure Modes and Misconceptions

- **“Local optimum means optimum.”** It quantifies only one neighborhood.
- **“Strict improvement is polynomial.”** It proves finite termination, not a polynomial move count.
- **“A larger neighborhood is free quality.”** Exhaustive move search can become intractable.
- **“No sampled improvement means local optimum.”** Unexamined moves remain possible.
- **“Equal moves are harmless.”** They can create cycles among symmetric encodings.
- **“Cached deltas are the objective.”** They are derived state requiring validation.
- **“Negative edge weights preserve Max-Cut factor two.”** The proof consumes nonnegativity.
- **“A deadline is a local-optimum certificate.”** It usually returns only an incumbent.
- **“More restarts prove robustness.”** Selection and tuning can bias reported results.
- **“Parallel improving moves combine.”** Conflicts can make the batch infeasible or worsening.
- **“Metaheuristic enhancements inherit the base proof.”** Changed acceptance and stopping require new analysis.
- **“Worst-case factor predicts production quality.”** Latency and workload distributions need separate evidence.

## Worked Examples

### Example 1

**Situation.** A triangle begins with every vertex on the same side.

Any vertex flip cuts its two incident edges, gaining two. After the flip, moving either remaining vertex changes one cut edge to uncut and one uncut to cut, while reversing the first vertex loses two. The cut value 2 is locally and globally optimal.

**Conclusion.** A short strict trajectory can reach optimum, but that is instance evidence only.

### Example 2

**Situation.** A four-cycle starts with adjacent vertices $\{0,1\}$ on one side.

Exactly two edges cross. Every vertex has one crossing and one uncut incident edge, so every flip has delta zero. Strict one-flip search stops, while alternating sides cut all four edges.

**Conclusion.** The one-flip locality gap of two is attained.

### Example 3

**Situation.** A maximization state has candidate gains 7, 7, and 3.

Best improvement with stable IDs chooses the lower-ID gain-seven move. First improvement chooses whichever gain-seven or gain-three move appears first. Both improve now, but may enter different basins.

**Conclusion.** Enumeration and tie order are algorithm semantics.

### Example 4

**Situation.** An integer objective begins at 1,000,000 and improves by one each move.

Strict improvement guarantees termination in at most one million moves for this bounded instance. If the encoded objective bound is exponential in input bits, the same argument is not polynomial in input length.

**Conclusion.** Count progress relative to encoding size, not numeric intuition.

### Example 5

**Situation.** A route delta cache predicts a 2-opt gain of 12, but full recomputation shows a loss of 4.

An earlier move changed one cached boundary edge without invalidation. Reject and rebuild; committing would violate monotonicity and corrupt all later stopping claims.

**Conclusion.** Incremental deltas need dependency-complete invalidation and full checks.

### Example 6

**Situation.** Search examines 1,000 of 10,000 swaps and finds no improvement before timeout.

The state is not a full-neighborhood local optimum. Report a feasible incumbent, sampled coverage 10%, selection policy, and termination reason; retain the best verified state.

**Conclusion.** Terminal labels must match actual neighborhood coverage.

### Example 7

**Situation.** Two independently improving facility swaps both close the same facility.

Their deltas were measured from one snapshot. Applying both can violate the facility count and invalidate client assignments. Commit one deterministic winner or validate the combined move as a distinct neighbor.

**Conclusion.** Parallel evaluation is safer than parallel mutation.

### Example 8

**Situation.** Twenty restarts produce costs; a report gives only the minimum.

The minimum reflects both algorithm quality and selection from twenty opportunities. Retain all results, median and tails, seeds, budget, initializer, and comparison baseline. Use a separate tuning set for restart count.

**Conclusion.** Best-of-run reporting without its selection process is misleading.

### Example 9

**Situation.** Floating objective improves from $10^{12}$ to $10^{12}-10^{-5}$ according to a delta sum.

The change may be below representable resolution at that scale. Recompute with scaled integers, compensated/exact arithmetic, or an explicit tolerance; do not claim strict descent from a lost subtraction.

**Conclusion.** Numerical semantics determine whether a move is truly improving.

### Example 10

**Situation.** A one-flip Max-Cut implementation returns value 60 on total nonnegative edge weight 100 but has not checked three vertices.

The value exceeds $W/2$, so this particular state already has a factor-two guarantee from $OPT\le W$, independent of local optimality. It cannot be labeled locally optimal, and a stronger neighborhood-derived claim still requires the missing checks.

**Conclusion.** Separate value certificates from terminal certificates.

## Cross-Program Connections

- **Algorithm Engineering:** [ALGE-064](./064-primal-dual-approximation.md) supplies constructive lower bounds; [ALGE-066](../ROADMAP.md#block-07--approximation-heuristics-and-randomized-algorithms) develops sampling used in randomized neighborhoods.
- **Data Structures Engineering:** owns dynamic neighborhoods, candidate indexes, delta caches, versioning, and priority structures.
- **Concurrent and Parallel Programming:** owns snapshot isolation, deterministic reductions, conflict detection, and atomic move commit.
- **Software Testing:** owns exhaustive neighbor oracles, trace replay, mutation tests, seed pairing, and uncertainty-aware comparison.
- **Software Delivery and Reliability Engineering:** owns deadlines, cancellation, rollback, resource limits, telemetry, and incumbent publication.
- **Data Engineering:** owns representative instance corpora, leakage-free tuning splits, and benchmark lineage.
- **Theory of Computation:** owns PLS and complexity distinctions between verifying and finding local optima.

## References

1. David P. Williamson and David B. Shmoys, [“Greedy Algorithms and Local Search”](https://www.cambridge.org/core/books/abs/design-of-approximation-algorithms/greedy-algorithms-and-local-search/5CB0128EBCA19A51353C64A425B57FFE), in *The Design of Approximation Algorithms*, Cambridge University Press, 2011/2012, doi:10.1017/CBO9780511921735.003. Publisher chapter checked 2026-09-05.
2. David S. Johnson, Christos H. Papadimitriou, and Mihalis Yannakakis, “How Easy Is Local Search?”, *Journal of Computer and System Sciences* 37(1), 79–100, 1988, [doi:10.1016/0022-0000(88)90046-3](https://doi.org/10.1016/0022-0000(88)90046-3). Primary PLS source; publisher and DBLP records checked 2026-09-05.
3. Vijay Arya, Naveen Garg, Rohit Khandekar, Adam Meyerson, Kamesh Munagala, and Vinayaka Pandit, “Local Search Heuristics for k-Median and Facility Location Problems,” *SIAM Journal on Computing* 33(3), 544–562, 2004, [doi:10.1137/S0097539702416402](https://doi.org/10.1137/S0097539702416402). Primary locality-gap source; SIAM/Duke record checked 2026-09-05.
4. Shen Lin and Brian W. Kernighan, “An Effective Heuristic Algorithm for the Traveling-Salesman Problem,” *Operations Research* 21(2), 498–516, 1973, [doi:10.1287/opre.21.2.498](https://doi.org/10.1287/opre.21.2.498). Primary routing-heuristic source; INFORMS/Princeton record checked 2026-09-05.
5. Emile Aarts and Jan Karel Lenstra, eds., [*Local Search in Combinatorial Optimization*](https://press.princeton.edu/books/paperback/9780691115221/local-search-in-combinatorial-optimization), Princeton University Press, 2003. Framework, neighborhoods, complexity, and applications reference.
6. Bernhard Korte and Jens Vygen, [*Combinatorial Optimization: Theory and Algorithms*](https://link.springer.com/book/10.1007/978-3-662-56039-6), 6th edition, Springer, 2018, doi:10.1007/978-3-662-56039-6. Combinatorial optimization and approximation reference.
7. Holger H. Hoos and Thomas Stützle, *Stochastic Local Search: Foundations and Applications*, Morgan Kaufmann, 2004, ISBN 978-1558608726. Stochastic search, restart, configuration, and empirical methodology reference.

## Exercises

### Exercise 1

Define a complete local-search algorithm for minimization. Distinguish feasibility, strict descent, termination, neighborhood-local optimality, and global approximation.

### Exercise 2

For a weighted triangle with edge weights $w_{01}=4$, $w_{02}=2$, and $w_{12}=3$, start from the empty side and run stable-ID best-improvement one-flip Max-Cut. Show every candidate delta, move, terminal condition, total weight, exact optimum, and factor certificate.

### Exercise 3

A scheduler accepts swaps using cached floating deltas, allows equal moves, and stops after 10,000 sampled pairs. Design invariants and tests that make its actual guarantees and terminal status honest.

### Exercise 4

Compare first improvement, best improvement, a complete two-swap neighborhood, and a candidate-pruned two-swap neighborhood. Address move cost, trajectory, terminal meaning, locality gap, determinism, parallelism, and deadline behavior.

### Exercise 5

A placement service tunes neighborhoods, restart count, seeds, and timeout on the same 200 workloads later used to claim superiority over an exact solver. Design a defensible proof-and-experiment contract for deployment.

## Answers to the Exercises

### Answer 1

Specify feasible set $F$, objective $f$, initializer, neighborhood $N(S)\subseteq F$, complete candidate enumeration, acceptance $f(S')<f(S)$, selection/tie rule, atomic update, and stop when a full sweep finds no accepted move. Feasibility says every published state is valid; strict descent plus finite $F$ proves termination, though not necessarily polynomial runtime. Exhausting $N(S)$ proves only neighborhood-local optimality. A global factor requires a separate locality-gap proof for that exact neighborhood, instance class, and terminal slack. A timeout or sampled sweep returns an incumbent, not that local certificate.

### Answer 2

At the empty side, flipping 0 cuts weights $4+2=6$, flipping 1 cuts $4+3=7$, and flipping 2 cuts $2+3=5$; choose vertex 1. The cut contains edges 01 and 12, value 7. From $\{1\}$, flipping 0 changes value by $2-4=-2$, flipping 1 by $-7$, and flipping 2 by $2-3=-1$, so it is locally optimal. Total weight is 9, giving generic bound $7\ge9/2\ge OPT/2$. Enumerating triangle cuts gives optimum 7, attained by isolating vertex 1. The realized result is optimal, but the neighborhood theorem alone promises only factor two.

### Answer 3

Maintain canonical feasible assignments, a full recomputed objective, versioned delta dependencies, and atomic state/cache commits. Compare every cached delta with full recomputation in exhaustive small tests, after adversarial overlapping moves, and periodically in production. Use scaled integers or a documented tolerance; equal moves need an acyclic secondary potential, visited-state rule, or budget because strict descent no longer proves termination. Record initializer, sampler, seed, unique pairs examined, objective trace, and cancellation. After 10,000 sampled pairs label the result feasible incumbent with sampled-neighborhood evidence, not pair-swap local optimum. Only a complete verified sweep earns that label.

### Answer 4

First improvement can stop candidate evaluation early but depends on scan order. Best improvement exhausts its declared neighborhood and chooses the greatest delta, which parallel snapshot evaluation can reproduce through stable reduction. Complete two-swap search offers a stronger terminal predicate and potentially smaller locality gap but often costs quadratic or worse per sweep. Candidate pruning reduces work but proves optimality only for the restricted neighborhood unless completeness is established. All four need deterministic enumeration or recorded randomness, exact feasibility/deltas, and deadline labels; a partial sweep returns an incumbent. No method inherits another neighborhood's factor automatically.

### Answer 5

Freeze mathematical constraints, objective, neighborhood semantics, feasibility checks, and any theorem separately from performance tuning. Split workloads by provenance into training/tuning and held-out evaluation strata; prevent near-duplicate leakage. Predeclare baselines, exact-solver limits and gaps, seed schedule, restart and resource budgets, hardware, metrics, failure treatment, and statistical comparison. Retain all trials, not only winners, and report distributions, paired differences, uncertainty, time-to-target, and unresolved exact bounds. Validate every final placement and trace. Reevaluate under drift and adversarial failures. Any factor claim must come from a proof covering the deployed variant; empirical superiority is limited to the sampled held-out workload and recorded environment.
