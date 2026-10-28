---
module_id: DARCH-044
program: Data Architecture Engineering
level: 1
module_number: 44
title: Data Mart Strategies
status: complete
last_verified: 2026-09-03
---

# Data Mart Strategies

## One-Page Review

### Governing question

How should architects create bounded analytical marts that improve consumer fit, performance, autonomy, and protection without multiplying incompatible facts, dimensions, metrics, histories, copies, and ownership?

### Essential definitions

- A **data mart** is a bounded analytical product shaped for a declared process, decision set, consumer population, and service contract.
- A **dependent mart** derives from governed enterprise or domain products rather than integrating operational sources independently.
- An **independent mart** acquires and interprets sources on its own, creating separate integration and governance responsibility.
- A **logical mart** exposes governed views or semantic definitions without necessarily persisting another result population.
- A **physical mart** persists consumer-oriented facts, dimensions, aggregates, indexes, extracts, or serving tables.
- An **aggregate mart** precomputes a reduced grain for recurring workloads while retaining lineage to finer-grained authority.
- A **consumer-aligned mart** adapts governed source or aggregate products to one consumer context without claiming universal meaning.
- **conformance** means facts, dimensions, keys, codes, time, and definitions are compatible for declared cross-mart uses.
- **drill across** compares separate fact populations after independently aggregating them to compatible conformed dimensions.
- **mart proliferation** is growth in overlapping marts whose costs, meanings, consumers, controls, or lifecycle are not governed.
- A **promotion path** turns exploratory logic into a supported product through ownership, contracts, tests, protection, and service evidence.
- A **mart portfolio** is the governed inventory of mart purposes, dependencies, consumers, overlaps, service, cost, risk, and lifecycle.

### Central model, mechanism, or theorem

Represent a mart decision as:

`M = (outcomes, consumers, sources, semantics, grain, time, materialization, service, protection, ownership, evidence, lifecycle)`

Choose mart boundaries from coherent decisions and workloads, not organization-chart labels alone. Prefer dependent or logically derived marts when governed upstream products already preserve suitable authority and history. Permit independent integration only when its outcome, risk, owner, evidence, and convergence or exit path are explicit. Cross-mart comparison aggregates each fact independently to compatible conformed dimensions; joining raw fact tables can multiply rows and measures.

### Critical invariants

- Every mart names its consumers, decisions, authoritative inputs, grain, identities, measures, time, history, permitted use, and owner.
- A mart is authoritative only for declared consumer-facing analytical assertions, not implicitly for operational sources or all enterprise meaning.
- Dependent marts preserve upstream identity, semantic, temporal, quality, lineage, correction, and protection contracts or document intentional transformation.
- Independent marts carry full source-integration, reconciliation, history, correction, and retirement responsibility.
- Cross-mart measures use compatible definitions, currencies, units, calendars, populations, and effective versions.
- Multiple fact populations are aggregated independently before drill across; row-level cross-products are prohibited unless explicitly intended.
- Physical duplication has justified performance, isolation, protection, or availability value and a governed refresh and deletion path.
- Exploratory marts have bounded access, cost, retention, and promotion or disposal criteria.
- Mart portfolio reviews expose overlap, unknown consumers, stale products, semantic divergence, protection gaps, and unfunded ownership.
- Retirement removes data, views, extracts, credentials, jobs, caches, catalog entries, alerts, contracts, and consumer dependencies while preserving required evidence.

### Common failures

Common failures are making one mart per department; calling any schema a mart; copying operational tables directly; building independent marts because enterprise delivery is slow; sharing dimension names without conformance; mixing grains in one table; joining fact tables row by row; using current dimensions for historical promises; implementing metrics privately in dashboards; treating a view as free; materializing every query; hiding source and release cutoffs; granting all analysts access to copied protected data; letting sandboxes become production; measuring only query speed; ignoring refresh and correction; keeping duplicate marts during migration indefinitely; assuming no queries means no consumers; and deleting mart tables while leaving extracts, credentials, caches, or scheduled reports.

### Compact example

A Sales mart records order-line revenue; a Returns mart records return events. Both use conformed Region and Calendar dimensions but have different grains. Joining raw facts by region produces a many-to-many multiplication and inflates Sales. Correct drill across aggregates Sales and Returns separately by conformed region and period, then joins the summaries. The mart contracts also align currency, recognition, cutoff, correction, and release versions before publishing net revenue.

### Connections

