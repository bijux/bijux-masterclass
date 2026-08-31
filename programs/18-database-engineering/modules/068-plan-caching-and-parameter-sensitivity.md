---
module_id: DBE-068
program: Database Engineering
level: 2
module_number: 68
title: Plan Caching and Parameter Sensitivity
status: complete
last_verified: 2026-08-30
---

# Plan Caching and Parameter Sensitivity

## One-Page Review

### Governing question

When may a database safely reuse compiled work, and how should it avoid reusing one physical plan for parameter values whose best plans differ materially?

### Essential definitions

A **prepared statement** separates parsing and analysis from repeated execution. A **plan cache** stores reusable compiled artifacts; it is not a result cache or a buffer pool. A **custom plan** is optimized with the current parameter values. A **generic plan** is optimized without those values and can be reused broadly. **Parameter sensitivity** exists when parameter values change cardinalities, physical properties, resource demand, or the best feasible plan. **Parameter sniffing** uses values visible at compilation as optimizer inputs. A **dispatcher** classifies an execution and selects among plan variants. **Invalidation** makes a cached artifact ineligible when one of its semantic or physical dependencies changes. **Plan regret** is realized cost of the selected cached plan minus realized cost of a reference-best eligible plan.

### Central model, mechanism, or theorem

Reuse is sound only when the cache identity and dependency generation preserve the statement's binding, authorization, semantics, and physical assumptions. Profitability then balances compilation cost against execution regret. For executions (i=1..n), policy (P) has total cost

$$
C(P)=C_{compile}(P)+\sum_i[C_{dispatch}(P,i)+C_{run}(plan(P,i),x_i)].
$$

A generic plan amortizes compilation but can pay large regret on skewed parameter classes. Per-execution custom planning adapts but repeatedly compiles. A dispatcher pays classification and variant-management costs to reuse several plans over disjoint, guarded parameter regions.

### Critical invariants

- Cache identity includes the bound statement, parameter types and semantic context; textual resemblance is insufficient.
- Reuse requires every recorded dependency generation to remain valid, including relevant schema, functions/operators, policies, statistics or model contract, configuration, and physical capabilities.
- Runtime parameters are data, not trusted cache-key syntax; literal values must be redacted or access-controlled in traces.
- A generic plan must not silently depend on a sampled, sniffed, or first-execution value.
- Dispatcher regions are total for the admitted domain, deterministic at boundaries, and paired with a safe fallback for unknown or out-of-distribution values.
- Variant selection never changes query results, snapshot, privileges, row policies, or transactional behavior.
- Evaluation reports compilation CPU, cache memory/churn, runtime distribution, tail latency, resource use, and regret—not cache-hit rate alone.

### Common failures

Failures include keying only by SQL text; confusing prepared statements with guaranteed plan reuse; letting the first execution dictate all later plans; treating average selectivity as representative; failing to invalidate after a semantic dependency changes; embedding tenant or privilege context in a shared reusable plan; generating one variant per value; measuring a warm cache against a cold alternative; forcing a plan indefinitely; and declaring a dispatcher successful because mean latency fell while p99, compilation storms, or memory grew.

### Compact example

For 80 small and 20 large executions, an index costs 20.50 for a small value but 2,520 for a large one; a scan costs 1,000. Including compilation, one generic index plan averages 520.45, one generic scan averages 1,000.05, custom planning averages 221.40, and a two-variant dispatcher averages 217.10. The dispatcher wins this finite workload. If the first small value fixes an index plan, a later large value pays 1,520 regret; reversing execution order makes a small value pay 1,000 under a scan. This demonstrates history sensitivity, not a universal policy.

### Connections

Retrieve [Cardinality Estimation](064-cardinality-estimation.md), [Cost Models](065-cost-models.md), [Join Ordering](066-join-ordering.md), and [Access-Path Selection](067-access-path-selection.md). Continue through [the roadmap](../ROADMAP.md) to Adaptive Query Processing, which changes decisions after execution begins.

## Governing Question

Compilation transforms a statement into executable machinery: parse and bind names, infer types, rewrite expressions, enumerate alternatives, estimate quantities, choose physical operators, allocate runtime structures, and sometimes generate code. Repeating all of that for a frequently executed statement wastes CPU and adds latency. Reusing it blindly is also dangerous. A plan selected for one customer, date range, search term, or optional predicate may be disastrous for another.

The governing question is therefore two questions joined by an invariant. First, under which contexts is a compiled artifact semantically eligible for reuse? Second, among eligible policies, when is reuse economically preferable to replanning or maintaining several variants? Semantic eligibility is non-negotiable; cost optimization operates only inside it.

## Why This Matters

Plan caching sits on a high-leverage path. A tiny compilation saving multiplied by millions of executions can free substantial CPU. Conversely, a reused nested loop, narrow index path, serial aggregate, undersized memory grant, or unselective remote lookup can turn a millisecond request into seconds, spills, lock retention, queueing, and a fleet-wide incident. Cache misses and simultaneous invalidations can also create compile storms that consume the very capacity needed to execute queries.

