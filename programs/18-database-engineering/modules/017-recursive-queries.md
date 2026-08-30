---
module_id: DBE-017
program: Database Engineering
level: 1
module_number: 17
title: Recursive Queries
status: complete
last_verified: 2026-08-30
---

# Recursive Queries

## One-Page Review

### Governing question

How can SQL derive a finite, auditable transitive result from an anchor and a self-referential expansion without confusing iteration order, path multiplicity, cycle safety, termination, or resource limits?

### Essential definitions

An **anchor term** seeds a recursive common table expression (CTE). A **recursive term** joins the current working relation to base data and emits the next frontier. A **frontier** contains rows to expand in one conceptual iteration; the **accumulated result** contains accepted rows so far. A **fixed point** is reached when expansion adds no new accepted rows. A **path** is an ordered sequence of vertices or edges; **reachability** asks only whether a vertex can be reached. A **cycle** revisits a tracked identity on a path. `UNION` applies whole-row duplicate elimination, while `UNION ALL` preserves every generated occurrence.

### Central model, mechanism, or theorem

Let anchor relation be `A`, expansion operator be `E`, and `T(X)=A union E(X)`. If the row domain is finite, `T` is monotone, and duplicate elimination admits each state at most once, iterative evaluation from the empty set reaches the least fixed point. But SQL rows may include depth, path, cost, or timestamps, so revisiting the same vertex can still produce a distinct row and defeat whole-row `UNION` termination. With `UNION ALL`, termination instead needs a well-founded measure, explicit bound, cycle guard, or an independently finite acyclic domain.

### Critical invariants

- Anchor and recursive arms expose the same positional schema, types, units, and null meanings.
- The recursive transition states exactly what one expansion step means.
- Termination follows from a written proof, not a friendly fixture or outer `LIMIT`.
- Cycle identity is defined over the correct vertex or composite state and checked before re-expansion.
- Reachable vertices, walks, simple paths, shortest paths, and aggregate quantities are not interchangeable.
- `UNION` versus `UNION ALL` follows the desired multiplicity and cycle policy.
- Traversal/evaluation order is not presentation order; final output has an explicit total `ORDER BY`.
- Depth, row, path-width, time, memory, spill, and cancellation budgets are enforced and observed.

### Common failures

Failures include a missing or nonshrinking termination predicate, using `UNION` while a changing depth/path column prevents deduplication, using `UNION ALL` on cyclic data without a guard, tracking the wrong cycle key, counting paths when only nodes were intended, multiplying bill-of-material quantities through duplicate relationships, relying on incidental breadth-first output, truncating recursive text or numeric values because the anchor fixed a narrow type, filtering after expansion instead of before it, accepting an outer `LIMIT` as a portable safety mechanism, and exposing unrestricted user-selected roots or depths.

### Compact example

Edges `A→B`, `A→C`, `B→D`, `C→D`, `C→E`, `D→B`, `E→F` contain cycle `B→D→B`. From A, reachable vertices are A through F. There are two simple paths to B and D, so path enumeration legitimately repeats their vertices. A path-local visited tuple rejects `A,B,D,B` and `A,C,D,B,D` as cycles. Minimum depths are A:0, B/C:1, D/E:2, F:3. A global visited set would answer reachability but erase alternate simple paths.

### Connections

[DBE-014](014-subqueries-and-common-table-expressions.md) defines CTE scope and materialization cautions. [DBE-016](016-set-operations.md) supplies bag and duplicate-elimination laws. Later DBE modules cover plans, indexes, statistics, memory, spill, transactions, and distributed execution. Algorithm and Data Structures Engineering provide graph traversal, shortest paths, topological order, and complexity proofs.

## Governing Question

Recursive SQL expresses repeated relational expansion in one statement: descendants in a hierarchy, parts within parts, graph reachability, dependency closure, date or integer series, organizational ancestry, and path enumeration. The surface syntax resembles mathematical recursion, but common engines execute it iteratively with working and intermediate relations. Correctness depends on the state represented by each row and on when that state is admitted, expanded, deduplicated, or rejected.

