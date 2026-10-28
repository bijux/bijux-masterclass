---
module_id: ALGE-026
program: Algorithm Engineering
level: 1
module_number: 26
title: Branch and Bound
status: complete
last_verified: 2026-09-04
---

# Branch and Bound

## One-Page Review

### Governing question

How can an exact optimization search use feasible incumbents and mathematically valid node bounds to discard noncompetitive subproblems while retaining an auditable optimality or interruption certificate?

### Essential definitions

- A **branch** partitions or covers a node's feasible completions with child subproblems.
- An **incumbent** is the best feasible complete solution found so far.
- For minimization, the incumbent value $U$ is a global upper bound on the optimum.
- A **node lower bound** $L(p)$ is no greater than the best feasible completion below node $p$.
- A **relaxation** removes or weakens constraints so its optimum bounds the original subproblem.
- A node is **fathomed** when infeasible, solved exactly, or unable to improve the incumbent.
- The **frontier** contains generated subproblems not yet processed.
- **Best-bound search** selects a frontier node with the smallest lower bound in minimization.
- An **absolute optimality gap** is the incumbent upper bound minus a valid global lower bound.
- **Anytime status** reports the incumbent and remaining bound when search stops before proof.

### Central model, mechanism, or theorem

For minimization, let $\mathcal C(p)$ be feasible completions below node $p$ and

$$
z^*(p)=
\min_{x\in\mathcal C(p)}f(x),
$$

with $z^*(p)=+\infty$ when no completion exists. A valid bound satisfies

$$
L(p)\le z^*(p).
$$

A feasible incumbent $\hat x$ supplies $U=f(\hat x)$ and $z^*\le U$. If only a strictly better objective is required, then

$$
L(p)\ge U
$$

proves no descendant can improve the incumbent, so $p$ may be pruned. If all optimal witnesses or a smaller secondary tie key are required, equality may still matter and the prune must be weakened or strengthened with a tie-aware bound.

If branching covers all feasible completions, bounds are valid, incumbents are feasible, arithmetic is conservative, and finite search terminates, exhaustion proves the final incumbent optimal. For frontier $Q$, a valid global lower bound is

$$
\underline z=
\min\left(
U,
\min_{p\in Q}L(p)
\right),
$$

where the inner minimum is $+\infty$ for an empty frontier. The absolute certified gap is $U-\underline z$ when $U$ is finite.

### Critical invariants

- Every feasible solution remains in the incumbent or at least one live child unless soundly fathomed.
- The incumbent always corresponds to a fully validated feasible solution.
- Every node bound has the correct direction for the objective and declared numeric model.
- A prune comparison respects whether equal-objective alternatives are still required.
- Branch children cover the parent subproblem; overlaps are recorded if duplicate work is possible.
- The frontier's stored bounds match node revisions or are conservatively recomputed.
- The reported global bound includes the incumbent when it may already be optimal.
- Floating-point rounding never makes a minimization lower bound falsely too high.
- Interrupted search reports feasible and dual bounds separately and never claims optimality without a closed gap.
- Parallel workers publish only validated incumbents and aggregate a globally valid frontier certificate.

### Common failures

Common failures include reversing lower and upper bounds; treating a heuristic solution as a lower bound in minimization; publishing an infeasible incumbent; pruning at equality while promising every optimum; solving a relaxation in the wrong direction; using a bound derived under violated sign assumptions; allowing floating-point rounding to overstate a lower bound; adding costs into fixed-width overflow; forgetting active nodes in the global certificate; using a stale priority as a stale bound; reporting local queue exhaustion as global completion; timing out and returning `optimal`; spending more on a tight bound than it saves; and trusting a learned prune score without a conservative mathematical envelope.

### Compact example

In minimum vertex cover, node $p$ has already selected vertices $S$ and leaves uncovered edge set $E_p$. Any set of pairwise vertex-disjoint uncovered edges is a matching, and every completion must select at least one endpoint per matching edge. Therefore

$$
L(p)=|S|+|M_p|
$$

is a valid lower bound for any matching $M_p\subseteq E_p$. Branch on uncovered edge $(u,v)$ by selecting $u$ or $v$. A feasible cover of size 5 gives $U=5$; any node with $L(p)\ge5$ cannot improve the objective, though equality pruning does not preserve every size-5 cover.

### Connections

[ALGE-025](./025-backtracking.md) supplies exhaustive candidate-tree correctness, [ALGE-022](./022-greedy-choice-and-exchange-arguments.md) can construct incumbents, [ALGE-023](./023-dynamic-programming-state-design.md) explains safe state merging, and [ALGE-027](../ROADMAP.md) uses balanced enumeration rather than incumbent bounds.

## Governing Question

What information certifies that an unexplored subproblem cannot contain a solution better than the best feasible one already known?

Backtracking removes branches proved infeasible. Branch and bound adds an optimization comparison: a node may contain feasible solutions, yet a valid optimistic bound proves none can improve the incumbent. That one comparison can eliminate most of a search tree—or silently delete the optimum if its direction, arithmetic, or assumptions are wrong.

The method is also a certificate framework. At any moment it can separate the best feasible objective found from a valid bound on what unexplored work might achieve. Search order changes how quickly these numbers meet; it does not change what makes them valid.

## Why This Matters

Branch and bound underlies discrete and mixed-integer optimization, traveling-salesperson solvers, scheduling, assignment, covering, routing, verification, and configuration. Exact algorithms often owe practical success not to a better worst-case class but to strong formulations, good incumbents, tight inexpensive bounds, effective branching, and disciplined node management.

Production systems need more than a final number. They may stop under a deadline and require a certified gap. They may distribute nodes across workers and need a global completion condition. They may compare decimal costs where one upward rounding error can prune the true optimum. They may accept a fast heuristic incumbent that is invalid under a rarely checked constraint and thereby corrupt every subsequent prune.