The subject crosses abstractions. Language semantics determine which statements and contexts are equivalent. Optimizer models decide whether values matter. Runtime systems govern memory, concurrency, eviction, and observability. Security determines whether artifacts, estimates, and traces may cross principals or tenants. Operations determines rollout and recovery. “The plan is cached” is therefore not a complete design or diagnosis.

Modern systems expose several policies. PostgreSQL 18 distinguishes custom and generic prepared-statement plans and exposes `plan_cache_mode`; its `EXPLAIN` can request a generic-plan view. SQL Server documents compilation using parameter values, parameter-sensitive plan optimization with a dispatcher and variants, and optional-parameter plan optimization in current releases. Oracle documents adaptive cursor sharing through bind-sensitive and bind-aware cursors. These are concrete implementations of a durable problem: map an execution context to a sound, low-regret reusable artifact.

## Prerequisites and Retrieval

Before this module, retrieve these ideas.

- From [Cardinality Estimation](064-cardinality-estimation.md): selectivity is conditional, skew and correlation defeat one global average, and estimates must declare whether parameters are known.
- From [Cost Models](065-cost-models.md): costs are scoped predictions with uncertainty, not elapsed-time guarantees.
- From [Join Ordering](066-join-ordering.md): cardinality changes can reverse join order and algorithm choice.
- From [Access-Path Selection](067-access-path-selection.md): selectivity, ordering, covering, and parameterization can reverse scan choice.
- From transactions and security: snapshot and policy are runtime semantic constraints even when the compiled skeleton is reusable.

The chapter assumes relational algebra, SQL null semantics, histograms, indexes, joins, memory grants, and latency percentiles. It does not assume a particular engine's cache implementation.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish statement preparation, plan compilation, plan caching, data caching, and result caching;
2. construct a cache identity and dependency set that protects semantics and authorization;
3. derive when generic, custom, recompiled, or multi-variant policies win;
4. detect parameter sensitivity from distributions, plan transitions, and realized regret;
5. design total, stable dispatcher regions with bounded variants and safe fallbacks;
6. diagnose cache misses, stale plans, pollution, invalidation storms, and history-dependent regressions;
7. validate and roll out a cache-policy change with semantic, performance, resource, security, and rollback evidence.

## Core Exposition

**Separate four kinds of reuse.** Preparation can retain parsed and analyzed statement state. Plan caching can retain a selected physical plan or optimizer artifact. A buffer pool caches database pages; an operating-system or object cache may cache bytes. A result cache stores answers under much stronger data-version, context, and determinism conditions. Warming the buffer pool can make a plan faster without increasing plan-cache reuse. Reusing a plan says nothing about whether its input pages or results are cached. Diagnostics must name the layer.

**Define semantic identity before looking at hits.** Raw SQL text is sometimes one input, never a sufficient universal identity. Equivalent text can bind differently because of database, schema search path, temporary objects, parameter types and lengths, collation, time zone, role, row-level policy, functions, operators, extensions, session settings, or compatibility mode. Conversely, harmless literal differences can create separate entries unless statements are parameterized or normalized safely.

A robust key points to a bound representation plus relevant context, not merely a string. It must distinguish `varchar(10)` from `varchar(4000)` when coercion or index compatibility changes, and distinguish two schemas where the same unqualified name resolves to different objects. It must not place secrets or raw tenant literals in broadly readable telemetry. Parameterization is a semantic transformation: preserve types, nulls, collations, implicit casts, constant-folding rules, and security behavior before expecting reuse.

**Record dependencies, not just a key.** A cache entry is eligible only while its assumptions remain valid. Dependencies can include object and index generations, column/type/collation definitions, function and operator implementations, constraints used in proofs, views, partition maps, row policies, privileges, extensions, optimizer configuration, statistics/model generations, storage capabilities, and generated-code ABI. Some changes demand invalidation for correctness; others make a plan merely stale or less profitable. Keep those categories separate.

Snapshot visibility normally remains an executor input rather than making every snapshot a distinct plan key. Yet a plan may contain access methods whose eligibility or cost relies on snapshot-related capabilities. The durable rule is not “key by snapshot”; it is “compile only assumptions certified reusable across the snapshots admitted by the plan contract, and enforce the actual snapshot at execution.” The same reasoning applies to current transaction state, locks, and memory availability.

**Generic versus custom.** Let `x` be a parameter vector. A custom plan optimizes with `x`; a generic plan uses a value-independent estimate or representative distribution. PostgreSQL's documented automatic policy initially uses custom plans, then compares their estimated costs with a generic alternative; its forced modes are valuable for controlled diagnosis. This is an engine policy, not proof that five samples or any fixed heuristic is optimal for every workload.

The correct comparison includes compilation. If generic plan `g` is compiled once for `n` executions,

$$
C_g=C_{compile}(g)+\sum_{i=1}^{n}C_{run}(g,x_i).
$$

If each execution is custom-planned,

$$
C_c=\sum_{i=1}^{n}[C_{compile}(p_i)+C_{run}(p_i,x_i)].
$$

Custom planning wins only when avoided execution regret exceeds extra planning cost and its operational externalities. A request can tolerate 5 ms compilation and save seconds; a micro-query executing millions of times may not. Compare CPU saturation and queueing as well as per-query latency.

