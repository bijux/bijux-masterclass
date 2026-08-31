---
module_id: DBE-070
program: Database Engineering
level: 2
module_number: 70
title: Diagnosing an Incorrect or Unstable Query Plan
status: complete
last_verified: 2026-08-30
---

# Diagnosing an Incorrect or Unstable Query Plan

## One-Page Review

### Governing question

How can an engineer move from “the plan is wrong” or “the query became slow” to a reproducible causal explanation, a safe containment, and a verified durable correction without confusing correlation, optimizer estimates, execution conditions, or plan shape with proof?

### Essential definitions

A **query fingerprint** groups statements under declared normalization rules. A **plan identity** names one bound, versioned physical plan; visual similarity is insufficient. A **plan regression** is a measured violation of a correctness, latency, throughput, resource, or stability gate relative to a comparable accepted baseline. **Plan instability** means materially different plans or outcomes occur across contexts or time; variation may be legitimate under parameters or resources. **Estimate error** compares predicted and observed quantities. For positive estimate (e) and actual (a), **q-error** is `max(a/e,e/a)`; zero cases need an explicit convention. A **first divergence** is the earliest causal layer where baseline and incident differ. **Containment** bounds harm before root cause is repaired. **Plan forcing** asks an optimizer to reproduce a known plan but can fail or age; it is a reversible control, not a causal proof.

### Central model, mechanism, or theorem

Diagnose along a causal chain:

$$
statement/context \rightarrow binding/rewrite \rightarrow candidates \rightarrow
estimates \rightarrow costs/search \rightarrow cache/adaptation \rightarrow
execution/resources \rightarrow client/workload.
$$

Hold the reproduction envelope constant and find the first material divergence. A later difference can be an effect, not the cause. A plan change is neither necessary nor sufficient for a performance regression: the same plan can slow under data, cache, locks, spill, or contention, and a new plan can remain within every gate. Establish causation with controlled interventions, alternative-plan execution where safe, repeated matched samples, and a mechanism explaining the observed row/resource flow.

### Critical invariants

- Verify query results, errors, snapshot, authorization, and side effects before performance; a semantically wrong plan is not a tuning problem.
- Capture normalized statement and exact text, parameters/types, role/policy, schema/indexes, data/statistics, configuration, software/build, plan/cache/adaptation state, resources, concurrency, and measurement boundaries.
- Compare estimated rows with actual occurrences at the same node, loop, and consumption boundary; normalize per-loop versus total explicitly.
- Keep optimizer cost units separate from milliseconds, and inclusive operator time separate from self time.
- Distinguish plan change, performance change, and workload/system change; none proves either of the others.
- Observation tools can execute writes, perturb timing, expose secrets, aggregate windows, sample, reset, or omit client/queue/commit time; record those limits.
- Containment has scope, owner, expiry/removal condition, failure behavior, and rollback.
- The durable fix targets the first demonstrated cause and is evaluated against the whole workload, not one query instance.

### Common failures

Failures include running an analyzed plan for mutating SQL in production; comparing different parameters or snapshots; reading optimizer cost as time; treating one high q-error at the root as the origin; forgetting loops; blaming a scan for descendant time; clearing every cache; assuming a plan changed because latency changed; assuming a changed plan caused latency; updating statistics blindly; adding or forcing an index from one run; pinning a fast plan across skewed parameters; ignoring locks, queueing, storage, memory, network, replicas, client fetch, or concurrency; comparing warm treatment with cold control; and leaving emergency hints indefinitely.

### Compact example

Four nodes have q-errors 1.20, 2.00, 100.00, and 1.00; with a material threshold of 4, the first cardinality divergence is the customer–orders join, not the root aggregate. An inner node reporting 20 rows over 2,500 loops processed 50,000 row occurrences. Plan A averages 803.33 ms and Plan B 5,000 ms, a 6.22× slowdown and 4,196.67 ms increase; at 120 executions/hour that is 503.60 extra database-seconds/hour. A 4,800 ms end-to-end breakdown—200 planning, 3,000 execution, 1,200 lock wait, 400 client—accounts exactly for the total. This finite arithmetic identifies hypotheses and impact, not causation.

### Connections

Retrieve [Profiling a Query Operator Pipeline](060-profiling-a-query-operator-pipeline.md), [Statistics and Histograms](063-statistics-and-histograms.md), [Cardinality Estimation](064-cardinality-estimation.md), [Cost Models](065-cost-models.md), [Join Ordering](066-join-ordering.md), [Access-Path Selection](067-access-path-selection.md), [Plan Caching and Parameter Sensitivity](068-plan-caching-and-parameter-sensitivity.md), and [Adaptive Query Processing](069-adaptive-query-processing.md). Continue through [the roadmap](../ROADMAP.md) to logging and recovery.

## Governing Question

An incident often begins with a sentence that already assumes its conclusion: “the optimizer chose the wrong plan.” Sometimes it did. But a query can become slow without changing plans because its inputs grew, cache locality fell, memory was denied, a lock blocked it, storage or a remote service slowed, concurrency increased, a spill occurred, or the client stopped consuming. A plan can change without becoming worse. An apparently faster forced plan may return different results, benefit from warm pages, or shift cost to writes and neighboring workloads.

The governing question is therefore not “which node looks expensive?” It is: what is the earliest evidenced divergence from the accepted behavior, through what mechanism does it produce the symptom, and which intervention isolates that cause without changing another relevant dimension?

## Why This Matters

Query plans are compressed explanations of decisions, not complete recordings of reality. Estimated rows and cost show what the optimizer believed. Actual plans add measurements, but tools differ on per-loop aggregation, inclusive time, worker detail, buffers, waits, memory, spills, serialization, and client transfer. Historical stores aggregate time windows and may evict plans. Sampling misses rare executions. Instrumentation changes timing. Plan text can expose SQL, object names, predicates, literals, policies, and distribution information.

