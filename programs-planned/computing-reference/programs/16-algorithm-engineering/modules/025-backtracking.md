---
module_id: ALGE-025
program: Algorithm Engineering
level: 1
module_number: 25
title: Backtracking
status: complete
last_verified: 2026-09-04
---

# Backtracking

## One-Page Review

### Governing question

How can an exact algorithm traverse a candidate tree, reject partial choices only when no required completion remains, and restore state so every valid solution is found once under a clear resource contract?

### Essential definitions

- A **partial candidate** records choices made at one search-tree node.
- An **extension** adds one legal next choice and descends to a child.
- A **completion** extends a partial candidate to a full candidate.
- A **feasible solution** is a complete candidate satisfying every declared constraint.
- A **prune predicate** rejects a node without visiting its descendants.
- **Sound pruning** means every pruned node has no required feasible completion.
- **Constraint propagation** removes values that cannot participate under current assignments; failure of a domain proves a dead end.
- **Variable ordering** chooses what to assign next; **value ordering** chooses the child visitation order.
- A **trail** records reversible mutations so they can be undone on return.
- **Search completeness** means every required solution is reached unless the API explicitly returns an incomplete status.

### Central model, mechanism, or theorem

Let $p$ be a partial candidate, $\mathcal C(p)$ its target completions, $X(p)$ a finite ordered set of extensions, and $p\oplus x$ the child after choice $x$. Require:

1. every target completion of $p$ belongs to at least one child completion set;
2. child sets are disjoint when duplicate-free enumeration is promised;
3. prune predicate $P$ satisfies

$$
P(p)\Longrightarrow\mathcal C(p)=\varnothing;
$$

4. every extension increases a bounded progress rank;
5. applying then undoing a choice restores all search-visible state.

The algorithm rejects when $P(p)$ holds, emits an accepted complete candidate, and otherwise explores every $x\in X(p)$. Soundness follows from the acceptance test. Completeness follows by tracing each solution through the exhaustive child partition; sound pruning never cuts its path. Termination follows from finite branching and bounded strict progress.

If $V$ is the set of visited partial candidates, work is more accurately expressed as

$$
\Theta\left(
\sum_{p\in V}
\left(
c_{\mathrm{check}}(p)+c_{\mathrm{choose}}(p)
+c_{\mathrm{apply}}(p)+c_{\mathrm{undo}}(p)
\right)
\right),
$$

plus propagation, output, allocation, and restoration validation. A full $b$-ary tree of depth $d$ has $(b^{d+1}-1)/(b-1)$ nodes for $b>1$; pruning changes visited nodes, not the worst-case guarantee without a theorem.

### Critical invariants

- The partial candidate represents exactly the choices on the active root-to-node path.
- Every active constraint index, domain, count, mask, and accumulated value agrees with that path.
- Child generation covers every legal next choice required by the output mode.
- A prune has a proof of empty target-completion set, not merely a poor score.
- Apply and undo are inverse over every search-visible field, including caches and indexes.
- Complete candidates are independently validated before emission or acceptance.
- Equal domain values and symmetries are removed only by a duplicate/orbit proof.
- Variable and value heuristics reorder exhaustive work without silently deleting choices.
- Cancellation, timeout, or node budget returns `incomplete`, never `unsatisfiable`.
- Counts, output volume, depth, memory, and adversarial branching have explicit bounds.

### Common failures

Common failures include accepting a partial candidate; pruning from a condition that is only usually bad; assuming current sum above target is hopeless when negative values remain; mutating shared state without undoing every field; yielding an alias to a mutable buffer; generating the same multiset permutation repeatedly; calling a value-ordering heuristic a proof; confusing local consistency with global satisfiability; applying a symmetry rule without orbit coverage; counting solutions after symmetry reduction without stabilizer reasoning; overflowing solution counts; interpreting timeout as absence; hiding exponential work behind recursion; storing all solutions when streaming suffices; and mixing objective-bound pruning into backtracking without the branch-and-bound proof developed in ALGE-026.

### Compact example

For $n$-queens, process rows in order. A partial tuple $(c_0,\ldots,c_{r-1})$ places one queen in each earlier row. A column $c$ is legal for row $r$ exactly when no earlier queen shares its column or diagonal:

$$
c\ne c_i
\quad\text{and}\quad
|c-c_i|\ne r-i
\qquad(0\le i<r).
$$

The two solutions for $n=4$ are $(1,3,0,2)$ and $(2,0,3,1)$. Column and diagonal masks reject conflicts before descent. Ordered columns make output deterministic; push followed by pop restores the active placement.

### Connections

[ALGE-004](./004-inductive-correctness-proofs.md) supplies correctness induction, [ALGE-023](./023-dynamic-programming-state-design.md) explains when histories can merge, [ALGE-024](./024-memoization-and-bottom-up-evaluation.md) evaluates repeated states, and [ALGE-026](../ROADMAP.md) adds admissible objective bounds and incumbents.

## Governing Question

Which partial choices should an exact search extend, which may it reject without losing a required solution, and how does it guarantee faithful restoration across every alternative?

Backtracking converts a declarative “choose values satisfying constraints” problem into a finite search tree. It makes one choice, updates incremental state, explores the consequences, reverses that update, and tries the next choice. The method is simple only when its proof obligations are made explicit.

The central distinction is between **ordering** and **pruning**. An ordering heuristic changes which branch is tried first. Exhaustive traversal remains complete even if the heuristic is poor. A prune deletes an entire descendant set and therefore needs a universal implication. Empirical success cannot replace that implication.

## Why This Matters

Backtracking underlies puzzle solvers, constraint satisfaction, exact cover, configuration, theorem proving, parsing, test generation, scheduling feasibility, and combinatorial enumeration. It is often the first exact method available when greedy choices are unsafe and overlapping subproblems do not yield a compact dynamic program.