The central engineering question has three layers. First, what relation is being computed: vertices, edges, paths, walks, costs, or quantities? Second, why must evaluation stop on every permitted input? Third, what resources can it consume before stopping? A finite-looking result on a tree fixture does not prove behavior on a directed cyclic multigraph with duplicate edges, self-loops, nulls, skew, or an adversarial root.

## Why This Matters

Recursive-query defects can be subtle or operationally severe. A hierarchy query that assumes a tree can duplicate descendants in a DAG. A cycle can run until an engine recursion cap or statement timeout. Adding a depth column makes every revisit distinct, so switching from `UNION ALL` to `UNION` may not stop anything. A bill-of-materials calculation can overflow or double-count shared components. A permissions closure can leak access if tenant predicates are absent from one expansion step.

Even terminating queries can exhaust resources. A graph with branching factor `b` and depth `d` can enumerate on the order of `b^d` paths. Path arrays grow with depth and increase comparison, memory, and temporary I/O. Duplicate elimination retains visited row state. One highly connected root can dominate a database worker. Correct production design requires semantic bounds, database-enforced limits, statement deadlines, cancellation, workload isolation, and observed plans.

Recursive output also tempts ordering myths. A working-table implementation may appear breadth-first, but SQL does not grant a presentation order without final ordering, and PostgreSQL explicitly separates computed search-order columns from actual visit order. Applications must not infer parent-before-child or shortest-first behavior from an incidental plan.

## Prerequisites and Retrieval

Retrieve relations and bags, set union, least fixed points, monotone functions, induction, directed graphs, trees and DAGs, paths and walks, cycles, breadth-first and depth-first search, keys, joins, null and equality, numeric bounds, type coercion, sorting, hashing, indexes, query plans, memory/spill, transactions, authorization, and cancellation.

Distinguish recursive specification from iterative execution; anchor from frontier; frontier from accumulated result; node identity from path identity; duplicate edge from alternate path; reachability from enumeration; cycle prevention from depth limiting; logical search order from evaluation order from final display order; and termination proof from emergency resource guard.

## Learning Objectives

After this module, you should be able to:

1. state anchor, recursive transition, row schema, and fixed-point meaning;
2. trace working and accumulated relations iteration by iteration;
3. prove termination using finiteness, a decreasing measure, or explicit bounds;
4. choose `UNION` or `UNION ALL` from desired state and multiplicity;
5. design path-local and global cycle strategies for the intended question;
6. distinguish reachability, walk/path enumeration, shortest depth, and quantity propagation;
7. produce deterministic depth-first or breadth-first presentation keys without assuming evaluation order;
8. control anchor/recursive type resolution, nulls, overflow, and path width;
9. enforce tenant, root, depth, row, time, and resource budgets; and
10. validate live results, plans, estimates, memory, spill, cancellation, and upgrade behavior.

## Core Exposition

A recursive CTE generally names output columns, gives a nonrecursive anchor, combines it with a recursive term using `UNION ALL` or `UNION`, and then consumes the resulting relation. Only the recursive term refers to the CTE itself. Dialects impose different restrictions on self-reference count, aggregation, windows, ordering, limits, and placement; portable principles do not imply portable syntax.

Conceptually, evaluate the anchor, accept its rows into both the result and a working relation, then repeatedly apply the recursive term to the current working rows. Accepted new rows become the next working relation. Evaluation stops when the next frontier is empty. PostgreSQL documents this working/intermediate-table model and notes that the mechanism is iterative even though the query is written recursively.

The row schema is an inductive invariant. Anchor and recursive arms must have compatible column counts and types, but compatibility is weaker than intent. Name the columns and cast the anchor deliberately: vertex ID, parent ID, depth type, path representation, quantity/cost type, cycle flag, tenant, and provenance. MySQL documents recursive CTE column types as determined by the nonrecursive part, so a narrow anchor string can cause later path values to fail or truncate depending on behavior; explicit adequate casts are essential. Other engines have their own resolution rules.

