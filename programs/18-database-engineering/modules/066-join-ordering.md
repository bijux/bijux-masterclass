---
module_id: DBE-066
program: Database Engineering
level: 2
module_number: 66
title: Join Ordering
status: complete
last_verified: 2026-08-30
---

# Join Ordering

## One-Page Review

### Governing question

How can an optimizer search the legally equivalent join-plan space, retain the alternatives whose properties may matter later, and choose a robust order before exact intermediate cardinalities and runtime conditions are known?

### Essential definitions

A **join graph** has relation occurrences as vertices and join predicates as edges; a **join hypergraph** permits predicates or semantic constraints involving multiple vertex sets. A **join tree** is a binary decomposition of the join. A **left-deep** tree repeatedly adds a base relation on one side; a **bushy** tree can join two composite subplans. A **connected subplan** has applicable predicates linking its parts. A **Cartesian product** joins disconnected parts. A **memo group** represents logically equivalent expressions. An **interesting property**—order, distribution, locality, parameterization, rewindability—can justify retaining a locally costlier subplan. **Dynamic programming (DP)** stores the best subplans for subsets and property classes. **Greedy** search makes a locally preferred extension. **Randomized**, **beam**, and **learned** methods restrict or guide search. **Plan regret** is the realized loss relative to a reference alternative.

### Central model, mechanism, or theorem

For each legal relation subset S and required property p, retain the least-cost known plan `Best[S,p]`. Construct S from legal connected splits `(A,B)` with `A union B=S`, cost both child property requests, physical join implementations, and enforcers, then keep non-dominated alternatives. Bellman's principle applies only when the state key contains every future-relevant property. Exact subset DP is exponential in relation count but can avoid enumerating duplicate syntax trees; graph-aware connected-subgraph/complement-pair enumeration avoids many Cartesian candidates. Search budgets trade planning time for plan quality.

### Critical invariants

- Relation occurrences, not merely table names, identify vertices; aliases, lateral dependencies, parameters, and repeated references remain distinct.
- Every rewrite is proven legal for join kind, predicate placement, null introduction/rejection, duplicate multiplicity, correlation, volatility, security barriers, and required output.
- Inner equijoins may often commute and associate; outer, semi, anti, mark, temporal, lateral, and non-equi joins require explicit legality rules.
- A memo key includes logical subset/expression plus all properties and parameter bindings relevant to future cost or legality.
- Cross products are excluded only under an explicit policy; disconnected query graphs or globally beneficial Cartesian steps still need a legal path.
- Cardinality and cost estimates are versioned inputs, not facts; uncertainty near a ranking boundary is observable.
- Search timeout, candidate coverage, pruning reason, incumbent, deterministic seed, fallback, and chosen plan are reproducible.

### Common failures

Failures include reordering an outer join as if it were inner; identifying a self-join by base table rather than alias; pushing an ON predicate into WHERE across null extension; keeping one cheapest subset plan while discarding useful order/distribution; using greedy “smallest first” as a proof; banning every Cartesian product; assuming final cardinality distinguishes orders; multiplying plan counts without stating tree/commutativity/algorithm restrictions; comparing enumeration algorithms under different cost/cardinality models; evaluating only optimizer-chosen plans; using nondeterministic search without seed/evidence; or improving estimated cost while increasing runtime regret.

### Compact example

Four relations form a chain A–B–C–D. Base rows are 30, 1,000, 1,000, 30; edge selectivities are 0.1, 0.1, and 0.0001. A deterministic greedy rule starts at tied-smallest A and produces intermediate rows 30, 3,000, 300,000, 900, with cumulative modeled cost 303,930. Exact connected left-deep DP finds D–C–B–A with 30, 3, 300, 900 and cost 1,233—about 246.50 times smaller—although both final estimates are 900. The executable proves this finite model, not universal DP superiority.

### Connections

Retrieve [Cardinality Estimation](064-cardinality-estimation.md), [Cost Models](065-cost-models.md), [Joins and Join Semantics](012-joins-and-join-semantics.md), and [Logical and Physical Plans](051-logical-and-physical-plans.md). Continue through [the roadmap](../ROADMAP.md) to access-path selection, plan caching, adaptive processing, and plan diagnosis.

## Governing Question

SQL states a result, not a binary execution tree. For n join participants, the optimizer must decide which subsets to combine, in which orientation, with which physical algorithms, access paths, distributions, and materialization boundaries. Many trees are semantically equivalent for inner joins yet differ by orders of magnitude in intermediate work; other apparently plausible reorderings are incorrect. How can search be complete enough to find a good plan, bounded enough to finish planning, and honest about uncertainty?