A disciplined diagnosis prevents two kinds of harm. The first is technical: a hint or index masks stale statistics, a parameter-sensitive plan is pinned globally, a memory increase reduces fleet concurrency, or a cache clear creates a compile storm. The second is epistemic: an organization accumulates folklore because every incident changes several variables and retains no reproducible evidence. The durable outcome is not merely a fast rerun; it is a supported causal account, a bounded remedy, and a regression guard.

Current systems provide complementary evidence. PostgreSQL 18 documents nonexecuting and executing `EXPLAIN`, machine-readable formats, buffers, WAL, settings, serialization, planning memory, and caveats; `auto_explain` can sample/log slow plans with overhead; `pg_stat_statements` aggregates normalized statement statistics. SQL Server Query Store retains plan, runtime, and wait history and supports reversible plan forcing, while documenting that forcing is attempted and normal optimization resumes if it fails. MySQL 8.4 documents iterator measurements in `EXPLAIN ANALYZE` and a separate optimizer trace. Oracle documents real-time SQL monitoring and workload diagnostics. Trino exposes distributed analyzed plans. SQLite explicitly warns that `EXPLAIN QUERY PLAN` output is for interactive debugging rather than a stable application API. Evidence must be interpreted under the named tool and version.

## Prerequisites and Retrieval

Retrieve these ideas before diagnosing a plan:

- SQL plans must preserve bag, null, type, collation, ordering, snapshot, and authorization semantics.
- Estimates are not observations; cost units are not elapsed time.
- Cardinality errors propagate into access paths, join order/algorithm, memory, parallelism, and distribution.
- Operator time can be inclusive; rows can be per loop; parallel workers overlap.
- Plan caching can make execution history-dependent and parameters can require different plan families.
- Adaptive execution can alter the active plan based on runtime evidence.
- latency can be CPU, I/O, locks, queues, scheduling, network, client consumption, commit, or cleanup.
- indexes and configuration changes affect the whole workload and ongoing maintenance.

The module assumes familiarity with query fingerprints, physical operators, statistics, caching, transactions, percentiles, controlled experiments, and production rollout.

## Learning Objectives

After completing this module, you should be able to:

1. classify an incident as semantic incorrectness, regression, instability, or expected context sensitivity;
2. construct a complete, privacy-aware reproduction envelope;
3. normalize plan metrics and find the first material cardinality, cost, candidate, or runtime divergence;
4. separate plan, data, parameter, cache, resource, concurrency, and client hypotheses with controlled tests;
5. use plan history, optimizer traces, forcing, hints, statistics, indexes, rewrites, and configuration at their proper evidentiary strength;
6. choose containment and durable corrections with explicit blast radius and removal conditions;
7. build regression, canary, observability, and rollback evidence sufficient for production change.

## Core Exposition

**Classify the symptom before collecting everything.** “Incorrect plan” has at least four meanings. A semantic failure returns wrong rows, wrong multiplicities/order where required, wrong errors, unauthorized data, or wrong side effects. A performance regression violates a declared baseline gate. Instability means the same declared identity/context produces plan or performance variation beyond tolerance. Context sensitivity means different parameters, tenants, statistics, or resources legitimately choose different plans. These categories can coexist, but their priorities differ: semantic or authorization failure demands containment before performance tuning.

Define the observable boundary. Does latency end at executor completion, final network byte, client decode, transaction commit, or job publication? Does throughput count submitted, completed, or successful statements? Is resource harm query-local or fleet-wide? Write the regression predicate before inspecting plan shapes: for example, “for fingerprint F and parameter class C under resource class R, p95 end-to-end latency rose from ≤1 s to 5 s and spill exceeded 2 GiB after deployment D.”

**Freeze the reproduction envelope.** Capture immutable or reconstructible evidence:

- exact SQL and a documented normalized/query identifier;
- parameter values in a protected store or redacted class, plus types, lengths, nulls, collation, and protocol binding;
- database/schema/search path, temporary objects, role, privileges, row policies, time zone, compatibility and session settings;
- schema, constraints, indexes, partitions, functions/extensions, statistics definitions/content fingerprints, analyze time, and relevant metadata generations;
- database build, optimizer/executor versions, feature flags, plan-cache mode, cached compile value/class, adaptive decisions, hints/baselines;
- data/snapshot or repeatable generator, scale, distribution/skew, tenant class, recent load/compaction/vacuum state;
- CPU, memory/grant, workers, storage/cache, NUMA/container/resource group, replica, remote services, concurrency, locks, queues, background work;
- plan/profiling format and options, sampling/window/reset behavior, warm-up/cache policy, client/network boundary, timestamps and clock basis.

Plans from different envelopes are not controlled evidence. If an exact production snapshot cannot be reproduced, state which dimensions are approximated and use historical telemetry plus a bounded production canary rather than claiming laboratory causation.

**Protect evidence collection.** Nonexecuting explain reveals estimates and chosen structure without running the statement. Executing explain/analyze runs it. For writes, volatile functions, sequences, external calls, locks, and large scans, a transaction rollback may not undo every consequence. Prefer a disposable replica/snapshot or product-supported live-plan capture. Restrict access because plans and traces can reveal literals, object names, policies, cardinalities, or tenant distributions.

Instrumentation has probe effect. Per-node timing, buffers, WAL, stack samples, optimizer traces, and distributed task detail add CPU, synchronization, memory, logging, or network. PostgreSQL's `auto_explain` documentation explicitly notes overhead and offers sampling/configuration. Calibrate representative queries with instrumentation off/on, sample rather than blanket-enable expensive detail, and capture the very slow production execution before rerunning a potentially different parameter or plan.