An anchor selects roots. It must include the same authorization, tenant, validity interval, snapshot, and deletion policy expected throughout expansion. A root supplied by a user is not safe merely because later joins are tenant-scoped; validate root ownership. Multiple roots can cause legitimate convergence on one node, and a root duplicated by the anchor produces duplicate traversals under `UNION ALL`.

The recursive transition encodes one step. For edges `(src,dst)`, a forward reachability step joins frontier vertex `v` to edges where `src=v` and emits `dst`. Reverse ancestry joins on `dst=v` and emits `src`. Reversing the condition can still return plausible rows in symmetric fixtures, so tests need asymmetric graphs. Predicates governing tenant, edge kind, validity, or status belong in every relevant step.

For pure reachability over a finite vertex set, state can be just vertex identity (and tenant if identity is scoped). `UNION` can reject vertices already accumulated, allowing a monotone least-fixed-point computation to terminate after at most the number of admissible vertices. This relies on whole-row equality matching the intended state. Add depth or path to the row, and repeated visits may no longer be duplicates.

`UNION ALL` preserves every generated occurrence. It is appropriate for an acyclic tree with one path per node, for deliberate path enumeration with cycle guards, or for quantity propagation where multiplicity has meaning. It can explode on DAGs because a node is reached along many paths, and it does not prevent cycles. Choosing it solely for speed is a semantic error.

Whole-row `UNION` is not a universal cycle detector. Suppose rows are `(vertex,depth)`. Cycle `B→D→B` generates `(B,1)`, `(D,2)`, `(B,3)`, `(D,4)`, all distinct. A path column makes distinctions even stronger. Cycle policy must track the identity whose repetition is forbidden, often vertex ID within the current path, rather than rely on complete output-row deduplication.

A path-local visited set prevents a vertex from repeating on one path and therefore enumerates simple paths. It still permits another path to reach the same vertex. This is correct for route enumeration but can be exponential; a finite graph can have exponentially many simple paths. The cycle key may be composite, such as `(tenant,node)` or `(node,state)`. Tracking too little rejects valid state transitions; tracking too much fails to detect the dangerous cycle.

A global visited relation accepts each vertex/state once and answers reachability efficiently, but recursive SQL support for explicit anti-joining against all prior results varies. Duplicate-eliminating recursion can provide this behavior when the CTE row is exactly the visited state. It discards alternate paths and cannot directly preserve all provenance. Separate the closure relation from path-evidence extraction when both are needed.

Depth limiting bounds iterations, not necessarily rows. With branching factor ten and depth eight, path occurrences can approach one hundred million before duplicates/cycles. A depth cap is an emergency and product constraint, not proof that the result is semantically complete. State whether depth counts vertices or edges, whether root depth is zero or one, and whether the bound is inclusive.

Row limits and statement timeouts provide additional containment. SQLite documents a recursive-term `LIMIT` that bounds rows added to its recursive table. PostgreSQL warns that relying on a parent `LIMIT` to stop a loop is implementation-dependent and can fail when the parent sorts or joins. MySQL exposes a configurable recursive CTE depth limit. Design to terminate independently, then enforce dialect-supported depth/row/time/resource guards as defense in depth.

Search order has three meanings. Evaluation order is an implementation choice. A breadth-first presentation key can be `(depth,path_or_tie_key)`; a depth-first key can be the full path. Standard-style `SEARCH` syntax is supported by some engines, including PostgreSQL, while SQLite documents recursive `ORDER BY` controls with engine-specific queue behavior. In every case, use a final `ORDER BY` on an explicit key for promised output order.

Breadth-first traversal over an unweighted graph is often associated with shortest edge count, but SQL results cannot claim first-seen shortest merely from incidental evaluation order. Compute minimum depth by grouping all bounded/cycle-safe path results, or use an engine/design with a proven breadth-first state acceptance rule. Weighted shortest paths require algorithms beyond naive recursive enumeration; negative edges and cycles add further constraints.

