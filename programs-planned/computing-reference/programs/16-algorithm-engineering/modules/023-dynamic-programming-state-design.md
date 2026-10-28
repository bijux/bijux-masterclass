---
module_id: ALGE-023
program: Algorithm Engineering
level: 1
module_number: 23
title: Dynamic Programming State Design
status: complete
last_verified: 2026-09-04
---

# Dynamic Programming State Design

## One-Page Review

### Governing question

What information from a partial history must a dynamic-programming state retain so every feasible continuation and its incremental objective depend only on that state?

### Essential definitions

- **Dynamic programming** solves overlapping subproblems once and composes their values through a recurrence.
- A **state** is a canonical description of all history information relevant to future choices and costs.
- A **state variable** is one coordinate such as position, remaining capacity, endpoint, subset, mode, or automaton state.
- A **sufficient state** never merges histories with different future feasibility or continuation values.
- A **minimal state** omits no necessary information and carries no future-irrelevant distinction, relative to a declared model.
- A **transition** applies one legal decision and moves to another state.
- A **Bellman recurrence** optimizes immediate contribution plus a child-state value.
- A **state DAG** has states as vertices and legal dependencies as directed edges.
- **Optimal substructure** means an optimal solution contains optimal solutions to the subproblems identified by the complete state.
- **Reconstruction metadata** records enough choices or values to recover a deterministic witness, not only its objective.

### Central model, mechanism, or theorem

Let state $s$ have legal actions $A(s)$, transition $\tau(s,a)$, immediate contribution $c(s,a)$, terminal set $F$, and optimization operator $\operatorname{opt}$. Then

$$
V(s)=
\operatorname*{opt}_{a\in A(s)}
\left(c(s,a)+V(\tau(s,a))\right),
$$

with declared terminal values $V(f)$ for $f\in F$. A rank $r$ must decrease along every dependency, or another well-founded evaluation argument must exist.

Two histories $h_1,h_2$ may share a state only if they induce the same legal continuation language and the same incremental objective for every continuation after any prefix contribution already stored separately. Under-specification corrupts the recurrence; over-specification can turn polynomially many equivalence classes into exponentially many histories.

If $\mathcal S_R$ is the set of reachable states and $A(s)$ their actions, a direct evaluation work bound is

$$
O\left(\sum_{s\in\mathcal S_R}(1+|A(s)|)\right),
$$

plus transition, comparison, and reconstruction costs. “States times transitions per state” must use reachable, representable states and actual transition cost.

### Critical invariants

- The state key contains every future-relevant constraint, resource, endpoint, and mode.
- Histories mapped to one state have identical legal continuations and aligned incremental costs.
- Every transition preserves domain invariants and moves toward a terminal state or follows an acyclic dependency order.
- The recurrence enumerates every legal first decision exactly as intended.
- Base states cover every transition boundary, including empty prefixes, zero budgets, and impossible states.
- Impossible states use a sentinel that cannot win arithmetic accidentally.
- Objective arithmetic, infinity, counts, and ties have explicit numeric semantics.
- Reconstruction choices correspond to the same recurrence and deterministic tie order.
- Complexity counts reachable states, outgoing transitions, key size, and representation width.
- Compression or dominance discards a state only with a proof that no future continuation can prefer it.

### Common failures

Common failures include using “position” when remaining capacity matters; using only a subset when the last endpoint matters; merging states with different automaton modes; retaining the entire decision history; writing a recurrence before defining semantics; assuming optimal substructure for an incomplete state; creating cyclic dependencies; forgetting empty and impossible states; adding to infinity and overflowing; confusing numeric magnitude with input length; allocating a capacity table from untrusted values; reconstructing with different tie rules; discarding equal-value states that differ in future resources; and quoting rectangular table size when most states are unreachable—or reachable exponential states when a polynomial table was implied.

### Compact example

For 0/1 knapsack, state $(i,b)$ means: using items with indices at least $i$ and remaining capacity $b$, what maximum additional value is possible? With weight $w_i$ and value $v_i$,

$$
V(i,b)=
\max\left(
V(i+1,b),
v_i+V(i+1,b-w_i)
\right)
$$

when $w_i\le b$, and only the skip branch otherwise. Item index prevents reuse; remaining capacity distinguishes histories with different futures. For items $A=(3,4)$, $B=(4,5)$, $C=(2,3)$, $D=(3,7)$ and capacity 6, the optimum selects $(A,D)$ with value 11 and weight 6.

### Connections

[ALGE-004](./004-inductive-correctness-proofs.md) supplies induction, [ALGE-021](./021-divide-and-conquer.md) supplies recursive decomposition, [ALGE-022](./022-greedy-choice-and-exchange-arguments.md) shows when alternatives may be discarded immediately, and [ALGE-024](../ROADMAP.md) evaluates the resulting state graph by memoization and bottom-up order.

## Governing Question

Which partial histories are equivalent with respect to every possible future, and how can those equivalence classes become a finite, correct, and tractable state graph?

Dynamic programming is often introduced as “store recursive results.” Storage is secondary. The central design act is choosing the subproblem. A state must remember enough context that the future no longer depends on the omitted history. It should also forget everything irrelevant, because each retained distinction multiplies the state space.

