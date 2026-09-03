---
module_id: DARCH-003
program: Data Architecture Engineering
level: 1
module_number: 3
title: Current-State Data Landscape
status: complete
last_verified: 2026-09-03
---

# Current-State Data Landscape

## One-Page Review

### Governing question

How can an organization build a trustworthy, decision-useful account of the data landscape it actually operates when inventories are incomplete, names conflict, runtime behavior changes, and important dependencies exist outside approved platforms?

### Essential definitions

- A **current-state data landscape** is an evidence-backed, time-bounded account of material data assets, systems, flows, meanings, responsibilities, controls, consumers, and lifecycle conditions within a declared scope.
- An **observation** is a dated claim emitted by a source such as a catalog, configuration scan, runtime event, interview, contract registry, access log, or control system.
- An **assertion** is a claim supplied by an accountable person or governed record; it may be authoritative for one property without proving runtime behavior.
- A **landscape entity** is a stable architectural identity for a dataset, service, store, job, report, model, interface, policy, organization, or other item—not merely one mutable name.
- A **flow** is a directed, purposeful dependency through which data is created, read, transformed, copied, served, corrected, archived, or deleted.
- **Coverage** measures the known portion of a defined population; **confidence** expresses the strength and agreement of evidence for a particular claim.
- An **unknown** is a first-class finding with impact, owner, and resolution plan, rather than an empty field silently treated as safe.

### Central model, mechanism, or theorem

Treat the landscape as a temporal, evidence-bearing graph:

`L(t) = (V, E, C, Q | scope, evidence, confidence, observed_at)`

where `V` contains entities, `E` contains typed relationships and flows, `C` maps policies and controls to their subjects and enforcement points, and `Q` records unresolved questions and conflicts. No source is complete. Claims are reconciled by identity, property, provenance, authority, recency, and corroboration; important unknowns remain visible until resolved.

### Critical invariants

- Every landscape claim records source and observation time; volatile claims also have an expiry or refresh rule.
- Conceptual datasets, physical distributions, services, jobs, and reports have distinct identities even when a tool collapses them.
- Every material cross-boundary flow names producer, consumer, purpose, data, interface, timing, owner, and failure or correction path.
- Authoritative ownership assertions and observed runtime behavior are preserved separately and compared.
- Coverage denominators are declared; “90% discovered” is meaningless without a bounded population.
- Conflicts, stale evidence, orphan assets, and shadow dependencies are findings, not cleanup noise.
- The repository of record can be rebuilt or reconciled from governed evidence; a visualization is never the sole source.

### Common failures

Common failures include treating the configuration-management database as truth, equating databases with data products, interviewing only platform teams, scanning only approved accounts, inferring business meaning from column names, drawing undocumented arrows, omitting extracts and spreadsheets, confusing declared lineage with observed lineage, hiding conflicts by last-write-wins merge, publishing percentages without denominators, and allowing the map to become obsolete immediately after a workshop.

### Compact example

A billing catalog says `invoice_summary` is owned by Finance and populated nightly from the ledger. Query logs show a support dashboard reading it hourly; orchestration logs reveal an undocumented CRM extract; the owner directory says the named steward left six months ago. A trustworthy landscape preserves all four observations, resolves the dataset identity, records the ownership conflict and hidden flow, and marks operational and policy consequences for review.

### Connections

[DARCH-001](001-data-architecture-as-structure-flow-ownership-and-policy.md) defines the architecture views joined here, while [DARCH-002](002-business-strategy-and-data-outcomes.md) determines which outcomes and decisions make parts of the landscape material. [DARCH-004](../ROADMAP.md) classifies system roles. Pipeline implementation is developed in [Data Engineering](../../19-data-engineering/ROADMAP.md), storage behavior in [Database Engineering](../../18-database-engineering/ROADMAP.md), and system context and interfaces in [Systems Engineering](../../26-systems-engineering/ROADMAP.md).

## Governing Question

An organization cannot responsibly design a target data architecture without knowing what it must preserve, replace, untangle, or stop. Yet the current state is not waiting in one inventory. It is distributed across cloud accounts, database catalogs, message brokers, schedulers, source repositories, access logs, contracts, dashboards, spreadsheets, vendor exchanges, support procedures, and human memory. Each source reveals a projection and carries its own omissions.

The governing question is therefore not “Which tool can draw our estate?” It is: how can multiple, fallible observations be turned into a bounded architectural account whose claims, gaps, and conflicts are explicit enough to support decisions? The answer requires disciplined scoping, stable identity, evidence reconciliation, graph reasoning, validation with people and runtime traces, and a maintenance mechanism.

A current-state landscape is a model, not a perfect copy of reality. It deliberately omits details that do not affect the decision at hand. But abstraction differs from accidental blindness. A good landscape states what is included, why it matters, how it was observed, when it was true, what remains unknown, and how much confidence a reviewer should place in each claim.