Depth-first path arrays are useful for presentation and cycle detection. Their element type must represent the full identity, and array/string serialization must avoid delimiter ambiguity. Composite keys need composite path elements, not concatenated text. Path width grows linearly with depth, and comparing/copying paths adds cost. Do not return internal authorization-sensitive paths to callers without a disclosure review.

Trees, DAGs, cyclic graphs, and multigraphs have different multiplicity. In a tree, one parent path reaches each node. In a DAG, shared descendants have several paths. In a multigraph, duplicate edges may represent separate relationships or ingestion duplicates. Decide whether results count nodes, distinct edges, paths, or relationship occurrences before aggregating. `DISTINCT` cannot repair an unspecified identity model.

Hierarchical bill-of-materials queries propagate quantity. If parent P requires three A and each A requires two B, that path contributes six B. Shared components require summing contributions across intended paths; duplicate source edges can double counts. Numeric type must withstand products and sums, units must align, cycles must be prohibited or governed, and independent rollups must reconcile. A cycle in a parts explosion is usually a data-integrity defect, not a path to ignore silently.

Organizational ancestry and access-control closure require temporal and tenant semantics. Manager relationships may be versioned; mixing edges from different effective times invents paths that never existed. Permission inheritance can have deny/override rules that are not monotone set union. Recursive SQL is safe only after the algebra of grant, deny, scope, and precedence is stated. Never infer authorization from reachability alone when policy composition is richer.

Recursive series generation needs a well-founded arithmetic measure. `n+1 WHERE n<bound` terminates for ordinary exact integers when start and bound are valid, but overflow, null bounds, negative steps, and floating increments can break reasoning. Validate direction, nonzero step, inclusive endpoint, maximum cardinality, and type bounds. Prefer native series/calendar facilities when supported and governed.

Null identity and edges need explicit policy. A null `src` or `dst` does not join under ordinary equality, so it may silently disconnect a graph. Null may mean missing data rather than a real vertex. Reject invalid edges through constraints or use a documented null-safe identity only if the domain truly includes a null-like vertex. Cycle path membership with null also follows dialect-specific semantics.

Aggregation inside recursive terms is restricted differently by engines and is hard to reason about because it acts on a frontier rather than necessarily the complete result. When a final quantity or minimum can be computed after a safe path/closure enumeration, prefer an outer aggregation. When dynamic programming is required, define state, monotonicity, dominance/pruning, and engine legality precisely; a recursive CTE is not automatically an efficient graph algorithm.

Termination proof should name a finite state space or a ranking function. For duplicate-eliminated reachability, each iteration adds at least one previously unseen admissible vertex or stops, so at most `|V|` successful additions occur. For integer series, remaining distance decreases by a positive step. For simple paths, path length increases while no vertex repeats, so length is at most `|V|`; output count can still be exponential. A cap without completeness reasoning is only containment.

Correctness can be proved inductively. Base: every anchor row represents a valid zero-step or root result. Step: assuming frontier rows represent valid paths/states, the recursive join adds exactly one permitted edge/transition and preserves schema, tenant, path, quantity, and bound invariants. Completeness: every desired finite path/state can be decomposed into a shorter desired prefix plus one permitted transition. Cycle filtering changes completeness intentionally to simple paths or visited states.

Physical plans typically repeatedly join working rows to base tables. Index the edge lookup direction and scope, for example `(tenant_id,src)` for forward traversal, while measuring write/storage cost. Estimate errors compound across levels. Capture loops/iterations where exposed, actual rows per level, frontier width, duplicate rejection, memory, temporary I/O, index access, join method, skew, and total latency.

