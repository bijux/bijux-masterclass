---
module_id: DBE-051
program: Database Engineering
level: 2
module_number: 51
title: Logical and Physical Plans
status: complete
last_verified: 2026-08-30
---

# Logical and Physical Plans

## One-Page Review

### Governing question

How does a database transform one declarative query meaning into an executable plan while preserving bag, null, ordering, type, visibility, and side-effect semantics across many implementation choices?

### Essential definitions

A **logical plan** represents what relational/expression operations must compute without committing to concrete algorithms or storage access paths. A **physical plan** chooses executable operators such as sequential/index scan, hash/merge/nested-loop join, sort, exchange, materialize, and aggregate. A transformation is **equivalence-preserving** only under stated semantics: SQL usually uses bags, three-valued predicates, null-sensitive constructs, collations, volatile expressions, errors, and observable ordering only when required. A **physical property** describes execution-relevant form—ordering, partitioning/distribution, uniqueness, rewindability, or representation—required or delivered by a plan. An **enforcer** such as sort, exchange, or materialize supplies a missing property. A **plan alternative** combines a logically equivalent expression with physical operators/properties and a cost estimate.

### Central model, mechanism, or theorem

Planning is property-directed refinement. Parse/analyze a statement into typed, bound semantics; normalize it into a logical expression; generate only transformations proven valid under the current semantic preconditions; implement each logical operator with physical alternatives; propagate required properties downward and delivered properties upward; add enforcers where necessary; estimate resource cost/cardinality; and choose a legal alternative. Correctness is feasibility plus equivalence; cost ranks only correct candidates.

### Critical invariants

- Names, types, collations, privileges, parameter identities, and expression volatility are resolved consistently.
- Logical rewrites preserve SQL bag multiplicity, null/three-valued logic, errors, side effects, and mandated order.
- Each physical operator declares input requirements, delivered properties, row schema, and lifecycle contract.
- Access predicates are separated into index conditions, join conditions, filters, and residual rechecks without losing rows.
- Required output ordering/distribution is either delivered or explicitly enforced.
- Estimates and costs never authorize an otherwise incorrect plan.
- Runtime plans obey snapshot, locking, DML, trigger, and retry semantics, not only relational output equivalence.
- Explain/plan artifacts are bound to engine/build, schema/statistics/configuration, parameters, and observation mode.

### Common failures

Failures include calling a parse tree a logical plan; treating join commutativity as universally valid under outer/semi/anti/lateral joins; forgetting duplicates or nulls; assuming subquery/CTE boundaries are always materialized; conflating predicates pushed to scans with discarded residual filters; losing ordering through hash/exchange operators; treating an index name as the full physical plan; comparing scalar cost numbers across engines; assuming estimated rows are measured rows; running `EXPLAIN ANALYZE` on mutating SQL without rollback/sandbox; pinning a plan from one dataset forever; and claiming two plans equivalent from one happy-path result.

### Compact example

Logical query: join customers to orders on customer ID, filter amount at least 50, project customer name and order ID, order by customer ID then order ID. Three physical realizations—hash join plus sort, ordered index nested loop, and merge join—return the same finite bag and order in the executable example. Their mechanisms/properties differ: hash join destroys useful order and needs an enforcer; index nested loop can preserve ordered outer/index traversal; merge join requires ordered inputs. Finite agreement is evidence for the example, not proof for arbitrary nulls, duplicates, collations, spills, or failures.

### Connections

Retrieve [Relational Algebra](002-relational-model-and-relational-algebra.md), [Joins and Join Semantics](012-joins-and-join-semantics.md), [Composite and Covering Indexes](035-composite-and-covering-indexes.md), and [Snapshot Visibility](047-snapshot-visibility.md). Continue through the Database Engineering [roadmap](../ROADMAP.md) to DBE-052 through DBE-060 for concrete operators and pipelines, then DBE-061 through DBE-070 for optimization.

## Governing Question

What contracts let optimizer rules replace a declarative expression with a cheaper executable tree or graph without changing the query's observable meaning?

## Why This Matters