Its risks are equally broad. Candidate trees can grow exponentially or factorially. Mutation bugs can create false solutions or omit valid ones. A duplicate generator can overwhelm output. A service can burn unbounded CPU on an adversarial instance. A timeout can be misreported as proof that no solution exists.

A production-quality solver therefore joins mathematics and mechanics: exhaustive child coverage, sound rejection, rank-based termination, reversible state, deterministic output, independent witness checking, honest status, resource governance, and structural telemetry.

## Prerequisites and Retrieval

Retrieve:

- predicates, quantifiers, sets, tuples, permutations, combinations, and graphs;
- induction, invariants, contradiction, and proof by partition;
- recursion trees, depth-first traversal, stacks, and exception-safe cleanup;
- state-space size, exponential and factorial growth, and output-sensitive bounds;
- mutable arrays, sets, bit masks, indexes, snapshots, and aliasing;
- dynamic-programming state equivalence and memoization boundaries;
- Boolean formulas, finite-domain constraints, exact cover, and graph coloring at an introductory level;
- exhaustive small-instance oracles, property testing, and witness replay.

You should be able to distinguish “this branch is visited later” from “this branch is proved irrelevant.”

## Learning Objectives

After completing this module, you should be able to:

1. model a combinatorial problem as partial candidates, extensions, acceptance, and rejection;
2. prove search soundness, completeness, uniqueness, and termination separately;
3. derive node-sensitive time, depth-sensitive space, and output lower bounds;
4. implement copy-based and reversible in-place search without state leakage;
5. design incremental checks, forward checking, and propagation with stated guarantees;
6. use variable and value ordering without mistaking heuristics for pruning proofs;
7. justify duplicate elimination and symmetry breaking by canonical representatives;
8. distinguish backtracking from dynamic programming and branch and bound;
9. expose cancellation, partial enumeration, counts, and deterministic witnesses honestly;
10. validate restoration, prune soundness, coverage, and resource behavior independently.

## Core Exposition

### Define the candidate space before writing recursion

Let a complete candidate assign variables $x_0,\ldots,x_{n-1}$ values from declared domains. A partial candidate $p$ assigns some prefix or selected subset of variables. Define:

- $\operatorname{complete}(p)$: all required variables are assigned;
- $\operatorname{accept}(p)$: a complete candidate satisfies the target predicate;
- $X(p)$: ordered next extensions;
- $p\oplus x$: child after extension $x$;
- $P(p)$: a sound dead-end predicate.

The output mode also belongs in the contract. “Find one,” “find lexicographically first,” “enumerate all,” “count,” and “optimize exhaustively” are different problems. Early return is correct for find-one but destroys all-solutions completeness. Counting can avoid materializing witnesses but needs a sufficiently wide numeric type.

### View nondeterministic choice as a deterministic tree

A high-level specification may say “choose any admissible value, then require all constraints.” A conventional machine realizes this by recording a choice point and visiting alternatives in a deterministic order.

Each root-to-leaf path represents a sequence of choices. Internal nodes represent partial candidates. Rejection stops one subtree. Backtracking returns to the most recent choice point whose alternatives remain.

This tree view separates candidate coverage from implementation syntax. Recursive calls, an explicit frame stack, coroutines, or solver continuations can realize the same ordered tree.

### Prove child coverage and uniqueness

For every noncomplete, nonpruned $p$, require

$$
\mathcal C(p)
=
\bigcup_{x\in X(p)}\mathcal C(p\oplus x).
$$

This union proves coverage. For duplicate-free enumeration, also require

$$
x\ne y
\Longrightarrow
\mathcal C(p\oplus x)\cap\mathcal C(p\oplus y)=\varnothing.
$$

Assigning one fixed variable next usually gives disjoint children because a complete assignment has exactly one value for that variable. Choosing unordered elements in arbitrary sequences may not: subset $\{a,b\}$ can arise through $a$ then $b$ or $b$ then $a$. Use increasing source indices or another canonical construction.

### Make every prune a theorem

A prune predicate must satisfy

$$
P(p)\Longrightarrow\mathcal C(p)=\varnothing.
$$

Examples include an already violated immutable constraint, duplicate selected identity, negative remaining capacity when future weights are nonnegative, or an empty variable domain after sound propagation.

The implication's assumptions matter. If current sum exceeds a target, pruning is sound when all remaining contributions are nonnegative and only additions remain. It is unsound when a remaining value may be negative. Record numeric domains beside the predicate.

“Unlikely,” “expensive,” and “low score” do not prove infeasibility. Objective-bound rejection belongs to branch and bound and needs an admissible bound plus incumbent logic.

### Separate leaf acceptance from partial consistency

Passing all constraints currently checkable does not make a partial candidate a solution. A three-coloring with half the vertices assigned may be locally consistent but incomplete.

Use partial consistency only to decide whether descent remains possible. At a leaf, validate completeness and every constraint, preferably through an independent witness checker. This defense catches missing incremental checks without weakening the search proof.

### Prove soundness, completeness, and termination

**Soundness.** The algorithm emits only after $\operatorname{complete}(p)$ and $\operatorname{accept}(p)$ succeed. Therefore every emitted candidate is a feasible solution.

**Completeness.** Fix any target solution $z$. At the root, coverage places $z$ in some child completion set. Sound pruning cannot reject a prefix of $z$. Repeating this argument follows a path to $z$, and exhaustive child traversal eventually visits it.

**Uniqueness.** If child completion sets are disjoint at every branch and emission occurs once per leaf, no solution appears twice.

**Termination.** Each extension strictly increases a bounded rank such as assigned-variable count. Every node has finitely many children. Hence every path and the entire finite tree terminate, absent an external failure.

These are separate claims. A terminating solver can be incomplete; a complete enumeration can contain duplicates; an emitted witness can be unsound even when every valid witness also appears.

### Count visited nodes rather than quoting only leaves

Let $V_k$ be visited nodes at depth $k$. Then

