---
module_id: DBE-065
program: Database Engineering
level: 2
module_number: 65
title: Cost Models
status: complete
last_verified: 2026-08-30
---

# Cost Models

## One-Page Review

### Governing question

How should a query optimizer translate an incomplete prediction of work and resource demand into a comparable, inspectable score that selects a useful execution plan without confusing the score with elapsed time or a performance guarantee?

### Essential definitions

A **cost model** maps a candidate physical plan, estimated properties, environment, and objective to a cost vector or ordering. **Startup cost** is work before the first useful row; **total cost** is work under full consumption. A **resource vector** separates CPU, I/O, network, memory, and other demands. **Scalarization** maps multiple dimensions to one order using declared units and weights. A **physical property** is an execution-relevant condition such as ordering, partitioning, locality, or rewindability. An **enforcer** obtains a missing property, for example by sorting or exchanging. A **feasibility constraint** rejects plans that cannot satisfy correctness or hard resource requirements. **Calibration** estimates model parameters from controlled measurements. **Plan regret** compares the realized outcome of the selected plan with a reference alternative. **Robustness** is low sensitivity to plausible estimation or environment error.

### Central model, mechanism, or theorem

For plan P, context x, and objective O, form `C(P|x)=(startup,total,cpu,io,network,peak_memory,money,risk,...)`. First reject infeasible plans and plans lacking required physical properties. Compare remaining candidates by the objective: first-row latency, full-result latency, throughput, resource budget, monetary cost, robustness, or a documented combination. Add serial work, take the critical path across genuine parallel work, model blocking boundaries, and avoid double-counting child costs. A scalar score preserves an ordering only for its declared weights and workload; multiplying every scalar component by the same positive constant preserves that ordering.

### Critical invariants

- Cost is attached to a precise plan, required properties, cardinality/width estimates, parameter class, storage placement, resource envelope, concurrency class, model generation, and objective.
- Correctness and hard feasibility precede cost; an impossible transfer, unavailable operator, or exceeded hard memory constraint is not merely “expensive.”
- Startup and total work, processed rows and emitted rows, logical and physical I/O, resident and peak memory, and network bytes and elapsed network time remain distinct.
- Child cost is composed exactly once; shared, repeated, materialized, cached, pipelined, parallel, and early-stopped work use explicit execution semantics.
- Units and weights are dimensionally meaningful; an arbitrary score is not reported as milliseconds, bytes, money, or capacity.
- Calibration data identifies hardware, software, data, cache, concurrency, parameter, and observation boundaries and is validated out of sample.
- Uncertainty, unsupported operators, out-of-distribution inputs, fallback, and model overhead are first-class outputs.

### Common failures

Failures include treating optimizer cost as time; minimizing total cost for a LIMIT workload; summing parallel branches that overlap; dividing all work by worker count; pricing bytes without access pattern or locality; omitting network, spill, decompression, serialization, UDF, lock, or compilation work; double-counting cumulative node costs; tuning global constants from one query; fitting elapsed time without censoring queueing and interference; training on optimizer-selected plans only; accepting better prediction error without better plan choices; or deploying a learned model without coverage, latency, privacy, canary, and rollback contracts.

### Compact example

A normalized model prices a 1,000-page, 100,000-row scan at 2,250 units. A selective index path fetching 100 rows costs 367.75, but the same shape fetching 60,000 rows costs 5,352, so the preferred access path crosses over. Multiplying all costs by ten changes neither choice. For two candidates, index startup favors the first row while a blocking alternative has lower total cost. Expected cost favors a plan at 280 over one at 330, but adding declared uncertainty penalties changes robust scores to 400 and 370. The executable reproduces these arithmetic facts; it does not benchmark a database.

### Connections

Retrieve [Cardinality Estimation](064-cardinality-estimation.md), [Sequential and Index Scans](052-sequential-and-index-scans.md), [External Sorting and Spilling](057-external-sorting-and-spilling.md), and [Logical and Physical Plans](051-logical-and-physical-plans.md). Continue through [the roadmap](../ROADMAP.md) to join ordering, access-path selection, parameter sensitivity, adaptive processing, and plan diagnosis.

## Governing Question

An optimizer can enumerate semantically equivalent physical plans, but equivalence does not decide which plan should run. How should it predict and compare the work, latency, resources, money, and risk of alternatives before the relevant execution conditions are fully known?

The answer is not “estimate runtime.” A useful cost model is a decision model with an explicit domain. It consumes estimates—rows, widths, distributions, pages, cache likelihood, physical properties, workers, locality, and parameters—and predicts enough about candidate behavior to order them for a stated objective. Its score can be an arbitrary but internally consistent unit, a resource vector, a predicted distribution, or a constrained objective. It is neither the query semantics nor a universal performance oracle.