## Why This Matters

Target designs fail when the current state is simplified into an approved-platform diagram. A migration retires a table that feeds a monthly regulatory workbook. A domain redesign overlooks a partner file whose identifier is the practical reconciliation key. A security program classifies cataloged columns but misses copied extracts. A cost initiative removes an apparently idle pipeline whose output is the only disaster-recovery input for another service.

These are landscape failures before they are migration failures. The harm comes from missing identity, dependency, meaning, ownership, control, or temporal behavior. The resulting surprise appears late, when reversal is expensive and stakeholder trust has already been spent.

Accurate current-state knowledge supports more than modernization. It enables incident blast-radius analysis, policy scoping, privacy impact assessment, contract change, cost allocation, recovery planning, merger integration, audit evidence, product discovery, and decommissioning. It also reveals organizational design: duplicated facts often expose unresolved authority; fragile manual transfers expose coordination boundaries; abandoned assets expose missing lifecycle accountability.

Completeness is contextual. A map sufficient for warehouse cost optimization may be unsafe for a records-disposition program. A payment-data review may require field-level lineage and enforcement points, while an early portfolio assessment may need only product, system, and cross-boundary flow detail. The landscape should be no more detailed than the decisions require, but no less evidenced than their consequences demand.

## Prerequisites and Retrieval

You should understand systems, databases, files, APIs, events, pipelines, access control, basic data modeling, and organizational roles. Recall from DARCH-001 that structure, flow, ownership, and policy are coupled views; from DARCH-002, recall that architecture scope should trace to outcomes and stakeholder decisions.

Retrieve the distinctions between a conceptual dataset and a physical representation, between an asserted relationship and observed execution, between semantic authority and technical custody, and between a missing value and evidence that no relationship exists. Graph terminology—node, edge, path, component, cycle, and degree—is useful but introduced as needed.

## Learning Objectives

After completing this module, you should be able to:

- define a decision-bounded scope and explicit coverage denominator for landscape discovery;
- distinguish datasets, distributions, services, jobs, stores, interfaces, reports, and organizational identities;
- design a canonical observation record with provenance, time, authority, and confidence;
- combine catalog, configuration, code, runtime, contract, control, and interview evidence without pretending that any source is complete;
- reconcile aliases and conflicting claims while preserving source assertions;
- map flows with purpose, semantics, timing, failure, correction, and control properties;
- use graph analysis to identify critical dependencies, cycles, orphan assets, and hidden concentration;
- record unknowns, staleness, and coverage limits as actionable findings;
- validate the landscape through sampling, reverse tracing, owner review, and operational evidence;
- establish change-driven maintenance and fitness measures for the landscape itself.

## Core Exposition

Start with the **decision boundary**. A landscape initiative needs a sponsor, named decisions, time horizon, systems of interest, organizations, environments, jurisdictions, and materiality rules. “Map enterprise data” has no natural stopping point. “Identify customer-data dependencies that could block retirement of the regional CRM within two quarters” can be tested.

Scope has multiple dimensions. Organizational scope names business units and external parties. Technical scope names production, recovery, development, end-user, and vendor environments. Data scope names domains, classifications, criticality, or products. Lifecycle scope states whether collection, processing, serving, archival, legal hold, and deletion are included. Temporal scope distinguishes the observation window from the business history represented in the data.

Define a **population frame** before reporting coverage. Examples include all production cloud accounts in the finance organization, all database instances registered to a payment service, all scheduled workflows in named orchestrators, or all reports used in a declared regulatory process. Several frames may overlap. Assets found outside them are not discarded; they may reveal that the original boundary was wrong.

The unit of analysis must be explicit. A server, database, schema, table, topic, object prefix, API, report, feature set, and conceptual data product answer different questions. Listing 40,000 tables does not mean 40,000 products have been discovered. Conversely, one “customer platform” node can conceal incompatible stores, authorities, retention rules, and consumers.

Use a layered identity model. A **conceptual entity** represents a business or information concept. A **dataset or product identity** represents a managed collection offered under a contract. A **distribution** represents an accessible serialization or projection. A **service** exposes operations. A **physical asset** locates bytes or execution. These identities may be linked, but they are not interchangeable.

