---
module_id: DBE-040
program: Database Engineering
level: 1
module_number: 40
title: Choosing Indexes from Workload Evidence
status: complete
last_verified: 2026-08-30
---

# Choosing Indexes from Workload Evidence

## One-Page Review

### Governing question

How can engineers choose an index portfolio that satisfies correctness and service objectives for a representative evolving workload while making read benefit, write/space/maintenance cost, uncertainty, interactions, and rollback explicit?

### Essential definitions

A **workload** is a versioned distribution or sequence of query and mutation templates with parameters, frequency, concurrency, tenants, roles, time slices, and service objectives—not a bag of SQL strings. A **query fingerprint/template** normalizes literals while retaining plan-relevant structure. A **candidate index** has exact keys/order, predicate, expressions, included payload, uniqueness, collation/operator semantics, partition scope, and engine version. A **configuration/portfolio** is a set of physical structures. A **what-if/hypothetical index** lets an optimizer estimate plans without paying full construction, but does not measure execution. **Benefit** is workload cost or observed service improvement relative to a controlled baseline. **Marginal benefit** is improvement when one candidate is added to a particular configuration. **Opportunity cost** is the best alternative excluded by storage, write, build, operational, or complexity budgets. **Workload drift** is a material change in shapes, weights, data distribution, objectives, or engine behavior.

### Central model, mechanism, or theorem

Index selection is constrained portfolio optimization. For workload templates `q` with weights `w_q`, estimated or observed cost `C(q,X)` under index set `X`, write/storage/build costs, and hard correctness/SLO constraints, minimize `Σ_q w_q C(q,X)+λ_w W(X)+λ_s S(X)+λ_o O(X)` subject to budgets and gates. Candidates interact: two indexes can substitute, complement through bitmap/index intersection, alter join order, or make another redundant, so individual recommendations cannot simply be summed. Optimizer estimates generate hypotheses; only execution/replay/canary evidence on representative data can support deployment. Semantic indexes for uniqueness or other enforced invariants are hard requirements, not optional score terms.

### Critical invariants

- Candidate definitions preserve exact comparison, collation, NULL, expression volatility, predicate implication, uniqueness, tenant, partition, and authorization semantics.
- Workload weights and slices include frequency, latency/SLO criticality, concurrency, writes, rare essential paths, replicas/roles, seasonality, and failure/recovery operations.
- Baseline and treatment use the same data snapshot/distribution, parameters, cache protocol, engine/configuration, concurrency, durability, and measurement interval unless the difference is deliberate.
- The evaluation considers whole configurations, including interactions, write amplification, storage/cache, maintenance, WAL/replicas, build/rollback, and plan regressions.
- Estimated cost is labeled as an estimate; execution time is repeated and uncertainty reported; neither alone proves production fitness.
- Every rollout has validation, canary/visibility controls where supported, observability, abort thresholds, and a tested recreation/rollback path.

### Common failures

Failures include indexing every filtered column; optimizing one slow query while harming a high-frequency path; trusting a missing-index recommendation as an order; multiplying correlated samples as independent; replaying only SELECTs; using production literals or sensitive SQL unsafely; ignoring parameter skew and prepared-plan behavior; treating optimizer cost as milliseconds; summing individual benefits despite interactions; mistaking a covering index for free; dropping an index from zero-use counters that reset or miss replicas; confusing invisible with unmaintained; changing schema and engine version together; testing a warm treatment against a cold baseline; excluding build/maintenance/recovery; and deploying without plan/result/SLO rollback gates.

### Compact example

Three candidates compete under `70` storage units and `25` write-cost units. A unique email index is a semantic requirement. Workload-weighted query cost plus `10×write_cost` makes the unique index alone feasible but slow; adding `(tenant,status)` yields objective `3630`. Adding `(status,created_at)` with the unique index exceeds storage. The selected pair is therefore not “the two highest independent benefits”; it is the best feasible configuration after a hard correctness gate.

### Connections

Retrieve [Composite and Covering Indexes](035-composite-and-covering-indexes.md), [Partial and Expression Indexes](036-partial-and-expression-indexes.md), [Bitmap and BRIN-Style Indexes](037-bitmap-and-brin-style-indexes.md), and [Index Maintenance and Write Amplification](039-index-maintenance-and-write-amplification.md). Continue through the [Database Engineering roadmap](../ROADMAP.md) to DBE-041, ACID and Transaction Boundaries.