Join ordering is not sorting table names by size. A filtered billion-row fact can become tiny; a small dimension can multiply duplicates; an index lookup needs parameters from an outer relation; an early merge may preserve an order that avoids a later sort; a distributed order may avoid terabytes of movement. The correct state combines logical membership, semantic constraints, physical properties, access paths, cardinalities, costs, and resource context.

The optimizer is solving a constrained, partially observed combinatorial problem. “Optimal” always means optimal within the generated legal candidates, cost model, estimates, property system, resource assumptions, and search budget. Production evidence must expose those qualifiers.

## Why This Matters

Join order controls intermediate cardinality, repeated probes, hash-build size, memory and spill, sort work, pipeline startup, vectorization, remote calls, partition elimination, exchange bytes, skew, and parallel critical paths. Bad early intermediates can dominate the query even when final output is small. The compact counterexample ends at 900 rows under both orders, yet one order materializes an estimated 300,000-row intermediate while the other peaks at 900.

System R established dynamic-programming access-path and join-order selection while preserving interesting orders. Cascades generalized equivalence groups, required physical properties, enforcers, memoization, and guided search. Moerkotte and Neumann's DPhyp work models predicates and non-inner-join constraints as a hypergraph and enumerates connected subgraphs/complements efficiently. These foundations explain why a serious join enumerator is a semantics-and-properties engine, not just a permutation generator.

Search itself consumes latency and memory. Current PostgreSQL 18 documentation describes exhaustive planning for smaller joins, a genetic search beyond a configurable threshold, and explicit JOIN/collapse controls that trade search freedom for planning time. Current SQLite documentation describes its bounded N-nearest-neighbors search and star-query heuristic. These products make different choices because enumeration is workload- and architecture-dependent.

Failures are consequential in production: parameter skew can flip the best order; stale statistics can inflate a build; a broadcast can multiply memory; an outer-join legality bug can corrupt results; a random search seed can destabilize plans; and a new enumerator can increase planning time for every query while helping only rare large joins. Evaluation must therefore cover semantics, candidate reachability, estimate sensitivity, planning resources, selected-plan regret, and workload outcomes.

## Prerequisites and Retrieval

You should understand SQL bag/null semantics, inner/outer/semi/anti joins, logical versus physical plans, statistics/cardinality, cost models, access paths, sorting, hashing, indexing, and distributed exchanges.

Retrieve: relation occurrence; join predicate; hyperedge; connected component; legal split; left-deep/right-deep/bushy tree; commutativity/associativity; null introduction/rejection; lateral/parameter dependency; memo group; property class; enforcer; interesting order; subset DP; connected-subgraph/complement pair; incumbent/upper bound; dominance; branch-and-bound; beam/greedy/randomized/genetic search; planning budget; plan regret; uncertainty; stability; and fallback.

## Learning Objectives

After this module, you can:

1. construct a join graph/hypergraph from bound relation occurrences and predicates;
2. prove or reject reorderings under inner, outer, semi, anti, lateral, and volatile semantics;
3. distinguish left-deep, right-deep, and bushy plan spaces and their execution consequences;
4. derive subset-DP recurrence and state requirements;
5. explain connected-subgraph enumeration, duplicate avoidance, and Cartesian policy;
6. integrate join algorithms, access paths, physical properties, and distribution into enumeration;
7. compare exact DP, top-down memo, greedy, beam, randomized, genetic, and learned guidance;
8. quantify sensitivity to cardinality, cost, parameters, and resource conditions;
9. design semantic, search-coverage, planning-cost, regret, and workload evaluations; and
10. deploy enumeration changes with deterministic evidence, canaries, observability, and rollback.

## Core Exposition

**Bind the problem exactly.** Create one vertex per relation occurrence after name resolution, view/CTE policy, predicate normalization, and security boundaries. `orders o1` and `orders o2` are different vertices. Record base filters, projected columns, keys/constraints, parameter producers, required outputs, row goals, and physical placement. Each edge/hyperedge binds the exact expression, join kind, null/equality semantics, residuals, and prerequisites.

A binary inner predicate between A and B is an ordinary edge. A predicate referencing A, B, and C is naturally a hyperedge whose evaluability requires all referenced vertices. LATERAL/correlated inputs induce direction: the parameter producer must be available before the consumer. Outer/semi/anti joins introduce semantic regions and preserved sides. The hypergraph is therefore more than a visualization; it is a compact legality interface.

**Separate equivalence from implementation.** For compatible inner joins, commutativity gives `A join B = B join A` and associativity gives `(A join B) join C = A join (B join C)` under the same conjunctive semantics and bag/null treatment. This does not mean every predicate can be evaluated at every node. Apply each predicate at the earliest legal boundary or retain it as a residual without changing truth conditions.

