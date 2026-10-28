---
module_id: DARCH-045
program: Data Architecture Engineering
level: 1
module_number: 45
title: Semantic and Metrics Layers
status: complete
last_verified: 2026-09-03
---

# Semantic and Metrics Layers

## One-Page Review

### Governing question

How should an organization publish reusable business entities, dimensions, measures, metrics, join paths, policies, and time semantics so different tools produce compatible analytical answers without centralizing every contextual decision or hiding ambiguity behind a “single source of truth” label?

### Essential definitions

- A **semantic layer** is an executable, governed model of analytical entities, relationships, dimensions, measures, metrics, policies, and query behavior over one or more data products.
- A **metrics layer** is the portion of semantic architecture that defines, composes, versions, evaluates, and serves named measures and metrics.
- A **measure** is a quantity observed or derived at a declared grain before a particular analytical aggregation.
- A **metric** is a governed calculation over measures, dimensions, filters, populations, time, and comparison rules for a declared decision context.
- An **entity** is a stable analytical identity used to relate semantic models; it is not established merely by two columns sharing a name.
- A **join path** is an allowed sequence of relationships with declared keys, cardinalities, time behavior, and fan-out handling.
- A **semantic context** identifies the decision, population, grain, time, policy, and owner within which a term or metric is valid.
- **metric conformance** means definitions and results are compatible for named comparisons, dimensions, periods, and releases.
- **additivity** states across which dimensions a measure may be summed without changing meaning.
- A **time spine** is a governed calendar or sequence used to construct complete periods, cumulative windows, comparisons, and zero-activity observations.
- A **semantic query plan** is the compiled set of sources, joins, filters, aggregations, policies, and physical operations used to answer a semantic request.
- A **semantic release** binds model, metric, policy, source, and compiler versions to reproducible consumer behavior.

### Central model, mechanism, or theorem

Represent a metric contract as:

`K = (identity, purpose, owner, measures, population, grain, dimensions, time, filters, aggregation, units, nulls, corrections, policy, service, version, evidence)`

Represent the semantic graph as entities and model nodes connected by governed relationship edges. A compiler may traverse only approved paths whose keys, cardinality, time, and policy preserve the requested metric. Metric equality requires more than matching formulas: numerator and denominator populations, distinctness, filters, time, units, late-data policy, releases, and access context must also agree. When contexts legitimately differ, publish distinct related metrics rather than forcing false uniformity.

### Critical invariants

- Every semantic object has stable identity, owner, purpose, definition, effective version, lineage, consumers, and lifecycle.
- Metric names never substitute for population, grain, filters, time, units, aggregation, null, correction, and policy contracts.
- Join paths declare keys, cardinalities, fan-out risk, temporal alignment, and permitted traversal direction.
- Measures aggregate only across dimensions for which their algebra and units are valid.
- Ratios preserve numerator and denominator components; subgroup ratios are not averaged unless mathematically justified.
- Distinct counts, percentiles, medians, balances, cumulative metrics, and conversion funnels state mergeability and window behavior explicitly.
- Semantic compilation cannot grant access that underlying sources, purposes, or result policies forbid.
- Cache and materialization identities include semantic release, source releases, parameters, policy context, and time boundary.
- Definition changes are versioned, impact-assessed, validated, communicated, and restated where historical comparison requires it.
- Retirement removes definitions, aliases, APIs, generated queries, caches, extracts, credentials, docs, and consumer dependencies while preserving required evidence.

### Common failures

Common failures are calling a glossary or wiki an executable semantic layer; declaring one universal metric by name; defining formulas without population; using ambiguous `customer_id` joins; allowing cycles or multiple unranked paths; joining facts before aggregation; summing balances through time; averaging percentages; summing distinct counts; using local time without a zone or calendar; letting current dimensions rewrite historical results; embedding private filters in dashboards; treating compiler success as correctness; applying policy only after a broad query; caching across tenants; publishing “latest” definitions without versioning; silently correcting past metrics; centralizing all semantic work in one bottleneck team; allowing local definitions with no relationship to governed metrics; and deleting catalog entries while APIs, extracts, caches, or reports continue to use them.

### Compact example

Four sessions include three conversions, but one converted session is ineligible for a campaign experiment. “All-session conversion” is 3/4 or 75 percent; “eligible-session conversion” is 2/3 or 66.67 percent. Both formulas divide conversions by sessions, yet they answer different questions. A valid semantic layer publishes distinct metric identities with population filters, purpose, owner, time, dimensions, release, and limitations rather than choosing one result because its label sounds canonical.

### Connections