[DARCH-025](025-source-aligned-aggregate-and-consumer-aligned-data.md), [DARCH-027](027-producer-and-consumer-contracts.md), [DARCH-041](041-enterprise-data-warehouse-architecture.md), and [DARCH-043](043-lakehouse-architecture.md) establish product, contract, warehouse, and platform foundations. Data Engineering [DENG-011](../../19-data-engineering/modules/011-grain-and-the-meaning-of-a-row.md) through [DENG-020](../../19-data-engineering/modules/020-validating-an-analytical-model-against-business-questions.md) own implementation-level modeling. This module defines mart strategy and prepares [DARCH-045](../ROADMAP.md) on semantic and metrics layers.

## Governing Question

Data marts are often described as small warehouses for departments. That description hides the important decisions: whether a mart integrates sources or derives from governed products, which analytical meaning it owns, which consumers it serves, why another materialization exists, and how it remains compatible with other marts.

The governing question is not whether marts are good or bad. It is which bounded analytical product shape creates consumer value while preserving authority, conformance, protection, service, and lifecycle across the wider data architecture.

## Why This Matters

The Kimball Group's [Data Warehouse Bus Architecture](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/kimball-data-warehouse-bus-architecture/) describes incremental process-oriented delivery through conformed dimensions. Its [Conformed Dimensions](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/conformed-dimension/) guidance and [Four-Step Dimensional Design Process](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/four-4-step-design-process/) make compatibility and grain architectural commitments, not naming conventions.

