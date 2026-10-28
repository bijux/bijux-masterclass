---
module_id: DE-019
program: Data Engineering
level: 1
module_number: 19
title: Metric Definitions and Semantic Consistency
status: complete
last_verified: 2026-09-02
---

# Metric Definitions and Semantic Consistency

## One-Page Review

### Governing question

How can an organization define a business metric once so that its population, grain, time, aggregation, dimensions, units, revisions and access rules produce the same meaning across SQL, dashboards, APIs, experiments and machine-learning features?

### Essential definitions

- A **measure** is a typed observed or derived quantity at a declared base grain, such as order revenue or active seconds.
- A **metric** is a governed business calculation over measures, entities and dimensions under population, time and aggregation rules.
- A **dimension** is a governed attribute used to group, filter or contextualize metric observations.
- An **entity** is the identified object at which measures or dimensions attach and through which semantic joins are permitted.
- A **metric grain** is the complete dimensional coordinate that identifies one published observation.
- An **eligibility predicate** defines the population allowed into the calculation; it is part of the metric, not a dashboard afterthought.
- A **semantic layer** stores reusable entities, dimensions, measures, metrics and join paths, then compiles governed queries for consumers.
- An **additive component** can be summed across declared dimensions. A **semi-additive** measure aggregates only along some dimensions. A **non-additive** metric such as a rate or distinct count needs components or special merge state.
- A **metric version** is an immutable interpretation contract. A breaking change to population, time, units or formula creates a new version or an explicit restatement.
- **Semantic consistency** means equivalent requests over the same governed snapshot and contract yield equivalent values and metadata across implementations.

### Central model, mechanism, or theorem

Represent a metric contract as

$$
M=(N,O,G,E,\Phi,A,T,W,D,U,V,Q),
$$

where $N$ is stable name, $O$ owner, $G$ base/published grain, $E$ entities, $\Phi$ eligibility/filter predicate, $A$ aggregation expression, $T$ governed time axis/calendar, $W$ window, $D$ allowed dimensions, $U$ unit, $V$ version and $Q$ quality/freshness policy.

For partition $j$ with numerator $x_j$, eligible denominator $n_j>0$ and rate $r_j=x_j/n_j$, the valid rollup is

$$
r=\frac{\sum_jx_j}{\sum_jn_j}=\sum_j\frac{n_j}{\sum_kn_k}r_j.
$$

Thus a global rate is a denominator-weighted mean of partition rates, not generally their arithmetic mean. Publish additive numerator and denominator components so regrouping preserves meaning.

### Critical invariants

- Every metric has one stable name, accountable owner, plain-language decision purpose and version.
- Source row grain, metric entity, published dimensions and allowed join paths are explicit.
- Eligibility, exclusions, numerator and denominator are independently inspectable.
- Event/as-of time, timezone, calendar, window boundaries and late-data closure are declared.
- Units, currency, scaling, rounding, null, zero, missing and divide-by-zero semantics are governed.
- Additive components reconcile at detail and rollups; rates are recomputed after aggregation.
- Distinct and approximate metrics declare identity scope, merge behavior and error semantics.
- Current-state versus event-time dimensions have different names.
- All implementations consume the same contract version and compatible data snapshot.
- Metric output carries contract version, source watermark, publication status and lineage.

### Common failures

Naming a SQL expression without defining population; counting rows instead of entities; averaging daily conversion rates; summing account balances through time; joining a one-to-many dimension and multiplying revenue; using current customer segment for historical reports without labeling it; mixing UTC and local business days; comparing incomplete current periods with complete prior periods; coalescing unknown to zero; converting currencies after aggregation with the wrong rate; calling approximate distinct exact; changing a filter under the same metric name; copying formulas into dashboard tools; serving stale cached values without watermark; and giving every team ownership of “revenue.”

### Compact example

Day 1 has one conversion among two eligible entities, a rate of 0.5. Day 2 has eight among ten, a rate of 0.8. The arithmetic mean is 0.65, but the two-day metric is $(1+8)/(2+10)=0.75$. Retaining `converted=9` and `eligible=12` lets any consumer regroup correctly; retaining only the two daily percentages loses denominator weight.

### Connections

[DE-011](011-grain-and-the-meaning-of-a-row.md) defines row meaning, [DE-012](012-facts-dimensions-and-measures.md) defines measure additivity, [DE-016](016-event-and-activity-models.md) defines behavioral populations, and [DE-017](017-wide-tables-and-denormalized-models.md) explains fanout. Planned DE-020 validates analytical models against business questions and appears in the [Data Engineering roadmap](../ROADMAP.md). Metric APIs connect to [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md), metric reliability to [Systems Engineering](../../26-systems-engineering/ROADMAP.md), and semantic infrastructure to [Platform Engineering](../../29-platform-engineering/ROADMAP.md).

## Governing Question

Can a decision-maker ask “what exactly is this number?” and receive one executable answer that identifies counted entities, eligible population, time boundary, dimensions, units, source freshness, revisions and owner—regardless of which tool displayed it?

Organizations rarely lack formulas. They lack contracts around formulas. Two teams can both calculate `SUM(revenue)` and disagree because one includes tax, the other converts currency differently, one uses order time, the other settlement time, and one filters refunds. A shared display name does not establish shared meaning.