The recurrence then becomes a specification over those states. It enumerates legal next decisions, composes immediate and future objective contributions, defines terminals and impossibility, and creates a dependency graph. Memoization and table order are evaluation strategies for that graph; ALGE-024 treats them separately.

## Why This Matters

State design is the difference between a correct polynomial algorithm, an incorrect small table, and an exact but exponential history search. Edit distance needs two prefix positions. Knapsack needs item position and remaining capacity. Traveling-salesperson subset DP needs both the visited subset and the current endpoint. Constrained strings may need input position and automaton state.

The same issue appears in production planners and optimizers. A query-plan state keyed only by joined relations can discard a slightly more expensive ordering that makes the parent cheaper. A scheduler keyed only by time can merge states with different remaining resources. A routing algorithm can discard a path that costs more but consumes less risk budget. State sufficiency is an interface and information problem.

Good designs make proof, complexity, reconstruction, and operations line up. The state semantics explain table keys. The recurrence explains dependencies. The rank explains evaluation order. The witness rule explains parent metadata. The state count explains memory exposure and input limits.

## Prerequisites and Retrieval

Retrieve:

- induction, invariants, sets, sequences, graphs, DAGs, and topological order;
- optimization, feasibility, prefix/suffix and interval notation, and deterministic ties;
- recursion trees, overlapping subproblems, and asymptotic analysis;
- arrays, maps, bitsets, tuples, integer ranges, overflow, and sentinel values;
- shortest paths in DAGs, finite automata, sequence editing, and subset enumeration;
- exhaustive search and independent small-instance oracles.

You should be able to state a subproblem in one sentence, prove a recurrence by classifying its first or last decision, and distinguish numeric input magnitude from its encoded bit length.

## Learning Objectives

After completing this module, you should be able to:

1. derive states as equivalence classes of future behavior;
2. detect under-specified and over-specified state keys;
3. define Bellman semantics, transitions, bases, and impossible values;
4. prove recurrence soundness and completeness by first/last-choice decomposition;
5. construct position, resource, interval, subset-endpoint, and automaton-product states;
6. derive reachable-state, transition, time, and space bounds;
7. distinguish polynomial, pseudopolynomial, and exponential dynamic programs;
8. design deterministic witness reconstruction and tie-breaking;
9. justify dominance, Pareto frontiers, and state compression safely;
10. validate state sufficiency with collision tests, exhaustive oracles, and boundary instrumentation.

## Core Exposition

### Start from histories and future equivalence

Let a history $h$ describe decisions already made. Define its feasible continuations $\mathcal C(h)$. After separating any fixed prefix contribution $g(h)$, two histories may share a state when:

1. $\mathcal C(h_1)=\mathcal C(h_2)$ under the same continuation representation;
2. every continuation $z$ has the same incremental contribution from both histories;
3. reconstruction can translate a state-level choice back to the required identities.

This is a Markov-style sufficiency condition. The future need not know how the state was reached. A state function $\phi(h)$ deliberately quotients histories into equivalence classes.

Under-specification maps inequivalent histories together. Over-specification keeps distinctions such as the complete chosen sequence even when only its endpoint and resource use affect the future. The former changes answers; the latter loses reuse.

### Write state semantics as a sentence

Before a formula, write:

> $V(s)$ is the optimal additional objective obtainable from exactly the unresolved instance described by $s$, subject to these retained constraints.

The words “additional” and “exactly” matter. They prevent double-counting prefix cost and ambiguity about what has already been consumed. Include direction—minimum or maximum—and the witness/tie contract.

For knapsack:

> $V(i,b)$ is the maximum additional value obtainable from items $i,\ldots,n-1$, choosing each at most once, with remaining capacity $b$.

This sentence immediately suggests bases, legal transitions, and proof induction on $n-i$.

### Derive recurrence by a complete decision partition

Classify every feasible solution by its first or last decision. For knapsack state $(i,b)$, every solution either excludes item $i$ or includes it. Inclusion is legal only when $w_i\le b$. These classes are disjoint and exhaustive, so

$$
V(i,b)=
\begin{cases}
0, & i=n,\\
V(i+1,b), & i<n\text{ and }w_i>b,\\
\max\{V(i+1,b),v_i+V(i+1,b-w_i)\}, & w_i\le b.
\end{cases}
$$

Soundness shows each branch constructs a feasible solution. Completeness shows every feasible solution belongs to a branch. Optimal substructure follows because a nonoptimal child completion could be replaced without changing the state boundary.

### Prove the state contains enough history

Try to construct a collision: two histories with the same proposed key but different legal futures or continuation values.

For 0/1 knapsack, key $i$ alone collides histories with different remaining capacity. Key $b$ alone permits reusing or skipping a different remaining item set. Pair $(i,b)$ resolves both for fixed item order.

For a path problem with a hop budget, vertex alone is insufficient: two arrivals at the same vertex with different remaining hops have different futures. State $(v,h)$ is sufficient when edge feasibility depends only on current vertex and remaining hops.

Collision search is a design tool, not a proof by testing. Once no collision is apparent, prove the future-equivalence condition for all histories admitted by the model.

### Remove future-irrelevant history

Suppose a sequence problem's future legality depends only on the last chosen category, not the full category sequence. Replace history tuple $(c_1,\ldots,c_k)$ with last category $c_k$, plus any other relevant resource coordinates. If accumulated cost is additive, keep it outside the state value rather than in the key.