**Where sensitivity comes from.** Parameter values alter selectivity under skew, heavy hitters, null prevalence, correlation, temporal hotspots, tenant size, and out-of-range values. Those changes can reverse access path, join order, join algorithm, aggregation strategy, parallelism, partition pruning, remote pushdown, materialization, memory grant, or row-goal behavior. Correlated parameters matter jointly: separate one-dimensional buckets for `country` and `city` can classify an impossible or highly selective combination incorrectly.

Optional predicates are a distinct shape. `WHERE region = :r OR :r IS NULL` means a point/range restriction in one class and no restriction in another. A single safe plan may scan broadly because it must serve the null case. Current SQL Server documentation describes optional-parameter plan optimization that dispatches between variants. The durable design is a total semantic split with an explicit null boundary, not reliance on a product label.

Resource sensitivity also matters. The same cardinality can require a different plan when memory, concurrency, accelerator availability, replica lag, or remote-service limits differ. Do not smuggle rapidly changing resource state into an unbounded cache key. Define a small set of certified resource classes, a fallback, and revalidation rules.

**Why first-execution sniffing becomes history-dependent.** Using current values at compile time is often beneficial: estimates become specific. Trouble begins when the resulting plan is installed as if representative. Then execution order becomes a hidden input. A first rare value may choose an index and nested loop that explodes on a common value; a first broad value may choose a scan/hash plan that wastes work for later point lookups. Restart, eviction, deployment, or failover changes which value arrives first, so the incident appears intermittent.

Parameter sniffing itself is not synonymous with a defect. Without it, every execution may receive a bland generic estimate. The defect is a mismatch among sensitivity, reuse scope, and policy. Diagnose the compile-time value or class, the later execution classes, the selected plan and estimates, and a same-environment alternative. Avoid folklore such as “always recompile” or “disable sniffing.”

**Multi-plan and parametric optimization.** Parametric query optimization studies the best plan as cost parameters vary. Ganguly's formulation associates plans with regions of parameter space; under linear cost functions, optimality regions have convex polyhedral structure. Real optimizers add discrete choices, nonlinear estimates, budgets, and uncertainty, so implementations typically approximate the region map.

A dispatcher implements such an approximation. It first maps `x` and selected context into a class, then invokes a cached variant. A good classifier has:

- a declared feature set and versions;
- disjoint boundaries with explicit equality/null behavior;
- total coverage or an explicit generic/custom fallback;
- bounded variant count and memory;
- enough observations before splitting or merging;
- hysteresis to prevent churn near a boundary;
- invalidation links from dispatcher to variants;
- per-class coverage, regret, and drift telemetry.

Boundaries commonly follow histogram ranges, heavy hitters, null/non-null, tenant-size classes, or learned partitions. They are policy hypotheses. Statistics change, tenants grow, correlations drift, and cost crossovers move. Never present a bucket boundary as a semantic guarantee unless it is derived from a constraint; it normally selects performance behavior only.

Recent research explores learned plan selection for parameterized queries. Kepler searches candidate plans and learns value-dependent selection from execution data while addressing regressions in its evaluated settings. RankPQO uses learned ranking to reduce candidate-selection work. These results broaden the design space but do not remove semantic validation, workload shift, feature privacy, exploration cost, or fallback requirements. A learned selector is one versioned dispatcher policy, not an oracle.

**Invalidation, eviction, and staleness.** Invalidation responds to changed dependencies. Eviction responds to finite capacity. Re-optimization responds to evidence that an eligible plan is no longer economical. Confusing them causes both correctness risks and cache churn. Use generation-checked publication: compile against dependency vector `d`, then install only if the current vector still equals `d`. At execution, validate the entry's generations or acquire a mechanism that prevents incompatible changes during use.

Statistics refresh may trigger immediate replan, lazy replan, age/feedback thresholds, or no automatic replan depending on the engine and dependency contract. Whatever the policy, record it. A syntactically valid cached plan can be badly stale after distribution or scale changes. Conversely, invalidating every plan after any metadata change causes unnecessary storms.

Eviction should account for size, compilation cost, reuse frequency, recent use, variant family, and harm. Pure least-recently-used policy can evict an expensive-to-compile periodic report just before each run. Pinning everything leaks memory. Admit entries only after evidence of reuse where appropriate, cap variants per fingerprint/tenant, and protect the cache from literalized ad hoc queries. Current SQL Server guidance describes optimizing storage for one-off ad hoc workloads; the general principle is to avoid spending full cache space before reuse is demonstrated.

**Concurrency and publication.** If many sessions miss the same entry, compiling independently wastes CPU. Single-flight compilation can elect one builder while others wait, use an older eligible plan, or compile under a bounded budget. But a global lock can serialize unrelated queries, and waiting behind a long compile can violate latency goals. Partition locks by identity, provide timeout/fallback, publish immutable entries atomically, and ensure a failed compile cannot poison the cache.

Feedback loops need the same discipline. Runtime row counts or memory outcomes can improve future plans, but concurrent, aborted, adversarial, or unrepresentative executions must not overwrite stable policy blindly. Aggregate by authorized identity/class, track sample size and censoring, version the feedback, bound influence, and retain rollback.