An engineering treatment therefore maintains two kinds of evidence: primal evidence from feasible solutions and dual or relaxation evidence from optimistic bounds. Neither may impersonate the other.

## Prerequisites and Retrieval

Retrieve:

- minimization and maximization, feasible sets, infimum/minimum, and tie contracts;
- backtracking coverage, pruning, restoration, and finite-tree termination;
- greedy feasible constructions, relaxations, linear programming, and matchings at an introductory level;
- priority queues, depth-first stacks, best-first search, and stale entries;
- fixed-width integer overflow, floating-point rounding, rational and interval arithmetic;
- concurrency, cancellation, snapshots, task ownership, and distributed termination;
- asymptotic and measured cost, output certificates, and exhaustive small-instance oracles.

You should be able to prove why a number is optimistic before comparing it with an incumbent.

## Learning Objectives

After completing this module, you should be able to:

1. orient incumbent and node bounds correctly for minimization and maximization;
2. prove branching coverage, bound validity, prune safety, and final optimality;
3. handle equality according to one-optimum, lexicographic, or all-optima output contracts;
4. derive bounds from relaxations, combinatorial arguments, and dominance;
5. compare depth-first, breadth-first, best-bound, and hybrid node selection;
6. maintain valid global lower bounds and interruption gaps;
7. protect bounds and incumbents from overflow, rounding, infeasibility, and stale state;
8. reason about shared incumbents, frontier ownership, and distributed termination;
9. measure bound cost, pruning power, node distributions, memory, and certificate progress;
10. validate every prune and reported optimum with independent bounded evidence.

## Core Exposition

### Fix one objective direction first

This chapter uses minimization as its primary convention. Let root feasible set be $\mathcal F$ and

$$
z^*=\min_{x\in\mathcal F}f(x).
$$

A feasible solution $\hat x\in\mathcal F$ gives

$$
z^*\le f(\hat x)=U.
$$

Thus the incumbent is an **upper** bound. A node lower bound is optimistic because it may understate the best feasible descendant:

$$
L(p)\le z^*(p).
$$

For maximization, reverse the roles: a feasible incumbent is a lower bound and a node bound must be an upper bound. Write the inequalities before code; words such as “best bound” are too ambiguous by themselves.

### Define node semantics and branching coverage

A node $p$ represents a subset $\mathcal C(p)$ of root feasible solutions consistent with its decisions and propagation. Children $p_1,\ldots,p_k$ must satisfy

$$
\mathcal C(p)\subseteq
\bigcup_{i=1}^{k}\mathcal C(p_i),
$$

with equality under an exact representation. Children may overlap and still preserve optimization completeness, but overlaps create duplicate work. A true partition additionally makes them pairwise disjoint.

Integer programming may branch on fractional variable $x_j$ with value $a$ by adding $x_j\le\lfloor a\rfloor$ in one child and $x_j\ge\lceil a\rceil$ in the other. A vertex-cover search may branch on endpoints of an uncovered edge. Scheduling may split on precedence or time windows.

Branching is valid because every parent completion satisfies at least one child condition, not because the children look balanced.

### Keep primal and bound evidence separate

The **primal** side contains complete feasible solutions. Only a full feasibility check may install an incumbent. A greedy construction, local search, repair heuristic, or rounded relaxation can propose a candidate; it becomes $U$ only after validation against the original model.

The **bound** side proves limitations on subproblems. A relaxation optimum, matching argument, remaining-cost estimate, or dual certificate may produce $L(p)$. It need not itself be feasible for the original problem.

An infeasible candidate cannot bound $z^*$ from above. A relaxation value cannot be returned as a feasible objective. Maintaining distinct types such as `FeasibleSolution` and `NodeLowerBound` prevents accidental substitution.

### Prove the fundamental prune

Assume $L(p)\le z^*(p)$ and a feasible incumbent value $U$. If

$$
L(p)\ge U,
$$

then every $x\in\mathcal C(p)$ satisfies

$$
f(x)\ge z^*(p)\ge L(p)\ge U.
$$

No descendant has a strictly smaller objective. The node may be fathomed when the contract asks for one optimal objective and an already retained witness.

The chain exposes every premise: feasible incumbent, lower-bound direction, matching objective units, safe arithmetic, and strict-improvement output semantics.

### Handle equality according to the output contract

If $L(p)=U$, the node cannot improve the primary objective but may contain:

- another optimal witness required by all-optima enumeration;
- an equal-primary witness with a better secondary lexicographic, fairness, risk, or stability objective;
- a proof or explanation required by the API.

For all primary optima, prune only when $L(p)>U$ unless another argument counts or reconstructs equal solutions. For lexicographic optimization, bound the full ordered objective tuple conservatively. For one arbitrary optimum, $L(p)\ge U$ is sufficient.

Document whether “deterministic” means stable first-found witness or lexicographically minimum witness. They are not the same.

### Derive bounds by relaxing constraints

For minimization node $p$, let relaxed feasible set $\mathcal R(p)$ contain the original descendants:

$$
\mathcal C(p)\subseteq\mathcal R(p).
$$

Then

$$
\min_{x\in\mathcal R(p)}f(x)
\le
\min_{x\in\mathcal C(p)}f(x)
=z^*(p).
$$

The relaxed optimum is a valid lower bound. Linear-programming relaxations drop integrality; assignment relaxations may drop subtour constraints; scheduling relaxations may ignore resource conflicts.

For maximization, enlarging the feasible set makes the relaxed maximum at least the original maximum, giving a node upper bound. Direction follows from set inclusion and objective direction, not memorized terminology.

### Build combinatorial bounds directly

Not every useful bound requires a general optimizer. Examples include:

- a matching-size lower bound for minimum vertex cover;
- sum of mandatory remaining processing times for scheduling makespan;
- minimum outgoing-edge contributions for a tour;
- fractional-knapsack upper bound for 0/1 knapsack maximization;
- conflict-clique lower bounds for coloring;
- remaining independent component optima when decomposition is exact.