A semantic system makes the contract executable. dbt's current [semantic-model documentation](https://docs.getdbt.com/docs/build/semantic-models) organizes models around entities, dimensions, a default aggregation time dimension and simple metric aggregations. Its [metric documentation](https://docs.getdbt.com/docs/build/metrics-overview) distinguishes simple, ratio, cumulative, derived and conversion metric dependencies. These are useful implementation patterns, but semantic consistency remains an organizational property: owners must agree on the business definition and validate every delivery surface.

The goal is not a giant catalog of numbers. It is a small, trustworthy vocabulary whose components compose safely, whose breaking changes are visible, and whose outputs state enough context to be interpreted correctly.

## Why This Matters

Metrics drive resource allocation, product changes, incident response, compensation, experiments and regulatory reporting. A plausible inconsistent number can cause more harm than a visibly missing one because it enters decisions without challenge.

Reusing metric logic reduces formula drift, but centralization alone is insufficient. If the shared metric joins through a fanout, uses a mutable dimension unexpectedly or hides an incomplete period, every consumer gets the same wrong answer. Semantic code needs data-grain, temporal and quality validation.

Metrics are also algebraic objects. Revenue sums can often be rolled up; daily balances cannot be summed across dates; ratios need their components; distinct counts need sets or mergeable sketches; medians generally cannot be recovered from subgroup medians. A semantic layer must know these behaviors to answer new dimensional requests safely.

Operational state affects meaning. A number can be correctly computed over incomplete inputs and still be unsuitable for a decision. Freshness, late-data status, approximation and revision policy are part of the result.

Finally, metric governance is a product discipline. Definitions need owners, consumers, tests, versions, deprecation and incident handling. A wiki paragraph detached from executable lineage will drift.

## Prerequisites and Retrieval

Retrieve the business decision and stakeholder; metric names/aliases; accountable owner and technical steward; numerator, denominator and eligibility language; entity identity and deduplication rules; source grains and keys; event/state/snapshot semantics; authoritative systems; units and currencies; tax/refund/discount treatment; time roles; timezone and fiscal/business calendar; window boundaries; partial-period behavior; cohort anchor; late-arrival distribution; restatement/finality policy; dimension definitions; current versus as-of needs; Type 2 history; join cardinalities; many-to-many allocation; null/zero/missing semantics; aggregation type; distinct-count scope; approximation algorithm/error; rounding/format; privacy classification; suppression/minimum-group rules; row/column access; lineage; source watermarks; publication cadence; service-level objective; caching; semantic-tool capabilities; SQL/dashboard/API/ML consumers; existing duplicate definitions; baseline historical series; acceptance examples; change approval; versioning; compatibility window; and incident/rollback owners.

Distinguish measure from metric; business definition from display label; base grain from output grain; entity from row; eligibility from activity; filter from dimension selection; numerator from denominator; additive component from derived ratio; simple average from weighted average; stock from flow; exact distinct from estimate; event time from ingestion/publication time; current period from complete period; current dimension from event-time dimension; currency amount from currency-converted amount; null from zero, suppressed and not applicable; missing source data from genuine no activity; provisional from final; correction from definition change; restatement from version comparison; implementation lineage from conceptual ownership; semantic consistency from coincidental equal totals; and metric SLO from business target.

Before implementation, create golden examples that include no eligible entities, eligible nonparticipants, duplicate events, refund/reversal, multiple currencies, exact boundary timestamps, daylight-saving transitions, late outcomes, identity merge/split, missing dimension, Type 2 change, one-to-many join, null amount, negative measure, partial current period, privacy-suppressed small group and approximate distinct. Hand-compute expected components and metadata, not only displayed rates.

## Learning Objectives

After completing this module, you should be able to:

1. express a metric as a complete executable contract;
2. distinguish entities, dimensions, measures, metrics and observations;
3. define eligibility, numerator, denominator, identity and time explicitly;
4. classify additive, semi-additive, non-additive and approximate calculations;
5. roll up ratios and averages from sufficient components;
6. prevent join fanout and temporal-dimension drift;
7. align units, currency, nulls, freshness and revisions;
8. implement reusable semantic definitions across delivery surfaces;
9. validate and observe cross-implementation consistency; and
10. version, deprecate and govern metrics as products.

## Core Exposition

### Begin with the decision

Ask which decision the metric informs, who makes it, at what cadence and what mistake is costly. “Activation rate” is ambiguous; “share of eligible new workspaces that connect a source and complete one successful job within seven days of creation” is testable.

Write the definition in plain language before SQL. Include counterexamples and exclusions. A stakeholder should be able to challenge population or time without reading code.

Avoid vanity metrics whose movement has no clear interpretation or action.

### Assign one accountable owner

One domain owner approves business meaning; a technical steward can operate its data implementation. Multiple contributors are healthy, but shared accountability without a decision mechanism produces forks.

Record support channel, review cadence and escalation. Ownership should survive team reorganizations through a durable domain role, not only a person's name.

Consumers own how they use a valid metric; the metric owner owns what it means.