**Establish a timeline.** Align application deploys, schema/index/partition changes, statistics refreshes, data loads, engine/configuration changes, cache invalidation/restart/failover, resource scaling, storage incidents, concurrency shifts, and plan changes. Query-history stores are valuable because the current plan cache may retain only the latest plan or evict entries. SQL Server Query Store, for example, records plans plus runtime and wait statistics over time windows. Aggregation can hide bimodal parameter classes, and asynchronous collection creates edge cases; inspect granularity and gaps.

Do not use “after” as “because.” Timeline narrows hypotheses. A plan changed after statistics refresh; a workload also doubled and storage latency rose. Controlled comparisons must separate them.

**Normalize plan evidence.** For every node, record stable logical role and operator occurrence; estimated startup/total cost, rows, width; actual rows, loops, first/last time; rows removed/rechecked; memory/spill; buffers/bytes/I/O; worker/task distribution; waits; and delivered properties. Tool-specific fields may be averages per loop or per worker. Convert to total occurrences only when documentation defines the aggregation. An inner node with 20 rows per loop and 2,500 loops represents 50,000 occurrences, not 20.

For positive estimates and actuals, q-error is symmetric: `max(a/e,e/a)`. It describes multiplicative error, not cause or impact. Define zero cases: exact zero/zero can be 1; one zero and one positive can be infinite or a documented cap for dashboards. Compare nodes at the same consumption boundary. LIMIT, short-circuit, early cancellation, or adaptive switching may prevent a child from being fully consumed, so a smaller actual row count is not automatically estimation error.

Time needs equal care. Node times may include descendants. Parallel workers overlap in wall time. A root may exclude client transfer. “Buffers hit” is not physical I/O. A high-time node may be waiting. Attribute row/byte amplification, CPU, I/O, memory/spill, lock/queue/network waits, and end-to-end residual separately rather than assigning elapsed time to the most visually prominent operator.

**Find the earliest divergence.** Walk the causal chain, not merely the displayed tree:

1. **Statement and context:** Was the same query/parameter/type/security/snapshot intended?
2. **Binding and rewrite:** Did names, views, policies, casts, constraints, functions, or transformations differ?
3. **Candidate generation:** Was the relevant access path, join order/algorithm, distribution, or property-carrying plan enumerated and legal?
4. **Estimation:** Where first did rows, width, distinctness, correlation, pages, or resource needs diverge materially?
5. **Cost/search:** Given the estimates, were alternatives ranked as the model predicts; did timeout/pruning exclude one?
6. **Cache/parameter/adaptation:** Which values/history compiled the plan; was a generic/custom/variant/adaptive policy selected correctly?
7. **Execution:** Did actual cache, I/O, memory, spill, skew, CPU, workers, locks, remote latency, failure, or retry differ?
8. **Workload/client:** Did queueing, concurrency, result size, network, client backpressure, commit, or surrounding queries change?

The first divergent estimate may occur at a join, while the visible catastrophe is a spill two nodes above. Raising memory treats the effect; repairing correlation statistics, predicate semantics, or estimation logic may address the cause. Conversely, estimates may be accurate while storage latency makes the cost calibration wrong, or the entire plan may be fine while lock wait dominates.

**Use q-error with topology and impact.** A 100× error at a leaf that produces ten rather than one row may be harmless. A 10× error inside 100,000 nested-loop invocations can explode. Trace propagation: input occurrences × loops × row width determine work and state; operator choice determines sensitivity. Mark the first threshold crossing that changes candidate ranking, memory, partitioning, or row goal. Root q-error is often accumulated evidence, not the origin.

**Distinguish candidate absence from bad ranking.** If a faster plan exists, ask whether it was enumerated. An unavailable index, incompatible type/collation, partial-index implication failure, missing delivered order, outer/lateral dependency, search timeout, or pruned memo state is not a cost-comparison error. Optimizer traces can expose transformations, candidate rejection, and costing, but their formats are version-specific, potentially huge, and sensitive. MySQL 8.4 documents optimizer trace separately from `EXPLAIN`; the trace is complementary, not a stable universal API.

If both candidates were present, replay the cost formulas with captured estimates, settings, and capabilities. Check units and double-counting. Then execute alternatives safely under matched conditions to measure regret. A model can consistently rank the wrong plan because random/sequential I/O, cache, CPU, network, spill, or parallel overhead is miscalibrated. One faster alternative does not show which input caused the ranking.

**Diagnose parameter and cache sensitivity.** Group results by parameter vector/class, tenant, compile context, generic/custom/variant, and plan identity. Randomize or deliberately permute first-execution order. A plan that is excellent for point values and catastrophic for broad ranges should not be judged by one overall mean. Clearing the entire plan or buffer cache changes many variables and can create fleet harm. Prefer scoped recompile/eviction or isolated sessions where supported, while measuring data-cache warmth separately.

Plan instability can be expected if classes legitimately have different optima. The problem is misclassification, reuse across incompatible classes, churn near a boundary, or tail harm. Compare within class before demanding one stable plan.

**Separate plan from runtime and workload.** Run the same plan under incident and healthy resource conditions, and competing plans under the same condition. Collect CPU runnable/steal/throttle, memory grant/use/pressure, spill, storage latency/queue/bytes, buffer hit/read meaning, network/remote requests, worker skew, lock/block graph, admission queue, retries, and client consumption. A two-by-two comparison—plan A/B × environment healthy/incident—can expose interaction. Do not force dangerous plans or reproduce overload without budgets and cancellation.

