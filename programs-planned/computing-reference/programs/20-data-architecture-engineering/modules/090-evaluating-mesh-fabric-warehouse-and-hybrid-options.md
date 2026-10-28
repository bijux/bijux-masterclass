---
module_id: DARCH-090
program: Data Architecture Engineering
level: 2
module_number: 90
title: Evaluating Mesh, Fabric, Warehouse, and Hybrid Options
status: complete
last_verified: 2026-09-03
---

# Evaluating Mesh, Fabric, Warehouse, and Hybrid Options

## One-Page Review

### Governing question

How should an organization choose and compose mesh, fabric, warehouse, lakehouse, and hybrid options for named outcomes and workloads without comparing labels that describe different architectural layers or turning “hybrid” into an ungoverned collection of everything?

### Essential definitions

- A **data architecture option** is a bounded combination of operating model, ownership, platform capabilities, integration, metadata, governance, storage, processing, serving, operations, migration, and closure—not a product category alone.
- **Data mesh** is a socio-technical operating model organized around domain-oriented ownership, data as a product, a self-service data platform, and federated computational governance. It does not prescribe one storage engine or topology.
- **Data fabric** is a connective capability pattern that uses metadata, integration, discovery, lineage, policy, automation, and orchestration across heterogeneous data environments. A vendor bundle is one possible implementation, not the definition.
- A **data warehouse** is an integrated analytical environment optimized for governed, repeatable, structured analysis and serving. Its centralization may concern physical data, logical models, platform control, or all three, so the boundary must be named.
- A **lakehouse** combines lake-style, directly accessible data and open or shared table formats with management and performance capabilities associated with analytical warehouses. The label does not prove transactional, governance, or workload outcomes.
- A **hybrid architecture** deliberately composes different ownership, connective, storage, processing, and serving choices for stated domains and workloads under common interfaces, policy, evidence, and lifecycle controls.
- A **baseline** is the credible no-change or minimum-change option, including existing costs, risks, obligations, and expiry—not zero cost.
- A **mandatory gate** is a noncompensable requirement whose failure disqualifies an option for a stated scenario regardless of strengths elsewhere.
- A **scenario** is a coherent workload and operating condition with users, decisions, data, load, failures, policy, service, economics, and horizon.
- A **decision criterion** is a measurable or auditable property used to discriminate among qualified options; it includes direction, scale, evidence, uncertainty, owner, and review date.
- A **Pareto frontier** contains qualified options for which no other option is at least as good on every declared criterion and strictly better on one.
- A **decision receipt** preserves the decision context, alternatives, gates, evidence, judgments, uncertainty, sensitivity, recommendation, dissent, commitments, and review triggers.
- **Reversibility** is the demonstrated ability to change placement, ownership, interface, or technology within bounded time, cost, data loss, policy, and service impact.
- **Closure** retires data copies, jobs, catalogs, policies, access paths, contracts, credentials, exceptions, recovery assets, and financial commitments while preserving required evidence.

### Central model, mechanism, or theorem

Represent an evaluation as:

`E = (U, W, D, O, P, G, Q, S, V, C, R, L)`

where `U` is users, outcomes, and decisions; `W` workloads and semantic needs; `D` domains, data, and topology; `O` ownership and operating model; `P` platform and connective capabilities; `G` governance, privacy, and security; `Q` quality and service; `S` scale, performance, and resilience; `V` evolution and interoperability; `C` economics and capacity; `R` risk, migration, reversibility, and recovery; and `L` lifecycle and closure. An option is eligible only if it passes every mandatory gate for the scenario. Among eligible options, compare evidence ranges and trade-offs, eliminate dominated alternatives, test sensitivity, and recommend a bounded portfolio with owners and review triggers.

### Critical invariants

- Outcomes, users, decisions, workloads, domains, products, capabilities, platforms, stores, interfaces, policies, evidence, options, recommendations, exceptions, and retirement states have distinct stable identities.
- Mesh, fabric, warehouse, lakehouse, and hybrid claims are decomposed by layer; a strength at one layer cannot compensate for a missing owner, policy control, workload fit, or lifecycle plan at another.
- The baseline and incremental improvements remain first-class alternatives throughout evaluation.
- Mandatory legal, security, privacy, sovereignty, correctness, recovery, and ownership constraints are gates, not low-weight criteria.
- Every criterion defines its unit or ordinal scale, direction, scenario, evidence, uncertainty, owner, and decision consequence.
- Measurements, estimates, assumptions, preferences, and unknowns remain distinguishable; a precise score cannot conceal weak evidence.
- Shared data products and platform capabilities have named producers, consumers, service expectations, costs, support, change, and retirement.
- Domain autonomy is bounded by consumer obligations and federated policy; central control is bounded by domain semantics and local accountability.
- Placement decisions are made per workload and data boundary, then checked as a portfolio for duplication, coupling, policy, skill, and cost.
- Migration and rollback preserve contracts, reconciliation, lineage, policy, recovery, and historical interpretation.
- The recommendation includes rejected alternatives, sensitivity, dissent, experiments, commitments, review triggers, and expiry.
- Closure makes retired paths nonoperable and nonrecoverable while preserving required decisions and records.

### Common failures

Common failures include treating mesh, fabric, warehouse, and lakehouse as mutually exclusive products; buying an operating model; decentralizing ownership before domains can operate products; centralizing semantics because storage is central; calling catalog installation a fabric; calling object storage a lakehouse; choosing from feature matrices before defining workloads; omitting the baseline; compensating for a legal failure with a performance score; summing ordinal ratings as precise utility; comparing vendor benchmarks as local evidence; hiding unknowns inside averages; declaring hybrid without allocation rules; duplicating every dataset into every engine; ignoring cross-domain consumers; funding build but not operation, migration, or exit; measuring platform adoption rather than consumer outcomes; and closing a service while copies, policies, credentials, or recovery paths remain.

### Compact example

Ten invented architecture candidates are classified against six mandatory gates. Four qualify; one each lacks an outcome, accountable ownership, workload fit, governance control, sufficient evidence, or a lifecycle and cost plan. The program also counts four architecture patterns, seven workload classes, four evaluation scenarios, ten decision receipts, and ten decision events. It verifies declared structure and arithmetic only—not real fitness, comparative utility, performance, cost, risk, adoption, or value.

### Connections

[DARCH-040](040-choosing-an-integration-style-from-semantics-and-latency.md), [DARCH-041](041-enterprise-data-warehouse-architecture.md), [DARCH-042](042-data-lake-architecture.md), [DARCH-043](043-lakehouse-architecture.md), [DARCH-050](050-mapping-data-workloads-to-platforms-and-serving-systems.md), [DARCH-081](081-data-mesh-principles.md), [DARCH-082](082-domain-oriented-decentralization.md), [DARCH-083](083-self-serve-data-platform-capabilities.md), [DARCH-084](084-federated-computational-governance.md), [DARCH-085](085-data-fabric-concepts.md), [DARCH-086](086-active-metadata.md), [DARCH-087](087-federated-query-and-data-virtualization.md), [DARCH-088](088-data-sharing-across-organizations.md), and [DARCH-089](089-interoperability-without-a-universal-model.md) provide the required principles, evidence, and mechanisms. [DARCH-091](../ROADMAP.md) next assesses architecture maturity.

## Governing Question

