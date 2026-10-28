---
module_id: DBE-064
program: Database Engineering
level: 2
module_number: 64
title: Cardinality Estimation
status: complete
last_verified: 2026-08-30
---

# Cardinality Estimation

## One-Page Review

### Governing question

How can an optimizer estimate the row occurrences produced at every logical and physical boundary, expose the assumptions and uncertainty behind those estimates, and improve plan decisions when exact evaluation would itself execute the query?

### Essential definitions

**Cardinality** is row-occurrence count for a declared operator boundary and loop/worker convention. **Selectivity** is output/input occurrences for a predicate-like operator. **Fanout** is output matches per input occurrence. A **base estimate** describes a scan population; a **derived estimate** propagates through operators. **Uniformity**, **independence**, **containment**, and **inclusion** are modeling assumptions, not facts. **Q-error** is symmetric multiplicative error for positive estimates and actuals. **Correlation** is dependence among predicates/columns/tables. A **query-driven learned estimator** learns from labeled queries; a **data-driven estimator** models data distributions. **Out-of-distribution (OOD)** input differs materially from training/summary coverage. **CE feedback** revises assumptions or estimates using executions. A **cardinality interval** expresses plausible bounds rather than one point.

### Central model, mechanism, or theorem

Annotate every expression v with an estimate `E(v)`, provenance, assumptions, and bounds. A filter commonly uses `E_out=E_in*s`. A uniform equijoin heuristic is `E=E(R)*E(S)/max(NDV_R,NDV_S)` under compatible non-null domains and containment assumptions. Group count is bounded by input rows and the joint NDV of grouping expressions. Local multiplicative error can propagate or amplify across joins: an eightfold underestimation before a threefold fanout remains eightfold afterward, while interacting errors can become much larger. Exact semantic lower/upper bounds, constraints, and row-goal behavior should constrain formulas.

### Critical invariants

- Each estimate names operator, expression bindings, predicate/parameters, input estimates, statistics/model generation, data snapshot, and aggregation convention.
- Estimates are nonnegative; semantic bounds such as filter output no greater than input and semi-join output no greater than left input are enforced.
- Nulls, bags, join kind, duplicate multiplicity, residual predicates, loops, workers, limits, and early termination are explicit.
- Keys, foreign keys, CHECK/partition constraints, uniqueness, and functional dependencies are used only when enforced and valid for the query.
- Independence, uniformity, containment, inclusion, interpolation, and fallback defaults are tagged and observable.
- Actual rows are compared at corresponding nodes; “never executed,” per-loop averages, row goals, and cancellation are not treated as ordinary actual totals.
- Zero actual/estimate cases have categorical policy; arbitrary epsilons do not manufacture finite accuracy.
- Learned and feedback estimators have training/coverage, drift, latency, resource, privacy, tenant, version, and safe-fallback contracts.

### Common failures

Failures include multiplying correlated selectivities; using `1/NDV` for heavy hitters; assuming filtered join-key distributions equal base distributions; confusing foreign-key integrity with uniform fanout; ignoring null and unmatched outer rows; estimating GROUP BY as a product of single-column NDVs; applying limit as universal cardinality rather than demand; comparing parent actual rows after early stop to full-consumption estimates; using average q-error; training/test leakage; silent OOD extrapolation; feedback from only completed cheap plans; or improving point estimates without improving selected plans or workload outcomes.

### Compact example

A finite population has 100 customers, 10 in SE, and 1,000 orders, 200 open. Independence predicts `1000*0.2*0.1=20` open-SE orders. But 160 of the open orders belong to SE customers, so q-error is 8. Adding exactly three line items per qualifying order yields estimate 60 versus actual 480; the upstream correlation error persists. The executable reproduces these counts and keeps zero cases separate.

### Connections

Retrieve [Statistics and Histograms](063-statistics-and-histograms.md), [Joins and Join Semantics](012-joins-and-join-semantics.md), [Logical and Physical Plans](051-logical-and-physical-plans.md), and [Profiling a Query Operator Pipeline](060-profiling-a-query-operator-pipeline.md). Continue through [the roadmap](../ROADMAP.md) to cost models, join ordering, access paths, parameter sensitivity, adaptation, and plan diagnosis.

## Governing Question

An optimizer compares plans before executing them. Exact intermediate row counts are generally as hard to obtain as running the alternatives, so it predicts them. How should it turn base statistics, constraints, predicates, join graphs, parameter classes, samples, models, and feedback into estimates whose meaning, uncertainty, failure modes, and decision consequences are inspectable?