$$
N=\sum_{k=0}^{d}|V_k|.
$$

For constant branching $b>1$ without pruning,

$$
N=1+b+\cdots+b^d
=\frac{b^{d+1}-1}{b-1}.
$$

Permutation generation has falling branching and

$$
N=\sum_{k=0}^{n}\frac{n!}{(n-k)!},
$$

with $n!$ complete leaves before constraint pruning. Exact enumeration of $K$ witnesses of length $d$ also requires $\Omega(Kd)$ output work if all materialized representations must be written.

Report nodes entered, children considered, immediate conflicts, propagation deletions, dead domains, leaves, solutions, maximum depth, and time per node. A smaller tree with very expensive propagation can lose to a larger tree with cheap checks.

### Maintain constraints incrementally

Rechecking every constraint from scratch at depth $k$ can add a factor proportional to $k$ or problem size. Maintain summaries such as:

- used identities or columns;
- remaining capacities and counts;
- occupied diagonals;
- clause satisfaction and unassigned-literal counts;
- finite-domain supports;
- adjacency conflicts;
- prefix automaton state.

An incremental summary needs its own invariant: it equals the value obtained by recomputing from the active partial candidate. Test that equality frequently on small cases.

### Use forward checking and propagation carefully

Forward checking removes values from unassigned variables when the latest choice makes them immediately inconsistent. If any required domain becomes empty, no completion exists and pruning is sound.

Stronger propagation repeatedly applies sound local inference until a fixed point or contradiction. Arc consistency, unit propagation, and exact-cover column updates are domain-specific instances. Local consistency generally does not prove global satisfiability; a nonempty reduced domain set means only “not yet disproved.”

Propagation trades fewer search nodes for more work and restoration state at each node. Count both deletions and constraint examinations.

### Choose variables and values as performance policies

The fail-first idea chooses a variable likely to expose contradiction early—often a minimum-remaining-values variable, with a stable tie key. A value-ordering heuristic may try the least constraining value first when find-one latency matters.

These policies preserve completeness only if every remaining variable/value alternative is still explored when earlier choices fail. They can change which valid witness is first, so deterministic output contracts must version and test the ordering.

Heuristic quality is workload-dependent. Compare node distributions, not a single puzzle, and preserve hard instances rather than tuning only to averages.

### Restore mutable state exactly

Copy-based search constructs an independent child state. It is simple and locally safe but may copy large structures at every node.

In-place search mutates shared state, descends, then undoes. Its restoration invariant is:

$$
\operatorname{undo}(\operatorname{apply}(S,x),x)\equiv S
$$

for every search-visible observation: assignments, domains, counts, indexes, masks, hashes, caches, and output buffers. Equality of the main assignment array alone is insufficient.

Use structured cleanup so early success, exception, cancellation, or resource rejection still restores state. A trail stores old values or inverse operations and rewinds to a checkpoint on return.

### Avoid mutable-output aliasing

A common enumerator appends a choice to one list, yields the list, then pops. If the caller stores references, every result aliases the same buffer and later mutations corrupt prior outputs.

Emit an immutable tuple, copy the completed buffer, or document an ephemeral callback contract that forbids retention. Include identity and ordering rules in serialization so parallel or resumed enumeration remains reproducible.

### Encode n-queens conflicts with bit masks

For board width $n$, let $M=2^n-1$. At the start of a row, masks $C,L,R$ mark attacked columns from placed queens, with diagonal masks already shifted into the current row. Legal positions are

$$
A=M\mathbin{\&}\mathord{\sim}(C\mathbin{|}L\mathbin{|}R).
$$

For selected one-bit position $q$, the next-row masks are

$$
C'=C\mathbin{|}q,
$$

$$
L'=((L\mathbin{|}q)\ll1)\mathbin{\&}M,
\qquad
R'=(R\mathbin{|}q)\gg1.
$$

Mask width, shift semantics, signed complement behavior, and $n$ validation are representation obligations. Iterating the least significant available bit visits columns in increasing order.

### Preserve executable restoration evidence

The following solver counts all eight-queens placements, records the first under increasing-column order, and checks that the mutable path is empty after complete traversal.