If same plan and same cardinalities differ, first investigate waits, cache, physical placement, contention, and external latency. If plan differs but latency does not, plan-shape alerting alone is noisy. If both differ, intervention is needed to establish whether the plan mediates the effect.

**Use controlled interventions.** Stronger evidence comes from changing one causal variable while holding others fixed: refresh a cloned statistics object; bind the same parameters; force a known prior plan in a canary; toggle one optimizer rule/session setting diagnostically; make an index invisible in a test environment; calibrate one cost parameter; reproduce a lock-free run; grant/deny memory within bounds; or replay the exact plan against fixed data. Repeat and alternate order to control warming and temporal drift.

Treat hints and forcing as experiments and containment. SQL Server documents that Query Store forcing asks the optimizer to use a retained plan and falls back to normal optimization if forcing fails. A forced plan may become illegal after schema changes, wrong for other parameter classes, or inferior as data grows. Record plan ID/generation, scope, owner, expiry, failure telemetry, rollback, and removal test. Never claim “forcing fixed it, therefore the optimizer was the cause.”

**Rank remedies by demonstrated cause.** If binding changed, qualify names or repair client types. If rewrite legality/implementation failed, correct that engine rule or query semantics. If candidate enumeration failed, repair capability, schema/index, search budget, or property representation. If statistics are stale or lack correlation, refresh or enrich them and fix maintenance. If the estimator/model is wrong, correct/calibrate it with broader workload evidence. If parameter sensitivity caused reuse mismatch, use custom/generic/variant policy. If runtime resources caused the issue, address spill, admission, skew, storage, lock duration, or remote behavior. If the client caused backpressure, fix fetching/pagination/network rather than the plan.

Indexes and rewrites can be valid product changes, but account for write amplification, storage/cache, maintenance, replicas, backup/restore, concurrency, and semantic equivalence. Global cost/configuration changes require corpus/workload evaluation. Prefer the smallest durable cause-aligned change, not the smallest textual edit.

**Quantify regression and impact.** Compare distributions within matched classes: execution count, mean/median/p95/p99, variance, CPU, reads/bytes, memory/spill, waits, rows, failures, and throughput. Separate absolute and multiplicative change. A 6× slowdown from 1 ms to 6 ms may matter at millions of calls; a 20% slowdown on a two-hour job may dominate capacity. Multiply extra resource/time per execution by frequency, but avoid summing overlapping wall time as exclusive demand.

The executable below performs finite normalization and triage arithmetic. It does not inspect a live database or prove causation.