Recursive queries need workload controls: permitted roots, maximum depth and rows, statement deadline, memory/temp quotas, concurrency limit, cancellation propagation, read-only role, and result-size limit. Observability should record normalized query/version, root class, snapshot, actual depth, rows per depth, cycles, truncation reason, time, memory/spill, and cancellation. Do not log sensitive full paths indiscriminately.

Concurrency affects the graph snapshot. One statement may see a consistent database-defined snapshot, but repeated pages or multiple recursive statements can see different edges depending on isolation. A hierarchy export needs an as-of contract and stable final order. If a graph changes faster than recursive reads can tolerate, use versioned edges or a materialized closure with explicit refresh and correction semantics.

Materialized transitive closure, closure tables, nested sets, materialized paths, and graph services trade write complexity for read behavior. Closure tables make reachability fast but updates can affect many pairs and require transactional maintenance. Materialized paths simplify subtree prefix reads but complicate moves and escaping. Recursive CTEs are flexible and current with the source snapshot, but per-query work can be unbounded without controls.

Testing starts with empty graph, root-only, chain, branching tree, diamond DAG, self-loop, multi-node cycle, duplicate edge, multiple roots, disconnected component, null endpoint, composite tenant key, maximum depth, path explosion, numeric overflow, and concurrent version cases. Derive frontiers and accepted rows by hand or an independent model. Then execute the exact target dialect, verify final sorted rows, and capture plan/resource evidence.

## Definitions and Notation

For vertex domain `V`, edge relation `E subseteq V×V`, anchors `A subseteq V`, and state relation `X`:

- `expand(X)={v | exists u in X: (u,v) in E}` for reachability state;
- `T(X)=A union expand(X)` is monotone under set inclusion;
- the least fixed point is `lfp(T)=union_{i>=0} T^i(empty)` when iteration stabilizes;
- a walk may repeat vertices/edges; a path here means a vertex-simple path unless stated otherwise;
- `depth(path)=|path|-1` counts edges from the root;
- a ranking function maps recursive states to a well-founded order and strictly decreases on every permitted transition.

SQL bag multiplicity, null equality, row types, and dialect evaluation rules refine this abstract set model and must be reviewed separately.

## Mechanisms, Invariants, or Proof Structure

A recursive-query review should:

1. name the desired relation—reachability, paths, ancestry, quantities, series, or another state;
2. specify anchor, one-step transition, positional schema, types, scope, and snapshot;
3. trace working/frontier and accumulated rows on an asymmetric adversarial fixture;
4. choose `UNION`/`UNION ALL` and cycle identity from desired multiplicity;
5. prove termination and separately define depth, row, time, memory, and output guards;
6. prove soundness by anchor/step induction and completeness for the bounded desired relation;
7. define search presentation keys and apply a final total order without assuming evaluation order;
8. verify null, duplicate-edge, DAG, cycle, overflow, truncation, and composite-key cases;
9. protect every anchor/transition with tenant, authorization, validity, and provenance rules; and
10. inspect actual iterations, rows per depth, estimates, indexes, memory, spill, skew, cancellation, concurrency, and upgrades.

The finite model below enumerates vertex-simple paths breadth-first from A, records rejected cycle-closing paths, then derives reachable vertices, minimum depths, and per-vertex simple-path counts. Its explicit queue order is part of this Python oracle, not a claim about SQL evaluation order.