An executive request to “choose mesh or fabric” sounds like a product decision. It is usually several decisions collapsed into one sentence: who owns meaning and quality; which capabilities should be common; where data is stored and processed; how consumers discover and access it; which policies are centrally defined or locally executed; which workload gets which engine; and who pays to operate, migrate, recover, and retire the result. Mesh and warehouse can coexist because one primarily concerns an operating model and the other an analytical environment. Fabric capabilities can connect both. A lakehouse can be one physical substrate inside any of those arrangements.

The governing question is therefore not which label wins. It is which bounded composition best serves named users and decisions across credible scenarios while meeting noncompensable constraints and remaining operable through change and closure. A defensible evaluation begins with the baseline, separates layers, inventories required capabilities, produces several coherent alternatives, exposes uncertainty, tests dominance and sensitivity, and records why a portfolio is preferable to its nearest alternatives.

## Why This Matters

Zhamak Dehghani's [data mesh principles](https://martinfowler.com/articles/data-mesh-principles.html) describe four principles: domain-oriented decentralized ownership and architecture, data as a product, self-serve data infrastructure as a platform, and federated computational governance. The article also states that practices and technology vary by organization. This makes mesh an organizational and architectural design problem, not a storage purchase.

IBM's [data fabric overview](https://www.ibm.com/think/topics/data-fabric) presents a vendor perspective centered on integration, cataloging, governance, security, self-service, and metadata-driven automation across distributed environments. It also describes fabric and mesh as potentially complementary. This is useful implementation context, but a vendor definition does not prove that a bundle supplies the required capabilities or produces local outcomes.