Each bound needs a lemma mapping its counted or relaxed objects to every completion. A greedy matching is not necessarily maximum, but its disjoint edges still form a valid vertex-cover lower bound; weakness affects pruning, not correctness.

### Balance bound strength against evaluation cost

If bound $L_2(p)\ge L_1(p)$ for all minimization nodes, $L_2$ is at least as tight. It may still be slower overall. Total work is roughly

$$
\sum_{p\in V}
\left(
c_{\mathrm{propagate}}(p)+c_{\mathrm{bound}}(p)
+c_{\mathrm{branch}}(p)+c_{\mathrm{queue}}(p)
\right).
$$

A costly relaxation can pay for itself near the root where pruning removes enormous subtrees and lose near leaves where only a few decisions remain. Layered solvers run a cheap bound first and invoke an expensive one only if the node survives and expected savings justify it.

Measure bound time, bound improvement over a baseline, nodes pruned uniquely by each bound, depth, relaxation iterations, and downstream subtree size.

### Construct good incumbents safely

A small minimization incumbent makes more lower bounds competitive. Run a deterministic greedy construction, repair a relaxed solution, complete promising partial nodes, or seed from a prior compatible instance.

Validate every candidate against original constraints, exact input revision, and numeric policy before publishing. A false incumbent that is too low makes sound lower bounds appear noncompetitive and can delete the true optimum. A merely poor but feasible incumbent preserves correctness and costs extra work.

Incumbent heuristics should have their own time budget. An elaborate primal search can delay the bound tree without improving $U$.

### Choose which live node to process

- **Depth-first** uses little frontier memory and reaches complete candidates quickly, often improving the incumbent early.
- **Breadth-first** exposes levels and parallelism but can retain an enormous frontier.
- **Best-bound** selects minimum $L(p)$, prioritizing the node most capable of improving the global lower certificate.
- **Best-estimate** uses a prediction of likely solution quality; unless conservatively bounded, it is ordering only.
- **Hybrid** strategies dive for incumbents, then return to best-bound proof progress.

With sound pruning and eventual fair processing, selection order does not change optimality. It changes time to first incumbent, time to close the gap, frontier memory, locality, and determinism.

### Maintain a valid anytime certificate

Suppose frontier $Q$ covers every not-yet-fathomed solution and $U$ is the best validated incumbent. Define

$$
\underline z=
\min\left(
U,
\min_{p\in Q}L(p)
\right).
$$

Then

$$
\underline z\le z^*\le U.
$$

Including $U$ matters when the optimum has already been found but remaining nodes have larger bounds. If $Q$ is empty and $U<+\infty$, then $\underline z=U$ and optimality is proven. If $Q$ is empty and no feasible incumbent exists, exhaustive sound search proves infeasibility.

The absolute gap

$$
g_{\mathrm{abs}}=U-\underline z
$$

is unambiguous in objective units. Relative gaps require a declared denominator and careful treatment of zeros and negative values; report both inputs rather than only a percentage.

### Preserve certificate truth under interruption

At timeout or cancellation, stop generating new work, account for every owned node, and collect a conservative frontier minimum. Return the feasible incumbent if one exists, the global lower bound, gap, input/model revision, and incomplete reason.

Do not claim the last popped node bound is global. Nodes may remain in worker deques, network leases, retry queues, or in-flight branching. A lost node breaks coverage and invalidates the certificate.

Approximate gap termination is exact with respect to the stated tolerance only when both primal and bound values are valid. It does not make the incumbent mathematically optimal unless the exact gap closes.

### Make numeric bounds conservative

For minimization, a computed lower bound that rounds upward above the true relaxed optimum can prune a better descendant. Use exact integer/rational arithmetic where practical, certified solver bounds, interval arithmetic, or directed rounding toward $-\infty$.

A blanket epsilon can avoid some false prunes but must be derived in objective units and propagated through operations. NaN must never compare as an ordinary bound. Positive/negative infinity, overflow, scaling, unit conversion, and mixed numeric types need explicit behavior.

For fixed-width integers, checked addition and multiplication are required in both feasible objectives and optimistic estimates. Saturating a minimization lower bound upward can be unsafe; a conservative failure should weaken the bound or stop with an error.

### Combine propagation, dominance, and bounds

Constraint propagation first removes infeasible values and may prove the node empty. Bound computation then estimates the best remaining objective. Dominance can remove a node $p$ if another retained node $q$ covers all relevant completions with no worse cost and compatible future state.

Dominance needs a state-sufficiency proof. Comparing only current cost can be wrong when nodes differ in capacity, endpoint, ordering, risk, or future constraints. Transposition tables must retain the best prefix information required by the bound and output contract.

Record whether a node was rejected by infeasibility, dominance, or objective bound; these are different certificates.

### Use branching to improve future bounds

Branching chooses not only tree balance but relaxation effect. A decision that removes a major fractional ambiguity or constraint violation can strengthen child bounds. Strong branching tentatively evaluates several candidates and chooses one predicted to improve the tree, at extra cost.

Branching rules remain coverage obligations. Learned or historical scores may choose among valid partitions, but they may not invent a child omission. Deterministic tie keys help reproduce node trees and debug changed performance.

### Preserve executable primal-bound correspondence

The following minimum-vertex-cover solver uses a deterministic feasible heuristic for $U$, a greedy matching lower bound, and endpoint branching. It prunes equality because its contract returns one stable optimal witness, not the lexicographically smallest or every optimum.