W3C [DCAT 3](https://www.w3.org/TR/vocab-dcat-3/) distinguishes datasets, distributions, data services, dataset series, catalog records, and broader catalog resources. This vocabulary is useful for interoperable descriptions and for preventing a file URL from becoming the dataset identity. It does not discover hidden assets or decide enterprise authority.

Stable identity is harder than stable naming. A table can be renamed without changing its product identity; a table can retain its name while its meaning changes. A copy can share schema and name while holding a different population or policy. Define identifiers within namespaces, preserve aliases, record validity intervals, and never merge records on display name alone.

For each observed claim, capture at least:

- `subject_id`: the entity to which the claim applies;
- `property`: such as owner, input, classification, schema, purpose, or endpoint;
- `value`: another identity or a typed value;
- `source_id`: the system, record, person, or observation process supplying the claim;
- `observed_at`: when the evidence was obtained or emitted;
- `valid_time`: when the described condition applied, if known;
- `authority`: why this source may decide or report the property;
- `confidence`: a reasoned assessment, not cosmetic precision;
- `evidence_ref`: a reproducible pointer where access permits;
- `expiry` or `refresh_rule`: when the claim must be checked again.

This observation model prevents destructive merging. If a catalog names one owner and repository metadata names another, retain both assertions. Resolution can select an effective value while the original evidence remains available. “Latest” is not automatically “authoritative”: an access log is strong evidence that a read occurred, but weak evidence of business purpose; a policy register may be authoritative for classification rules, but not proof that enforcement occurred.

Discovery combines complementary channels. **Configuration sources** include cloud resource inventories, database system catalogs, broker metadata, storage listings, scheduler definitions, deployment manifests, network rules, and infrastructure code. They reveal deployed things and declared connections, but often miss external and manual use.

**Runtime sources** include query history, job-run events, API telemetry, message offsets, file-transfer logs, audit trails, network observations, and storage access logs. They show behavior during an observation window. Absence of activity is not proof of nonuse: annual processing, failed telemetry, sampling, or a dormant recovery path may explain silence.

**Code and contract sources** include SQL, transformation projects, application repositories, schemas, interface specifications, event definitions, data contracts, and tests. Static analysis can reveal intended dependencies that have not run recently. Dynamic SQL, user-defined code, generated queries, and external configuration limit inference.

**Management and policy sources** include product catalogs, owner directories, service registries, risk registers, classifications, processing records, retention schedules, contracts, support rosters, and recovery plans. They reveal authority and obligations, but can be stale or aspirational. A control statement should be joined to its enforcement point and operating evidence.

**Human discovery** includes structured interviews, workflow observation, consumer surveys, incident reviews, architecture decision records, and facilitated map validation. People explain meaning, purpose, exceptions, and manual work that scanners cannot infer. Interviews are assertions with provenance, not unquestionable truth. Ask for examples, execution evidence, and names of upstream and downstream stakeholders.

Shadow assets deserve deliberate search. Look for scheduled desktop tasks, shared drives, collaboration exports, unmanaged notebooks, local databases, emailed files, embedded dashboard extracts, SaaS connectors, partner transfers, service-account activity, and long-lived object-store prefixes. Do not frame their users as offenders by default. Shadow processes often exist because official products do not satisfy latency, semantics, accessibility, or control needs.

Data flows are typed relationships, not generic arrows. A flow record should identify source, destination, data identity, producer, consumer, purpose, interface, trigger, frequency, latency, volume, transformation, delivery semantics, security boundary, classification, contract, owner, error handling, correction propagation, retention, and deletion behavior. Capture what is known and expose what is not.

Distinguish **design lineage** from **runtime lineage**. Design lineage says a job is declared to read `A` and write `B`. Runtime lineage says a particular execution observed those inputs and outputs. [OpenLineage](https://openlineage.io/docs/spec/object-model/) models Jobs, Runs, and Datasets and supports both run events and design-time events. Its model enables interoperable observations; completeness still depends on instrumentation and naming.

Lineage also varies in granularity. System-level lineage supports portfolio reasoning. Dataset-level lineage supports dependency and incident analysis. Column-level lineage supports semantic and policy impact where transformations can be parsed. Record-level provenance may be necessary for scientific, legal, or high-consequence decisions but is much more expensive. Choose the least granularity that answers the decision safely.

Meaning cannot be reliably extracted from structure alone. A column called `status` might mean current workflow state, last emitted event, payment disposition, or a denormalized label. Capture definitions, populations, business keys, units, code sets, null semantics, event time, valid time, transaction time, update and correction behavior, and known data-quality conditions. Link each definition to an accountable authority and version.

Ownership is also a set of decisions. Record who may define meaning, authorize creation and correction, approve contracts, accept quality risk, grant access, fund operations, respond to incidents, preserve records, and retire the asset. A single `owner` field can hide important separation. Empty, group-only, departed-person, and contradictory ownership are all findings.

Policy mapping asks which rules apply to which entities and flows, where they are enforced, how exceptions work, and what evidence demonstrates operation. A label in a catalog is not equivalent to access control, purpose enforcement, retention, legal hold, or deletion. Trace sensitive data through derived products and external transfers; transformations may reduce, preserve, or create risk.

Current state includes operational condition. Record availability and freshness commitments, observed incidents, recovery dependencies, capacity, cost allocation, end-of-support technology, manual interventions, single-person knowledge, and change frequency where material. An architectural dependency that is logically clean but operationally abandoned is still a current-state risk.

Temporal modeling prevents a landscape from presenting incompatible observations as simultaneous truth. Record observation time separately from valid time. A weekly scan taken Monday may describe configuration effective then; an interview on Friday may describe an owner change effective Wednesday. Snapshots support comparison, while event history can reconstruct changes. Do not silently overwrite history when migration decisions depend on it.

Confidence should be explainable. A practical ordinal scheme may rate a claim `confirmed`, `corroborated`, `asserted`, `inferred`, or `unknown`. Define the evidence combinations for each level. Avoid multiplying arbitrary scores into fake probability. Confidence applies to a claim, not an entire asset: physical location may be confirmed while purpose is unknown.

Reconciliation has three distinct operations. **Entity resolution** decides whether observations describe the same entity. **Claim adjudication** determines which value currently governs a property. **Conflict management** preserves disagreement, consequence, and resolution authority. Automate exact and safe matches; route ambiguous semantic merges to accountable reviewers.

Graph analysis turns an inventory into architectural evidence. In-degree can reveal assets with many producers or accidental convergence. Out-degree can reveal widely consumed products and change blast radius. Strongly connected components expose feedback cycles. Bridges and cut vertices can reveal concentration, though graph topology alone cannot measure business criticality. Unowned nodes, flows without contracts, policy-bound data leaving enforcement zones, and target systems fed by deprecated sources become review queues.

Criticality is not popularity. A dataset read once a year may determine a statutory filing. A heavily queried cache may be easily rebuilt. Combine dependency topology with consumer impact, decision consequence, recovery needs, replacement options, regulatory obligations, and time sensitivity.

Validate through **triangulation**. For sampled products, trace forward from source to consumers and backward from consequential outputs to origins. Compare declared and runtime lineage. Reconcile catalog ownership with current organization records. Test whether classifications survive transformations. Ask operators to explain failure and recovery paths. Ask consumers what they actually use and how they detect errors.

Use negative tests. Search for active credentials with no registered product, queries from unknown clients, scheduled jobs without repositories, tables written by multiple authorities, data transfers with no recipient contract, and assets referenced by incidents but absent from the catalog. A landscape process that only confirms registered records cannot discover its blind spots.

Report coverage honestly. State each denominator, observation window, source failures, excluded environments, sampling design, and known blind spots. Separate `not observed` from `does not exist`. A claim such as “95% of in-scope production database instances were scanned successfully during 1–7 September” is reviewable; “the landscape is 95% complete” is not.

Prioritize findings by decision consequence. Immediate concerns may include ungoverned sensitive export, unknown regulatory-report input, unsupported critical store, conflicting write authority, or unrecoverable dependency. Lower-risk documentation gaps can wait. The landscape is an input to governance; it does not itself authorize deletion, migration, access, or policy exception.

Publish different views from the same governed observations. Executives need concentration, exposure, and transition implications. Domain owners need concepts, products, consumers, and decision rights. Engineers need endpoints, jobs, contracts, and runtime dependencies. Security and privacy reviewers need classification, purpose, boundaries, controls, and recipients. All views must resolve to consistent identities and evidence.

Maintenance should be change-driven. Integrate registration and validation with deployment, contract publication, new accounts, owner changes, interface changes, classification decisions, incidents, and decommissioning. Periodic scans still detect drift. Set refresh objectives by volatility and consequence: a runtime endpoint may expire quickly, while a legal retention authority changes less frequently but demands formal review.

The landscape process itself needs ownership. Assign responsibility for the observation schema, identity rules, source connectors, adjudication forums, coverage metrics, access protection, retention, and consumer support. Landscape metadata may reveal sensitive topology, identities, vulnerabilities, and commercial relationships, so access and disclosure require control.

## Definitions and Notation

Let the bounded population at time `t` be `U(t)`. The landscape model is:

`L(t) = (V(t), E(t), C(t), Q(t))`

where:

- `V(t)` is the set of known entity identities and types;
- `E(t)` is the set of typed relationships, including data flows and responsibility links;
- `C(t)` maps policies, controls, enforcement points, and evidence to entities and flows;
- `Q(t)` is the set of unresolved unknowns, conflicts, stale claims, and coverage gaps.

An observation is `o = (s, p, v, r, ta, tv, a, e)`: subject `s`, property `p`, value `v`, source `r`, observation time `ta`, valid-time interval `tv`, authority basis `a`, and evidence reference `e`. Reconciliation produces an effective claim only under a declared rule `R_p` for property `p`; it does not erase contributing observations.

For population frame `U_k` and successfully examined members `D_k`, discovery coverage is:

`coverage_k = |D_k| / |U_k|`

provided the denominator and date are stated. Asset-property completeness can be measured separately. For required property set `P_req`, the completeness of entity `x` is the proportion of properties with non-expired, non-unknown effective claims. Completeness does not prove correctness.

A flow `f` can be represented as `(source, target, data, purpose, interface, timing, transformation, contract, control, owner)`. A path is a sequence of compatible flows. Reachability estimates potential propagation or blast radius only within the observed graph; uninstrumented edges limit the conclusion.

A **system of record** is authoritative for named facts and decisions under a boundary, not necessarily the only store containing them. A **source of observation** reports evidence. A **catalog** organizes metadata. A **repository of record** preserves governed effective claims and provenance. These roles may be implemented together but must not be confused.

## Mechanisms, Invariants, or Proof Structure

A defensible current-state assessment can proceed through nine gates.

**1. Decision and scope gate.** Name sponsors, decisions, consequences, stakeholders, environments, organizations, classifications, lifecycle stages, observation window, and explicit exclusions. Define materiality and population frames before collection.

**2. Identity gate.** Establish entity types, namespaces, stable identifiers, alias rules, version and valid-time semantics, and criteria for merge and split. Test collisions on a sample before bulk ingestion.

**3. Evidence gate.** Register sources and their capabilities, access, owners, latency, retention, and known blind spots. Separate configuration, runtime, code, contract, management, control, and human evidence.

**4. Collection gate.** Ingest minimally necessary observations with provenance and time. Protect secrets and personal data. Record connector failures, excluded regions, sampling, and source freshness alongside results.

**5. Reconciliation gate.** Resolve identities, apply property-specific authority rules, preserve conflicts, and assign confidence. Do not use a global last-write-wins policy. Escalate semantic and ownership disputes to authorized decision makers.

**6. Relationship gate.** Construct typed flows and dependencies. Join declared and observed lineage, purposes, contracts, failure behavior, corrections, controls, and consumer identities. Represent unknown endpoints rather than dropping incomplete edges.

**7. Analysis gate.** Evaluate coverage, orphan assets, shadow flows, cycles, critical paths, concentration, policy exposure, ownership gaps, stale technology, recovery gaps, and migration constraints. Rank findings by consequence and uncertainty.

**8. Validation gate.** Sample high-risk and ordinary assets; trace forward and backward; compare runtime with declarations; conduct owner, consumer, operator, and control reviews. Record dissent and corrections as new evidence.

**9. Publication and maintenance gate.** Generate stakeholder-specific views, secure sensitive metadata, connect findings to decisions, assign resolution owners, and establish event-driven and periodic refresh. Define landscape fitness objectives and re-scope triggers.

The following executable example reconciles four inventory feeds. It preserves every observation, selects an effective owner only when a current organization assertion corroborates the catalog, exposes an active undocumented consumer, and treats silence as unknown rather than proof of absence.

<!-- bijux-verify: {"id":"landscape-evidence-reconciliation","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"assets=3\nobservations=10\nconfirmed_owners=1\nactive_shadow_flows=1\nunknown_owners=2\nfindings=customer_export:shadow-flow,invoice_summary:owner-conflict,legacy_rates:owner-unknown\n","stderr":""}} -->
```python
observations = (
    ("invoice_summary", "catalog_owner", "finance-data", "2026-09-01"),
    ("invoice_summary", "directory_owner", "revenue-platform", "2026-09-02"),
    ("invoice_summary", "runtime_read", "support-dashboard", "2026-09-02"),
    ("invoice_summary", "declared_consumer", "support-dashboard", "2026-09-01"),
    ("customer_export", "catalog_owner", "crm-team", "2026-09-01"),
    ("customer_export", "directory_owner", "crm-team", "2026-09-02"),
    ("customer_export", "runtime_read", "partner-transfer", "2026-09-02"),
    ("customer_export", "declared_consumer", "warehouse", "2026-09-01"),
    ("legacy_rates", "runtime_read", "pricing-batch", "2026-09-02"),
    ("legacy_rates", "declared_consumer", "pricing-batch", "2026-09-01"),
)

assets = sorted({row[0] for row in observations})
by_asset = {
    asset: [row for row in observations if row[0] == asset]
    for asset in assets
}
confirmed_owners = 0
shadow_flows = 0
unknown_owners = 0
findings = []

for asset, rows in by_asset.items():
    values = {}
    for _, property_name, value, _ in rows:
        values.setdefault(property_name, set()).add(value)

    catalog = values.get("catalog_owner", set())
    directory = values.get("directory_owner", set())
    if catalog and catalog == directory:
        confirmed_owners += 1
    elif catalog and directory:
        findings.append(f"{asset}:owner-conflict")
        unknown_owners += 1
    else:
        findings.append(f"{asset}:owner-unknown")
        unknown_owners += 1

    observed = values.get("runtime_read", set())
    declared = values.get("declared_consumer", set())
    if observed - declared:
        findings.append(f"{asset}:shadow-flow")
        shadow_flows += 1

print(f"assets={len(assets)}")
print(f"observations={len(observations)}")
print(f"confirmed_owners={confirmed_owners}")
print(f"active_shadow_flows={shadow_flows}")
print(f"unknown_owners={unknown_owners}")
print(f"findings={','.join(sorted(findings))}")
```

This fixture proves only the deterministic behavior of the stated teaching policy. It does not establish that two strings identify the same real team, that the four feeds are complete, that every runtime read is authorized, or that matching owner labels establish valid accountability. A production mechanism needs governed identity resolution, property-specific authorities, temporal rules, access controls, and human adjudication.

## Alternatives and Trade-Offs

**Top-down inventory versus outcome-led tracing.** Top-down scans offer breadth and comparability but can collect vast low-value detail. Outcome-led tracing reaches consequential dependencies quickly but may miss shared infrastructure and unrelated exposure. Use bounded population scans with deep traces from important decisions.

**Central repository versus federated metadata.** A central repository simplifies search, cross-domain analysis, and common controls. It can become stale, bottlenecked, and semantically coercive. Federation preserves local authority and richer context but needs shared identity, query, minimum metadata, and conflict rules.

**Automated discovery versus curated assertion.** Automation observes scale and change; it cannot reliably infer purpose, lawful basis, meaning, or accountability. Curation supplies semantics and authority but can be slow and aspirational. Preserve and reconcile both.

**Declared versus runtime lineage.** Declared lineage exists before execution and covers dormant paths; it can diverge from reality. Runtime lineage is empirical for an observed run; it misses uninstrumented systems and unused contingencies. Compare them and treat differences as evidence.

**System-level versus field-level mapping.** Coarse mapping is cheaper and adequate for portfolio boundaries. Fine lineage supports policy and change impact but is expensive, tool-dependent, and difficult with procedural transformations. Escalate granularity according to consequence.

**Snapshot versus event history.** Snapshots are simple to reason about and publish. They lose the sequence of changes and can combine observations from different times. Events preserve temporal evidence but require compaction, identity stability, and retention policy. Many programs need both.

**Broad access versus restricted topology.** Open metadata improves discovery and collaboration. Landscape records can expose sensitive classifications, endpoints, vulnerabilities, people, contracts, and concentration risk. Separate public descriptions from protected operational and control views.

**Strict registration gate versus retrospective discovery.** A deployment gate prevents new unknown assets but can drive work around the process if registration is costly. Retrospective scans detect reality but always lag. Make the paved registration path cheap, then scan and reconcile drift.

## Failure Modes and Misconceptions

1. **The catalog is the landscape.** It is one evidence source and may contain assertions without runtime confirmation.
2. **A complete CMDB implies complete data knowledge.** Component inventories rarely establish meaning, purpose, consumers, corrections, or policy inheritance.
3. **No observed use means safe to delete.** Observation windows, telemetry gaps, seasonal processing, recovery paths, and external users invalidate that inference.
4. **Matching names prove identical assets.** Names collide, meanings drift, and copies retain labels; identity needs namespace and evidence.
5. **Schema reveals semantics.** Types and column names omit populations, units, business rules, temporal meaning, and authority.
6. **One owner field is enough.** Semantic, service, access, risk, incident, funding, and lifecycle decisions may have different authorities.
7. **Every arrow is lineage.** Generic arrows hide purpose, timing, interface, transformation, failure, correction, and control.
8. **Automation removes human bias.** Tools encode source access, naming assumptions, parsers, retention windows, and platform boundaries.
9. **Interviews reveal the whole truth.** People forget, describe intended procedures, and see only their boundary; assertions need corroboration.
10. **Coverage is one percentage.** Each bounded population, property, source, and observation window has distinct coverage.
11. **Unknown means low risk.** Uncertainty can increase risk precisely because consequence and control are unverified.
12. **The map is finished when published.** Without change events, refresh rules, ownership, and fitness checks, it becomes historical fiction.

## Worked Examples

### Example 1

**Question:** A scan discovers 800 tables from 1,000 registered production databases. Is landscape coverage 80%?

**Reasoning:** No. The denominator counts databases while the numerator counts tables. Report database scan coverage and table discovery separately, including failed connections and excluded stores.

**Conclusion:** Coverage requires comparable units and a declared population.

### Example 2

**Question:** A catalog and owner directory disagree about an asset owner. Which record wins?

**Reasoning:** Determine which authority governs the relevant decision, compare effective dates and identities, and seek accountable adjudication. Preserve both observations and the conflict.

**Conclusion:** Reconciliation is property-specific, not last-write-wins.

### Example 3

**Question:** Query logs show no reads from a tax-report table for nine months. Can it be retired?

**Reasoning:** The report may be annual; logs may be incomplete; an extract or external identity may conceal use. Verify the full reporting cycle, consumers, contracts, recovery use, and accountable approval.

**Conclusion:** Runtime silence is bounded evidence, not proof of nonuse.

### Example 4

**Question:** Should a CSV export and the governed dataset behind it share one node?

**Reasoning:** Model the conceptual dataset separately from the CSV distribution. Link the distribution to its dataset, generation process, location, recipient, and policy.

**Conclusion:** Separate identity prevents representations from inheriting false equivalence.

### Example 5

**Question:** Static SQL says job `J` reads `A`; runtime events show it reading `A` and `B`.

**Reasoning:** Preserve declared lineage and observed lineage. Investigate dynamic configuration, unparsed code, or an unauthorized dependency; do not overwrite one with the other.

**Conclusion:** Difference between design and runtime is an architectural finding.

### Example 6

**Question:** A spreadsheet is outside the approved platform. Should it be excluded?

**Reasoning:** If it materially influences an in-scope decision or flow, include it with its actual control and ownership condition. Its existence may reveal unmet product needs.

**Conclusion:** Current state describes reality, including shadow paths.

### Example 7

**Question:** An asset has high out-degree. Is it automatically critical?

**Reasoning:** High out-degree indicates broad observed dependency. Criticality also depends on consumer consequence, replacement, recovery, time sensitivity, and obligation.

**Conclusion:** Topology informs but does not determine business criticality.

### Example 8

**Question:** How should a mapper record `customer_id` when no one can define its population?

**Reasoning:** Record the observed field, source evidence, known uses, and an explicit semantic unknown with owner and resolution priority. Do not infer “all customers” from the name.

**Conclusion:** Honest unknowns are more useful than invented definitions.

### Example 9

**Question:** A sensitive source is tokenized before export. Can the downstream asset be marked nonsensitive automatically?

**Reasoning:** Review reidentification, retained fields, combination risk, purpose, keys, recipient, and applicable policy. A transformation changes evidence, not automatically the governing classification.

**Conclusion:** Policy propagation requires authorized evaluation.

### Example 10

**Question:** When is a landscape fit to support a migration decision?

**Reasoning:** When the decision scope and denominators are explicit, consequential paths have corroborated identities and consumers, material unknowns have been resolved or accepted by authority, and reverse traces, runtime samples, and owner reviews support the claims.

**Conclusion:** Fitness is decision-specific evidence, not universal completion.

## Cross-Program Connections

[Data Engineering](../../19-data-engineering/ROADMAP.md) supplies pipeline, lineage, observability, quality, SLO, lifecycle, and recovery mechanisms whose evidence populates the landscape. The architecture view remains broader because it includes semantics, authority, policy, consumers, and manual or external paths.

[Database Engineering](../../18-database-engineering/ROADMAP.md) explains catalogs, schemas, transactions, logs, replication, backup, and engine behavior. A database inventory becomes architectural only when those physical facts are linked to information identities and stakeholder concerns.

[Software Engineering: Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) contributes system context, components, interfaces, architecture descriptions, and decision records. [Systems Engineering](../../26-systems-engineering/ROADMAP.md) adds system-of-interest boundaries, verification, validation, configuration, lifecycle, and socio-technical stakeholder reasoning.

[Security Engineering](../../25-security-engineering/ROADMAP.md) consumes asset, flow, boundary, identity, threat, control, and evidence views. Security scanning is also an important discovery source, but a vulnerability tool is not a semantic or ownership inventory.

## References

- ISO/IEC/IEEE, [*ISO/IEC/IEEE 42010:2022 — Software, systems and enterprise — Architecture description*](https://standards.ieee.org/ieee/42010/6846/), 2022. Authoritative architecture-description concepts for systems of interest, stakeholders, concerns, viewpoints, views, and models.
- The Open Group, [*The TOGAF Standard, 10th Edition*](https://www.opengroup.org/togaf), 2022, site checked 2026-09-03. Official enterprise-architecture method family, including baseline, target, gap, and transition reasoning.
- W3C, [*Data Catalog Vocabulary (DCAT) — Version 3*](https://www.w3.org/TR/vocab-dcat-3/), W3C Recommendation, 2024. Normative vocabulary distinguishing catalog resources, datasets, distributions, data services, dataset series, and catalog records.
- OpenLineage, [*OpenLineage Object Model*](https://openlineage.io/docs/spec/object-model/), checked 2026-09-03. Official model of dataset, job, run, runtime, and design-lineage events.
- NIST, [*Research Data Framework (RDaF) Version 2.0*](https://doi.org/10.6028/NIST.SP.1500-18r2), NIST SP 1500-18r2, 2024. Lifecycle-oriented research-data vocabulary and guidance, including inventories, provenance, preservation, and organizational roles.
- NIST, [*Cybersecurity Framework (CSF) 2.0*](https://doi.org/10.6028/NIST.CSWP.29), NIST CSWP 29, 2024. Authoritative outcomes covering asset inventories, network data flows, suppliers, roles, risk, protection, detection, response, and recovery.
- NIST, [*Big Data Interoperability Framework: Volume 6, Reference Architecture, Version 3*](https://doi.org/10.6028/NIST.SP.1500-6r2), NIST SP 1500-6r2, 2019. Vendor-neutral roles, interfaces, fabrics, metadata catalogs, and lifecycle data-management components.
- CISA, [*Software Bill of Materials (SBOM)*](https://www.cisa.gov/sbom), checked 2026-09-03. Official guidance for component transparency; useful as an analogy and evidence source for technical composition, not a substitute for data semantics or lineage.

## Exercises

### Exercise 1

Define the decision scope and at least three coverage denominators for mapping data dependencies before retiring a regional customer platform. Include temporal and organizational boundaries.

### Exercise 2

Design an observation schema for the claim “dataset `orders_daily` is owned by Commerce and read by Finance.” Show how catalog, directory, runtime, and interview evidence can disagree without being overwritten.

### Exercise 3

Given declared flows `A -> B -> D` and observed flows `A -> B`, `C -> B`, and `B -> D`, identify findings, validation actions, and limits on any blast-radius conclusion.

### Exercise 4

Propose a discovery and validation strategy for sensitive data used in a quarterly regulatory report that includes a warehouse, a desktop workbook, and a partner file transfer.

### Exercise 5

Design fitness measures and a maintenance process for a federated landscape repository. Address coverage, freshness, conflict, identity, human review, access protection, and change events.

## Answers to the Exercises

### Answer 1

The decision is whether and how to retire the regional platform within a named program horizon while preserving authorized customer operations, reporting, rights, and recovery. Include the region's production and recovery environments, corporate consumers, vendors, partner exchanges, and end-user processes; state exclusions. Observe at least one full seasonal and reporting cycle. Denominators might be all registered platform databases and object stores, all deployed jobs and interfaces tied to platform identities, all named business and regulatory outputs in the retirement register, and all active service identities that access the platform. Report successful examination separately for each population. Assets discovered beyond those frames trigger re-scoping rather than silent exclusion.

### Answer 2

Create stable subject and organization identities. Store each claim as subject, property, value, source, observation time, applicable valid time, authority basis, evidence reference, and confidence. The catalog may assert `semantic_owner=commerce`; the organization directory may show that group dissolved; runtime logs may observe a Finance service read; an interview may explain that Finance receives the output through a shared reporting team. Preserve all claims. Apply a governed ownership rule for the semantic-owner property, resolve organizational aliases, and open a conflict if no currently authorized group accepts the decision. A runtime read supports consumer evidence but does not prove purpose or authorization. Effective values link back to every contributing and dissenting observation.

### Answer 3

The observed `C -> B` edge is undeclared and may represent dynamic configuration, incomplete static analysis, or an unauthorized source. The agreement on `A -> B` and `B -> D` corroborates those edges only for the observed runs and identities. Inspect job versions, configuration, query plans, run windows, and contracts; ask owners about `C`; test other execution paths. Within the observed graph, changes to `A` or `C` may propagate through `B` to `D`. That is not a complete enterprise blast radius because dormant, uninstrumented, manual, external, and misidentified edges may exist.

### Answer 4

Start backward from the submitted report and its accountable authority. Identify workbook versions, formulas, macros, operators, approved submission, review, correction, and retention procedures. Observe warehouse queries and extracts over at least a full quarterly cycle; inspect scheduler and access evidence; resolve the partner endpoint, contract, encryption, recipient, purpose, and acknowledgement. Trace report fields to definitions and sources at the granularity required for regulatory assurance. Map classifications, legal and policy authorities, segregation, access, transfer, preservation, deletion, incident, and recovery controls. Reconcile declared procedures with an observed rehearsal or production cycle. Any inaccessible partner evidence, uncontrolled workbook copy, ambiguous definition, or single-person step remains a named risk requiring authorized disposition; the mapping exercise itself does not certify compliance.

### Answer 5

Define separate coverage measures for registered environments, deployed interfaces, cataloged products, and sampled consequential outputs, each with a denominator and observation window. Track claim freshness by property-specific expiry, unresolved identity collisions, source failures, conflicting effective claims, orphan entities, undeclared runtime edges, and time to adjudication. Require stable namespace rules and preserve aliases and provenance. Domain authorities review semantics and ownership; consumers and operators validate sampled forward and reverse traces; policy authorities review classifications and controls. Restrict sensitive topology and evidence while publishing safe discovery metadata. Trigger updates from deployments, contract and schema changes, new accounts, ownership changes, classifications, incidents, exceptions, and retirement; supplement them with periodic scans. Audit whether change events were ingested and whether sampled reality agrees with published views.