[DARCH-015](015-shared-vocabulary-and-business-glossaries.md), [DARCH-027](027-producer-and-consumer-contracts.md), [DARCH-041](041-enterprise-data-warehouse-architecture.md), and [DARCH-044](044-data-mart-strategies.md) establish language, contract, warehouse, and serving foundations. Data Engineering [DENG-019](../../19-data-engineering/modules/019-metric-definitions-and-semantic-consistency.md) owns implementation-level metric definition. This module defines enterprise semantic architecture and prepares [DARCH-046](../ROADMAP.md) on operational data stores.

## Governing Question

Organizations rarely suffer from a total absence of metric definitions. They suffer from definitions scattered across SQL, dashboards, notebooks, reports, APIs, spreadsheets, and conversations, each with different populations, clocks, filters, joins, policies, and correction behavior.

The governing question is not how to put formulas in one tool. It is how to make business meaning executable, governed, context-aware, interoperable, observable, and evolvable across analytical products and consumer interfaces.

## Why This Matters

The Kimball Group's guidance on [Additive, Semi-Additive, and Non-Additive Facts](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/additive-semi-additive-non-additive-fact/) and [Conformed Dimensions](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/conformed-dimension/) shows that analytical compatibility depends on algebra and shared dimensional meaning, not column names.