**Security and isolation.** A plan can embed object identifiers, policy-expanded predicates, cardinality estimates, partition bounds, compiled expressions, or generated code. Reusing it across roles or tenants may violate authorization even if results are rechecked later, and timing/plan telemetry may reveal distribution. Key or guard on every context that affects semantics and access. Prefer shared artifacts only when their contract is explicitly principal-independent. Redact literals, restrict plan inspection, isolate feedback, authenticate invalidation events, and threat-model deliberate cache flooding or classifier manipulation.

**Diagnose by first divergence.** Capture an authorized, redacted fingerprint; parameter types and class; compile/reuse times; cache identity; dependency generations; dispatcher and variant; estimated and actual rows; operator/runtime metrics; relevant resource class; invalidation/eviction reason; and comparison plan. Ask in order:

1. Did equivalent executions map to the intended identity, or did key fragmentation/collision occur?
2. Was the entry semantically eligible under current bindings, policy, and generations?
3. Which values/context informed compilation, and what class did later values occupy?
4. Was sensitivity visible in cardinality, access, join, memory, parallelism, or remote behavior?
5. Did policy classify correctly, and was a better eligible variant available?
6. Did runtime conditions rather than parameters explain the difference?
7. Did eviction, invalidation, or concurrency cause a compile storm?

Reproducing with one fast parameter proves little. Compare multiple classes in controlled order, clear or isolate only the intended cache layer, keep data/buffer warmth comparable, and measure compilation separately.

**Validate in layers.** Semantic tests vary schemas/search paths, parameter types, collations, nulls, roles, policies, temporary objects, transactions, and dependency changes. They establish that reuse cannot alter results or authority. Classification tests cover every boundary, unknown value, missing feature, and resource class. Small exhaustive workloads can compare generic, custom, and dispatcher decisions with all candidate plans. Production-like replay measures compilation CPU, planning latency, cache hit/admission/eviction, memory, variant count, runtime, spill, I/O, network, locks, throughput, and percentiles by class.

The executable below validates only a finite arithmetic model. It intentionally makes the large parameter prefer a scan and the small parameter prefer an index.