## Governing Question

Given incomplete observations, interacting candidates, finite resources, evolving data, and asymmetric failure costs, what evidence justifies creating, retaining, reshaping, hiding, or dropping each index as part of a coherent portfolio?

## Why This Matters

Indexes are easy to propose and expensive to own. A single query plan may improve by orders of magnitude, yet each extra access path consumes build time, storage/cache, DML/WAL/replica bandwidth, vacuum/compaction work, backup/restore time, and operational attention. An index that helps a weekly report may be vital; one that helps a frequent query may still be dominated by another configuration. A uniqueness index is part of correctness regardless of scan counts.

Selection is harder than matching `WHERE` columns to B-trees. Real plans combine joins, filters, ordering, grouping, LIMIT, visibility, correlation, partitions, statistics, parameters, and competing access paths. Candidate indexes alter cardinality-dependent join orders and each other's marginal value. Workload samples are censored: slow queries may time out, rare incident paths may be absent, replicas carry different reads, and normalized fingerprints may hide skew. Current cost models are useful but approximate.

A production-grade decision therefore moves through evidence levels: semantic inventory, observational workload, candidate/mechanism reasoning, optimizer what-if, controlled execution, representative concurrent replay, reversible canary, and post-deployment monitoring. Each level answers a different question. No advisor, EXPLAIN plan, benchmark screenshot, or index-usage counter collapses them into certainty.

## Prerequisites and Retrieval

You should understand B-tree/hash/bitmap/BRIN/full-text mechanisms; leftmost/composite ordering; covering/index-only conditions; partial-predicate implication; expression/collation semantics; page/write maintenance; query plans and cardinality estimates at a basic level; and percentile/SLO measurement. Retrieve selectivity, correlation, parameter skew, controlled experiment, confidence interval, opportunity cost, semantic constraint, write amplification, and rollback. Later query-optimization modules deepen plan costing; this chapter focuses on choosing physical access paths from evidence.

## Learning Objectives

After this module, you can:

1. construct a privacy-safe, versioned workload model across templates, parameters, roles, tenants, writes, concurrency, and time slices;
2. separate semantic/SLO hard constraints from weighted optimization objectives;
3. generate precise B-tree, hash, partial, expression, covering, summary, and search-index candidates from access requirements;
4. detect redundant, substituting, and complementary candidate interactions;
5. interpret statistics, plans, usage counters, advisors, hypothetical indexes, and missing-index signals without overclaiming;
6. define workload benefit and lifecycle cost at comparable boundaries;
7. execute fair cold/warm, repeated, concurrent, and steady-state experiments with correctness oracles;
8. design reversible invisible-index/canary/create/drop rollouts under engine-specific semantics;
9. detect workload/data/engine drift and trigger review without autonomous unsafe churn; and
10. defend an index portfolio with evidence, uncertainty, owners, expiry/review conditions, and rollback.

## Core Exposition

**Start with requirements, not candidates.** Inventory every table's primary/unique/exclusion/foreign-key or engine-required indexes and distinguish semantic enforcement from performance. Record exact definition, owner, dependent constraints, query roles, tenant/security boundary, creation reason, observation provenance, build/rebuild cost, and rollback recipe. A performance tuner may compare optional indexes only after hard semantic requirements are fixed.

Define service gates before minimizing a score: result equivalence, constraint preservation, authorization/tenant isolation, maximum permitted regression for critical templates, p99 write/read limits, replication lag, storage headroom, maintenance window, recovery target, and build/cancel safety. A weighted average must not buy a catastrophic checkout or incident-path regression with many cheap background wins.

**Construct the workload.** Capture query fingerprints plus plan-relevant features: predicates/operators, joins, projection, ordering, grouping, LIMIT, lock mode, consistency/isolation, partition, role, source/replica, and write operation. Store privacy-preserving parameter classes or synthetic/replayable values, not raw secrets. Weight by executions, resource time, business/SLO importance, tenant fairness, and temporal slices. Frequency alone undervalues rare mandatory paths; total elapsed alone can double-count concurrency waits.