Avoid storing answer-so-far in the key when $V(s)$ already means optimal remaining value. That distinction prevents a separate state for every prefix objective. Retain prefix information only when it changes future feasibility, transition cost, or required output identity.

Minimality is relative to the problem model and cost representation. A supposedly irrelevant field can become necessary when the API adds a constraint or a secondary objective.

### Design position and resource states

Many sequence/resource problems use $(i,b)$:

- $i$ separates processed from unprocessed decisions;
- $b$ represents remaining or used budget;
- transition advances $i$ and updates $b$.

For nonnegative integer capacity $B$, a rectangular 0/1 knapsack table has $(n+1)(B+1)$ possible states and constant outgoing actions, giving $O(nB)$ arithmetic operations and $O(nB)$ stored values in the direct layout.

This is pseudopolynomial. If $B$ is encoded in binary, input length for the capacity is $\Theta(\log B)$, while the table is linear in its numeric magnitude. Validate $B$, multiplication, allocation bytes, and service limits before constructing it.

If weights are real or enormous sparse integers, capacity indexing may be invalid or impractical. Alternative value-indexed, Pareto-frontier, approximation, or search formulations need their own bounds.

### Design prefix-pair states for sequence transformation

For strings $x$ and $y$, let $D(i,j)$ be the minimum cost to transform prefix $x[0:i)$ into $y[0:j)$. Unit-cost edit distance uses

$$
D(0,j)=j,
\qquad
D(i,0)=i,
$$

and for $i,j>0$,

$$
D(i,j)=\min\begin{cases}
D(i-1,j)+1,\\
D(i,j-1)+1,\\
D(i-1,j-1)+[x_{i-1}\ne y_{j-1}].
\end{cases}
$$

The last operation is deletion, insertion, or match/substitution. These classes cover every edit script's final operation. State $(i,j)$ is sufficient because earlier character identities outside the prefixes no longer affect the remaining recurrence under the declared additive edit model.

Changing the model can require more state. Adjacent transpositions, affine gap costs, bounded runs, normalization, or context-dependent substitutions introduce modes or additional indices.

### Use interval states when boundaries define the residual problem

Matrix-chain multiplication and many parsing problems use interval state $(i,j)$. A split $k$ creates $(i,k)$ and $(k+1,j)$, and recurrence considers every legal final split.

For matrix dimensions $p_0,\ldots,p_n$, let $M(i,j)$ be minimum scalar multiplications for matrices $A_i\cdots A_j$. Then

$$
M(i,i)=0,
$$

$$
M(i,j)=
\min_{i\le k<j}
\left(
M(i,k)+M(k+1,j)+p_{i-1}p_kp_j
\right).
$$

There are $\Theta(n^2)$ intervals and up to $\Theta(n)$ splits each, giving $\Theta(n^3)$ direct work. Bound dimension products with checked arithmetic; overflow can reverse the chosen plan.

An interval key is sufficient only when the subproblem's outside context does not change its cost. Grammar parsing may need a nonterminal coordinate; boundary-conditioned optimization may need endpoint states.

### Add an endpoint to subset state

For traveling salesperson with fixed start $0$, subset alone is insufficient: future cost depends on the current last city. Define

$$
H(S,j)
$$

as the minimum cost of a path starting at 0, visiting exactly $S$ (including $0$ and $j$), and ending at $j$. Then

$$
H(S,j)=
\min_{i\in S\setminus\{j\}}
\left(H(S\setminus\{j\},i)+d_{ij}\right).
$$

The endpoint makes transition cost well defined. The state count is $\Theta(n2^n)$ and transitions yield $O(n^22^n)$ work in a straightforward implementation. Dynamic programming removes duplicate histories but does not guarantee polynomial state count.

Bitmask representation requires a bound on $n$, canonical city indexing, checked shifts, and memory accounting. Symmetry reductions need proof that reconstruction and asymmetric costs remain valid.

### Form product states for finite memory constraints

If a sequence must satisfy a finite automaton, combine position $i$ with automaton state $q$:

$$
V(i,q)=
\operatorname*{opt}_{a\in\Sigma:\,\delta(q,a)\in Q_{\mathrm{safe}}}
\left(c(i,q,a)+V(i+1,\delta(q,a))\right).
$$

The automaton state is a compact summary of all prefix history relevant to future acceptance. With $m$ positions and $|Q|$ modes, there are at most $O(m|Q|)$ product states.

This pattern handles run-length restrictions, forbidden patterns, parity, protocol modes, and bounded local context. If the constraint requires unbounded history, a finite $q$ may not exist.

### View the recurrence as a state DAG

Create one vertex for each reachable state and an edge $s\to t$ for every transition whose value depends on $V(t)$. Bases are sinks or sources depending on edge orientation. A rank such as remaining items, prefix sum $i+j$, interval length, or subset cardinality supplies a topological order.

This view reveals:

- cycles caused by a missing progress coordinate;
- unreachable rectangular table cells;
- fan-out and transition costs;
- parallel wavefronts;
- reconstruction edges;
- equivalence to shortest or longest paths in a DAG.

If the recurrence contains genuine cycles, ordinary finite DAG dynamic programming does not apply directly. Reformulate, solve a fixed point under justified conditions, or use a graph algorithm suited to cycles.

### Count reachable states and transition work