Cardinality estimation is not one formula at the root. It is compositional inference over a plan DAG. Every scan, filter, join, aggregate, window, union, exchange, and limit changes the row population. The estimator must preserve bag multiplicity and operator semantics while compressing a high-dimensional joint distribution into bounded planning work.

The quality objective is not “small average row error.” It is choosing robust plans under planning latency and resource limits. A twofold error at a memory-spill threshold can be decisive; a hundredfold error on an irrelevant one-row leaf may not change anything. Evaluation therefore connects node estimates to alternatives, costs, memory, distribution, and end-to-end workload outcomes.

## Why This Matters

Cardinality drives access path, join algorithm/order, build side, parallelism, exchange partitioning, memory grants, admission, materialization, compilation, and row-goal decisions. Underestimate a hash build and it spills; underestimate an inner side and nested loops repeat unexpected work; underestimate a distributed join and a broadcast overwhelms workers. Overestimate and the optimizer may scan instead of seek, reserve scarce memory, or reject useful parallel work.

Errors are correlated across a tree because a parent's estimate consumes its children's estimates. The 1991 Ioannidis and Christodoulakis paper formalized how join-size errors propagate. The 2015 Leis et al. study separated cardinality, cost, and enumeration effects on the Join Order Benchmark and found cardinality errors could dominate cost-model errors in that studied setting. Neither result means cardinality is always the only problem; it means evaluation must isolate components and full-plan consequences.

Classical estimators remain valuable because they are fast, interpretable, and robust on ordinary shapes. Histograms, MCVs, NDV, constraints, and extended statistics often solve the important local errors. Samples and sketches handle selected gaps. Learned methods can represent wider correlations but introduce training, drift, inference, coverage, and operational surfaces. An elite system composes exact facts, interpretable estimates, specialized models, uncertainty, and fallback rather than replacing one monolith with another.

## Prerequisites and Retrieval

You should understand relational algebra, bags/nulls, joins and outer joins, statistics/histograms, conditional probability, query plans, and profiling. Recall that DBE-063 distinguishes a summary from the estimator consuming it.

Retrieve: base/derived cardinality; selectivity; NDV; MCV; fanout; conditional distribution; uniformity; independence/correlation; inclusion/containment; key/foreign key; joint NDV; row goal; actual rows/loops; q-error; signed log error; zero category; workload/decision-weighted metric; query-driven/data-driven model; OOD; calibration; feedback; uncertainty interval; and robust plan.

## Learning Objectives

After this module, you can:

1. define estimator inputs, output boundary, provenance, assumptions, and bounds;
2. derive scan, filter, conjunction/disjunction, join, aggregate, set, and limit estimates;
3. distinguish uniformity, independence, inclusion, and containment assumptions;
4. use keys, foreign keys, nullability, functional dependencies, and joint statistics safely;
5. trace cardinality and q-error propagation through multi-operator plans;
6. diagnose parameter, skew, correlation, out-of-range, and join-crossing failures;
7. compare synopsis-, sampling-, feedback-, query-driven-, and data-driven estimators;
8. design zero-aware, coverage-aware, decision-aware evaluation;
9. add uncertainty, fallback, privacy, resource, and version controls; and
10. deploy estimator changes through reproducible shadowing, canaries, rollback, and regression gates.

## Core Exposition

**Define the estimated event.** For node v, record logical/physical operator, input populations, output schema, predicate/join/group expressions, parameter values or privacy-safe class, requested row goal, loops/workers/partitions, statistics/model generation, data snapshot/epoch, and whether E is total occurrences, per loop, per worker, distinct groups, batches, or bytes. A bare `rows=100` is ambiguous.

Associate a provenance expression with E: exact constraint; catalog-scaled base count; MCV lookup; histogram interpolation; residual uniformity; independence product; join containment; sample; sketch; learned model; feedback; default; clamp; or composite. Capture lower/upper bounds and a confidence/coverage indicator where meaningful. This turns estimation into inspectable inference.

**Base scans.** Estimate visible table/partition rows from a compatible catalog population, scaling only according to the engine's documented model. PostgreSQL 18's row-estimation examples describe scaling stored tuples when current pages differ. Partition/file pruning can make a base estimate conditional on known parameters. Visibility, snapshots, deletes, row policies, and remote source counts affect the population.

**Filters.** A filter uses `E_out=E_in*s`, clamped to semantic bounds. Equality may use MCV mass, residual `mass/NDV`, exact uniqueness, or default. Ranges use histogram integration. `IS NULL` uses null fraction. `IN`/OR requires union of events and overlap accounting; adding selectivities can exceed one or double-count. Negation uses the correct SQL TRUE/FALSE/UNKNOWN population, not naïve `1-s` if null/unknown semantics differ.

