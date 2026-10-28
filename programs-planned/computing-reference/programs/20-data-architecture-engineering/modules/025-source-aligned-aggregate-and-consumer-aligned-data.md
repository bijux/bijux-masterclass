---
module_id: DARCH-025
program: Data Architecture Engineering
level: 1
module_number: 25
title: Source-Aligned, Aggregate, and Consumer-Aligned Data
status: complete
last_verified: 2026-09-03
---

# Source-Aligned, Aggregate, and Consumer-Aligned Data

## One-Page Review

### Governing question

How can architects distinguish source-aligned, aggregate, and consumer-aligned data products by their semantic authority, transformations, intended decisions, quality obligations, and lifecycle so reuse increases without disguising derivation as source truth or multiplying uncontrolled extracts?

### Essential definitions

- A **data product** is a governed, discoverable, supported data offering with a defined purpose, semantic contract, interfaces, quality commitments, ownership, protection, evidence, and lifecycle.
- A **source-aligned product** publishes authoritative domain assertions close to the process that creates or validates them while insulating consumers from operational implementation details.
- An **aggregate product** combines, reconciles, summarizes, or derives information from multiple assertions or products for a reusable cross-domain purpose.
- A **consumer-aligned product** shapes data for a named consumer class, decision, workflow, model, report, or experience and owns the fitness and interpretation of that representation.
- **Alignment** identifies the locus of semantic responsibility and intended use; it is not determined solely by database, team, pipeline stage, or file format.
- **Authoritative assertion** is the accepted claim for a subject, predicate, context, jurisdiction, and effective time under declared evidence and authority.
- **Derivation** is a transformation whose result depends on inputs, rules, parameters, versions, and execution context.
- **Semantic distance** is the degree to which a product's concepts and claims depart from authoritative source assertions through integration, interpretation, aggregation, inference, or presentation.
- **Product contract** is the reviewable agreement covering meaning, identifiers, grain, time, schema, quality, service, change, protection, support, and use limitations.
- **Fitness for use** is the degree to which data characteristics satisfy the requirements of a declared use; it cannot be proven independently of consumer context.

### Central model, mechanism, or theorem

Represent a product as:

`P = (purpose, alignment, assertions, authoritative_inputs, transformations, semantic_contract, interfaces, quality, provenance, ownership, policies, lifecycle)`

Classify alignment from the product's responsibility: source-aligned products preserve and publish bounded domain assertions; aggregate products own reconciliation or derivation across inputs; consumer-aligned products own a representation for specified decisions or workflows. Each product must expose provenance, semantic distance, limitations, and change effects. No alignment is inherently more truthful or valuable than another, and every derived product remains accountable for its own claims.

### Critical invariants

- Product alignment is declared from semantic responsibility and purpose, not inferred from a bronze/silver/gold layer, storage system, or team name.
- Source-aligned products expose authoritative assertions without leaking operational schemas as permanent enterprise contracts.
- Aggregate products preserve input provenance, reconciliation rules, grain, time semantics, transformation versions, and unresolved conflicts.
- Consumer-aligned products name intended decisions, users, fitness criteria, interpretation limits, and downstream responsibilities.
- Every product owns its contract, quality evidence, service behavior, change process, support, protection, and retirement regardless of alignment.
- Derived values never silently overwrite source assertions; corrections propagate through explicit lineage and recomputation policy.
- Shared aggregates have explicit reuse criteria and do not become accidental universal truth merely because many consumers depend on them.
- Consumer convenience does not remove security, privacy, purpose, retention, records, licensing, ethical, or contractual constraints.
- Product dependencies are versioned and observable; failures, delays, incompatibilities, and corrections have bounded propagation and communication.
- Redundant products are justified by distinct semantics, service, protection, jurisdiction, or consumer needs and otherwise converge or retire.

### Common failures

Common failures are wrapping an operational table and calling it source-aligned; treating the first warehouse layer as authoritative; labeling every join an aggregate product; publishing enterprise metrics without reconciliation policy; constructing “Customer 360” with no predicate-level source authority; letting dashboards define business semantics privately; denormalizing for consumers without change ownership; stripping provenance after materialization; presenting model features as observed facts; treating popularity as truth; forcing all consumers onto one canonical aggregate; copying sensitive data into convenience marts; chaining products with no dependency objectives; and retaining abandoned extracts after their decision purpose ends.

### Compact example

An Order source-aligned product publishes accepted order assertions using stable business keys, event and correction semantics, and a contract independent of the transactional schema. A Revenue aggregate product combines orders, refunds, fulfillment, tax, and accounting adjustments under documented recognition rules, currencies, grains, periods, and reconciliation evidence. A Sales Forecast consumer-aligned product reshapes those measures with pipeline features and scenarios for regional planning, explicitly distinguishing observations from predictions. Each has a separate owner, quality objectives, protection rules, provenance, service expectations, change path, and retirement decision.

### Connections

[DARCH-021](021-business-capabilities-and-data-domains.md) and [DARCH-022](022-domain-boundaries.md) establish domain candidates and boundaries. [DARCH-023](023-data-ownership-and-accountability.md) and [DARCH-024](024-stewardship-roles.md) assign accountable and operational roles. This module establishes product-alignment choices before [DARCH-026](../ROADMAP.md) develops product service expectations and [DARCH-027](../ROADMAP.md) formalizes producer-consumer contracts.