Do not stop at “there are two loops.” Let $\mathcal S_R$ be reachable states. Then a generic bound is

$$
O\left(
\sum_{s\in\mathcal S_R}
(\operatorname{cost}_{\mathrm{lookup}}(s)
+\sum_{a\in A(s)}\operatorname{cost}(s,a))
\right).
$$

A dense array can make lookup constant but allocate unreachable cells. A map can store only reachable states but pays hashing, key storage, and allocator overhead. A subset key costs more to hash and compare than a small integer index.

Report state count, attempted and accepted transitions, maximum fan-out, key bytes, value bytes, parent bytes, and peak storage. Separate asymptotic operation count from measured physical cost.

### Preserve impossible states safely

Minimization often uses $+\infty$ and maximization $-\infty$. In fixed-width code, a largest integer sentinel plus edge cost can overflow into a winning negative value. Either:

- use a tagged `unreachable` variant;
- guard addition before arithmetic;
- use a numeric infinity with defined behavior;
- prove a finite bound and choose checked representation.

Base cases distinguish valid empty solutions from impossibility. Knapsack's no-items state has value zero for every nonnegative remaining capacity. Exact-fill knapsack would instead make positive residual capacity impossible. The same table shape can encode different problems; semantics control bases.

### Design witness reconstruction with the value recurrence

An objective value may be insufficient for the API. Reconstruction strategies include:

- store the chosen action per state;
- compare child values again during a second traversal;
- store persistent witness fragments;
- divide and recompute to trade time for space.

Define a total tie order, such as maximum value, then minimum used weight, then lexicographically smallest identity sequence. Apply it inside every state comparison. A later reconstruction rule that breaks ties differently can select a transition inconsistent with stored compressed values.

Count parent/action storage and validate that reconstructed transitions start at the requested state, remain legal, reach a terminal, and reproduce the reported objective.

### Use dominance only when every future agrees

At the same logical position, state $a$ may dominate $b$ if it uses no more of every constrained resource, has no worse accumulated objective, and has at least the same future action set. Then no continuation can make $b$ uniquely preferable.

With multiple resources, retain a Pareto frontier rather than one scalar best. A cheaper plan with worse ordering, risk, latency, or memory may not dominate a more expensive one if a parent values that property.

Prove dominance componentwise under the transition model. Approximate pruning, beam limits, and capped frontiers turn an exact DP into an approximation or heuristic unless a quality theorem survives.

### Preserve executable state evidence

The teaching implementation below uses state $(i,b)$ and returns value, used weight, and identities under deterministic ties. Caching is only an execution convenience here; ALGE-024 compares evaluation strategies.