For conjunction `p AND q`, independence uses `s_p*s_q`. Perfect positive correlation may use approximately `min(s_p,s_q)` for compatible nested events; mutual exclusion gives zero. Exponential backoff and damping sit between extremes. Current SQL Server documentation explicitly names independence, uniformity, containment, inclusion, and later correlation/base-containment assumptions; these are model versions with workload trade-offs, not SQL guarantees.

Extended MCVs, dependencies, expression statistics, and constraints can replace defaults for supported forms. PostgreSQL 18 currently documents multivariate dependency/MCV/NDV statistics but notes extended statistics are not used for join selectivity. Product limitations belong in estimator provenance.

**Inner equijoins.** A common heuristic under uniform compatible domains is

`E_join = E_R * E_S / max(NDV_R(k), NDV_S(k))`.

It assumes non-null join values spread uniformly and a containment relationship. More explicit frequency reasoning sums `freq_R(v)*freq_S(v)` across values, using joint MCVs plus residual models. Null equality matches no nulls under ordinary `=`. Composite keys need joint, not multiplied, NDV. Non-equi, interval, spatial, temporal, expression, and user-defined joins require specialized estimators.

A declared primary-key/foreign-key relationship proves each non-null valid foreign-key occurrence has one parent match. It does not prove filters are independent of the key, uniform fanout by parent, or that a filtered parent retains a base fraction of child rows. If open orders concentrate in one country, filtering order status and customer country is a join-crossing correlation.

**Join kinds impose bounds.** Inner join lower bound is generally zero and upper bound `E_R*E_S` absent stronger facts. Left outer output is at least the left input under full consumption, and at most inner matches plus unmatched left occurrences. Semi-join output lies `[0,E_R]` and counts each left occurrence once if any match. Anti-join also lies `[0,E_R]`. Full outer includes unmatched occurrences from both sides. Null-aware anti/mark semantics require separate truth states.

**Other operators.** Projection preserves bag row count unless duplicate elimination occurs. DISTINCT/GROUP BY output is bounded by input rows and joint NDV of expressions; multiply single-column NDVs only under an explicit independence model, then clamp. Aggregate without GROUP BY normally emits one row even on empty input, subject to grouping-set semantics. `UNION ALL` sums inputs; `UNION DISTINCT`, INTERSECT, and EXCEPT need overlap/distinct models. Unnest/set-returning functions introduce per-row fanout distributions. Recursive queries require termination/iteration models or guarded caps.

LIMIT's output under full child availability is `min(input,limit)` after offset rules, but a row goal also changes how much work the parent requests. An `EXPLAIN ANALYZE` node may show fewer actual child rows because execution stopped early; PostgreSQL 18 explicitly documents such a discrepancy as not necessarily estimation error. Compare identical consumption boundaries.

The executable constructs a finite correlated population and compares it with an independence estimator.