dbt Labs documents [Semantic Models](https://docs.getdbt.com/docs/build/semantic-models) and [Metrics](https://docs.getdbt.com/docs/build/metrics-overview) as executable entities, dimensions, measures, joins, and metric types. The W3C [RDF Data Cube Vocabulary](https://www.w3.org/TR/vocab-data-cube/) defines observations, dimensions, measures, attributes, structures, and integrity constraints. These sources illustrate mechanisms; architecture must govern their organizational meaning and limits.

OpenLineage's [Lineage Dataset Facet](https://openlineage.io/docs/spec/facets/dataset-facets/lineage/) provides machine-readable input and field transformation relationships. Google's [Addressing Cascading Failures](https://sre.google/sre-book/addressing-cascading-failures/) matters when semantic compilers and caches become shared runtime dependencies. NIST [SP 800-160 Volume 1 Revision 1](https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final) frames trustworthy lifecycle engineering. Semantic trust requires definition, execution, evidence, operation, and closure.

## Prerequisites and Retrieval

You should understand conceptual and logical models, entities, keys, facts, dimensions, measures, grain, joins, cardinality, time, history, data products, marts, APIs, lineage, policy, caching, quality, and lifecycle.

Retrieve glossary, ontology, logical model, semantic model, entity, dimension, measure, metric, aggregation, additivity, distinctness, ratio, cumulative, conversion, time spine, join path, cardinality, fan-out, compilation, pushdown, cache key, release, conformance, context, restatement, and deprecation.

As a retrieval test, inspect “monthly active customers.” Ask which customer identity, eligible population, qualifying activity, distinctness, calendar, zone, late data, deletion, dimensions, source releases, policy context, owner, version, and decision apply. The metric name alone answers none of these.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish glossaries, ontologies, logical models, semantic layers, metrics layers, marts, and presentation tools;
2. define entities, dimensions, measures, metrics, relationships, and contexts as governed executable contracts;
3. qualify join paths by keys, cardinality, fan-out, temporal behavior, and policy;
4. encode additive, semi-additive, non-additive, ratio, distinct, cumulative, conversion, and approximate metric behavior;
5. govern time spines, calendars, valid and system time, late data, corrections, and restatements;
6. compile semantic requests into safe source, join, filter, aggregation, and physical plans;
7. propagate purpose, authorization, minimization, derived sensitivity, result limits, and audit through semantic queries;
8. validate metric definitions and results across engines, APIs, caches, materializations, and consumer tools;
9. federate semantic ownership while maintaining discoverability, conformance, review, and change governance;
10. operate versioning, adoption, incidents, migration, deprecation, portability, and retirement.

## Core Exposition

**Start with decisions and questions.** Name the decision, actor, consequence, cadence, comparison, and dimensions a metric supports.

Do not begin with a dashboard tile. One number can support different decisions only when its semantic context remains compatible.

**Distinguish language artifacts.** A glossary defines terms in prose. An ontology formalizes concepts and relationships. A logical model structures information independently of implementation. A semantic layer compiles governed analytical behavior.

These artifacts should link to one another, not masquerade as interchangeable repositories.

**Define stable semantic identities.** Assign durable IDs to entities, dimensions, measures, metrics, relationships, calendars, policies, and releases.

Names and labels can change. Stable identities support lineage, dependency, compatibility, aliases, impact analysis, and retirement.

**Assign contextual authority.** Name the domain or function accountable for each source assertion, business rule, metric, policy, and consumer promise.

Finance may own recognized revenue; Growth may own experiment conversion; the platform owns compilation reliability. No tool owns meaning by installation.

**Model entities explicitly.** Define business identity, key mappings, grain, source authority, merges, splits, reuse, time, and unresolved members.

Two models exposing `customer_id` cannot join safely until identity equivalence is proven for the requested population and interval.

**Model dimensions as contracts.** State allowed values, hierarchy, ordering, unknown behavior, valid intervals, roll-ups, labels, localization, classification, and owner.

A dimension is not merely a selectable column. It defines how observations may be sliced, grouped, filtered, and compared.

**Model measures before metrics.** A measure has an observation grain, expression, unit, null behavior, source lineage, and permitted aggregations.

Metrics compose measures under populations, filters, time, and comparison. Separating them exposes algebra and reuse.

**Specify full metric contracts.** Record identity, name, purpose, owner, numerator and denominator, eligible population, grain, dimensions, filters, time, aggregation, units, nulls, corrections, policy, service, version, and evidence.

A formula such as `sum(revenue)` is incomplete without currency, recognition, status, tax, period, and source boundaries.

**Treat context as part of identity.** All-session and experiment-eligible conversion are related but distinct metrics.

Do not force one universal result where decision contexts differ. Publish relationships and translation rules so consumers choose knowingly.

**Govern the semantic graph.** Represent models and entities as nodes and allowed relationships as edges with keys, cardinality, direction, temporal rule, fan-out behavior, and policy.

Reject ambiguous paths unless precedence is explicit. Cycles require a deliberate resolution rule rather than whichever route a compiler finds first.

**Declare cardinality accurately.** One-to-one, many-to-one, one-to-many, and many-to-many relationships affect row preservation and aggregation.

Validate cardinality against released populations. A declared primary key that is not unique makes symmetric or fan-out-safe aggregation claims unreliable.

**Prevent fact-to-fact multiplication.** Aggregate facts independently to compatible dimensions before comparison, or use proven bridge and allocation semantics.

A semantic layer cannot repair a wrong join graph automatically. It can block unsafe paths when metadata and tests are correct.

**Classify additivity.** Additive measures sum across all supported dimensions. Semi-additive measures exclude some dimensions, often time. Non-additive measures require components or special algorithms.

Balances may sum across accounts but not dates. Prices and percentages usually should not be summed.

**Preserve ratio components.** Compute a ratio from aggregated numerator and denominator at the requested scope.

Do not average subgroup ratios unless weights and algebra justify it. Expose denominator and zero-denominator policy for interpretation.

**Govern distinct counts.** Exact distinct counts require identity and set union; partition-level counts cannot generally be summed.

Approximate sketches may be mergeable under specific algorithms and parameters. Label estimates, error behavior, seed or precision, and unsupported deletions.

**Govern percentiles and medians.** Subgroup medians do not combine into an overall median. Exact percentiles need the distribution or suitable ordered state.

Approximate summaries require documented algorithms, error, merge behavior, and versions. Do not expose approximate results as exact silently.

**Govern cumulative metrics.** Define accumulation start, reset, window, time grain, inclusion, late-data behavior, and partial-period treatment.

Year-to-date revenue depends on fiscal calendar and restatement policy. A running SQL window alone is not the contract.

**Govern conversion metrics.** Define eligible population, entry event, conversion event, entity, attribution, ordering, window, censoring, repeated events, and late outcomes.

All sessions and campaign-eligible sessions can produce different valid denominators. Publish the distinction.

**Use time spines deliberately.** A time spine provides complete calendar members for zero-activity periods, windows, and comparisons.

Define calendar, zone, granularity, holidays, fiscal periods, partial periods, and valid range. Joining the wrong spine fabricates or omits observations.

**Separate time concepts.** Distinguish business-effective, event, source transaction, observation, ingestion, release, query, and correction time.

Metrics must state which controls grouping, eligibility, freshness, and historical reconstruction.

**Model historical dimensions.** Decide whether metrics group by dimension values at event time, current time, release time, or another explicit point.

Current hierarchy can legitimately answer current portfolio questions while as-of hierarchy answers historical accountability. They need distinct semantics.

**Define late-data and correction behavior.** State lateness horizon, finality, provisional results, materiality, restatement, notification, and affected consumers.

A metric release can be internally consistent and later superseded. Preserve version and explanation.

**Compile from semantic intent.** A request names metric IDs, dimensions, filters, time range, comparison, release, and access context.

The compiler selects sources, paths, predicates, aggregations, joins, materializations, and physical execution. Emit an explainable plan.

**Validate compilation before execution.** Check allowed dimensions, filters, grain, cardinality, join ambiguity, policy, cost bounds, source availability, release compatibility, and engine capabilities.

Fail closed when meaning or access is ambiguous. A syntactically valid query can be semantically unsafe.

**Push down without changing meaning.** Engines may filter, aggregate, or join beneath the semantic service for efficiency.

Verify null, decimal, time, collation, distinctness, approximate function, and authorization behavior across targets. Equivalent SQL text is not the goal; equivalent contract results are.

**Use materializations as physical aids.** Precomputed metric marts, aggregates, cubes, caches, and indexes can accelerate stable workloads.

They must share semantic identity, release, refresh, correction, policy, lineage, and invalidation. Do not fork definitions into each acceleration path.

**Build complete cache keys.** Include semantic release, source release vector, metric and dimension IDs, filters, time range, comparison, parameters, locale, principal or policy context, and result-shaping options.

Caching across tenants or policy versions can leak data. Time-to-live does not repair an incomplete key.

**Apply policy before and during compilation.** Authorize semantic objects, dimensions, filters, rows, fields, derived results, and requested precision for the declared purpose.

Underlying storage remains protected. The semantic layer cannot be the only control when direct engine or object access exists.

**Limit inference through results.** Counts, small groups, repeated queries, differencing, rankings, metadata, errors, and timing can reveal protected facts.

Use minimum groups, suppression, query budgets, differential privacy where appropriate, result review, and auditing based on threat and purpose—not as universal defaults.

**Propagate derived sensitivity.** A metric or segment can be more sensitive than its visible columns.

Classify definitions, intermediate results, caches, exports, and lineage. Restrict explanations that reveal hidden filters or source identities.

**Audit semantic requests and outcomes.** Record principal, purpose, semantic release, objects, parameters, policy decision, compiled plan identity, source releases, result classification, cost, and outcome status.

Avoid logging raw sensitive filters or results unnecessarily. Preserve evidence required for incident and reproducibility.

**Test definitions with fixtures.** Cover ordinary, empty, null, duplicate, late, corrected, zero-denominator, boundary-time, hierarchy-change, and unauthorized cases.

Fixtures prove local logic only. Also reconcile production releases and validate consumer decisions.

**Use algebraic property tests.** Check valid additivity, invariance under safe partitioning, component recomposition, monotonicity where required, and deliberate non-mergeability.

Counterexamples are valuable. A test should fail when someone sums daily balances or averages ratios.

**Run cross-engine conformance tests.** Evaluate the same pinned semantic and source releases through every supported compiler and engine path.

Compare types, rows, values, nulls, time, dimensions, policies, plans, and errors. Version certification by complete stack.

**Reconcile semantic and materialized results.** Compare generated live queries with metric marts and caches at compatible releases and policies.

Use keys, dimensions, components, totals, distributions, and missing populations. Matching grand totals can hide grouped defects.

**Publish lineage at semantic granularity.** Connect metric to measures, fields, sources, relationships, filters, transformations, policies, materializations, and downstream consumers.

Runtime lineage shows which path actually executed. Declared lineage alone may miss compiler choices.

**Expose contracts through multiple interfaces.** BI tools, SQL generation, APIs, notebooks, spreadsheets, and applications can consume the same semantic identities.

Each interface must preserve types, versions, access, pagination or result limits, release, errors, and deprecation. Display labels can differ without forking meaning.

**Design metric APIs carefully.** Accept stable metric and dimension IDs, bounded filters, time ranges, release selectors, and idempotent export requests.

Do not expose arbitrary SQL as a semantic API. Return definition version, source freshness, quality, units, warnings, and lineage links with results.

**Federate semantic ownership.** Domains own source meaning; cross-domain councils or accountable functions own shared conformance; platform teams own languages, compilers, registries, controls, and support.

Local teams can publish contextual metrics through contracts. Federation is not absence of review or global central editing.

**Define contribution gates.** Require stable identity, owner, purpose, contract completeness, sources, joins, tests, policy, documentation, service, lineage, and lifecycle.

Automate safe checks and reserve human review for semantic conflict, high consequence, protection, and cross-domain decisions.

**Manage aliases and discovery.** Search can map familiar labels to canonical or contextual objects, but results must show owner, purpose, version, certification, and differences.

An alias cannot make two incompatible metrics equivalent. Deprecate ambiguous labels.

**Version semantic changes.** Classify changes to labels, documentation, formulas, populations, dimensions, sources, calendars, policy, precision, or service.

Compatibility depends on consumers and decision context. A seemingly small filter change can rewrite history.

**Use effective intervals.** Record when a definition is valid for new queries and whether historical periods are recomputed under old or new semantics.

Separate definition-effective time from deployment time and data-effective time. Preserve reproducible prior releases.

**Impact-assess change.** Traverse metrics, models, joins, materializations, caches, APIs, dashboards, extracts, alerts, models, reports, and decisions.

Unknown consumers require observation and communication before removal. Dependency graphs need runtime reconciliation.

**Support dual evaluation safely.** Run old and new definitions on pinned populations, compare results by dimension and period, explain differences, and validate decisions.

Name which version is authoritative for each cohort and bound coexistence. Do not publish two unqualified “revenue” metrics.

**Operate semantic service objectives.** Measure registry availability, compile latency, query latency, freshness, plan failures, policy denials, cache correctness, reconciliation, and consumer success.

Separate semantic control-plane health from downstream engine and source fitness.

**Protect the service from overload.** Bound query dimensions, ranges, cardinality, fan-out, concurrency, scans, exports, and retries.

Use estimates, admission control, quotas, asynchronous jobs, backpressure, cancellation, and load shedding. One expensive semantic request can amplify across sources.

**Observe cost by semantic object.** Attribute compilation, engine work, storage scans, materialization, cache, egress, and support to metrics and consumers.

Cost informs physical optimization and deprecation. It does not override correctness or access constraints.

**Measure adoption carefully.** Query counts, dashboards, and users show activity, not decision value or semantic correctness.

Track governed reuse, conflicting definition reduction, time to answer, incidents, correction time, consumer trust, and retired duplicate logic.

**Plan portability.** Export semantic identities, models, expressions, graphs, tests, lineage, policies, releases, and consumer mappings in documented forms.

Compiler languages and engine functions differ. Test representative definitions on an alternate stack rather than assuming metadata export is executable.

**Migrate incrementally.** Inventory definitions across code, dashboards, reports, APIs, notebooks, and spreadsheets. Group by decision, meaning, consumer, and evidence.

Publish governed metrics, validate pinned results, migrate cohorts, monitor legacy use, and keep rollback and correction explicit.

**Retire definitions completely.** Stop new use, remove aliases and discovery, migrate consumers, invalidate caches and materializations, revoke APIs and credentials, remove generated code and docs, and preserve required evidence.

Verify absence of calls and scheduled extracts. A hidden formula can outlive its catalog entry.

**Measure semantic value.** Track compatible decisions, reuse, safe self-service, compile and query service, definition defects, restatement impact, protection incidents, cost, and retirement.

A semantic layer earns authority through transparent contracts and evidence, not through the ambition to own every number.

## Definitions and Notation

Represent semantic architecture as $S=(E,D,M,K,J,T,P,C,L,O,V)$, where $E$ is entities, $D$ dimensions, $M$ measures, $K$ metrics, $J$ governed join paths, $T$ time, $P$ policy, $C$ compilation and serving, $L$ lineage, $O$ ownership and operation, and $V$ versions and lifecycle.

For ratio metric $k$, define $k(X)=N(X)/D(X)$ for eligible population $X$ when denominator policy permits. In general, the mean of subgroup ratios is not $(\sum_i N_i)/(\sum_i D_i)$; preserve components and aggregate them before division.

For semantic request $q$, let `Plan(q,s,p,r)` be compilation under semantic release $s$, policy context $p$, and source release vector $r$. Cache equivalence requires all result-affecting inputs and authorization context to agree.

Define `FitSemantic(S,k,t)` as a review predicate requiring owned purpose, complete metric and graph contracts, valid algebra and time, safe joins, effective protection, reproducible compilation, conformance evidence, supported service, versioned change, portability, consumer validation, and bounded lifecycle at time $t$.

## Mechanisms, Invariants, or Proof Structure

Use ten gates for every consequential semantic object and metric.

**1. Purpose gate.** Name decision, consumers, consequence, context, owner, scope, value, and exclusions.

**2. Entity gate.** Define identities, keys, grain, mappings, relationships, cardinality, time, fan-out, and path precedence.

**3. Metric gate.** Define measures, populations, filters, dimensions, aggregation, units, nulls, distinctness, components, windows, and limitations.

**4. Time gate.** Define calendars, zones, event and valid time, releases, late data, correction, restatement, and history.

**5. Compilation gate.** Validate requested objects, paths, grain, policy, cost, sources, engines, pushdown, plans, errors, and explainability.

**6. Protection gate.** Apply purpose, minimization, row and field access, derived sensitivity, inference controls, cache context, egress, and audit.

**7. Evidence gate.** Test fixtures, algebra, cross-engine results, releases, materializations, quality, lineage, and consumer decisions.

**8. Ownership gate.** Assign domains, shared conformance, platform, protection, operations, consumers, incidents, disputes, and support.

**9. Change gate.** Version definitions, assess impacts, dual-evaluate, communicate, migrate cohorts, deprecate aliases, and bound coexistence.

**10. Lifecycle gate.** Record adoption, service, cost, portability, review triggers, consumer closure, evidence retention, and verified retirement.

The executable example compares two fully named conversion populations that share a formula but not a decision context.

<!-- bijux-verify: {"id":"semantic-metric-population-contract","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"all_sessions=4\neligible_sessions=3\nall_conversions=3\neligible_conversions=2\nall_conversion_rate=0.7500\neligible_conversion_rate=0.6667\ndifference_percentage_points=8.33\n","stderr":""}} -->
```python
from decimal import Decimal, ROUND_HALF_UP

sessions = [
    {"id": "S1", "eligible": True, "converted": True},
    {"id": "S2", "eligible": False, "converted": True},
    {"id": "S3", "eligible": True, "converted": False},
    {"id": "S4", "eligible": True, "converted": True},
]

all_sessions = len(sessions)
eligible = [session for session in sessions if session["eligible"]]
all_conversions = sum(session["converted"] for session in sessions)
eligible_conversions = sum(session["converted"] for session in eligible)

all_rate = Decimal(all_conversions) / Decimal(all_sessions)
eligible_rate = Decimal(eligible_conversions) / Decimal(len(eligible))
difference_pp = (all_rate - eligible_rate) * Decimal(100)

print(f"all_sessions={all_sessions}")
print(f"eligible_sessions={len(eligible)}")
print(f"all_conversions={all_conversions}")
print(f"eligible_conversions={eligible_conversions}")
print(f"all_conversion_rate={all_rate.quantize(Decimal('0.0001'))}")
print(f"eligible_conversion_rate={eligible_rate.quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP)}")
print(f"difference_percentage_points={difference_pp.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)}")
```

The result proves only the arithmetic of two declared in-memory populations. It does not establish which metric is appropriate, whether sessions or conversions are valid, how identities, attribution, time, censoring, late data, policy, source releases, or consumer decisions should be governed.

## Alternatives and Trade-Offs

**Central versus federated semantic ownership.** Central ownership can improve consistency but bottleneck domain change. Federation preserves expertise while requiring contribution contracts and cross-domain governance.

**One universal metric versus contextual metrics.** One metric simplifies communication when meaning truly agrees. Contextual variants preserve legitimate differences but need clear names, relationships, and discovery.

**Semantic layer versus governed metric marts.** Runtime compilation supports flexible dimensions. Metric marts provide predictable service. Shared contracts can generate and reconcile both.

**Logical versus materialized evaluation.** Logical evaluation sees current pinned sources and avoids copies. Materialization controls latency and load but adds freshness, invalidation, correction, and policy duties.

**Tool-native versus tool-neutral model.** Native models exploit features and integration. Neutral identities and contracts improve portability. Adapters still need conformance tests.

**Compile-time versus runtime policy.** Compile-time checks block invalid plans early. Runtime enforcement handles underlying data and dynamic context. Consequential systems need aligned layers.

**Exact versus approximate metrics.** Exact evaluation supports strict reconciliation at higher cost. Approximation can serve exploration or scale when error and limitations are explicit.

**Current-definition versus as-published history.** Recomputing supports present comparability. Preserving prior releases supports audit and decision reconstruction. Offer both when justified and label them.

**Flexible graph traversal versus approved paths.** Automatic traversal increases convenience but risks ambiguity and fan-out. Approved paths improve safety at modeling cost.

**Strict standardization versus local extension.** Standards reduce duplication. Governed extensions support contextual decisions. Require ownership, compatibility, and lifecycle rather than prohibiting all variation.

## Failure Modes and Misconceptions

1. **A glossary is a semantic layer.** Prose does not compile or enforce analytical behavior.
2. **A formula defines a metric.** Population, grain, time, filters, policy, and versions remain.
3. **One name should have one universal result.** Legitimate decision contexts can differ.
4. **Matching key names permit a join.** Identity, cardinality, population, and time must align.
5. **A semantic compiler prevents fan-out automatically.** Its relationship metadata must be true.
6. **All numeric measures can be summed.** Balances, ratios, prices, and distinct counts require specific algebra.
7. **Subgroup percentages can be averaged.** Numerator and denominator weights matter.
8. **Time travel preserves metric history.** Definitions, policies, sources, and business-valid time also matter.
9. **Current dimensions are correct for every historical question.** As-of and current contexts differ.
10. **Compiler success proves correctness.** Semantic, source, policy, and consumer evidence remain.
11. **Caching is transparent.** Incomplete keys can return stale or unauthorized results.
12. **The semantic layer can replace source security.** Alternate access paths remain.
13. **Central ownership guarantees consistency.** It can create queues and uninformed definitions.
14. **Federation means every team defines anything.** Shared contracts and conflict governance remain.
15. **Versioning only formulas is enough.** Populations, joins, calendars, sources, and policies change behavior.
16. **Usage proves value.** Widely used metrics can be wrong or harmful.
17. **Deleting a metric entry retires it.** APIs, queries, caches, extracts, and reports can persist.

## Worked Examples

### Example 1

Finance publishes recognized revenue with currency, recognition event, exclusions, fiscal period, owner, and restatement policy. A dashboard consumes the stable metric ID rather than duplicating SQL. **Conclusion:** reuse begins with a complete contract.

### Example 2

All-session conversion is 75 percent while experiment-eligible conversion is 66.67 percent on the same four rows. Both are published with distinct purposes. **Conclusion:** population is part of metric identity.

### Example 3

A semantic graph offers two Customer-to-Order paths, one through account ownership and one through billing identity. Compilation fails until the request selects its context. **Conclusion:** ambiguity should be exposed, not resolved accidentally.

### Example 4

Daily balances average 120, 140, and 130. Summing them to 390 is rejected; month-end balance selects the final observation while average balance uses a declared time-weighting method. **Conclusion:** semi-additivity belongs in metadata.

### Example 5

Regional conversion rates of 90 percent for 10 sessions and 50 percent for 1,000 sessions are not averaged equally. Aggregated conversions divided by aggregated eligible sessions produces the enterprise result. **Conclusion:** ratios preserve components.

### Example 6

A current Product hierarchy moves an item to a new category. Historical-as-published and current-portfolio reports intentionally differ and cite separate semantic releases. **Conclusion:** time context prevents false inconsistency.

### Example 7

A cache key omits tenant and policy version, returning one tenant's metric to another. The design adds full authorization context and retains underlying row controls. **Conclusion:** caching is part of the security model.

### Example 8

Two supported engines disagree on local timestamp conversion during a daylight-saving boundary. Cross-engine fixtures block certification until the model uses an instant, source zone, and explicit calendar. **Conclusion:** compilation portability requires result evidence.

### Example 9

A local churn definition gains enterprise consumers. Governance retains its domain context, relates it to inactivity and cancellation metrics, adds ownership and tests, and avoids renaming it to universal `churn`. **Conclusion:** promotion need not erase legitimate context.

### Example 10

After consumer migration, a deprecated metric is removed from search and APIs, caches and aggregates expire, scheduled extracts stop, aliases fail clearly, and call telemetry confirms closure. **Conclusion:** semantic retirement extends beyond metadata deletion.

## Cross-Program Connections

- **Data engineering:** facts, dimensions, transformations, tests, metric code, marts, lineage, freshness, and materialization implement semantic contracts.
- **Database engineering:** keys, joins, constraints, aggregates, views, query plans, transactions, temporal data, and caches shape compilation.
- **Distributed systems:** graph services, caching, consistency, clocks, retries, partial failure, replication, and convergence shape runtime semantics.
- **API and service engineering:** stable identities, schemas, versions, authorization, pagination, quotas, errors, idempotency, and deprecation govern access.
- **Platform engineering:** registries, compilers, paved paths, self-service, policy, observability, workload control, and support enable adoption.
- **Cybersecurity and privacy:** purpose, minimization, row and field policy, inference, derived sensitivity, caches, egress, and audit constrain results.
- **Economics and decision science:** measurement validity, denominators, uncertainty, causal context, cost attribution, and decision value shape metrics.
- **Systems engineering:** stakeholder needs, interfaces, configuration baselines, verification, assurance cases, change control, and closure structure trust.

## References

1. Kimball Group, *Additive, Semi-Additive, and Non-Additive Facts*. <https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/additive-semi-additive-non-additive-fact/>
2. Kimball Group, *Conformed Dimensions*. <https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/conformed-dimension/>
3. dbt Labs, *Semantic Models*. <https://docs.getdbt.com/docs/build/semantic-models>
4. dbt Labs, *Creating Metrics*. <https://docs.getdbt.com/docs/build/metrics-overview>
5. W3C, *The RDF Data Cube Vocabulary*, W3C Recommendation, 2014. <https://www.w3.org/TR/vocab-data-cube/>
6. OpenLineage, *Lineage Dataset Facet*. <https://openlineage.io/docs/spec/facets/dataset-facets/lineage/>
7. Beyer, B., Jones, C., Petoff, J., and Murphy, N. R., eds., *Site Reliability Engineering: Addressing Cascading Failures*, Google, 2016. <https://sre.google/sre-book/addressing-cascading-failures/>
8. NIST, *Systems Security Engineering: Considerations for a Multidisciplinary Approach in the Engineering of Trustworthy Secure Systems*, SP 800-160 Volume 1 Revision 1, 2022. <https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final>

## Exercises

### Exercise 1

Define complete contracts for recognized revenue, active customer, conversion rate, month-end balance, and 95th-percentile fulfillment time. Explain their algebra and context.

### Exercise 2

Design a semantic graph connecting Customer, Account, Order, Shipment, Payment, Product, and Region. Identify ambiguous paths, fan-out, time, and policy constraints.

### Exercise 3

Create a validation and certification strategy for one semantic release across two warehouses, a metric API, one materialized mart, and a BI cache.

### Exercise 4

Design federated semantic ownership and contribution governance that permits contextual domain metrics while resolving cross-domain conflicts.

### Exercise 5

Plan migration from hundreds of dashboard formulas to governed semantic objects with versioning, dual evaluation, consumer cohorts, rollback, and retirement.

## Answers to the Exercises

### Answer 1

Recognized revenue specifies eligible contracts and performance events, gross and adjustment measures, recognition and reversal rules, currency conversion source and instant, tax treatment, fiscal period, grain, dimensions, late entries, restatement, Finance owner, and release. It is additive only across compatible currencies and dimensions after conversion. Active customer defines stable customer identity, qualifying activity, lookback window, zone, exclusions, distinctness, late activity, and context; regional distinct counts cannot simply sum when customers span regions.

Conversion rate preserves eligible denominator and converted numerator with entry and outcome events, entity, attribution, ordering, window, censoring, repeated events, dimensions, zero-denominator behavior, and owner. Month-end balance selects an as-of observation under account, currency, calendar, lateness, and restatement rules; it is additive across compatible accounts but not dates. Fulfillment p95 defines order or shipment grain, start and end events, incomplete and canceled cases, time zone, precision, window, dimensions, exact or approximate algorithm, error, and non-mergeability of subgroup percentiles.

### Answer 2

Give every entity stable identity, source mappings, grain, valid interval, classification, and owner. Define Order-to-Customer through ordering identity, Account-to-Customer through ownership with time, Order-to-Shipment as one-to-many, Order-to-Payment potentially many-to-many through allocations, Order-to-Product through order lines, and address or operational Region as distinct contexts. Declare keys and tested cardinalities per release.

Block raw Order, Shipment, and Payment fact joins; aggregate each to compatible dimensions or use governed allocation bridges. Expose ambiguity between billing Customer, ordering Customer, account owner, shipping Region, and customer-home Region rather than selecting by shortest path. Apply as-of rules for ownership and product hierarchy. Propagate row and field policy across every path, prohibit paths that infer protected relationships, and validate fan-out, unknown identities, cycles, boundary times, duplicate bridge rows, and source-release compatibility.

### Answer 3

Pin semantic release, source release vector, compiler, policies, calendars, engine and connector versions, and materialization or cache identities. Build fixtures for ordinary, empty, null, duplicate, zero-denominator, late, corrected, boundary-time, historical-dimension, ambiguous-path, high-cardinality, and unauthorized requests. Include sums, balances, ratios, distinct counts, percentiles, cumulative, and conversion metrics.

Compile and run the same supported requests on both warehouses and through the API. Compare types, rows, keys, dimensions, components, values, rounding, time, errors, policies, and plans. Reconcile the materialized mart at an equivalent release and verify refresh, invalidation, and correction. Include full semantic and policy context in BI cache keys and test revocation. Benchmark normal, peak, expensive, cancellation, engine failure, retry, and recovery. Publish certification scope and limitations; recertify after any result-affecting version change.

### Answer 4

Domains own source assertions, local entities, dimensions, measures, and contextual metrics. Named enterprise functions own high-consequence shared metrics. A cross-domain governance body resolves identity, conformed dimensions, calendars, shared measures, conflicts, and aliases. The platform team owns schema, registry, compiler, policy hooks, tests, observability, APIs, migration tools, and support—not business meaning.

Contribution gates require stable identity, purpose, owner, complete metric context, sources, paths, algebra, time, protection, tests, lineage, service, version, consumers, and lifecycle. Automate structural, graph, policy, algebra, fixture, and compatibility checks. Escalate genuine semantic or risk disputes to accountable decision owners with evidence. Permit related contextual variants with honest names and mappings. Track adoption, incidents, stale ownership, overlap, and deprecation; provide a fast paved path so governance does not become central ticket work.

### Answer 5

Inventory formulas in dashboards, SQL, reports, notebooks, spreadsheets, APIs, alerts, models, extracts, and caches. Group by claimed metric, decision context, population, sources, grain, filters, dimensions, time, units, owner, consumers, and runtime use. Identify compatible definitions, legitimate variants, unknown consumers, and unsafe joins. Prioritize high-consequence and high-reuse metrics.

Publish governed entity, dimension, measure, and metric IDs with source releases, tests, lineage, policy, service, and version. Dual-evaluate old and new definitions on pinned populations; compare components and results by period and dimension; explain differences and validate decisions. Migrate consumer cohorts with named authority, dashboards and API adapters, telemetry, communication, and rollback. Bound aliases and coexistence. After acceptance, remove legacy formulas, generated SQL, caches, aggregates, extracts, APIs, credentials, and docs, preserve required evidence, and verify no scheduled or observed consumer remains.