<!-- bijux-verify: {"id":"n-queens-backtracking","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"n=8 solutions=92 nodes=2057\nfirst=(0, 4, 7, 5, 2, 6, 1, 3)\nvalid=True deterministic=True\nrestored=True\n","stderr":""}} -->
~~~python
def enumerate_queens(size):
    mask = (1 << size) - 1
    placement = []
    first = None
    solutions = 0
    nodes = 0

    def visit(row, columns, left_diagonals, right_diagonals):
        nonlocal first, solutions, nodes
        nodes += 1
        if row == size:
            witness = tuple(placement)
            solutions += 1
            if first is None:
                first = witness
            return

        available = mask & ~(columns | left_diagonals | right_diagonals)
        while available:
            position = available & -available
            available ^= position
            placement.append(position.bit_length() - 1)
            visit(
                row + 1,
                columns | position,
                ((left_diagonals | position) << 1) & mask,
                (right_diagonals | position) >> 1,
            )
            placement.pop()

    visit(0, 0, 0, 0)
    return solutions, nodes, first, tuple(placement)


def valid(witness):
    return len(set(witness)) == len(witness) and all(
        abs(witness[left] - witness[right]) != right - left
        for left in range(len(witness))
        for right in range(left + 1, len(witness))
    )


n = 8
count, visited, first_solution, final_path = enumerate_queens(n)
repeat = enumerate_queens(n)
print(f"n={n} solutions={count} nodes={visited}")
print(f"first={first_solution}")
print(f"valid={valid(first_solution)} deterministic={repeat[:3] == (count, visited, first_solution)}")
print(f"restored={final_path == () and repeat[3] == ()}")
~~~

**Reasoning:** The run visits 2,057 legal partial placements including root and 92 leaves, emits 92 labeled-board solutions, and restores the shared path after both traversals.

**Conclusion:** This is finite implementation and restoration evidence. It does not prove arbitrary-size counts, bounded integer shifts, universal performance, or safety for untrusted $n$.

### See SAT search as decide, propagate, conflict, undo

For a Boolean formula in conjunctive normal form, DPLL-style search selects an unassigned variable, tries a truth value, propagates unit clauses, and backtracks on a falsified clause. A clause with no true literal and no unassigned literal is a sound conflict certificate for the current partial assignment.

Unit propagation is forced: if every literal but one is false, the last literal must be true in any satisfying completion. Record each implied assignment and its reason on the trail. Undo all assignments and watched/index state created after the decision checkpoint.

Modern clause-learning solvers extend this model substantially. Learned clauses, nonchronological backtracking, restarts, and proof logging need their own invariants. The durable lesson here is that propagation-based rejection must preserve all models and that `unsatisfiable` requires exhausted complete search or a checkable proof—not a resource timeout.

### Model exact cover with reversible incidence state

An exact-cover solution selects rows so every primary column is covered exactly once. Algorithm X chooses a remaining column, branches over rows containing it, removes conflicting rows and covered columns, then restores them on return.

Choosing a column with few candidate rows is fail-first ordering. It changes tree shape but not the solution set. Dancing-links structures implement removal and restoration by reversible pointer updates; their speed relies on the cover/uncover operations being exact inverses.

The representation is delicate. Restore in the reverse order of removal, preserve column sizes, and never expose a structure mid-uncover. A slow independent set-based exact-cover oracle is valuable for bounded differential testing.

### Prevent duplicates by construction

When input values repeat, permuting indices can produce the same value sequence several times. Sorting values and skipping an equal unused value after an equivalent sibling has been explored creates one canonical branch per distinct value at that depth.

The condition is local to a fixed parent. A global “seen value” set would remove legitimate repetition at different positions. For combinations, advancing a start index after selection prevents reorderings of the same subset.

State the identity contract. If equal-valued objects have distinct identities that must be enumerated, value deduplication is wrong. Duplicate equivalence comes from the requested output, not visual equality alone.

### Break symmetry only with orbit coverage

A symmetry maps solutions to equivalent solutions while preserving constraints. A symmetry-breaking rule chooses representatives, such as fixing one distinguished object to a canonical position.

To preserve feasibility search, prove every solution orbit contains an allowed representative. To enumerate original labeled solutions, also reconstruct every member without duplicates. Multiplying representative counts by a constant is unsafe when some solutions have nontrivial stabilizers or an odd central case.

Symmetry breaking can transform output semantics from “all labeled solutions” to “one per equivalence class.” Name that change rather than quietly reporting the smaller count as the original problem's answer.

### Distinguish backtracking from dynamic programming

Backtracking treats different partial histories as different nodes unless explicitly canonicalized. Dynamic programming merges histories with identical future behavior and reuses their value. A transposition table can memoize a backtracking residual state, but its key must meet ALGE-023's sufficiency condition and its cached result must match the output mode.

Caching Boolean feasibility may be sound for find-one yet insufficient for enumerating witnesses, counts, or explanations. Caching “no solution below this residual state” can be useful; caching one witness may suppress other required witnesses.

If a compact state DAG exists, dynamic programming may replace exponential duplicate histories. If histories carry future-relevant distinctions or the state count remains exponential, backtracking may remain appropriate.

### Distinguish infeasibility pruning from objective bounds

Plain backtracking can enumerate every feasible candidate and retain the best. It may prune nodes whose constraints make all descendants infeasible.

Branch and bound additionally prunes a feasible partial candidate because a proven optimistic objective bound cannot beat the incumbent. That requires objective direction, incumbent semantics, bound admissibility, tie policy, and numeric safety. ALGE-026 owns that argument.

Do not call an arbitrary “current cost is too high” check backtracking pruning unless it logically proves infeasibility under a hard constraint.

### Support find-one, enumerate, and count explicitly

For find-one, stop after the first accepted candidate in the declared traversal order. Ensure cleanup still unwinds every mutation. For all-solutions enumeration, stream immutable witnesses when possible and define callback/backpressure failures.

For counting, the recurrence can add child counts instead of storing candidates. Counts may grow as $2^n$, $n!$, or faster relative to fixed-width types; use arbitrary precision or prove bounds and reject overflow.

A node or time budget changes the result type. Return a status such as `complete(count)` or `incomplete(lower_bound=count_so_far, reason=budget)`. A partial count is not the total, and no witness found yet is not an unsatisfiability proof.

### Make parallel enumeration deterministic when promised

Independent root subtrees can run concurrently. Work stealing improves utilization when subtree sizes vary, but completion order becomes scheduler-dependent.

If output order matters, assign stable subtree sequence numbers and merge ordered streams, buffering within explicit limits. If only the set matters, canonicalize and validate outputs while documenting nondeterministic arrival order. Shared global “found” flags for find-one need cancellation and restoration rules.

Parallel search can duplicate propagation state, contend on shared clauses/indexes, and amplify memory. Measure total work as well as wall time; speedup from doing more speculative nodes is not free.

### Bound adversarial resource use

Validate variable count, domain sizes, mask widths, graph size, constraint arity, recursion depth, output mode, and requested count width. Compute allocation products with checked arithmetic. Enforce per-request node, time, depth, memory, solution, and output-byte budgets.

On cancellation, restore or discard the entire solver instance. Never return a pooled mutable structure until its trail is at the root and integrity checks pass. Isolate tenants so one pathological search cannot consume shared worker or cache capacity.

Telemetry must not leak candidate secrets. Prefer aggregate nodes, depth, conflicts, domain sizes, and reason codes over raw assignments. Treat witnesses as sensitive domain data when appropriate.

### Validate coverage and restoration independently

Use several evidence layers:

1. enumerate every complete candidate for very small instances with a separate direct predicate;
2. compare solution sets or canonical multisets, not only counts;
3. at each node, recompute incremental summaries from the path;
4. snapshot state before apply and compare after undo;
5. inject exceptions, early success, cancellation, and output backpressure at every depth;
6. perturb variable/value order and require the same solution set;
7. disable each prune on small cases and verify it removes no solutions;
8. replay every emitted witness through an independent checker;
9. preserve known unsatisfiable, duplicate-heavy, symmetric, and hard instances;
10. record structural counters and resource termination status.

For a candidate prune $P$, bounded tests can seek a counterexample by enumerating all completions below pruned prefixes. Passing does not prove the implication universally, but failure gives an actionable witness and strong regression protection.

## Definitions and Notation

- $x_0,\ldots,x_{n-1}$: variables or choice positions.
- $D_i$: declared domain of variable $x_i$ before propagation.
- $p$: active partial candidate or assignment.
- $|p|$: chosen depth or assigned-variable count when the construction is prefix-based.
- $p\oplus x$: extension of $p$ by choice $x$.
- $X(p)$: finite ordered next-choice set.
- $\mathcal C(p)$: required complete solutions extending $p$.
- $\operatorname{complete}(p)$: predicate that every required choice is assigned.
- $\operatorname{accept}(p)$: full feasibility predicate.
- $P(p)$: prune or reject predicate.
- $V_k$: visited nodes at depth $k$.
- $N$: total visited nodes.
- $b,d$: branching factor and maximum depth in a simplified tree model.
- $K$: number of emitted solutions.
- **Choice point:** saved position with unexplored alternatives.
- **Conflict:** evidence that the active partial candidate has no valid completion under a declared inference rule.
- **Forward checking:** removal of immediately inconsistent values from future domains.
- **Propagation:** repeated sound inference until quiescence or contradiction.
- **Trail:** reversible log of mutations since checkpoints.
- **Checkpoint:** trail position to which restoration rewinds.
- **Fail-first ordering:** policy that tries to expose small or constrained subproblems early.
- **Symmetry orbit:** solutions reachable from one another under declared symmetry transformations.
- **Incomplete result:** bounded search result that makes no exhausted-search claim.

“Promising” is safe terminology only when it is defined operationally. If `promising(p)` controls pruning, its false case needs the same empty-completion proof as $P(p)$.

## Mechanisms, Invariants, or Proof Structure

Use this backtracking design and review worksheet.

1. **Output contract.** Declare find-one, deterministic-first, enumerate, count, or optimize-all behavior.
2. **Candidate semantics.** Define what a partial and complete candidate represent.
3. **Choice partition.** Define $X(p)$ and prove coverage; prove disjointness for unique enumeration.
4. **Progress rank.** Show every extension increases a bounded measure.
5. **Acceptance.** Validate completeness and all constraints independently at emission.
6. **Prune inventory.** State each implication and every domain assumption that makes it sound.
7. **Incremental state.** Map each constraint to summaries and recomputation invariants.
8. **Propagation.** Define deletions, fixed point, contradiction, and preservation of all solutions.
9. **Ordering policy.** Separate variable/value order from deletion and version deterministic ties.
10. **Mutation model.** Choose copy or trail; enumerate every field changed by apply and undo.
11. **Restoration proof.** Establish inverse operations and reverse order from checkpoints.
12. **Duplicate policy.** Define output identity, canonical paths, and symmetry orbits.
13. **Cost model.** Count nodes, choices, checks, propagation, mutation, output, depth, and bytes.
14. **Termination status.** Separate exhaustive completion, first witness, infeasibility, cancellation, and resource exhaustion.
15. **Concurrency.** Define subtree ownership, shared state, cancellation, ordering, and aggregation.
16. **Independent evidence.** Compare solution sets with brute force, recompute summaries, inject failures, and replay witnesses.

The proof architecture follows the worksheet: acceptance proves soundness; child coverage plus prune implications proves completeness; disjoint children and canonical symmetry rules prove uniqueness; progress and finite branching prove termination; apply/undo invariants connect the mathematical tree to the mutable implementation.

## Alternatives and Trade-Offs

- **Generate-and-test versus incremental rejection:** full candidates simplify reasoning; partial checks avoid doomed suffix generation.
- **Copy versus mutate-and-trail:** copies isolate siblings; trails reduce copying but enlarge restoration obligations.
- **Recursion versus explicit frames:** recursion mirrors the tree; explicit stacks govern depth, checkpoints, and pause/resume.
- **Static versus fail-first variable order:** static order is reproducible and cheap; fail-first can shrink trees but costs domain measurement.
- **Natural versus least-constraining value order:** natural order stabilizes first witness; lookahead can improve find-one latency.
- **Forward checking versus stronger propagation:** stronger inference may remove more nodes while costing more per node and more trail traffic.
- **One solution versus all solutions:** early return bounds output; enumeration needs uniqueness, streaming, and output budgets.
- **Enumeration versus counting:** counts avoid witness storage but may overflow and do not provide explanations.
- **Labeled versus quotient solutions:** labeled enumeration preserves identities; symmetry representatives reduce work but change output semantics.
- **Backtracking versus dynamic programming:** tree search preserves histories; DP merges sufficient residual states and may avoid recomputation.
- **Backtracking versus branch and bound:** infeasibility proofs remove impossible completions; objective bounds remove noncompetitive feasible completions.
- **Sequential versus parallel subtrees:** sequential order is simple; parallel search needs aggregation, memory, cancellation, and deterministic-output policy.
- **Exact completion versus budgeted search:** exhaustive status proves absence; bounded status protects resources but remains incomplete.
- **Domain-specific structure versus generic solver:** specialized masks and indexes can be fast; generic propagation can improve reuse and modeling.

## Failure Modes and Misconceptions

1. **Solution-space ambiguity:** identities, equality, and output mode are undeclared.
2. **Partial acceptance:** consistency so far is mistaken for a complete solution.
3. **Missing branch:** next-choice generation omits a legal value.
4. **Duplicate paths:** unordered selections are constructed in several orders.
5. **Unsound prune:** a heuristic score is treated as an impossibility theorem.
6. **Hidden sign premise:** sum or capacity pruning assumes nonnegative future contributions.
7. **Local-global confusion:** arc consistency or nonempty domains are treated as satisfiability proof.
8. **Order deletes choices:** fail-first or value scoring accidentally filters rather than reorders.
9. **Unstable ties:** iteration through an unordered container changes the first solution.
10. **No progress:** an extension can reproduce the same partial candidate or depth.
11. **State leak:** undo misses a count, mask, domain, index, cache, or hash.
12. **Wrong undo order:** dependent reversible mutations are restored forward rather than backward.
13. **Exceptional leak:** early return, callback failure, or cancellation skips cleanup.
14. **Mutable yield:** every saved witness aliases the active path buffer.
15. **Overcopying:** a large state is cloned per node despite small reversible deltas.
16. **Stale propagation:** support counts or watched structures no longer match domains.
17. **Value deduplication by accident:** equal-valued distinct identities disappear.
18. **Global sibling dedup:** a value used at one depth is forbidden at every later depth.
19. **Unproved symmetry:** at least one orbit has no allowed representative.
20. **Bad symmetry count:** representative count is multiplied by a constant despite stabilizers.
21. **Wrong memo key:** distinct histories with different remaining outputs share a cached search result.
22. **Cached witness loss:** feasibility caching suppresses required alternative witnesses.
23. **Count overflow:** a plausible small integer replaces an enormous exact count.
24. **Output explosion:** all witnesses are retained in memory rather than streamed or bounded.
25. **Timeout means false:** resource exhaustion is returned as unsatisfiable.
26. **Hidden factorial cost:** concise recursive code is described as efficient without a node bound.
27. **Parallel arrival nondeterminism:** scheduler order violates a stable enumeration contract.
28. **Shared mutable solver:** tenants or concurrent subtrees corrupt one another's trails.
29. **Sensitive telemetry:** candidate assignments or proofs leak through logs.
30. **Benchmark by one instance:** a heuristic is declared superior without distribution and tail evidence.

## Worked Examples

### Example 1

**Question:** How should an all-subsets search avoid constructing the same subset in different orders?

**Reasoning:** Give each source element an index and pass a strictly increasing next-start index. After choosing index $i$, descendants may choose only $j>i$. Every subset then has one path: its sorted index sequence.

**Conclusion:** Canonical construction proves duplicate-free coverage without a global result-deduplication set.

### Example 2

**Question:** Why may n-queens reject two queens on one diagonal immediately?

**Reasoning:** Placed queens never move. Any completion retains both conflicting queens, so every descendant violates the constraint. The current partial candidate therefore has an empty feasible-completion set.

**Conclusion:** Diagonal-conflict pruning is logically sound and cheaper than generating full boards.

### Example 3

**Question:** Is “current sum exceeds target” always a sound prune?

**Reasoning:** For target 5, prefix sum 7 and remaining selectable value $-2$ produce a valid completion. The prune becomes sound only under assumptions such as all remaining values nonnegative and additions irreversible.

**Conclusion:** Put numeric-domain assumptions in the prune proof, not only in test data.

### Example 4

**Question:** What restoration bug arises if a graph-coloring solver removes neighbor colors but undoes only the selected vertex?

**Reasoning:** A sibling begins with domains narrowed by the prior branch. It may be falsely rejected or forced, omitting valid colorings. The main assignment array can look correct while auxiliary state is stale.

**Conclusion:** Trail every domain deletion and rewind to the exact pre-choice checkpoint.

### Example 5

**Question:** Why can minimum-remaining-values ordering help a finite-domain puzzle?

**Reasoning:** A variable with one legal value either forces progress or exposes contradiction now; choosing a variable with ten values can create ten large subtrees before discovering the same failure. Both orders remain exact if all alternatives are retained.

**Conclusion:** Fail-first changes tree shape, not the prune theorem or solution set.

### Example 6

**Question:** Does Sudoku propagation eliminate the need for search whenever no cell domain is empty?

**Reasoning:** Removing row, column, and box conflicts can reach a fixed point with several nonempty domains while global alternatives still conflict later. Local consistency means only that these inference rules found no contradiction.

**Conclusion:** Propagation and branching alternate; a nonempty fixed point is not a completed grid.

### Example 7

**Question:** How many distinct permutations does multiset $\{A,A,B\}$ have?

**Reasoning:** Index permutations number $3!=6$, but swapping the two equal $A$ identities does not change a value sequence. The distinct sequences are `AAB`, `ABA`, and `BAA`, totaling $3!/2!=3$.

**Conclusion:** Deduplicate by value only if the output contract treats equal $A$ objects as interchangeable.

### Example 8

**Question:** May an n-queens counter search explore only half the first-row columns and double the count?

**Reasoning:** Reflection pairs off-center solutions, but odd $n$ has a central-column first-row branch mapped to itself at that first decision. It must be searched and counted separately; more complex symmetries can have other stabilizers.

**Conclusion:** Symmetry arithmetic needs orbit reasoning, not a blanket multiplier.

### Example 9

**Question:** Can an enumerator output one billion length-100 witnesses in sublinear time?

**Reasoning:** Merely writing materialized witnesses requires at least $100$ billion value positions, regardless of how efficiently the search tree is traversed.

**Conclusion:** State output-sensitive lower bounds and offer count, stream, limit, or sample modes explicitly.

### Example 10

**Question:** What should a configuration service return after a ten-million-node budget expires with no witness found?

**Reasoning:** Unvisited branches may contain a solution. The observations prove only that the explored prefix contains none. Returning `unsatisfiable` would turn a resource policy into a false mathematical claim.

**Conclusion:** Return an incomplete status with budget reason and structural counters; reserve infeasibility for exhausted or certified search.

## Cross-Program Connections

- [Theory of Computation & Complexity](../../15-theory-of-computation-and-complexity/ROADMAP.md) owns nondeterminism, reducibility, NP search, lower bounds, and proof/certificate complexity.
- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) owns bitsets, reversible lists, persistent states, trails, watched indexes, and compact stacks.
- [Programming Languages & Semantics](../../01-programming-languages-and-semantics/ROADMAP.md) owns recursion, mutation, aliasing, exceptions, generators, cleanup, and effect semantics.
- [Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) owns exhaustive oracles, property-based generation, fault injection, differential checking, and reproducible benchmarks.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) owns adversarial resource exhaustion, tenant isolation, sensitive candidates, authorization, and safe failure status.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) owns partitioned search, duplicate work, leases, checkpointing, cancellation, and deterministic aggregation across workers.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md) owns resource budgets, admission, telemetry, operational limits, and failure containment.