<!-- bijux-verify: {"id":"correlated-cardinality-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"customers=100\norders=1000\nopen_orders=200\nse_customers=10\nindependent_join_estimate=20\nactual_join_rows=160\njoin_q_error=8.0\nestimated_lineitems=60\nactual_lineitems=480\nlineitem_q_error=8.0\nactual_groups=10\nzero_policy=separate\nevidence=finite_correlated_population\n","stderr":""}} -->
```python
customers = tuple(range(100))
se_customers = set(range(10))

open_orders = tuple(
    list(range(10))[index % 10] if index < 160 else 10 + (index % 90)
    for index in range(200)
)
closed_orders = tuple(index % 100 for index in range(800))
orders = tuple((customer_id, "open") for customer_id in open_orders) + tuple(
    (customer_id, "closed") for customer_id in closed_orders
)

open_fraction = sum(status == "open" for _, status in orders) / len(orders)
se_fraction = len(se_customers) / len(customers)
independent_estimate = round(len(orders) * open_fraction * se_fraction)
actual = sum(status == "open" and customer_id in se_customers
             for customer_id, status in orders)
join_q_error = max(actual / independent_estimate, independent_estimate / actual)

lineitems_per_order = 3
estimated_lineitems = independent_estimate * lineitems_per_order
actual_lineitems = actual * lineitems_per_order
actual_groups = len({customer_id for customer_id, status in orders
                     if status == "open" and customer_id in se_customers})

print(f"customers={len(customers)}")
print(f"orders={len(orders)}")
print(f"open_orders={sum(status == 'open' for _, status in orders)}")
print(f"se_customers={len(se_customers)}")
print(f"independent_join_estimate={independent_estimate}")
print(f"actual_join_rows={actual}")
print(f"join_q_error={join_q_error:.1f}")
print(f"estimated_lineitems={estimated_lineitems}")
print(f"actual_lineitems={actual_lineitems}")
print(f"lineitem_q_error={max(actual_lineitems / estimated_lineitems, estimated_lineitems / actual_lineitems):.1f}")
print(f"actual_groups={actual_groups}")
print("zero_policy=separate")
print("evidence=finite_correlated_population")
```

The estimator knows both marginal fractions exactly and is still eightfold wrong because the conjunction crosses the join. Multiplying both actual and estimated rows by exact fanout three preserves q-error. Other operators can attenuate, clamp, or amplify error; there is no universal monotone rule for q-error through arbitrary plans.

**Trace first divergence.** Bind machine-readable plans before and after execution. Normalize tool semantics for actual rows and loops. Starting at leaves, compute estimate/actual and identify the earliest material discrepancy, not merely the largest root error. Inspect predicates, parameter, histogram/MCV, dependencies, join-key distributions after filters, nulls, constraints, partition scope, sample/model coverage, and row goal.

If a child estimate is correct but join output is wrong, the missing fact is likely join overlap/fanout/correlation rather than stale base row count. If a scan is wrong only for one parameter class, inspect heavy hitters and plan caching. If errors appear after a projection expression, check expression statistics and casts. If grouping is wrong with accurate input, inspect joint NDV and functional dependencies.

**Error metrics need policy.** For positive E,A, `q=max(E/A,A/E)`. Signed log error preserves direction: `log(E/A)`. Absolute error captures resource magnitude. Relative error is unstable near zero. Treat `(0,0)`, `(0,A>0)`, and `(E>0,0)` as explicit categories; optimizers often clamp to a small nonzero estimate for search stability, but evaluation must retain the unclamped semantic case.

Report distributions by operator/query shape, join count, parameter class, actual-cardinality scale, data/time split, and OOD status. Include median, p90/p95/p99, maximum with minimized examples, under/over direction, zero categories, and coverage. Weight by optimizer decisions: plan regret versus an oracle/better-known alternative, spill/broadcast/admission threshold crossings, memory error, and end-to-end workload latency/throughput. Q-error alone may not predict plan quality; CardEst benchmark work has highlighted this limitation.

**Sampling approaches.** Base-table samples answer predicates cheaply when sample hits exist, but zero qualifying sample rows produce weak upper information and joins can encode correlations absent from independent samples. Join sampling, wander joins, or sampling-based reoptimization target multi-table distributions at extra planning/runtime cost. Cache sample results only with data/query/predicate/version identity. Do not issue hidden expensive probes on production sources without budgets.

**Learned estimators.** Query-driven models map featurized tables/joins/predicates plus labels to cardinality; MSCN is a primary example combining query features and samples. They can learn workload correlations but face cold start, label cost, training-query distribution, unseen constants/operators/shapes, and feedback selection.

Data-driven models approximate table or join distributions and integrate query predicates; NeuroCard is a primary multi-table autoregressive example. They aim to answer broader query sets without a representative query workload, but face model build/update, schema/join-graph assumptions, high-cardinality representation, inference variance/latency, drift, and difficult explainability. Neither category removes null/bag/join semantic engineering.

For any model, version feature encoding, schemas, training data/snapshot, labels, split strategy, seed, code/model artifact, hyperparameters, calibration, inference hardware, and supported grammar. Detect OOD columns/constants/ranges/shapes and missing features. Produce bounds/confidence or at least coverage scores calibrated on held-out time/databases, and fall back to classical facts/defaults. Do not trust a point estimate because a neural network emitted it.

Benchmarks must prevent query/template/data leakage. Randomly splitting queries from the same templates can exaggerate generalization. Use template, time, parameter-domain, schema, and cross-database splits appropriate to the claim. CardBench was introduced to broaden learned-CE evaluation across many real-world databases; it still cannot represent every production distribution and decision context.

**Uncertainty and robust planning.** Exact constraints yield hard bounds. Samples/models may yield calibrated intervals. Propagate intervals conservatively where practical; dependencies make naïve independent interval arithmetic misleading. When plausible cardinalities cross a plan-choice threshold, select a robust plan, spend bounded extra estimation effort, preserve adaptive escape hatches, or generate parameter-class variants. A fragile point-optimal plan may be worse than a slightly higher expected-cost plan across the interval.

Parameter-sensitive estimates should not be averaged into one universal plan. Classify heavy hitters, ranges, tenant sizes, null/non-null, and recent/out-of-range values. Bind cached plans to generic/custom policy and statistics/model generation. DBE-068 will develop plan caching; here the invariant is that the estimator declares whether parameters are known, sniffed, bucketed, or unknown.

**Feedback and adaptation.** Current SQL Server documentation describes persisted CE feedback for repeating queries in selected correlation, containment, and row-goal scenarios, with regression verification. General feedback systems should bind actuals to normalized query/subplan, parameters/class, plan, data/statistics/model generation, engine version, execution completeness, and resource context. Separate one-off runtime adaptation from durable model update.

Feedback is censored by chosen plans, admission, timeouts, cancellations, and caching. Include failures and coverage, bound tenant influence, decay stale evidence, and validate on a control cohort. Never let a single noisy execution rewrite global estimates without safeguards. Privacy applies to query texts, literals, distributions, model membership, and labels.

**Productionize estimator changes.** Run deterministic semantic/unit tests, finite exhaustive populations, randomized differential generation, benchmark suites, historical plan replay, and shadow estimation. Compare old/new estimates without changing plans first. Then simulate or cost alternative plans, canary selected fingerprints/tenants, and observe planning latency/memory, plan changes, execution distributions, resource/spill/exchange outcomes, and regressions. Keep model/rule version switches and rollback.

An estimate can improve while the plan worsens because the cost model or search changes. Conversely, a worse point estimate can choose the same or better robust plan. Handoff must state estimator coverage, fallbacks, zero policy, known unsupported operators, model/data age, and whether performance—not just q-error—was verified.

## Definitions and Notation

- **E(v), A(v)**: estimated and actual row occurrences for node v under one convention.
- **s(p|X)**: selectivity of predicate p conditional on population X.
- **F(R->S)**: match fanout distribution from R occurrences to S.
- **NDV_R(k)**: estimated non-null distinct join keys in R's relevant population.
- **Q(E,A)**: `max(E/A,A/E)` for positive values.
- **Signed log error**: `log(E/A)`, negative for underestimation.
- **Point estimate**: one predicted cardinality.
- **Cardinality interval**: lower/upper plausible cardinality with stated coverage semantics.
- **Query-driven estimator**: model trained from query features and cardinality labels.
- **Data-driven estimator**: model of data/join distributions queried for cardinality.
- **OOD**: input outside declared training/statistical coverage.
- **Plan regret**: workload cost difference between chosen plan and a reference best available alternative under actual execution/evidence.

Every operator formula uses conditional input populations. Base-table NDV is not automatically filtered-input NDV; marginal distributions are not automatically joint distributions.

## Mechanisms, Invariants, or Proof Structure

**Semantic bounds.** Filter and semi/anti join output cannot exceed their relevant input under full consumption. DISTINCT/group count cannot exceed input rows. `UNION ALL` is additive. Outer joins preserve unmatched-side lower bounds. Apply exact zero from contradictory enforced constraints when the operator semantics permit it.

**Uniform join derivation.** If R and S have compatible domains, every non-null key is equally frequent, and the smaller domain is contained in the larger, expected matches per key produce `|R||S|/max(NDV_R,NDV_S)`. Violate frequency uniformity, overlap/containment, or filtered-distribution assumptions and the formula loses justification.

**Correlation counterexample.** The executable fixes marginals `P(open)=0.2` and `P(SE customer)=0.1` but constructs `P(open AND SE)=0.16`. Any estimator using only those marginals cannot distinguish this population from an independent one. Joint information or a modeling assumption is necessary.

**Error propagation.** If a downstream operator multiplies both estimate and actual by the same positive exact fanout, q-error is unchanged. If fanout is also estimated with correlated error, ratios multiply/divide. Clamps, outer lower bounds, limits, and duplicate elimination can alter direction and magnitude. Trace algebraically per operator rather than asserting universal exponential growth.

**Estimator precedence.** Exact constraints/bounds dominate compatible statistics; specialized joint/MCV/expression evidence dominates generic independence; validated sample/model evidence applies within coverage; fallback applies otherwise. Combining evidence must avoid double counting and record provenance.

**Evaluation separation.** Training and validation differ by query template, time, parameter domain, and database according to the generalization claim. Actual labels exclude or separately classify partial/cancelled/row-goal executions. Semantic, estimate, plan-choice, and performance evaluations are separate gates.

**Deployment invariant.** A model/rule generation is immutable and rollbackable, has resource and latency limits, returns supported/bounded/fallback status, and cannot silently alter plans outside its canary scope. Security and tenant policies constrain features, labels, logs, and feedback.

## Alternatives and Trade-Offs

**Classical synopses** are fast, compact, explainable, and locally maintainable; they miss high-dimensional and join-crossing correlations.

**Constraints** yield exact bounds and transformations when enforced; they cover fewer distributions and cannot encode merely typical behavior.

**Sampling** sees current data and arbitrary predicates; rare/zero hits, join sampling cost, source load, latency, and caching complicate use.

**Query-driven models** target workload patterns and can learn plan-shape correlations; they risk cold start, template leakage, feedback bias, and poor unseen-query generalization.

**Data-driven models** target broader queries by modeling distributions; they face schema/data updates, high-dimensional integration, inference cost, and OOD support.

**Feedback** adapts repeating queries and assumptions; it learns after mistakes, can be censored/poisoned, and requires stable identity and regression verification.

**Point estimates** integrate easily with existing optimizers. **Intervals/distributions** support robust choices but increase propagation/search complexity and require calibration.

**Plan-independent q-error** is comparable and easy. **Decision/plan-regret metrics** better reflect optimizer value but require executing/costing alternatives and carefully controlled evidence.

## Failure Modes and Misconceptions

1. “Fresh statistics make estimates accurate” ignores compression, correlation, and unsupported predicates.
2. “Join rows are product divided by max NDV” hides uniformity and containment premises.
3. “A foreign key fixes join cardinality” not after correlated filters or for fanout distribution.
4. “Selectivities multiply” only under conditional independence.
5. “Minimum selectivity is correlation” it is a model extreme, not evidence of actual joint mass.
6. “Limit actual rows prove overestimation” early stop changes the observed work boundary.
7. “Q-error handles zero with epsilon” arbitrary epsilon changes rankings and meaning.
8. “Median q-error proves quality” tails, coverage, direction, scale, and decisions may fail.
9. “Better estimates guarantee better plans” cost/search/runtime and thresholds mediate benefit.
10. “Learned estimators capture all correlations” only within representation, training/data, grammar, and inference limits.
11. “Random query splits test generalization” template/parameter leakage can make them nearly duplicates.
12. “Feedback labels are unbiased” chosen plans, timeouts, admission, and tenants select observations.
13. “One model serves all tenants safely” distributions, privacy, poisoning, fairness, and resource isolation differ.
14. “Fallback is failure” explicit conservative fallback is a correctness and availability feature.

## Worked Examples

### Example 1

**MCV equality.** N=1,000,000 and tenant A MCV frequency 0.4 gives E=400,000. `N/NDV` with NDV 10,000 gives 100, a 4,000-fold underestimate. Conclusion: frequent values need explicit mass.

### Example 2

**Independent conjunction.** Marginals 0.2 and 0.1 produce 0.02 under independence. The executable actual is 0.16. Conclusion: exact marginals do not identify joint probability.

### Example 3

**Uniform equijoin.** R has 1,000 rows/100 uniform keys; S has 500 rows/50 uniform keys whose domain is contained in R. Formula gives `1000*500/max(100,50)=5,000`; per contained key it is 10*10 across 50 keys=5,000. Conclusion: the heuristic is derivable under strong premises.

### Example 4

**Disjoint domains.** R and S each have 1,000 rows and 100 keys, but R keys 1–100 and S keys 101–200. Uniform max-NDV gives 10,000 while actual is zero. Conclusion: NDV without overlap/containment cannot establish join size.

### Example 5

**Left outer lower bound.** Left has 100 rows, inner matches total 20 from 10 left rows. Left outer emits 20 matched occurrences plus 90 unmatched null-extended rows=110, not `max(100,20)` by coincidence alone; duplicate matches matter. Conclusion: estimate matched-left distinctness as well as match rows.

### Example 6

**Group joint NDV.** Country NDV=200 and city NDV=50,000, but each city belongs to one country and there are 50,000 observed pairs. Product clamped to N may be far too high; joint NDV is 50,000. Conclusion: GROUP BY needs joint distinctness/dependencies.

### Example 7

**Row-goal mismatch.** Child estimate is 1,000 qualifying rows, but parent LIMIT requests two and stops. Child actual reports two produced rows. Conclusion: compare full-cardinality prediction to an execution that consumed full output, or label row-goal demand separately.

### Example 8

**Error threshold.** A hash build estimated 90 MB but actually 110 MB crosses a 100 MB grant and spills; q-error 1.22. Another leaf estimate 1 versus actual 100 has q-error 100 but stays irrelevant. Conclusion: decision-aware impact complements q-error.

### Example 9

**Learned OOD query.** Training uses equality filters on known columns; production submits range predicates on a new partition with unseen values. A numeric prediction without OOD status is unsafe. Fall back to fresh histogram/sample/default and schedule retraining. Conclusion: coverage is part of the estimator API.

### Example 10

**Production diagnosis.** A broadcast join OOMs only for large tenants. Find the first divergence at a tenant/status join, confirm MCV marginals but missing cross-table correlation, shadow a joint/sample/specialized estimate, compare alternative partitioned join, canary large-tenant fingerprints, and monitor memory/exchange/tails. Conclusion: repair the causal estimate and validate the decision, not merely refresh every statistic.

## Cross-Program Connections

- [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md): approximation, sampling, randomized validation, and robust optimization shape estimators.
- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md): histograms, sketches, samples, indexes, and memo metadata supply compact evidence.
- [Data Engineering](../../19-data-engineering/ROADMAP.md): data drift, partitions, quality, lineage, and incremental refresh determine estimator inputs.
- [Large-Scale Data Systems Engineering](../../21-large-scale-data-systems-engineering/ROADMAP.md): exchanges, broadcast/repartition decisions, skew, and cluster memory amplify cardinality consequences.
- [Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md): split design, differential generation, coverage, metamorphic checks, and regressions establish evidence.
- [Security Engineering](../../25-security-engineering/ROADMAP.md): model/data leakage, tenant isolation, poisoning, access, and privacy constrain learning/feedback.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md): model serving, budgets, canaries, rollback, observability, and multitenancy operationalize CE.