<!-- bijux-verify: {"id":"vertex-cover-branch-and-bound","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"graph vertices=8 edges=10\ninitial=(0, 2, 3, 5, 6) size=5\nreturned=(0, 2, 3, 5, 6) size=5\nlexicographic_optimum=(0, 1, 3, 5, 6) size=5\nnodes=11 bounds=11 pruned=6 improvements=0\nfeasible=True objective_matches=True\n","stderr":""}} -->
~~~python
from itertools import combinations


vertices = tuple(range(8))
edges = (
    (0, 1),
    (0, 2),
    (1, 2),
    (2, 3),
    (3, 4),
    (3, 5),
    (4, 5),
    (5, 6),
    (5, 7),
    (6, 7),
)


def is_cover(candidate):
    chosen = set(candidate)
    return all(left in chosen or right in chosen for left, right in edges)


def greedy_cover(uncovered):
    remaining = list(uncovered)
    chosen = set()
    while remaining:
        degrees = {vertex: 0 for edge in remaining for vertex in edge}
        for left, right in remaining:
            degrees[left] += 1
            degrees[right] += 1
        vertex = min(degrees, key=lambda item: (-degrees[item], item))
        chosen.add(vertex)
        remaining = [edge for edge in remaining if vertex not in edge]
    return tuple(sorted(chosen))


def matching_size(uncovered):
    used = set()
    size = 0
    for left, right in uncovered:
        if left not in used and right not in used:
            used.update((left, right))
            size += 1
    return size


def solve():
    initial = greedy_cover(edges)
    if not is_cover(initial):
        raise AssertionError("incumbent heuristic returned an infeasible cover")
    best = initial
    nodes = 0
    bounds = 0
    pruned = 0
    improvements = 0

    def visit(chosen, uncovered):
        nonlocal best, bounds, improvements, nodes, pruned
        nodes += 1
        bounds += 1
        lower_bound = len(chosen) + matching_size(uncovered)
        if lower_bound >= len(best):
            pruned += 1
            return
        if not uncovered:
            candidate = tuple(sorted(chosen))
            if len(candidate) < len(best):
                best = candidate
                improvements += 1
            return

        degrees = {vertex: 0 for edge in uncovered for vertex in edge}
        for left, right in uncovered:
            degrees[left] += 1
            degrees[right] += 1
        edge = min(
            uncovered,
            key=lambda item: (-(degrees[item[0]] + degrees[item[1]]), item),
        )
        for vertex in edge:
            visit(
                chosen | {vertex},
                tuple(candidate for candidate in uncovered if vertex not in candidate),
            )

    visit(frozenset(), edges)
    return initial, best, nodes, bounds, pruned, improvements


def brute_force():
    return min(
        (len(candidate), candidate)
        for size in range(len(vertices) + 1)
        for candidate in combinations(vertices, size)
        if is_cover(candidate)
    )[1]


initial, result, nodes, bounds, pruned, improvements = solve()
lexicographic = brute_force()
print(f"graph vertices={len(vertices)} edges={len(edges)}")
print(f"initial={initial} size={len(initial)}")
print(f"returned={result} size={len(result)}")
print(f"lexicographic_optimum={lexicographic} size={len(lexicographic)}")
print(f"nodes={nodes} bounds={bounds} pruned={pruned} improvements={improvements}")
print(f"feasible={is_cover(result)} objective_matches={len(result) == len(lexicographic)}")
~~~

**Reasoning:** Four disjoint uncovered edges give the root lower bound 4, while the validated greedy cover gives upper bound 5. Eleven nodes certify that no cover of size below 5 exists. Equality pruning retains the stable heuristic witness and deliberately skips the lexicographically smaller size-5 cover.

**Conclusion:** The run demonstrates one finite bound/prune certificate and an equality-contract consequence. It does not prove the solver's result or performance for arbitrary graphs.

### Coordinate parallel incumbents and frontiers

Parallel workers can explore disjoint or merely covering node sets. A newly validated smaller $U$ may prune nodes elsewhere. Workers using a stale larger incumbent do extra work but do not lose the optimum. A falsely smaller or infeasible incumbent is unsafe because it can trigger invalid pruning.

Incumbent publication needs candidate validation, objective recomputation, input revision, and atomic comparison. Frontier ownership needs durable identities: queued, leased, active, completed, retried, and lost nodes must be distinguishable. Global termination requires no live, queued, leased, or recoverable node anywhere—not an empty local queue.

For an interrupted global bound, include conservative bounds from every live or in-flight node. If a worker disappears and its node cannot be recovered, the system has lost coverage and may report only an incomplete result without the former certificate.

### Separate search predictions from prune certificates

Historical statistics or learned models may predict which node, branch, relaxation, or heuristic will work well. Use them to order valid choices, allocate bounded effort, or select among independently correct mechanisms.

A predicted objective is not a safe node bound unless wrapped in a proven conservative envelope. Distributional accuracy, calibration, or zero training errors do not establish the universal inequality required for pruning.

Version features and models, bound their inference cost, preserve a deterministic fallback, and compare proof progress as well as runtime. Adversarial or shifted inputs can reverse learned rankings without affecting correctness when predictions control order only.

### Engineer the node representation

A node may store explicit decisions, a parent plus delta, a copied relaxation, or a reversible trail checkpoint. Include objective prefix, constraint state, bound value and provenance, branching metadata, input/model revision, and deterministic identity.

Priority queues often keep stale bound entries after strengthening, incumbent changes, or node updates. A stale **weaker** lower bound can delay work safely; using a stale **stronger** number not valid for the current node can prune incorrectly. Revalidate version and bound before fathoming.

Serialization must preserve numeric type and direction. A decimal string parsed into binary floating point or a missing infinity tag can change comparisons across workers.

### Validate bounds against descendant optima

For bounded instances, enumerate every completion below every generated node and recompute

$$
z^*(p)=\min_{x\in\mathcal C(p)}f(x).
$$

Assert $L(p)\le z^*(p)$, including infeasible nodes where $z^*(p)=+\infty$. Also compare the solver's incumbent with independent full enumeration and replay its witness.

Metamorphic checks can weaken a relaxation and require its minimization lower bound not to increase, improve a feasible incumbent and require no extra node to survive incumbent pruning, or permute stable input identities and map witnesses back.

Inject overflow, NaN, upward rounding, infeasible heuristic candidates, stale incumbent messages, duplicate/lost node delivery, cancellation, and worker failure. The solver must fail closed as incomplete rather than manufacture optimality.

### Measure proof progress, not only elapsed time

Useful structural evidence includes:

- nodes generated, processed, branched, and fathomed by reason;
- incumbent value and timestamped improvement sequence;
- global lower bound and gap sequence;
- bound cost, distribution, and incremental improvement;
- relaxation failures and numeric fallbacks;
- frontier size, peak bytes, depth, queue waits, and stale entries;
- propagation reductions and dominance hits;
- duplicate/retried/lost worker nodes;
- final feasibility replay and certificate status.

Benchmark with identical stopping conditions. Comparing one solver at optimality with another at a fixed time without reporting gaps answers neither time-to-proof nor anytime-quality fairly.

## Definitions and Notation

- $\mathcal F$: feasible set of the root minimization problem.
- $f(x)$: objective of complete candidate $x$.
- $z^*$: global optimal objective.
- $p$: branch-and-bound node or subproblem.
- $\mathcal C(p)$: root-feasible completions represented below $p$.
- $z^*(p)$: best feasible descendant objective, or $+\infty$ if none.
- $L(p)$: valid minimization lower bound satisfying $L(p)\le z^*(p)$.
- $\hat x$: incumbent feasible witness.
- $U=f(\hat x)$: incumbent minimization upper bound.
- $Q$: live frontier whose nodes cover every not-yet-fathomed candidate.
- $\underline z$: valid global minimization lower bound.
- $g_{\mathrm{abs}}=U-\underline z$: absolute certified gap.
- **Primal heuristic:** procedure proposing feasible complete candidates.
- **Relaxation:** problem with a superset of feasible completions in minimization or maximization.
- **Fathom:** finish a node by infeasibility, exact solution, dominance, or bound.
- **Best-bound:** select smallest live $L(p)$ under the minimization convention.
- **Bound provenance:** method, assumptions, numeric representation, and revision supporting a bound.
- **Primal status:** feasibility and objective of an incumbent.
- **Dual/bound status:** certified limit on unexplored objective quality.
- **Optimality certificate:** closed primal-bound gap under complete frontier accounting.

“Upper” and “lower” always refer to the objective number, not tree position or solution quality. For minimization, a smaller feasible $U$ is better while a larger valid $L(p)$ is tighter.

## Mechanisms, Invariants, or Proof Structure

Use this branch-and-bound design and review worksheet.

1. **Objective contract.** Declare minimization/maximization, numeric units, feasibility, and tie/output mode.
2. **Node semantics.** Define exactly which complete solutions $\mathcal C(p)$ a node represents.
3. **Branch coverage.** Prove child union covers the parent and record overlap or disjointness.
4. **Incumbent type.** Install only independently validated original-model solutions.
5. **Bound direction.** State and prove $L(p)\le z^*(p)$ for minimization or its maximization dual.
6. **Bound arithmetic.** Define infinity, overflow, rounding direction, units, and failure fallback.
7. **Equality policy.** Decide whether equal optima, secondary ties, counts, or explanations remain required.
8. **Fathom proof.** Label infeasible, solved, dominant, and bound-pruned nodes separately.
9. **Node selection.** Choose depth, breadth, best-bound, estimate, or hybrid without altering coverage.
10. **Incumbent construction.** Budget primal heuristics and validate every proposed witness.
11. **State management.** Preserve decisions, relaxations, trails, bound provenance, and revisions.
12. **Global certificate.** Account for frontier, active, leased, retrying, and incumbent states.
13. **Interruption contract.** Return incumbent, global bound, gap, revision, and incomplete reason.
14. **Concurrency.** Define atomic incumbent updates, node ownership, duplicate safety, and termination.
15. **Cost evidence.** Measure bound strength/cost, fathom reasons, frontier memory, and proof progress.
16. **Independent validation.** Enumerate descendant optima, replay incumbents, and inject numeric/distributed faults.

The optimality proof composes four lemmas: branch coverage retains every root solution; sound infeasibility and dominance preserve any potentially optimal representative; valid bounds justify incumbent comparison; finite fair processing exhausts or fathoms the covered frontier. A feasible incumbent remaining after exhaustion is therefore optimal.

## Alternatives and Trade-Offs

- **Weak cheap versus strong expensive bound:** weak bounds visit more nodes; strong relaxations may dominate per-node cost.
- **Depth-first versus best-bound:** depth-first limits frontier and finds incumbents; best-bound often improves the global certificate sooner.
- **Static versus strong branching:** static choices are cheap and reproducible; tentative solves may create much tighter children.
- **Feasible heuristic versus proof search:** primal work improves $U$; bound work improves $\underline z$; workloads need both in proportion.
- **Exact versus floating bounds:** exact arithmetic simplifies pruning proof; floating relaxations can be faster but require conservative certification.
- **One optimum versus lexicographic/all optima:** equality pruning is powerful for one value; richer output must preserve equal-bound nodes.
- **Full node copies versus deltas/trails:** copies isolate workers; deltas save memory but complicate restoration and serialization.
- **Central versus distributed frontier:** central order simplifies global bounds; distribution scales work but complicates ownership and termination.
- **Eager versus layered bounds:** eager strong bounds prune early; layered evaluation avoids expensive work on easy nodes.
- **Recompute versus cache relaxations:** reuse saves solves; cached bounds need complete node and model identity.
- **Deterministic versus adaptive policies:** deterministic trees reproduce failures; adaptive policies can reduce work but need versioned evidence.
- **Exact completion versus gap stop:** full exhaustion proves optimality; a certified tolerance can meet latency needs while remaining explicitly approximate.
- **Branch and bound versus dynamic programming:** B&B searches subproblem regions using global incumbents; DP computes reusable exact state values.
- **Branch and bound versus heuristic search:** heuristic search may share admissible-bound ideas; B&B explicitly maintains feasible incumbents and global optimization gaps.

## Failure Modes and Misconceptions

1. **Direction reversal:** a minimization heuristic objective is called a lower bound.
2. **Infeasible incumbent:** an unvalidated candidate supplies an unsafe $U$.
3. **Wrong relaxation inclusion:** the relaxed set excludes original completions.
4. **Bound assumption drift:** signs, capacities, graph structure, or policy version differ from the proof.
5. **Equality loss:** $L(p)\ge U$ prunes required equal-primary witnesses.
6. **Tie-blind tuple:** primary objective is bounded but secondary objective is not.
7. **Unit mismatch:** cents, dollars, time units, or scaled relaxation values are compared directly.
8. **Overflowed objective:** feasible or bound arithmetic wraps across the incumbent.
9. **Upward lower-bound rounding:** a true improving minimization node appears noncompetitive.
10. **NaN comparison:** unordered numeric data silently bypasses or triggers a prune.
11. **Infinite sentinel arithmetic:** adding to a sentinel creates a finite winning number.
12. **Heuristic as certificate:** a learned or greedy estimate directly deletes nodes.
13. **Weak-bound mythology:** validity is confused with tightness or practical benefit.
14. **Overpriced bound:** relaxation time exceeds the subtree work it saves.
15. **Unvalidated warm start:** an incumbent belongs to a different input or model revision.
16. **Lost branch:** children fail to cover every parent completion.
17. **Duplicate overlap:** overlapping branches multiply work without detection.
18. **Stale strong bound:** a queue entry from incompatible node state triggers fathoming.
19. **Local bound reported global:** other queues or in-flight nodes have smaller bounds.
20. **Empty local queue means done:** distributed work remains leased or retryable.
21. **Lost-node certificate:** worker failure removes a subproblem from frontier coverage.
22. **Stale high incumbent panic:** safe extra work is mistaken for incorrectness.
23. **False low incumbent:** corrupted publication prunes the actual optimum.
24. **Gap denominator ambiguity:** relative percentages hide zero or negative objectives.
25. **Timeout optimality:** an incumbent is returned without incomplete status or remaining bound.
26. **No-incumbent infeasibility:** failure to find a solution under a budget is called infeasible.
27. **Unfair scheduling:** some live nodes are starved, so finite completion assumptions fail.
28. **Nondeterministic tie tree:** unstable priority iteration prevents reproduction.
29. **Unbounded frontier:** best-first search exhausts memory before proof.
30. **Final-number-only testing:** bound violations and missing nodes happen to yield the right sample optimum.

## Worked Examples

### Example 1

**Question:** In minimization, is a feasible value 30 a lower or upper bound on an unknown optimum?

**Reasoning:** The optimum is no greater than every feasible objective, so $z^*\le30$. The candidate may be far worse than optimum but still limits it from above.

**Conclusion:** Feasible minimization incumbents are upper bounds; optimistic node relaxations are lower bounds.

### Example 2

**Question:** May a node with $L(p)=U=12$ be pruned?

**Reasoning:** It contains no solution with objective below 12. It may contain other objective-12 witnesses. Pruning is sound for one arbitrary optimum but not for all optima or an unbounded secondary tie objective.

**Conclusion:** The comparison operator belongs to the output contract.

### Example 3

**Question:** Why is a fast incumbent candidate dangerous before feasibility replay?

**Reasoning:** Suppose its reported cost is 90 but it violates one constraint, while the true optimum is 100. Treating 90 as $U$ can prune every node whose valid lower bound is at least 90, including the optimum.

**Conclusion:** Candidate construction and incumbent publication are separate operations.

### Example 4

**Question:** Why does dropping integrality give a minimization lower bound?

**Reasoning:** Every integer-feasible point remains feasible in the enlarged continuous set. Minimizing over more points cannot raise the optimum.

**Conclusion:** Relaxation direction follows from feasible-set inclusion.

### Example 5

**Question:** Why do four vertex-disjoint uncovered edges imply four more cover vertices?

**Reasoning:** No one vertex is incident to two edges in the matching. Each edge requires at least one endpoint, and the four chosen endpoints must therefore be distinct.

**Conclusion:** Matching cardinality is a valid cover lower bound even when the matching is merely greedy and weak.

### Example 6

**Question:** What bound does fractional knapsack provide for 0/1 knapsack maximization?

**Reasoning:** Allowing fractions enlarges the maximization feasible set, so its density-ordered fractional value is at least the best remaining integral value. Adding fixed selected value yields a node upper bound.

**Conclusion:** The same relaxation reverses bound direction when the objective reverses.

### Example 7

**Question:** An incumbent is 17 and live lower bounds are 12, 15, and 14. What is certified?

**Reasoning:** The global lower bound is $\min(17,12,15,14)=12$. Therefore $12\le z^*\le17$ and the absolute gap is 5.

**Conclusion:** The best frontier bound limits undiscovered improvement; it is not itself a feasible solution.

### Example 8

**Question:** Can rounding a true node lower bound 10.0004 to 10.01 be unsafe with incumbent 10.005?

**Reasoning:** The rounded number exceeds the true lower bound. Comparing 10.01 to 10.005 prunes, although a descendant objective between 10.0004 and 10.005 may improve the incumbent.

**Conclusion:** Minimization lower bounds must round conservatively downward or carry certified error intervals.

### Example 9

**Question:** What happens when a worker still uses old feasible incumbent 120 after another publishes 100?

**Reasoning:** It fails to prune nodes with bounds between 100 and 120, doing extra work. Because 120 is feasible and weaker, it does not delete a candidate that the valid 100 incumbent would retain.

**Conclusion:** A stale high minimization incumbent costs work; a false low incumbent threatens correctness.

### Example 10

**Question:** Is a bound that cuts nodes by 40 times worthwhile if it costs 50 times more per node?

**Reasoning:** Not necessarily. Include base node work, depth distribution, unique prunes, and downstream subtree sizes. A layered policy may apply it near the root and skip it near leaves.

**Conclusion:** Bound strength and total solver cost are different metrics.

## Cross-Program Connections

- [Theory of Computation & Complexity](../../15-theory-of-computation-and-complexity/ROADMAP.md) owns NP optimization, reductions, lower bounds, and certificate complexity.
- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) owns priority queues, persistent nodes, trails, matchings, transposition tables, and compact frontier representation.
- [Database Engineering](../../18-database-engineering/ROADMAP.md) owns cost-based plan search, property-aware dominance, cardinality estimates, and plan-cache identity.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) owns leases, retries, duplicate work, global termination, failure recovery, and consistent incumbent publication.
- [Computer Architecture](../../23-computer-architecture/ROADMAP.md) owns relaxation kernels, locality, vectorization, numeric throughput, and frontier memory behavior.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) owns adversarial instances, tenant budgets, numeric attacks, sensitive candidates, and safe incomplete status.
- [Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) owns descendant oracles, metamorphic bound checks, fault injection, benchmark design, and certificate regression.