Include mutations and background work. Inserts/updates/deletes determine index maintenance; bulk loads, retention deletes, vacuum/compaction, statistics, backups, replicas, rebuilds, and recovery consume the same budgets. Record concurrency and arrival sequence because cache, locks, queueing, plan cache, and maintenance debt make a sequence different from isolated queries. Mark sampling rate, dropped/time-out requests, counter reset, failover, deployment, and seasonality.

Normalization needs care. Queries differing only in literals can share a fingerprint, but parameter distributions may require separate classes: common versus rare value, recent versus historical range, small versus large tenant, empty versus dense partition, short versus deep pagination. Prepared/generic and custom plans can differ. Preserve enough structure to reproduce those regimes without retaining sensitive content.

**Generate candidates from access semantics.** Equality/join columns often lead composite prefixes; range/order/group needs constrain subsequent ordering; included payload may avoid table fetches only when visibility/storage conditions permit. Partial indexes require a stable predicate that the query can imply. Expression indexes require exact expression/collation/volatility semantics. Hash supports scoped equality; BRIN/summary indexes suit correlated large tables with recheck; inverted/full-text indexes require analyzer/query compatibility. Partition-local/global and clustered/secondary choices change identity, pruning, maintenance, and uniqueness.

Do not enumerate arbitrary column permutations. Derive candidates from normalized query requirements, existing useful prefixes, engine limits, cardinality/correlation, and explicit maximum key/payload width. Canonicalize definitions so identical candidates merge. Prune candidates that cannot preserve semantics, exceed hard build/space limits, duplicate an equivalent existing index, or have no supported query. Retain candidates serving constraints or rare critical templates even if weights are small.

**Understand interactions.** Suppose indexes `a` and `b` both accelerate the same filter. Their individual improvements share the same baseline, so selecting both rarely yields the sum. Conversely, bitmap/intersection plans can make them complementary; an index can change join order so another becomes useful; a covering extension can subsume a narrow prefix for some queries but cost more writes/cache; a partial index and general index can serve different slices. Define marginal benefit

`Δ(a|X)=Cost(W,X)-Cost(W,X∪{a})`.

Because `Δ(a|X)` depends on `X`, rank-alone greedy choice has no universal correctness guarantee. Exhaustive search works only for small sets; practical advisors prune/search configurations with heuristics, relaxation, integer/program-specific techniques, or iterative what-if calls. Treat their result as a candidate design with assumptions, not authority.

**Objective and gates.** For templates `q`, configuration `X`, weights `w_q`, query cost `C(q,X)`, and portfolio costs `W,S,O`, a teaching objective is:

`J(X)=Σ_q w_q C(q,X)+λ_w W(X)+λ_s S(X)+λ_o O(X)`.

Subject to required indexes `R⊆X`, storage/write/build budgets, and per-template/service gates. Units require calibration: optimizer cost cannot be added directly to bytes or milliseconds without an explicit normalization/utility function. Often Pareto frontiers are more honest: expose configurations not dominated simultaneously on read latency, write cost, storage, and risk, then apply policy.

Hard constraints are not infinite weights hidden in code. List them and explain their authority. If no feasible configuration exists, report infeasibility and the binding constraints; do not silently violate semantics or SLOs. Opportunity cost is part of the decision: accepting one wide covering index may exclude two narrower critical indexes under cache/storage/build budgets.

The following finite model enumerates every portfolio. Query costs are transparent invented estimates; `idx_email_unique` is required for semantics. It demonstrates interactions and feasibility, not a DBMS advisor or performance benchmark.