<!-- bijux-verify: {"id":"knapsack-state-sufficiency","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"items=(('A', 3, 4), ('B', 4, 5), ('C', 2, 3), ('D', 3, 7)) capacity=6\nvalue=11 weight=6 selected=('A', 'D')\nstates=18 hits=3 misses=18\nfeasible=True matches_bruteforce=True\n","stderr":""}} -->
~~~python
from functools import cache
from itertools import combinations


items = (
    ("A", 3, 4),
    ("B", 4, 5),
    ("C", 2, 3),
    ("D", 3, 7),
)
capacity = 6


def better(left, right):
    if left[0] != right[0]:
        return left if left[0] > right[0] else right
    if left[1] != right[1]:
        return left if left[1] < right[1] else right
    return left if left[2] < right[2] else right


@cache
def solve(index, remaining):
    if index == len(items):
        return 0, 0, ()
    best = solve(index + 1, remaining)
    identity, weight, value = items[index]
    if weight <= remaining:
        child_value, child_weight, child_ids = solve(index + 1, remaining - weight)
        take = value + child_value, weight + child_weight, (identity,) + child_ids
        best = better(best, take)
    return best


def brute_force():
    best = 0, 0, ()
    for count in range(len(items) + 1):
        for chosen in combinations(items, count):
            weight = sum(item[1] for item in chosen)
            if weight <= capacity:
                candidate = (
                    sum(item[2] for item in chosen),
                    weight,
                    tuple(item[0] for item in chosen),
                )
                best = better(best, candidate)
    return best


result = solve(0, capacity)
info = solve.cache_info()
value, weight, selected = result
print(f"items={items} capacity={capacity}")
print(f"value={value} weight={weight} selected={selected}")
print(f"states={info.currsize} hits={info.hits} misses={info.misses}")
print(f"feasible={weight <= capacity} matches_bruteforce={result == brute_force()}")
~~~

The finite run does not prove pseudopolynomial allocation safety, arbitrary numeric behavior, recursion-depth safety, or that $(i,b)$ is sufficient after changing the problem's constraints.

### Validate state meaning, not only final value

Use four layers of tests:

1. **state collision tests:** generate histories mapping to one key and compare legal continuations and incremental costs;
2. **recurrence tests:** enumerate first/last decisions and compare each state with an independent brute-force subproblem solver;
3. **graph tests:** verify transition legality, strict rank progress, reachable counts, and terminal coverage;
4. **witness tests:** replay reconstructed actions and recompute feasibility, objective, identities, and ties.

Include empty inputs, zero and exact budgets, unreachable targets, all ties, negative values where admitted, maximum indices, overflow boundaries, sparse reachable regions, and exponential-state rejection. Metamorphic tests can add a dominated option, permute stable identities, translate all costs, or append irrelevant suffixes when the model predicts invariance.

Instrumentation should expose states created/evaluated, cache hits only when evaluating by memoization, transitions considered, impossible transitions, frontier widths, dominance deletions, parent bytes, reconstruction length, and peak storage. An unexpectedly high collision or state count often identifies a design error before it appears in final answers.

## Definitions and Notation

- $h$: a partial decision history.
- $\phi(h)$: state-key function mapping histories to future-equivalence classes.
- $s$: one canonical state.
- $\mathcal S_R$: states reachable from the requested initial state.
- $A(s)$: legal actions from $s$.
- $\tau(s,a)$: successor state after action $a$.
- $c(s,a)$: immediate objective contribution.
- $V(s)$: optimal additional value from state $s$.
- $F$: set of terminal states.
- $r(s)$: rank used to prove acyclic dependencies.
- $i,j$: positions, endpoints, or prefix lengths as declared.
- $b,B$: remaining resource and initial numeric budget.
- $S$: a visited subset in subset DP.
- $q\in Q$: finite automaton or mode state.
- $\bot$: impossible or unreachable tagged value.
- $\preceq$: dominance relation whose direction and coordinates are declared.

State sufficiency is semantic: equal keys imply identical future behavior. State reachability is operational: a semantically valid state may never arise from the selected initial instance. Pseudopolynomial means polynomial in numeric magnitudes but not necessarily in their encoded bit length.

## Mechanisms, Invariants, or Proof Structure

Use this state-design worksheet.

1. **History model.** Define decisions, accumulated contribution, and complete-solution feasibility.
2. **Future dependence.** List every history property that can change future actions or incremental cost.
3. **Candidate key.** Encode those properties canonically and omit additive prefix objective.
4. **Collision challenge.** Seek equal keys with different continuation languages or values.
5. **State sentence.** Define exactly what $V(s)$ optimizes and what remains unresolved.
6. **Action partition.** Enumerate disjoint or deliberately overlapping first/last-decision classes covering every feasible completion.
7. **Transitions.** Prove successor keys represent precisely the residual problems.
8. **Bases and impossibility.** Cover empty, exhausted, exact-resource, invalid, and unreachable boundaries.
9. **Rank.** Prove every dependency decreases a well-founded measure or follows a topological order.
10. **Recurrence proof.** Prove branch soundness, completeness, and replacement of nonoptimal child completions.
11. **State count.** Bound reachable keys, key representation, and input-dependent numeric ranges.
12. **Transition count.** Bound fan-out and nonconstant transition work.
13. **Witness contract.** Define action metadata, ties, and replay validation.
14. **Compression.** Prove rolling storage, dominance, symmetry, or frontier deletion preserves every needed dependency and witness.
15. **Independent evidence.** Exhaust small histories/states, compare with a separate oracle, inspect graph counters, and enforce resource limits.

For edit distance, action partition is the last edit and rank is $i+j$. For interval DP, action is final split and rank is interval length. For subset-endpoint DP, action is predecessor endpoint and rank is subset cardinality. For product-state DP, the automaton coordinate proves omitted prefix text affects the future only through mode $q$.

## Alternatives and Trade-Offs

- **Small state versus sufficient state:** fewer coordinates reduce memory; omitting one future-relevant coordinate invalidates reuse.
- **History key versus quotient state:** full history is obviously sufficient; canonical future equivalence can collapse exponentially many histories.
- **Dense table versus sparse map:** arrays give compact predictable lookup; maps store reachable states but add key/hash/allocation cost.
- **Resource-indexed versus value-indexed DP:** either may be smaller depending on numeric bounds; both can be pseudopolynomial.
- **Scalar best versus Pareto frontier:** one value is compact; multiple future-relevant resources require nondominated alternatives.
- **Forward versus backward semantics:** either can be correct; bases, action contribution, reconstruction, and rank must align.
- **Prefix versus suffix state:** choose the direction that makes transitions local and dependencies acyclic.
- **Value only versus parents:** values minimize storage; parents simplify deterministic witness recovery.
- **Store versus recompute witnesses:** stored choices use memory; recomputation uses time and must reproduce ties exactly.
- **Exact versus pruned frontier:** exact retention preserves optimum; caps and beams require an approximation theorem or heuristic label.
- **DP versus greedy:** greedy needs a safe irreversible choice; DP retains alternatives distinguished by state.
- **DP versus divide and conquer:** DP exploits overlapping state identities; independent child instances may need no table.
- **DP versus shortest-path formulation:** state DAG paths can clarify correctness; generic graph materialization may cost more than implicit transitions.

## Failure Modes and Misconceptions

1. **Cache-first thinking:** memoization is chosen before subproblem semantics exist.
2. **Position-only state:** resource, endpoint, mode, or constraint history is missing.
3. **Whole-history state:** no overlapping histories merge, so exponential search remains.
4. **Subset-only tour:** transition cost is undefined without current endpoint.
5. **Value-only planner:** order, distribution, risk, or memory needed by parents is discarded.
6. **Recurrence-before-sentence:** symbols lack an exact unresolved-problem meaning.
7. **Incomplete action partition:** a legal first/last decision is absent.
8. **Unsound branch:** a transition constructs an infeasible completion.
9. **Double-counted prefix:** accumulated contribution appears both in key/value and transition cost.
10. **Wrong empty base:** optional and exact-fill variants are silently conflated.
11. **Winning infinity:** sentinel arithmetic overflows into a competitive value.
12. **Dependency cycle:** a transition does not decrease rank.
13. **Topological mismatch:** a table cell is read before its dependencies are valid.
14. **Magnitude blindness:** $O(nB)$ is called polynomial in binary input length.
15. **Untrusted allocation:** capacity or dimension product creates an enormous table.
16. **Rectangular fiction:** unreachable cells are counted as executed—or sparse overhead is ignored.
17. **Free transition:** subset iteration, hashing, copying, or split scanning disappears from cost.
18. **Unsafe dominance:** equal scalar value hides different future resource or property quality.
19. **Unproved symmetry:** merged identities have different costs or witness requirements.
20. **Tie drift:** value evaluation and witness traversal select different equal branches.
21. **Local indices:** reconstructed child coordinates are not translated to global identities.
22. **Count overflow:** number of optimal solutions exceeds its numeric representation.
23. **Floating equality:** approximate costs make state comparisons nontransitive or platform-dependent.
24. **Oracle echo:** tests reproduce the same recurrence rather than enumerate independent solutions.
25. **Final-value-only test:** illegal transitions or wrong parents happen to yield the right objective.
26. **Silent heuristic:** frontier caps or beams remove exactness without changing the claim.

## Worked Examples

### Example 1

**Question:** Why is knapsack state $i$ alone insufficient?

**Reasoning:** Two histories can reach the same next item $i$ with remaining capacities 0 and 5. An item of weight 3 is illegal from the first and legal from the second.

**Conclusion:** Remaining capacity is future-relevant; fixed-order 0/1 knapsack needs at least $(i,b)$ under this formulation.

### Example 2

**Question:** How many rectangular states does knapsack have for $n=100$ and $B=1000$?

**Reasoning:** There are $101$ item boundaries and $1001$ capacities:

$$
(100+1)(1000+1)=101{,}101.
$$

**Conclusion:** Constant-action evaluation is $O(nB)$, a pseudopolynomial rather than bit-polynomial bound.

### Example 3

**Question:** What edit distance recurrence branch applies when final characters match?

**Reasoning:** For prefixes ending in the same character, diagonal transition adds zero. Deletion and insertion remain legal competitors if costs allow, but the diagonal candidate is $D(i-1,j-1)$.

**Conclusion:** State $(i,j)$ plus the fixed strings makes the final-operation partition local.

### Example 4

**Question:** Why can affine gap alignment need an extra mode?

**Reasoning:** Extending an existing gap can cost differently from opening one. Prefix indices $(i,j)$ do not reveal whether the preceding action is inside a gap.

**Conclusion:** Add modes such as match, gap-in-$x$, and gap-in-$y$, or use equivalent multiple value tables.

### Example 5

**Question:** How many split candidates does matrix-chain state $(i,j)$ have?

**Reasoning:** Every $k$ with $i\le k<j$ is a possible final multiplication split, so there are $j-i$ transitions.

**Conclusion:** $\Theta(n^2)$ intervals times $O(n)$ splits yields $\Theta(n^3)$ direct work.

### Example 6

**Question:** Why does traveling-salesperson state need endpoint $j$ in addition to subset $S$?

**Reasoning:** Two paths visiting the same cities but ending at different cities pay different costs to the next city. Subset alone cannot price the transition.

**Conclusion:** $(S,j)$ is the standard sufficient state, with exponential state count despite history merging.

### Example 7

**Question:** A binary-string constraint forbids substring `11`. What compact state suffices while scanning positions?

**Reasoning:** Future legality needs only whether the previous bit was 1. An automaton has states `previous-zero-or-start` and `previous-one`.

**Conclusion:** Position times two automaton modes replaces storing the full prefix.

### Example 8

**Question:** What rank proves unit edit-distance dependencies acyclic?

**Reasoning:** Each predecessor decreases $i$, $j$, or both, so $r(i,j)=i+j$ strictly decreases.

**Conclusion:** Increasing $i+j$, row/column order, or top-down recursion all respect the same DAG.

### Example 9

**Question:** Can a lower-cost partial route dominate every higher-cost route at the same vertex?

**Reasoning:** Not if routes retain different remaining fuel or risk budgets. A higher current cost with more remaining resource may enable the only feasible completion.

**Conclusion:** Dominance must compare every future-relevant coordinate, not the scalar objective alone.

### Example 10

**Question:** What does the executable prove for capacity six?

**Reasoning:** It evaluates 18 distinct $(i,b)$ states, observes three repeated calls, returns value 11 with weight 6 and identities $(A,D)$, and agrees with an independent subset enumeration.

**Conclusion:** This is finite correspondence evidence for the chosen state and ties, not a universal proof or production capacity bound.

## Cross-Program Connections

- [Theory of Computation & Complexity](../../15-theory-of-computation-and-complexity/ROADMAP.md) owns state-space lower bounds, encoded input length, exponential algorithms, automata, and exactness.
- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) owns dense/sparse tables, bitsets, persistent parents, Pareto containers, and state-key representation.
- [Database Engineering](../../18-database-engineering/ROADMAP.md) owns property-aware query-plan states, memo groups, dominance, and reconstruction of physical plans.
- [Programming Languages & Semantics](../../01-programming-languages-and-semantics/ROADMAP.md) owns recursion, numeric/sentinel types, hashing/equality, ownership, exceptions, and deterministic values.
- [Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) owns independent oracles, state collision generation, metamorphic testing, instrumentation, and resource regression.
- [Computer Architecture](../../23-computer-architecture/ROADMAP.md) owns table layout, locality, bandwidth, vectorization, and sparse-versus-dense physical cost.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) owns untrusted magnitude allocation, state-space exhaustion, numeric overflow, and adversarial transition fan-out.