SQL hides access paths and operator algorithms deliberately. The same query may scan a heap, probe an index, build a hash table, merge ordered streams, run a nested loop, repartition data, spill, or execute in parallel. This freedom enables performance, but every alternative must still implement exactly the intended semantics.

The logical/physical boundary is where many database bugs and performance misunderstandings begin. A rewrite valid for sets may be wrong for bags. Pushing a predicate through an outer join can remove null-extended rows. A hash join can be value-equivalent yet fail an ordering requirement. A plan cost can look lower because cardinality is wrong. A cached physical plan can become poor after skew or parameter change while remaining logically correct.

For practitioners, plan literacy is a diagnostic discipline, not tree-shape folklore. PostgreSQL 18 documents `EXPLAIN` output as a tree of plan nodes with estimated startup/total cost, rows, and width; `EXPLAIN ANALYZE` executes the statement and adds measurements. Estimates vary with statistics and cost settings. Machine-readable output is preferable for tooling, but even structured plans are engine/version artifacts, not a stable universal interchange contract.

For engine builders, the distinction creates replaceable layers: a logical algebra and rules can support new physical operators; properties let optimizers reason about order/distribution without encoding every combination; cost models rank alternatives; executor contracts make pipelines composable. The boundary is conceptual rather than identical across systems—some fuse, lower, compile, or serialize plans differently.

## Prerequisites and Retrieval

You should understand SQL binding and type checking, relational algebra, bags versus sets, three-valued logic, joins, indexes, pages/buffers, transactions/snapshots, trees/DAGs, asymptotic and resource cost, and statistics. Retrieve selection, projection, join, aggregation, correlated/lateral reference, predicate, residual filter, equivalence, access path, cardinality, selectivity, physical property, enforcer, pipeline breaker, and parameterization.

Level I established query semantics, storage, indexes, and transaction visibility. Level II begins by joining those layers: a correct physical plan must produce the logical result from visible physical versions while satisfying requested order and side-effect contracts. Later modules specialize each operator and then derive optimizer search and estimation.

## Learning Objectives

After this module, you can:

1. distinguish SQL syntax trees, analyzed trees, logical algebra, physical plans, and runtime operator state;
2. annotate logical operators with schema, types, multiplicity, nullability, correlations, and expression properties;
3. judge common rewrites under bags, nulls, outer joins, volatility, errors, and order;
4. map scans, joins, aggregates, sorts, exchanges, and materialization into physical alternatives;
5. derive required and delivered ordering, distribution, uniqueness, and rewindability properties;
6. explain enforcers and why locally cheap operators can make a globally expensive plan;
7. separate semantic feasibility, cardinality estimation, costing, and runtime measurement;
8. read structured and textual plans without treating them as portable or stable APIs;
9. test plan equivalence using adversarial data and independent oracles; and
10. diagnose plan regressions from bound environment, estimates, actuals, resources, and concurrency evidence.

## Core Exposition

**A query passes through several representations.** Text first becomes tokens and a syntax tree that reflects grammar. Analysis binds names to catalog objects, resolves overloads/types/collations, expands some syntactic forms, checks privileges, and identifies parameters/correlations. The result expresses meaning more precisely than raw syntax. A logical plan then represents relational and scalar operations independent of chosen algorithms; a physical plan chooses algorithms, access paths, properties, and often parallel/distributed boundaries. Execution instantiates runtime state—iterators, vectors, hash tables, buffers, workers, spill files, locks, and counters.

These are roles, not mandatory class names. One engine may combine analysis and logical rewriting; another uses a memo of equivalent expressions rather than one logical tree; another lowers into bytecode/vector pipelines; distributed frameworks serialize a portable algebra and let consumers refine it. Always identify which questions the representation answers.

**Logical plans need more than operator names.** A selection carries a three-valued predicate; a projection carries expressions, aliases, types, nullability, volatility, and error behavior; a join carries join kind, keys, residual predicate, correlation, and multiplicity; aggregation carries grouping equivalence/collation and aggregate modes; limit/order/window operators carry sequence requirements. Every edge has a row schema and name/identity discipline.