### Choose a stable metric name

Names should describe the phenomenon and distinguish important variants: `net_recognized_revenue`, `weekly_active_accounts`, `trial_to_paid_conversion_30d`.

Do not encode every filter in a long name, but never reuse one name for incompatible populations or time windows. Maintain aliases and glossary links for common business language.

A display label may be friendly; the programmatic identifier should be durable and unique.

### Separate measures from metrics

A measure is a building block at base grain: quantity, amount, duration, one-per-event indicator. It has type, unit and aggregation behavior.

A metric combines measures and rules: net revenue, conversion rate, average resolution time. Several metrics can reuse one measure with different eligibility or time windows.

Do not hide business filters inside a column named `amount`.

### Identify the metric entity

State what is counted: people, accounts, devices, orders, tickets, sessions or events. The entity key needs tenant/scope, deduplication and merge/split rules.

`COUNT(*)` counts rows, not necessarily business entities. One account can have many events and one person can have multiple accounts.

If a metric changes entity between stages, such as visitor-to-account conversion, define the identity mapping and unmatched behavior.

### Declare base and output grain

The base grain identifies each input measure observation. The requested output grain combines selected dimensions and time bucket.

The W3C [RDF Data Cube vocabulary](https://www.w3.org/TR/vocab-data-cube/) distinguishes dimensions that identify observations, measures that represent observed phenomena and attributes such as unit or status that qualify interpretation. That separation is useful beyond RDF.

Require uniqueness at the complete published coordinate plus metric version/snapshot identity.

### Define eligibility independently

Eligibility describes who could meaningfully contribute, not who generated an event. An onboarding denominator may be all qualifying new accounts, including those that never acted.

Build eligibility from an authoritative population table or explicit event, with anchor time and exclusions. Activity-only sources cannot reveal silent eligible entities.

Publish eligible count as a component and monitor eligibility drift.

### Define numerator and denominator

For a proportion, specify entity uniqueness, qualifying condition, order/window and whether numerator must be a subset of denominator.

Use separate inspectable relations/components before division. Validate $0\leq x\leq n$ for subset counts.

When $n=0$, return null/undefined or a governed not-applicable status—not a fabricated zero rate.

### Define aggregation algebra

Sums of compatible flows and counts are often additive. Balances are usually semi-additive over time. Ratios, medians, percentiles and distinct counts are non-additive.

Record allowed rollup dimensions and sufficient merge state. A mean needs sum and count; variance needs more state; a quantile generally needs raw/distribution/sketch information.

Refuse unsupported regrouping rather than returning plausible nonsense.

### Recompute rates after aggregation

Store or expose numerator and denominator at each materialized grain. When grouping days into a month, sum both and divide once.

An arithmetic mean of subgroup rates gives equal weight to subgroups regardless of exposure. It is valid only when that equal weighting is the intended estimand or denominators are equal.

Label macro-average versus micro/pooled rate explicitly when both are useful.

### Handle averages with sufficient statistics

Average order value is total eligible order value divided by eligible order count. Average of store averages is generally wrong when stores have different counts.

Null-valued measures need a denominator policy: count non-null values, all eligible rows, or impute under a documented rule. SQL defaults are not the business definition.

Retain sum, count and any weights needed for rollup.

### Govern distinct counts

Define the entity key, scope and time window. Daily distinct users cannot be summed to monthly distinct users because the same user can appear on many days.

Exact rollup needs underlying identities or set-equivalent state. Mergeable sketches can estimate unions but introduce algorithm/version/error metadata.

Google BigQuery's current [approximate aggregate documentation](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/approximate_aggregate_functions) explicitly distinguishes estimates such as approximate distinct counts from exact aggregation and notes the performance/accuracy trade.

### Govern quantiles and distributions

The median of daily medians is not the monthly median. Percentiles require the combined distribution or a mergeable sketch designed for the operation.

Declare exact versus approximate, interpolation convention, sketch parameters, error bounds/validation and merge compatibility.

Keep histogram bucket boundaries/version stable if histograms are aggregated.

### Separate stock and flow metrics

Revenue during a month is a flow and may sum across days. Closing inventory is a stock at a cutoff and should use last-valid/as-of logic, not daily summation.

Average balance is an exposure measure with a defined day/duration denominator. Its unit differs from closing balance.

Semantic metadata should block invalid time aggregation for semi-additive measures.

### Define time role and clock

Choose the business timestamp: order accepted, service delivered, invoice issued, cash settled or snapshot cutoff. Each answers a different question.

Specify timezone, calendar, bucket boundaries, timestamp precision and inclusion at exact boundaries. Partition/load date is not automatically metric time.

Expose alternate time roles as distinct dimensions, not a generic date.

### Define windows and anchors

Rolling seven days, calendar week, week-to-date and prior seven complete days are different. State open/closed boundaries and whether the anchor event is included.

Conversion windows attach to entity/anchor: outcome occurs after qualifying start and within $W$. Repeated starts need first, latest or episode rules.

Use half-open intervals where practical to avoid double inclusion at adjacent boundaries.

### Handle partial periods

A current-day/month metric may be provisional and incomparable with a complete prior period. Return completeness status, elapsed fraction and latest source watermark.

Period-over-period comparison should align complete periods or explicitly compare like-for-like elapsed windows.

Do not fill future intervals with zero and then claim performance declined.

### Choose current or as-of dimensions

Historical revenue by customer segment can use segment at transaction time or the customer's current segment. Both are legitimate but not interchangeable.

Name the temporal interpretation and resolve Type 2 intervals deterministically. Current dimensions may cause history to reclassify after changes.

Metric version plus dimension version/snapshot is needed for reproduction.

### Control semantic joins

Declare entities and relationship cardinalities. A metric at order grain joined to order items can fan out order measures.

Google Looker's [symmetric-aggregate guidance](https://docs.cloud.google.com/looker/docs/best-practices/understanding-symmetric-aggregates) demonstrates why a unique primary key is necessary to count a fact once across fanout joins. Tool protection complements, but does not replace, correct grain modeling.

Validate allowed dimension paths and block ambiguous loops or many-to-many paths without allocation.

### Treat dimensions as contracts

Define code values, unknown members, hierarchy, temporal behavior, privacy classification and owner. `region` might mean billing, shipping, sales territory or current residence.

Conformed dimensions should produce compatible values across metrics. If two domains require distinct meanings, use distinct names rather than forced unification.

Monitor unmapped/other rates and hierarchy reconciliation.

### Preserve units through algebra

Every measure has a unit: orders, people, seconds, bytes, currency, percentage points. Addition requires compatible units; division produces a derived unit.

`revenue/orders` yields currency per order. A proportion is dimensionless but can be displayed as fraction or percent; percentage-point change differs from percent change.

Include scale and display formatting separately from stored value.

### Handle currency and conversion

Keep original amount/currency and define target currency, rate source, rate type and effective timestamp. Convert at transaction grain before additive aggregation when rates vary by transaction/date.

Do not add USD and EUR as if they share a unit. Do not average exchange rates independently of amount weights.

Restated rates or accounting close rules may require metric versions or publication snapshots.

### Define null, zero and missing

Zero is an observed quantity. Null may mean unknown, not applicable, suppressed or absent. Missing rows require population/coverage evidence before interpretation.

`COALESCE(value,0)` changes meaning and denominators. Use it only when the source contract proves missing/null equals zero for that measure.

Output status fields can distinguish provisional, estimated, suppressed and not applicable from ordinary values.

### Define rounding and precision

Calculate with sufficient precision, aggregate components, then round for presentation. Rounding row-level currency before summing may be required by accounting policy or may introduce drift; document the chosen rule.

Rates stored as binary floating point can differ slightly across engines. Set comparison tolerances grounded in numeric type and decision materiality.

Do not use display equality as reconciliation evidence.

### Define freshness and finality

Metric output should state included source/event watermark, successful publication time, dependency completeness and status such as preliminary or final.

Freshness is constrained by the stalest required source, not dashboard cache refresh alone. Late events and corrections need a reopen/restatement horizon.

Define when a period closes and who can reopen it.

### Version semantic changes

Changing name display or description without changing meaning can be compatible. Changing population, entity, formula, time role, units, window, dimension interpretation or approximation is usually breaking.

Publish a new contract version or dual-run comparison. Do not silently rewrite the definition behind a historical series.

Data corrections under the same contract are output revisions; keep definition version separate from data snapshot/version.

### Build a metric dependency graph

Derived metrics depend on base measures/metrics, filters, entities, dimensions and calendars. Store these edges so impact analysis finds consumers before changes.

The dbt metric specification explicitly models ratio dependencies on numerator/denominator and derived metrics on input metrics. A general registry should also capture hidden filter and calendar dependencies.

Detect cycles and prevent derived definitions from importing differently versioned aliases accidentally.

### Implement a semantic layer

Store metric contracts as version-controlled metadata/code, compile requests to reviewed query plans and expose the same definitions to BI, notebooks, APIs and applications.

The layer should know valid entities, joins, dimensions, aggregation behavior and time. It should reject unsafe combinations rather than generate arbitrary SQL.

Retain query/result metadata with metric version and source snapshot for reproduction.

### Preserve lineage to fields and jobs

Metric lineage must reach source measures, filters, identity maps, dimensions, calendars and transformations. Table-only lineage may miss a critical exclusion predicate.

The [OpenLineage dataset-lineage facet](https://openlineage.io/docs/spec/facets/dataset-facets/lineage/) supports dataset/job inputs and field-level transformations, illustrating a machine-readable foundation for structural lineage.

Supplement structural lineage with semantic ownership and rule rationale.

### Materialize components safely

Preaggregated metric tables can improve predictable workloads. Their grain includes dimensions, time bucket, contract version and publication snapshot.

Materialize additive components rather than only final ratios. Ensure aggregate awareness chooses a table whose dimensions/time and filters are compatible with the request.

Reconcile materialized results to direct semantic evaluation before promotion.

### Serve metrics through APIs

An API response includes metric ID/version, requested dimensions, time range/timezone, value plus components where appropriate, unit, approximation/status, source watermark and generated time.

Pagination/order do not apply to scalar values but matter for multidimensional series. Cache keys include all semantic parameters and authorization scope.

Avoid endpoints whose undocumented defaults vary from dashboard defaults.

### Apply privacy and access rules

Metrics can reveal sensitive information even without direct identifiers. Apply row/column policies before aggregation, and minimum-group or disclosure controls after grouping where required.

Suppressed is not zero. The sum of visible small cells should not allow trivial reconstruction of hidden cells.

Authorization is part of cache identity and result lineage.

### Test with golden fixtures

Create tiny datasets with hand-computed results for every rule boundary. Test exact keys/components, not only final formatted values.

Include duplicate/fanout, zero denominator, time-boundary, late event, missing dimension, current/as-of change, currency conversion, null, negative/reversal, approximate label and privacy suppression cases.

Run contract tests against SQL compilation and each important delivery adapter.

### Reconcile independent implementations

During migration or dual-run, freeze the same source snapshot, contract version, parameters and authorization. Compare component rows at the finest shared grain.

Classify differences as population, identity, join, time, unit, null, approximation, late-data or numeric-precision issues. Equal totals can hide offsetting slice errors.

Store diff evidence and signed approval before cutover.

### Observe metric health

Monitor value and components, eligible population, numerator subset violations, unmapped dimensions, join multiplicity, null rates, freshness, revisions, approximation error checks, query failures/latency, cache age and consumer adoption.

An abrupt metric shift can be real or a pipeline/definition defect. Correlate with releases, source coverage and business events.

Provide drill-through from observation to contributing governed entities where authorization permits.

### Govern lifecycle and deprecation

Review definitions with domain, finance/risk/privacy and technical owners appropriate to impact. Tier critical metrics and require stronger controls for executive, contractual or regulatory use.

When replacing a metric, publish mapping, definition diff, historical comparison, consumer inventory, migration date and retirement date. Preserve old version access only as policy allows.

Retire aliases and duplicate dashboard formulas so inconsistency does not return.

## Definitions and Notation

Let $R_s$ be an immutable governed source snapshot. Let $E_{M,p}(R_s)$ be the eligible entity set for metric contract $M$ and parameters $p$, and $X_{M,p}(R_s)\subseteq E_{M,p}(R_s)$ the successful subset for a proportion. Then

$$
rate(M,p,R_s)=\begin{cases}
|X_{M,p}(R_s)|/|E_{M,p}(R_s)|,&|E_{M,p}(R_s)|>0,\\
undefined,&|E_{M,p}(R_s)|=0.
\end{cases}
$$

Let dimension coordinate $d=(d_1,\ldots,d_k)$ and time bucket $t$ identify an output observation. A published key includes $(M.id,M.version,s,p,d,t)$ or an equivalent immutable result-snapshot identity.

For partitions $j$, additive numerator $x_j$, denominator $n_j$ and $N=\sum_jn_j>0$,

$$
\frac{\sum_jx_j}{N}=\sum_j\left(\frac{n_j}{N}\right)\left(\frac{x_j}{n_j}\right).
$$

Distinct entity sets obey $|A\cup B|=|A|+|B|-|A\cap B|$, showing why distinct counts are additive only when partitions are disjoint on the entity identity.

For stock $B_t$, a valid time rollup operator might be `last_valid` rather than sum. For flow $F_{(t_0,t_1]}$, adjacent compatible intervals add. Aggregation metadata is therefore a function of measure and dimension, not the numeric type alone.

Define evaluator $I(M,p,R_s)$ for an implementation. Cross-surface consistency requires equivalent canonical output and metadata for every governed request in a conformance suite, within declared numeric/approximation tolerance.

## Mechanisms, Invariants, or Proof Structure

**Definition mechanism.** Start from a decision, select entity/population, declare base grain/measures, define time and dimensions, specify aggregation/unit/null/revision/access behavior, assign owner/version, implement once, validate with golden cases and expose through governed interfaces.

**Weighted-rate theorem.** Since $r_j=x_j/n_j$, multiply each rate by weight $w_j=n_j/N$. Then $\sum_jw_jr_j=\sum_j(n_j/N)(x_j/n_j)=\sum_jx_j/N$. The arithmetic mean uses weight $1/J$ and is equal only under special conditions such as equal denominators or compensating rates.

**Subset invariant.** For a count-based conversion where every success must be eligible, $X\subseteq E$ implies $0\leq|X|\leq|E|$ and thus $0\leq rate\leq1$ when the denominator is positive. Violations expose identity, time, join or predicate mismatch.

**Distinct-union invariant.** Summing partition distinct counts is safe only if entity sets are pairwise disjoint. Otherwise intersections are double-counted; a global distinct operation or mergeable set/sketch state is required.

**Dimensional reconciliation invariant.** For an additive measure and a complete mutually exclusive dimension partition, the sum of slices equals the ungrouped total. Unknown/unmapped must appear as a governed member rather than disappear.

**Unit invariant.** Addition and comparison require compatible units and scale; conversion precedes aggregation when the conversion factor varies at finer grain. A ratio's derived unit follows numerator divided by denominator.

**Consistency condition.** Two deterministic implementations consuming the same contract/version, parameters, authorization, normalized source snapshot and numeric rules must be extensionally equal. A mismatch therefore identifies either a hidden input/rule difference or an implementation defect; coincidental equality on one total does not prove equivalence.

**Empirical evidence boundary.** Golden tests and dual-run comparisons demonstrate selected inputs/requests. They do not prove the business definition is useful, future data satisfies contracts or untested dimensional combinations are safe.

<!-- bijux-verify: {"id":"weighted-rate-rollup","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"eligible=12\nconverted=9\nratio_of_sums=0.7500\nmean_daily_rate=0.6500\ndifference=0.1000\nempty_denominator=undefined\nrollup_preserves_components=True\n","stderr":""}} -->
```python
daily = (
    {"day": "d1", "eligible": 2, "converted": 1},
    {"day": "d2", "eligible": 10, "converted": 8},
)
eligible = sum(row["eligible"] for row in daily)
converted = sum(row["converted"] for row in daily)
ratio_of_sums = converted / eligible
mean_daily_rate = sum(row["converted"] / row["eligible"] for row in daily) / len(daily)
empty_rate = None
print(f"eligible={eligible}")
print(f"converted={converted}")
print(f"ratio_of_sums={ratio_of_sums:.4f}")
print(f"mean_daily_rate={mean_daily_rate:.4f}")
print(f"difference={ratio_of_sums - mean_daily_rate:.4f}")
print(f"empty_denominator={'undefined' if empty_rate is None else empty_rate}")
print(f"rollup_preserves_components={eligible == 12 and converted == 9}")
```

## Alternatives and Trade-Offs

**Central semantic layer versus governed metric marts.** A semantic layer supports flexible dimensions and one definition graph. Metric marts offer predictable performance and simple access. Use the same contract to generate/reconcile both.

**Metric registry versus prose catalog.** A prose catalog improves discovery but cannot enforce joins, time or aggregation. Executable metadata enables compilation/testing but still needs human rationale and ownership.

**Exact versus approximate distinct/quantile.** Exactness simplifies interpretation and may be costly at scale. Sketches improve mergeability/performance but require visible uncertainty, parameters and compatible versions.

**Current versus as-of dimensions.** Current classification answers today's portfolio view; as-of classification preserves historical context. Neither should silently substitute for the other.

**Precomputed ratio versus stored components.** A final ratio is convenient but not safely rollable. Components take more columns but retain aggregation flexibility and auditability.

**Fixed versus parameterized metric.** Fixed windows/populations improve comparability. Parameters support exploration but can create countless incomparable variants. Constrain and record allowed parameters.

**Restate versus freeze.** Restatement improves corrected historical truth but changes prior reports. Frozen publication supports audit but retains known errors. Versioned snapshots can support both views under policy.

**Strict rejection versus best-effort output.** Blocking on incomplete inputs protects critical decisions. Provisional results improve timeliness. Return explicit quality/finality metadata and choose by consequence.

**Shared definition versus domain-specific variant.** A conformed metric reduces disagreement. Distinct domain decisions may require honest variants rather than a lowest-common-denominator formula.

**Semantic query versus dashboard calculation.** Central queries preserve contract and lineage. Dashboard calculations are fast to experiment with but drift easily; promote valuable experiments into governed definitions.

## Failure Modes and Misconceptions

- **“A metric is its formula.”** Population, time, grain, units and status are also semantic.
- **“A good name is self-defining.”** `active_user` still needs entity, action, window and eligibility.
- **“One owner means no collaboration.”** It establishes a decision point, not solitary design.
- **“Count rows equals count customers.”** Source grain may contain many rows per entity.
- **“Only actors belong in the denominator.”** Nonparticipants can be eligible.
- **“Numerator and denominator can use similar filters.”** Similar is not identical/subset-safe.
- **“Zero denominator means zero conversion.”** The rate is undefined or not applicable.
- **“Percentages can be averaged.”** Denominator weights determine pooled rates.
- **“Daily distincts sum to monthly distinct.”** Returning entities overlap days.
- **“Medians roll up from subgroup medians.”** The combined distribution is missing.
- **“All numeric fields are additive.”** Stocks, ratios and distincts have different algebra.
- **“Null is zero.”** Unknown, absent, suppressed and not applicable differ.
- **“Current month can be compared with last full month.”** Completeness and elapsed windows differ.
- **“Date is obvious.”** Created, fulfilled, invoiced and settled time answer different questions.
- **“UTC day is universal.”** Business calendars and timezone boundaries matter.
- **“Current segment is historical segment.”** Temporal dimension policy changes attribution.
- **“A semantic layer prevents bad joins automatically.”** Entity/cardinality metadata must be correct.
- **“Symmetric aggregates fix every model.”** They protect supported measures, not ambiguous meaning.
- **“USD and EUR are both money, so sum them.”** Currency is part of the unit.
- **“Round early for consistency.”** Early rounding may accumulate drift unless policy requires it.
- **“Approximate counts are close enough to call exact.”** Estimates require algorithm/error metadata.
- **“Published now means fresh now.”** Inputs may have old watermarks.
- **“Final means no correction can occur.”** Closure is a governance policy, not physical certainty.
- **“Fixing data changes the metric definition.”** Output revision and semantic version are distinct.
- **“Same dashboard total proves consistency.”** Slice-level differences can cancel.
- **“A wiki is a semantic layer.”** Prose does not compile/enforce behavior.
- **“Copying governed SQL into another tool preserves governance.”** The copy can drift and lose version/lineage.
- **“Aggregate metrics are anonymous.”** Small groups and differences can disclose sensitive facts.

## Worked Examples

### Example 1

Two dashboards report monthly active users. One counts devices with any page view; the other counts authenticated accounts completing a meaningful action.

Both SQL queries are internally valid, but the metrics differ in entity, eligibility and action. The organization assigns distinct names and owners, then chooses one governed executive metric rather than averaging or silently replacing them.

### Example 2

A trial conversion dashboard builds its denominator from purchase events. Trials that never purchase are absent, so displayed conversion is 100 percent.

The correct eligibility table contains every qualifying trial at start. Purchases form a time-ordered subset within 30 days. The output publishes eligible and converted counts plus rate and completeness.

### Example 3

Store A converts 1 of 2 visitors and Store B converts 8 of 10. A dashboard averages 50 and 80 percent to 65 percent.

The pooled business metric sums components to 9 of 12, or 75 percent. A 65-percent macro-average can be separately valid when every store should have equal policy weight, but it needs that name and purpose.

### Example 4

Daily unique accounts are 100 and 120. Adding them produces 220 monthly active accounts, but 80 accounts used the service both days.

The true union is $100+120-80=140$. The model retains identity-level evidence or a compatible mergeable distinct sketch; it never labels the sum of daily distincts as monthly distinct.

### Example 5

A revenue metric joins orders to items and doubles orders with two items. The final monthly total is inflated while item filters appear to work.

The semantic graph declares order as primary entity and join cardinality. Revenue aggregates once per order key, or line-level revenue is used at item grain. Grain/fanout fixtures and base reconciliation block the faulty definition.

### Example 6

A customer moves from SMB to Enterprise in March. A January report changes after a dimension refresh because it uses current segment.

The system exposes `revenue_by_segment_at_order` and `revenue_by_current_segment` as separate dimension semantics. January's as-of series remains reproducible; the current portfolio view can legitimately reclassify.

### Example 7

Orders are recorded in EUR and USD. A monthly job sums original amounts, then multiplies the total by one month-end EUR/USD rate.

The metric converts each eligible transaction using the governed rate effective at its declared time, then sums target-currency values. It retains original amount/currency and rate lineage so finance can reconcile.

### Example 8

An approximate unique-user sketch changes precision during a quarter. The quarter union merges incompatible states and silently shifts.

The metric contract includes algorithm, precision and sketch version. Incompatible states are recomputed from identities or kept as separate versions; output is labeled estimate with validation/error metadata.

### Example 9

A dashboard refreshes at 09:00, but one source watermark is 02:00 and another is 08:55. It displays “updated 09:00.”

The result reports publication time 09:00 and conservative data cutoff 02:00, with dependency details and provisional status. Freshness alerts target the lagging source rather than the dashboard cache.

### Example 10

A team changes “active account” from one login to three meaningful actions and edits the existing semantic definition. Historical charts break with no visible boundary.

The new definition receives a new contract version/name alias, runs side by side over the same snapshots and publishes component/slice differences. Consumers migrate deliberately; prior reports retain their original version.

## Cross-Program Connections

- [Database Engineering](../../18-database-engineering/ROADMAP.md): keys, numeric types, constraints, temporal joins and aggregates implement metric contracts.
- [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md): business vocabulary, ownership, lineage and conformed dimensions provide enterprise semantic governance.
- [Large-Scale Data Systems Engineering](../../21-large-scale-data-systems-engineering/ROADMAP.md): sketches, preaggregation, caching and distributed joins shape scalable metric execution.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md): measurement validity, feedback delay and uncertainty determine whether a metric can control a system safely.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md): late data, snapshot consistency, idempotence and versioned publication affect reproducibility.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md): metric APIs need explicit parameters, versions, status, authorization and cache semantics.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md): catalogs, semantic compilation, observability, access control and change workflows make metrics operable.