<!-- bijux-verify: {"id":"finite-plan-regression-triage","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"nodes=4\nfirst_cardinality_divergence=customer_orders_join\nfirst_q_error=100.00\ninner_total_rows=50000\nbaseline_mean_ms=803.33\nregressed_mean_ms=5000.00\nslowdown_ratio=6.22\nabsolute_regression_ms=4196.67\nextra_db_seconds_per_hour=503.60\nlatency_accounted_ms=4800\nlatency_residual_ms=0\nexecution_fraction=0.625\nlock_wait_fraction=0.250\nplan_change_correlated=true\ncausation_proven=false\nforced_plan_role=containment\nsemantic_equivalence_required=true\nevidence=finite_diagnostic_arithmetic\n","stderr":""}} -->
```python
from statistics import mean

nodes = [
    ("orders_scan", 100_000, 120_000),
    ("recent_orders_filter", 10_000, 20_000),
    ("customer_orders_join", 500, 50_000),
    ("regional_aggregate", 50, 50),
]


def q_error(estimate, actual):
    if estimate == actual == 0:
        return 1.0
    if estimate == 0 or actual == 0:
        return float("inf")
    return max(actual / estimate, estimate / actual)


material_threshold = 4.0
first_divergence = next(
    (name, q_error(estimate, actual))
    for name, estimate, actual in nodes
    if q_error(estimate, actual) >= material_threshold
)

inner_rows_per_loop = 20
inner_loops = 2_500
inner_total_rows = inner_rows_per_loop * inner_loops

baseline_samples = [800, 820, 790]
regressed_samples = [4_800, 5_200, 5_000]
baseline_mean = mean(baseline_samples)
regressed_mean = mean(regressed_samples)
absolute_regression = regressed_mean - baseline_mean
executions_per_hour = 120

latency = {
    "planning": 200,
    "execution": 3_000,
    "lock_wait": 1_200,
    "client": 400,
}
end_to_end = 4_800
accounted = sum(latency.values())

print(f"nodes={len(nodes)}")
print(f"first_cardinality_divergence={first_divergence[0]}")
print(f"first_q_error={first_divergence[1]:.2f}")
print(f"inner_total_rows={inner_total_rows}")
print(f"baseline_mean_ms={baseline_mean:.2f}")
print(f"regressed_mean_ms={regressed_mean:.2f}")
print(f"slowdown_ratio={regressed_mean / baseline_mean:.2f}")
print(f"absolute_regression_ms={absolute_regression:.2f}")
print(f"extra_db_seconds_per_hour={absolute_regression * executions_per_hour / 1000:.2f}")
print(f"latency_accounted_ms={accounted}")
print(f"latency_residual_ms={end_to_end - accounted}")
print(f"execution_fraction={latency['execution'] / end_to_end:.3f}")
print(f"lock_wait_fraction={latency['lock_wait'] / end_to_end:.3f}")
print("plan_change_correlated=true")
print("causation_proven=false")
print("forced_plan_role=containment")
print("semantic_equivalence_required=true")
print("evidence=finite_diagnostic_arithmetic")
```

**Validate the fix against its mechanism.** A statistics remedy must improve the first bad estimate and downstream plan/outcome across relevant distributions. An index must be used under intended predicates and improve end-to-end workload without unacceptable writes/space/maintenance. A parameter policy must reduce per-class regret without compilation storms or cache growth. A memory remedy must reduce spills without harming concurrency. A lock remedy must shorten/avoid the blocking dependency. A client remedy must change delivery metrics, not merely executor time.

Run semantic differential tests first. Then controlled performance trials with warm/cold policy, repeated samples, randomized/blocked order, concurrent load, and unchanged control. Record confidence/variability and negative cohorts. A passing single query is not enough for a global configuration, schema, or optimizer change.

**Productionize with detection and rollback.** Retain a privacy-safe query/plan identity, parameter class, plan history, compile/invalidation/adaptation events, estimated-versus-actual samples, resource/wait metrics, and end-to-end SLO. Alert on outcomes and first-divergence signals, not raw plan hash alone. Plan hash changes can be harmless; unchanged hashes can hide resource regressions; hashes may change format across versions.

Shadow candidate estimates/plans where possible. Canary selected fingerprints, parameter/tenant classes, replicas, and workload cohorts. Gate semantic equivalence, errors, latency tails, throughput, CPU, I/O, memory/spill, locks, write amplification, storage, replicas, and neighboring workload. Preserve the prior compatible configuration/plan/index state, a kill switch, and a tested rollback. Remove emergency forcing only after the durable fix passes its declared removal experiment.

## Definitions and Notation

- **Fingerprint F**: statement equivalence class under documented normalization and binding rules.
- **Plan identity P**: versioned bound physical plan and relevant optimizer/executor context.
- **Reproduction envelope E**: statement, context, data/statistics, software/configuration, resources/workload, and measurement conditions.
- **Baseline / incident**: accepted comparison distribution and observed violating distribution.
- **Regression gate**: explicit correctness/performance/resource/stability predicate.
- **Estimated / actual rows**: optimizer prediction and measured output occurrences at a declared node/loop boundary.
- **q-error**: symmetric multiplicative estimate error for positive values.
- **First divergence**: earliest material difference in the causal chain supported by comparable evidence.
- **Plan regret**: realized selected-plan objective minus realized reference-best eligible-plan objective.
- **Containment**: reversible harm-reduction control pending durable correction.
- **Forcing/hint/baseline**: mechanism constraining or influencing optimization; not a correctness or causal proof.
- **Probe effect**: workload behavior changed by instrumentation.
- **Counterfactual**: outcome predicted under an alternative plan/environment; strongest when directly and safely executed.
- **Removal criterion**: evidence required to retire containment.

“Wrong plan” should be replaced by a falsifiable claim: which gate failed, for which identity/context, because which first divergence changed which mechanism?

## Mechanisms, Invariants, or Proof Structure

**Causal-chain argument.** Later plan nodes are functions of earlier binding, rewrites, candidates, estimates, costs/search, cache/adaptation, and runtime inputs. If the first baseline/incident difference is an underestimated join input and later spill follows from a too-small build choice/grant, the join estimate is a causal candidate; the spill is an effect. Controlled correction of that estimate while holding other dimensions fixed, followed by predicted plan/resource improvement, strengthens causation. Temporal order alone does not.

**q-error properties.** For positive `a,e`, q-error is at least 1, equals 1 iff `a=e`, and is symmetric under exchanging actual and estimate. It measures ratio magnitude but has no units, sign, topology, frequency, or cost sensitivity. Therefore q-error ranks estimation discrepancy only after defining zero, node/loop, consumption, and materiality conventions.

**Per-loop normalization.** If a tool reports average output `r` over `l` executions of a node, total occurrences are `r*l`, subject to its documented rounding and aggregation. Comparing parent total to child per-loop value creates false amplification. For parallel workers, sum rows only if partitions/attempt ownership prevent duplicates; do not sum overlapping wall times.

**Causation test.** Let P denote plan identity and Y outcome. Correlation `P changed and Y regressed` does not establish `P -> Y` because parameters, data, statistics, resources, concurrency, and cache may confound both. A controlled comparison fixes these variables and intervenes on P where safe. Repeated predicted changes in row/resource flow and Y support the mechanism; residual differences and unmeasured confounding bound the claim.

**Containment invariant.** A forced plan or hint is acceptable only for an identified scope, compatible schema/context, bounded lifetime, monitored failure/regret, and immediate rollback. It never waives semantic validation. The durable correction plus a passing removal experiment terminates containment; otherwise temporary policy silently becomes architecture.

**Evidence ladder.** Static semantics and plan inspection reject invalid hypotheses. Historical correlation narrows time/context. Actual execution measures one environment. Controlled interventions support causation. Workload replay establishes scoped system effects. Canary establishes bounded production outcomes. No level proves universal optimizer correctness, future stability, or absence of security leakage.

## Alternatives and Trade-Offs

**Nonexecuting explain** is safer and cheap but contains predictions. **Analyzed execution** adds actuals while running the query and perturbing it. **Live-plan capture** observes the incident but may be sampled/incomplete. **Historical stores** preserve changes and distributions but aggregate, evict, and consume storage.

**Text plans** are human-readable and diff poorly. **Structured plans** support tooling but remain engine/version-specific. **Plan hashes** cheaply detect some shape changes but omit runtime/context and can change format. Store raw authorized artifacts plus a versioned semantic normalization rather than assuming one cross-engine schema.

**Statistics refresh/enrichment** addresses stale or missing distribution evidence; frequent/high-resolution statistics cost maintenance and cannot encode every correlation. **Index/schema changes** add capabilities but incur writes/storage/operations. **Query rewrites** can clarify intent or expose access paths; semantic equivalence is difficult under bags/nulls/outer joins/volatility.

**Hints/forcing** rapidly contain a known regression and enable counterfactual tests; they constrain future adaptation and can fail or age. **Cost/configuration changes** repair systemic calibration but have broad blast radius. **Engine fixes/upgrades** address optimizer defects durably; rollout and compatibility evidence are larger. **Resource increases** absorb symptoms quickly; they can reduce concurrency and obscure causal defects.

**Stable one-plan policy** is predictable; parameter/resource classes may need variants. **Plan variation** can be optimal; churn and misclassification harm tails. Evaluate regret within class and stability of the policy, not sameness of every tree.

## Failure Modes and Misconceptions

1. “The plan changed, so it caused the slowdown” confuses temporal correlation with intervention evidence.
2. “The plan did not change, so it is not a query problem” ignores data, cache, spill, skew, waits, and resources.
3. “Highest-cost node is slowest” treats arbitrary optimizer units as measured time.
4. “Root q-error is root cause” ignores propagation from an earlier child.
5. “Actual rows are totals” ignores per-loop/per-worker aggregation and rounding.
6. “Node time is self time” ignores descendants, overlap, and waits.
7. “Buffer hits mean no I/O problem” ignores cache layer, contention, dirty/writeback, and measurement semantics.
8. “EXPLAIN ANALYZE is read-only” ignores DML, volatile/nontransactional effects, locks, and load.
9. “Current plan reproduces the incident” ignores eviction, compile context, parameters, adaptation, and environment.
10. “Refresh all statistics” changes many inputs without proving which was stale or harmful.
11. “The missing index is obvious” ignores predicate semantics, ordering, visibility, write cost, and whole workload.
12. “A forced old plan proves causation” it may change warmth, compilation, parameters, or other context.
13. “One fast rerun validates the fix” ignores variance, warming, concurrency, tails, and negative cohorts.
14. “One stable plan is always desirable” ignores legitimate parameter-sensitive optima.
15. “Plan hash alerting catches regressions” hashes can change harmlessly or stay constant during severe runtime regressions.
16. “Emergency forcing can remain until it fails” converts containment into unmanaged permanent policy.

## Worked Examples

### Example 1

**Semantic failure first.** A rewritten left join returns 998 rather than 1,000 customer rows because a predicate moved onto the preserved side. The new plan is faster. Conclusion: quarantine the rewrite; performance cannot justify changed bag semantics.

### Example 2

**Per-loop normalization.** An inner index probe reports 20 rows and 2,500 loops. Total is 50,000 occurrences. A parent returning 50,000 rows is not unexplained amplification. Conclusion: normalize documented per-loop metrics before diagnosis.

### Example 3

**First estimate divergence.** Scan q-error is 1.2, filter 2, join 100, root aggregate 1. The join is the first threshold crossing; the accurate root count does not erase 100× intermediate work. Conclusion: traverse causal row flow, not just root accuracy.

### Example 4

**Same plan, slower runtime.** Plan and actual rows match healthy history, but lock wait rises from 0 to 1.2 seconds and storage is unchanged. The blocker holds rows while calling a remote service. Conclusion: shorten transaction/external wait; forcing an index cannot remove this first divergence.

### Example 5

**Changed plan, no regression.** A statistics update changes hash join to merge join, while p95, CPU, reads, spill, and throughput remain within gates. Conclusion: plan-shape change alone is not an incident and should not be forcibly reverted.

### Example 6

**Parameter sensitivity.** A point parameter uses an index in 10 ms; a 40%-selective range uses a scan in 800 ms. Forcing the point plan makes the range take 12 seconds. Conclusion: compare within parameter class and preserve a variant/custom policy.

### Example 7

**Candidate absence.** A text parameter is bound with an incompatible collation, so the expected index path is never enumerated. Lowering random-page cost cannot select a nonexistent candidate. Conclusion: repair binding/collation or the supported access expression before costing.

### Example 8

**Instrumentation trap.** Engineers enable per-node timing on every sub-millisecond query and logging becomes the bottleneck. Sampled production capture plus an isolated detailed replay preserves incident coverage with measured overhead. Conclusion: the observer belongs in the reproduction envelope.

### Example 9

**Forcing as containment.** A prior plan restores p99 during an incident. It is forced only for one fingerprint/class, with schema generation guard, failure alert, owner, 48-hour expiry, and unforce command. A statistics/correlation fix is tested separately. Conclusion: reversible containment buys diagnostic time without pretending to be the cure.

### Example 10

**Whole-workload correction.** A covering index cuts target latency 6× but adds 35% write latency, doubles replica lag, and expands backup time beyond its window. A narrower partial index plus rewritten predicate meets read and write gates. Conclusion: a query-local winner can be a production regression.

## Cross-Program Connections

- [Software Engineering Patterns](../../11-software-engineering-patterns/ROADMAP.md): hypothesis isolation, observability boundaries, feature flags, and rollback structure durable diagnosis.
- [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md): search-space coverage, counterfactual evaluation, q-error, robust choice, and regret formalize evidence.
- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md): indexes, histograms, sketches, caches, and trace stores determine diagnostic signals.
- [Data Engineering](../../19-data-engineering/ROADMAP.md): loads, partitions, compaction, statistics freshness, skew, and replay explain changing inputs.
- [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md): workload ownership, tenant boundaries, serving models, and SLOs define comparison classes.
- [Security Engineering](../../25-security-engineering/ROADMAP.md): query text, plans, literals, policies, and traces require least privilege, redaction, retention, and audit.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md): parameter binding, timeouts, retries, pagination, client backpressure, and tracing affect the observed query.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md): resource classes, fleet history, canaries, capacity, incident controls, and rollback operationalize remedies.