The CIDR paper [Lakehouse: A New Generation of Open Platforms that Unify Data Warehousing and Advanced Analytics](https://www.cidrdb.org/cidr2021/papers/cidr2021_paper17.pdf) argues for directly accessible formats, first-class support for data science and machine learning, and warehouse-class management and performance. Its architectural argument and reported prototypes motivate an option; they do not transfer benchmark results, operational maturity, or cost to another organization.

Snowflake's [key concepts and architecture](https://docs.snowflake.com/en/user-guide/intro-key-concepts) describe a managed implementation with storage, independent compute clusters, and cloud services. This illustrates how an analytical platform can separate storage, compute, and control concerns. It is vendor documentation, not neutral comparative evidence, and it leaves domain ownership, product obligations, cross-platform policy, and exit to the adopter.

Apache Iceberg's [documentation](https://iceberg.apache.org/docs/latest/) describes an open table format with schema and partition evolution, snapshots, reliability mechanisms, and integrations with multiple engines. Such capabilities can reduce some coupling between stored tables and engines. They do not make semantics portable, eliminate catalog dependencies, guarantee connector parity, or remove maintenance and governance work.

Trino's [pushdown documentation](https://trino.io/docs/current/optimizer/pushdown.html) explains that predicate, projection, aggregation, join, limit, and other pushdowns depend on the connector and underlying source. It demonstrates why “query anything in place” is not one uniform capability: workload fitness depends on source semantics, connector support, network, policy, and actual plans.

OpenMetadata's [documentation](https://docs.open-metadata.org/latest/) presents catalog, discovery, lineage, quality, governance, and collaboration capabilities across services. A metadata plane can connect heterogeneous systems and responsibilities, but catalog breadth alone does not establish ownership, metadata correctness, enforcement, or consumer value.

OpenLineage's [object model](https://openlineage.io/docs/spec/object-model/) represents datasets, jobs, runs, events, namespaces, names, and extensible facets. It can support evidence across a composed architecture, provided producers emit consistent identities and facets. Instrumentation coverage is an evaluation criterion, not an automatic consequence of choosing a label.

The Bitol [Open Data Contract Standard](https://bitol-io.github.io/open-data-contract-standard/latest/) supplies machine-readable sections for schema, quality, service, roles, support, and infrastructure. Contracts help compare whether domain-owned products and central platforms can express obligations across options. Publishing a contract does not prove its assertions or operation.

W3C [Data Catalog Vocabulary 3](https://www.w3.org/TR/vocab-dcat-3/) models catalogs, datasets, distributions, data services, relationships, versions, and profiles. It shows that a shared discovery surface can describe heterogeneous access and representation instead of requiring one physical platform or universal model.

The Open Policy Agent [policy language documentation](https://www.openpolicyagent.org/docs/policy-language) describes policy decisions over structured input using Rego. Policy-as-code can make some federated controls testable and distributable. An engine still needs authoritative inputs, policy ownership, enforcement coverage, exception handling, decision evidence, and safe rollout.

The OpenTelemetry [specification](https://opentelemetry.io/docs/specs/otel/) standardizes telemetry concepts and signals across implementations. Common observability supports comparative trials and end-to-end operation, but emitted spans and metrics must be tied to user outcomes, product identities, costs, quality, and policy decisions.

NIST's [Cybersecurity Framework](https://www.nist.gov/cyberframework) provides outcome-oriented guidance for managing cybersecurity risk. It supports evaluating architecture alternatives against governed security outcomes rather than assuming centralization or decentralization is inherently safer.

NIST's [Privacy Framework](https://www.nist.gov/privacy-framework/using-privacy-framework-11) provides a risk- and outcome-oriented structure for identifying and managing privacy risk. Data movement, discovery, joining, retention, access, and domain delegation change privacy exposure differently across alternatives and require explicit assessment.

NASA's [Decision Analysis](https://www.nasa.gov/reference/6-8-decision-analysis/) describes defining criteria, identifying alternatives, selecting evaluation methods, evaluating alternatives, documenting results, and making recommendations while reducing uncertainty and assessing robustness. It provides a disciplined frame for architecture trade studies without claiming that a numeric method removes judgment.

The FinOps Foundation's [FinOps Framework](https://www.finops.org/framework/) describes collaboration among engineering, finance, business, and other personas; usage and cost understanding; value quantification; optimization; and governance. Architecture economics therefore includes allocation, unit economics, forecasting, commitments, and ownership—not just an initial price estimate.

Together, these sources support layer separation, explicit ownership, metadata and policy capabilities, workload-sensitive placement, observable contracts, security and privacy outcomes, evidence-based trade studies, and lifecycle economics. They do not identify a universal winner, validate marketing categories, prove local domain maturity, make scores objective, guarantee interoperability, transfer performance results, or establish stakeholder value. Those conclusions require locally owned scenarios, measurements, experiments, incidents, costs, adoption evidence, and outcomes.

## Prerequisites and Retrieval

You should understand domain boundaries, data products, platform products, analytical warehouses, lakes and lakehouses, metadata, catalogs, lineage, contracts, policy, privacy, security, storage and compute separation, query federation, streaming, batch processing, machine learning, transactions, semantic modeling, service objectives, capacity, distributed systems, migration, recovery, cost allocation, and architecture decisions.

Retrieve operating model, domain ownership, data product, self-service platform, federated computational governance, fabric, active metadata, catalog, contract, lineage, warehouse, lakehouse, table format, query federation, control plane, data plane, workload placement, baseline, option, gate, criterion, evidence, uncertainty, scenario, dominance, Pareto frontier, sensitivity, reversibility, decision receipt, migration, recovery, and closure.

As a retrieval test, consider a regulated enterprise with recurring financial reporting, exploratory analytics, machine-learning feature generation, operational dashboards, partner sharing, and event detection. Ask which outcomes and consumers matter; which domains own source meaning; which work requires conformed historical models; which data must remain in place; which policies must be uniformly enforced; which platform services are genuinely self-service; which connectors and table features work at the expected scale; which costs can be attributed; which failure and recovery exercises exist; which option is the baseline; and what evidence would cause the recommendation to change. “Use a hybrid mesh fabric lakehouse” answers none of those questions.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish operating-model, connective-capability, storage, processing, serving, and governance choices hidden behind architecture labels;
2. define outcome- and workload-specific scenarios with mandatory constraints, criteria, evidence, uncertainty, and review horizons;
3. inventory mesh, fabric, warehouse, lakehouse, federation, and shared-platform capabilities without equating them to products;
4. construct a credible baseline plus incremental, centralized, decentralized, and deliberately hybrid alternatives;
5. use gates, evidence ranges, dominance, Pareto frontiers, sensitivity, and experiments without false numerical precision;
6. evaluate ownership, product obligations, platform maturity, governance, interoperability, security, privacy, performance, resilience, and economics together;
7. allocate architecture patterns by workload and domain while controlling portfolio duplication and coupling;
8. specify migrations, canaries, reconciliation, rollback, recovery, and reversibility before selecting an option;
9. write decision receipts with recommendation, dissent, uncertainty, commitments, triggers, expiry, and rejected alternatives; and
10. retire obsolete data, interfaces, policies, credentials, contracts, recovery assets, and financial commitments safely.

## Core Exposition

**Begin with the decision, not the nouns.** Name the sponsor, affected users, consumer decisions, outcome, scope, authority, deadline, horizon, risk tolerance, constraints, and review trigger. “Modernize data” is not a decision statement.

**Separate the layers.** At minimum, model ownership and funding; product obligations; platform services; metadata and policy; ingestion and integration; storage; processing; serving; semantics; observation; and lifecycle. Put every claimed benefit and cost on one or more layers. This immediately reveals that mesh, fabric, warehouse, and lakehouse are neither strict substitutes nor complete architectures.

**Treat mesh as an operating-model hypothesis.** Ask whether stable domains exist, whether they can own semantic and operational obligations, whether consumers can discover and trust products, whether a self-service platform reduces cognitive load, and whether federated governance can encode globally necessary policy without recreating a central ticket queue.

**Treat fabric as a capability hypothesis.** Inventory catalog, metadata collection, lineage, contract validation, integration, policy decisions, identity, quality, orchestration, automation, observation, and lifecycle. For each, distinguish declared, demonstrated, production-ready, and broadly adopted. A product called fabric may omit critical capabilities; an organization may assemble fabric capabilities without using the label.

**Treat warehouse and lakehouse as workload-placement hypotheses.** Describe data representation, ownership, ingestion, transformation, compute isolation, concurrency, transactions, history, semantics, serving, machine-learning access, open access, governance, recovery, and cost. Centralized storage need not imply centralized meaning, and distributed ownership need not imply one store per team.

**Define hybrid as an allocation function.** State which domain, data class, workload, jurisdiction, consumer, and lifecycle state uses which operating and technical pattern. Also define the shared contracts, metadata, identity, policy, lineage, cost, and support plane. If the allocation rule is absent, “hybrid” means accidental heterogeneity.

**Model the current system honestly.** The baseline includes current people, queues, manual extracts, shadow copies, fragile jobs, undocumented semantics, incidents, commitments, delays, control gaps, and opportunity cost. It also includes working capabilities and migration risk. A new option compared with a fictional zero-cost baseline will always look attractive.

**Name workload classes.** Separate recurring governed reporting, interactive business intelligence, exploratory analysis, data science, feature generation, low-latency operational analytics, stream processing, partner exchange, archival, discovery, and regulatory evidence. Each has different latency, freshness, concurrency, semantic, mutability, privacy, recovery, and cost needs.

**Define the unit of placement.** A decision may concern a dataset, product, aggregate, stream, domain, tenant, region, query class, processing job, or consumer interface. Whole-enterprise placement is usually too coarse. Extremely granular placement creates an unmanageable portfolio. Choose a unit whose owner, contract, telemetry, cost, and lifecycle can be governed.

**Inventory semantic topology.** Identify authoritative domain models, conformed analytical models, shared reference data, mappings, aggregates, event meanings, metric definitions, and cross-domain joins. Mesh does not abolish shared semantics; a warehouse does not automatically create them; a fabric cannot infer authority from metadata frequency.

**Assess domain readiness.** Examine domain stability, owner authority, engineering capacity, semantic expertise, operational support, product management, consumer relationships, policy competence, funding, and incentives. Decentralization without these conditions exports central bottlenecks into many under-supported teams.

**Assess platform readiness.** Evaluate paved paths for publishing, contract tests, storage and compute, orchestration, catalog registration, lineage, quality, identity, policy, secrets, telemetry, cost, incident response, migration, recovery, and retirement. Self-service means a team can achieve a safe outcome with bounded cognitive load and lead time; a portal alone is not self-service.

**Assess governance topology.** List decisions that must be global, domain-local, product-specific, platform-owned, or jointly governed. Global concerns may include identity, classification, retention, audit evidence, encryption, interoperability profiles, and critical metric definitions. Federated governance distributes execution and contribution while preserving explicit authority and conformance evidence.

**Make product obligations concrete.** Each data product needs named consumers, purpose, semantics, contract, quality, service, support, access, policy, change, cost, telemetry, incident, and closure expectations. Product language without durable obligations is branding.

**Examine control and data planes separately.** A shared catalog, policy engine, identity service, lineage model, or orchestrator can centralize control while storage and compute remain distributed. Conversely, a central store can expose domain-owned products. Evaluate availability, latency, consistency, blast radius, tenancy, versioning, and recovery for both planes.

**Evaluate integration modes.** Compare copy and transform, log or event propagation, virtual or federated query, shared tables, APIs, file exchange, semantic mappings, and materialized products. State where computation runs, which semantics apply, how policy propagates, what fails, how freshness is measured, and who owns correction.

**Test federation rather than assuming it.** Capture query plans, pushdowns, bytes moved, source load, join behavior, partial failure, snapshot consistency, policy application, retries, caching, and cost for representative queries. Federation is excellent for some discovery and bounded access; it is not a universal substitute for materialization.

**Test table-format portability.** Verify every required reader and writer operation, concurrency model, schema and partition evolution, delete behavior, snapshots, maintenance, catalog, authorization, encryption, lineage, and recovery across exact engine versions. File accessibility is narrower than safe multi-engine operation.

**Evaluate warehouse fitness explicitly.** Measure recurring transformations, conformed history, concurrency, workload isolation, materialization, query performance, semantic serving, data sharing, recovery, administration, and predictable operation. Central analytical environments can provide valuable coherence even inside a domain-oriented operating model.

**Evaluate lakehouse fitness explicitly.** Measure data-science access, structured and less-structured data, direct file or table access, engine choice, batch and streaming integration, transactions, governance, maintenance, small-file behavior, catalog dependency, serving performance, and skill demands. Openness is a property with tests, not a slogan.

**Evaluate fabric capabilities individually.** For discovery, lineage, contracts, quality, policy, integration, and automation, record coverage, correctness, timeliness, interoperability, enforcement, override, failure behavior, owner, and exit. A broad capability map often reveals that the durable choice is incremental improvement rather than one replacement program.

**Create coherent alternatives.** Include the baseline; targeted repairs; strengthened warehouse with domain-owned products; shared lakehouse substrate; mesh operating model on common infrastructure; metadata and policy fabric across existing platforms; and a bounded hybrid. Each option must be internally consistent and funded through operation and closure.

**Avoid straw alternatives.** Give every serious alternative its strongest plausible governance, migration, and operating model. Do not compare a carefully designed favorite with an unmodernized caricature. Record who constructed and challenged each option.

**Use mandatory gates first.** Examples include legal location, prohibited joins, identity isolation, recovery objective, audit evidence, semantic ownership, bounded data loss, and minimum service. If evidence is absent, mark unknown or require an experiment; do not award a neutral midpoint.

**Build discriminating criteria.** A criterion should change the decision. Define its scenario, measure, direction, acceptable range, evidence source, confidence, owner, and date. Remove duplicate criteria that count the same benefit twice, such as agility, lead time, and time to data when all use one observation.

**Keep ordinal judgments ordinal.** High, medium, and low may order options but do not imply equal intervals. Adding them can create false arithmetic. If a value function is used, define how outcomes map to value, identify stakeholder ownership, expose compensation assumptions, and run sensitivity.

**Preserve ranges and distributions.** Estimate migration duration, run cost, demand, performance, staffing, and incidents as ranges with assumptions and dependencies. Correlated uncertainties should not be multiplied as independent. Prefer a decision that remains acceptable across credible ranges over one that wins at a fragile point estimate.

**Eliminate dominated options.** If option B is no worse than A on every declared criterion and better on at least one, A is dominated for that evidence state. Review whether a hidden criterion was omitted before discarding it. The remaining Pareto frontier exposes real trade-offs for accountable judgment.

**Run sensitivity by scenario.** Vary workload growth, egress, adoption, domain maturity, vendor price, regulation, recovery need, and platform staffing. Record which threshold changes the recommendation. A robust decision has wide acceptable regions or a cheap path to adapt.

**Price the whole lifecycle.** Include discovery, design, migration, dual running, licenses, compute, storage, network, catalog, observability, security, quality, support, training, domain capacity, incident response, recovery, compliance, commitments, stranded assets, and closure. Express unit economics such as cost per governed product, active consumer, successful query class, or business outcome where defensible.

**Model organizational capacity as a constraint.** Architecture consumes attention, on-call capability, product management, semantic expertise, policy work, procurement, and change leadership. A theoretically superior portfolio can fail because it creates more ownership surfaces than the organization can operate.

**Separate platform adoption from value.** Published products, catalog entries, migrated tables, and active users are leading or activity indicators. Measure reduced decision delay, fewer reconciliations, controlled risk, improved model delivery, lower incident impact, or other named outcomes. Preserve countermetrics for cost, cognitive load, duplicated data, and consumer breakage.

**Use experiments to buy information.** A trial should target a decision-changing uncertainty: cross-source join behavior, policy propagation, contract adoption, engine interoperability, recovery, product ownership, or unit cost. Define hypothesis, population, boundary, success and stop rules, duration, telemetry, adverse effects, and how the result updates the decision.

**Demand production-shaped evidence.** Use representative data volumes, distributions, skew, concurrency, access policies, network paths, failure injection, schema changes, historical replay, and actual operators. Demonstrations with synthetic tiny data establish mechanics only.

**Record provenance of claims.** Distinguish source documentation, vendor assertion, benchmark, local measurement, expert judgment, stakeholder preference, assumption, and unknown. Bind each to versions, configurations, dates, workloads, and limitations. A decision receipt should make later reinterpretation possible.

**Design interfaces before migrations.** Stabilize product contracts, metadata identities, policy decision points, lineage, and compatibility expectations so movement does not become simultaneous semantic reinvention. Preserve a consumer's decision and evidence, not only table shape.

**Migrate by bounded slices.** Select a workload or product with an owner, consumers, reversible path, and useful uncertainty reduction. Establish baseline evidence, run contract and reconciliation checks, canary consumers, observe outcomes and countermetrics, then expand only when exit criteria pass.

**Specify dual running precisely.** Define authoritative writes, replication direction, reconciliation keys, time windows, tolerances, divergence ownership, consumer routing, rollback point, and end date. Indefinite dual systems double ambiguity and cost.

**Design rollback as an architecture.** Preserve compatible inputs, state transfer, policy, credentials, contracts, reference data, capacity, operator procedures, and reconciliation. A configuration toggle is not rollback if data or semantics cannot return safely.

**Exercise recovery across the portfolio.** Restore catalogs, policy bundles, identity relationships, metadata, lineage, table state, orchestrators, product interfaces, secrets, and cost controls in dependency order. Validate that recovered data is current, authorized, semantically interpretable, and not resurrecting retired paths.

**Make reversibility measurable.** State maximum exit time, data extraction and validation, interface portability, metadata export, policy translation, skill transfer, commitment exposure, consumer migration, and permitted loss. Open formats improve one dimension; they do not guarantee operational exit.

**Govern exceptions as expiring decisions.** An option may need a legacy store, manual control, central product, or nonstandard interface temporarily. Record scope, owner, risk, compensating control, evidence, expiry, review, migration target, and recovery behavior. Do not let “hybrid” hide permanent exceptions.

**Review portfolio interactions.** Independently good placements can collectively overload the catalog, create inconsistent policy, duplicate sensitive data, fragment skills, saturate networks, or multiply contracts. Evaluate common failure, dependency, cost, semantic, and ownership topology after local placement.

**Write the recommendation as an allocation.** State which operating model, capabilities, stores, engines, and interfaces apply to each bounded class; which are explicitly excluded; what is common; who owns each surface; which experiments remain; how migration proceeds; and what triggers reconsideration.

**Preserve dissent and uncertainty.** Record material objections, disputed evidence, unrepresented stakeholders, irreducible uncertainty, and the consequence if a minority view is correct. Consensus is not proof and suppressed disagreement is lost risk information.

**Time-bound the decision.** Architecture fitness changes with workloads, people, regulation, products, prices, and technology. Define scheduled review and event triggers such as a price threshold, consumer growth, policy change, repeated incident, domain readiness, connector capability, or failed recovery exercise.

**Close what the portfolio replaces.** Drain consumers, stop writers and readers, reconcile state, expire caches and shares, revoke access, remove jobs and catalog routes, terminate commitments, resolve quarantines, preserve required lineage and decisions, and test that recovery cannot reactivate obsolete architecture.

## Definitions and Notation

Let an evaluation be `E = (U, W, D, O, P, G, Q, S, V, C, R, L)` with the components defined in the review. Let `A = {a_0, ..., a_n}` be alternatives, including baseline `a_0`. Let `Z = {z_1, ..., z_k}` be scenarios, `H_z` the mandatory gates for scenario `z`, and `K_z` its discriminating criteria.

Define gate result `h(a, z)` as `pass`, `fail`, or `unknown`. Eligibility is:

`Eligible(a, z) iff every h in H_z is pass`

An unknown is not a pass. It may justify a bounded experiment, a conservative decision, or rejection depending on consequence and information value.

For criterion `k`, represent evidence as `x(a, z, k) = (range, unit, direction, method, configuration, confidence, date, owner)`. Do not compare values whose scope, units, method, or direction differ. An ordinal rating remains ordinal unless an explicit, reviewed value function maps it to utility.

For two eligible options, `b` dominates `a` in scenario `z` when `b` is at least as good on every criterion in `K_z` and strictly better on at least one, under declared uncertainty rules. The Pareto frontier is the set of eligible, nondominated alternatives. Overlapping uncertain ranges may make dominance indeterminate.

Let `Alloc(d, w, z) -> (o, p, g, s)` assign a domain or data boundary `d` and workload `w` in scenario `z` to an operating model, platform and connective capabilities, governance execution, and storage or serving design. A hybrid is governed only when this function and its exceptions are explicit.

Represent lifecycle cost as a range rather than one scalar:

`C_life = C_discovery + C_build + C_migrate + C_dual + C_run + C_change + C_incident + C_recover + C_exit`

This identity prevents license or compute price from masquerading as total economics. It does not imply components are independent or exactly measurable.

Define a decision receipt as `DR = (id, context, alternatives, gates, criteria, evidence, assumptions, uncertainty, analysis, recommendation, dissent, commitments, triggers, expiry)`. A new evidence state produces a new receipt linked to the prior one; it does not silently overwrite history.

Define `Reversible(a, t, c, l, p, s)` to mean option `a` can exit or change within bounded time `t`, cost `c`, permitted loss `l`, policy conditions `p`, and service impact `s`, as demonstrated by evidence appropriate to the risk.

Define `Closed(a)` to require no live or recoverable job, copy, interface, product, catalog route, policy, credential, exception, commitment, cache, quarantine, or recovery configuration can reactivate retired parts of `a`, while required records remain controlled.

## Mechanisms, Invariants, or Proof Structure

Use the following assurance gates.

**Decision gate.** Name authority, users, decisions, outcomes, scope, horizon, risk tolerance, deadline, success, countermetrics, and review triggers.

**Layer gate.** Decompose every option into operating model, ownership, product, platform, metadata, integration, governance, storage, processing, serving, observation, economics, and lifecycle.

**Baseline gate.** Preserve the credible no-change and minimum-change choices with current strengths, debts, incidents, commitments, controls, costs, and expiry.

**Workload gate.** Bind data, semantics, volume, skew, freshness, latency, concurrency, consistency, mutability, query, machine-learning, sharing, policy, service, and history requirements.

**Ownership gate.** Verify authority, domain readiness, consumer obligations, platform responsibilities, funding, incentives, support, change, incident, and closure.

**Capability gate.** Map required capabilities to demonstrated services, interfaces, versions, operators, adoption, evidence, failure behavior, portability, and gaps.

**Governance gate.** Allocate global, federated, platform, domain, product, and consumer decisions with policies, enforcement, exceptions, evidence, and appeal.

**Security and privacy gate.** Evaluate identity, authorization, isolation, classification, purpose, minimization, movement, joining, retention, sovereignty, audit, response, and recovery.

**Interoperability gate.** Test contracts, schemas, semantics, identities, mappings, connectors, table operations, query behavior, policy propagation, lineage, versions, and exit.

**Service gate.** Measure quality, freshness, latency, availability, capacity, recovery, support, dependency, consumer impact, and error budgets for exact workloads.

**Economics gate.** Include lifecycle costs, allocation, unit economics, commitments, demand ranges, staffing, opportunity cost, stranded assets, and closure.

**Evidence gate.** Distinguish documentation, assertion, benchmark, local measurement, experiment, incident, judgment, preference, assumption, and unknown.

**Trade-off gate.** Apply mandatory constraints, compare compatible evidence, expose ordinal judgments, remove duplicated criteria, identify dominance, and test sensitivity.

**Portfolio gate.** Reassess local placements for shared failures, duplication, network, policy, semantic, catalog, skill, support, and cost interactions.

**Migration gate.** Specify bounded slices, contracts, authority, lineage, policy, canaries, reconciliation, dual running, stop rules, rollback, and consumer outcomes.

**Recovery gate.** Exercise dependency-ordered restoration, current authorization, semantic interpretation, reconciliation, recovery objectives, and nonactivation of retired paths.

**Decision-receipt gate.** Preserve context, alternatives, evidence, limitations, analysis, recommendation, dissent, commitments, experiments, owners, triggers, and expiry.

**Closure gate.** Remove live and recoverable data, jobs, routes, access, contracts, caches, exceptions, commitments, and obsolete operational knowledge while retaining required evidence.

### Executable evidence: architecture-candidate gating

The following program classifies ten invented architecture candidates against six mandatory gates. These gates are intentionally noncompensable; there is no total score.

<!-- bijux-verify: {"id":"architecture-candidate-gating","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"candidates=10\nqualified=4\nmissing_outcome=1\nmissing_ownership=1\nworkload_mismatch=1\ngovernance_gap=1\ninsufficient_evidence=1\nlifecycle_cost_gap=1\narchitecture_patterns=4\nworkload_classes=7\nevaluation_scenarios=4\ndecision_receipts=10\ndecision_events=10\n","stderr":""}} -->
```python
candidates = [
    {"pattern": "warehouse", "workloads": {"reporting", "bi"}, "scenarios": {"steady"}, "outcome": True, "ownership": True, "workload_fit": True, "governance": True, "evidence": True, "lifecycle": True},
    {"pattern": "mesh", "workloads": {"sharing", "discovery"}, "scenarios": {"growth"}, "outcome": True, "ownership": True, "workload_fit": True, "governance": True, "evidence": True, "lifecycle": True},
    {"pattern": "fabric", "workloads": {"federation", "discovery"}, "scenarios": {"regulated"}, "outcome": True, "ownership": True, "workload_fit": True, "governance": True, "evidence": True, "lifecycle": True},
    {"pattern": "hybrid", "workloads": {"reporting", "ml", "streaming"}, "scenarios": {"steady", "growth"}, "outcome": True, "ownership": True, "workload_fit": True, "governance": True, "evidence": True, "lifecycle": True},
    {"pattern": "mesh", "workloads": {"sharing"}, "scenarios": {"growth"}, "outcome": False, "ownership": True, "workload_fit": True, "governance": True, "evidence": True, "lifecycle": True},
    {"pattern": "fabric", "workloads": {"discovery"}, "scenarios": {"regulated"}, "outcome": True, "ownership": False, "workload_fit": True, "governance": True, "evidence": True, "lifecycle": True},
    {"pattern": "warehouse", "workloads": {"streaming"}, "scenarios": {"burst"}, "outcome": True, "ownership": True, "workload_fit": False, "governance": True, "evidence": True, "lifecycle": True},
    {"pattern": "hybrid", "workloads": {"ml"}, "scenarios": {"regulated"}, "outcome": True, "ownership": True, "workload_fit": True, "governance": False, "evidence": True, "lifecycle": True},
    {"pattern": "lakehouse", "workloads": {"ml"}, "scenarios": {"growth"}, "outcome": True, "ownership": True, "workload_fit": True, "governance": True, "evidence": False, "lifecycle": True},
    {"pattern": "hybrid", "workloads": {"federation"}, "scenarios": {"burst"}, "outcome": True, "ownership": True, "workload_fit": True, "governance": True, "evidence": True, "lifecycle": False},
]

def evaluate(candidate):
    if not candidate["outcome"]:
        return "missing_outcome"
    if not candidate["ownership"]:
        return "missing_ownership"
    if not candidate["workload_fit"]:
        return "workload_mismatch"
    if not candidate["governance"]:
        return "governance_gap"
    if not candidate["evidence"]:
        return "insufficient_evidence"
    if not candidate["lifecycle"]:
        return "lifecycle_cost_gap"
    return "qualified"

results = [evaluate(candidate) for candidate in candidates]
print(f"candidates={len(candidates)}")
for outcome in ["qualified", "missing_outcome", "missing_ownership", "workload_mismatch", "governance_gap", "insufficient_evidence", "lifecycle_cost_gap"]:
    print(f"{outcome}={results.count(outcome)}")
print(f"architecture_patterns={len({candidate['pattern'] for candidate in candidates} - {'lakehouse'})}")
print(f"workload_classes={len(set().union(*(candidate['workloads'] for candidate in candidates)))}")
print(f"evaluation_scenarios={len(set().union(*(candidate['scenarios'] for candidate in candidates)))}")
print(f"decision_receipts={len(candidates)}")
print(f"decision_events={len(results)}")
```

The output reports ten candidates, four qualified and one of each declared failure, four counted decision patterns, seven workload classes, four scenarios, ten receipts, and ten decisions. The pattern count deliberately treats the lone unqualified lakehouse declaration as a storage implementation detail rather than a separately qualified portfolio pattern.

The evidence is deliberately narrow. Invented Booleans, sets, and classifications establish only deterministic gate order and counts. They do not establish that the gates are sufficient, candidate declarations are true, patterns are coherent, workloads are fitted, governance works, evidence is representative, one candidate dominates another, or any migration, performance, reliability, cost, risk, adoption, recovery, reversibility, closure, or outcome claim holds. Production evaluation requires owned scenarios, comparable measurements, production-shaped trials, contracts, policy tests, workload traces, incidents, cost records, recovery exercises, stakeholder judgments, sensitivity analysis, and decision receipts.

## Alternatives and Trade-Offs

**Baseline with targeted repairs.** Existing skills, contracts, and operations remain stable while the highest-value capability gaps are corrected. Architectural debt and fragmented experience may persist, but this option often has the best reversibility and information value.

**Strengthened central warehouse.** Conformed history, governed reporting, workload management, and repeatable operations can improve. Central queues, duplicated source interpretation, proprietary coupling, and weak domain incentives can remain unless ownership and interfaces change.

**Warehouse with domain-owned products.** Domains own semantics and obligations while a shared analytical platform supplies storage, compute, policy, and operations. This combines coherence with accountability, but responsibility boundaries and funding must be explicit.

**Shared lakehouse substrate.** Open or directly accessible tables can serve analytics and machine-learning workflows across engines. Catalog coupling, maintenance, connector differences, serving performance, policy enforcement, and operator skill become critical.

**Domain-oriented mesh on shared infrastructure.** Product ownership and federated governance change while common infrastructure limits duplicated plumbing. Domain readiness, platform quality, incentives, consumer experience, and cross-domain semantics determine success.

**More physically distributed mesh.** Domains select or operate more of their own stores and engines. Local optimization and regulatory isolation can improve, while skill duplication, interoperability, observation, recovery, and portfolio cost grow.

**Metadata and policy fabric over current platforms.** Discovery, lineage, contracts, quality, and controls can improve without immediate data relocation. Metadata correctness, enforcement coverage, connector quality, dependency availability, and automation safety constrain value.

**Integration-heavy fabric.** A common layer orchestrates movement, transformation, access, and policy across systems. It can reduce point solutions but may become a central bottleneck, semantic dumping ground, broad blast radius, or vendor dependency.

**Federated query access.** Some consumers gain timely access without copying data. Cross-source joins, consistency, pushdown, network movement, source load, policy, and failure semantics can make predictable service difficult.

**Materialized data products.** Consumer-shaped products isolate workloads and preserve reproducible semantics. Copies, freshness, storage, reconciliation, privacy exposure, and lifecycle work increase.

**One strategic platform.** Standardization can reduce cognitive load and simplify policy, procurement, and support. Workload compromises, migration concentration, lock-in, systemic failures, and slow accommodation of legitimate exceptions grow.

**Best-of-breed portfolio.** Each workload can use a strong engine or service. Interfaces, skills, policy consistency, metadata, cost allocation, recovery, and exit become a platform-design problem.

**Build core capabilities.** Interfaces and operations can fit local needs and avoid some vendor coupling. Engineering capacity, security, maintenance, ecosystem compatibility, and long-term opportunity cost are substantial.

**Buy managed capabilities.** Delivery and operations may accelerate. Service boundaries, roadmap dependence, metering, data movement, contractual exit, regional availability, and opaque implementation need scrutiny.

**Sequential incremental adoption.** Each bounded change buys evidence and limits blast radius. Benefits arrive gradually and temporary coexistence costs require explicit expiry.

**Broad transformation program.** Coordinated ownership, platform, governance, and migration can address systemic constraints together. Interdependencies, delayed feedback, organizational saturation, and irreversible commitments magnify risk.

**Standardized global governance.** Uniform controls and evidence can improve. Domain semantics and local regulation can be misrepresented if standards do not support profiles and exceptions.

**Federated governance.** Domains contribute and execute policy within shared outcomes and computational controls. Authority, conflict resolution, policy versioning, conformance, and platform support require mature mechanisms.

**Immediate migration.** Dual-running cost is minimized. Evidence, rollback, consumer adaptation, reconciliation, and operator learning are weakest.

**Canary migration with bounded dual running.** Risk and uncertainty decrease through comparison and rollback. Duplicate operation and authority ambiguity cost more until explicit exit conditions are met.

## Failure Modes and Misconceptions

1. **“Mesh, fabric, warehouse, and lakehouse are mutually exclusive products.”** They describe different and overlapping layers.
2. **“A label is an architecture.”** Ownership, interfaces, policy, operation, and lifecycle are missing.
3. **“Mesh means one technology stack.”** Its principles permit many technical realizations.
4. **“Buying a mesh platform creates domain ownership.”** Authority, capability, incentives, and obligations cannot be installed.
5. **“Decentralization removes central teams.”** Shared platforms and global governance still need owners.
6. **“Every domain should operate its own infrastructure.”** Domain semantic ownership can coexist with common infrastructure.
7. **“Domain autonomy means consumer obligations are optional.”** Products exist to serve bounded consumers under contracts.
8. **“Data as a product means adding a product page.”** Quality, service, support, change, cost, and closure remain.
9. **“Self-service means a portal exists.”** Safe outcomes, cognitive load, lead time, and support determine self-service.
10. **“Federated governance means each team chooses its rules.”** Shared outcomes and enforceable authority remain necessary.
11. **“Fabric is a single purchasable layer.”** Required connective capabilities and their evidence must be decomposed.
12. **“A catalog creates a fabric.”** Discovery without correct metadata, policy, integration, or operation is narrower.
13. **“Active metadata is automatically correct.”** Automation can accelerate stale or misleading assertions.
14. **“Lineage proves semantic correctness.”** It records relationships, not meaning or fitness.
15. **“Policy as code guarantees enforcement.”** Inputs, coverage, decision points, rollout, and exceptions can fail.
16. **“A warehouse always centralizes ownership.”** Physical placement and semantic authority are separate choices.
17. **“A central warehouse guarantees one truth.”** Conformed models require governance, evidence, and bounded definitions.
18. **“A lakehouse is object storage plus a query engine.”** Transactions, metadata, maintenance, governance, and service matter.
19. **“Open files eliminate lock-in.”** Catalogs, semantics, features, operations, and contracts can still bind the system.
20. **“Multiple engines are interchangeable.”** Operation and connector semantics differ by version and configuration.
21. **“Federated query avoids data movement.”** Plans can move large intermediate results across networks.
22. **“Querying in place avoids copies.”** Caches, spill, extracts, materializations, and consumer tools may copy data.
23. **“Pushdown either exists or does not.”** Operators, connectors, types, policies, and sources support different subsets.
24. **“Hybrid is the safe compromise.”** An undefined hybrid hides duplication and inconsistent responsibility.
25. **“Hybrid means use every platform.”** A governed allocation should exclude unnecessary choices.
26. **“The current architecture costs nothing.”** Incidents, queues, manual work, commitments, and delay belong in the baseline.
27. **“The newest option should be compared only with replacement.”** Targeted improvement may dominate broad change.
28. **“One architecture should fit every workload.”** Reporting, streaming, machine learning, sharing, and discovery differ.
29. **“Feature matrices determine workload fit.”** Production shape, behavior, policy, and operation require evidence.
30. **“A vendor benchmark predicts local performance.”** Data, concurrency, configuration, price, and versions differ.
31. **“A mandatory constraint can receive a low weight.”** A compensating score cannot legalize a prohibited design.
32. **“Unknown evidence deserves a neutral score.”** Unknowns require experiments or conservative treatment.
33. **“High, medium, and low are arithmetic intervals.”** Ordinal categories do not justify addition.
34. **“More decimal places make a decision objective.”** Precision can conceal judgments and weak measurements.
35. **“Weights represent every stakeholder.”** Authority, affected parties, conflicts, and dissent must be explicit.
36. **“The highest total score is robust.”** Small changes in assumptions may reverse it.
37. **“Cost means license and compute.”** People, migration, dual running, network, risk, recovery, and exit matter.
38. **“Centralization is inherently cheaper.”** Queueing, scale, lock-in, and central coordination can dominate.
39. **“Decentralization is inherently faster.”** Repeated plumbing and weak platform support can slow every domain.
40. **“Published product count measures value.”** Products can be unused, untrusted, duplicated, or harmful.
41. **“Catalog searches measure successful discovery.”** Consumers need correct understanding and usable access.
42. **“A successful trial proves enterprise fitness.”** Scale, diversity, failures, skills, and long-term operation remain.
43. **“Migration is data copying.”** Contracts, semantics, policy, consumers, lineage, recovery, and cost must move.
44. **“Dual running is automatically safer.”** Split authority and unresolved divergence can increase harm.
45. **“Rollback is a routing toggle.”** State, schema, policy, capacity, and reconciliation must support return.
46. **“Open formats guarantee reversibility.”** Interfaces, metadata, policy, skills, and commercial commitments remain.
47. **“Recovery is complete when data is readable.”** Current authorization, semantics, services, and dependencies matter.
48. **“A decision record is permanent approval.”** Evidence and context expire.
49. **“Stopping new writes closes the old architecture.”** Readers, copies, jobs, access, caches, and recovery paths remain.
50. **“A restored backup cannot revive a retired design.”** Obsolete credentials, routes, policies, and jobs can reactivate it.

## Worked Examples

### Example 1

A bank's regulatory reporting uses a central warehouse because conformed history, repeatability, controlled changes, and audit evidence dominate. Business domains own source products and definitions, while a jointly governed reporting model owns regulated transformations. This is domain ownership with a central serving environment, not a contradiction.

### Example 2

A retailer has mature merchandising and supply domains but a small platform team. It adopts domain-owned products on shared storage and compute, with common publication, contracts, lineage, policy, and incident tooling. Allowing every domain to choose infrastructure fails the capacity gate even though it appears more decentralized.

### Example 3

A catalog vendor demonstrates automated lineage for one query engine. A trial finds incomplete column lineage through stored procedures and no policy-decision evidence for partner exports. The fabric option remains eligible only after the capability map records bounded coverage and a compensating control; the brand name is irrelevant.

### Example 4

Data scientists need direct access to versioned training tables, while executive dashboards require high concurrency and a governed semantic layer. A hybrid allocation uses an open table substrate for training and a warehouse serving layer for dashboards. Shared product identities, contracts, classifications, lineage, and cost tags connect both without claiming they are interchangeable.

### Example 5

A federated engine answers simple filtered queries efficiently because predicates and projections reach sources. A representative cross-source join moves terabytes, overloads an operational database, and violates the latency objective. Discovery stays federated, while the recurring join becomes a materialized product with a freshness contract.

### Example 6

One architecture option offers lower median query cost but lacks a tested regional recovery path required by law. Another costs more and passes the recovery gate. The cheaper option is disqualified rather than rescued by a weighted score; a recovery experiment may later supply decision-changing evidence.

### Example 7

A team rates alternatives high, medium, and low, converts them to 3, 2, and 1, and reports a winner by 0.07 points. Review removes duplicated agility criteria, restores unknown evidence, and varies stakeholder preferences. Two options remain on the Pareto frontier, so the decision authority chooses the more reversible one pending a workload trial.

### Example 8

A healthcare network cannot centralize identifiable records across jurisdictions. Domains retain regulated stores, a shared catalog exposes permitted metadata, policy decisions execute near data, and approved aggregates enter a regional warehouse. The hybrid is explicit by data class, purpose, jurisdiction, consumer, and closure rule.

### Example 9

A migration canaries one finance product. Old and new paths bind the same source cutoff, contract, reference data, and policy; reconciliation checks totals, dimensions, late changes, lineage, and consumer decisions. A material divergence stops expansion, preserves old authority, and creates new evidence for the decision receipt.

### Example 10

Retirement of a fabric connector removes collection jobs, cached credentials, catalog routes, lineage ingestion, policy bindings, network access, support ownership, and disaster-recovery configuration. Historical decisions and permitted lineage remain. A recovery exercise proves the connector cannot resume after an old control-plane backup is restored.

## Cross-Program Connections

- [Data Engineering](../../19-data-engineering/ROADMAP.md) implements ingestion, transformation, data products, contracts, quality, lineage, reconciliation, orchestration, migration, and workload evidence across selected patterns.
- [Large-Scale Data Systems Engineering](../../21-large-scale-data-systems-engineering/ROADMAP.md) supplies storage, table, stream, batch, query, metadata, consistency, scaling, isolation, and recovery mechanisms used to test workload fitness.
- [Database Engineering](../../18-database-engineering/ROADMAP.md) owns physical design, transactions, indexing, partitioning, query plans, concurrency, statistics, constraints, backup, restoration, and engine-specific evidence.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) owns stable product interfaces, access semantics, errors, compatibility, idempotency, service objectives, and consumer migrations.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) treats self-service data infrastructure, catalogs, policy, identity, telemetry, cost, support, paved paths, and recovery as products for domain teams.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) assesses identity, trust boundaries, isolation, policy enforcement, data movement, attack surface, supply chain, incident response, and recovery.
- [Network Engineering](../../24-network-engineering/ROADMAP.md) tests topology, throughput, latency, egress, private access, intermediaries, cross-region movement, and failure behavior behind federation and replication.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) provides reasoning about partial failure, consistency, clocks, duplication, ordering, convergence, replay, coordination, and common-mode risk.
- [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) connects bounded contexts, dependency direction, platform boundaries, modularity, evolutionary architecture, decision records, and migration seams.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies stakeholder analysis, alternatives, trade studies, interfaces, configuration, verification, validation, hazards, lifecycle, recovery, and emergent-risk discipline.

## References

1. Zhamak Dehghani, [Data Mesh Principles and Logical Architecture](https://martinfowler.com/articles/data-mesh-principles.html), domain ownership, data as a product, self-service platform, and federated computational governance.
2. IBM, [What Is a Data Fabric?](https://www.ibm.com/think/topics/data-fabric), vendor context for integration, catalog, governance, security, self-service, metadata, and automation.
3. Armbrust et al., [Lakehouse: A New Generation of Open Platforms that Unify Data Warehousing and Advanced Analytics](https://www.cidrdb.org/cidr2021/papers/cidr2021_paper17.pdf), architectural argument and scoped prototype evidence.
4. Snowflake, [Key Concepts and Architecture](https://docs.snowflake.com/en/user-guide/intro-key-concepts), managed storage, compute, and cloud-services implementation context.
5. Apache Software Foundation, [Apache Iceberg Documentation](https://iceberg.apache.org/docs/latest/), open tables, evolution, snapshots, reliability, maintenance, and engine integrations.
6. Trino, [Pushdown](https://trino.io/docs/current/optimizer/pushdown.html), connector- and source-dependent predicate, projection, aggregation, join, limit, and related pushdowns.
7. OpenMetadata, [Documentation](https://docs.open-metadata.org/latest/), catalog, discovery, lineage, quality, governance, and collaboration implementation context.
8. OpenLineage, [Object Model](https://openlineage.io/docs/spec/object-model/), dataset, job, run, event, namespace, name, and facet identities.
9. Bitol, [Open Data Contract Standard](https://bitol-io.github.io/open-data-contract-standard/latest/), machine-readable schema, quality, service, role, support, and infrastructure obligations.
10. W3C, [Data Catalog Vocabulary 3](https://www.w3.org/TR/vocab-dcat-3/), catalogs, datasets, distributions, data services, relationships, versions, and profiles.
11. Open Policy Agent, [Policy Language](https://www.openpolicyagent.org/docs/policy-language), structured policy decisions and Rego implementation context.
12. OpenTelemetry, [Specification](https://opentelemetry.io/docs/specs/otel/), cross-implementation telemetry concepts, signals, resources, context, and compatibility.
13. NIST, [Cybersecurity Framework](https://www.nist.gov/cyberframework), outcome-oriented cybersecurity risk guidance.
14. NIST, [Privacy Framework 1.1](https://www.nist.gov/privacy-framework/using-privacy-framework-11), outcome- and risk-oriented privacy guidance.
15. NASA, [Decision Analysis](https://www.nasa.gov/reference/6-8-decision-analysis/), criteria, alternatives, methods, uncertainty reduction, robustness, results, and recommendations.
16. FinOps Foundation, [FinOps Framework](https://www.finops.org/framework/), collaborative operating model, usage and cost, value, optimization, governance, and technology decisions.

## Exercises

### Exercise 1

Evaluate mesh, fabric, warehouse, lakehouse, and hybrid choices for an enterprise with regulated reporting, exploratory analytics, machine-learning training, operational dashboards, and partner exchange. Separate architectural layers, define scenarios and gates, inventory evidence, and produce coherent alternatives including the baseline.

### Exercise 2

Design a readiness assessment for domain-oriented ownership and a self-service data platform. Include domains, authority, product obligations, skills, funding, incentives, common capabilities, governance allocation, adoption, incidents, recovery, costs, and conditions that would stop decentralization.

### Exercise 3

Construct a trade study for three qualified architecture portfolios. Define evidence ranges, ordinal judgments, uncertainty, mandatory constraints, dominance rules, sensitivity variables, stakeholder authority, dissent, experiments, and review triggers without relying on one unexplained score.

### Exercise 4

Plan a migration from a central analytical estate to a bounded hybrid. Include product contracts, semantic authority, workload allocation, metadata, policy, lineage, canaries, dual running, reconciliation, rollback, consumer evidence, cost, recovery, exceptions, and retirement.

### Exercise 5

Write the closure and reversibility plan for a managed data platform in a multi-platform portfolio. Address data and metadata extraction, interfaces, table behavior, policies, identities, credentials, lineage, consumers, commitments, skills, incidents, restoration, historical evidence, and nonactivation tests.

## Answers to the Exercises

### Answer 1

Model mesh as ownership and operating choices, fabric as catalog, lineage, contract, policy, integration, and automation capabilities, and warehouse or lakehouse as storage, processing, and serving choices. Define scenarios for steady reporting, exploratory growth, model training, low-latency dashboards, partner failure, regulation change, and recovery. Gates include lawful placement and joining, accountable semantic ownership, required audit evidence, workload service, bounded loss, and tested recovery. The baseline records present platforms, teams, manual work, incidents, commitments, and useful capabilities. Alternatives include targeted repairs; domain-owned products on a strengthened warehouse; a shared open-table substrate; a metadata and policy fabric over existing stores; and an explicit hybrid allocating governed reporting to warehouse serving, training to open tables, operational analytics to bounded materializations, and partner exchange to contracted interfaces. Evidence remains scoped by data, configuration, version, operator, time, and uncertainty.

### Answer 2

Assess each candidate domain for stable boundaries, source authority, semantic expertise, engineering and on-call capacity, product management, consumer relationships, policy competence, budget, incentives, and willingness to accept service and closure obligations. Assess the platform for safe publication, contracts, storage and compute, orchestration, catalog and lineage, quality, identity, policy, telemetry, cost allocation, support, migration, recovery, and retirement with measured lead time and cognitive load. Allocate global controls, domain decisions, platform responsibilities, and joint semantic governance explicitly. Track successful consumer decisions, contract conformance, incidents, support burden, unit cost, and countermetrics rather than product count. Stop or narrow decentralization when ownership is nominal, platform toil is exported, required policy cannot be enforced, consumer harm rises, recovery fails, or total operating capacity is exceeded.

### Answer 3

Disqualify any portfolio that fails legal, security, privacy, semantic ownership, service, or recovery gates. For qualified options, preserve measured latency, concurrency, migration time, unit cost, recovery time, and staffing as ranges tied to exact scenarios and methods. Keep expert ratings of organizational fit or reversibility ordinal unless stakeholders define a value function. Identify options dominated under compatible evidence and retain the Pareto frontier. Vary workload growth, egress price, domain maturity, platform staffing, adoption, vendor price, and recovery frequency; record thresholds at which the recommendation changes. Name decision authority and affected stakeholders, preserve dissent, and commission trials only for uncertainties capable of changing the choice. The receipt records evidence, assumptions, frontier, judgment, commitments, experiment results, expiry, and event-based review triggers.

### Answer 4

Choose products and workloads as bounded migration units. Stabilize producer and consumer contracts, semantic owners, product identities, policies, lineage, quality, and current baseline evidence before moving data. Define the allocation function by domain, data class, jurisdiction, workload, and consumer. Canary a reversible product; bind old and new paths to the same source intervals and reference data; reconcile keys, totals, distributions, late changes, policy decisions, lineage, service, costs, and consumer outcomes. During bounded dual running, identify authoritative writes, routing, divergence ownership, rollback point, capacity, and exit date. Exercise recovery of both paths. Expand only when gates and outcome thresholds pass. Expire every exception. Retirement drains consumers, stops paths, revokes access, removes catalog and recovery routes, ends commitments, resolves quarantine, preserves required evidence, and proves nonactivation.

### Answer 5

Define exit time, cost, permitted loss, service impact, policy conditions, owner, and evidence. Inventory export of source and derived data, snapshots, schemas, contracts, catalog identities, lineage, quality history, policy bundles and decisions, identities, access grants, encryption dependencies, orchestration state, observability, cost records, and incident evidence. Test required table operations and semantic equivalence on replacement engines instead of assuming files are portable. Maintain versioned consumer interfaces or a funded migration path. Record commercial commitments, egress, staffing, documentation, and operator skill transfer. Revoke credentials and network access, terminate jobs and shares, reconcile and validate extracted state, preserve required historical records, and remove obsolete support paths. Restore an old backup in an isolated exercise and verify that retired policies, credentials, routes, jobs, products, and consumers cannot reactivate the managed platform.