<!-- bijux-verify: {"id":"finite-plan-cache-policy","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"executions=100\nsmall_executions=80\nlarge_executions=20\ngeneric_index_avg=520.45\ngeneric_scan_avg=1000.05\ncustom_avg=221.40\ndispatcher_avg=217.10\nbest_policy=dispatcher\nsmall_plan=index\nlarge_plan=scan\nsniffed_small_large_cost=2520.00\nsniffed_large_small_cost=1000.00\nlarge_regret=1520.00\nhistory_sensitive=true\ninvalidation_generation=required\nevidence=finite_parameter_workload\n","stderr":""}} -->
```python
small_executions = 80
large_executions = 20
compile_once = 5.0
compile_custom = 5.0
compile_dispatcher = 20.0
dispatch_cost = 0.5


def index_cost(rows):
    return 20.0 + rows * 0.05


def scan_cost():
    return 1000.0


small_index = index_cost(10)
large_index = index_cost(50000)
small_scan = scan_cost()
large_scan = scan_cost()
executions = small_executions + large_executions

generic_index = compile_once + small_executions * small_index + large_executions * large_index
generic_scan = compile_once + executions * scan_cost()
custom = executions * compile_custom + small_executions * min(small_index, small_scan) + large_executions * min(large_index, large_scan)
dispatcher = compile_dispatcher + executions * dispatch_cost + small_executions * min(small_index, small_scan) + large_executions * min(large_index, large_scan)

averages = {
    "generic_index": generic_index / executions,
    "generic_scan": generic_scan / executions,
    "custom": custom / executions,
    "dispatcher": dispatcher / executions,
}

print(f"executions={executions}")
print(f"small_executions={small_executions}")
print(f"large_executions={large_executions}")
print(f"generic_index_avg={averages['generic_index']:.2f}")
print(f"generic_scan_avg={averages['generic_scan']:.2f}")
print(f"custom_avg={averages['custom']:.2f}")
print(f"dispatcher_avg={averages['dispatcher']:.2f}")
print(f"best_policy={min(averages, key=averages.get)}")
print(f"small_plan={'index' if small_index < small_scan else 'scan'}")
print(f"large_plan={'index' if large_index < large_scan else 'scan'}")
print(f"sniffed_small_large_cost={large_index:.2f}")
print(f"sniffed_large_small_cost={small_scan:.2f}")
print(f"large_regret={large_index - large_scan:.2f}")
print("history_sensitive=true")
print("invalidation_generation=required")
print("evidence=finite_parameter_workload")
```

**Evaluate alternatives, not folklore.** A controlled experiment should compare forced generic, forced custom/recompile, and candidate multi-variant policies where the engine permits it. Partition measurements by parameter class and execution order. Include an unchanged control cohort. Reject a change that improves the target fingerprint while creating system-wide compile pressure, cache displacement, memory growth, or workload interference.

**Productionize reversibly.** Version identity rules, dependency tracking, normalization, estimates/models, classifier, thresholds, and variants. Shadow classification without changing execution; compare predicted class and alternative cost. Canary bounded fingerprints, principals, tenants, and resource pools with semantic checks, compilation and cache budgets, tail-latency/resource gates, and a kill switch. Preserve an eligible generic or previous policy for rollback. Do not clear an entire production cache as an ordinary deployment step: that changes thousands of workloads simultaneously and destroys causal evidence.

## Definitions and Notation

- **S, x, c**: bound statement, runtime parameter vector, and semantic/resource context.
- **K(S,c)**: cache identity derived from the statement and relevant context.
- **D**: versioned dependency vector required by an entry.
- **g**: generic plan independent of the current parameter values under its contract.
- **p(x)**: custom plan optimized using parameter vector x.
- **δ(x,c)**: dispatcher mapping to a guarded plan variant or fallback.
- **Parameter class**: region whose values share a policy decision; it is not necessarily a semantic equivalence class.
- **Compile cost**: planning CPU/latency and associated contention or code-generation work.
- **Regret**: `realized(selected) - realized(reference best eligible)` under a declared metric.
- **Cache pollution**: capacity consumed by low-value entries that displace more valuable ones.
- **Invalidation storm**: burst of entry invalidations and recompilations following a dependency or deployment event.
- **History dependence**: behavior changes when execution order changes although the multiset of requests is unchanged.
- **Fallback**: certified plan or planning path used when classification, availability, or evidence is insufficient.

“Generic” means value-independent within a plan's declared parameter contract; it does not mean context-free, permanent, or universally optimal. “Custom” means value-informed for an execution, not necessarily globally optimal.

## Mechanisms, Invariants, or Proof Structure

**Reuse-soundness argument.** Suppose entry `e` was compiled from bound statement `S`, context projection `c*`, and dependencies `D`. Reuse for `(S',c')` is sound only if identity proves the same bound semantics over every omitted context dimension, guards establish compatible authorization and capabilities, and all dependency generations in `D` still match. The executor must still enforce current parameters, snapshot, locks, and policies promised as runtime inputs. A text hash alone proves none of these premises.

**Amortization threshold.** Compare a generic plan with per-execution custom planning. Let `r_i=C_run(g,x_i)-C_run(p_i,x_i)` be generic execution regret and `k_i` the extra custom compilation cost. Custom planning is cheaper exactly when `sum(r_i) > sum(k_i)` after adding dispatch, contention, and memory terms consistently. This derivation explains why “custom is faster at runtime” is insufficient: saved execution time may be smaller than compilation cost.

**Dispatcher partition.** For admitted domain X, regions `R_1...R_m` must be disjoint and cover X, or uncovered values must map to fallback F. Every boundary has one owner, including null and equality cases. The selected variant may change physical work but must implement the same relational result and authorization. Performance optimality is empirical; semantic equivalence is mandatory.

**Generation-safe publication.** Read dependency vector `D0`; compile; before publishing, compare current vector `D1`. Publish only if `D0=D1`, otherwise retry or fall back. Execution rechecks or protects the generations until it has safely acquired the referenced objects. This prevents a plan compiled concurrently with DDL from entering the cache under a false generation.

**Bounded adaptation.** A feedback-driven split needs minimum evidence and estimated benefit exceeding compilation, memory, and churn costs. Merge or evict variants with hysteresis so noisy observations near a boundary do not repeatedly reverse policy. Bound variants globally and per identity. Unknown or low-confidence classifications use fallback rather than extrapolating silently.

**Evidence ladder.** Static inspection establishes key/dependency coverage. Differential execution establishes tested semantic equivalence. Exhaustive finite candidate execution establishes scoped regret. Replay establishes workload behavior under recorded conditions. Canary establishes bounded production outcomes. No rung proves universal optimality, absence of side channels, or correctness for contexts outside its coverage.

## Alternatives and Trade-Offs

**Always generic** minimizes compilation and variant memory and gives stable behavior; it can have severe regret under skew. **Always custom/recompile** adapts to current values and new statistics; it spends planning CPU, adds latency, and can create storms. **Automatic generic/custom selection** balances observed planning estimates; it may miss rare but costly classes or inherit model error.

**A few guarded variants** capture important skew while amortizing compilation; classification, memory, invalidation, and boundary drift become new failure surfaces. **Fine-grained parametric regions** can reduce regret further; construction and maintenance may dominate, especially in many dimensions. **Learned selection** can model complex regions; it needs representative execution data, exploration controls, calibrated uncertainty, privacy protection, and a deterministic fallback.

**Literal queries** expose exact constants for optimization but fragment cache identity and risk sensitive telemetry. **Parameterized queries** improve reuse and injection safety when used correctly, but hide exact values from a generic plan and can change type/coercion behavior if the client binds poorly. **Plan hints/baselines** provide emergency stability; they freeze assumptions and require expiry/removal evidence.

**Eager invalidation** quickly removes stale assumptions but creates synchronized recompilation. **Lazy generation checks** spread work and retain unaffected entries but require precise dependency tracking. **Large caches** reduce capacity misses but consume memory and can retain stale/low-value variants; **small caches** churn expensive plans. Admission and family-aware eviction are usually more informative controls than size alone.

## Failure Modes and Misconceptions

1. “Prepared means one plan is always reused” confuses statement lifecycle with engine policy and invalidation.
2. “Same SQL text means same statement” ignores binding, types, collation, schema, role, policy, and session semantics.
3. “Different literal text must be different plans” ignores safe normalization and parameterization opportunities.
4. “A high hit ratio proves success” ignores per-hit regret, p99, memory, and compile storms.
5. “The first plan was fast, so caching is correct” ignores later parameter classes and execution order.
6. “Parameter sniffing is always bad” ignores the value of specific estimates and the actual reuse-policy mismatch.
7. “The average parameter is representative” fails for heavy tails, optional predicates, tenants, and correlated vectors.
8. “One bucket per column handles correlation” can classify impossible or high-frequency combinations incorrectly.
9. “DDL is the only invalidation cause” ignores functions, policies, privileges, settings, statistics policy, capabilities, and extensions.
10. “Snapshot must be in every key” confuses runtime visibility with compile-time identity; the plan contract decides what is reusable.
11. “One variant per value is optimal” ignores capacity, compilation, sparse evidence, and adversarial pollution.
12. “Clearing the cache diagnoses the query” changes compilation, data warmth, contention, and unrelated workloads.
13. “A forced plan proves the optimizer defect” shows one alternative under one environment, not the causal divergence.
14. “A learned selector removes the need for safeguards” ignores shift, uncertainty, poisoning, privacy, and fallback.
15. “Cross-tenant reuse is safe because rows are filtered later” can leak metadata/timing or embed unauthorized bindings and policy.

## Worked Examples

### Example 1

**Compilation amortization.** A generic plan costs 40 ms to compile and 3 ms per execution. Custom planning costs 4 ms plus 1 ms execution. For 10 calls, generic costs 70 ms and custom 50 ms; for 100 calls, generic costs 340 ms and custom 500 ms. Conclusion: reuse break-even depends on horizon and execution regret, not runtime alone.

### Example 2

**History-dependent sniffing.** The executable's small value selects a 20.50 index plan; installing it globally makes a large value cost 2,520 instead of a 1,000 scan. If a large value arrives first, the cached scan makes a later small value cost 1,000 instead of 20.50. Conclusion: execution order is an unintended policy input when a sniffed plan is reused beyond its class.

### Example 3

**Optional parameter boundary.** `region=:r OR :r IS NULL` has two semantic classes. Non-null can seek matching region; null makes the predicate true for every row and favors a scan in a large table. Dispatcher rules `is null -> broad` and `is not null -> selective` are disjoint and total. Conclusion: null needs an explicit guarded variant, not an average-selectivity estimate.

### Example 4

**Correlated vector counterexample.** A classifier has separate buckets for `country='SE'` and `city='Paris'`; each looks common in its marginal. Their conjunction is impossible in clean data, while `FR,Paris` is common. Multiplying or independently dispatching marginals selects a broad plan for zero rows. Conclusion: parameter sensitivity can be joint and needs correlation-aware classes or a conservative fallback.

### Example 5

**Type-fragmented cache.** Two clients execute the same visible statement but bind an identifier as `varchar(36)` and `nvarchar(4000)`. The latter introduces a conversion and different access eligibility; treating them as identical can be unsound or slow, while treating every observed length as unique pollutes the cache. Conclusion: identity must preserve meaningful type semantics and normalize only proven-irrelevant dimensions.

### Example 6

**Generation race.** Session A reads index generation 7 and begins compilation. Session B drops/replaces the index, producing generation 8. A finishes with a plan referencing generation 7. Publication compares generations and rejects the entry; execution falls back or recompiles. Conclusion: invalidation notification alone is insufficient without generation-safe publication.

### Example 7

**Variant boundary.** Index cost is `20+0.05r`; scan cost is 1,000. Equality occurs at `r=(1000-20)/0.05=19,600`. A dispatcher assigns exactly 19,600 to one declared side, monitors error around the estimate, and uses hysteresis before moving the boundary. Conclusion: mathematical crossover informs a policy boundary but estimation uncertainty prevents false precision.

### Example 8

**Cache pollution.** A service emits 100,000 literalized one-off timestamps. Full compiled entries displace a 2 MB plan used every minute and cause repeated expensive recompilation. Parameterizing timestamps, admitting a compact stub until second use, and capping a fingerprint family preserve capacity. Conclusion: admission policy and query generation can matter more than nominal cache size.

### Example 9

**Misleading benchmark.** Engineers clear every cache, run a custom alternative after it warms data pages, then compare it with the first cold cached execution. The result mixes plan compilation, plan cache, buffer warmth, and storage effects. A controlled test alternates policies, records both planning and runtime, fixes parameter class and environment, and repeats. Conclusion: isolate cache layers before attributing causality.

### Example 10

**Production rollout.** A two-variant policy reduces median latency for a skewed tenant query but triples compile CPU during a schema deployment and exposes raw tenant IDs in traces. The release is rejected. The revision redacts identities, links variants to precise generations, single-flights compilation, caps families, shadows classifications, canaries tenant cohorts, and retains the generic fallback. Conclusion: an elite cache policy satisfies semantic, security, resource, tail, and recovery criteria together.

## Cross-Program Connections

- [Programming Languages: Object-Oriented Programming](../../02-programming-languages-object-oriented-programming/ROADMAP.md): identity, immutability, encapsulated cache entries, and safe publication shape implementation.
- [Programming Languages: Functional Programming](../../03-programming-languages-functional-programming/ROADMAP.md): referential reasoning, memoization keys, purity, and explicit effects clarify when reuse is sound.
- [Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md): single-flight compilation, generation races, immutable publication, and contention govern concurrent caches.
- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md): hash tables, eviction queues, sketches, interval maps, and bounded indexes implement cache and dispatcher structures.
- [Data Engineering](../../19-data-engineering/ROADMAP.md): skew, partition evolution, workload replay, and data quality determine parameter classes.
- [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md): tenant boundaries, serving models, workload ownership, and semantic contexts govern reuse scope.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md): client parameter typing, query construction, admission, SLOs, and retries influence plan-cache behavior.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md): fleet configuration, observability, deployment waves, capacity, and rollback operationalize plan policy.