<!-- bijux-verify: {"id":"finite-recursive-graph","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"breadth_first_rows=(('A', 0, ('A',)), ('B', 1, ('A', 'B')), ('C', 1, ('A', 'C')), ('D', 2, ('A', 'B', 'D')), ('D', 2, ('A', 'C', 'D')), ('E', 2, ('A', 'C', 'E')), ('B', 3, ('A', 'C', 'D', 'B')), ('F', 3, ('A', 'C', 'E', 'F')))\ncycle_paths=(('A', 'B', 'D', 'B'), ('A', 'C', 'D', 'B', 'D'))\nreachable_nodes=('A', 'B', 'C', 'D', 'E', 'F')\nminimum_depths=(('A', 0), ('B', 1), ('C', 1), ('D', 2), ('E', 2), ('F', 3))\npath_counts=(('A', 1), ('B', 2), ('C', 1), ('D', 2), ('E', 1), ('F', 1))\nedge_expansions=9\n","stderr":""}} -->
```python
from collections import Counter, deque

edges = (
    ("A", "B"),
    ("A", "C"),
    ("B", "D"),
    ("C", "D"),
    ("C", "E"),
    ("D", "B"),
    ("E", "F"),
)

children = {node: [] for edge in edges for node in edge}
for source, target in edges:
    children[source].append(target)
for targets in children.values():
    targets.sort()

queue = deque([("A", ("A",))])
rows = []
cycle_paths = []
edge_expansions = 0
while queue:
    node, path = queue.popleft()
    rows.append((node, len(path) - 1, path))
    for child in children[node]:
        edge_expansions += 1
        candidate = path + (child,)
        if child in path:
            cycle_paths.append(candidate)
        else:
            queue.append((child, candidate))

reachable = tuple(sorted({node for node, _, _ in rows}))
minimum_depths = tuple((node, min(depth for candidate, depth, _ in rows if candidate == node)) for node in reachable)
counts = Counter(node for node, _, _ in rows)
path_counts = tuple((node, counts[node]) for node in reachable)

print(f"breadth_first_rows={tuple(rows)}")
print(f"cycle_paths={tuple(cycle_paths)}")
print(f"reachable_nodes={reachable}")
print(f"minimum_depths={minimum_depths}")
print(f"path_counts={path_counts}")
print(f"edge_expansions={edge_expansions}")
```

Python tuple/list equality, queue order, integers, and dictionary behavior are not SQL type, null, collation, working-table, or plan semantics. The model omits duplicate edges, tenants, temporal versions, authorization, numeric propagation, database recursion limits, memory, spill, concurrency, and distributed execution.

## Alternatives and Trade-Offs

Recursive CTEs are flexible, statement-scoped, and operate on current relational data, but compute expansion per request and expose dialect restrictions. Closure tables make reachability and ancestor reads fast, but inserts/deletes/moves require transactional maintenance and can amplify writes. Materialized paths support subtree prefix access but need encoding and costly moves. Nested-set intervals make subtree reads simple for mostly static trees but are awkward under change and do not generalize naturally to DAGs.

A specialized graph engine can provide optimized traversals and path algorithms, but introduces another authority, consistency model, query language, and operational system. Application traversal offers precise budgets and algorithms but can incur many database round trips unless edges are fetched in batches. Materialized recursive results improve repeated reads but require refresh, invalidation, lineage, and staleness contracts.

## Failure Modes and Misconceptions

- “Recursive SQL calls itself on the stack.” Common engines document iterative working-relation evaluation.
- “`UNION` always stops cycles.” Changing depth or path fields makes revisits distinct.
- “A depth limit proves termination correctness.” It bounds one dimension and may silently truncate valid results.
- “No repeated nodes means low cost.” A DAG can contain exponentially many simple paths.
- “First row found is shortest.” Evaluation order is not a portable result contract.
- “Breadth-first-looking output is ordered.” Only a final explicit total `ORDER BY` guarantees presentation.
- “A tree fixture validates graph code.” Diamonds, self-loops, cycles, duplicate edges, and multiple roots change multiplicity.
- “Compatible recursive columns are safe.” Anchor-derived widths, numeric bounds, units, and null meanings can still fail.
- “Outer `LIMIT` is a termination guard.” Parent operations or other engines may demand the full recursive result.
- “Reachability proves permission.” Policy may include deny, precedence, time, tenant, and condition semantics.

## Worked Examples

### Example 1

Anchor 1 and transition `n+1` while `n<5` produce frontiers `{1}`, `{2}`, `{3}`, `{4}`, `{5}`, then empty. Termination follows because integer distance `5-n` strictly decreases while nonnegative. Validate start, step, bound, overflow, and expected cardinality before generalizing.

### Example 2

Chain `A→B→C` gives anchor A at depth zero, then B at one and C at two. Soundness follows by adding one real edge per step; completeness follows by decomposing each reachable chain prefix. Final `ORDER BY depth,path_key` supplies presentation order.

### Example 3

Diamond `A→B`, `A→C`, `B→D`, `C→D` reaches D twice under path enumeration but once under vertex reachability. Counting recursive rows as distinct descendants overcounts D. State whether the measure is nodes or paths before selecting `ALL` or deduplication.

### Example 4

Cycle `B→D→B` with rows `(vertex,depth)` generates distinct depths forever under whole-row `UNION`. A path-local membership check rejects a child already in the path. A global vertex closure is smaller but intentionally discards alternate paths.

### Example 5

A composite vertex `(tenant_id,node_id)` cannot use `node_id` alone for cycle detection if IDs repeat across tenants. Every anchor and edge join also carries tenant equality. The root is authorized before recursion, and tenant remains in internal rows even if presentation omits it.

### Example 6

Part P uses three A; A uses two B. The P→A→B contribution is six B. If P also uses one B directly, total is seven after safe path expansion and outer aggregation. Duplicate BOM edges, cycles, units, numeric overflow, and effective versions must be governed.

### Example 7

For depth-first display, carry a path of stable sibling-order keys and sort by it outside. For breadth-first display, sort by `(depth,path)`. Neither computed key controls the engine's recursive visit order; it controls only final presentation.

### Example 8

An anchor casts path to a five-character string, but recursion appends identifiers beyond that width. A target engine can reject or truncate later values depending on its rules. Cast the anchor to a proven maximum representation or use a structured path type with explicit depth/size bounds.

### Example 9

A permissions graph includes grants and denies. Pure reachability through grant edges is monotone, but “nearest deny overrides inherited grant” requires depth, precedence, and conflict resolution. Compute candidate evidence safely, then apply the documented policy algebra; do not label raw closure as effective authorization.

### Example 10

A production root expands to 12 million paths despite depth eight. Evidence must include rows per depth, branching/skew, cycle rejections, working width, actual plan, index `(tenant,src)`, memory/temp I/O, deadline and cancellation, concurrency, and whether the product should switch to closure materialization.

## Cross-Program Connections

- [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) supplies BFS, DFS, shortest-path, fixed-point, and complexity reasoning.
- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) supplies queues, stacks, visited sets, graphs, and external-memory representations.
- [Theory of Computation and Complexity](../../15-theory-of-computation-and-complexity/ROADMAP.md) formalizes induction, fixed points, termination, and exponential output families.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) applies recursive dependency closure to lineage, orchestration, CDC, and backfills.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) governs tenant isolation, authorization inheritance, query budgets, and denial-of-service controls.