Outer joins are not generally commutative or associative because they introduce null-extended rows. Moving a predicate between ON and WHERE can turn preservation into rejection. Semi and anti joins expose only one side and have duplicate/existence behavior unlike inner joins. FULL JOIN, lateral dependencies, volatile functions, user-defined semantics, temporal/as-of joins, security barriers, and error-observable expressions further constrain transformations. Use proven rules with side conditions; never infer legality from similar-looking columns.

**Describe tree spaces.** A left-deep tree joins the current composite with one base participant, enabling pipelined nested loops and outer-parameter index probes. A right-deep tree can support build/probe pipelines in some hash implementations. A bushy tree joins composites, allowing independent branches, parallelism, early reduction on both sides, and better distributed placement. Bushy search is larger and its candidates may demand materialization or extra memory. “More complete” is not automatically operationally better if planning cost or executor capability dominates.

Even counting requires a convention: labeled relations or not; ordered children or commutative equivalence; all binary trees or left-deep only; algorithm/orientation/access-path/property choices included or not. State the space rather than quoting one factorial/Catalan number as universal.

**Subset dynamic programming.** For an inner-join component, initialize base plans for each singleton subset and property class. For increasing subset sizes, consider legal partitions `A union B=S`, `A intersection B=empty`, with an applicable crossing predicate or explicit Cartesian permission. Combine retained child plans using supported physical joins and property requests. Add local join/enforcer cost to child cumulative cost and retain the best or Pareto-nondominated plan per state.

The recurrence is conceptually `Best[S,p] = min Combine(Best[A,pA], Best[B,pB], join, enforcers -> p)`. It is valid only if the state contains every future-relevant fact. Keeping one cheapest plan per relation subset loses an ordered, partitioned, parameterized, rewindable, low-memory, or fast-start alternative that a parent may prefer. System R's interesting orders and Cascades property requests address exactly this issue.

**Avoid duplicate and disconnected work.** Naive subset partitioning revisits symmetric splits and many disconnected subsets. Canonical orientation avoids `(A,B)` and `(B,A)` duplication when semantically/physically equivalent. Graph-aware DP enumerates connected subgraphs and connected complements rather than all partitions. DPhyp extends this reasoning to hyperedges and non-inner joins. Still, “avoid Cartesian products” is a heuristic, not a semantic law: disconnected query components require them, and unusual cost structures can make an intermediate Cartesian product beneficial. Make the exception explicit and bounded.

The executable enumerates a finite connected left-deep space. Its cost is sum of estimated rows after each prefix, including the singleton. Edge selectivities multiply when a newly added relation crosses multiple already joined vertices. This is deliberately simpler than a production cardinality/cost model.