## References

1. Sumit Ganguly, [“Design and Analysis of Parametric Query Optimization Algorithms”](https://www.vldb.org/conf/1998/p228.pdf), *VLDB 1998*. Primary formulation of plan-optimality regions and parametric query optimization.
2. PostgreSQL Global Development Group, [PostgreSQL 18: `PREPARE`](https://www.postgresql.org/docs/18/sql-prepare.html), retrieved 2026-08-30. Current prepared-statement lifecycle, custom/generic selection, re-analysis, and replanning behavior.
3. PostgreSQL Global Development Group, [PostgreSQL 18: Query Planning Configuration](https://www.postgresql.org/docs/18/runtime-config-query.html), retrieved 2026-08-30. Current `plan_cache_mode` automatic, forced-custom, and forced-generic controls.
4. PostgreSQL Global Development Group, [PostgreSQL 18: `EXPLAIN`](https://www.postgresql.org/docs/18/sql-explain.html), retrieved 2026-08-30. Current generic-plan inspection and plan evidence interface.
5. PostgreSQL Global Development Group, [PostgreSQL 18: PL/pgSQL Plan Caching](https://www.postgresql.org/docs/18/plpgsql-implementation.html#PLPGSQL-PLAN-CACHING), retrieved 2026-08-30. Current function-expression and prepared-statement caching behavior.
6. Microsoft, [Query Processing Architecture Guide](https://learn.microsoft.com/en-us/sql/relational-databases/query-processing-architecture-guide), retrieved 2026-08-30. Current SQL Server compilation, reuse, parameterization, and parameter-sniffing architecture.
7. Microsoft, [Parameter Sensitive Plan Optimization](https://learn.microsoft.com/en-us/sql/relational-databases/performance/parameter-sensitive-plan-optimization), retrieved 2026-08-30. Current dispatcher, boundary, and query-variant design.
8. Microsoft, [Optional Parameter Plan Optimization](https://learn.microsoft.com/en-us/sql/relational-databases/performance/optional-parameter-optimization), retrieved 2026-08-30. Current optional-predicate dispatcher and variant behavior.
9. Oracle, [Oracle Database SQL Tuning Guide: Adaptive Cursor Sharing](https://docs.oracle.com/en/database/oracle/oracle-database/19/tgsql/improving-rwp-cursor-sharing.html), retrieved 2026-08-30. Bind-sensitive and bind-aware cursor behavior.
10. Ryan Marcus et al., [“Kepler: Robust Learning for Faster Parametric Query Optimization”](https://www.vldb.org/pvldb/vol16/p1736-marcus.pdf), *PVLDB 16*, 2023. Primary learned plan-candidate and parameter-dependent selection study.
11. Guoliang Li et al., [“RankPQO: Learning-to-Rank for Parametric Query Optimization”](https://www.vldb.org/pvldb/vol18/p1647-li.pdf), *PVLDB 18*, 2025. Primary recent learned ranking approach for parametric plan selection.
12. Microsoft, [Optimize for Ad Hoc Workloads Server Configuration Option](https://learn.microsoft.com/en-us/sql/database-engine/configure-windows/optimize-for-ad-hoc-workloads-server-configuration-option), retrieved 2026-08-30. Current plan-cache admission guidance for one-use ad hoc batches.

## Exercises

### Exercise 1

Define the minimum cache identity and dependency records for a parameterized query that uses an unqualified table name, a tenant row policy, a user-defined function, an index, and a timestamp parameter.

### Exercise 2

Using the executable workload, recompute all four policy averages, the index/scan crossover row count, and the regret caused by reusing the small-value index plan for a large value. State what the arithmetic does and does not prove.

### Exercise 3

A query is fast after restart for tenant A, then slow for tenant B; reversing their first-execution order reverses the outcome. Design a diagnosis that separates parameter sensitivity from buffer warmth, statistics drift, locking, and resource contention.

### Exercise 4

Design a bounded dispatcher for parameters `(tenant_id, start_time, end_time, include_archived)` where tenants and time windows are skewed and correlated. Specify regions, fallbacks, invalidation, telemetry, and anti-churn rules.

### Exercise 5

Design a production validation and rollout protocol for replacing a generic-plan policy with learned plan selection in a multi-tenant database service. Include correctness, privacy, poisoning resistance, resource economics, uncertainty, canary gates, and rollback.

## Answers to the Exercises

### Answer 1

The identity begins with the parsed and bound statement or a collision-resistant reference to it, not raw text alone. It records the database and the schema/search-path resolution that binds the unqualified table; timestamp parameter type, precision, time-zone semantics, nullability/coercions, and relevant collation; the tenant-policy identity/generation and authorization or a proof that the compiled skeleton is principal-independent; and relevant session/compatibility settings. Dependencies include table/type/column generations, the user-defined function's identity/version/volatility and execution context, index generation and access capability, policy and privilege generations, optimizer/statistics/model generations according to the repository's staleness policy, and generated-code/runtime ABI if used. Actual timestamp and tenant literals should not appear in a broadly readable key or trace. Snapshot and transaction state remain guarded executor inputs unless the plan explicitly requires a narrower contract. Reuse requires identity compatibility plus current dependency generations and runtime authorization.

### Answer 2

Small index cost is `20+10*.05=20.50`; large index cost is `20+50000*.05=2520`; every scan costs 1,000. Generic index total is `5+80*20.5+20*2520=52,045`, average 520.45. Generic scan total is `5+100*1000=100,005`, average 1,000.05. Custom total is `100*5+80*20.5+20*1000=22,140`, average 221.40. Dispatcher total is `20+100*.5+80*20.5+20*1000=21,710`, average 217.10. Solve `20+.05r=1000` to get crossover `r=19,600`. Reusing the index for a large value has regret `2520-1000=1520`. The finite arithmetic proves those values and ranking under the stated deterministic functions, workload counts, and overheads. It does not prove an engine's costs, cardinalities, classifier accuracy, semantic correctness, operational safety, or universal superiority of dispatching.

### Answer 3

Capture both execution orders in an isolated test while holding schema, statistics, configuration, data snapshot, parameter types, role/policy, concurrency, and resource class constant. Record cache identity, compile timestamp/value or class, generic/custom/variant status, planning time, estimates, actual rows, access/join algorithms, memory/spill, I/O, buffer reads/hits, locks/waits, and elapsed/CPU. Run each tenant under forced custom or explicit recompile and under a forced generic policy if safely supported; execute the alternative physical plans in the same environment. Warm data pages independently or alternate runs so buffer state is balanced, and never infer a plan-cache result from a whole-system cache clear. If first tenant controls the reused plan and forced-custom removes the reversal while rows and resources explain a plan crossover, parameter sensitivity is supported. If plan stays constant but physical reads change, suspect warmth; if estimates change after statistics refresh, suspect drift; if wait time dominates, diagnose locks/queues; if resource metrics vary, reproduce in a fixed class. Report scope and uncertainty rather than naming sniffing from elapsed time alone.

### Answer 4

Start with semantic classes for `include_archived` and null/invalid time boundaries. Within valid requests, derive joint features: tenant size/hotness, window width and recency, expected archived fraction, partition count, and confidence. A bounded design might keep: small-tenant/narrow-window index variant; large-tenant/narrow-recent partition-pruned index variant; broad-window or include-archived scan/parallel variant; plus a generic or custom-planning fallback for unknown, low-confidence, out-of-range, or unavailable-resource cases. Define exact half-open boundary ownership and total null behavior. Do not multiply independent tenant/window estimates when correlation evidence is absent. Cap variants per fingerprint and globally; require minimum samples and expected regret reduction before splitting; merge only after a longer contrary interval; apply hysteresis around width/row thresholds. Link dispatcher and variants to table, partition map, index, policy, statistics/model, and resource-class generations. Telemetry reports redacted class, confidence, selected/fallback plan, estimated/actual rows, compilation/dispatch/runtime, regret sample, memory/spill/I/O, tail latency, drift, eviction, and invalidation. Reclassify/shadow after tenant growth or partition/statistics changes and retain a safe fallback.

### Answer 5

Build a candidate corpus from authorized plans and representative, temporally separated parameter classes; split training, validation, shift, and adversarial sets by tenant and time so repeated values do not leak across evaluation. Differentially verify every candidate against the trusted query result under identical snapshot, policy, types, and transactional context. The selector consumes redacted, least-privilege features; raw tenant values and result-derived secrets are excluded or tightly controlled. Sign/version model, features, candidate set, dependency generations, and configuration. Bound exploration, per-tenant influence, variant count, compile CPU, memory, and query runtime; reject malformed/low-confidence features to a deterministic fallback. Test poisoned feedback, rare classes, missing features, distribution shift, schema/policy/statistics changes, concurrent publication, and invalidation storms.

Offline evaluation reports class coverage, top-plan accuracy only as a secondary metric, realized regret against executed eligible candidates, regressions, uncertainty calibration, compile/dispatch/runtime, memory, spill/I/O, throughput, fairness across authorized tenant cohorts, and tails. Shadow first, logging selected versus actual without changing execution. Canary a bounded fingerprint and tenant/resource cohort against an unchanged control, with gates for result equivalence, authorization, p50/p95/p99, worst-class regret, errors, compilation CPU, cache memory/churn, spills, and fleet interference. A kill switch atomically returns to the previous eligible generic/dispatcher policy; immutable artifacts and dependency records make rollback reproducible. Promotion expands gradually and stops on uncertainty or drift. This evidence supports only the tested workloads, versions, environments, and threat model; it does not establish universal optimality, privacy, fairness, or external review.