SQL's default bag semantics make many textbook set rewrites conditional. Projection cannot always be discarded because duplicate multiplicity/expressions matter. Pushing a filter below a duplicate-producing operator may change how often a volatile or erroring expression runs. `DISTINCT`, grouping, union versus union-all, and semi/anti joins need explicit multiplicity reasoning.

Nulls and outer joins are decisive. Predicate `right.x=5` after a left join rejects null-extended rows; pushing it into the right input while retaining unmatched left rows changes the result unless join form/predicate placement is transformed carefully. `NOT IN` differs from `NOT EXISTS` when nulls occur. Equality also depends on collation/type/coercion and null-safe operators.

**Logical equivalence is contextual.** Inner joins are associative and commutative under pure predicates and compatible semantics, enabling join reorder. Outer joins, lateral/correlated inputs, semi/anti joins, recursion, windows, ordered aggregates, limit/offset, locking clauses, volatile functions, exceptions, and DML constrain reorder or duplicate evaluation. A rule should encode preconditions, not rely on a slogan such as “filters always push down.”

Order is not generally part of a relational result, but SQL makes it observable at explicit boundaries: final `ORDER BY`, window frames, ordered aggregates, merge requirements, some cursor/limit semantics, and engine-specific constructs. Incidental order from an index or current plan is not an API guarantee unless the query/contract requires it.

**Physical plans implement logical operators.** A logical scan of relation R with predicate P can become sequential scan plus filter, index scan with residual recheck, bitmap construction plus heap scan, index-only scan subject to visibility/coverage, partition pruning plus child scans, or remote/columnar access. A logical join can become nested loop, hash, merge, index nested loop, or adaptive/distributed variants. Logical aggregation can use hash or ordered aggregation; ordering can use in-memory/external/incremental/top-N strategies.

Physical operators need contracts beyond output schema: required input order/partitioning; delivered order/partitioning/uniqueness; blocking/streaming behavior; rescan/rewind support; parameter dependencies; memory and spill policy; parallel safety; batch/row representation; cancellation and error cleanup; and visibility/locking behavior.

The executable example evaluates one logical query with three physical join strategies over finite, null-free, unique-key data. Each implementation applies the same amount filter and produces the required `(customer_id, order_id)` order before projecting the public columns.