<!-- bijux-verify: {"id":"connected-join-order-dp","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"relations=4\nconnected_left_deep_orders=8\ngreedy_order=A-B-C-D\ngreedy_intermediates=30,3000,300000,900\ngreedy_cost=303930\ndp_order=D-C-B-A\ndp_intermediates=30,3,300,900\ndp_cost=1233\ncost_ratio=246.50\nfinal_rows_equal=true\ncartesian_prefixes_rejected=true\nevidence=finite_left_deep_enumeration\n","stderr":""}} -->
```python
from itertools import permutations

relations = ("A", "B", "C", "D")
base_rows = {"A": 30, "B": 1000, "C": 1000, "D": 30}
selectivity = {("A", "B"): 0.1, ("B", "C"): 0.1, ("C", "D"): 0.0001}


def edge(left, right):
    return selectivity.get(tuple(sorted((left, right))))


def evaluate(order):
    joined = {order[0]}
    rows = float(base_rows[order[0]])
    cost = rows
    intermediates = [rows]
    for relation in order[1:]:
        crossing = [edge(relation, prior) for prior in joined if edge(relation, prior) is not None]
        if not crossing:
            return None
        rows *= base_rows[relation]
        for factor in crossing:
            rows *= factor
        cost += rows
        intermediates.append(rows)
        joined.add(relation)
    return cost, intermediates


valid = []
for order in permutations(relations):
    result = evaluate(order)
    if result is not None:
        valid.append((result[0], order, result[1]))

greedy = [min(relations, key=lambda relation: (base_rows[relation], relation))]
while len(greedy) < len(relations):
    candidates = []
    for relation in relations:
        if relation in greedy:
            continue
        result = evaluate(tuple(greedy + [relation]))
        if result is not None:
            candidates.append((result[1][-1], relation))
    greedy.append(min(candidates)[1])

greedy_cost, greedy_rows = evaluate(tuple(greedy))
dp_cost, dp_order, dp_rows = min(valid)
render = lambda values: ",".join(str(round(value)) for value in values)

print(f"relations={len(relations)}")
print(f"connected_left_deep_orders={len(valid)}")
print(f"greedy_order={'-'.join(greedy)}")
print(f"greedy_intermediates={render(greedy_rows)}")
print(f"greedy_cost={round(greedy_cost)}")
print(f"dp_order={'-'.join(dp_order)}")
print(f"dp_intermediates={render(dp_rows)}")
print(f"dp_cost={round(dp_cost)}")
print(f"cost_ratio={greedy_cost / dp_cost:.2f}")
print(f"final_rows_equal={str(greedy_rows[-1] == dp_rows[-1]).lower()}")
print("cartesian_prefixes_rejected=true")
print("evidence=finite_left_deep_enumeration")
```

**Integrate algorithms and access paths.** Join order and join implementation are coupled. A nested loop can use a parameterized index only when its outer side supplies the key. Hash join orientation determines build memory. Merge join may exploit or deliver order. Batched lookup, memoization, runtime filters, vectorization, and index intersection alter local costs and properties. Enumerating logical orders first and assigning algorithms afterward can miss a plan whose value depends on that coupling.

**Retain physical properties.** Suppose `(A join B)` is cheapest as a hash join, but a merge/index alternative delivers the parent ORDER BY or distribution for joining C. Discarding it by subset alone destroys optimal substructure. Key memo entries by required/delivered properties or retain a bounded frontier. In distributed systems include hash/range/singleton/replicated placement, locality, partition keys, skew, and exchange enforcers. Orca demonstrates memoized optimization with order and distribution requests/enforcement.

**Top-down search and pruning.** Cascades-style search begins from a goal, explores transformations, implements expressions, and uses an incumbent cost bound. If partial cost plus a valid lower bound cannot beat the incumbent, prune. Lower bounds must be admissible for any completeness claim; heuristic promise/timeout pruning forfeits that claim and should record why candidates were skipped. Memoize results for the same group/property/context and avoid cycles/duplicate expressions.

**Bounded alternatives.** Greedy search is cheap but can make irreversible local mistakes, as the executable shows. Beam/N-nearest approaches keep several partial plans, trading memory/time for resilience; SQLite's current N3 documentation describes this design and a star-query heuristic. Randomized/genetic search explores large spaces without exhaustive DP; PostgreSQL's current GEQO exposes threshold, effort, pool, generations, selection bias, and seed. Deterministic seeds and repeated-seed distributions are evidence requirements, not cosmetic options.

Learned guidance can rank transformations, partial plans, or complete candidates, and reinforcement learning can reuse workload experience. It remains search guidance under a representation, training distribution, objective, and budget. OOD query graphs, schema changes, new operators, hardware drift, and feedback bias require detection and fallback. Simpler algorithms can be competitive on studied benchmarks; no method dominates every query graph and environment.

**Manage uncertainty.** Perturb base/filter/join cardinalities, widths, access costs, memory, network, and parameter classes. Identify whether the incumbent remains stable and where rankings cross. Retain a robust alternative if a small plausible error causes catastrophic spill, repeated lookup, or broadcast. Parameter-sensitive planning may produce multiple plan families; adaptive execution may defer a decision. These are not substitutes for correct enumeration but responses to missing compile-time facts.

**Diagnose the first decisive divergence.** Normalize old/new query, bindings, schema/statistics, parameters, configuration, search seed/budget, memo trace, and hardware/resource context. Compare legal candidate generation first: was the good order reachable? Then property/access-path/algorithm availability; cardinality; local cost; pruning; timeout; and tie-breaking. A wrong selected plan caused by a missing candidate is not fixed by retuning cost constants.

**Evaluate in layers.** Semantic tests exhaust small bags with duplicates, nulls, unmatched rows, aliases, and mixed join kinds against a trusted evaluator. Enumerator tests compare exact small cases with brute-force legal trees, verify no duplicates, and check property states. Planning tests measure candidate/memo counts, time, memory, timeout, determinism, and seed variance. Decision tests execute or faithfully simulate multiple candidates, report regret and catastrophic inversions, and separate cardinality/cost/enumeration. Workload tests measure end-to-end latency/tails, throughput, resources, plan churn, and fairness.

**Productionize safely.** Version legality rules, enumerator, cost/cardinality models, statistics, and configuration. Shadow old/new enumeration on identical inputs, retaining decisive traces without sensitive literals. Canary bounded fingerprints/tenants with semantic result checks, planning budgets, runtime/resource gates, a control cohort, kill switch, and rollback. Monitor planning time/memory, timeout/fallback rate, plan changes, spills, exchanges, OOMs, cancellations, tails, and workload interference. Do not claim better join ordering from estimated cost alone.

## Definitions and Notation

- **V, E/H**: relation-occurrence vertices and predicate edges/hyperedges.
- **S**: a legal joined subset of V.
- **CCP**: connected-subgraph/complement pair used to construct a connected join.
- **T(S,p)**: retained plan(s) for logical subset S and property class p.
- **Left-deep tree**: every join's designated inner/right child is a base relation under the convention.
- **Bushy tree**: at least one join combines two composite subplans.
- **Legal split**: partition whose combination preserves semantics and dependencies.
- **Interesting property**: non-final property worth retaining because a later operator may exploit it.
- **Incumbent**: cheapest complete/goal-satisfying plan found so far.
- **Admissible lower bound**: never exceeds the best possible completion cost from a partial state.
- **Search coverage**: declared candidate space and fraction/conditions explored.
- **Regret**: realized selected-plan objective minus realized reference-best objective.

Final inner-join cardinality can be order-independent under the same predicates while intermediate cardinalities and costs vary drastically. Enumeration therefore reasons about every boundary, not merely the root.

## Mechanisms, Invariants, or Proof Structure

**Inner-join equivalence.** Under a conjunction of compatible inner-join predicates, relational join is commutative and associative at the result-bag level when predicate bindings and expression behavior are preserved. This licenses alternative binary trees; it does not license premature evaluation of a predicate lacking inputs or movement across semantic barriers.

**DP induction.** Base states contain optimal feasible singleton plans for each property. Assume retained child states are optimal for all proper subsets/property requests. Any legal binary plan for S has a root split A,B and child properties. Enumerating that split, child states, implementation, and enforcers considers a plan no worse than it. Taking the minimum yields an optimal plan for S within the declared space. The proof fails if state keys omit a future-relevant property, legal split, implementation, or context.

**Greedy counterexample.** The executable's deterministic local choice selects A before the highly selective C–D edge can be exploited. Exact enumeration finds D–C first. Both orders apply the same three selectivities and finish at 900 rows, but cumulative intermediate-row cost differs by factor 246.50. Thus local minimum extension and final cardinality do not establish global minimum cumulative cost.

**Connectivity invariant.** Every prefix in the finite executable has at least one crossing predicate. This eliminates accidental Cartesian prefixes but not all legitimate Cartesian plans. For disconnected graphs, enumerate component plans then combine them under explicit product policy.

**Property sufficiency.** Bellman's principle permits discarding a subplan only when another plan dominates it for every future-relevant dimension under the same semantics/context. Lower scalar cost alone is insufficient when order, distribution, parameterization, rewindability, startup, memory, or risk differs.

**Evidence separation.** Brute-force small-space equivalence proves enumerator coverage only for that grammar; model scores prove internal choice under estimates; candidate execution supports regret for tested contexts; canaries support scoped operational claims. None proves universal plan optimality.

## Alternatives and Trade-Offs

**Exact subset DP** gives an optimum within a precisely modeled space and is easy to oracle-check on small joins; exponential state growth limits large queries. **Graph-aware DP/DPhyp** avoids irrelevant disconnected partitions and handles richer predicates/constraints; implementation and legality machinery are sophisticated.

**Top-down memo/branch-and-bound** can find good incumbents early and prune with bounds, integrates naturally with properties/rules, and supports anytime behavior; search order and bound quality strongly affect work. **Greedy** is deterministic and cheap; local mistakes can be extreme. **Beam/N3** retains several prefixes and has predictable bounds; the right width is workload-dependent and can miss late-payoff plans.

**Randomized/genetic** search scales to large spaces and can escape greedy traps; quality varies by effort/seed and optimality is not assured. **Learned guidance** amortizes workload patterns and can prioritize promising regions; it introduces training coverage, drift, inference, privacy, and fallback obligations. **Rule/hint-constrained ordering** reduces planning time and repairs known queries; it can freeze a plan against future data/parameter changes.

**Left-deep restriction** favors pipelining and parameterized access and reduces search. **Bushy search** enables independent reduction, parallelism, and placement choices but expands states and executor demands. **Cartesian avoidance** is effective on connected selective graphs; hard prohibition is incomplete for disconnected or exceptional cost cases.

**Single best plan** minimizes storage and simplifies caching. **Property/robustness frontiers** preserve valuable alternatives and parameter classes but increase planning/cache complexity. The frontier dimensions must correspond to real future choices, or state explosion gains nothing.

## Failure Modes and Misconceptions

1. “Inner joins are always freely reorderable” ignores volatility, correlation, barriers, and predicate bindings.
2. “Outer joins can be treated like inner joins after estimation” confuses semantics with cost.
3. “Smallest base table first is optimal” ignores filtering, selectivity, fanout, access paths, and later properties.
4. “The smallest next intermediate gives the best whole order” is refuted by the executable.
5. “Same final rows means same plan quality” ignores intermediate work and physical effects.
6. “One best plan per subset is sufficient” omits interesting properties and parameterization.
7. “All cross products are bad” makes disconnected graphs incomplete and misses rare beneficial plans.
8. “Exhaustive permutations equal exhaustive plans” omits trees, orientations, algorithms, access paths, and properties.
9. “Bushy is always better” ignores planning size, materialization, memory, and executor limits.
10. “Timeout returns the best plan” returns the best discovered plan, not necessarily the space optimum.
11. “A fixed random seed proves heuristic quality” proves reproducibility for one trajectory only.
12. “Learned search removes estimation” still depends on features, labels, objective, and environment.
13. “Lower estimated cost proves improvement” ignores candidate execution, regret, and model error.
14. “A manual hint fixes the optimizer” may mask statistics, legality, search, property, or cost defects and age badly.

## Worked Examples

### Example 1

**Three-way inner equivalence.** For A–B and B–C predicates, `(A join B) join C` and `A join (B join C)` apply the same conjunction when expression bindings are preserved. A–C first has no predicate and introduces a product. Conclusion: equivalence permits all legal trees, while connectivity prioritizes predicate-bearing splits.

### Example 2

**Outer-join barrier.** `A LEFT JOIN B ON p` preserves unmatched A. Applying a null-rejecting B predicate in WHERE removes those rows, whereas placing it in ON preserves A with null extension. Conclusion: predicate placement and null introduction constrain reassociation.

### Example 3

**Self-join identity.** `employee manager` and `employee report` reference the same base table but play different roles and predicates. Collapsing both to one vertex corrupts bindings and cardinalities. Conclusion: enumerate relation occurrences/aliases, not catalog identities.

### Example 4

**Greedy trap.** A–B–C–D has base rows 30/1000/1000/30 and selectivities .1/.1/.0001. Greedy A–B–C–D costs 303,930; DP D–C–B–A costs 1,233. Conclusion: a locally smallest extension can conceal a much stronger later reduction.

### Example 5

**Interesting order.** Hash `(A join B)` costs 100; merge costs 120 and delivers order k. If the parent otherwise sorts for 80, totals are 180 versus 120. Conclusion: discard by `(subset,cost)` and the global optimum disappears; retain the order property.

### Example 6

**Parameterized access.** Customer filter emits 10 IDs; joining orders second enables ten index probes. Reversing the outer/inner role may scan all orders. Conclusion: orientation and access path belong inside ordering state.

### Example 7

**Disconnected graph.** Query components `{A,B}` and `{C,D}` each have predicates but no edge between components. A final Cartesian combination is semantically required. Conclusion: avoid unnecessary products inside components, then explicitly combine components.

### Example 8

**Bushy distribution.** `(A join B)` and `(C join D)` can reduce independently on collocated partitions before one exchange; a left-deep order may repeatedly move growing intermediates. But concurrent hash builds can exceed memory. Conclusion: bushy value depends on distribution, concurrency, and memory properties.

### Example 9

**Heuristic reproducibility.** GEQO-like search returns costs 100, 130, and 400 under three seeds at the same effort. Reporting only the best seed is selection bias. Conclusion: retain seed, coverage/effort, distribution, timeout, incumbent, and fallback.

### Example 10

**Production regression.** A new enumerator picks a 20% cheaper estimate but runtime p99 triples for large tenants. Trace shows the prior broadcast alternative was pruned before tenant-specific width/skew costing. Restore candidate reachability, shadow parameter classes, and canary resource outcomes. Conclusion: repair the first search divergence and validate regret, not merely weights.

## Cross-Program Connections

- [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md): dynamic programming, graph/hypergraph enumeration, pruning, approximation, and complexity govern search.
- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md): bitsets, memo tables, DAGs, priority queues, hash-consing, and Pareto frontiers implement enumeration.
- [Data Engineering](../../19-data-engineering/ROADMAP.md): star/snowflake schemas, partitions, file statistics, and skew shape join graphs and placement.
- [Large-Scale Data Systems Engineering](../../21-large-scale-data-systems-engineering/ROADMAP.md): broadcast, repartition, locality, parallelism, elasticity, and failures enlarge the property space.
- [Software Engineering: Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md): exhaustive small oracles, differential tests, deterministic replay, and canary gates establish evidence.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md): planning budgets, workload isolation, observability, configuration rollout, and rollback operationalize enumerators.
- [Security Engineering](../../25-security-engineering/ROADMAP.md): security barriers, literal/plan privacy, tenant isolation, model poisoning, and diagnostic access constrain search tooling.