<!-- bijux-verify: {"id":"index-portfolio-selection","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"baseline_weighted_query_cost=11700\nrequired_indexes=('idx_email_unique',)\nstorage_budget=70\nwrite_budget=25\nfeasible_configurations=(('idx_email_unique',), ('idx_tenant_status', 'idx_email_unique'))\nselected=('idx_tenant_status', 'idx_email_unique')\nselected_weighted_query_cost=3410\nselected_write_cost=22\nselected_storage=65\nselected_objective=3630\ninvariants=True\n","stderr":""}} -->
```python
from itertools import combinations

queries = {"tenant_status": (100, 100), "status_recent": (20, 80), "email": (2, 50)}
candidates = {
    "idx_tenant_status": {"storage": 40, "write": 12, "costs": {"tenant_status": 20, "status_recent": 70}},
    "idx_status_created": {"storage": 50, "write": 18, "costs": {"tenant_status": 30, "status_recent": 15}},
    "idx_email_unique": {"storage": 25, "write": 10, "costs": {"email": 5}},
}
required = {"idx_email_unique"}
storage_budget = 70
write_budget = 25


def query_cost(configuration: tuple[str, ...], query: str, baseline: int) -> int:
    alternatives = [baseline]
    for index in configuration:
        if query in candidates[index]["costs"]:
            alternatives.append(candidates[index]["costs"][query])
    return min(alternatives)


def evaluate(configuration: tuple[str, ...]) -> tuple[int, int, int, int]:
    weighted = sum(weight * query_cost(configuration, query, baseline) for query, (weight, baseline) in queries.items())
    write = sum(candidates[index]["write"] for index in configuration)
    storage = sum(candidates[index]["storage"] for index in configuration)
    return weighted + 10 * write, weighted, write, storage


names = tuple(candidates)
configurations = tuple(
    combination
    for count in range(len(names) + 1)
    for combination in combinations(names, count)
)
feasible = tuple(
    configuration
    for configuration in configurations
    if required.issubset(configuration)
    and evaluate(configuration)[2] <= write_budget
    and evaluate(configuration)[3] <= storage_budget
)
selected = min(feasible, key=lambda configuration: (evaluate(configuration)[0], configuration))
objective, weighted, write, storage = evaluate(selected)
baseline = sum(weight * cost for weight, cost in queries.values())

print(f"baseline_weighted_query_cost={baseline}")
print(f"required_indexes={tuple(sorted(required))}")
print(f"storage_budget={storage_budget}")
print(f"write_budget={write_budget}")
print(f"feasible_configurations={feasible}")
print(f"selected={selected}")
print(f"selected_weighted_query_cost={weighted}")
print(f"selected_write_cost={write}")
print(f"selected_storage={storage}")
print(f"selected_objective={objective}")
print(f"invariants={required.issubset(selected) and write <= write_budget and storage <= storage_budget}")
```

The minimum-cost alternative per query models substitution, but not index intersection or join-order complementarity; a real evaluator must ask its optimizer or execution engine about each configuration. The objective's costs are unitless teaching values. It omits builds, plans, SQL, data, concurrency, uncertainty, maintenance, crashes, replicas, security, and drift.

**Evidence ladder.** Schema reasoning rejects impossible candidates. Statistics estimate row counts, distinctness, null fractions, histograms, dependencies/correlation, and physical correlation; stale or coarse statistics distort candidates and plans. `EXPLAIN` shows optimizer choices and estimates. `EXPLAIN ANALYZE` or equivalent executes—possibly causing writes/triggers/locks—so use safe environments/transactions and understand side effects. Compare estimated versus actual rows at each node, loops/searches, table fetches/rechecks, sort/spill, buffers/I/O, memory, and time.

Hypothetical indexes and advisors avoid full builds and use optimizer costing. They are valuable for candidate pruning and interaction search, but inherit cost-model/cardinality errors and generally cannot prove build cost, cache pressure, write amplification, concurrency, result correctness, or tail latency. Missing-index features see particular observed plans and may emit overlapping, wide, or transient suggestions. Preserve recommendation inputs/version and test the resulting configuration.

Usage counters answer narrowly defined questions. PostgreSQL's current `pg_stat_all_indexes.idx_scan`, for example, counts initiated index searches and one executor node can initiate multiple searches; it is not “business queries served.” Counters can reset at restart/manual reset, exclude other databases/roles/replicas, and miss disabled/failed/timed-out paths. Join counters to definitions/dependencies and a known observation interval. An unused enforcement index can still reject bad writes.

**Controlled execution.** Materialize candidates in an isolated representative clone or supported safe environment. Use the same schema/statistics/data snapshot, engine/config, hardware limits, durability, connection pool, concurrency, parameter sequence, and cache protocol for baseline/treatment. Randomize or alternate run order to reduce temporal confounding; repeat enough to report distribution and uncertainty. Separate cold-cache, warm-cache, and steady-state questions rather than choosing the flattering one.

Verify exact result sets, ordering/ties, errors/constraints, row counts, authorization/tenant behavior, and transaction effects before performance. Capture per-template and whole-workload p50/p95/p99/max, timeouts, throughput, CPU, memory, logical/physical I/O, cache, temp/spill, locks, WAL/redo, DML bytes/latency, index/table bytes, maintenance debt, replica lag, and storage headroom. Run long enough for checkpoints, splits, vacuum/merge, and device steady state. Test build, cancel, crash/recovery, restore, and rollback separately.

Do not interpret a plan change as improvement or unchanged plan as no effect: construction can displace cache and add writes even if unused. Optimizer cost is a relative planning signal in engine-specific units, not elapsed time. An observed speedup on replay is conditional on its workload/data/environment. Report confidence and uncovered slices.

**Reversible production learning.** Some engines support invisible indexes. Current MySQL documents that invisible indexes are ignored by the optimizer by default but remain maintained and continue enforcing uniqueness; primary indexes have restrictions. This makes visibility useful for testing query-plan dependence, not for measuring write savings. Selected sessions can explicitly consider invisible indexes under documented controls. Engine semantics differ; never emulate visibility by editing catalogs.

For addition, build online/concurrently only with understood locks, catch-up, WAL, space, replica, failure, and invalid-artifact behavior. Start invisible/session-scoped or on a canary when supported, compare plan/result/SLO gates, expand gradually, and retain rollback. For removal, first prove semantic non-dependence, observe all roles/seasons, make invisible where supported, watch slow/error/plan/write metrics, then drop only after the evidence window. Recreation duration and peak load determine rollback realism.

**Drift and governance.** Store a decision record: workload snapshot/fingerprint distribution, data/statistics snapshot, engine version/config, candidate definitions, estimates, replay commands/results, uncertainty, constraints/budgets, chosen Pareto tradeoff, reviewer/owner, rollout, rollback, expiry, and reevaluation triggers. Triggers include schema/query release, data growth/skew/correlation, tenant mix, season, SLO, hardware/storage, engine/optimizer/statistics change, counter reset, and maintenance/recovery regression.

Automation may detect drift, generate candidates, and run bounded what-if/replay. Autonomous create/drop changes are external-state operations with data availability and performance risk; require scoped authorization, budgets, canary gates, rate limits, audit, and rollback. Oscillation is a failure: use minimum evidence windows, hysteresis, change cost, cooldowns, and a stable baseline. “Self-tuning” still needs an authority and safety contract.

## Definitions and Notation

- `W={(q,w_q)}`: versioned weighted workload; `q` includes parameter/slice class and objective, not only SQL text.
- `A`: finite canonical candidate index set; `X⊆A` is one configuration.
- `R⊆X`: semantically or operationally required indexes.
- `C(q,X)`: estimated or observed cost for `q` under configuration `X`, with units/evidence level declared.
- `J(X)`: explicitly normalized portfolio objective, never an unlabeled sum of unlike units.
- `Δ(a|X)=Cost(W,X)-Cost(W,X∪{a})`: configuration-conditional marginal benefit.
- `B_s,B_w,B_b`: storage, steady write, and build/operational budgets.
- `G_k(X)≤0`: a hard gate/constraint such as critical-template regression, storage, or recovery headroom.
- **Dominance:** `X` dominates `Y` if no worse on every declared objective and strictly better on at least one; a **Pareto frontier** contains nondominated configurations.
- **Estimate:** model output conditional on statistics/cost model; **observation:** measured run; **causal evidence:** controlled contrast supporting an intervention effect under assumptions.
- **Plan regression:** a treatment plan violates a declared correctness/resource/SLO gate relative to its accepted baseline, not merely any textual plan difference.

## Mechanisms, Invariants, or Proof Structure

Selection correctness has layers. Semantic filtering first proves candidate definitions and required constraints preserve the database contract. Feasibility proves `R⊆X` and every hard budget/gate. Optimization then compares only feasible configurations under a declared objective or Pareto ordering. Execution validation finally tests the model's assumptions. A low `J(X)` cannot compensate for failure at an earlier layer.

Interaction invalidates naive addition. If `a` and `b` substitute for the same query, `Δ(a|∅)+Δ(b|∅)` double-counts the baseline; if a join-order or intersection benefit appears only together, individual deltas undercount. Therefore an advisor must evaluate configurations or use a justified approximation. The executable finite search is exact only for its tiny candidate/evaluator model.

A/B causal interpretation requires exchangeability or controlled replay: treatment differs only by configuration, workload assignment/order is unbiased, measurement covers the relevant lifecycle, and interference is controlled. Shared cache, replicas, background jobs, evolving data, learning/adaptive optimizers, or maintenance spillover break simple independence. Record them or use alternating/repeated designs.

Safe removal is a conjunction: no semantic dependency; no required workload slice needs the index within evidence bounds; alternative plans meet gates; write/space benefit is material; visibility/canary produces no abort signal; and recreation/rollback fits risk. Failure to observe use is only one input, never a proof of absence.

## Alternatives and Trade-Offs

- **Manual design versus advisor:** humans reason about semantics/rare paths; advisors search more configurations consistently. Combine auditable automation with human authority.
- **What-if versus materialized replay:** what-if is cheap and broad but model-bound; replay observes execution but costs build/resources and remains environment-bound.
- **Weighted scalar versus Pareto frontier:** scalar ranking is automatable but hides exchange rates; a frontier exposes tradeoffs but requires policy choice.
- **Broad covering versus narrow indexes:** covering can reduce fetches and serve order but increases size/cache/write/build; narrow indexes may intersect or serve distinct slices.
- **General versus partial index:** general supports more shapes; partial saves space/write and can improve density when predicates are provably implied.
- **Add versus rewrite query/schema/statistics:** an index treats access symptoms; query shape, denormalization, partitioning, statistics, caching, or workload policy may dominate.
- **Invisible/canary versus immediate drop:** reversible learning costs continued maintenance; immediate drop realizes savings but makes rollback a potentially long rebuild.
- **Periodic versus continuous tuning:** periodic is stable/auditable but slower to drift; continuous detects quickly but risks churn, interference, and unsafe automation.

## Failure Modes and Misconceptions

- “Index every predicate.” Low selectivity, ordering, joins, correlation, existing prefixes, writes, and cache change value.
- “The advisor chose it.” Advisors optimize a sampled/modelled objective under candidate and cost-model assumptions.
- “Estimated cost fell 80%, so latency will.” Cost units are not milliseconds and cardinality/cache/concurrency can be wrong.
- “Each index saves 30%, so two save 60%.” Marginal benefits depend on configuration.
- “A covering index avoids all table work.” Visibility/recheck, width, cache, updates, and engine semantics remain.
- “Invisible means free.” MySQL still maintains invisible indexes and enforces uniqueness.
- “Zero scans means safe to drop.” Counters and observation scopes are incomplete; semantics and rare paths remain.
- “One benchmark result is evidence.” Repeat, alternate, report distributions, and cover steady-state maintenance.
- “Production canary proves global safety.” It supports only sampled tenants/shapes/time and can be confounded.
- “More indexes cannot hurt reads.” They consume cache and optimizer search, and builds/maintenance interfere.
- “Automatic tuning should always converge.” Drift/noise without hysteresis and change cost can oscillate.
- “Rollback is CREATE INDEX.” Rebuild time, load, locks, WAL, space, replicas, and lost SLO determine recovery.

## Worked Examples

### Example 1

A query filters `tenant_id=? AND status=?`, orders by `created_at DESC`, and limits 50. `(tenant_id,status,created_at DESC)` can seek and order; `(status,tenant_id)` may serve equality but has different cross-query prefixes. Conclusion: derive key order from the whole workload, not a slogan about most selective first.

### Example 2

One fingerprint has 99% tiny tenants and 1% tenant holding half the rows. A single mean parameter hides two plans. Split parameter classes and weight both, including the large tenant's SLO. Conclusion: normalized SQL is not a complete workload unit.

### Example 3

Candidates `a` and `b` each cut a query cost from 100 to 20 alone; together cost remains 20. Summed claimed saving is 160 against a 100 baseline. Conclusion: substitution makes independent-benefit addition impossible.

### Example 4

Two individually unused single-column indexes can be intersected for a rare conjunction only under certain optimizer/statistics conditions; a composite may dominate at added width. Conclusion: inspect configuration plans and observed slices before declaring redundancy.

### Example 5

A partial index covers active orders, 5% of rows. It wins only when query predicates provably imply the same active condition; a parameterized/rewritten predicate may not. Conclusion: small size is irrelevant if the optimizer cannot safely use it.

### Example 6

An advisor recommends a wide covering index from SELECT-only traces. Replay adds real updates: WAL doubles, p99 writes regress, and cache evicts another hot index. Conclusion: workload selection must include mutations and lifecycle effects.

### Example 7

`pg_stat_all_indexes.idx_scan=0` since a restart three days ago. The index backs a monthly report on a read replica. Conclusion: record reset, database/role/replica/season scope; absence in this counter is not absence of need.

### Example 8

A MySQL index becomes invisible. Query plans regress in the canary, but write cost does not fall because the index is still maintained. Making it visible rolls query behavior back quickly. Conclusion: visibility tests plan dependence, not drop savings.

### Example 9

Treatment runs after baseline and inherits a warm cache plus completed checkpoint. Latency improves without a useful index plan. Alternating runs with controlled cache removes the effect. Conclusion: temporal order and background interference are confounders.

### Example 10

A Pareto frontier offers X: 40% read gain/5% write cost and Y: 50% read gain/40% write cost. A write-critical service chooses X; an analytical replica may choose Y. Conclusion: the frontier informs a policy decision; it does not encode one universal winner.

## Cross-Program Connections

- [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) supplies constrained search, approximation, Pareto dominance, and experimental complexity.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) supplies workload capture, replay, privacy-safe telemetry, drift, and backfill/reconciliation.
- [Software Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) supplies oracles, experimental design, regression gates, and adversarial coverage.
- [Software Delivery and Reliability Engineering](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) supplies canaries, SLOs, observability, abort thresholds, and rollback.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) supplies tenant/authorization invariants and safe handling of query/parameter evidence.