## References

1. PostgreSQL Global Development Group, [PostgreSQL 18: `EXPLAIN`](https://www.postgresql.org/docs/18/sql-explain.html), retrieved 2026-08-30. Current plan/actual options, formats, settings, buffers, WAL, serialization, planning memory, and execution caveats.
2. PostgreSQL Global Development Group, [PostgreSQL 18: `pg_stat_statements`](https://www.postgresql.org/docs/18/pgstatstatements.html), retrieved 2026-08-30. Current normalized statement, planning/execution, row, block, WAL, and timing aggregation.
3. PostgreSQL Global Development Group, [PostgreSQL 18: `auto_explain`](https://www.postgresql.org/docs/18/auto-explain.html), retrieved 2026-08-30. Current automatic slow-plan logging, sampling, formats, nested statements, settings, and overhead controls.
4. PostgreSQL Global Development Group, [PostgreSQL 18: Run-Time Statistics](https://www.postgresql.org/docs/18/runtime-config-statistics.html), retrieved 2026-08-30. Current query identifiers, I/O timing, statistics collection, and profiling controls.
5. Microsoft, [Monitor Performance by Using the Query Store](https://learn.microsoft.com/en-us/sql/relational-databases/performance/monitoring-performance-by-using-the-query-store), retrieved 2026-08-30. Current plan, runtime, wait, aggregation, retention, and history interfaces.
6. Microsoft, [Tune Performance with the Query Store](https://learn.microsoft.com/en-us/sql/relational-databases/performance/tune-performance-with-the-query-store), retrieved 2026-08-30. Current regression analysis, parameter variation, forcing, and unforcing workflow.
7. Microsoft, [`sp_query_store_force_plan`](https://learn.microsoft.com/en-us/sql/relational-databases/system-stored-procedures/sp-query-store-force-plan-transact-sql), retrieved 2026-08-30. Current plan-forcing semantics, permissions, failure behavior, and controls.
8. Oracle, [MySQL 8.4: `EXPLAIN`](https://dev.mysql.com/doc/refman/8.4/en/explain.html), retrieved 2026-08-30. Current plan formats and iterator-based `EXPLAIN ANALYZE` estimates, actual times, rows, and loops.
9. Oracle, [MySQL 8.4: Tracing the Optimizer](https://dev.mysql.com/doc/refman/8.4/en/optimizer-tracing.html), retrieved 2026-08-30. Current optimizer-decision trace interface and scope.
10. Oracle, [Oracle Database 23ai Performance Tuning Guide](https://docs.oracle.com/cd/G11854_01/tgdba/database-performance-tuning-guide.pdf), retrieved 2026-08-30. Current workload diagnostics, real-time SQL monitoring, plan statistics, and performance methodology.
11. Trino Software Foundation, [Trino 483: `EXPLAIN ANALYZE`](https://trino.io/docs/current/sql/explain-analyze.html), retrieved 2026-08-30. Current distributed execution plan, costs, statistics, and statement-execution behavior.
12. SQLite Project, [`EXPLAIN QUERY PLAN`](https://www.sqlite.org/eqp.html), retrieved 2026-08-30. Current high-level scan/search plan interpretation and output-stability warning.

## Exercises

### Exercise 1

Define semantic incorrectness, performance regression, instability, expected context sensitivity, first divergence, q-error, containment, and durable correction. Explain why plan change is neither necessary nor sufficient for regression.

### Exercise 2

Recompute every executable result, including node q-errors, per-loop total, latency fractions, slowdown, absolute impact, and hourly impact. State the zero conventions and evidentiary limits.

### Exercise 3

A query changed from 900 ms to 12 s after a release. The plan hash changed, statistics refreshed, traffic doubled, and storage p99 rose. Design a controlled diagnosis that can distinguish binding/rewrite, estimation/cost, cache/parameter, storage, lock, and workload causes.

### Exercise 4

Design safe containment and durable remediation for a parameter-sensitive regression where one prior plan helps 90% of calls but catastrophically harms the largest tenants. Include scope, observability, forcing failure, expiry, experiments, and removal criteria.

### Exercise 5

Design an elite cross-engine plan-regression evidence system for PostgreSQL, SQL Server, MySQL, Oracle, Trino, and SQLite without pretending their plan formats or metrics are identical. Include privacy, retention, overhead, causation, canaries, and rollback.

## Answers to the Exercises

### Answer 1

Semantic incorrectness changes the authorized query outcome: row values/multiplicities/order where required, errors, snapshot/transaction behavior, or side effects. A performance regression violates a predeclared comparable outcome/resource gate. Instability is material variation across executions sharing the declared identity/context; expected sensitivity is deliberate variation across parameter/resource classes whose optima differ. First divergence is the earliest supported causal-layer difference between baseline and incident. Q-error is symmetric multiplicative estimate discrepancy for positive actual/estimate. Containment reversibly bounds harm while diagnosis/correction proceeds. Durable correction removes the demonstrated causal defect and passes removal/whole-workload evidence.

A plan change is not necessary because identical physical structure can slow under larger inputs, cold/contended storage, memory denial/spill, skew, locks, queues, remote latency, retries, or client backpressure. It is not sufficient because a changed plan may preserve every semantic, latency, throughput, and resource gate. Even when plan and performance change together, parameters, statistics, data, resources, or workload can confound both. Controlled interventions and a row/resource-flow mechanism are needed for causation.

### Answer 2

Node q-errors are `max(120000/100000,...)=1.20`, `20000/10000=2.00`, `50000/500=100.00`, and `50/50=1.00`; threshold four first selects the join. Per-loop total is `20*2500=50,000`. Baseline mean is `(800+820+790)/3=803.33 ms`; incident mean `(4800+5200+5000)/3=5,000 ms`. Slowdown is `5000/(2410/3)=6.22`; absolute increase is `5000-2410/3=4,196.67 ms`. At 120/hour, extra database time is `4196.666...*120/1000=503.60 seconds/hour`. Accounted latency is `200+3000+1200+400=4800`, residual zero; execution fraction `3000/4800=.625` and lock fraction `1200/4800=.250`.

The code defines zero/zero q-error as one and one-zero/one-positive as infinity. Dashboards may cap infinity only if they retain the uncapped condition. Results prove finite arithmetic, first threshold under node order, and impact under the declared frequencies. They do not prove that the join is causal, that plan B caused the regression, that samples represent a distribution, that timing categories are independent, or that forcing plan A is correct/safe.

### Answer 3

First preserve incident evidence: exact and normalized statement, parameter values/classes and types, role/policy/search path, old/new plans and compilation context, schema/index/view/function/rewrite generations, before/after statistics and analyze event, engine/configuration, data/snapshot/distributions, plan/adaptation/cache events, traffic/concurrency, resources, storage telemetry, locks/waits, client boundaries, and release timeline. Verify semantic equivalence before performance. Normalize rows/loops/workers, bytes, memory/spill, waits, and end-to-end time.

Construct matched cells rather than one before/after pair: old/new application binding against the same database snapshot; old/new statistics clone with the same statement; prior/current plan under identical parameter classes, warm/cold policy, resource class, concurrency, and storage; point/broad/tenant classes with controlled first compilation; healthy/incident storage latency with the same plan; low/current traffic and lock-free/current blockers. Use a replica or bounded canary and alternate/randomize order. Nonexecuting plan/optimizer trace establishes binding, rewrite, candidate, estimate, cost, and search differences. Safe analyzed execution measures actual rows, loops, I/O, memory/spill, and time. History ties plans/waits to windows.

Find the first divergence. If new binding introduces a cast and removes an index candidate, repair binding. If candidate set is stable but a refreshed histogram misestimates a correlated join and controlled old/new statistics reverses the predicted plan/outcome, repair statistics/estimator. If only compile order/class changes behavior, repair cache/variant policy. If same plan/rows become slow only under elevated storage p99, address storage/cost calibration. If waits dominate, identify blocker chain. If doubling concurrency alone creates queues/spill, address admission/capacity/workload. Report remaining confounding; do not select the most convenient story.

### Answer 4

Do not force the 90%-plan globally. Define at least ordinary and largest-tenant parameter classes from authorized, stable features. Immediate containment may force the prior plan only for the ordinary class or route that class to a known compatible plan, while largest/unknown tenants retain custom/dispatcher planning or a robust fallback. Bind forcing to fingerprint, parameter/types, schema/policy generation, engine version, and resource class. Record owner, approval, start/expiry, plan ID, affected calls, forcing success/failure event, fallback behavior, errors, latency/resource regret by class, and exact unforce/rollback control. Cap duration and automatically disable on semantic discrepancy, plan incompatibility, p99/resource/fleet gates, or class uncertainty.

Diagnose why classes differ: conditional selectivity/cardinality, access path, join order/algorithm, memory, and compile-history evidence. Compare generic, per-class/custom, and guarded variants under matched workload. A durable remedy may be parameter-sensitive variants, corrected multivariate statistics, a schema/access path valid for both, or a robust query rewrite—each semantically differential-tested and evaluated for compile/cache, writes, storage, replicas, concurrency, and tails. Shadow classification, then canary ordinary, large, boundary, unknown, and drifted tenants against control. Removal criteria require the durable policy to pass semantic and per-class/fleet gates, forcing to be removed in a controlled cohort without regression, and rollback to remain tested. Expiry without a successful removal experiment escalates; it does not silently renew.

### Answer 5

Store a common envelope and typed evidence model, not a fake universal plan tree. Common fields include authorized fingerprint/exact-text reference; protected parameter class/types; role/policy/schema/statistics/software/configuration generations; plan identity and raw artifact; compile/cache/adaptation events; execution/time window; rows/loops/tasks; CPU, I/O/bytes, memory/spill, waits, latency boundaries; resources/concurrency; collection method/version/overhead; and retention/redaction policy. Each engine adapter preserves raw output and maps only documented semantics with provenance: PostgreSQL EXPLAIN/pg_stat_statements/auto_explain, SQL Server Query Store and forcing events, MySQL EXPLAIN ANALYZE/optimizer trace, Oracle SQL monitoring/workload diagnostics, Trino distributed analyzed plans, and SQLite's explicitly unstable interactive plan output. Unknown fields remain unknown.

Version normalization and plan-diff rules per engine/build. Encrypt and least-privilege raw SQL/plans/traces; tokenize or classify literals/tenants; separate policy-sensitive artifacts; audit access; bound retention and deletion. Calibrate overhead, sample by latency/class, preserve rare failures, record aggregation/reset/eviction gaps, and use safe nonexecuting capture for mutating or side-effecting SQL. Detection combines outcome distributions, plan history, first-cardinality divergence, spill/waits/resources, and workload changes; plan hash alone is informational.

For causation, automatically assemble matched baseline/incident envelopes and propose bounded single-variable experiments, never auto-force arbitrary plans. Differentially verify semantics, replay representative and adversarial parameter/concurrency/resource classes, execute eligible alternatives safely, and report regret plus confounders. Shadow candidate remedies, then canary fingerprint/class/tenant/replica cohorts with correctness, error, p50/p95/p99, throughput, CPU/I/O/memory/spill/wait, write/replica/storage, and fleet gates. Every forcing/config/index/rewrite has owner, generation, failure telemetry, expiry/removal criteria, kill switch, and tested rollback. Evidence remains scoped to captured versions, contexts, workloads, and threat model; it does not prove cross-engine equivalence, universal optimizer correctness, privacy, certification, or external review.