## Governing Question

Data moves through sources, transformations, aggregates, features, reports, and applications. Naming these layers does not answer which claims are authoritative, which are derived, which decision they serve, or who must correct them. A raw copy can already be semantically distant if it omits source context; a heavily transformed product can be highly trustworthy for a declared decision.

The architectural problem is to create useful products at several alignments without building either extreme: a centralized universal model that cannot represent legitimate contexts, or thousands of private extracts whose semantics and risks are invisible. The solution begins by declaring the kind of responsibility each product accepts.

## Why This Matters

Source processes know how facts are created, but their schemas optimize transactions, vendor applications, or local workflows. Consumers need stable meaning, history, quality, and interfaces. Source-aligned products bridge this gap by publishing domain assertions as products rather than exposing operational internals.

Cross-domain decisions require reconciliation. Revenue, customer experience, supply availability, fraud, and regulatory reporting combine assertions governed by different domains and clocks. Aggregate products make those derivations explicit and reusable. Without them, each consumer independently reproduces joins and disagreements.

Decisions also need purpose-shaped data. A forecasting model, executive report, real-time intervention, and statutory return may require different grain, latency, history, features, and controls. Consumer-aligned products can meet those needs without pretending their representation is universal.

Zhamak Dehghani's [Data Mesh Principles and Logical Architecture](https://martinfowler.com/articles/data-mesh-principles.html) describes domain-oriented ownership, data as a product, self-serve infrastructure, and federated computational governance. This module uses those ideas as an architectural influence, not as proof that one topology fits every organization.