## References

1. Ailsa H. Land and Alison G. Doig. [“An Automatic Method of Solving Discrete Programming Problems”](https://doi.org/10.2307/1910129), *Econometrica* 28(3), 1960, pp. 497–520. Primary discrete-programming branch-and-bound work.
2. John D. C. Little, Katta G. Murty, Dura W. Sweeney, and Caroline Karel. [“An Algorithm for the Traveling Salesman Problem”](https://doi.org/10.1287/opre.11.6.972), *Operations Research* 11(6), 1963, pp. 972–989. Primary named branch-and-bound TSP formulation.
3. Eugene L. Lawler and David E. Wood. [“Branch-and-Bound Methods: A Survey”](https://doi.org/10.1287/opre.14.4.699), *Operations Research* 14(4), 1966, pp. 699–719. Classical framework, applications, and computation/storage trade-offs.
4. Peter E. Hart, Nils J. Nilsson, and Bertram Raphael. [“A Formal Basis for the Heuristic Determination of Minimum Cost Paths”](https://doi.org/10.1109/TSSC.1968.300136), *IEEE Transactions on Systems Science and Cybernetics* 4(2), 1968, pp. 100–107. Admissible bounds and best-first search foundations.
5. George L. Nemhauser and Laurence A. Wolsey. [*Integer and Combinatorial Optimization*](https://doi.org/10.1002/9781118627372), Wiley, 1988. Authoritative relaxations, valid inequalities, and integer optimization reference.
6. Laurence A. Wolsey. [*Integer Programming*, second edition](https://doi.org/10.1002/9781119606475), Wiley, 2020. Modern presolve, primal heuristics, formulations, and exact-solver practice.
7. David Goldberg. [“What Every Computer Scientist Should Know About Floating-Point Arithmetic”](https://doi.org/10.1145/103162.103163), *ACM Computing Surveys* 23(1), 1991, pp. 5–48. Floating-point representation and rounding foundations.
8. ACM, IEEE Computer Society, and AAAI. [*Computer Science Curricula 2023: Algorithmic Foundations*](https://csed.acm.org/algorithms-and-complexity/), endorsed 2024; consulted 2026-09-04. Current curricular scope for search, optimization, correctness, and evaluation.

## Exercises

### Exercise 1

Trace best-bound minimization from incumbent $U=15$. Root children are $A$ with lower bound 9, $B$ with lower bound 11, and infeasible $C$. Expanding $A$ yields complete $A_1$ of value 13 and node $A_2$ of lower bound 14. Expanding $B$ yields complete $B_1$ of value 12 and node $B_2$ of lower bound 12. The contract needs one optimum. Give processing, incumbent, pruning, frontier-bound, and final-certificate steps.

### Exercise 2

Prove that any matching in an uncovered graph supplies a lower bound for minimum vertex cover below a node with already selected set $S$. Explain why branching on endpoints of one uncovered edge covers all completions, why a greedy nonmaximum matching remains valid, and how `>=` versus `>` changes the witness contract.

### Exercise 3

Diagnose three defects: a minimization relaxation lower bound is rounded upward; a distributed worker publishes a low objective before original-model feasibility replay; and one node is declared dominant solely because its prefix cost is smaller although it has less remaining capacity. Give counterexamples, repairs, and targeted tests.

### Exercise 4

A weak bound costs 1 unit per node and leaves 100,000 processed nodes. A strong bound costs 40 units per node and leaves 2,500 processed nodes. Common propagation, branching, and queue work costs 5 units per processed node. Compute modeled totals and speedup, then list evidence omitted by this aggregate comparison and design a layered policy.

### Exercise 5

Design branch and bound for assigning nonpreemptive jobs with integer processing times to identical machines while minimizing makespan. Specify nodes, coverage, a feasible incumbent, at least three valid lower-bound terms, equality/tie semantics, symmetry, node order, checked arithmetic, interruption certificate, parallel ownership, telemetry, exhaustive tests, and rollout evidence.

## Answers to the Exercises

### Answer 1

Initially discard $C$ by its infeasibility proof. The frontier is $A(9),B(11)$, so the global lower bound is

$$
\underline z=\min\{15,9,11\}=9.
$$

Best-bound selects $A$. Complete $A_1$ is feasible with value 13, so validate it and set $U=13$. Node $A_2$ has $L=14\ge13$ and is pruned. The remaining frontier is $B(11)$, giving $11\le z^*\le13$.

Expand $B$. Complete $B_1$ validates at 12, so set $U=12$. Node $B_2$ has $L=12$. Because one optimum suffices, equality cannot improve the primary objective and $B_2$ is pruned.

The frontier is empty. With the empty-frontier minimum treated as $+\infty$,

$$
\underline z=\min\{U,+\infty\}=12.
$$

Thus $12\le z^*\le12$ and the $B_1$ witness is optimal. If all objective-12 witnesses or a better secondary tie were required, $B_2$ could not be discarded from its scalar equality alone.

### Answer 2

Let $M$ be any set of pairwise vertex-disjoint uncovered edges. Every completion vertex cover must contain at least one endpoint of each edge in $M$. Because the matching edges share no vertices, those choices require at least $|M|$ distinct additional vertices. Therefore

$$
L(p)=|S|+|M|\le z^*(p).
$$

Maximum matching would give the strongest bound of this form, but every greedy matching is still a matching. Smaller $|M|$ weakens pruning without reversing the inequality.

For uncovered edge $(u,v)$, every cover contains $u$ or $v$, so children selecting $u$ and selecting $v$ cover the parent. Covers containing both may appear below both children unless an exclusion condition makes the branches disjoint; overlap affects work, not one-optimum completeness.

With a validated incumbent size $U$, pruning at $L\ge U$ preserves one incumbent of optimal cardinality but may remove other size-$U$ covers and a lexicographically smaller one. Use $L>U$ for all primary optima, or add conservative secondary-objective bounds before equality pruning.

### Answer 3

For upward rounding, let the true node lower bound be 10.0004, the stored rounded value 10.01, and incumbent 10.005. The stored comparison prunes although a descendant at 10.003 would improve $U$. Use exact/rational computation, a certified interval's lower endpoint, or directed rounding toward $-\infty$. Test values bracketing every rounding boundary and exhaust descendants to assert stored $L(p)\le z^*(p)$.

For the premature incumbent, suppose a candidate reports 90 but violates a constraint while the true optimum is 100. Publishing $U=90$ can prune all valid nodes with lower bounds at least 90. Validate original constraints, recompute objective with checked arithmetic, and bind input/model revision before atomic publication. Inject invalid warm starts, stale revisions, overflow, and worker races; assert none changes the incumbent.

For dominance, node $p$ may cost 5 with no remaining capacity while node $q$ costs 6 with capacity 10; only $q$ may admit a cheap completion. Prefix cost alone does not establish coverage of future states. Compare every future-relevant resource, endpoint, property, and constraint, or omit the dominance prune. Enumerate bounded descendant sets and require every completion represented by the deleted node to have a no-worse retained counterpart.

### Answer 4

Weak-bound modeled work is

$$
100{,}000(5+1)=600{,}000
$$

units. Strong-bound work is

$$
2{,}500(5+40)=112{,}500
$$

units. The modeled speedup is

$$
\frac{600{,}000}{112{,}500}=\frac{16}{3}\approx5.33.
$$

This aggregate omits depth-dependent bound cost, nodes generated but not processed, relaxation setup/reuse, incumbent timing, frontier memory, cache locality, parallelism, numeric fallback, bound failures, distribution tails, and whether the strong bound uniquely caused each prune.

A layered policy computes the weak bound first. If it already meets $U$, prune without paying 40 units. Otherwise run the strong bound near high-subtree-potential depths or when a validated model predicts enough saved descendants; predictions only select the bound, never prune directly. Version the threshold, cap strong-bound time, fall back conservatively, and compare held-out total work and certificate progress.

### Answer 5

A node assigns a prefix of jobs to machine identities and stores checked machine loads plus remaining jobs. Sort jobs initially by descending processing time with stable job-identity ties. Branch by assigning the next job to each machine load state not removed by proven symmetry. Children cover every labeled schedule; canonical equal-load representatives preserve at least one schedule per machine-permutation orbit.

A deterministic list-scheduling completion supplies a feasible makespan $U$: assign each remaining job to the currently least-loaded machine with stable machine ties, then validate every job appears once and recompute loads.

For node loads $\ell_1,\ldots,\ell_m$, remaining processing sum $R$, and largest remaining job $p_{\max}$, valid lower-bound terms include

$$
L_1=\max_i\ell_i,
$$

$$
L_2=\left\lceil\frac{\sum_i\ell_i+R}{m}\right\rceil,
$$

and, when work is nonnegative,

$$
L_3=\min_i\ell_i+p_{\max}.
$$

Every completion retains current loads, distributes total work over $m$ machines, and must place the largest remaining job on a machine whose present load is at least the minimum. Thus $L=\max(L_1,L_2,L_3)$ is valid. An exact relaxation or subset packing bound may strengthen it.

If only one deterministic optimum is required, `L >= U` may prune and the stable traversal defines the returned witness. For lexicographically smallest labeled assignment or all schedules, scalar equality is insufficient. Machine-load symmetry is safe for objective value because permuting equal-load identical machines preserves feasible makespan, but labeled-output reconstruction must map or enumerate the orbit explicitly.

Use depth-first dives for early feasible schedules and a best-bound frontier for proof progress, or a governed hybrid. Compute sums and ceiling division with widened checked integers; reject negative durations, invalid machine counts, overflow, and impossible allocations. Never use floating division for an exact integer lower bound.

At interruption return validated schedule and $U$, global $\underline z$ from every queued/active/leased node, absolute gap, model revision, and incomplete reason. Parallel workers own immutable node IDs and private state, publish incumbents only after replay, renew/recover leases, tolerate duplicate exploration, and establish global termination only after all ownership states close.

Record nodes, depth, branches, equal-load symmetry skips, incumbent timeline, each lower-bound term, fathom reasons, frontier/lease counts, peak bytes, checked-arithmetic failures, global gap, retries, duplicates, cancellations, and witness replay.

For small job multisets and machine counts, enumerate all $m^n$ assignments independently, compare optimum and required tie witness, and check $L(p)\le z^*(p)$ at every generated node. Include zero durations, one machine, more machines than jobs, equal jobs/loads, overflow boundaries, adversarial imbalance, interruption at every node, duplicate/lost worker messages, and stale incumbents. Shadow an established exact solver on immutable workloads, require zero certificate or feasibility mismatches and enforced resource ceilings, then canary with deterministic rollback.