Costing is inseparable from enumeration. A perfect model cannot select a plan the search never generates. A broad search with a misleading model can prefer a disastrous candidate. Cost also depends on requested properties: an unordered hash join and an order-preserving merge join are not interchangeable if the parent requires order. The model therefore participates in a contract among logical equivalence, physical properties, search, cardinality, resource governance, and execution.

## Why This Matters

Cost decides sequential versus index access, nested-loop versus hash or merge join, join order, sort versus hash aggregation, materialization, compilation, parallelism, exchange placement, partition pruning, cache reuse, and first-row versus full-result strategies. A small ranking mistake near a crossover can change the entire plan. When estimates are wrong, that mistake can multiply through repeated inner scans, spills, broadcasts, and skewed workers.

The 1979 System R work made cost-based access-path selection central to relational optimization: retain useful alternatives and choose the plan minimizing a modeled total access cost. Cascades later separated logical and physical expressions, required properties, enforcers, memoized search, and cost limits in an extensible framework. Those ideas remain durable even though current systems include columnar execution, vectorization, cloud storage, distributed exchanges, accelerators, compilation, autoscaling, and learned components.

Current PostgreSQL 18 documentation states that its planner constants use an arbitrary relative scale and that only relative values matter. Its `EXPLAIN` documentation distinguishes startup and total cost, explains that parent costs are cumulative, and warns that costs cover what the planner models rather than every runtime activity. This is the right epistemic stance: cost is useful precisely because it is a controlled abstraction, and dangerous when its omissions or units are hidden.

Production goals extend beyond single-query elapsed time. Admission control needs peak memory and resource consumption. A multitenant warehouse cares about throughput, queueing, interference, and monetary spend. An interactive application values first-row latency and tail behavior. A distributed service must price movement and skew. A robust optimizer may accept slightly higher expected cost to avoid catastrophic spill or broadcast under plausible error. The objective must be named before “cheapest” has meaning.

## Prerequisites and Retrieval

You should understand relational algebra and bag semantics, physical plans/properties, scans and indexes, join algorithms, aggregation, sorting/spilling, pipeline execution, statistics, and cardinality estimation.

Retrieve: candidate and memo group; required and delivered physical property; enforcer; estimated cardinality and width; startup/total cost; processed versus emitted rows; resource vector; scalarization; blocking/pipelined operator; critical path; repeated work; cache/locality; spill threshold; exchange/broadcast/repartition; feasibility; calibration; residual; ranking loss; plan regret; uncertainty; sensitivity; OOD; fallback; shadow; canary; and rollback.

## Learning Objectives

After this module, you can:

1. specify a cost model's inputs, units, objective, scope, and unsupported states;
2. derive simplified scan, index, join, sort, aggregate, exchange, and parallel costs;
3. compose startup, total, serial, parallel, blocking, repeated, and shared work correctly;
4. distinguish resource prediction, scalar ranking, feasibility, and actual latency;
5. explain how cardinality, width, locality, memory, concurrency, and parameters affect crossovers;
6. calibrate interpretable parameters without overfitting one query or environment;
7. evaluate numerical error, pairwise ranking, selected plans, regret, and runtime outcomes separately;
8. compare analytical, calibrated, learned, hybrid, multiobjective, and risk-aware approaches;
9. diagnose a wrong plan by finding the first decisive cost divergence; and
10. productionize model changes with versioning, coverage, observability, canaries, and rollback.

## Core Exposition

**Define the costing event.** A cost record names the physical expression and child alternatives; logical bindings; required/delivered order, distribution, locality, and rewindability; estimated input/output rows and widths; parameter class; storage/table space; cache assumption; worker/resource/concurrency envelope; model/code/statistics generation; objective; units; and whether it represents startup, full consumption, per-worker demand, critical-path time, cumulative work, or peak resource. A naked `cost=42` is not portable evidence.

Let a resource prediction be

`R(P|x)=(cpu_cycles, logical_io, physical_bytes, network_bytes, peak_memory, temp_bytes, compile_work)`.

A decision function may scalarize it as `S=w dot R`, compare it lexicographically, form a Pareto frontier, impose hard constraints and minimize one remaining objective, or predict a latency distribution. Addition is valid only within compatible units. A weight maps a resource unit into an objective unit; it is not a decoration. If every term of one scalar model is multiplied by positive k, candidate ordering is unchanged. If only I/O weights change relative to CPU, crossovers can change.

**Correctness and feasibility come first.** A candidate that cannot deliver a required ordering/distribution, cannot access a remote site, violates an execution capability, or exceeds a hard safety constraint must be rejected or paired with an enforcer. Cascades models an optimization goal using a group, cost limit, and physical properties; enforcers such as sort connect a candidate to the required property. Infinity can represent impossible implementation, as current Apache Calcite's `RelOptCost` interface permits. Soft penalties are appropriate only for negotiable policy.