## References

1. PostgreSQL Global Development Group, [The Cumulative Statistics System](https://www.postgresql.org/docs/current/monitoring-stats.html), current `pg_stat_all_indexes` definitions and caveats.
2. PostgreSQL Global Development Group, [Using EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html), current plan estimates, execution, loops/searches, buffers, and measurement guidance.
3. PostgreSQL Global Development Group, [Multicolumn Indexes](https://www.postgresql.org/docs/current/indexes-multicolumn.html), current column-order, skip-scan, and access-method guidance.
4. Oracle, [MySQL 8.4 Invisible Indexes](https://dev.mysql.com/doc/refman/8.4/en/invisible-indexes.html), current visibility, optimizer, maintenance, uniqueness, and primary-index semantics.
5. SQLite Project, [Query Planning](https://www.sqlite.org/queryplanner.html), official search, multi-column, covering, OR, sorting, and statistics explanation.
6. Surajit Chaudhuri and Vivek Narasayya, [“An Efficient Cost-Driven Index Selection Tool for Microsoft SQL Server”](https://www.vldb.org/conf/1997/P146.PDF), *VLDB*, 1997.
7. Nicolas Bruno and Surajit Chaudhuri, [“Automatic Physical Database Tuning: A Relaxation-based Approach”](https://www.microsoft.com/en-us/research/wp-content/uploads/2005/01/newdta.pdf), *SIGMOD*, 2005.
8. Sanjay Agrawal, Eric Chu, and Vivek Narasayya, [“Automating Physical Database Design: Workload as a Sequence”](https://www.microsoft.com/en-us/research/publication/automating-physical-database-design-workload-as-a-sequence/), *SIGMOD*, 2006.
9. K. Schnaitter et al., [“COLT: Continuous On-Line Database Tuning”](https://www.vldb.org/pvldb/1/1454179.pdf), *PVLDB* 1(1), 2008.
10. Andrew Pavlo et al., [“Self-Driving Database Management Systems”](https://db.cs.cmu.edu/papers/2017/p42-pavlo-cidr17.pdf), *CIDR*, 2017, workload forecasting, planning, deployment, and feedback architecture.

## Exercises

### Exercise 1

Normalize a mixed workload of equality/range/join/order/aggregate queries plus inserts, indexed/unindexed updates, deletes, and a rare incident query. Define fingerprints, parameter classes, slices, weights, privacy controls, and hard gates.

### Exercise 2

Given four candidates with a table of per-query costs, storage/write/build costs, one uniqueness requirement, and budgets, enumerate feasible portfolios, compute marginal benefits in two contexts, and identify the Pareto frontier.

### Exercise 3

An advisor predicts 70% benefit, but replay produces 15% median gain, worse p99 writes, two result-order differences, and a replica lag spike. Diagnose estimate, correctness, experiment, and operational causes; state the release decision.

### Exercise 4

Design a safe create-and-drop rollout using hypothetical/materialized indexes, invisible indexes where supported, concurrent build, canary sessions, semantic validation, abort gates, recreation, replicas, crash/cancel, and audit evidence.

### Exercise 5

Design a continuous but non-oscillating index-governance system for a multi-tenant evolving database. Include authority, data minimization, drift, uncertainty, budgets, hysteresis, rare paths, rollback, and human review.

## Answers to the Exercises

### Answer 1

Fingerprint by plan-relevant relational shape: tables/joins/operators/projection/order/group/LIMIT/lock/isolation and mutation target, while replacing raw literals. Split parameters by selectivity/skew (common/rare, tenant size, recent/history, empty/dense partition) and prepared/custom plan regime. Slice by tenant tier, API/job, primary/replica, role, hour/season/release and timeout/censoring. Weight execution count and resource share but add explicit business/SLO/rare-incident importance; include concurrency/sequence. Retain sampled/synthetic buckets or one-way identifiers under access/retention controls, never secrets/raw personal values. Hard gates include exact results/order contract, uniqueness/foreign/security semantics, critical-template p99, write/lag/headroom, recovery, and rollback. Record capture range, sampling, resets, failures, and uncovered slices.

### Answer 2

First reject every set missing the unique index or exceeding storage, write, or build budget. For each remaining `X`, sum `w_q C(q,X)` using configuration costs—not individual savings—then retain separate write/storage/build objectives or apply declared normalized coefficients. Compute `Δ(a|X)=Cost(W,X)-Cost(W,X∪{a})` for two different `X`; differing values demonstrate interaction. Configuration Y is dominated if another feasible X is no worse on query cost, write, storage, build, and risk and better on at least one. The frontier is every nondominated feasible set. A complete answer lists all sets/calculations and then applies the stated service policy; it never trades away uniqueness through a finite weight or adds optimizer cost directly to bytes without normalization.

### Answer 3

Block release immediately because result-order differences may violate semantics and p99/replica gates fail, regardless of median. Check whether order was contractually deterministic/tie-broken, result multisets match, collation/NULL/snapshot differ, or replay is faulty. Compare estimated/actual rows, join order, scans/fetches/rechecks, spills, cache, parameters, statistics, generic/custom plans, and advisor workload/engine version. Inspect DML fan-out, WAL, checkpoint/maintenance, shared I/O, replica apply, build catch-up, run order and duration. The 70% is model-relative, not milliseconds. Repair oracle/definition/experiment, include steady-state writes and lag, rerun repeated controlled slices, and release only if correctness and every hard gate pass with uncertainty bounds; otherwise reject/reshape the candidate.

### Answer 4

Freeze definitions, engine/config, baseline workload/data/statistics, constraints, plans/results, SLOs and resource budgets. Use hypothetical indexes only to prune. Build the exact candidate on a representative clone and run correctness plus concurrent steady-state replay. In production use documented online/concurrent construction with lock/WAL/space/replica/cancel monitoring; validate the built artifact. If supported, keep additions invisible and enable only selected canary sessions, or route a tenant/shard canary. For removal, prove no semantic dependency, observe all roles/seasons, make invisible first, and note maintenance continues. Abort on result/error/constraint, critical-plan, p99, timeout, write, lag, debt, or headroom gates. Visibility restores plans quickly; dropped-index rollback requires tested recreation time/capacity. Handle crash/invalid artifacts explicitly, retain audit inputs/results/approvals, and drop old state only after the evidence window.

### Answer 5

Collect minimized fingerprint/parameter-class/plan/resource telemetry with tenant access controls, sampling provenance, retention, and reset markers. Detect distribution, data/statistics, SLO, schema/query, engine/hardware, and maintenance drift using minimum sample/effect thresholds and uncertainty. Generate bounded canonical candidates; protect semantic and rare critical indexes as hard constraints. Evaluate interactions with what-if, then scheduled clone replay; automation may recommend or canary only within explicit authority, storage/write/build/concurrency budgets and rate limits. Require improvement beyond confidence plus change/rebuild cost, persist for multiple windows, enforce cooldown/hysteresis, and cap changes per table to prevent oscillation. Use tenant/failure slices and fairness gates. Every change has owner, approval, digest/version, canary, abort, rollback/recreation, expiry, and post-change comparison. Humans decide infeasible or high-risk tradeoffs; the system never silently drops constraints or expands external mutation authority.