W3C [DCAT 3](https://www.w3.org/TR/vocab-dcat-3/) provides vocabulary for describing datasets, data services, distributions, catalogs, and relationships. It supports discovery and exchange while leaving domain authority, fitness, and product operating choices to adopters.

W3C [PROV-O](https://www.w3.org/TR/prov-o/) represents entities, activities, agents, and derivation relationships. W3C's [Data Quality Vocabulary](https://www.w3.org/TR/vocab-dqv/) supports expressing data-quality information, and [Data on the Web Best Practices](https://www.w3.org/TR/dwbp/) addresses publication, metadata, provenance, quality, versioning, and reuse. Together they reinforce that reusable data needs context and evidence, not only access.

[ISO/IEC 25012:2008](https://www.iso.org/standard/35736.html) defines a general data-quality model, while [ISO/IEC 25024:2015](https://www.iso.org/standard/35749.html) defines measures for data quality. Product teams must specialize general characteristics and measures for declared populations, decisions, and consequences.

The NIST [Privacy Framework 1.0](https://www.nist.gov/privacy-framework/privacy-framework) provides a risk-based structure for privacy activities. Product alignment changes neither legal facts nor ethical obligations; reuse and convenience can increase exposure, linkability, inference, and purpose risk.

## Prerequisites and Retrieval

You should understand domains, bounded contexts, source authority, entities, business keys, events, temporal models, schemas, data quality, lineage, provenance, privacy, security, service objectives, contracts, and lifecycle.

Retrieve source-aligned, aggregate, consumer-aligned, data product, source system, system of record, authoritative assertion, operational schema, publication model, semantic contract, grain, measure, dimension, reconciliation, derivation, feature, mart, view, materialization, lineage, provenance, quality, service, purpose, correction, version, replay, and retirement.

As a retrieval test, inspect a table named `gold.customer_360`. Ask which claims it makes; which sources are authoritative for each predicate; how identities reconcile; what grain and time mean; which values are observed, derived, or inferred; which consumers and decisions it supports; what quality is promised; how correction propagates; and who owns change. The word `gold` establishes none of these.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish source-aligned, aggregate, and consumer-aligned products by semantic responsibility and declared purpose;
2. separate operational source systems, authoritative assertions, publication models, derivations, and consumer representations;
3. classify product assertions by observation, adoption, reconciliation, aggregation, calculation, inference, and presentation;
4. design contracts for keys, grain, time, schema, quality, provenance, service, protection, change, support, and lifecycle;
5. preserve predicate-level source authority and correction semantics across product dependency graphs;
6. design aggregate products with explicit reconciliation, uncertainty, double-counting, late-data, and restatement policies;
7. design consumer-aligned products around decisions without creating undocumented marts or semantic lock-in;
8. evaluate reuse, semantic distance, coupling, cost, latency, privacy, security, licensing, and operational trade-offs;
9. govern product composition, versions, observability, failures, backfills, migrations, redundancy, and retirement;
10. select and justify an alignment using evidence rather than platform-layer naming conventions.

## Core Exposition

**Define a product before classifying it.** A data product is more than a dataset. It has users, purpose, owner, steward, semantic contract, interfaces, quality objectives, service behavior, support, protection, cost, evidence, change process, and lifecycle. It may expose tables, files, streams, events, APIs, models, metrics, or several synchronized interfaces.

A pipeline output with no owner or contract is an artifact. A catalog entry with no support or change discipline is documentation. Product treatment means consumers can discover what the offering claims, determine fitness, use it safely, report problems, and respond to change.

**Classify by semantic responsibility.** Ask where the product's meaning comes from and what promise it makes. A source-aligned product promises governed publication of domain assertions. An aggregate product promises a defined reconciliation or derivation across inputs. A consumer-aligned product promises fitness for a specified decision context.

Implementation cannot decide alignment. All three types can live in a warehouse, lake, stream, API, or application store. All can contain transformations. The important question is which semantics the product owns and which it inherits.

**Separate source systems from source-aligned products.** An operational application processes commands and supports a workflow. Its physical tables reflect transaction boundaries, performance, vendor design, and deployment history. Direct exposure couples consumers to concerns they do not own.

A source-aligned product publishes stable business assertions from that domain. It may rename fields, join normalized tables, decode statuses, validate constraints, preserve history, tokenize identifiers, remove operational fields, and expose event semantics. These transformations can reduce implementation coupling while retaining domain alignment.

**Define authoritative scope by predicate.** One system rarely owns an entire entity. Commerce may be authoritative for order acceptance, fulfillment for shipment, finance for settlement, and support for contact preference. Authority can vary by jurisdiction, process, evidence, and effective time.

Source-aligned contracts should state subject, predicate, source process, authority basis, validity, correction, and limitations. A “Customer source product” that merges every assertion without this scope may already be an aggregate, regardless of its source-layer label.

**Preserve business keys and identity evidence.** A source-aligned product exposes durable identifiers or documented matching evidence. Internal row IDs and changeable vendor keys should not become enterprise identity by accident. When identifiers rotate or merge, publish mappings and effective intervals.

Identity resolution across sources is a derivation with rules, confidence, survivorship, exceptions, and review. A mastered Party product is often aggregate-aligned because it owns reconciliation, even when the team calls it a source of truth.

**Publish time explicitly.** Distinguish event time, business-effective time, source-record time, ingestion time, processing time, publication time, and correction time. State whether records are current snapshots, append-only events, bitemporal histories, or restatable facts.

A source-aligned product should represent source corrections faithfully. It must not pretend the source always knew the corrected value. Consumers need enough temporal semantics to reconstruct what happened, what was believed, and when the publication changed.

**Own the publication contract.** Source alignment does not mean zero transformation or zero responsibility. The product team owns interface stability, publication delay, completeness, duplicate handling, schema evolution, documentation, access, incident communication, and deprecation.

When the operational source changes, the product absorbs compatible implementation variation where possible. Breaking semantic changes require a product version and consumer migration, even if the source team considers them routine application releases.

**Identify aggregate products.** An aggregate product combines or derives information under a reusable semantic purpose. It may reconcile customers, calculate recognized revenue, build an inventory position, construct a supply forecast, or publish enterprise risk exposure.

Aggregation here is broader than a SQL `GROUP BY`. Joins, survivorship, harmonization, unit conversion, currency conversion, classification, imputation, enrichment, calculation, and inference can all create aggregate-aligned responsibility.

**Name the owned derivation.** An aggregate contract specifies inputs, versions, authority, mappings, transformations, parameters, grain, dimensions, measures, time, exclusions, uncertainty, lineage, and validation. It owns the correctness of that defined derivation, not the correctness of every source assertion.

If source evidence conflicts, the aggregate must not silently select a preferred value. Publish a resolution rule, retain conflict evidence, expose uncertainty where relevant, and route source correction. Survivorship is a business decision, not merely a deduplication technique.

**Control grain and double counting.** Every fact has a grain: one order line, shipment event, account-day, customer-month, or claim version. Joins across mismatched grains can multiply amounts while producing plausible totals.

Aggregate products declare grain before measures. They test uniqueness and join cardinality, distinguish additive, semi-additive, and non-additive measures, and define snapshot versus flow behavior. Reconciliation connects product totals to input populations and accepted exclusions.

**Define time and restatement.** Aggregates depend on late events, corrections, exchange rates, reference versions, closing periods, and policy changes. State whether a published period is provisional, final, restatable, or frozen, and who may reopen it.

Version transformation logic and parameters. A backfill should preserve execution evidence and affected consumers. If historical results change, communicate whether the cause was source correction, model change, policy change, or defect repair.

**Treat enterprise metrics as products.** A metric requires name, purpose, formula, grain, population, dimensions, units, calendar, source inputs, exclusions, owner, steward, quality, latency, version, and interpretation. A dashboard expression is not enterprise semantics.

A reusable Revenue product can serve many consumers if their recognition concepts align. If regulatory, management, and operational revenue legitimately differ, publish linked scoped measures rather than forcing a false universal number.

**Identify consumer-aligned products.** A consumer-aligned product organizes data for a named class of decisions or workflows: fraud investigation, demand planning, customer support, model training, experimentation, regulatory reporting, or board oversight.

It may filter, denormalize, pivot, feature-engineer, precompute, label, summarize, or combine products. These choices are acceptable when the product owns their meaning, limitations, change, protection, support, and retirement.

**Name the decision context.** “Analytics mart” is too broad. State users, decisions, frequency, consequence, accepted uncertainty, latency, history, dimensions, access mode, and interpretation limits. Fitness depends on this context.

A churn-feature product may be fit for monthly retention prioritization but not credit decisions, real-time intervention, or causal claims. The contract should make such exclusions prominent and enforceable where possible.

**Separate observation from inference.** Consumer-aligned products often include predictions, scores, clusters, labels, imputations, and scenarios. Mark each value's nature, model and feature versions, training or calibration period, confidence or uncertainty, monitoring status, and permitted uses.

An inferred household or predicted income is not a source-observed fact. Downstream products must preserve that distinction. Source correction does not automatically correct a model output without recomputation and validation.

**Avoid the private-mart trap.** Consumer alignment is not permission for undocumented copies. A viable product has ownership, discovery, contract, provenance, protection, quality, support, change control, cost visibility, and lifecycle. Personal exploratory work can remain provisional, but promotion to shared decision use triggers product obligations.

Repeated private marts can reveal a missing source or aggregate capability. Analyze common logic and needs. Promote a reusable product when semantics truly align; do not centralize merely because expressions look syntactically similar.

**Model semantic distance.** Source-aligned products usually have low distance from domain assertions, but even publication choices introduce interpretation. Aggregate products add reconciliation and derivation. Consumer-aligned products add decision-specific shaping. Distance is not bad; hidden distance is.

Record transformation classes, semantic changes, inferred values, loss of detail, exclusions, uncertainty, and reversibility. Greater distance generally demands stronger provenance, validation, explanation, and use constraints.

**Preserve provenance through composition.** Product provenance connects output assertions to input product versions, transformations, agents, parameters, execution, and time. Technical lineage alone may not explain why a reconciliation rule was chosen or which authority approved it.

Capture machine-readable edges where practical and link them to semantic and decision records. Consumers need enough provenance to trace defects, assess fitness, reproduce material results, and understand restatements without receiving unnecessary sensitive details.

**Assign ownership at every alignment.** A source owner is accountable for published domain assertions and source-process correction within scope. An aggregate owner is accountable for reconciliation and derived claims. A consumer-product owner is accountable for fitness to the declared decision and its presentation.

These roles collaborate but cannot transfer blame indefinitely upstream. A product that knowingly applies an unsuitable source owns that selection. A source product that violates its contract owns its failure. Shared incident handling follows lineage while preserving scoped accountability.

**Design quality by product purpose.** Source-aligned products emphasize fidelity, completeness of declared source populations, validity, timeliness, correction, and stable identifiers. Aggregates emphasize input coverage, reconciliation, transformation correctness, grain, consistency, restatement, and uncertainty. Consumer products emphasize decision fitness, usability, latency, representativeness, interpretation, and outcome monitoring.

Use common quality vocabulary but specialize measures. A 99 percent completeness score has no meaning without attribute, population, time, computation, exclusions, consequence, and threshold. Publish both results and measurement provenance.

**Design service dependencies.** A consumer product depends on aggregate and source products with latency, availability, freshness, recovery, support, and change expectations. End-to-end service cannot exceed every dependency mechanically, because buffering and graceful degradation can help, but hidden dependencies make promises unreliable.

Model critical paths, failure modes, time budgets, retry and replay, stale-data behavior, fallbacks, and notification. A dashboard that renders cached values during an upstream outage must disclose their age rather than appearing current.

**Govern change across the graph.** Contracts define compatible and breaking changes, review, notice, migration, deprecation, and retirement. Compatibility includes meaning, not only schema. A field whose type stays integer but changes from gross to net amount is breaking.

Use dependency discovery and consumer registration, but assume unknown consumers may exist. Monitor use, publish versions, run contract tests, provide migration evidence, and sunset deliberately. Emergency changes require incident communication and later reconciliation.

**Propagate corrections deliberately.** A source correction identifies affected assertions and periods. Downstream products decide whether to replay, restate, disclose, or preserve prior decisions based on contract and legal or operational requirements.

Maintain correction lineage and idempotent processing where feasible. Do not overwrite all history without evidence. Consumers may need both corrected truth and the values actually used for a past decision.

**Apply protection at every product.** Aggregation and consumer shaping can increase or decrease risk. Removing direct identifiers may still leave linkable or inferential data. Combining benign sources may reveal sensitive behavior. Product purpose can exceed original collection or sharing authority.

Classify products, enforce least privilege and purpose, minimize fields and populations, govern retention, respect licensing and contracts, review cross-border or provider use, and plan incident response. Derived products inherit relevant constraints and can add new ones.

**Design for legitimate variants.** Different jurisdictions, legal entities, languages, calendars, risk appetites, latency needs, and decisions can justify variants. Make differences explicit and map shared concepts. Reuse should reduce needless duplication, not erase context.

Variants need owners and lifecycle. A local product should not silently become enterprise standard through popularity. An enterprise aggregate should not force unsafe concessions on regulated local use.

**Choose materialization deliberately.** Products can be logical views, materialized tables, streams, APIs, files, or semantic models. Logical composition reduces copies but can create runtime coupling and unpredictable cost. Materialization improves isolation and performance but adds staleness, storage, protection, and correction work.

Choose based on service, scale, failure isolation, consistency, replay, access, and cost. The interface form does not decide the product's alignment.

**Avoid layer-name architecture.** Bronze, silver, and gold can describe processing states, but organizations often attach inconsistent meanings. Raw, cleansed, conformed, and presentation have the same problem. Keep them as local implementation labels if useful.

Product contracts should state assertions, purpose, derivation, provenance, quality, and support directly. A consumer should not need to infer trust from a color or medal.

**Evaluate reuse honestly.** Reuse benefits include consistent semantics, lower duplicate effort, shared quality investment, and easier correction. Costs include coordination, broader service expectations, slower change, concentrated failure, expanded access, and pressure toward generic design.

Promote reuse when consumers share meaning and requirements. Fork when purposes or controls genuinely differ, while preserving provenance and avoiding unmanaged divergence. Revisit the choice as use and cost evolve.

**Find accidental hubs.** A product can become critical because everyone happened to copy it, not because it was designed for enterprise use. Measure dependency count, consequence, change failures, queue load, and service gaps.

Either strengthen ownership, contract, service, protection, and capacity or migrate consumers to appropriate products. Popularity without product investment creates systemic risk.

**Control circular dependencies.** Product graphs can become circular when domains consume each other's derived outputs as source truth. Cycles complicate correction, availability, replay, and semantic authority.

Identify cycles, distinguish feedback signals from authoritative inputs, delay or version feedback where necessary, and establish convergence rules. A credit decision can inform customer treatment without redefining the underlying identity assertion.

**Support discovery and evaluation.** Catalog entries should expose purpose, alignment, owner, steward, contract, interfaces, examples, provenance, quality, service, protection, cost, versions, support, consumers, limitations, and lifecycle. Search ranking must not substitute for fitness assessment.

Provide evaluation samples safely, machine-readable contracts, usage guidance, and consumer feedback. Record known limitations visibly. Consumers remain responsible for checking their context rather than assuming catalog publication is approval for any use.

**Observe products and graphs.** Monitor interface availability, freshness, volume, schema, distributions, quality rules, transformation execution, lineage coverage, consumer errors, costs, incidents, and service objectives. Link signals to product and dependency context.

Alerting needs consequence-based routing and actionable ownership. A silent stale aggregate can be worse than an unavailable one. Validate monitoring itself and record blind spots.

**Retire products and copies.** Retirement inventories consumers, dependencies, reports, models, extracts, legal holds, retention, contracts, access, and historical correction duties. Provide migration, final versions, archive policy, and support end dates.

Remove schedules, credentials, storage, catalog routing, and duplicated controls after evidence of closure. Retain enough provenance and contract history to explain past decisions. A replacement does not automatically erase the old product's obligations.

**Select alignment with evidence.** Begin with purpose and claims. Locate authoritative inputs, describe transformations, identify intended decisions, calculate semantic distance, assign ownership, define quality and service, assess risk and reuse, and trace lifecycle.

The decisive test is not where the product sits. It is whether producers and consumers can explain what it claims, why those claims are trustworthy for the declared purpose, how they derive from authority, what limits apply, who acts when they fail, and how change and retirement occur.

## Definitions and Notation

Let a data product be `P = (u, a, C, I, T, K, F, Q, V, O, R, L)`, where `u` is purpose and users, `a` alignment, `C` product assertions, `I` authoritative inputs, `T` transformations, `K` semantic contract, `F` interfaces, `Q` quality and service commitments, `V` provenance, `O` ownership and stewardship, `R` policies and restrictions, and `L` lifecycle.

Let `a ∈ {source, aggregate, consumer}` denote primary alignment. Products may have secondary characteristics, but the primary value identifies the responsibility consumers rely upon. Ambiguous alignment requires decomposition or an explicit composite contract.

For assertion `c`, define provenance `Prov(c) = (inputs, authorities, transformations, parameters, agents, execution, time, evidence)`. Let `Dist(c)` describe semantic operations such as filtering, mapping, reconciliation, aggregation, imputation, inference, or presentation. It is a structured explanation, not necessarily one numeric score.

Represent a product dependency edge as `E = (producer_version, consumer_version, contract, service, protection, change, correction)`. A graph is operationally credible only when critical edges are discoverable, monitored, and assigned.

Fitness is contextual: `Fit(P,U,t)` evaluates product `P` against use requirements `U` at time `t`. Passing one product quality threshold does not imply fitness for an undeclared use.

## Mechanisms, Invariants, or Proof Structure

Use ten gates for every material product-alignment decision.

**1. Purpose gate.** Name users, decisions, workflows, consequence, frequency, time horizon, and excluded uses.

**2. Alignment gate.** Declare source, aggregate, consumer, or justified composite responsibility from semantics rather than implementation layer.

**3. Authority gate.** Identify predicate-level authoritative inputs, adoption rules, reconciliation authority, and derived claims.

**4. Contract gate.** Specify keys, grain, time, schemas, measures, codes, interfaces, versions, examples, and limitations.

**5. Derivation gate.** Preserve transformations, parameters, mappings, uncertainty, lineage, provenance, reproducibility, and correction behavior.

**6. Quality gate.** Define purpose-specific measures, populations, thresholds, evidence, exceptions, validation, and outcome monitoring.

**7. Service gate.** Define freshness, latency, availability, recovery, support, dependency budgets, degradation, notification, and cost.

**8. Protection gate.** Apply access, purpose, minimization, privacy, security, records, licensing, jurisdiction, ethics, and incident controls.

**9. Change gate.** Govern compatibility, semantic change, versions, tests, consumers, notice, migration, backfill, restatement, and deprecation.

**10. Lifecycle gate.** Monitor ownership, adoption, redundancy, dependencies, risks, value, succession, retirement, archive, and historical duties.

The executable example checks four narrow classification failures: missing authoritative source scope, absent provenance, missing consumer context, and undeclared alignment.

<!-- bijux-verify: {"id":"product-alignment-integrity","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"products=4\nvalid=0\nfindings=churn-features:missing-consumer-context,customer-360:missing-alignment,orders-source:missing-authoritative-inputs,revenue-aggregate:missing-provenance\nready=false\n","stderr":""}} -->
```python
products = (
    {"id": "orders-source", "alignment": "source", "authoritative_inputs": False, "provenance": True, "consumer_context": True},
    {"id": "revenue-aggregate", "alignment": "aggregate", "authoritative_inputs": True, "provenance": False, "consumer_context": True},
    {"id": "churn-features", "alignment": "consumer", "authoritative_inputs": True, "provenance": True, "consumer_context": False},
    {"id": "customer-360", "alignment": "", "authoritative_inputs": True, "provenance": True, "consumer_context": True},
)

findings = []
valid = 0
for product in products:
    local = []
    if not product["alignment"]:
        local.append("missing-alignment")
    if not product["authoritative_inputs"]:
        local.append("missing-authoritative-inputs")
    if not product["provenance"]:
        local.append("missing-provenance")
    if not product["consumer_context"]:
        local.append("missing-consumer-context")
    if local:
        findings.extend(f"{product['id']}:{finding}" for finding in local)
    else:
        valid += 1

print(f"products={len(products)}")
print(f"valid={valid}")
print("findings=" + ",".join(sorted(findings)))
print(f"ready={str(valid == len(products)).lower()}")
```

The checker validates four declared product predicates only. It does not prove source authority, semantic correctness, complete provenance, transformation reproducibility, quality, service fulfillment, lawful use, protection, decision fitness, consumer adoption, cost effectiveness, or production readiness. Those require local contracts, source evidence, code and data tests, reconciliation, lineage review, operational measurements, consumer validation, risk and legal review, and accountable approval.

## Alternatives and Trade-Offs

**Direct source access versus source-aligned publication.** Direct access reduces initial work and can preserve detail, but couples consumers to operational change, access patterns, and undocumented semantics. Publication adds cost and latency while creating a stable governed interface.

**Shared aggregate versus consumer-specific derivation.** A shared product reduces duplicate logic and supports reconciliation; it can become broad, slow, and politically overloaded. Consumer products preserve focus but can duplicate rules. Share stable semantics and specialize genuine decision context.

**Canonical enterprise model versus mapped domains.** One model simplifies exchange when meaning truly aligns but can erase context and stall change. Domain models with explicit mappings preserve autonomy while increasing integration work. Use shared identifiers and concepts selectively.

**Logical view versus materialized product.** Views reduce storage and correction copies but increase runtime dependency and performance variability. Materialization isolates service and supports history but creates staleness, cost, and protection obligations.

**Detailed data versus pre-aggregation.** Detail supports new questions and audit but raises volume, exposure, and complexity. Pre-aggregation improves simplicity and minimization but loses reversibility. Match representation to declared use and preserve controlled lineage.

**One mutable product versus versioned products.** Mutation reduces catalog clutter but breaks reproducibility. Versioning preserves contracts and decisions but costs migration and support. Use compatibility rules and bounded parallel versions.

**Central product team versus domain ownership.** Central teams can standardize and scale skills but may lack source authority. Domain teams act with context but need platform support and federated controls. Assign semantics near authority and infrastructure as a shared capability.

**Maximum reuse versus bounded duplication.** Maximum reuse concentrates investment but can create systemic coupling and generic products. Bounded duplication can isolate risk and purpose at ongoing cost. Justify variants and review them for convergence or retirement.

## Failure Modes and Misconceptions

1. **Raw means authoritative.** A copy can omit context, constraints, corrections, or predicate-level authority.
2. **Source-aligned means operational schema.** A publication model should protect consumers from application implementation details.
3. **Gold means trusted.** Layer names do not establish semantics, provenance, quality, or fitness.
4. **Every join creates an aggregate product.** Product status requires owned reusable semantics, contract, service, and lifecycle.
5. **An aggregate is universal truth.** It is a governed derivation for declared purposes and rules.
6. **Customer 360 has one obvious meaning.** Identity, predicates, survivorship, context, and time require explicit authority.
7. **Consumer alignment excuses duplication.** Shared decision use still requires product discipline and redundancy review.
8. **A dashboard can own a metric privately.** Material decision semantics need discoverable definition, provenance, ownership, and change control.
9. **Derived data inherits source truth automatically.** Transformations and selection create new claims and responsibilities.
10. **Technical lineage explains meaning.** Semantic rules, authority, rationale, and limitations also matter.
11. **Schema compatibility prevents breaking change.** Stable types can carry changed meaning, grain, time, or population.
12. **Corrections should overwrite history everywhere.** Some consumers need prior decision state and restatement evidence.
13. **Popular products are fit for every use.** Adoption signals utility, not universal suitability or lawful purpose.
14. **Aggregation always reduces privacy risk.** Combinations, small groups, and inference can increase exposure.
15. **One quality score proves fitness.** Measures are contextual and must name population, method, time, and consequence.
16. **Unknown consumers prevent all change.** Discovery, monitoring, versions, notice, and bounded support enable managed evolution.
17. **A replacement permits immediate deletion.** Dependencies, retention, legal holds, reports, models, and historical support require closure.

## Worked Examples

### Example 1

An ERP order table is exposed directly to analysts. A source-aligned Order product publishes stable order keys, accepted status semantics, business-effective events, corrections, quality evidence, and a versioned schema while absorbing vendor-table changes.

### Example 2

A Customer 360 selects the most recent value for every attribute. Architects reclassify it as an aggregate product, define predicate-level authorities, survivorship, confidence, conflicts, time, and correction, and stop advertising a context-free single truth.

### Example 3

Finance combines orders, invoices, refunds, taxes, and exchange rates. The Revenue aggregate declares recognition policy, grain, calendar, rate version, exclusions, reconciliation totals, restatement, and distinct regulated and management measures.

### Example 4

A demand-planning product reshapes inventory and sales into weekly region-item features. It names forecast planning as its use, publishes feature versions and uncertainty, and prohibits interpreting scenario outputs as observed inventory.

### Example 5

A dashboard team changes a metric while retaining the same column type. Contract checks pass syntactically, but semantic review identifies a population change. The team publishes a new version, recomputes history, and explains the break.

### Example 6

A source correction changes shipment dates for a closed period. Downstream products trace affected versions; operations restates performance, finance preserves closed reporting under policy, and both retain evidence of original and corrected values.

### Example 7

Many teams copy a successful risk aggregate. Dependency analysis shows critical enterprise use beyond its staffing and service design. Leadership funds product hardening, protection review, support, recovery, and migration from uncontrolled copies.

### Example 8

A churn model uses inferred household and income fields. The feature product labels inference, model and source versions, permitted use, confidence, monitoring, and recomputation. Consumers cannot present those values as customer-supplied facts.

### Example 9

Six regions use different fiscal calendars. A global product preserves local authoritative periods and publishes mapped comparison periods with loss rules, rather than overwriting local truth with one calendar.

### Example 10

A marketing mart is replaced, but annual campaign audits depend on old segment definitions. Retirement archives contracts, code, provenance, access decisions, and final data under retention policy while migrating active consumers and revoking obsolete credentials.

## Cross-Program Connections

- **Data engineering:** ingestion, transformations, orchestration, materialization, testing, observability, backfills, and serving implement product contracts.
- **Platform engineering:** self-service interfaces, catalogs, policy enforcement, lineage, identity, cost, delivery, and service tooling support products at scale.
- **Domain-driven design:** bounded contexts, language, aggregates, events, context maps, and anti-corruption layers inform semantic alignment.
- **Product management:** user problems, value, discovery, roadmaps, support, adoption, service, cost, and retirement make data offerings products.
- **Analytics and machine learning:** metrics, features, labels, training sets, predictions, uncertainty, experiments, and reports are consumer-aligned claims requiring provenance.
- **Security and privacy:** purpose, access, minimization, linkability, inference, incidents, retention, and provider constraints travel through derivations.
- **Software engineering:** API contracts, semantic versioning, dependency graphs, compatibility, testing, incident response, and deprecation provide strong implementation analogies.
- **Systems engineering:** interfaces, configuration baselines, traceability, verification, change control, hazard propagation, and lifecycle assurance shape product graphs.

## References

1. Dehghani, Z., *Data Mesh Principles and Logical Architecture*, 2020. <https://martinfowler.com/articles/data-mesh-principles.html>
2. W3C, *Data Catalog Vocabulary (DCAT)—Version 3*, W3C Recommendation, 2024. <https://www.w3.org/TR/vocab-dcat-3/>
3. W3C, *PROV-O: The PROV Ontology*, W3C Recommendation, 2013. <https://www.w3.org/TR/prov-o/>
4. W3C, *Data on the Web Best Practices: Data Quality Vocabulary*, W3C Note, 2016. <https://www.w3.org/TR/vocab-dqv/>
5. W3C, *Data on the Web Best Practices*, W3C Recommendation, 2017. <https://www.w3.org/TR/dwbp/>
6. ISO/IEC, *25012:2008 Software engineering—Software product Quality Requirements and Evaluation (SQuaRE)—Data quality model*, 2008. <https://www.iso.org/standard/35736.html>
7. ISO/IEC, *25024:2015 Systems and software engineering—SQuaRE—Measurement of data quality*, 2015. <https://www.iso.org/standard/35749.html>
8. NIST, *Privacy Framework: A Tool for Improving Privacy through Enterprise Risk Management*, Version 1.0, 2020. <https://www.nist.gov/privacy-framework/privacy-framework>

## Exercises

### Exercise 1

Classify products for orders, recognized revenue, customer identity, churn features, inventory availability, and regulatory reporting. For each, define purpose, alignment, assertions, authoritative inputs, transformations, contract, quality, provenance, owner, and excluded uses.

### Exercise 2

Redesign direct analyst access to an operational claims database as a source-aligned product. Preserve authoritative detail while addressing keys, time, corrections, schema change, protection, quality, service, and migration.

### Exercise 3

Design a cross-domain Customer 360 aggregate that refuses false universal truth. Include predicate authority, identity resolution, conflicts, survivorship, time, provenance, uncertainty, quality, correction, access, and lifecycle.

### Exercise 4

Create a consumer-aligned feature product for fraud investigation. Define decisions, users, observed and inferred fields, latency, history, labels, fitness, protection, versions, monitoring, limitations, and feedback.

### Exercise 5

Evaluate whether three similar regional revenue marts should become one shared aggregate. Include semantic compatibility, calendars, policy, service, protection, dependencies, migration, cost, systemic risk, and justified variants.

## Answers to the Exercises

### Answer 1

Orders are source-aligned when they publish accepted order assertions from Commerce with stable keys, event and correction semantics. Recognized Revenue is aggregate-aligned because it owns reconciliation across orders, invoices, refunds, tax, fulfillment, policy, currency, and periods. Customer identity is source-aligned only if one domain has bounded authority; cross-source identity resolution is aggregate-aligned. Churn features are consumer-aligned to retention prediction and intervention, with inference and use limits. Inventory availability may be aggregate-aligned when it reconciles stock, reservations, in-transit supply, and safety rules. Regulatory reporting is consumer-aligned to a statutory decision even when it consumes reusable finance aggregates.

For each product record users and decisions, claims, predicate-level authorities, derivations, keys, grain, time, interface, quality and service objectives, provenance, protection, owner and steward, change, correction, support, and retirement. Explicitly exclude uses not validated—for example, churn features as credit evidence or management revenue as a statutory measure. Product names and platform layers do not decide the classification.

### Answer 2

The Claims domain publishes stable claim and claim-event identifiers rather than internal row keys. The contract defines accepted assertions, source process, authority, grain, status transitions, event and business-effective time, record and publication time, corrections, late events, duplicates, deletions, and history. It maps operational codes to governed meanings while preserving source detail and evidence. The interface removes internal workflow fields and minimizes protected content for declared consumers.

Quality measures cover declared-population completeness, validity, uniqueness, temporal ordering, source fidelity, and publication freshness. Service expectations state delay, availability, recovery, support, and stale behavior. Schema and semantic versions absorb compatible vendor change and provide notice and migration for breaks. Access is purpose-bound, least-privileged, logged, retained, and reviewed. Consumers migrate from direct queries through parallel validation; unknown dependencies are observed; corrections and incidents propagate through registered lineage.

### Answer 3

Define assertions before an entity-wide owner: legal identity, contact preference, billing address, service address, risk status, consent, relationship, and segment can have different authorities. Identity resolution records identifiers, evidence, matching features, thresholds, confidence, merge and split rules, human review, and effective time. Survivorship applies per predicate and context, never “latest wins” universally. Preserve conflicting assertions and their provenance where resolution is uncertain.

The product contract states purpose, grain, temporal model, authoritative inputs and versions, mappings, transformations, uncertainty, quality, service, and limitations. Corrections route upstream and trigger bounded recomputation; decision history preserves values actually used. Access accounts for linkability and newly inferred sensitivity. An aggregate owner answers for resolution logic and published claims, while source owners retain their assertions. Review expanding use, monitor false merges and splits, publish conflict measures, notify consumers of restatements, and retire mappings and identities under evidence-backed lifecycle rules.

### Answer 4

Name fraud investigators and bounded alert prioritization or case enrichment decisions; do not imply automated guilt or unrestricted enforcement. Separate observed transactions and account events from derived velocity, network features, anomaly scores, imputed values, labels, and scenarios. Record source products and versions, transformations, model and feature versions, event and processing time, history window, freshness, uncertainty, missing-data behavior, and training or calibration periods.

Fitness measures include input coverage, feature correctness, timeliness, drift, alert performance, subgroup analysis where lawful and appropriate, investigation usability, and outcome feedback. Protect identifiers, networks, investigations, access, evidence, and retention; review purpose and provider use. Version breaking semantics, preserve reproducibility, monitor dependencies and model-feature skew, and support correction and appeal paths. Product owners govern contracts and consumer outcomes; source owners correct assertions; investigators remain responsible for contextual judgment within policy.

### Answer 5

Compare recognition definitions, grain, entities, currencies, exchange-rate policy, calendars, close and restatement rules, exclusions, source authority, quality, latency, access, retention, and decision uses. Similar SQL does not establish shared semantics. If core recognition and measures align, create a reusable aggregate with explicit local dimensions, mapped periods, provenance, reconciliation, variants, and a federated change body. Keep regulated or materially different local products linked to the shared core.

Model service and failure concentration: a shared product needs capacity, recovery, regional deadlines, support, protected access, dependency observability, and change discipline. Compare duplicated engineering and inconsistency cost against migration, coordination, latency, and systemic risk. Validate in parallel, reconcile historical periods, register consumers, version contracts, and retire redundant marts only after evidence of migration and archival duties. Review variants periodically; neither forced consolidation nor permanent duplication is the default.