## References

1. Solomon W. Golomb and Leonard D. Baumert. [“Backtrack Programming”](https://doi.org/10.1145/321296.321300), *Journal of the ACM* 12(4), 1965, pp. 516–524. Primary systematic backtracking source.
2. Robert W. Floyd. [“Nondeterministic Algorithms”](https://doi.org/10.1145/321420.321422), *Journal of the ACM* 14(4), 1967, pp. 636–644. Primary choice-to-backtracking formulation with eight-queens and graph examples.
3. Martin Davis, George Logemann, and Donald W. Loveland. [“A Machine Program for Theorem-Proving”](https://doi.org/10.1145/368273.368557), *Communications of the ACM* 5(7), 1962, pp. 394–397. Primary SAT decision, propagation, and backtracking work.
4. Alan K. Mackworth. [“Consistency in Networks of Relations”](https://doi.org/10.1016/0004-3702%2877%2990007-8), *Artificial Intelligence* 8(1), 1977, pp. 99–118. Constraint consistency and propagation foundations.
5. Robert M. Haralick and Gordon L. Elliott. [“Increasing Tree Search Efficiency for Constraint Satisfaction Problems”](https://doi.org/10.1016/0004-3702%2880%2990051-X), *Artificial Intelligence* 14(3), 1980, pp. 263–313. Forward checking and fail-first search evidence.
6. Donald E. Knuth. [“Dancing Links”](https://arxiv.org/abs/cs/0011047), 2000. Primary reversible-update treatment for exact-cover-style depth-first search.
7. Francesca Rossi, Peter van Beek, and Toby Walsh, editors. [*Handbook of Constraint Programming*](https://shop.elsevier.com/books/handbook-of-constraint-programming/rossi/978-0-444-52726-4), Elsevier, 2006. Authoritative constraint modeling, propagation, search, and application reference.
8. ACM, IEEE Computer Society, and AAAI. [*Computer Science Curricula 2023: Algorithmic Foundations*](https://csed.acm.org/algorithms-and-complexity/), endorsed 2024; consulted 2026-09-04. Current curricular scope for backtracking and algorithmic problem solving.

## Exercises

### Exercise 1

Trace the increasing-column bit-mask solver for four queens. List all two solutions, count legal partial placements at every depth and in total, explain each mask's meaning, and prove push/pop restoration and deterministic order.

### Exercise 2

Prove the generic backtracking theorem: under complete child coverage, disjoint child completion sets, sound pruning, complete acceptance, finite branching, and a bounded increasing rank, the algorithm terminates and emits every target solution exactly once and no invalid candidate. Identify which premise proves each claim.

### Exercise 3

Diagnose three defects in a subset-sum enumerator: it prunes whenever partial sum exceeds target although negative values are allowed; it removes a selected value from a `used` set but forgets to restore its multiplicity count; and it appends the live mutable path object to its results. Give minimal counterexamples, repairs, and regression properties.

### Exercise 4

A depth-40 search state occupies 2 MiB. Copy-based recursion retains one full state per active depth. A trail-based implementation retains one 2 MiB base state and at most six 16-byte change records per depth. Compute peak state/trail bytes excluding common call frames, compare the results, and state the proof and measurement obligations before choosing trails.

### Exercise 5

Design an exact multi-tenant dependency configurator. Components have versions, conflicts, required capabilities, optional dependencies, license policies, and platform constraints. The API supports deterministic first solution, all-solutions streaming, and a node budget. Specify candidates, choices, sound prunes, propagation, ordering, mutation/restoration, duplicate identity, statuses, concurrency, security/resource limits, telemetry, independent tests, and rollout evidence. Do not use objective-bound pruning.

## Answers to the Exercises

### Answer 1

The solutions are

$$
(1,3,0,2)
\quad\text{and}\quad
(2,0,3,1).
$$

Counting the root and every conflict-free partial placement gives depth counts

$$
|V_0|,|V_1|,|V_2|,|V_3|,|V_4|
=1,4,6,4,2,
$$

so total nodes are

$$
1+4+6+4+2=17.
$$

At each row, $C$ marks occupied columns. $L$ and $R$ mark columns attacked in the current row by the two diagonal directions; after choosing one-bit $q$, shifting prepares attacks for the next row. Intersecting the complement with $M=2^4-1$ confines positions to four columns.

The least significant available bit is selected first, so columns are visited $0,1,2,3$. Each descent appends exactly the chosen column and each return pops exactly that value. Mask arguments are passed by value in this implementation. By induction on active depth, the list equals the root-to-node columns before every call and returns to its prior tuple after every child; it is empty after the root returns.

An independent checker verifies distinct columns and $|c_i-c_j|\ne|i-j|$. Exhausting all $4^4=256$ row-to-column tuples finds exactly the same two witnesses.

### Answer 2

Termination follows from strict increase of a bounded rank: every root-to-leaf path is finite. Finite branching then makes the entire reachable tree finite.

Soundness follows from complete acceptance: emission occurs only for a complete candidate satisfying the full target predicate. It does not follow from partial consistency alone.

For completeness, fix target solution $z$. At any visited prefix whose completion set contains $z$, child coverage places $z$ in at least one child completion set. Sound pruning cannot reject this prefix or that child because its completion set is nonempty. Exhaustive child traversal and termination therefore reach a complete node representing $z$.

Disjoint child completion sets make that child unique at every depth. Induction gives one root-to-leaf path for $z$, and one emission per accepted leaf gives no duplicate. Without disjointness, sound and complete enumeration could still emit the same solution several times.

Thus acceptance proves no invalid output; coverage plus sound pruning proves no missing target; disjointness proves uniqueness; rank plus finite branching proves termination. Mutation correctness is an additional implementation premise needed to ensure the executed tree matches this mathematical tree.

### Answer 3

For target 5, values $(7,-2)$ form a minimal sign counterexample: after choosing 7, the current sum exceeds 5, yet adding $-2$ succeeds. Repair by removing the prune, or derive interval bounds from remaining values. For example, prune only when target lies outside

$$
\left[
s+\sum_{v\in R}\min(v,0),
s+\sum_{v\in R}\max(v,0)
\right],
$$

where $s$ is current sum and $R$ the remaining multiset. Test every small signed multiset against direct subset enumeration and specifically require $(7,-2)$.

The stale multiplicity count corrupts sibling state. With values $(1,1)$ and a representation that tracks two available copies, returning from a branch can leave only one or zero available, omitting a legitimate two-copy selection. Trail the prior count or increment it in guaranteed cleanup, and assert the complete frequency map equals its pre-choice snapshot after every child and injected exception.

Appending the live path aliases results. For values $(1,2)$ an enumerator may ultimately show several references all equal to the final empty or last-mutated list. Append `tuple(path)` or a list copy. Test object identities, immutable contents after traversal, and behavior when a consumer retains results while iteration continues.

### Answer 4

One mebibyte is $2^{20}=1{,}048{,}576$ bytes, so one 2 MiB state is 2,097,152 bytes. Under the exercise's one-full-state-per-active-depth convention, depth 40 uses

$$
40\cdot2{,}097{,}152=83{,}886{,}080\text{ bytes}
$$

or 80 MiB.

If “depth 40” instead meant 40 edges below a separately retained root, 41 full states would have to be charged; depth conventions must be explicit in measured reports.

The trail holds at most

$$
40\cdot6\cdot16=3{,}840\text{ bytes}
$$

plus the 2,097,152-byte base, totaling 2,100,992 bytes. The nominal reduction is 81,785,088 bytes, about 77.996 MiB.

This model omits container capacity, allocator headers, copied sharing, indexes, call frames, and propagation work. Trails are acceptable only after proving every mutation is recorded once as needed, rewind order is inverse-correct, checkpoints nest, and exception/cancellation paths restore. Differentially compare solution sets with copying, snapshot before/after every child, inject failures, and measure actual resident bytes and per-node time on representative tree shapes.

### Answer 5

A partial candidate maps selected component identities to exact versions and records unresolved capability requirements. The output identity distinguishes package source, canonical name, version, platform build, and policy-relevant metadata. Deterministic first-solution mode versions a total variable and value order; all-solutions mode streams immutable canonical lockfiles.

Choose an unresolved requirement or component, then branch over every admissible provider/version in stable order. Sound prunes include a selected-version conflict, an unsatisfied requirement with no remaining provider, a license or platform rule that no future choice can reverse, two incompatible singleton requirements, and an empty domain after sound propagation. Do not reject a branch merely because its download size or version score looks poor.

Propagation removes versions conflicting with a selection, adds transitive required capabilities, intersects platform/license domains, and repeats to a fixed point. A fail-first rule may choose the requirement with fewest remaining providers, with canonical identity ties. Every deletion and inserted requirement is trailed from a checkpoint; unwind in reverse order and verify domains, reverse indexes, counts, hashes, and the selected map.

Deduplicate by full component identity, not display name. If two repositories publish byte-identical artifacts but policy treats their provenance differently, they remain distinct. Prove any repository mirroring or platform symmetry before quotienting it.

Return `solution`, `unsatisfiable` after exhaustive search, or `incomplete(reason, nodes, solutions_so_far)` at a node/time/memory/output budget. Find-one cleanup completes before returning. Enumeration provides backpressure and a solution/byte cap; exact counts use checked arbitrary-precision arithmetic or a declared maximum.

Use one isolated solver state per request or owned subtree. Parallel root branches receive immutable input snapshots and private trails. Merge by stable branch sequence if deterministic stream order is promised. Cancellation discards or fully rewinds the instance; no partially restored object returns to a pool.

Validate manifest size, versions, domain products, dependency depth, constraint arity, signature/provenance data, and policy revision. Apply per-tenant admission, worker, CPU, memory, node, depth, and output limits. Avoid logging private package coordinates or policy inputs; report aggregate domain and conflict reason codes.

Record nodes by depth, choices, conflicts by proven rule, propagation checks/deletions, empty domains, backtracks, maximum trail, solutions, duplicates rejected, status, budgets, latency, bytes, cancellation, and restoration failures. An independent brute-force oracle enumerates all small version products and directly checks constraints. Differential tests permute input order, disable each prune, compare copy versus trail, inject cancellation at every depth, exercise duplicate identities and unsatisfiable cores, and replay every emitted lockfile.

Roll out in shadow mode against an established exact evaluator on immutable signed snapshots. Require zero unexplained solution/status mismatches, stable first witnesses, restoration integrity, enforced resource ceilings, and acceptable tail cost before canary expansion. Keep deterministic rollback and never promote a speed improvement that converts incomplete search into false unsatisfiability.