<!-- bijux-verify: {"id":"logical-physical-equivalence","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"logical_rows=(('Ada', 101), ('Babbage', 103))\nhash_join_rows=(('Ada', 101), ('Babbage', 103))\nindex_nested_rows=(('Ada', 101), ('Babbage', 103))\nmerge_join_rows=(('Ada', 101), ('Babbage', 103))\nhash_requires_sort=True\nindex_nested_preserves_order=True\nmerge_requires_ordered_inputs=True\nall_physical_plans_equivalent=True\nevidence=finite_logical_physical_equivalence\n","stderr":""}} -->
```python
customers = ((1, "Ada"), (2, "Babbage"), (3, "Codd"))
orders = ((101, 1, 70), (102, 1, 20), (103, 2, 55), (104, 4, 99))

logical = tuple(
    (name, order_id)
    for customer_id, name in customers
    for order_id, order_customer_id, amount in orders
    if customer_id == order_customer_id and amount >= 50
)

customer_hash = {customer_id: name for customer_id, name in customers}
hash_pairs = [
    (order_customer_id, order_id, customer_hash[order_customer_id])
    for order_id, order_customer_id, amount in orders
    if amount >= 50 and order_customer_id in customer_hash
]
hash_rows = tuple((name, order_id) for _, order_id, name in sorted(hash_pairs))

orders_by_customer = {}
for order_id, customer_id, amount in sorted(orders, key=lambda row: (row[1], row[0])):
    orders_by_customer.setdefault(customer_id, []).append((order_id, amount))
index_nested_rows = tuple(
    (name, order_id)
    for customer_id, name in customers
    for order_id, amount in orders_by_customer.get(customer_id, ())
    if amount >= 50
)

left = iter(sorted(customers))
right = iter(sorted(orders, key=lambda row: (row[1], row[0])))
customer = next(left, None)
order = next(right, None)
merged = []
while customer is not None and order is not None:
    if customer[0] < order[1]:
        customer = next(left, None)
    elif customer[0] > order[1]:
        order = next(right, None)
    else:
        customer_id, name = customer
        while order is not None and order[1] == customer_id:
            order_id, _, amount = order
            if amount >= 50:
                merged.append((name, order_id))
            order = next(right, None)
        customer = next(left, None)
merge_rows = tuple(merged)

print(f"logical_rows={logical}")
print(f"hash_join_rows={hash_rows}")
print(f"index_nested_rows={index_nested_rows}")
print(f"merge_join_rows={merge_rows}")
print("hash_requires_sort=True")
print("index_nested_preserves_order=True")
print("merge_requires_ordered_inputs=True")
print(f"all_physical_plans_equivalent={logical == hash_rows == index_nested_rows == merge_rows}")
print("evidence=finite_logical_physical_equivalence")
```

The code does not model SQL bags with duplicate customer keys, nulls, collations, overflow, volatile/erroring expressions, MVCC, memory/spill, indexes, cost, parallelism, or a real optimizer/executor. It confirms only the recorded finite values/properties.

**Properties connect operators globally.** Suppose the query requires `(customer_id,order_id)` order. A hash join may deliver no useful order, requiring a sort. A merge join requires both sides ordered on join keys and can often deliver join-key order, subject to duplicate/tie details. An index nested loop may preserve an ordered outer stream and inner index order. The cheapest join operator in isolation may be worse after enforcers.

Optimizers propagate a required property from parent to child and record delivered properties for alternatives. A distributed aggregation may require hash partitioning on group keys; a merge join needs compatible order/distribution; a window needs partition/order; a repeated inner subtree may need rewindability/materialization. Interesting properties can justify retaining a locally costlier subplan because it saves a later sort/exchange.

Property claims require precision. Order is a sequence of expressions, directions, null placement, and collation; a prefix may satisfy some consumers. Partitioning includes keys/hash definitions/node sets. Uniqueness can simplify joins/aggregates but must be valid after predicates and null semantics. Representation and batch shape affect compatible operators.

**Search separates equivalence and implementation.** Rule-based optimizers use transformations such as join reorder, predicate pushdown, decorrelation, projection pruning, and aggregate transformations to populate equivalent logical expressions. Implementation rules map logical expressions to physical operators. A memo groups expressions by logical equivalence and stores alternatives/property-specific best costs.

System R established dynamic-programming access-path/join-order selection and “interesting orders.” Volcano/Cascades-style frameworks generalize extensible logical/physical rules, required properties, goal-directed search, and pruning. Modern engines vary widely, but the durable decomposition remains: correctness rules define the legal search space; estimates/cost guide choice within it.

Pruning must preserve the best legal alternative under its assumptions. Search budgets and heuristics may intentionally sacrifice optimality, never semantics. If no native operator delivers a required property, an enforcer makes a candidate feasible at added cost. If a feature is unsupported—say a correlated distribution pattern—the planner must reject or choose a supported fallback, not emit an invalid plan.

**Cost is conditional evidence.** An estimated plan annotates cardinality, row width, startup/total work, I/O, CPU, memory, network, parallelism, and spill risk according to an engine-specific model. Cost units are not elapsed milliseconds and are not comparable across engines/configurations. A plan with low startup cost can win for LIMIT/interactive response while a lower total-cost plan wins for full consumption.

Cardinality errors compound. Underestimating a selective-looking predicate may choose nested loops that execute millions of inner probes; underestimating build size may cause a hash spill; missing correlation between columns makes independence assumptions wrong. Costs are conditional on catalog statistics, parameters, configuration, available indexes, cache/hardware assumptions, and optimizer search coverage.

Separate four questions: Is the plan semantically legal? What does it estimate? Why did the optimizer rank it? What happened at runtime? Correctness precedes performance. Runtime measurements can calibrate estimates/cost but one warm-cache execution does not prove a universally better plan.

**Plan structure can be a tree or graph.** Shared subexpressions, common scans, recursive references, subplans, exchanges, spools/materialization, and adaptive alternatives create DAGs or control/data-flow graphs. Text indentation may hide execution direction and multiple relationships. Read child/parent roles, parameters, init/subplans, exchange producer/consumer, and loops rather than assuming rows flow visually top-to-bottom.

Parameterization binds an inner plan to outer values in nested loop or lateral/correlated evaluation. A displayed scan that looks cheap once may execute once per outer row. Runtime `loops`, rows per loop, memoization/cache hits, and total work matter. Logical decorrelation can turn repeated subplans into joins only when null/multiplicity/error semantics allow.

**DML plans carry side effects.** UPDATE/DELETE/MERGE plans first identify candidate rows, then lock/recheck/version and apply triggers/constraints/returning behavior. Concurrent changes can make the physical operation observe/recheck current versions according to isolation. Reordering volatile expressions, duplicate target matches, or Halloween-style revisitation can change effects. Plan equivalence for DML therefore includes affected row identity/count, errors, triggers, generated values, locks, and returned results—not merely a relation of output tuples.

Running `EXPLAIN ANALYZE` executes the statement. For mutating statements, use a safe disposable environment or transaction rollback only after considering nontransactional effects such as sequences/external functions. Restrict production explain tooling, parameters, and output because plans can expose schema, predicates, constants, and operational data.

**Explain output is scoped evidence.** Record exact query/parameter classes, engine/build, schema/index definitions, statistics timestamp/sampling, relevant settings, hardware/resource limits, concurrency/cache state, and whether execution occurred. Prefer structured formats for automation and normalize only fields whose loss is justified. Preserve the raw artifact under controlled access.

Estimated versus actual row ratios localize cardinality errors, but actual timing includes instrumentation, cache, contention, I/O, and concurrency. Buffers, spill/temp, memory, loops, worker distribution, waits, and output consumption often explain more than the operator name. A changed plan can be beneficial despite visual difference; a stable plan can regress because data/resources changed.

Plan forcing/hints can mitigate emergencies but freeze an implementation under current assumptions. Prefer durable fixes—correct statistics, schema/index, sargable semantics, cost/resource configuration, or optimizer defects—with versioned regression evidence. If a plan is pinned, define supported parameter/data envelope, expiry/removal trigger, and correctness compatibility across upgrades.

**Testing needs adversarial semantic data.** Differentially run logical reference and physical alternatives over duplicates, nulls, empty inputs, unmatched outer rows, many-to-many keys, collations, boundary numerics, volatile/error cases, and varied order. Assert bags with multiplicities and explicit order only where required. For DML assert target identities, affected rows, constraints/triggers/errors, and concurrency outcomes.

Property tests can generate small relations and compare alternatives. Metamorphic tests apply known-valid rewrites and compare. Plan-shape tests should be rare and scoped to intentional operator/property behavior because exact shapes change across versions/statistics. Always retain result correctness and resource/performance gates independently.

## Definitions and Notation

- **Syntax/analyzed tree:** grammatical structure versus names/types/semantics bound to catalog and context.
- **Logical operator:** declarative relational/scalar operation independent of execution algorithm.
- **Physical operator:** executable algorithm/access path implementing logical behavior under a contract.
- **Physical property:** ordering, distribution, uniqueness, rewindability, or representation required/delivered.
- **Enforcer:** operator inserted to establish a missing property, such as sort/exchange/materialize.
- **Plan alternative:** logical-equivalent expression plus physical choices and properties.
- **Memo:** optimizer structure grouping equivalent expressions and property-specific alternatives.
- **Cardinality/selectivity:** estimated row count/fraction after an operation.
- **Startup/total cost:** model estimates before first output versus full consumption.
- **Residual predicate/recheck:** condition not completely enforced by an access path and still evaluated.
- **Pipeline breaker:** operator requiring substantial input/materialization before producing output.
- `Bag(P,D)`: output multiset of plan P over database snapshot/input D; order is separate unless required.

## Mechanisms, Invariants, or Proof Structure

For each rewrite `L -> L'`, prove `Bag(L,D)=Bag(L',D)` for every allowed D under explicit types, nulls, collations, expression purity/error, correlation, and order/side-effect assumptions. Schema and multiplicities must match. Counterexamples outside preconditions justify rule guards.

For implementation `Phys(L,p)`, prove row/schema semantics implement L and delivered physical properties include parent requirement p, possibly through enforcers. Compose operators inductively: correct children satisfy their contracts; the parent algorithm produces the logical operator's result and advertised properties; the root satisfies externally observable order/result/effects.

Cost never appears in the semantic proof. Only after feasibility/equivalence can alternatives be ranked. Runtime evidence can falsify estimates or expose implementation defects but does not retroactively make an illegal rewrite valid.

The executable checks three independent finite implementations against a direct logical reference. Its agreement is a regression oracle for that dataset, not the universal quantifier required by the rule proof.

## Alternatives and Trade-Offs

- **Tree pipeline versus memo/DAG:** trees are readable/executable; memos capture equivalence/sharing but require group/property reasoning.
- **Heuristic rewrite versus cost-based search:** heuristics are cheap/predictable; costing compares interactions but consumes planning time and depends on estimates.
- **Row versus vector/compiled physical plan:** row iterators compose simply; vector/compiled pipelines reduce dispatch and improve locality but complicate boundaries/debugging.
- **Hash versus merge versus nested loop:** each has different input properties, memory, startup, spill, order, and parameterization—not one universal winner.
- **Native property versus enforcer:** preserving order/distribution can avoid work; explicit sort/exchange broadens feasible choices at cost.
- **Adaptive/reoptimization versus fixed plan:** adaptation responds to misestimation; it adds runtime state, transition semantics, and observability complexity.
- **Portable plan IR versus engine-native plan:** portable logical exchange aids interoperability; physical details/capabilities remain consumer-specific and versioned.

## Failure Modes and Misconceptions

- “Logical plan is parsed SQL.” Binding/normalization and logical algebra answer different questions from grammar.
- “Equivalent for sets means valid SQL rewrite.” Bags, nulls, order, volatility, and errors can refute it.
- “Inner joins can always move.” Correlation, effects, DML, and non-inner operators constrain transformations.
- “Index condition contains the full filter.” Residual recheck may be required for correctness.
- “Ordered input means ordered output.” Hash, exchange, aggregation, parallel gather, and duplicate handling can destroy/refine order.
- “Cost 100 means 100 ms.” Cost is an engine/configuration-specific ranking unit.
- “Estimated rows are observed rows.” Only execution instrumentation supplies actuals, with its own overhead.
- “The root is the first operator to run.” Demand/data/control flow depends on the execution model and blocking nodes.
- “One loop means one scan.” Parameterized inner nodes can execute once per outer row.
- “EXPLAIN ANALYZE is read-only.” It executes DML and possibly nontransactional effects.
- “Stable plan equals stable performance.” data, cache, resources, concurrency, and output consumption change.
- “Different physical outputs prove optimizer error.” Normalize only nonobservable order; compare full bags/types/effects and explicit required properties.

## Worked Examples

### Example 1

SQL syntax contains `a JOIN b`; analysis binds two catalog relations, coerces key types, and resolves collation. Logical plan expresses inner join; physical plan chooses hash join. Conclusion: each representation adds different commitments.

### Example 2

Pushing `right.x=5` below a left join while leaving the outer join retains unmatched left rows that the original post-filter removed. Conclusion: outer-join predicate pushdown needs a proven transformation/precondition.

### Example 3

`NOT IN (subquery)` with one null can yield UNKNOWN where `NOT EXISTS` yields true/false differently. Conclusion: decorrelation/anti-join rewrites must encode null semantics.

### Example 4

A hash join costs less locally but final ORDER BY adds a large spill sort; merge join consumes existing indexes and delivers order. Conclusion: required/delivered properties make plan choice global.

### Example 5

An index predicate covers `x<10` but a lossy bitmap/access method returns candidates requiring recheck. Removing the residual emits false matches. Conclusion: access condition and semantic filter are distinct contracts.

### Example 6

Estimated outer rows 10 choose index nested loop; actual rows 1,000,000 cause one million inner probes. Conclusion: inspect cardinality and loop multiplication before blaming the join algorithm alone.

### Example 7

A CTE is inlined in one engine/version and materialized in another or under a directive. Conclusion: SQL naming boundary does not universally specify a physical spool.

### Example 8

Parallel workers emit locally ordered streams into unordered gather; results appear sorted in tests until worker timing changes. Conclusion: only an order-preserving exchange/final sort plus SQL ORDER BY establishes order.

### Example 9

`EXPLAIN ANALYZE UPDATE` changes production rows while an engineer expects inspection only. Conclusion: use nonexecuting explain or a controlled disposable/rollback environment with nontransactional effects considered.

### Example 10

A plan pin fixes one skewed parameter but harms common parameters after data changes. Conclusion: bind mitigations to parameter/data envelopes and prefer statistics/model/index corrections with expiry gates.

## Cross-Program Connections

- [Programming Languages and Semantics](../../01-programming-languages-and-semantics/ROADMAP.md) supplies intermediate representations, typing, lowering, equivalence, and effect-sensitive optimization.
- [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) supplies dynamic programming, branch-and-bound, search spaces, approximation, and cost/error analysis.
- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) supplies trees/DAGs, memo tables, indexes, hash tables, heaps, and graph traversal.
- [Computer Architecture](../../23-computer-architecture/ROADMAP.md) supplies cache/locality, SIMD, branch behavior, memory bandwidth, and hardware cost.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies partitioning, exchanges, distributed joins, partial failure, and coordination.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) supplies portable plan/dataflow representations, batch/stream execution, and pipeline observability.