**Startup and total cost.** Streaming plans may emit early; blocking sort or hash build pays substantial startup before output. Store `C_s` and `C_t`. A simple partial-consumption interpolation is `C(f)=C_s+f(C_t-C_s)` for fraction f, but this is a model: selectivity, page granularity, batching, prefetch, LIMIT semantics, and skew can make work nonlinear. PostgreSQL's current source documents a similar interpolation for partial result fetching and explicitly keeps base row estimates independent of LIMIT. Optimize the observed demand distribution, not a guessed universal fraction.

**A simplified sequential scan.** For relation pages B, examined tuples N, emitted tuples M, sequential-page price `p_s`, tuple price `c_t`, predicate price `c_q`, and projection price `c_o`, one model is

`C_seq = B*p_s + N*(c_t+c_q) + M*c_o`.

The predicate usually touches examined rows, not merely emitted rows. Compression may trade fewer bytes for decompression CPU; columnar projection may avoid unrelated bytes; remote/object storage adds requests, latency, and transfer. PostgreSQL 18 demonstrates the simpler `pages*seq_page_cost + rows*cpu_tuple_cost` foundation and adds per-row predicate evaluation.

**A simplified index path.** Separate tree/index traversal, index pages, index entries, heap/page fetches, residual qualification, row materialization, and output. A sketch is

`C_idx = startup + B_i*p_i + N_i*c_i + B_h*p_h(locality,cache,repeats) + N_h*(c_t+c_q) + M*c_o`.

Heap pages are not simply output rows. Clustering/correlation can turn logically adjacent hits into fewer and more sequential fetches; uncorrelated hits can scatter. Index-only visibility, covering columns, batching, repeated probes, cache reuse, prefetch, and key comparison cost matter. PostgreSQL's index cost API explicitly separates index access cost, selectivity, correlation, and index pages, leaving parent-table retrieval to the caller.

The following executable uses deliberately normalized constants and finite equations. It verifies arithmetic and crossover logic, not PostgreSQL's complete implementation or hardware latency.