## References

1. Richard Bellman. [“On the Theory of Dynamic Programming”](https://doi.org/10.1073/pnas.38.8.716), *Proceedings of the National Academy of Sciences* 38(8), 1952, pp. 716–719. Primary dynamic-programming formulation.
2. Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein. [*Introduction to Algorithms*, fourth edition](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/), MIT Press, 2022. State recurrences, optimal substructure, reconstruction, and complexity foundations.
3. Robert A. Wagner and Michael J. Fischer. [“The String-to-String Correction Problem”](https://doi.org/10.1145/321796.321811), *Journal of the ACM* 21(1), 1974, pp. 168–173. Primary edit-distance dynamic programming result.
4. Saul B. Needleman and Christian D. Wunsch. [“A General Method Applicable to the Search for Similarities in the Amino Acid Sequence of Two Proteins”](https://doi.org/10.1016/0022-2836%2870%2990057-4), *Journal of Molecular Biology* 48(3), 1970, pp. 443–453. Primary global sequence-alignment dynamic programming method.
5. Michael Held and Richard M. Karp. [“A Dynamic Programming Approach to Sequencing Problems”](https://doi.org/10.1137/0110015), *Journal of the Society for Industrial and Applied Mathematics* 10(1), 1962, pp. 196–210. Primary subset-state sequencing and traveling-salesperson work.
6. Jon Kleinberg and Éva Tardos. [*Algorithm Design*](https://www.pearson.com/en-us/subject-catalog/p/algorithm-design/P200000003259), Addison-Wesley, 2005. Weighted interval scheduling, sequence alignment, knapsack, and state-design patterns.
7. ACM, IEEE Computer Society, and AAAI. [*Computer Science Curricula 2023: Algorithmic Foundations*](https://csed.acm.org/al-cs-core/), endorsed 2024; consulted 2026-09-04. Current curricular scope for dynamic programming, correctness, complexity, and optimization.

## Exercises

### Exercise 1

For items $A=(weight 2,value 3)$, $B=(3,4)$, $C=(4,8)$, $D=(5,8)$ and capacity 7, define $V(i,b)$ precisely, write bases and recurrence, compute the optimal value and deterministic witness under ties “lower weight, then lexicographic identities,” and explain why $i$ and $b$ are both necessary.

### Exercise 2

Derive unit-cost edit distance state and recurrence for transforming `kitten` into `sitting`. Compute the distance, provide one edit script, prove the final-operation recurrence, give state/transition bounds, and state how affine gap cost changes the state.

### Exercise 3

For matrix dimensions $(10,30,5,60)$, compute both parenthesizations of $A_1A_2A_3$, fill the needed interval values, choose the optimum, and prove the interval recurrence. Include overflow and reconstruction requirements.

### Exercise 4

Define Held–Karp state $H(S,j)$ for a four-city directed setting, including base and final tour closure. Derive state and transition bounds, explain why subset alone fails, and state representation limits for bitmasks and unreachable edges.

### Exercise 5

Design an exact dynamic program for choosing a length-$m$ string over an alphabet with position-dependent rewards while forbidding a supplied finite set of patterns. Specify automaton-product state, recurrence, bases, rank, impossible states, ties, witness reconstruction, complexity, input/resource validation, exhaustive tests, and how frontier capping changes the claim.

## Answers to the Exercises

### Answer 1

Let $V(i,b)$ be the maximum additional value obtainable from items $i,\ldots,3$, each at most once, with remaining integer capacity $b$. Define $V(4,b)=0$ for $0\le b\le7$. For item $(w_i,v_i)$,

$$
V(i,b)=
\begin{cases}
V(i+1,b), & w_i>b,\\
\max\{V(i+1,b),v_i+V(i+1,b-w_i)\}, & w_i\le b.
\end{cases}
$$

Feasible combinations within capacity seven include $A+B$ with value 7, $A+C$ with value 11 and weight 6, and $A+D$ with value 11 and weight 7. $B+C$ has value 12 and weight 7, which is optimal. Thus the witness is $(B,C)$.

Every completion either excludes or includes current item $i$; inclusion moves to $i+1$ and subtracts its weight. Those classes are exhaustive and feasible branches construct legal subsets. Replacing a branch's suffix by a better solution of the same $(i+1,b')$ preserves item availability and capacity, proving optimal substructure.

Index alone merges different remaining capacities. Capacity alone merges histories with different remaining item identities and can permit reuse. The pair is sufficient for a fixed ordered item list. Deterministic comparison is maximum value, then lower used weight, then lexicographic identities; parent metadata must use the same order.

### Answer 2

Let $D(i,j)$ be the minimum edits converting `kitten` prefix length $i$ to `sitting` prefix length $j$. Bases are $D(0,j)=j$ insertions and $D(i,0)=i$ deletions. For positive indices,

$$
D(i,j)=\min\left{
D(i-1,j)+1,
D(i,j-1)+1,
D(i-1,j-1)+[x_{i-1}\ne y_{j-1}]
\right}.
$$

The distance is 3. One script substitutes `s` for initial `k`, substitutes `i` for `e`, and inserts final `g`, producing `sitting`.

Every nonempty edit script ends with deletion, insertion, match, or substitution. Removing that final operation leaves exactly the corresponding predecessor-prefix problem. Conversely, appending the operation to any predecessor script produces a valid script, proving soundness and completeness. A nonoptimal predecessor could be replaced without changing prefixes or final operation.

There are $(|x|+1)(|y|+1)=O(|x||y|)$ states and at most three transitions per interior state, hence $O(|x||y|)$ work in the direct model. Full values use $O(|x||y|)$ space; evaluation-specific compression belongs to ALGE-024.

Affine gaps distinguish opening from extension. Use modes for match/substitution, gap in $x$, and gap in $y$—equivalently three tables per $(i,j)$—with transitions that charge open or extend appropriately.

### Answer 3

Matrices have shapes $10\times30$, $30\times5$, and $5\times60$. The two parenthesizations cost

$$
(A_1A_2)A_3:
10\cdot30\cdot5+10\cdot5\cdot60
=1500+3000=4500,
$$

$$
A_1(A_2A_3):
30\cdot5\cdot60+10\cdot30\cdot60
=9000+18000=27000.
$$

Bases are $M(i,i)=0$. Thus $M(1,2)=1500$, $M(2,3)=9000$, and

$$
M(1,3)=\min\{M(1,1)+M(2,3)+10\cdot30\cdot60,
M(1,2)+M(3,3)+10\cdot5\cdot60\}=4500.
$$

For interval $(i,j)$, every full parenthesization has a unique final split $k$. Its left and right expressions solve $(i,k)$ and $(k+1,j)$. Replacing either with a cheaper parenthesization preserves boundary dimensions and improves total cost. Minimizing all $k$ is therefore sound and complete.

Compute dimension products in checked widened arithmetic before addition; overflow can select a false minimum. Store the winning $k$ with a deterministic tie rule, then recursively reconstruct, validating interval boundaries.

### Answer 4

Fix start city 0. For $S\subseteq V$ with $0,j\in S$, let $H(S,j)$ be minimum cost of a path starting at 0, visiting every city in $S$ exactly once, and ending at $j$. Base is

$$
H(\{0\},0)=0,
$$

with other invalid bases unreachable. For $j\ne0$,

$$
H(S,j)=\min_{i\in S\setminus\{j\}}
\left(H(S\setminus\{j\},i)+d_{ij}\right).
$$

The tour cost is

$$
\min_{j\ne0}\left(H(V,j)+d_{j0}\right).
$$

Subset alone cannot price the next edge because paths over the same $S$ can end at different cities. There are $O(n2^n)$ subset-endpoint states and up to $O(n)$ predecessor transitions, for $O(n^22^n)$ direct work and $O(n2^n)$ values.

For four cities, use masks containing bit zero and an endpoint bit. Validate $n$ before shifting or allocating; a machine-word mask only represents a bounded number of cities. Use tagged unreachable values for absent directed edges and guard addition. Store predecessor endpoints for reconstruction and verify the final cycle visits every identity once.

### Answer 5

Build a deterministic finite automaton whose state $q$ records the longest suffix of the current prefix that is also a prefix of a forbidden pattern; transition to a rejecting sink when a pattern completes. Let $Q_{\mathrm{safe}}$ exclude that sink.

Define $V(i,q)$ as maximum additional reward for positions $i,\ldots,m-1$ given current safe automaton state $q$. Base is $V(m,q)=0$ for safe $q$. For $i<m$,

$$
V(i,q)=
\max_{a:\delta(q,a)\in Q_{\mathrm{safe}}}
\left(reward(i,a)+V(i+1,\delta(q,a))\right).
$$

If no symbol is legal, return tagged impossible. Rank $m-i$ decreases on every edge. The automaton state is sufficient because it recognizes exactly which future symbol strings complete a forbidden pattern; the full prefix has no other effect under additive position rewards.

Use a total tie rule such as maximum reward then lexicographically smallest output. Store the chosen symbol per state or recompare values with exactly that rule. Replay the witness through the automaton and recompute its reward.

There are at most $(m+1)|Q_{\mathrm{safe}}|$ states and $|\Sigma|$ transitions per nonterminal state, giving $O(m|Q||\Sigma|)$ direct work and $O(m|Q|)$ full value/parent storage. Count automaton construction separately in total pattern length.

Validate alphabet, pattern encodings, empty forbidden patterns, $m$, reward dimensions, numeric overflow, state/table byte multiplication, and resource limits before allocation. Exhaust short alphabets, lengths, and pattern sets; enumerate every string as an independent oracle. Check state collisions by grouping prefixes with the same $q$ and comparing legal suffixes, plus impossible cases, all ties, extreme rewards, witness replay, and deterministic input ordering.

Capping states, keeping a beam, or pruning nondominated-looking modes without a proof can remove the optimum. Label that implementation heuristic, or provide a separate approximation bound; do not retain the exact claim merely because bounded tests pass.