Microsoft's [Star Schema Guidance](https://learn.microsoft.com/en-us/power-bi/guidance/star-schema) explains fact and dimension roles in analytical semantic models. The W3C [RDF Data Cube Vocabulary](https://www.w3.org/TR/vocab-data-cube/) formalizes observations, dimensions, measures, attributes, and integrity constraints. PostgreSQL's [Materialized Views](https://www.postgresql.org/docs/current/rules-materializedviews.html) documentation illustrates that persisted query results differ operationally from ordinary views.

Google's [Addressing Cascading Failures](https://sre.google/sre-book/addressing-cascading-failures/) applies when many marts contend for shared sources, warehouses, catalogs, and compute. NIST [SP 800-160 Volume 1 Revision 1](https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final) frames trustworthy lifecycle engineering. Mart strategy must combine semantic and operational discipline.

## Prerequisites and Retrieval

You should understand data products, facts, dimensions, grain, measures, conformance, history, warehouses, lakes, lakehouses, views, materialization, contracts, lineage, quality, access control, service objectives, and lifecycle cost.

Retrieve data mart, dependent, independent, logical, physical, aggregate, consumer-aligned, source-aligned, conformed dimension, conformed fact, drill across, semantic model, extract, cache, refresh, release, sandbox, promotion, overlap, portfolio, deprecation, and retirement.

As a retrieval test, inspect “Marketing needs its own mart.” Ask which decisions, consumers, authoritative inputs, grain, dimensions, measures, time, freshness, workload, protection, existing products, autonomy constraint, owner, and expiry apply. Without these, the request names an organizational container rather than an analytical product.

## Learning Objectives

After completing this module, you should be able to:

1. define a mart from coherent outcomes, consumers, semantics, workloads, and ownership;
2. distinguish dependent, independent, logical, physical, aggregate, domain, and consumer-aligned mart strategies;
3. select mart sources and boundaries while preserving operational and analytical authority;
4. design compatible grains, facts, dimensions, measures, time, releases, and histories across marts;
5. use safe drill-across patterns and detect cross-fact multiplication;
6. justify views, materializations, extracts, caches, and serving stores by service and lifecycle evidence;
7. govern refresh, quality, reconciliation, correction, restatement, and consumer notification;
8. apply purpose, minimization, authorization, derived sensitivity, retention, deletion, and egress controls;
9. operate a mart portfolio that manages overlap, sandboxes, promotion, cost, deprecation, and retirement;
10. migrate marts incrementally while preserving contracts, validation, rollback, and closure.

## Core Exposition

**Start with a coherent decision set.** Name the decisions, questions, reports, models, and workflows that share consumers, meaning, service, and change cadence.

A department may need several marts; several departments may share one mart. Organization charts are evidence about accountability, not sufficient product boundaries.

**Define consumers precisely.** Record roles, tools, skills, access contexts, concurrency, query patterns, extracts, automation, consequences, and support expectations.

“Analysts” is too broad. A month-end controller, exploratory scientist, customer-facing application, and regulator need different contracts.

**Assign analytical authority.** Name who owns each measure, classification, conformed dimension, release, and consumer promise.

The mart team can own presentation and service without owning source facts or enterprise definitions. Record derivation and escalation boundaries.

**Bound the product.** Declare included processes, entities, periods, regions, populations, facts, dimensions, measures, histories, consumers, and exclusions.

Avoid marts named only `business`, `reporting`, or `analytics`. Durable names describe the process or decision capability.

**Classify the mart strategy.** Determine whether the mart derives from governed enterprise or domain products, integrates sources independently, exposes logical views, persists physical results, preaggregates a workload, or adapts a product for one consumer.

Strategies can combine. Record each responsibility rather than applying one label to the entire stack.

**Prefer dependent derivation when suitable.** A dependent mart inherits authoritative inputs, stable identities, conformed semantics, history, quality, correction, lineage, and protection from governed upstream products.

Inheritance is not automatic. Validate that transformations preserve or intentionally adapt those contracts and that freshness meets the consumer need.

**Treat independent marts as integration systems.** Direct source acquisition creates duties for snapshots or changes, source positions, identity, mappings, history, quality, reconciliation, correction, protection, and source change.

Independent can be justified by urgent bounded need, regulatory isolation, acquisition constraints, or unavailable upstream semantics. It is not a free shortcut.

**Define convergence or permanence.** A temporary independent mart needs an expiry and migration trigger. A permanent independent mart needs explicit enterprise relationship and duplicated-control funding.

Do not promise future convergence without an owner, target product, compatibility plan, and decision date.

**Use logical marts where persistence adds little.** Views and semantic definitions can provide naming, row and field restriction, joins, calculations, and consumer contracts over governed tables.

Logical does not mean costless. Runtime source load, query latency, availability coupling, optimizer behavior, and policy must be tested.

**Use physical marts for named value.** Materialization can isolate workloads, precompute complex logic, stabilize latency, preserve releases, localize data, or serve specialized engines.

It adds storage, refresh, lag, synchronization, correction, protection, lineage, recovery, and retirement. Quantify both sides.

**Use aggregate marts carefully.** Preaggregate recurring facts to a declared grain and retain dimensions required by supported questions.

Aggregation discards detail. Preserve lineage to atomic authority, document additivity and filters, and reconcile results after every logic or source change.

**Use consumer-aligned marts without universalizing them.** A finance close mart may apply materiality, calendar, and currency rules appropriate to Finance.

Label the context. Do not silently publish its result as the only enterprise definition when other decisions legitimately differ.

**Keep source-aligned and consumer-aligned responsibilities separate.** Source products preserve domain assertions; marts organize them for a decision.

Combining them physically can be efficient, but owners and contracts should still distinguish source correction from consumer transformation.

**Declare grain first.** State exactly what one fact row, dimension row, aggregate row, and snapshot represents.

Test uniqueness at its population and time. Mart convenience does not justify mixing orders, lines, shipments, customers, and monthly summaries in one ambiguous row.

**Conform dimensions deliberately.** Define stable identities, shared attributes, code mappings, hierarchy, unknown members, valid intervals, source precedence, and permitted subsets.

Conformance may be exact, subset, or roll-up. Similar columns and names do not establish compatibility.

**Conform facts and measures.** Align event definitions, grain, units, currency, sign, tax, allocation, estimation, null behavior, additivity, effective version, and owner.

Two `revenue` fields can both be correct for different contexts. Cross-mart comparison needs a named compatible definition or explicit translation.

**Preserve time semantics.** Distinguish business-effective, source transaction, observation, ingestion, transformation, release, and query time.

Align calendars, zones, period closing, late data, and restatement before comparing marts. A shared date dimension cannot repair incompatible cutoffs.

**Use drill across rather than raw fact joins.** Aggregate each fact population independently to compatible conformed dimensions, then join the summaries.

Raw Sales and Returns facts can have many rows per region and create a cross-product. Safe comparison respects each grain.

**Validate conformed coverage.** Compare dimension keys, unknown rates, hierarchy versions, effective intervals, and population boundaries across participating marts.

Shared dimension tables can still be used inconsistently when facts resolve different versions or exclude different members.

**Define mart releases.** Bind upstream snapshots or releases, transformation and metric versions, quality, reconciliation, exceptions, protection, and publication time.

Consumers should be able to reproduce a report without guessing which “current” inputs were combined.

**Align multi-mart releases.** Cross-mart products need a compatible vector of mart releases or a defined staleness relationship.

Individually current marts can reflect different source cutoffs. Record acceptable skew and degraded behavior.

**Reconcile from authority to mart.** Compare source or governed product populations by keys, measures, dimensions, time, deletes, distributions, and exceptions.

Equal totals can mask offsetting defects. Reconciliation uses equivalent cutoffs and canonical rules.

**Design correction and restatement.** Identify affected keys, periods, marts, metrics, extracts, caches, reports, models, and decisions.

Publish successor releases, preserve required prior evidence, notify consumers, and verify downstream repair. A corrected upstream table does not automatically repair every copy.

**Separate semantic and physical optimization.** A stable logical contract can map to a view, table, materialized view, aggregate, index, cache, or specialized serving store.

Change physical form behind versioned contracts when evidence justifies it. Do not force consumers to depend on implementation names.

**Benchmark consumer workloads.** Measure end-to-end freshness, query latency percentiles, concurrency, scan volume, cache states, update frequency, peak, failure, backfill, and cost.

A single dashboard query is not representative. Include competing workloads and upstream publication delay.

**Isolate critical marts.** Month-end close, regulatory reports, and customer-facing analytics may need reserved compute, workload queues, replicas, or separate serving systems.

Isolation reduces interference but adds copies and operations. Verify it against named service consequences.

**Protect shared platforms from mart fan-out.** Hundreds of marts can duplicate scans, refresh simultaneously, exhaust catalogs, or retry against failing sources.

Coordinate schedules, quotas, caching, materialization, backpressure, retry, and source budgets. Consumer autonomy needs platform guardrails.

**Apply purpose and minimization.** A consumer-focused mart should usually contain fewer fields and rows than its upstream sources.

Do not copy protected columns “in case.” Record purpose, subject relation, classification, transformations, and approved consumers.

**Trace derived sensitivity.** Aggregates, segments, scores, small cohorts, inferred attributes, and combined dimensions can reveal protected facts.

Reclassify outputs and metadata after derivation. Aggregation is not automatically anonymization.

**Control egress.** BI extracts, spreadsheets, files, APIs, caches, notebooks, and model inputs become downstream copies with their own retention and correction.

Register durable consumers, scope credentials, limit downloads, observe use, watermark exports where appropriate, and propagate deletion.

**Design row and field security across paths.** Mart tables, views, semantic models, direct storage, query caches, and exports must agree on policy.

A secure dashboard over a broadly readable table is not an access-control boundary.

**Define freshness at the decision boundary.** Mart refresh completion does not prove fresh upstream inputs, updated semantic logic, refreshed extracts, or current dashboards.

Measure source observation through consumer use. Publish stale and incomplete states explicitly.

**Define mart service.** Record publication schedule, freshness, completeness, query latency, concurrency, availability, recovery, correction, support, and deprecation.

Different marts can have different service tiers. Uniform gold labels hide cost and consequence.

**Recover more than tables.** Restore upstream release links, schemas, transformations, metric versions, policies, identities, lineage, schedules, extracts, caches, and consumer routes.

Test rebuilding dependent marts and restoring irreplaceable independent history. State RPO and RTO per responsibility.

**Make mart metadata discoverable.** Publish purpose, owner, consumers, authoritative inputs, grain, measures, dimensions, time, releases, quality, lineage, policy, service, cost, incidents, and lifecycle.

Reconcile catalog declarations with runtime dependencies and observed use. Unknown consumers block safe change.

**Maintain a portfolio inventory.** Group marts by process, source, measure, consumer, platform, and overlap.

Track value, adoption, freshness, quality, cost, incidents, protection exceptions, semantic divergence, and lifecycle status. Inventory enables rational consolidation.

**Detect harmful overlap.** Two marts can overlap safely when they serve different service, protection, history, or consumer contracts.

Overlap is harmful when the same assertion has conflicting owners or meanings, duplicated work has no benefit, or no one can identify authority.

**Govern sandboxes.** Exploratory marts need scoped data, isolated compute, cost limits, expiry, owner, classification, and no implicit production consumers.

Exploration benefits from flexibility. Its outputs become products only through promotion gates.

**Define promotion.** Require stable ownership, named consumers, semantic contracts, tests, quality, lineage, protection, service, operations, recovery, support, and lifecycle.

Do not promote merely by moving a table to a production schema. Validate results against the exploratory claim and governed inputs.

**Support local autonomy with paved paths.** Provide templates for mart contracts, conformed identities, transformations, testing, publication, access, observability, cost, and deprecation.

Central review should focus on consequence and interoperability, not become a queue for every safe local change.

**Handle exceptions explicitly.** An independent mart or private metric may be necessary during acquisition, incident response, or regulatory isolation.

Record scope, owner, risk, controls, review date, consumer warnings, and removal or permanence decision.

**Migrate by consumer cohort.** Inventory marts, dashboards, extracts, schedules, APIs, notebooks, models, credentials, owners, histories, and observed queries.

Build target products, validate equivalent releases and decisions, move registered cohorts, and keep authority and rollback explicit.

**Bound dual running.** Old and new marts can diverge in refresh, semantics, correction, and access.

Set reconciliation cadence, accepted differences, write rules, exception owner, exit criteria, and expiry. Coexistence is a temporary product with cost.

**Retire completely.** Stop refreshes and queries; revoke identities and routes; remove tables, views, extracts, files, caches, jobs, alerts, catalog entries, and licenses.

Preserve required evidence and holds. Verify consumer closure and absence of use before declaring retirement.

**Measure mart value.** Track decision lead time, query service, semantic consistency, consumer adoption, defects, correction time, protection exceptions, source load, cost, and retired duplication.

Table count and dashboard count are activity. Value is fit decisions with controlled architecture and lifecycle.

## Definitions and Notation

Represent mart architecture as $M=(U,C,S,G,T,P,V,Q,Z,O,E,L)$, where $U$ is outcomes, $C$ consumers, $S$ authoritative sources, $G$ grain and semantics, $T$ time and history, $P$ physical or logical form, $V$ release and serving behavior, $Q$ service and quality, $Z$ protection, $O$ ownership, $E$ evidence, and $L$ lifecycle.

For facts $F_1$ and $F_2$ with compatible conformed dimension projection $d$, safe drill across computes $A_1=aggregate(F_1,d)$ and $A_2=aggregate(F_2,d)$ independently, then joins $A_1$ and $A_2$ on $d$. Joining raw facts on nonunique $d$ can create $|F_{1,d}|\times|F_{2,d}|$ rows per member.

For mart release $r$, let $R_r$ bind upstream releases, mart model and metric versions, consumer grain, quality and reconciliation evidence, protection state, and publication time. Current table state alone is not this contract.

Define `FitMart(M,r,t)` as a review predicate requiring coherent outcomes, authoritative and compatible inputs, declared grain and time, justified materialization, validated measures and conformance, acceptable service and quality, effective protection, supported ownership, lifecycle advantage, migration seams, and evidence at time $t$.

## Mechanisms, Invariants, or Proof Structure

Use ten gates for every consequential mart.

**1. Outcome gate.** Name consumers, decisions, processes, questions, consequence, scope, value, owner, and exclusions.

**2. Authority gate.** Define source assertions, analytical ownership, upstream products, independence, duplicated integration, and escalation.

**3. Semantic gate.** Define grain, keys, facts, dimensions, measures, units, currency, time, history, corrections, and limitations.

**4. Conformance gate.** Test identities, attributes, codes, hierarchies, populations, calendars, releases, drill-across compatibility, and divergence.

**5. Form gate.** Justify logical views, physical tables, aggregates, materialized views, extracts, caches, indexes, or serving stores.

**6. Release gate.** Bind upstream cutoffs, transformations, metric versions, quality, reconciliation, exceptions, publication, and restatement.

**7. Protection gate.** Apply purpose, minimization, row and field access, derived sensitivity, regions, retention, deletion, holds, egress, and audit.

**8. Service gate.** Test freshness, query performance, concurrency, isolation, capacity, failure, recovery, correction, support, and cost.

**9. Portfolio gate.** Record discovery, consumers, overlap, sandboxes, promotion, exceptions, incidents, value, deprecation, and consolidation.

**10. Lifecycle gate.** Plan migration, coexistence, rollback, review triggers, consumer closure, data disposition, and verified retirement.

The executable example contrasts a raw cross-fact join with safe drill across.

<!-- bijux-verify: {"id":"mart-safe-drill-across","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"sales_fact_rows=3\nreturn_fact_rows=3\nunsafe_join_rows=5\nunsafe_sales_total=400\nsafe_sales_total=250\nsafe_returns_total=35\nsafe_net_total=215\nconformed_regions=EU,NA\n","stderr":""}} -->
```python
sales = [
    {"region": "EU", "revenue": 100},
    {"region": "EU", "revenue": 50},
    {"region": "NA", "revenue": 100},
]
returns = [
    {"region": "EU", "refund": 15},
    {"region": "EU", "refund": 10},
    {"region": "NA", "refund": 10},
]

unsafe = [
    (sale, returned)
    for sale in sales
    for returned in returns
    if sale["region"] == returned["region"]
]

def aggregate(rows, value_name):
    result = {}
    for row in rows:
        region = row["region"]
        result[region] = result.get(region, 0) + row[value_name]
    return result

sales_by_region = aggregate(sales, "revenue")
returns_by_region = aggregate(returns, "refund")
regions = sorted(set(sales_by_region) | set(returns_by_region))

safe_sales = sum(sales_by_region.values())
safe_returns = sum(returns_by_region.values())
unsafe_sales = sum(sale["revenue"] for sale, _ in unsafe)

print(f"sales_fact_rows={len(sales)}")
print(f"return_fact_rows={len(returns)}")
print(f"unsafe_join_rows={len(unsafe)}")
print(f"unsafe_sales_total={unsafe_sales}")
print(f"safe_sales_total={safe_sales}")
print(f"safe_returns_total={safe_returns}")
print(f"safe_net_total={safe_sales - safe_returns}")
print(f"conformed_regions={','.join(regions)}")
```

The result proves only that these two declared in-memory fact populations produce row multiplication under a raw region join and the stated totals under independent aggregation. Production drill across also needs compatible dimension identities, grains, measures, currencies, calendars, populations, releases, corrections, quality, and consumer validation.

## Alternatives and Trade-Offs

**Dependent versus independent mart.** Dependence reuses integration and conformance but inherits upstream latency and priorities. Independence increases local control while duplicating semantic, quality, protection, and lifecycle duties.

**Logical versus physical mart.** Logical marts avoid persistent copies but couple runtime service. Physical marts improve isolation and latency while adding refresh, correction, recovery, and deletion.

**Atomic versus aggregate mart.** Atomic detail supports flexible questions and audit. Aggregates reduce work for stable questions but discard dimensions and need reconciliation.

**Process-aligned versus department-aligned mart.** Processes often support reusable facts across teams. Department alignment can clarify ownership for unique decisions. Choose from coherence, not slogans.

**Domain-aligned versus enterprise mart.** Domain ownership preserves meaning and change autonomy. Enterprise products resolve shared cross-domain decisions. Both need explicit conformance boundaries.

**One shared mart versus consumer-specific variants.** Sharing reduces duplication and semantic drift. Variants can meet distinct latency, protection, or usability needs. Govern relationships and precedence.

**Central delivery versus self-service.** Central teams can enforce shared controls but become bottlenecks. Guardrailed self-service improves throughput while requiring strong contracts, observability, and portfolio governance.

**View versus materialized view or pipeline table.** Views compute at read; managed materialization follows engine rules; pipeline tables expose full workflow control. Retrieve refresh, consistency, failure, and cost behavior.

**Temporary exception versus permanent product.** Exceptions accelerate bounded outcomes. Permanent marts need durable ownership and integration. Every temporary mart needs expiry evidence.

**Consolidation versus coexistence.** Consolidation reduces duplication but can erase legitimate context. Coexistence is justified when differences are explicit, valuable, and funded.

## Failure Modes and Misconceptions

1. **Every department needs one mart.** Product boundaries follow coherent decisions and contracts.
2. **A schema is a mart.** A mart includes consumers, semantics, service, controls, ownership, and lifecycle.
3. **Independent marts are faster overall.** They shift integration, correction, and governance costs locally.
4. **Dependent marts inherit correctness automatically.** Transformations and refresh can violate upstream contracts.
5. **Shared names mean conformance.** Identity, meaning, time, codes, and populations must align.
6. **Facts can be joined through any shared dimension.** Nonunique raw facts can multiply one another.
7. **An aggregate supports every detail question.** Discarded grain and dimensions cannot be recovered.
8. **A logical mart is free.** Runtime load, latency, failure, and policy remain.
9. **A physical mart is stale by definition.** Freshness depends on source-to-consumer boundaries and maintenance.
10. **One metric must have one universal context.** Legitimate contexts can differ when clearly named and related.
11. **Dashboard formulas are a semantic layer.** Private expressions lack governed ownership and reuse.
12. **Sandboxes can quietly become production.** Product use requires promotion evidence.
13. **Fast queries prove mart value.** Correct decisions, service, protection, and cost matter.
14. **No observed queries means no consumers.** Extracts, caches, schedules, APIs, and manual workflows may remain.
15. **Cloud schemas eliminate mart proliferation.** Cheap creation can increase copies and ambiguity.
16. **Dual running is a safe steady state.** Divergence and unclear authority grow over time.
17. **Dropping tables retires a mart.** Jobs, extracts, credentials, consumers, metadata, and obligations remain.

## Worked Examples

### Example 1

A Finance close mart derives from governed Orders, Billing, Ledger, Currency, and Calendar products, then applies Finance-owned recognition rules. **Conclusion:** a dependent mart can own consumer semantics without replacing source authority.

### Example 2

An acquired business creates an independent regulatory mart because central ingestion cannot enter its jurisdiction. The exception has local controls, reconciliation, a permanent ownership decision, and no vague convergence promise. **Conclusion:** independence can be an explicit architecture, not merely debt.

### Example 3

A logical Customer Support mart filters governed interaction tables and masks payment fields. Runtime benchmarks meet the modest workload, so no new persistent copy is justified. **Conclusion:** serving contracts do not always require materialization.

### Example 4

Sales and Returns facts share conformed Region but differ in grain. Raw joining inflates revenue; independent aggregation followed by a regional join produces valid comparison. **Conclusion:** drill across preserves fact grains.

### Example 5

A daily aggregate mart accelerates store-category reporting by 40 times but cannot answer transaction-level fraud questions. Its catalog states supported grain and links to atomic authority. **Conclusion:** optimization boundaries must be visible.

### Example 6

Two churn marts use the same name but one measures voluntary cancellation within 30 days and another all inactivity over 90 days. They are renamed, related to distinct decisions, and not forcibly averaged. **Conclusion:** consistency begins with truthful distinction.

### Example 7

A sandbox segmentation table gains three automated consumers. Promotion pauses use until ownership, training cutoff, protected attributes, refresh, tests, service, and deletion are governed. **Conclusion:** runtime dependency is evidence that exploration became a product candidate.

### Example 8

Five marts refresh simultaneously from the same operational replica, causing lag and retries. Shared source budgets, staggered dependent refreshes, and reusable upstream products contain the load. **Conclusion:** mart autonomy must include system-wide capacity.

### Example 9

A portfolio review finds three identical inventory marts, one low-latency protected variant, and an unused extract. The duplicates consolidate, the justified variant remains, and the extract is retired. **Conclusion:** overlap is evaluated by contracts and value, not count alone.

### Example 10

A migration moves dashboard cohorts to a new mart, revokes old credentials, stops refreshes, deletes eligible data and extracts, updates catalogs and lineage, and verifies scheduled reports no longer depend on it. **Conclusion:** consumer closure completes retirement.

## Cross-Program Connections

- **Data engineering:** modeling, transformations, tests, materialization, orchestration, freshness, serving, and backfills implement marts.
- **Database engineering:** views, materialized views, indexes, partitions, transactions, query plans, concurrency, and recovery shape physical forms.
- **Distributed systems:** snapshots, clocks, retries, consistency, caches, replication, partial failure, and convergence shape releases and copies.
- **API and service engineering:** contracts, versions, identity, quotas, errors, compatibility, and deprecation govern programmatic mart access.
- **Platform engineering:** self-service, paved paths, tenancy, workload isolation, catalogs, observability, capacity, cost, and support enable portfolios.
- **Cybersecurity and privacy:** purpose, minimization, derived sensitivity, row and field policy, retention, deletion, egress, and audit constrain marts.
- **Economics and operations research:** materialization value, shared capacity, opportunity cost, portfolio optimization, and retirement inform decisions.
- **Systems engineering:** stakeholder needs, interface control, verification, configuration baselines, assurance, migration, and closure structure governance.

## References

1. Kimball Group, *Kimball Data Warehouse Bus Architecture*. <https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/kimball-data-warehouse-bus-architecture/>
2. Kimball Group, *Conformed Dimensions*. <https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/conformed-dimension/>
3. Kimball Group, *Four-Step Dimensional Design Process*. <https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/four-4-step-design-process/>
4. Microsoft, *Understand Star Schema and the Importance for Power BI*. <https://learn.microsoft.com/en-us/power-bi/guidance/star-schema>
5. W3C, *The RDF Data Cube Vocabulary*, W3C Recommendation, 2014. <https://www.w3.org/TR/vocab-data-cube/>
6. PostgreSQL Global Development Group, *Materialized Views*. <https://www.postgresql.org/docs/current/rules-materializedviews.html>
7. Beyer, B., Jones, C., Petoff, J., and Murphy, N. R., eds., *Site Reliability Engineering: Addressing Cascading Failures*, Google, 2016. <https://sre.google/sre-book/addressing-cascading-failures/>
8. NIST, *Systems Security Engineering: Considerations for a Multidisciplinary Approach in the Engineering of Trustworthy Secure Systems*, SP 800-160 Volume 1 Revision 1, 2022. <https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final>

## Exercises

### Exercise 1

Design a mart strategy for Sales, Returns, Inventory, and Finance consumers. Identify dependent, independent, logical, physical, aggregate, and consumer-aligned choices with justification.

### Exercise 2

Define a conformance and drill-across contract for Sales and Returns facts across Region, Product, Customer, Currency, and Calendar.

### Exercise 3

Create a mart portfolio review method that detects harmful overlap, unknown consumers, stale products, semantic divergence, protection gaps, and retirement candidates.

### Exercise 4

Design a sandbox promotion path for an exploratory customer-risk model that now serves an automated decision workflow.

### Exercise 5

Plan consolidation of twelve independent marts into governed upstream products and fewer consumer marts without breaking reports, histories, or legitimate local contexts.

## Answers to the Exercises

### Answer 1

Define decisions and consumers first. A dependent Sales mart can derive order-line facts and conformed Customer, Product, Region, and Calendar from governed upstream products. A dependent Returns mart keeps return-event grain and shares compatible dimensions. Inventory may use a physical snapshot mart for predictable store-category service and a logical detail view for investigation. Finance owns a consumer-aligned close mart with recognition, currency, materiality, period, and restatement rules.

An acquired jurisdiction may justify an independent mart when data cannot enter the central platform; assign full source integration, protection, quality, correction, and lifecycle responsibility plus an explicit permanence review. Use aggregates for stable executive workloads while retaining atomic lineage. Record every mart's authoritative inputs, grain, time, measures, release, consumers, service, protection, owner, cost, and retirement. Do not create one mart merely because each department requested a namespace.

### Answer 2

Declare Sales at accepted order-line grain and Returns at return-event grain. Define stable Region, Product, and Customer identities; unknown and merged members; hierarchy versions; effective intervals; and compatible subsets. Define sales revenue and refund amounts with currency, tax, sign, unit, recognition, status, cancellation, and correction rules. Align transaction, business-effective, observation, and release time, plus fiscal and civil calendars.

Each mart publishes pinned upstream and mart releases, quality, unresolved dimension rates, and accepted skew. Aggregate Sales and Returns independently by the requested conformed dimension members and periods, then join summaries. Never join raw facts on Region, Product, or Customer alone. Test row uniqueness, dimension coverage, currency conversion version, late facts, historical hierarchy, missing members, zero activity, reversals, and reconciliation to each authority. Publish limitations when a dimension or period is not compatible.

### Answer 3

Inventory mart ID, purpose, owner, consumers, observed queries and extracts, sources, grain, measures, dimensions, time, releases, platform, physical copies, service, quality, lineage, protection, cost, incidents, age, lifecycle, and declared successor. Cluster by overlapping processes, sources, assertions, consumers, and physical data. Compare semantics and service before calling two marts duplicates.

Flag conflicting owners or definitions for the same assertion, unexplained independent integration, unknown consumers, missing releases, stale quality or catalog metadata, expired sandboxes, broad access, unresolved deletion, synchronized refresh load, high cost with low outcome evidence, and absent support. Retain variants justified by latency, protection, jurisdiction, history, or usability. Consolidate only with target contracts, consumer validation, migration, rollback, and preservation of legitimate contexts. Retire through job, data, access, extract, cache, catalog, alert, and consumer closure.

### Answer 4

Freeze and inventory the exploratory model's sources, feature meanings, labels, training cutoff, code, parameters, environment, results, owner, automated consumers, decision consequence, protected attributes, temporary copies, and known limitations. Stop uncontrolled dependency growth. Assign product and domain semantic owners, validate purpose and authorization, minimize features, test leakage and bias within the relevant governance scope, and define correction and appeal where decisions affect people.

Rebuild on governed upstream releases with stable identities, point-in-time feature contracts, reproducible training evidence, quality and drift tests, lineage, versioned outputs, service objectives, access and egress controls, monitoring, incident response, recovery, support, and deprecation. Compare the promoted product with the exploratory baseline and actual decision outcomes. Migrate consumers under an explicit release and rollback. Expire sandbox credentials, data, jobs, and exports after preserving required evidence.

### Answer 5

Discover all sources, mart tables, views, transformations, facts, dimensions, metrics, histories, releases, schedules, reports, extracts, APIs, notebooks, models, credentials, owners, consumers, policies, costs, and runtime use. Classify authoritative meanings, legitimate variants, duplications, unknown dependencies, protection constraints, and required history. Define governed source-aligned and aggregate upstream products plus a conformance matrix.

Choose vertical consumer cohorts. Build target dependent or logical marts, preserve context-specific consumer semantics, and pin equivalent releases. Compare keys, measures, dimensions, effective histories, corrections, quality, performance, access, and actual decisions; document justified differences rather than forcing byte equality. Name authority, rollback, and reconciliation during bounded coexistence. After cohort acceptance, stop old refreshes and routes, revoke credentials, remove marts, views, extracts, caches, jobs, alerts, catalogs, and infrastructure, preserve required evidence and holds, and verify no consumer remains.