<!-- bijux-verify: {"id":"deterministic-cost-comparison","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"seq_total=2250.00\nindex_selective_total=367.75\nselective_choice=index\nindex_broad_total=5352.00\nbroad_choice=seq\nscaled_choice=index\nfirst_row_choice=index\nall_rows_choice=hash\nbroadcast_network_mb=300\nrepartition_network_mb=1050\nexpected_cost_choice=hash\nrisk_aware_choice=merge\nevidence=deterministic_cost_equations\n","stderr":""}} -->
```python
seq_page = 1.0
random_page = 4.0
cpu_tuple = 0.01
cpu_index_tuple = 0.005
cpu_operator = 0.0025


def seq_cost(pages, rows, predicates=1):
    return pages * seq_page + rows * (cpu_tuple + predicates * cpu_operator)


def index_cost(index_pages, heap_pages, rows, startup=2.0):
    return (
        startup
        + index_pages * seq_page
        + heap_pages * random_page
        + rows * (cpu_index_tuple + cpu_tuple + cpu_operator)
    )


seq = seq_cost(1000, 100000)
selective_index = index_cost(4, 90, 100)
broad_index = index_cost(300, 1000, 60000)
scaled_seq = seq * 10
scaled_selective = selective_index * 10
index_first = 2.0 + (selective_index - 2.0) / 100
hash_first = 200.0 + (300.0 - 200.0) / 100
broadcast_mb = 100 * (4 - 1)
repartition_mb = 100 + 950
risk_hash = 280 + 120
risk_merge = 330 + 40

print(f"seq_total={seq:.2f}")
print(f"index_selective_total={selective_index:.2f}")
print(f"selective_choice={'index' if selective_index < seq else 'seq'}")
print(f"index_broad_total={broad_index:.2f}")
print(f"broad_choice={'index' if broad_index < seq else 'seq'}")
print(f"scaled_choice={'index' if scaled_selective < scaled_seq else 'seq'}")
print(f"first_row_choice={'index' if index_first < hash_first else 'hash'}")
print(f"all_rows_choice={'index' if selective_index < 300 else 'hash'}")
print(f"broadcast_network_mb={broadcast_mb}")
print(f"repartition_network_mb={repartition_mb}")
print(f"expected_cost_choice={'hash' if 280 < 330 else 'merge'}")
print(f"risk_aware_choice={'hash' if risk_hash < risk_merge else 'merge'}")
print("evidence=deterministic_cost_equations")
```

**Joins and repeated work.** A nested loop includes outer cost plus, for every outer occurrence or batch, inner startup/scan/probe cost, join predicate work, and output. Memoization changes repeated distinct parameters, hit rates, capacity, and eviction. Hash join includes build input, hashing/insertion, memory allocation, probe input, hashing/comparison, residuals, output, and spill partitions. Merge join includes sorted inputs or enforcer sorts, comparisons, duplicate-band buffering/rewind, residuals, and output. Cardinality and width enter multiple terms; one underestimate can hide both repeated CPU and spill.

**Sort, aggregation, and memory.** An in-memory comparison sort is often approximated by `N log N` comparisons plus movement proportional to row width. External sort adds run generation and merge passes determined by memory, page/block size, and fan-in. Hash aggregation predicts groups, entry bytes, hash work, and partitioning/spill. Peak memory is not additive along the entire tree: lifetimes and concurrent pipelines matter. A soft spill price should not substitute for a hard process/tenant safety limit.

**Distributed execution.** A local resource unit is inadequate when candidates move data. Estimate rows times serialized width, compression, partition/broadcast fanout, protocol overhead, and skew. Broadcasting a 100 MB build to three other workers moves about 300 MB under the executable's convention; repartitioning 1,050 MB of both inputs moves 1,050 MB. This arithmetic alone does not select the plan: broadcast duplicates memory, repartition may overlap and balance better, placement may already collocate data, and network contention changes latency. Current Amazon Redshift documentation identifies redistribution as a major plan cost and distinguishes collocated, broadcast, and redistributed operations.

**Parallel execution.** Do not divide serial cost by workers. Decompose setup, serial fraction, divisible work, per-worker startup, exchange, coordination, merge/finalize, skew, synchronization, cache/bandwidth contention, and unavailable workers. Elapsed-time approximation follows the critical path, while total resource work can increase. The planner may need both: latency chooses a degree of parallelism; admission and throughput account for aggregate worker demand.

**Cumulative composition.** A parent cost normally includes child costs once. For serial tree execution, total work may add. For pipelined or concurrent branches, elapsed time is closer to a maximum/critical path plus synchronization, while resource consumption can add. Shared subplans need one materialization plus reads if truly shared, not one construction per syntactic reference. Correlated subplans need invocation count. Cache reuse is conditional evidence, never a free subtraction.

**Calibration.** Begin with identifiable parameters and controlled micro/macro experiments: sequential/random access under relevant cache states; predicate/function/vector costs; serialization/compression; exchange bandwidth/latency; allocation; sort/hash spill; compilation; and worker scaling. Record engine/version, hardware, storage, topology, configuration, data shape, warm/cold policy, concurrency, repetitions, failures, and uncertainty. Fit on one partition of observations and validate on unseen sizes, distributions, operators, plans, and time windows. Avoid setting global constants from a few favored queries; PostgreSQL's current documentation explicitly warns that ideal constants are not well-defined and should reflect the installation's query mix.

Calibration does not imply every score becomes milliseconds. A weighted model can be calibrated for rankings even when absolute predictions are biased. If predicting latency, separate planning, queue, execution, client backpressure, and interference; censored timeouts are not ordinary observations. Check residuals by operator, cardinality, width, cache, resource class, concurrency, and parameter class. Recalibrate when drift exceeds gates, not on every noisy sample.

**Evaluate the decision chain.** First test formula invariants and units. Then compare predicted resource components with measurements. Measure pairwise ranking accuracy and, more importantly, whether the selected plan is near the best candidate actually evaluated. Report plan regret, crossover errors, catastrophic tail regressions, planning overhead, resource constraint violations, and workload throughput/latency/cost. The Leis et al. controlled optimizer study found cost-model errors less influential than cardinality errors in its studied benchmark when other components were isolated; that scoped result does not excuse weak cost models elsewhere.

**Learned and hybrid models.** Statistical models can learn hardware- and operator-specific nonlinearities. The 2012 Li et al. work combined per-operator statistical models with asymptotic scaling functions to improve resource estimation and extrapolation in its studied SQL Server workloads. Recent learned-cost-model research covers plan representations, model architectures, batch and streaming tasks, and generalization challenges. Learned models still need semantic features, monotonic/boundary checks where applicable, OOD detection, inference budgets, immutable versions, privacy controls, and analytical fallback. A hybrid can use analytical structure for extrapolation and a learned residual for effects the base model misses.

**Uncertainty and robustness.** Point estimates hide sensitivity. Perturb cardinality, width, cache, bandwidth, workers, and memory across justified intervals; identify plan-ranking boundaries. One policy minimizes expected cost; another minimizes an upper quantile, expected regret, or `expected + lambda*risk`. The executable's expected scores choose hash 280 over merge 330, while declared penalties choose merge 370 over hash 400. Those penalties are illustrative, not calibrated probabilities. The 2025 Roq paper formalizes plan, estimation, and suboptimality risks and evaluates risk-aware learned selection; its results are evidence for that design, not universal dominance.

**Production control.** Emit a costing trace for decisive candidates: model version, inputs/provenance, terms, properties, feasibility, pruned alternatives, score, uncertainty, and objective. Shadow old/new models on the same memo and compare candidate rankings. Replay representative plans, then canary query fingerprints/tenants with result equivalence, budgets, control cohorts, kill switches, and rollback. Monitor planning latency/memory, chosen-plan churn, runtime/resource distributions, spills, exchanges, OOMs, queueing, and monetary outcomes. Never expose sensitive literals, tenant distributions, or learned features through diagnostics.

## Definitions and Notation

- **P, x, O**: candidate physical plan, costing context, and objective.
- **R(P|x)**: resource-demand vector for P under x.
- **C_s(P), C_t(P)**: startup and total/full-consumption cost.
- **S(P)**: scalar or otherwise totally ordered decision score.
- **w**: declared resource-to-objective weights used in scalarization.
- **Required property**: order, distribution, locality, rewindability, or other property demanded by a parent.
- **Enforcer**: physical operator that establishes a missing property.
- **Feasible set F**: candidates satisfying semantics, capabilities, properties, and hard constraints.
- **Critical path**: dependency path determining elapsed completion time under the model.
- **Crossover**: context where two candidate cost functions are equal and their order can reverse.
- **Residual**: observed outcome minus prediction under a declared convention.
- **Plan regret**: realized selected-plan objective minus a reference best candidate's realized objective.
- **Calibration domain**: environments, data, queries, plan features, and resource states represented by calibration evidence.
- **OOD/fallback**: unsupported or out-of-domain condition and the conservative alternative used.

Units belong in names or schemas. “Rows processed” is not “rows emitted”; logical page visits are not physical reads; aggregate CPU is not elapsed time; memory allocation sum is not peak residency; bytes transferred are not network duration.

## Mechanisms, Invariants, or Proof Structure

**Positive scaling invariance.** For scalar candidates with score S and k>0, `S(P)<S(Q)` if and only if `kS(P)<kS(Q)`. Therefore changing the common unit scale cannot change the optimum. Changing one relative weight or adding a candidate-specific term can. This is why arbitrary units are valid for ordering but not physical interpretation.

**Optimal substructure is conditional.** Dynamic-programming or memo optimization can retain a cheapest subplan only for the same logical group, required properties, parameterization, and relevant resource state. A globally useful ordered subplan may cost more locally than an unordered one. Discarding it without its property key violates the principle that justifies reuse.

**Composition invariant.** Every execution event is charged once in the appropriate dimension and lifetime. Child cumulative costs are not re-summed from every displayed node; repeated invocations multiply only repeatable portions; shared materialization is charged according to ownership; concurrent work contributes to aggregate resources and critical-path time differently.

**Crossover derivation.** If sequential cost is approximately constant for a full scan and index cost grows with selected rows/pages, solve `C_idx(s)=C_seq` for selectivity s under stated locality/cache assumptions. Below the threshold, index wins; above, scan wins. Cardinality uncertainty around the threshold is decision-critical even if its q-error is small.

**Feasibility before optimality.** The optimizer solves `arg min_{P in F} objective(C(P|x))`. A cheap P outside F is not a valid solution. Hard memory/safety/capability limits define F; soft preferences belong in the objective. Confusing the two permits unsafe plans or eliminates graceful spill alternatives.

**Critical-path proof sketch.** For two independent parallel branches with durations a and b that start together and synchronize before a parent, elapsed branch time is approximately `max(a,b)` plus coordination, while aggregate busy time is approximately `a+b`. This holds only if resources allow overlap; contention or scheduling serializes work. The model must declare which quantity it predicts.

**Evaluation separation.** Formula checks establish internal arithmetic, calibration checks prediction on observed domains, ranking tests evaluate candidate order, regret tests selected decisions, and workload trials operational outcomes. Passing one layer does not prove later layers.

## Alternatives and Trade-Offs

**Rule-based heuristics** are predictable and cheap but cannot compare many interacting alternatives quantitatively. **Analytical cost models** expose assumptions, extrapolate structurally, and are efficient during search; simplified constants miss hardware, cache, implementation, and interference effects.

**Calibrated analytical models** preserve structure while fitting environment-specific parameters; experiments are expensive and parameters drift. **Learned models** capture nonlinear interactions and systematic residuals; they require representative labels, coverage controls, inference budgets, interpretability, and safe extrapolation. **Hybrid models** combine equations with learned corrections but can double-count signals unless the interface is explicit.

**Scalar objectives** provide simple total ordering and pruning; weights can hide incomparable resource trade-offs. **Cost vectors/Pareto frontiers** preserve trade-offs and support multiple objectives; frontiers expand search. **Lexicographic objectives** protect a primary SLO or hard preference; small changes near priorities may be discontinuous. **Constrained optimization** makes resource budgets explicit; feasibility estimates can themselves be uncertain.

**Expected cost** is efficient under a stable known distribution. **Worst-case/upper-quantile/regret-aware selection** can reduce catastrophic tails but may sacrifice common-case performance and needs calibrated uncertainty. **Per-query optimization** can minimize individual latency while harming throughput. **Workload-aware optimization** captures interference and money but increases state, coupling, and fairness questions.

**Static calibration** is reproducible and stable; it ages. **Online feedback** adapts but is censored by chosen plans, queueing, failures, and changing workloads. Use guarded updates, control cohorts, decay, minimum support, tenant isolation, and rollback rather than turning each execution into global truth.

## Failure Modes and Misconceptions

1. “Cost 500 means 500 milliseconds” ignores arbitrary units and unmodeled runtime work.
2. “The lowest total cost is always best” ignores first-row demand, cancellation, and LIMIT.
3. “Parent EXPLAIN costs can be summed” double-counts cumulative children.
4. “Parallel cost is serial cost divided by workers” omits setup, serial work, skew, exchange, and contention.
5. “Selected rows determine index I/O” ignores page clustering, cache, visibility, batching, and repeats.
6. “More accurate cardinalities guarantee correct cost” ignores widths, operators, hardware, memory, and interference.
7. “A spill is just slower” ignores temp capacity, tail amplification, and hard safety limits.
8. “Broadcasting the smaller table is cheap” ignores fanout, serialized width, memory duplication, and concurrency.
9. “One benchmark can calibrate global constants” overfits its operators, cache state, data, and hardware.
10. “Low mean prediction error proves good optimization” ignores pairwise inversions and plan regret.
11. “Observed production plans form unbiased training data” ignores optimizer selection and timeout censoring.
12. “A learned cost model replaces formulas” ignores extrapolation, invariants, OOD, and fallback.
13. “Uncertainty penalty is automatically robust” requires calibrated uncertainty and a justified objective.
14. “Cheapest query maximizes system efficiency” may violate fairness, throughput, SLO, or monetary constraints.

## Worked Examples

### Example 1

**Sequential scan arithmetic.** With 1,000 pages at 1, 100,000 examined rows at 0.01, and one predicate at 0.0025 per row, cost is `1000 + 100000*(0.0125)=2,250`. Conclusion: predicate CPU is charged to examined rows even when few rows are emitted.

### Example 2

**Access-path crossover.** The executable prices a 100-row index path at 367.75 and a 60,000-row path at 5,352 against scan cost 2,250. The first index plan wins; the second loses. Conclusion: “use an index” is conditional on cardinality, pages, locality, and prices.

### Example 3

**Unit rescaling.** Multiplying both scan and selective-index costs by ten gives 22,500 and 3,677.5; index still wins. Increasing only random-page price can reverse it. Conclusion: common scale is arbitrary, relative weights are decision-bearing.

### Example 4

**First row versus all rows.** Index has startup 2 and total 367.75; a blocking hash-like alternative has startup 200 and total 300. At fraction 0.01, interpolation gives about 5.66 versus 201, so index wins early; at completion, hash wins. Conclusion: objective and consumption semantics can reverse candidate order.

### Example 5

**Cumulative-plan trap.** A displayed parent total 500 already contains child total 350. Adding them reports 850 and double-counts. To attribute local incremental cost, subtract only under the tool's compatible semantics and beware parallelism. Conclusion: read the plan-cost convention before aggregating nodes.

### Example 6

**Nested-loop cardinality error.** Outer actual is 10,000 but estimated 100; inner probe costs 3. Estimated repeated inner work is 300, actual is 30,000, before output and cache effects. Conclusion: cardinality error becomes repeated-work error through operator mechanics.

### Example 7

**Spill boundary.** A hash build estimates 90 MiB under a 100 MiB budget but actually needs 110 MiB. A modest 1.22 ratio crosses a partition/spill threshold and changes I/O/tail behavior. Conclusion: distance to a discontinuity matters more than error factor alone.

### Example 8

**Distributed movement.** Broadcasting a 100 MB build to three other workers moves 300 MB; repartitioning 100 MB plus 950 MB moves 1,050 MB. Broadcast wins on bytes but duplicates build memory and can fail under concurrency. Conclusion: a network-only scalar cannot certify the distributed plan.

### Example 9

**Parallel critical path.** Two independent branches take 8 and 5 seconds and truly overlap. The branch critical path is about 8 seconds plus coordination, while aggregate busy time is 13 seconds. If they contend for the same bottleneck, neither number alone predicts elapsed time. Conclusion: latency and resource work require different composition.

### Example 10

**Risk-aware deployment decision.** Expected scores choose hash 280 over merge 330. Validated uncertainty penalties 120 and 40 yield robust scores 400 and 370, choosing merge for the declared policy. Shadow traces must show what caused the reversal; a canary must then measure regret, latency, spill, and resource outcomes. Conclusion: uncertainty changes decisions only through an explicit, empirically governed objective.

## Cross-Program Connections

- [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md): asymptotic models, external memory, approximation, multiobjective optimization, and sensitivity support costing.
- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md): cache, allocation, indexing, sketches, and concurrency give operator-level mechanics.
- [Data Engineering](../../19-data-engineering/ROADMAP.md): file formats, partitioning, data quality, drift, and orchestration determine cost inputs.
- [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md): placement, ownership, serving contracts, and workload topology shape system-wide objectives.
- [Large-Scale Data Systems Engineering](../../21-large-scale-data-systems-engineering/ROADMAP.md): exchanges, skew, elasticity, scheduling, and failures shape distributed costs.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md): resource classes, admission, observability, model serving, canaries, and rollback operationalize model changes.
- [Software Engineering: Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md): differential tests, experiment design, coverage, and regressions establish evidence.