## References

1. P. Griffiths Selinger et al., [“Access Path Selection in a Relational Database Management System”](https://doi.org/10.1145/582095.582099), *SIGMOD 1979*. Primary dynamic-programming access-path/join-order and interesting-order foundation.
2. Goetz Graefe, [“The Cascades Framework for Query Optimization”](https://15721.courses.cs.cmu.edu/spring2019/papers/22-optimizer1/graefe-ieee1995.pdf), *IEEE Data Engineering Bulletin* 18(3), 1995. Primary memo, property, enforcer, cost-bound, and guided-search framework.
3. Guido Moerkotte and Thomas Neumann, [“Dynamic Programming Strikes Back”](https://15721.courses.cs.cmu.edu/spring2020/papers/20-optimizer2/p539-moerkotte.pdf), *SIGMOD 2008*. Primary DPhyp hypergraph and connected-subgraph enumeration for complex predicates/non-inner joins.
4. PostgreSQL Global Development Group, [PostgreSQL 18: Controlling the Planner with Explicit `JOIN` Clauses](https://www.postgresql.org/docs/18/explicit-joins.html), retrieved 2026-08-30. Current reordering freedom, outer-join constraints, collapse controls, and planning/runtime trade-off.
5. PostgreSQL Global Development Group, [PostgreSQL 18: Query Planning](https://www.postgresql.org/docs/18/runtime-config-query.html), retrieved 2026-08-30. Current GEQO threshold, effort, population, generations, bias, and seed controls.
6. SQLite Project, [The Next-Generation Query Planner](https://www.sqlite.org/queryplanner-ng.html), retrieved 2026-08-30. Current N3 bounded search, dependency graph, star-query heuristic, and plan-stability discussion.
7. SQLite Project, [The SQLite Query Optimizer Overview](https://www.sqlite.org/optoverview.html), retrieved 2026-08-30. Current nested-loop join ordering, inner/outer/CROSS JOIN behavior, and manual controls.
8. Viktor Leis et al., [“How Good Are Query Optimizers, Really?”](https://vldb.org/pvldb/vol9/p204-leis.pdf), *PVLDB* 9(3), 2015. Primary Join Order Benchmark and controlled cardinality/cost/enumeration analysis.
9. Mohamed A. Soliman et al., [“Orca: A Modular Query Optimizer Architecture for Big Data”](https://15721.courses.cs.cmu.edu/spring2018/papers/15-optimizer1/p337-soliman.pdf), *SIGMOD 2014*. Primary distributed memo, properties, enforcers, stages, and parallel optimizer architecture.
10. Justin Jaffray, [“An Introduction to Join Ordering”](https://www.cockroachlabs.com/blog/join-ordering-pt1/), Cockroach Labs, 2018, retrieved 2026-08-30. Official engineering exposition of join graphs, plan space, and cross-product nuance.
11. Ankur Dutt et al., [“Simpli-Squared: A Very Simple Yet Unexpectedly Powerful Join Ordering Algorithm without Cardinality Estimates”](https://arxiv.org/abs/2111.00163), 2021. Primary statistics-free heuristic evaluated on the Join Order Benchmark.
12. Sanjay Krishnan et al., [“Learning to Optimize Join Queries With Deep Reinforcement Learning”](https://arxiv.org/abs/1808.03196), 2018. Primary learned join-search guidance and evaluation.

## Exercises

### Exercise 1

For `A JOIN B ON p LEFT JOIN C ON q`, construct vertices/edges and state which reorderings require additional proof. Include a null-rejecting predicate on C in ON versus WHERE.

### Exercise 2

Derive the subset-DP recurrence and prove its optimality within a declared inner-join/property space. Identify one omitted state dimension that invalidates the proof.

### Exercise 3

Recompute the executable's greedy and DP costs, enumerate all valid connected left-deep orders, and explain why identical final rows do not imply identical cost.

### Exercise 4

Compare exact graph-aware DP, top-down memo/branch-and-bound, greedy, beam/N3, genetic, and learned guidance for a 25-way distributed join. Define selection and fallback policy.

### Exercise 5

Design an elite join-enumerator verification and rollout system covering semantics, exact small-space coverage, properties, uncertainty, planning resources, regret, multitenancy, privacy, canaries, and rollback.

## Answers to the Exercises

### Answer 1

Use occurrence vertices A, B, C; p connects A/B and q binds the preserved `(A join B)` side to nullable C. A and B may commute/associate under p only if expression behavior and all dependencies permit it. Moving C below/through the inner join requires an outer-join associativity rule with preserved-side, predicate-reference, null-rejection, key/match, and multiplicity side conditions; do not assume it. `LEFT JOIN C ON (q AND C.flag=1)` retains unmatched left rows and null-extends C. Applying `WHERE C.flag=1` afterward rejects null-extended rows and can make the result inner-like for that predicate. They are not interchangeable. Record q's earliest legal boundary, C's null introduction, any later null rejection, aliases, lateral/volatile/security constraints, and verify candidate results over duplicates, null keys, multiple matches, and unmatched rows.

### Answer 2

For each legal subset S and required property p, initialize feasible singleton physical plans. For every canonical legal split A,B of larger S, every compatible child property pair, physical join implementation/orientation, and necessary enforcer producing p, compute `cost(T[A,pA])+cost(T[B,pB])+local/enforcer cost`; retain the least or nondominated plan. Induct on subset size: any plan for S has a root split and child property requests. By the induction hypothesis the retained children are no worse than that plan's children; enumerating the same root choice constructs a no-worse candidate, so the minimum is optimal within the declared space. Omit delivered order, for example, and a locally costlier ordered child may avoid a parent sort; the retained unordered child no longer dominates it, so the induction premise fails. Distribution, parameterization, startup/total, memory/risk, and resource context can fail similarly.

### Answer 3

Greedy begins with tied-smallest A=30, then only connected B: `30*1000*.1=3000`; then C: `3000*1000*.1=300000`; then D: `300000*30*.0001=900`. Including singleton, cost is `30+3000+300000+900=303930`. D–C gives `30*1000*.0001=3`; add B gives `3*1000*.1=300`; add A gives `300*30*.1=900`; cost `30+3+300+900=1233`; ratio is about 246.50. The eight connected left-deep orders are A-B-C-D, B-A-C-D, B-C-A-D, B-C-D-A, C-B-A-D, C-B-D-A, C-D-B-A, and D-C-B-A. All apply base products and the same three selectivities, so final estimate is 900; their prefixes differ, changing CPU, memory, spill, access, and cumulative cost.

### Answer 4

Exact graph-aware DP gives a reference when each component/property state remains within budget, but 25-way properties/distributions can explode. Top-down memo can use a fast incumbent and valid bounds, retaining exactness only where pruning/budget conditions justify it. Greedy supplies a deterministic emergency plan; beam/N3 retains diverse prefixes at a bounded width; genetic/randomized search explores beyond the beam with recorded seed/effort; learned guidance may prioritize transformations only when query graph/operator/schema/environment is within coverage. Split semantic regions first; optimize small/connected components exactly; retain distribution/order/parameter/memory frontiers; set time/memory/candidate budgets; use top-down/beam for the remainder; optionally run reproducible multi-seed or learned guidance inside the budget. Always return the best legal incumbent, with fallback to conservative deterministic order if no covered model or candidate exists. Shadow exact solutions on smaller sampled subproblems and report coverage, timeout, seed variance, planning cost, candidate regret, exchanges/spills, and tenant/resource outcomes.

### Answer 5

Define a canonical bound query/hypergraph grammar and legality matrix for inner/outer/full/semi/anti/lateral/correlated joins, volatile/error/security barriers, bags, nulls, aliases, and predicates. Exhaustively generate small databases and legal trees; compare results with a trusted evaluator, brute-force enumeration, and a duplicate-free canonical oracle. Verify memo keys include properties/parameters/context, enforcers satisfy requirements, pruning bounds are valid where completeness is claimed, disconnected components remain solvable, and deterministic traces bind versions/seeds/budgets. Perturb estimates, widths, memory, network, workers, and parameter classes; measure candidate reachability, pairwise order, regret, catastrophic spill/broadcast, planning time/memory, timeout/fallback, and seed distributions. Replay representative and adversarial workloads, execute safe alternatives, and separate cardinality, cost, enumeration, and runtime causes. Least-privilege/redact query literals and tenant metadata; isolate learned/feedback labels and defend poisoning. Shadow old/new on identical inputs, then canary bounded fingerprints/tenants with result checks, control cohort, SLO/resource/fairness gates, kill switch, immutable versions, and rollback. Evidence supports only declared grammars, candidates, versions, workloads, environments, and budgets; it does not prove universal semantic coverage, global optimality, representative performance, privacy, fairness, or deployment fitness, and external review requires named humans.