## References

1. PostgreSQL Global Development Group, [Using EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html), PostgreSQL 18 current documentation, retrieved 2026-08-30; plan trees, estimates, actuals, and interpretation caveats.
2. PostgreSQL Global Development Group, [The Path of a Query](https://www.postgresql.org/docs/current/query-path.html), PostgreSQL 18 current documentation, retrieved 2026-08-30; parse, rewrite, plan, and execute stages.
3. Patricia Griffiths Selinger et al., [“Access Path Selection in a Relational Database Management System”](https://web.eecs.umich.edu/~michjc/eecs584/Papers/selinger_1979.pdf), *SIGMOD*, 1979; System R access paths, dynamic programming, costs, and interesting order.
4. Goetz Graefe and William J. McKenna, [“The Volcano Optimizer Generator: Extensibility and Efficient Search”](https://www.cs.cornell.edu/~mshong/DDG_Fall05/Volcano.pdf), *ICDE*, 1993; logical/physical algebra, rules, properties, and search.
5. Goetz Graefe, [“Query Evaluation Techniques for Large Databases”](https://web.stanford.edu/class/cs346/2014/graefe.pdf), *ACM Computing Surveys* 25(2), 1993; physical operator algorithms and resource trade-offs.
6. Goetz Graefe, [“The Cascades Framework for Query Optimization”](https://liuyehcf.github.io/resources/paper/The-Cascades-Framework-For-Query-Optimization.pdf), *IEEE Data Engineering Bulletin* 18(3), 1995; memoized rule/property-driven optimization.
7. Apache Calcite Project, [Algebra](https://calcite.apache.org/docs/algebra.html), current official documentation, retrieved 2026-08-30; relational expressions, traits, conventions, and planner transformations.
8. Substrait Project, [Specification](https://substrait.io/spec/specification/), current specification, retrieved 2026-08-30; logical and physical relation plan interchange.
9. SQLite Project, [EXPLAIN QUERY PLAN](https://www.sqlite.org/eqp.html), current documentation, retrieved 2026-08-30; plan-output instability and scan/search interpretation.
10. DuckDB Foundation, [EXPLAIN: Inspect Query Plans](https://duckdb.org/docs/current/guides/meta/explain), current documentation, retrieved 2026-08-30; logical/physical plan inspection and cardinality presentation.

## Exercises

### Exercise 1

Translate a SQL query with join, filter, projection, grouping, HAVING, and ORDER BY into an analyzed schema and logical operator tree. Annotate bag, null, type, collation, and ordering semantics.

### Exercise 2

For a left outer join with predicates on both sides, derive which pushdowns are valid. Supply counterexamples for invalid placement using nulls and unmatched rows.

### Exercise 3

Enumerate hash, merge, and index nested-loop physical plans for a two-table ordered query. State required/delivered properties, enforcers, startup/total resources, and spill/parameter boundaries.

### Exercise 4

Diagnose a plan regression whose estimated outer cardinality is 50 and actual is 2 million. Design evidence collection and compare statistics, index/schema, rewrite, resource, adaptive, and pinning remedies.

### Exercise 5

Design a logical-to-physical plan verification program for a database engine, covering rule proofs, generated adversarial data, differential/metamorphic oracles, DML/concurrency, plan serialization/versioning, performance evidence, and release gates.

## Answers to the Exercises

### Answer 1

Bind every relation/column/function, resolve overload/coercion/collation, and record output identities/types/nullability. A representative logical tree is sort(order keys) over projection over filter(HAVING) over aggregate(group keys, aggregates) over filter(WHERE) over join(inputs, join predicate). WHERE precedes grouping; HAVING filters groups; projection expressions may expose aggregate/group values; final ORDER BY is the external order contract. Preserve bag multiplicity until distinct/group semantics change it, apply three-valued predicates (only TRUE retained), identify nullable columns introduced by outer joins, and mark volatile/erroring/correlated expressions so rewrites cannot duplicate/reorder them without proof.

### Answer 2

A predicate using only preserved left input can often push into left before a left join if expression evaluation/effects allow. A predicate in the ON clause using only right input can push to right because it controls matches while unmatched left rows remain. A post-join WHERE predicate `right.x=5` is null-rejecting: original removes unmatched left rows; pushing it only into right while retaining a left join wrongly preserves them. It may support transforming the join to inner under proven null-rejection and effect conditions. `right.x IS NULL` is not null-rejecting and can select both unmatched rows and matched rows whose x is null; pushing changes meaning. Include duplicates, volatile/erroring predicates, and correlated references in rule guards.

### Answer 3

Hash join accepts unordered inputs, builds one side in memory/spill partitions, streams probes, and usually delivers no required order; add final sort/exchange as needed. Merge join requires compatible join-key ordering, obtained from indexes or sorts, can stream after startup sorting, and may deliver a useful join-key order subject to duplicate/tie semantics. Index nested loop requires parameterized inner lookup; ordered outer plus an index ordered by join key and requested suffix may preserve final order, but cost multiplies probes by outer cardinality and random access/cache behavior. Compare build/probe versus sort versus per-row lookup; record row widths, selectivity, memory/spill, startup versus total, parallel/distribution, rescan, null/outer behavior, and enforcer costs.

### Answer 4

Capture exact engine/build, query/parameters, schema/indexes, statistics age/sample/extended stats, settings, structured estimated and actual plan, loops, buffers, memory/spill/temp, workers, waits, cache/concurrency, and output consumption. A 40,000x outer underestimate can make nested-loop probes dominate and propagate into join/aggregate choices. Validate stale/missing statistics, skew and parameter correlation, expressions/coercions, predicate sargability, and cross-column dependence. Remedies include accurate/extended statistics, a semantically correct index/schema, query expression correction, resource configuration, or engine estimator defect fix; adaptive/reoptimization is useful when parameter uncertainty is inherent. Pinning/hints are scoped emergency controls with data/parameter envelope and expiry. Recheck full result semantics and workload p95/p99/resources, not one warm run.

### Answer 5

Specify typed logical operators, scalar effect/null/error semantics, physical operator contracts, and properties. For every transformation, record preconditions and proof/counterexamples under bags, nulls, collation, correlation, order, volatility, errors, and DML effects. Generate small adversarial relations with duplicates, nulls, empty/unmatched/many-to-many keys and boundary values; evaluate a simple independent logical interpreter and all applicable physical alternatives, comparing bags/types and explicit order. Use metamorphic valid rewrites and planted-invalid rules to validate the checker. Add target-engine tests for visibility, locks, affected rows, triggers/constraints/RETURNING, cancellation, spill, parallel/exchange, and failures. Version structured plan schemas and reject unknown operators/properties rather than silently parsing. Gate correctness first; separately gate estimator calibration, planning time/search budget, memory/spill, latency/throughput, and plan-regression envelopes across engine/configuration/data versions. State finite coverage and no claim of universal rule or production fitness without broader review.