## References

1. dbt Labs, [Semantic Models](https://docs.getdbt.com/docs/build/semantic-models). Documents semantic entities, dimensions, time dimensions, measures/simple metrics and graph-based joins.
2. dbt Labs, [Creating Metrics](https://docs.getdbt.com/docs/build/metrics-overview). Documents simple, ratio, cumulative, derived and conversion metric definitions and dependencies.
3. World Wide Web Consortium, [The RDF Data Cube Vocabulary](https://www.w3.org/TR/vocab-data-cube/). Defines observations, dimensions, measures, attributes, units/status metadata and reusable data structures.
4. Google Cloud, [Looker Measure Types](https://docs.cloud.google.com/looker/docs/reference/param-measure-types). Documents aggregation categories, distinct measures and post-query calculations.
5. Google Cloud, [Understanding Symmetric Aggregates](https://docs.cloud.google.com/looker/docs/best-practices/understanding-symmetric-aggregates). Explains fact-grain aggregation under join fanout and reliance on unique primary keys.
6. Google Cloud, [BigQuery Approximate Aggregate Functions](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/approximate_aggregate_functions). Distinguishes scalable estimates from exact distinct and quantile calculations.
7. OpenLineage, [Lineage Dataset Facet](https://openlineage.io/docs/spec/facets/dataset-facets/lineage/). Defines machine-readable dataset/job inputs and field-level transformation lineage.

## Exercises

### Exercise 1

Write a complete contract for monthly net recognized revenue across currencies. Include entity/grain, eligibility, components, tax/discount/refund treatment, time, conversion, dimensions, units, precision, close/revision, lineage, owner and tests.

### Exercise 2

Three segments have conversions `(1,2)`, `(20,100)` and `(0,0)` as `(success,eligible)`. Compute the pooled valid rate and macro-average policy options. Explain zero-denominator handling and which components must be retained.

### Exercise 3

Design weekly and monthly active-account metrics from event data. Address meaningful action taxonomy, account identity merge/split, timezone, rolling versus calendar windows, daily-distinct non-additivity, late events, bots/tests and current/as-of dimensions.

### Exercise 4

Two implementations of average resolution time disagree by 4 percent. Produce a component-level reconciliation plan covering grain, eligibility, time, reopenings, pauses, nulls, quantiles/means, precision, snapshot and access.

### Exercise 5

Plan a breaking activation-metric change from “created first project” to “published first successful workflow within seven days.” Specify dual run, versions, historical recomputation, acceptance evidence, API/dashboard migration, cache behavior, communication and retirement.

## Answers to the Exercises

### Answer 1

Define one recognized revenue component row per governed recognition line, linked to contract/order but unique independently. Eligibility includes posted, in-scope legal entities and accounting statuses; exclude voided entries, represent refunds/reversals as signed lines, and specify whether tax/discount belong in gross-to-net components. Use recognition-effective timestamp in the legal entity's governed accounting calendar, not ingestion or payment time.

Retain original amount/currency, rate source/type/effective time and converted reporting-currency amount; convert at line grain before summing. Publish gross, discount, refund, tax (if applicable) and net components that reconcile. Dimensions use as-of accounting mappings and unknown members. Specify decimal types, line versus final rounding, monthly close, allowed restatement/version snapshots and finality. Assign finance-domain owner and technical steward; expose source/FX lineage, watermarks and contract version. Test multi-currency, negative reversal, late posting, boundary instant, missing rate, duplicate line, dimension change, closed-period correction and ledger control totals.

### Answer 2

Ignore the third segment as a rate observation because its denominator is zero, but retain its `eligible=0`, `success=0`, and undefined/not-applicable status. The pooled rate across eligible population is $(1+20)/(2+100)=21/102\approx0.205882$.

A macro-average over segments with defined rates is $(0.5+0.2)/2=0.35$ if the policy intentionally weights the two observed segments equally. Treating the undefined segment as zero would give $0.2333\ldots$ and invent meaning. Retain success and eligible counts per segment, output status and weighting policy; recompute the pooled rate from summed components.

### Answer 3

Define account as the entity within tenant and a versioned allowlist of meaningful accepted events. Exclude test/internal/bot or consent-ineligible records through explicit dispositions. Choose business timezone and either calendar week/month or rolling windows as different metrics. Deduplicate event identity and count each resolved account once per requested window; never sum daily distinct counts.

Version identity merges/splits and define whether prior activity is retroactively reassigned. Use event time with deterministic boundaries; publish source watermark and reopen periods within allowed lateness. For segmentation, name current and event-time/as-of variants separately. Tests cover silent eligible accounts if a rate is involved, duplicate/replayed events, exact week boundary, late offline action, bot burst, account merge, missing segment and partial current window.

### Answer 4

Freeze one contract/version, parameter set, authorization and source snapshot. Extract one row per ticket/episode from each implementation with opened/closed/reopened milestones, pause durations, eligibility disposition, effective duration, unit and exclusion reason. Compare exact key sets before averages; classify missing/extra/duplicate episodes and fanout.

Align whether resolution uses first close, final close or each cycle; whether reopened tickets remain eligible; business versus elapsed clock; timezone; paused intervals; unresolved/null handling; and negative/corrected times. Confirm both compute the same statistic—mean versus median/percentile—and use sum duration plus eligible count for the mean. Compare numeric types/rounding and source watermarks. Slice diffs by source/status/date, resolve access-filter differences, then rerun golden cases and full component reconciliation before cutover.

### Answer 5

Keep the existing metric contract immutable and create a new version with account eligibility, creation anchor, successful workflow event authority, ordering, seven-day half-open window, identity/time rules and finality. Compute both from identical historical snapshots and publish eligible, project-created, workflow-published and conversion components by important dimensions.

Agree acceptance examples and expected business differences with the owner; investigate unexpected key-level diffs. Recompute history under the new version without overwriting old published snapshots. Add the version to semantic queries and API responses, include it in authorization-aware cache keys, and dual-display dashboards during migration. Inventory consumers, publish definition/version comparison and migration deadline, switch defaults explicitly, monitor usage/value changes, then retire old aliases/endpoints after confirmed migration while retaining governed historical reproducibility.