## References

1. P. Griffiths Selinger et al., [“Access Path Selection in a Relational Database Management System”](https://doi.org/10.1145/582095.582099), *SIGMOD 1979*. Primary System R cost-based access-path and join-ordering foundation.
2. Goetz Graefe, [“The Cascades Framework for Query Optimization”](https://15721.courses.cs.cmu.edu/spring2019/papers/22-optimizer1/graefe-ieee1995.pdf), *IEEE Data Engineering Bulletin* 18(3), 1995. Primary memo, properties, enforcers, cost-limit, and extensibility framework.
3. PostgreSQL Global Development Group, [PostgreSQL 18: Query Planning](https://www.postgresql.org/docs/18/runtime-config-query.html), retrieved 2026-08-30. Current arbitrary relative units, I/O/CPU/parallel parameters, cache assumptions, and tuning cautions.
4. PostgreSQL Global Development Group, [PostgreSQL 18: Using `EXPLAIN`](https://www.postgresql.org/docs/18/using-explain.html), retrieved 2026-08-30. Current startup/total, cumulative-cost, row/width, LIMIT, and modeled-work semantics.
5. PostgreSQL Global Development Group, [PostgreSQL 18: Index Cost Estimation Functions](https://www.postgresql.org/docs/18/index-cost-estimation.html), retrieved 2026-08-30. Current extension interface for index access cost, selectivity, correlation, and pages.
6. PostgreSQL Global Development Group, [`costsize.c`](https://github.com/postgres/postgres/blob/master/src/backend/optimizer/path/costsize.c), retrieved 2026-08-30. Current implementation commentary and costing routines; a moving development source, not a stable released API.
7. Apache Calcite Project, [`RelOptCost`](https://calcite.apache.org/javadocAggregate/org/apache/calcite/plan/RelOptCost.html), retrieved 2026-08-30. Current row-work/CPU/I/O vector and infinite/unimplementable cost interface.
8. Amazon Web Services, [Creating and Interpreting an Amazon Redshift Query Plan](https://docs.aws.amazon.com/redshift/latest/dg/c-the-query-plan.html), retrieved 2026-08-30. Current relative/cumulative cost, row/width, and plan interpretation.
9. Amazon Web Services, [Data Distribution for Query Optimization](https://docs.aws.amazon.com/redshift/latest/dg/t_Distributing_data.html), retrieved 2026-08-30. Current redistribution, broadcast, collocation, skew, and network trade-offs.
10. Viktor Leis et al., [“How Good Are Query Optimizers, Really?”](https://vldb.org/pvldb/vol9/p204-leis.pdf), *PVLDB* 9(3), 2015. Primary controlled separation of cardinality, cost-model, and enumeration effects.
11. Jiexing Li et al., [“Robust Estimation of Resource Consumption for SQL Queries using Statistical Techniques”](https://www.vldb.org/pvldb/vol5/p1555_jiexingli_vldb2012.pdf), *PVLDB* 5(11), 2012. Primary operator/statistical resource-estimation approach with asymptotic scaling.
12. Amin Kamali et al., [“Robust Plan Evaluation based on Approximate Probabilistic Machine Learning”](https://www.vldb.org/pvldb/vol18/p2626-kamali.pdf), *PVLDB* 18(8), 2025. Primary risk and uncertainty formalization with learned cost evaluation.
13. Roman Heinrich et al., [“Learned Cost Models for Query Optimization: From Batch to Streaming Systems”](https://www.vldb.org/pvldb/vol18/p5482-li.pdf), *PVLDB* 18(12), 2025. Current research tutorial on learned cost-model inputs, architectures, tasks, and deployment challenges.

## Exercises

### Exercise 1

Define a complete costing record for an index scan under `ORDER BY ... LIMIT 20`. Distinguish estimates, physical properties, startup/total work, resources, context, and objective.

### Exercise 2

Derive the sequential-scan result in Example 1 and prove positive common rescaling preserves its ordering against every candidate. Explain what rescaling does not preserve.

### Exercise 3

A plan expected to build a 90 MiB hash table actually uses 140 MiB and spills; its outer estimate is accurate. Give a first-divergence diagnostic and a model/test repair.

### Exercise 4

Design a cost model for choosing broadcast versus repartitioned join in a multitenant cluster. Include resources, skew, uncertainty, feasibility, calibration, and workload evaluation.

### Exercise 5

Design an elite replacement of an analytical model with a hybrid learned residual model. Specify evidence gates from formula correctness through production rollout, including privacy and rollback.

## Answers to the Exercises

### Answer 1

Record the bound table/index generation, predicate and parameter class; estimated examined index entries, heap pages, qualifying/output rows, widths, and confidence/provenance; required total order and whether the index delivers it without sort; visibility/covering status; forward/backward scan and collation/null semantics; startup traversal, first-page/first-row estimate, total index/heap/predicate/projection work; CPU, logical/physical I/O, bytes, peak memory, locks/pins, and optional money; cache/tablespace, hardware, engine/model/statistics versions, concurrency/resource class, row-goal and cancellation distribution; unsupported/OOD/fallback state; and objective such as p95 time to 20 correct rows subject to a resource limit. The LIMIT affects demand, not base cardinality truth. Correct ordering and feasibility are checked before cost.

### Answer 2

The scan has page term `1000*1=1000` and per-examined-row term `0.01+0.0025=0.0125`; `100000*0.0125=1250`, so total is 2250. For any candidates P,Q and k>0, if `S(P)<S(Q)`, multiplying by k preserves the inequality because positive multiplication is order preserving; the converse follows by dividing by k. Thus a common change of scalar unit leaves every pairwise ordering and argmin unchanged. It does not make arbitrary units physical time, preserve absolute thresholds expressed in the old unit, preserve an objective when only some components are scaled, or preserve ordering if candidate-specific nonlinear/clamped terms change.

### Answer 3

Bind estimated/actual rows and widths at the build input, then compare hash entry count, per-entry payload/metadata/alignment, bucket/load-factor allocation, allocator overhead, parallel copies/shared table, runtime filters, and peak lifetime. Accurate outer rows rule out only one input. The first divergence may be underestimated width, distinct/hash entry representation, duplicated worker state, or a missing fixed/overhead term. Reproduce with a finite build at widths and group counts around the budget; instrument entry/bucket/allocation/temp bytes; verify the spill threshold and cleanup; add a conservative peak-memory equation or calibrated residual with monotonic/boundary checks. Test below/equal/above threshold, null/variable-width/skew, worker counts, memory denial and temp exhaustion. Shadow plan rankings, then canary with hard admission limits and rollback; do not merely raise the memory grant globally.

### Answer 4

For each candidate estimate serialized/compressed bytes, per-link/fanout network movement, build duplication, per-worker and aggregate memory, CPU serialization/hash/compression, local I/O, setup, critical-path latency, and spill/failure risk. Model existing collocation, topology/bandwidth, concurrent traffic, worker availability, partition-count overhead, and key/row-size skew. Reject broadcast if worst justified build memory times concurrent copies violates a hard tenant/node budget. Calibrate network/serialization/compression and hash behavior across sizes, topologies, concurrency and failures; validate unseen keys, widths, cluster sizes and workload windows. Perturb cardinality/width/skew/bandwidth intervals and compare expected, upper-quantile, or regret objective explicitly. Evaluate pairwise choice, realized regret, p50/p95/p99 latency, bytes, CPU, spill/OOM, queueing, throughput, fairness, and money in shadow and controlled canaries. Version model and inputs, tenant-isolate evidence, retain analytical fallback and a kill switch.

### Answer 5

Keep the analytical model as a named baseline and define the learned output as a residual or correction for specified operators/resources, with a no-double-counting equation. Unit-test dimensions, nonnegativity, composition, positive scaling where applicable, physical-property keys, feasibility and synthetic crossover cases. Build labels with execution boundary, hardware/software/data/model versions, cache/concurrency, completion/censoring and tenant/privacy policy. Split by plan shape, parameter, data/time, engine/hardware and tenant according to the generalization claim. Report resource/latency residual distributions, coverage/OOD, calibration, inference and planning overhead, pairwise ranking, chosen-plan regret, hard-limit violations and workload outcomes against analytical and current baselines. Enforce feature access, literal redaction, retention, model-membership and poisoning controls. Shadow identical candidate sets, replay safe alternatives, canary bounded fingerprints/tenants with control cohort and result checks, observe plan churn/tails/spill/network/OOM/queueing/money, and rollback automatically on declared gates. Immutable model generations and analytical fallback remain available. This evidence supports only the tested domains; it does not prove universal prediction, optimality, fairness, privacy, or production fitness, and external review requires named humans.