## References

1. Yannis Ioannidis and Stavros Christodoulakis, [“On the Propagation of Errors in the Size of Join Results”](https://www.cs.du.edu/~leut/4423/papers/joinSize.pdf), *SIGMOD 1991*. Primary formal error-propagation analysis.
2. Viktor Leis et al., [“How Good Are Query Optimizers, Really?”](https://vldb.org/pvldb/vol9/p204-leis.pdf), *PVLDB* 9(3), 2015. Primary controlled evaluation of cardinality, cost, and enumeration effects.
3. PostgreSQL Global Development Group, [PostgreSQL 18: Row Estimation Examples](https://www.postgresql.org/docs/18/row-estimation-examples.html), retrieved 2026-08-30. Current base, range, conjunction, and join estimation examples.
4. PostgreSQL Global Development Group, [PostgreSQL 18: `CREATE STATISTICS`](https://www.postgresql.org/docs/18/sql-createstatistics.html), retrieved 2026-08-30. Current dependency/MCV/NDV/expression support and join-estimation limitation.
5. Microsoft, [SQL Server Cardinality Estimation](https://learn.microsoft.com/en-us/sql/relational-databases/performance/cardinality-estimation-sql-server?view=sql-server-ver17), retrieved 2026-08-30. Current CE model assumptions, versions, comparison, and diagnostics.
6. Microsoft, [Cardinality Estimation Feedback](https://learn.microsoft.com/en-us/sql/relational-databases/performance/intelligent-query-processing-cardinality-estimation-feedback?view=sql-server-ver17), retrieved 2026-08-30. Current persisted feedback scenarios and regression verification.
7. Andreas Kipf et al., [“Learned Cardinalities: Estimating Correlated Joins with Deep Learning”](https://www.cidrdb.org/cidr2019/papers/p101-kipf-cidr19.pdf), *CIDR 2019*. Primary query-driven MSCN estimator.
8. Zongheng Yang et al., [“NeuroCard: One Cardinality Estimator for All Tables”](https://vldb.org/pvldb/vol14/p61-yang.pdf), *PVLDB* 14(1), 2021. Primary data-driven multi-table estimator.
9. Apache Calcite Project, [`RelMetadataQuery`](https://calcite.apache.org/javadocAggregate/org/apache/calcite/rel/metadata/RelMetadataQuery.html), retrieved 2026-08-30. Current extensible row-count, selectivity, distinctness, population, and metadata interface.
10. Andreas Kipf et al., [“CardBench: A Benchmark for Learned Cardinality Estimation in Relational Databases”](https://arxiv.org/abs/2408.16170), 2024. Primary multi-database learned-CE benchmark design.
11. Benjamin Hilprecht and Carsten Binnig, [“Are We Ready For Learned Cardinality Estimation?”](https://arxiv.org/abs/2012.06743), 2020. Primary deployment-readiness analysis covering accuracy, robustness, and cost dimensions.

## Exercises

### Exercise 1

Derive the uniform equijoin formula from per-key frequencies. State null, overlap/containment, uniformity, filtering, bag, and composite-key premises.

### Exercise 2

Given estimates/actuals `(0,0)`, `(0,10)`, `(10,0)`, `(20,160)`, and `(1,100)`, classify zeros, compute positive q-errors and signed log directions, and explain why one aggregate average is invalid.

### Exercise 3

A `GROUP BY country,city` estimate is N after multiplying NDVs, while actual groups are 50,000. Diagnose with constraints/statistics and design a correction plus held-out validation.

### Exercise 4

Compare classical synopses, online sampling, query-driven MSCN-like, data-driven NeuroCard-like, and CE feedback for a changing multitenant workload. State coverage, latency, refresh, security, and fallback contracts.

### Exercise 5

Design an elite CE evaluation and rollout system that proves semantic alignment, estimate quality, plan benefit, performance, resource safety, OOD behavior, privacy, canary containment, and rollback—without claiming universal optimality.

## Answers to the Exercises

### Answer 1

Let d_R,d_S be compatible non-null NDVs, with the smaller key set contained in the larger. Uniform frequencies are `|R|/d_R` and `|S|/d_S`; the intersection contains `min(d_R,d_S)` keys. Join rows are `min(d_R,d_S)*(|R|/d_R)*(|S|/d_S)=|R||S|/max(d_R,d_S)`. Inputs are bags, so occurrence frequencies multiply. Ordinary `=` excludes nulls or uses non-null counts. Key equality/types/collation agree; each filtered input retains the modeled uniform key distribution; domains satisfy containment; frequencies are uniform; NDVs are joint for composite keys; and no residual predicate changes output. Without overlap, frequency, or conditional-distribution evidence the formula is heuristic, not identity.

### Answer 2

`(0,0)` is exact-zero; `(0,10)` is missed-nonzero/infinite underestimation; `(10,0)` is false-positive/infinite overestimation. Do not add epsilon. For `(20,160)`, q-error is 8 and signed log `log(20/160)=log(0.125)<0`, underestimation. For `(1,100)`, q-error is 100 and signed log is negative. An arithmetic mean cannot mix finite factors with categorical infinities meaningfully; even finite q-errors lose direction and cardinality/decision scale. Report zero categories, finite distribution/tails, signed direction, actual scale, operator/shape coverage, and plan/resource consequences.

### Answer 3

Check input E/A, bound expressions, nulls, filters, data/statistics generation, and whether each city belongs to one country. Single NDVs 200 and 50,000 multiplied imply ten million combinations and clamp to N, but a functional dependency city→country or joint NDV can establish about 50,000 observed pairs. Use an enforced semantic constraint only if the business rule is absolute; otherwise collect multivariate NDV/dependency statistics on the exact bound expressions under the supported product/version. Re-estimate and compare held-out countries/cities, nulls, duplicate city names across countries, recent partitions, rare/out-of-domain values, parameter classes, planning cost, chosen aggregation strategy, memory/spill, and workload tails. A better group estimate must not be generalized to unsupported join selectivity.

### Answer 4

Classical histograms/MCVs/NDV/constraints are low-latency and interpretable but miss high-dimensional cross-table dependence. Online sampling sees current predicates and data but costs source work, struggles on zero hits/joins, and needs snapshot/cache budgets. A query-driven model learns query-shape/workload correlations but requires labels, cold-start/OOD detection, template/time splits, and protection from tenant/feedback bias. A data-driven model targets broader queries by learning data/join distributions but needs schema-aware training, updates, inference limits, and join-graph/grammar coverage. CE feedback cheaply adapts repeating queries after observed errors but is delayed/censored and must verify regressions. Compose them: exact facts first, classical baseline, bounded specialized sample/model when covered, feedback under stable identity, and explicit fallback otherwise. Version all artifacts; cap planning latency/memory/source work; isolate tenant data/labels; redact/control literals and models; detect drift/OOD; and retain old generation/plan controls.

### Answer 5

Define canonical operator/row/loop/worker/row-goal semantics and verify plans against finite reference execution before measuring estimates. Retain estimator provenance, assumptions, bounds, parameters, data/statistics/model versions, coverage/OOD/fallback, and actual completeness. Test deterministic formulas/bounds, exhaustive small bags/nulls/joins/groups, randomized differential queries, constraints and metadata faults, zero cases, and model serving failures. Split by template, parameter domain, time, schema/database, and tenant according to claims. Report node q-error distributions, direction, zeros, actual scale, coverage, calibration, inference/planning latency/memory, and first divergences. Replay plan search/costs, execute selected alternatives safely, measure regret, spill/memory/exchange/admission and end-to-end distributions. Shadow old/new estimates, then canary scoped fingerprints/tenants with budgets, result checks, control cohort, kill switch, immutable generations, and rollback. Threat-model feature/label/model leakage and poisoning; least-privilege and tenant-isolate. The evidence supports named grammars, versions, data/workload splits, and environments only; it does not prove all-query accuracy, global plan optimality, universal performance, privacy, or deployment fitness, and external review requires named humans.