## References

1. PostgreSQL Global Development Group, [WITH Queries: Recursive Queries, Search Order, and Cycle Detection](https://www.postgresql.org/docs/18/queries-with.html), PostgreSQL 18 documentation.
2. PostgreSQL Global Development Group, [SELECT: Recursive WITH, SEARCH, and CYCLE](https://www.postgresql.org/docs/18/sql-select.html), PostgreSQL 18 documentation.
3. PostgreSQL Global Development Group, [UNION Type Resolution](https://www.postgresql.org/docs/18/typeconv-union-case.html), PostgreSQL 18 documentation.
4. PostgreSQL Global Development Group, [Client Connection Defaults: Statement Timeout](https://www.postgresql.org/docs/18/runtime-config-client.html#GUC-STATEMENT-TIMEOUT), PostgreSQL 18 documentation.
5. SQLite Project, [The WITH Clause](https://www.sqlite.org/lang_with.html), including recursive evaluation, queue controls, examples, and caveats.
6. SQLite Project, [Implementation Limits](https://www.sqlite.org/limits.html), SQLite documentation.
7. Oracle, [WITH Common Table Expressions](https://dev.mysql.com/doc/refman/8.4/en/with.html), MySQL 8.4 Reference Manual.
8. Oracle, [`cte_max_recursion_depth`](https://dev.mysql.com/doc/refman/8.4/en/server-system-variables.html#sysvar_cte_max_recursion_depth), MySQL 8.4 Reference Manual.

## Exercises

### Exercise 1

Trace anchor, working frontier, accepted rows, and termination for edges `A→B`, `A→C`, `B→D`, `C→D` under (a) vertex reachability with whole-row duplicate elimination and (b) simple-path enumeration with `UNION ALL` and path-local cycle checks.

### Exercise 2

Explain why changing rows from `(vertex)` to `(vertex,depth)` can turn a terminating duplicate-eliminated traversal of cycle `A→B→A` into nontermination. Give two correct remedies for two different desired outputs.

### Exercise 3

Write a termination proof for a positive-step integer series and for simple-path enumeration on a finite graph. Contrast the bound on maximum depth with the bound on number of output paths.

### Exercise 4

Design a tenant-safe bill-of-materials recursive contract. Include schema, anchor, step, cycle policy, quantities/units, temporal version, overflow, duplicate edges, aggregation boundary, reconciliation, and budgets.

### Exercise 5

Propose production evidence for a recursive dependency query over 50 million edges. Cover adversarial fixtures, snapshots, result semantics, indexes, estimates, rows/frontier per depth, memory/spill, skew, depth/row/time limits, cancellation, concurrency, security, and upgrades.

## Answers to the Exercises

### Answer 1

Reachability frontiers are `{A}`, `{B,C}`, `{D}`, then empty; accepted vertices are `{A,B,C,D}` because the second D is rejected as already seen. Simple-path frontiers contain paths `(A)`, then `(A,B),(A,C)`, then `(A,B,D),(A,C,D)`, then empty; D appears twice because two valid simple paths exist. There is no cycle here, but the path guard defines behavior if one is added.

### Answer 2

With state `(vertex)`, revisiting A or B duplicates an accepted row and adds no frontier. With `(vertex,depth)`, the cycle produces `(A,0),(B,1),(A,2),(B,3),...`, all distinct. For reachability, keep the recursive deduplication state to vertex identity and derive other attributes separately. For path output, use `UNION ALL`, carry a path, reject a child already in that path, and enforce independent resource bounds.

### Answer 3

For start `s`, positive step `k`, and upper bound `u`, the nonnegative remaining interval decreases by `k` on each accepted transition, so at most `floor((u-s)/k)+1` values appear when `s<=u`. For simple paths on finite `V`, each step appends a previously absent vertex, so depth is at most `|V|-1`. That proves termination, but the number of distinct simple paths can be exponential in `|V|`; shallow depth alone does not bound output tightly.

### Answer 4

Use rows `(tenant,part,path,depth,cumulative_quantity,unit,version)` with an authorized/versioned root anchor. Join edges on tenant, parent part, and effective version; multiply in an exact bounded type after unit validation; reject a child already in the composite tenant/part path; and treat duplicate source edges according to relationship identity. Aggregate quantities outside the safe path enumeration, reconcile direct and rolled totals independently, fail on overflow/cycles if they indicate invalid BOM data, and enforce approved root, depth, row, time, memory, and cancellation limits.

### Answer 5

Derive results independently on empty, chain, tree, diamond, duplicate-edge, self-loop, cycle, disconnected, composite-tenant, maximum-depth, and explosive-path fixtures. State whether output is vertices or paths, the snapshot/as-of, cycle key, completeness bound, and final order. On production-shaped distributions capture actual index/join plans, estimates, iterations, frontier and cumulative rows by depth, width, memory, temporary I/O, skew, latency, timeout and cancellation behavior under concurrency. Test role/tenant isolation in anchor and step, record truncation distinctly from completeness, and rerun semantic plus resource thresholds after engine, schema, statistics, index, or configuration changes.
