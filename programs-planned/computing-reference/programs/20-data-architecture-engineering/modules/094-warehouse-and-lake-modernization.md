---
module_id: DARCH-094
program: Data Architecture Engineering
level: 2
module_number: 94
title: Warehouse and Lake Modernization
status: complete
last_verified: 2026-09-03
---

# Warehouse and Lake Modernization

## One-Page Review

### Governing question

How can an organization modernize warehouse and lake estates so named workloads, users, and decisions gain measurable value while semantics, history, policy, service, recovery, economics, transition safety, and eventual retirement remain controlled?

### Essential definitions

- **Warehouse and lake modernization** is the governed change of analytical capabilities, operating models, data products, storage, processing, interfaces, controls, and lifecycle obligations to improve declared outcomes; changing location or product alone is migration, not proof of modernization.
- A **modernization portfolio** is the complete set of workloads, data, consumers, dependencies, platforms, contracts, controls, costs, dispositions, transition states, and closure obligations considered together.
- A **workload disposition** is an evidence-backed decision to retain, repair, retire, archive, rehost, replatform, replace, refactor, consolidate, federate, or rebuild a bounded workload.
- A **modernization unit** is the smallest analytical product, workload, subject area, pipeline, table family, consumer cohort, domain slice, region, or capability that can move and be governed coherently.
- A **semantic continuity claim** states how grain, keys, measures, dimensions, code sets, nulls, time, corrections, history, and consumer decisions remain equivalent or intentionally change.
- A **historical continuity claim** states which population and time range moves, how source snapshots align with subsequent changes, and how completeness, ordering, duplicates, deletes, late facts, and corrections are reconciled.
- **Platform fitness** is observed suitability for named workload scenarios across correctness, latency, freshness, concurrency, isolation, scalability, operability, recovery, policy, interoperability, skills, and cost.
- A **modernization wave** is a bounded set of migration units with a declared outcome, dependency closure, authority, evidence, capacity, cutover, rollback, retirement, and decision owner.
- A **parity envelope** is the declared set of differences between old and new results that are allowed by semantics, timing, precision, policy, or presentation and do not invalidate a consumer decision.
- A **modernization receipt** binds a disposition and wave to its baselines, mappings, evidence, decisions, exceptions, costs, authority changes, retirement, and limitations.
- **Modernization debt** is any temporary duplicate pipeline, representation, adapter, catalog entry, privilege, copy, reconciliation job, capacity reservation, contract, or operating burden with owner, expiry, successor, and removal test.
- **Closure** proves superseded workloads, data paths, access, schedules, credentials, infrastructure, licenses, recovery assets, and authority cannot silently return while required records remain controlled.

### Central model, mechanism, or theorem

Represent a modernization portfolio as:

`M = (O, B, W, S, H, P, G, Q, T, E, C, R, L)`

where `O` is outcomes, users, and decisions; `B` observed current and approved target baselines; `W` workloads, consumers, dependencies, and dispositions; `S` semantics, models, contracts, and interfaces; `H` history, snapshots, changes, corrections, and lineage; `P` storage, processing, serving, metadata, and control planes; `G` ownership, governance, security, privacy, and policy; `Q` quality, service, capacity, resilience, and recovery; `T` transition waves, authority, cutover, and rollback; `E` experiments, reconciliations, adoption, and outcome evidence; `C` cost, commitments, skills, support, and organizational capacity; `R` risk, uncertainty, stop conditions, and replanning; and `L` lifecycle, debt, retirement, and closure. Modernization is established only when the portfolio produces better bounded outcomes than its baseline after transition and lifecycle burdens are counted.

### Critical invariants

- Baseline, target, disposition, workload, product, dataset, contract, semantic version, platform version, wave, evidence, decision, exception, debt, and retirement have stable identities.
- Current, copied, transformed, reconciled, canary, authoritative, degraded, recovered, rolled-back, archived, and closed states remain distinguishable.
- Every workload and dependency has one explicit disposition; “move everything” and unowned residue are not dispositions.
- Grain, keys, measures, dimensions, code sets, nulls, time, history, correction, and consumer interpretation are preserved or changed through an approved versioned contract.
- A snapshot and subsequent changes share a durable consistency boundary, replay model, lineage, and reconciliation population.
- Warehouse, lake, lakehouse, source, archive, and serving choices are justified by workload fitness rather than by one enterprise label.
- Policy, purpose, classification, access, encryption, residency, retention, deletion, audit, and legal-hold obligations survive copy, conversion, replay, failure, rollback, and retirement.
- Performance and cost evidence includes representative volume, skew, concurrency, schedules, failure, recovery, background maintenance, network transfer, and control-plane behavior.
- Cutover changes authority only after semantic, historical, consumer, service, policy, recovery, and operator gates pass.
- Rollback accounts for target-only data and external effects; recovery restores a coherent business state rather than merely restarting compute.
- Modernization debt, double running, commitments, training, support, and retirement are funded and time bounded.
- Closure removes obsolete authority and verifies that restored automation, credentials, catalogs, routes, and recovery artifacts cannot reactivate it.

### Common failures

- Calling a hosting move modernization without specifying an improved user outcome.
- Rebuilding every source object instead of rationalizing workloads and dependencies.
- Converting syntax while silently changing business meaning, history, or time.
- Treating matching row counts or dashboard screenshots as decision equivalence.
- Selecting one target engine for workloads with incompatible service and cost shapes.
- Benchmarking a toy query while excluding concurrency, ingest, maintenance, failure, and recovery.
- Copying data before classification, purpose, residency, retention, deletion, and access controls are ready.
- Moving pipelines but leaving semantic models, reports, extracts, notebooks, partners, and recovery paths behind.
- Cutting over on schedule while reconciliation, consumer, or operator evidence remains incomplete.
- Keeping old platforms “for safety” without owners, expiry, cost, access removal, or nonactivation tests.

### Compact example

A finance warehouse, exploration lake, and eighty dependent reports are not declared a single migration. The organization inventories workloads and discovers that ten reports are unused, five regulatory extracts require exact historical reproduction, and feature engineering needs direct table access. It retires the unused reports, retains one regulated mart until a mandated filing cycle completes, replatforms conformed finance models, refactors ingestion into replayable products, and places feature workloads on governed open tables. A consistent snapshot and change position anchor history; mappings preserve grain, slowly changing dimensions, fiscal calendars, rounding, nulls, and late corrections. Shadow runs compare decision outputs, month-end load, concurrency, policy, lineage, recovery, and full unit cost. Authority moves by consumer cohort only after gates pass. Old jobs, credentials, licenses, backups, and restore automation close under nonactivation tests.

### Connections

[DARCH-003](003-current-state-data-landscape.md), [DARCH-008](008-data-risk-and-criticality.md), [DARCH-019](019-model-versioning.md), [DARCH-027](027-producer-and-consumer-contracts.md), [DARCH-041](041-enterprise-data-warehouse-architecture.md), [DARCH-042](042-data-lake-architecture.md), [DARCH-043](043-lakehouse-architecture.md), [DARCH-050](050-mapping-data-workloads-to-platforms-and-serving-systems.md), [DARCH-067](067-schema-registries.md), [DARCH-079](079-audit-and-provenance-architecture.md), [DARCH-089](089-interoperability-without-a-universal-model.md), [DARCH-092](092-target-state-architecture.md), and [DARCH-093](093-transition-architectures.md) establish the baseline, structures, contracts, evidence, target, and transition mechanics. [DARCH-095](../ROADMAP.md) next concentrates on retiring legacy integration.

## Governing Question

“Move the warehouse to the cloud,” “turn the lake into a lakehouse,” and “consolidate analytics” sound like target architectures. Each hides a portfolio of decisions: which outcomes should improve; which workloads should remain, change, combine, or disappear; which meanings and historical behaviors must survive; where each workload belongs; which contracts and consumers change; how policy and recovery operate during coexistence; and which costs and legacy obligations actually end.

The governing question is therefore not where bytes should be copied or which engine should replace another. It is how a governed portfolio can produce better named outcomes through bounded dispositions and transition waves while preserving required truth and service. A rigorous answer inventories the real estate, observes workloads and dependencies, selects a disposition per unit, proves semantic and historical continuity, validates platform fitness under representative conditions, moves authority deliberately, measures adoption and value, and closes every superseded path.

## Why This Matters

The Kimball Group's [data warehouse bus architecture](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/kimball-data-warehouse-bus-architecture/) connects business processes through conformed dimensions while permitting incremental dimensional delivery. Its [four-step dimensional design process](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/four-4-step-design-process/) begins with business process, grain, dimensions, and facts. These sources explain why a warehouse migration cannot be validated by table names alone: analytical meaning depends on grain, keys, measures, dimensions, and process scope.

Apache Parquet's [overview](https://parquet.apache.org/docs/overview/) describes a column-oriented file format designed for efficient storage and retrieval, with compression and encoding. A format can improve interoperability and scan economics, but file readability does not establish table transactions, semantic compatibility, policy enforcement, workload fitness, or lifecycle ownership.

The Apache Iceberg [table specification](https://iceberg.apache.org/spec/) defines table metadata, snapshots, manifests, schema and partition evolution, delete representations, sequence numbers, and optimistic concurrency behavior. Such mechanisms can support reliable open-table modernization, yet exact readers, writers, catalogs, maintenance, policy, and recovery behavior still require testing.

The Delta Lake [transaction-log protocol](https://github.com/delta-io/delta/blob/master/PROTOCOL.md) specifies how readers and writers interact through versioned actions, features, checkpoints, and table state. The Apache Hudi [timeline documentation](https://hudi.apache.org/docs/timeline/) describes ordered actions and instants supporting table services and incremental processing. These projects illustrate that “lakehouse table” is not one interchangeable behavior: protocols, capabilities, concurrency, maintenance, and engine support differ by version.

PostgreSQL [logical replication](https://www.postgresql.org/docs/current/logical-replication.html) documents publications, subscriptions, initial snapshots, ongoing changes, ordering behavior, restrictions, conflicts, monitoring, and security. Debezium's [architecture documentation](https://debezium.io/documentation/reference/stable/architecture.html) describes log-based connectors, source offsets, schemas, records, and deployment forms. Both support historical-copy-plus-change migration patterns, but neither converts warehouse semantics, makes source mutations domain events, or proves target reconciliation.

Google's SRE chapter on [data integrity](https://sre.google/sre-book/data-integrity/) discusses backups, restores, replication, corruption, validation, and disaster planning. Analytical modernization creates new failure and corruption paths; a target that answers queries but cannot be restored to a coherent, policy-compliant state is not ready.

The Bitol [Open Data Contract Standard](https://bitol-io.github.io/open-data-contract-standard/latest/) provides machine-readable schema, quality, service, role, support, and infrastructure obligations. OpenLineage's [object model](https://openlineage.io/docs/spec/object-model/) identifies datasets, jobs, runs, events, namespaces, names, and extensible facets. Contracts and lineage can preserve accountability across old and new estates, but published metadata must be tested against runtime production and consumer use.

The Open Policy Agent [policy-language documentation](https://www.openpolicyagent.org/docs/policy-language) describes structured policy decisions over runtime input. The OpenTelemetry [specification](https://opentelemetry.io/docs/specs/otel/) standardizes telemetry signals, resources, context, and semantic conventions. Common policy and observation planes can span warehouse and lake systems, provided enforcement points, identities, defaults, sampling, batch correlation, and failure behavior are explicitly designed.

NASA [Product Transition](https://www.nasa.gov/reference/5-5-product-transition/) emphasizes readiness of the product, receiving site, operators, users, documentation, and transition work products. This systems view matters because data modernization changes people, procedures, support, controls, contracts, and recovery—not only technology.

NIST [SP 800-160 Volume 1 Revision 1](https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final) applies systems-security engineering across the lifecycle of trustworthy secure systems. Temporary copies, broader connectivity, new identities, conversion tools, suppliers, and retained legacy paths expand the attack and privacy surface during modernization.

The FinOps Foundation's [FinOps Framework](https://www.finops.org/framework/) joins engineering, finance, product, leadership, procurement, and other roles around usage, cost, value, optimization, governance, and technology decisions. Warehouse and lake economics must include double running, transfer, storage classes, idle capacity, burst compute, background maintenance, support, commitments, licensing, migration, recovery, and exit.

Together these sources support dimensional continuity, open storage and table mechanics, snapshot and change movement, recoverability, explicit contracts and lineage, policy, observability, readiness, lifecycle security, and value-aware economics. They do not select a disposition, establish business equivalence, guarantee engine interoperability, prove representative performance, authorize a policy, validate a cutover, or demonstrate realized value. Those conclusions require local owners, observed dependencies, production-shaped evidence, reconciliations, consumer decisions, recovery exercises, costs, incidents, and outcomes.

## Prerequisites and Retrieval

You should understand warehouse, lake, lakehouse, dimensional modeling, normalized and denormalized models, data vault, table formats, columnar files, catalogs, schemas, semantics, batch and streaming, change capture, replication, transactions, lineage, contracts, quality, security, privacy, workload management, query planning, recovery, distributed systems, migration, platform engineering, cost allocation, and retirement.

Retrieve modernization, migration, portfolio, disposition, modernization unit, business process, grain, fact, dimension, conformance, subject area, workload class, dependency, lineage, contract, historical continuity, parity envelope, schema conversion, semantic conversion, query conversion, snapshot, change position, dual run, shadow validation, platform fitness, benchmark, wave, cutover, rollback, recovery, debt, adoption, value, retirement, and closure.

As a retrieval test, inspect an estate with a finance warehouse, departmental marts, an object-store lake, hundreds of jobs, reports, extracts, notebooks, machine-learning features, and partner feeds. Ask which decisions each artifact supports; which objects are actually used; which calendars, keys, dimensions, measures, nulls, and corrections define meaning; which jobs depend on undocumented ordering; which history and legal holds must remain; which workloads need concurrency, elasticity, direct files, or predictable serving; which policies apply to temporary copies; how source and target reconcile at a durable position; how month-end and disaster scenarios are tested; what coexistence costs; and which proof removes every old schedule, credential, license, restore image, and route.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish warehouse and lake modernization from relocation, version upgrade, product replacement, and unbounded transformation;
2. build an observed portfolio of workloads, consumers, semantics, dependencies, policies, service, recovery, costs, and legacy burdens;
3. select explicit retain, repair, retire, archive, rehost, replatform, replace, refactor, consolidate, federate, or rebuild dispositions;
4. define modernization units and waves whose outcomes, dependencies, authority, evidence, rollback, and retirement are bounded;
5. preserve or deliberately change grain, keys, measures, dimensions, code sets, time, history, corrections, contracts, and consumer decisions;
6. design snapshot, backfill, change propagation, query conversion, reconciliation, shadow, cutover, rollback, and recovery mechanisms;
7. evaluate warehouse, lake, lakehouse, federation, archive, and serving platforms under production-shaped workload scenarios;
8. govern security, privacy, lineage, quality, retention, deletion, residency, audit, and exceptions through coexistence;
9. evaluate full lifecycle economics, skills, organizational capacity, adoption, outcomes, transition debt, and exit; and
10. produce decision and closure receipts that make progress, residual risk, authority, value, and nonactivation auditable.

## Core Exposition

**Define modernization through outcomes.** State the sponsor, users, affected decisions, present burden, intended improvement, scope, deadline, constraints, evidence horizon, and reconsideration trigger. Faster queries may matter, but so may shorter model lead time, consistent financial reporting, reduced incident exposure, lawful deletion, recoverability, lower unit cost, or the ability to exit unsupported technology. A product installation is an input, not an outcome.

**Separate migration from modernization.** Migration changes location, implementation, or provider. Modernization may change capabilities, interfaces, ownership, operating practices, economics, and lifecycle behavior to improve an outcome. Rehosting can be the correct bounded response to a data-center deadline, but it should not be credited with semantic repair, elasticity, self-service, or cost reduction until evidence shows those results.

**Build the observed portfolio before drawing the target.** Inventory warehouses, marts, lake zones, tables, files, views, streams, semantic models, reports, extracts, notebooks, models, APIs, partner exchanges, schedulers, catalogs, policies, identities, infrastructure, licenses, backups, and recovery automation. Combine configuration evidence with query logs, lineage, schedules, billing, access decisions, incidents, owner interviews, and consumer confirmation. “No known owner” and “not observed in thirty days” are findings, not proof of disuse.

**Identify the workload, not only the object.** A table may support month-end reporting, interactive exploration, feature computation, data exchange, and regulatory evidence with different requirements. Model the workload as consumer, decision, input population, transformation, schedule, interface, service expectation, policy, failure behavior, recovery need, and cost. One physical object may therefore receive multiple migration treatments until dependencies are separated.

**Classify workload shapes.** Distinguish governed recurring reporting, interactive BI, exploratory analysis, data science, feature generation, stream processing, low-latency operational analytics, bulk exchange, archival, regulatory reproduction, and ad hoc investigation. Capture volume, growth, skew, scan selectivity, joins, concurrency, arrival pattern, freshness, retention, mutability, isolation, latency, recovery, and cost sensitivity. “Analytical” is far too broad for placement.

**Discover semantic assets.** Record business processes, grain, natural and surrogate keys, facts, dimensions, hierarchies, calendars, currencies, units, code sets, classifications, metric definitions, valid and transaction time, slowly changing behavior, late arrivals, restatements, corrections, unknown members, null meanings, and aggregation rules. SQL conversion cannot recover definitions that were never made explicit.

**Map dependencies as observed edges.** Include producers, ingestion, staging, transformations, reference data, semantic models, reports, extracts, notebooks, models, APIs, partner transfers, policies, identities, schedules, alerts, recovery jobs, and manual controls. Label each edge by contract, frequency, authority, criticality, evidence, and confidence. Hidden shared files, database links, stored procedures, macros, and calendar dependencies often determine the true migration order.

**Create a baseline of service and economics.** Measure correctness incidents, freshness, latency distributions, concurrency, queueing, retries, missed schedules, recovery time, data loss exposure, operator effort, change lead time, compute, storage, network, software, support, and commitment cost. Include unused reserved capacity, manual reconciliation, shadow systems, and delayed consumer decisions. Without the baseline, target improvement is untestable.

**Assign one disposition per bounded unit.** Retain when current capability remains the best bounded choice. Repair a defect without changing platform. Retire unused or harmful capability. Archive history when active computation is unnecessary but governed retrieval remains. Rehost to meet a location or support constraint. Replatform onto a compatible managed or upgraded environment. Replace a tool or service. Refactor pipelines or models for a new architecture. Consolidate duplicate capabilities. Federate access when movement is unnecessary or prohibited. Rebuild only where desired behavior and evidence justify the cost.

**Record why each alternative lost.** A disposition receipt includes outcome, baseline, dependencies, constraints, selected path, rejected paths, evidence, uncertainty, owner, target, transition, cost, risk, review trigger, and closure. “Cloud first” or “lakehouse standard” does not replace workload-specific reasoning.

**Choose modernization units at semantic seams.** Useful units include a business process and conformed dimensions, a data product and consumers, a subject area, a pipeline family, a report cohort, a partner interface, or a workload class. Units should contain enough meaning and authority to reconcile coherently, but remain small enough for bounded evidence and rollback. Splitting a transaction or conformed dimension arbitrarily creates cross-wave inconsistency.

**Sequence by dependency and learning.** Build a directed dependency graph and identify cycles, common reference assets, shared platforms, critical paths, and resource contention. Start with units that test important assumptions without exposing catastrophic consequence. Do not postpone the only difficult semantic, scale, or regulatory case until after architecture commitment. A wave plan is an evolving dependency-and-evidence model, not a static calendar.

**Design the target as a portfolio.** A modern target may retain a governed warehouse for conformed recurring reporting, open tables for data science and cross-engine processing, streams for event detection, federated access for constrained sources, an archive for infrequent evidence, and specialized serving stores for low latency. Uniform contracts, identity, policy, metadata, lineage, observation, cost allocation, and lifecycle rules can bind heterogeneous execution.

**Preserve dimensional intent.** When modernizing a warehouse, reconstruct the business process, declare grain before facts and dimensions, preserve or version conformed dimensions, define key generation, model slowly changing behavior, and test additive properties. A table with the same columns can change answers if join paths, unknown members, effective intervals, fiscal calendars, rounding, or late-arriving facts differ.

**Modernize lakes as governed products.** Raw, refined, and serving labels are useful only when each zone has purpose, authority, schema policy, quality, ownership, access, retention, deletion, service, lineage, and promotion rules. Copying every source indefinitely creates an expensive evidence and privacy liability. Quarantine malformed inputs, preserve source fidelity where required, and ensure refined products are reproducible from governed inputs.

**Treat table formats as protocols.** Test exact format versions, catalog behavior, reader and writer features, concurrency, snapshots, isolation, schema and partition evolution, deletes, compaction, clustering, metadata growth, orphan cleanup, expiration, encryption, authorization, and recovery. An engine reading files does not mean it safely commits to the table. Unsupported write features can corrupt or strand shared state.

**Separate physical from semantic openness.** Open files or protocols can reduce some provider coupling. Portability also depends on catalog identities, SQL dialects, functions, procedures, orchestration, security, policy, lineage, observability, semantic models, serving interfaces, skills, and egress. Define exit scenarios and exercise them against exact versions rather than claiming openness from file suffixes.

**Plan schema and code conversion as engineering.** Inventory types, precision, collation, time zones, nulls, constraints, keys, defaults, generated values, procedures, user-defined functions, macros, optimizer hints, transaction assumptions, permissions, and error behavior. Categorize conversions as mechanical, behaviorally compatible, intentionally changed, or unresolved. Generated conversion accelerates work but remains untrusted until tested.

**Version semantic changes separately.** A migration is already complex; changing metric meaning at the same boundary makes discrepancy diagnosis harder. When semantics must change, publish old and new definitions, mappings, applicability intervals, consumers, expected differences, validation, approval, and sunset. Never hide a business redefinition in syntax conversion.

**Establish historical scope and authority.** State the first retained instant, latest source position, inclusion and exclusion rules, deleted and corrected records, legal holds, archive boundary, current authority, and reconstruction method. Decide whether history is copied, recomputed, summarized, archived, federated, or retired. Every reduction needs authorized purpose and consumer consequences.

**Bind snapshot to subsequent change.** Capture a consistent source snapshot and durable log, sequence, watermark, or replay boundary. Specify transactions, ordering, duplicates, deletes, key changes, schema changes, late events, connector restarts, gaps, overlaps, poison records, source failover, and resnapshot behavior. A bulk copy followed by “turn on CDC” can silently omit or duplicate the boundary.

**Make transformations replayable.** Version code, configuration, schemas, reference data, policy, runtime, dependencies, inputs, positions, clocks, randomness, and outputs. Isolate non-idempotent side effects. Record lineage and checkpoints. Replayability supports correction and recovery, but exact byte reproduction may be impossible or undesirable when sources, algorithms, or lawful retention change; define the required equivalence.

**Reconcile meaning, not only storage.** Define population, keys, source and target positions, time window, exclusions, exact comparisons, tolerances, invariants, aggregates, distributions, referential relationships, lineage, policy decisions, and consumer outputs. Attribute divergences to lag, source defect, target defect, mapping, permitted semantic change, observation error, or unknown. Every class needs owner, correction, recheck, and decision consequence.

**Create parity envelopes explicitly.** Exact equality is appropriate for many identifiers, counts, balances, classifications, and policy decisions. Floating computations, approximate algorithms, time-bound ingestion, and approved semantic changes may require bounded differences. Tolerance must be justified from consumer decision sensitivity, not selected after seeing an inconvenient result.

**Convert queries and consumers as contracts.** Inventory SQL, procedures, semantic models, reports, extracts, notebooks, models, APIs, drivers, authentication, error behavior, schedules, and caches. Test not only whether a query runs, but whether its population, time, joins, nulls, precision, ordering, security, latency, and downstream decision remain correct. Observe each consumer identity through representative cycles.

**Use shadow execution before authority where possible.** Run target pipelines and queries on production-shaped inputs without governing user-visible results or causing unsafe side effects. Compare outputs, lineage, policy, freshness, latency, resource contention, cost, maintenance, and operator behavior. Shadow activity remains production workload and must obey access, purpose, minimization, retention, and capacity controls.

**Benchmark scenarios, not isolated queries.** Include representative volume, growth, skew, file sizes, partitions, joins, concurrency, ingest, updates, deletes, late data, maintenance, metadata operations, cache states, failures, retries, and recovery. Warm and cold results answer different questions. Record exact versions, configurations, data populations, plans, clocks, and cost so results can be reproduced and bounded.

**Test workload isolation and interference.** A target may pass every query separately and fail when ingestion, month-end reporting, exploration, feature computation, compaction, backup, and catalog operations overlap. Exercise priorities, quotas, queues, autoscaling, admission control, noisy neighbors, cancellation, backpressure, and degraded modes. Measure downstream decision delay, not only engine utilization.

**Verify the complete control plane.** Catalog, identity, authorization, secrets, policy, lineage, quality, orchestration, telemetry, billing, configuration, and support services can become common-mode dependencies. Test their latency, availability, consistency, scale, versioning, recovery, and fallback. Decoupled storage and compute do not eliminate control-plane coupling.

**Design policy continuity before copying.** Classify data and lawful purpose; map owners, processors, jurisdictions, residency, minimization, access, encryption, key ownership, masking, row and column rules, retention, deletion, legal holds, audit, incident response, and suppliers. Apply controls to staging, failed loads, snapshots, logs, caches, exports, backups, shadow results, and rollback paths—not only final tables.

**Test policy decisions at enforcement points.** Equivalent policy text can yield different outcomes when identities, attributes, defaults, time, group expansion, data classification, or enforcement coverage differs. Create positive, negative, boundary, expired, revoked, break-glass, and unavailable-control cases. Correlate decisions with data, consumer, contract, and wave identities.

**Carry quality ownership through coexistence.** Define completeness, validity, uniqueness, timeliness, consistency, integrity, distribution, and semantic tests at source, movement, transformation, product, and consumer boundaries. A target may expose an inherited source defect more visibly; classify origin without excusing it. Quality exceptions need owner, affected population, consequence, expiry, and correction.

**Make lineage operational.** Preserve stable dataset, job, run, contract, semantic-version, and consumer identities across old and new paths. Verify coverage and correctness with injected known flows and incidents. Lineage should support impact analysis, reconciliation, policy, correction, recovery, and retirement; a visually dense graph is not itself trustworthy evidence.

**Instrument outcomes and operations.** Collect data volume, freshness, latency, errors, retries, divergence, queue time, resource use, policy decisions, access, adoption, consumer success, change lead time, incidents, recovery, unit cost, and declared business outcomes. Join signals through stable identities and recorded clocks. Sampling must not hide rare but high-impact workloads.

**Engineer cutover as an authority change.** Separate writes, transformations, reads, semantic models, reports, extracts, APIs, and recovery authority when necessary. Declare the exact position and time, owners, prerequisites, freeze or buffer behavior, consumer cohorts, caches, routes, credentials, stop conditions, rollback limit, communication, evidence, and final decision. DNS or scheduler changes are implementation details.

**Plan rollback around new-only state.** After target authority begins, new records, corrections, deletions, classifications, consumer decisions, and external exports may no longer fit the source. Define whether rollback replays target changes, partitions authority, compensates effects, preserves target operation, or becomes unsafe after a point of no return. Test state convergence rather than only route reversal.

**Exercise recovery in every transition state.** Restore source-only, copying, dual-run, canary, target-authoritative, rollback, and post-retirement states. Recover data, metadata, catalogs, keys, policy, orchestration, lineage, semantic layers, consumers, and evidence in dependency order. Validate business invariants and authorized authority after restore. A successful object restore does not prove a usable analytical service.

**Prepare people and receiving systems.** Domain owners, data engineers, database administrators, analysts, modelers, report developers, platform operators, security, privacy, finance, procurement, support, partners, auditors, and consumers need roles, access, skills, procedures, escalation, capacity, and decision rights. Training attendance does not prove operational readiness; exercises and supported work do.

**Count all economics.** Model current baseline, target steady state, transition, incidents, recovery, and exit. Include compute, storage, requests, catalog operations, transfer, egress, licenses, support, tooling, observability, backups, duplicate environments, commitments, engineering, review, training, partner change, and retirement. Normalize by useful workload and outcome, not by raw terabyte alone.

**Distinguish cost optimization from cost displacement.** Lower infrastructure spend may be offset by more engineering, governance, network, supplier, or incident burden. Chargeback can move cost without reducing it. Autoscaling can lower idle capacity but amplify unconstrained consumption. Record allocation confidence, shared costs, forecast error, and unit-cost drivers.

**Manage commitments and exit.** Reservations, minimum spends, support agreements, licenses, network contracts, retention obligations, and specialist skills influence sequencing. Model early termination, overlap, renewal dates, data extraction, conversion, control-plane replacement, and post-exit recovery. A target whose exit is untested has an unpriced lifecycle risk.

**Measure adoption rather than deployment.** A migrated table can coexist with old reports, exports, caches, and analyst routines. Track authorized consumers, workload executions, decisions, support requests, errors, old-path use, contract versions, and outcome changes. Interpret zero traffic carefully: quarterly, disaster, regulatory, and investigation workloads may be rare but essential.

**Control modernization debt.** Inventory every duplicate pipeline, old-new mapping, compatibility view, copy, sync job, comparison query, temporary privilege, exception, flag, reservation, credential, route, support duty, and retained recovery artifact. Each has purpose, owner, cost, risk, dependencies, expiry, successor, removal test, and escalation. Portfolio limits prevent many locally reasonable bridges from becoming a permanent parallel estate.

**Retire by evidence.** Before removal, prove consumers migrated or were authorized to close, required history is preserved, target recovery succeeds, obligations transfer, divergences close, exceptions end, and rollback no longer depends on the asset. Then remove schedules, writers, readers, identities, credentials, policies, catalog entries, monitors, backups, infrastructure, licenses, and support.

**Test nonactivation.** Restore legacy configuration and recovery artifacts in isolation. Persistent authority tombstones, revoked credentials, deny policies, removed routes, expired contracts, and disabled automation should prevent old data or logic from publishing, authorizing, charging, or becoming authoritative. This catches dormant paths that a normal shutdown cannot reveal.

**Measure realized value after closure.** Compare outcomes, service, risk, lead time, adoption, unit economics, incident burden, recovery, and legacy scope with the versioned baseline. Attribute carefully: modernization, demand shifts, policy changes, and organizational changes may overlap. If outcomes do not improve, revisit target assumptions rather than redefining installed capability as success.

**Preserve a modernization receipt.** Bind baseline observations, workload identities, dispositions, target versions, mappings, positions, tests, reconciliations, policy evidence, performance scenarios, costs, consumer confirmations, authority changes, exceptions, incidents, recovery results, retirement, outcome observations, limitations, dissent, and next review. The receipt makes future correction and audit possible without pretending uncertainty vanished.

## Definitions and Notation

Let a modernization portfolio be:

`M = (O, B, W, S, H, P, G, Q, T, E, C, R, L)`.

`O` contains identified users, affected parties, decisions, baseline burdens, intended outcomes, countermetrics, and observation horizons. An outcome claim is `o = (u, d, b, y, m, h, k)`: user `u`, decision or work `d`, baseline `b`, desired change `y`, measure `m`, horizon `h`, and countermetrics `k`.

`B = (b_c, b_t)` contains versioned observed-current and approved-target baselines. A baseline includes logical and physical architecture, workloads, ownership, semantics, dependencies, policy, service, costs, recovery, deployment, and evidence date. Planned diagrams are not observations.

`W = (w_1, ..., w_n)` is the workload portfolio. Each workload `w = (i, u, d, x, f, s, p, q, r, c)` has identity `i`, consumer `u`, decision `d`, inputs and outputs `x`, transformation `f`, schedule or trigger `s`, policy `p`, quality and service `q`, recovery `r`, and cost `c`.

A disposition is:

`disposition(w) in {retain, repair, retire, archive, rehost, replatform, replace, refactor, consolidate, federate, rebuild}`.

Disposition is not a maturity rank. Retain can be correct when change has no justified value; retire can be the most valuable modernization; rebuild can be the worst when it reproduces unwanted behavior.

`S` contains semantic and interface contracts. A semantic claim is `s = (g, k, f, d, z, n, t, h, c, a)`: grain `g`, keys `k`, facts or measures `f`, dimensions `d`, code sets and units `z`, null rules `n`, time semantics `t`, history `h`, correction `c`, and applicability `a`.

`H` contains historical populations, snapshots, change positions, mappings, replay, lineage, corrections, and reconciliation. For snapshot `S_0` and ordered subsequent changes `changes_(p0,p]`, an intended target state may be written:

`T_p = F_v(S_0, changes_(p0,p], R_v, P_v)`,

where `F_v` is versioned transformation, `R_v` is versioned reference data, and `P_v` is versioned policy. This expression is an obligation to define the boundary and versions; it is not proof that every source exposes a total order or that transformation is deterministic.

`P` contains physical and control-plane elements: warehouse, lake, lakehouse, streams, archive, serving systems, storage formats, table protocols, engines, catalogs, orchestration, identity, policy, lineage, telemetry, and administration.

`G` contains owners, decision rights, contracts, security, privacy, classification, purpose, residency, access, encryption, retention, deletion, legal hold, audit, exceptions, and supplier responsibilities.

`Q` contains quality, latency, freshness, availability, concurrency, isolation, capacity, scalability, resilience, data-loss bounds, recovery-time bounds, degraded modes, and support. A platform-fitness claim is indexed by scenario:

`fit(p, w, scenario, v, e)`,

where platform `p` supports workload `w` under `scenario`, exact version and configuration `v`, and evidence `e`. Fitness does not generalize automatically to other workloads, versions, data shapes, or failure conditions.

`T` contains modernization units, waves, dependency ordering, authority states, exposure, cutover, rollback, and retirement. Authority is a function:

`A(f, d, u, time) -> (writer, reader, semantics, policy, clock, correction)`,

for fact or decision `f`, data population `d`, consumer `u`, and time interval `time`.

`E` contains inventory confidence, experiments, benchmark records, reconciliations, consumer confirmations, adoption, incidents, outcome observations, and limitations. A parity envelope `Pi` defines allowed differences:

`equiv(old, new, Pi, D, time)`,

for named population `D` and interval `time`. The envelope must derive from semantics and decision sensitivity before results are judged.

`C` contains baseline, transition, target, recovery, and exit economics; staffing and skills; capacity; contracts and commitments; support; and organizational readiness. Full lifecycle cost is:

`C_L = C_current + C_transition + C_target + C_risk + C_exit - C_avoided`.

Terms require horizons and uncertainty ranges. Adding them does not make forecasts precise or prove value.

`R` contains assumptions, dependencies, uncertainty, risks, countermetrics, thresholds, pause and stop conditions, rollback limits, points of no return, dissent, and replanning triggers.

`L` contains modernization debt, successors, expiry, archive, retention, retirement, nonactivation, evidence preservation, and closure. Closure is a tested state, not a project date.

A modernization wave `v` is admissible only if:

`Admit(v) = O_v ∧ D_v ∧ S_v ∧ H_v ∧ Q_v ∧ L_v`,

where `O_v` binds an outcome, `D_v` closes known dependencies, `S_v` establishes semantic continuity or approved change, `H_v` establishes historical reconciliation, `Q_v` supplies service and recovery evidence, and `L_v` funds retirement and closure. These six predicates are necessary gates in this model, not proof of universal sufficiency.

A modernization value claim compares the completed portfolio with its baseline:

`V(M) = outcome_change - C_transition - C_residual - R_residual`.

The expression is a reasoning scaffold. Outcomes, cost, and risk are multidimensional, differently timed, and often not commensurable; mandatory policy and safety gates cannot be traded away by a high aggregate score.

## Mechanisms, Invariants, or Proof Structure

The assurance argument proceeds from observed portfolio to closed legacy authority. Each gate emits evidence and names who may accept residual uncertainty.

**Charter gate.** Bind sponsor, users, decisions, baseline burden, desired outcomes, countermetrics, scope, deadline, constraints, authority, evidence horizon, and reconsideration triggers.

**Inventory gate.** Identify workloads, data, semantics, consumers, schedules, interfaces, dependencies, owners, policies, service, recovery, infrastructure, licenses, costs, evidence, and confidence.

**Disposition gate.** Assign each bounded workload retain, repair, retire, archive, rehost, replatform, replace, refactor, consolidate, federate, or rebuild with rationale, alternatives, uncertainty, owner, and review date.

**Semantic gate.** Version business process, grain, keys, measures, dimensions, code sets, units, nulls, time, history, correction, transformations, interfaces, applicability, and approved changes.

**Dependency gate.** Close known producer, transformation, reference, consumer, policy, identity, schedule, network, platform, recovery, and human dependencies for the proposed wave.

**Historical gate.** Bind population, snapshot, change position, schemas, mappings, ordering, duplicates, deletes, late data, corrections, lineage, exclusions, replay, reconciliation, and archive.

**Target-fitness gate.** Test exact formats, protocols, engines, catalogs, versions, configurations, volumes, skew, concurrency, ingest, queries, maintenance, failure, recovery, interoperability, and exit for named workloads.

**Contract gate.** Verify producers, schemas, semantics, behavior, quality, service, policy, support, compatibility, consumers, change, deprecation, and closure.

**Policy gate.** Govern purpose, classification, ownership, identity, access, encryption, residency, minimization, retention, deletion, legal hold, audit, incidents, suppliers, exceptions, and temporary copies.

**Lineage gate.** Preserve stable dataset, job, run, semantic, contract, consumer, and wave identities; test coverage, correctness, impact analysis, correction, recovery, and retirement use.

**Conversion gate.** Classify schema, type, SQL, procedure, orchestration, report, semantic-model, driver, authentication, and error conversions as mechanical, compatible, deliberately changed, or unresolved.

**Reconciliation gate.** Define population, position, interval, keys, equality, tolerances, invariants, aggregates, distributions, policy, lineage, consumer outputs, divergence classes, owners, correction, and recheck.

**Performance gate.** Exercise representative volumes, growth, skew, schedules, concurrency, ingest, query, maintenance, metadata, caches, interference, failures, recovery, plans, clocks, and costs.

**Exposure gate.** Bound shadow or canary users, workloads, data classes, jurisdictions, side effects, duration, control, sample, countermetrics, expansion, pause, stop, and rollback.

**Service gate.** Verify correctness, freshness, latency, availability, capacity, isolation, backpressure, dependencies, degraded modes, support, incidents, data-loss bounds, and recovery-time bounds.

**Recovery gate.** Restore data, metadata, schemas, catalogs, keys, policy, orchestration, lineage, semantic layers, consumers, and evidence in every relevant transition state.

**Authority gate.** Allocate writers, transformations, reads, semantics, policy, clocks, correction, cutover, rollback, incident, and closure decisions by population, consumer, and time.

**Consumer gate.** Demonstrate correct behavior for reports, extracts, notebooks, models, APIs, partners, caches, schedules, rare cycles, restored clients, and named human decisions.

**Economics gate.** Count current, transition, target, incident, recovery, and exit costs; attribute shared usage; model commitments, forecast uncertainty, skills, support, and avoided legacy burden.

**Readiness gate.** Prepare owners, engineers, modelers, analysts, operators, security, privacy, finance, procurement, support, partners, auditors, consumers, access, documentation, exercises, and decision rights.

**Wave gate.** Bind units, dependencies, capacity, outcome, authority, evidence, change window, freeze or buffer, cohort, communication, thresholds, cutover, rollback, successor, and retirement.

**Rollback gate.** Account for target-only state, mappings, missed changes, consumers, contracts, policies, capacity, external effects, correction, evidence, and point of no return.

**Adoption gate.** Observe authorized use, decisions, contract versions, support, errors, old-path activity, periodic workloads, outcome measures, and countermetrics across a sufficient horizon.

**Debt gate.** Give each duplicate path, mapping, view, copy, sync, comparison, privilege, exception, credential, route, capacity reservation, and support duty an owner, cost, risk, expiry, successor, and removal test.

**Retirement gate.** Prove consumer closure or migration, preserved history, transferred obligations, target recovery, closed divergence and exceptions, and independence from rollback before removal.

**Nonactivation gate.** Restore obsolete configurations in isolation and verify revoked credentials, deny controls, removed routes, authority tombstones, expired contracts, and disabled automation prevent reactivation.

**Outcome gate.** Compare service, risk, lead time, adoption, unit cost, incidents, recovery, legacy burden, and user outcomes with the versioned baseline; record attribution limits and replan when claims fail.

**Receipt gate.** Bind every baseline, disposition, mapping, version, position, test, result, divergence, policy decision, cost, consumer confirmation, authority change, exception, incident, recovery, retirement, outcome, limitation, and review trigger.

### Executable evidence: modernization-wave admission

The following program classifies ten invented modernization waves against six mandatory gates.

<!-- bijux-verify: {"id":"modernization-wave-admission","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"waves=10\nadmissible=4\nmissing_outcome=1\nunknown_dependency=1\nsemantic_gap=1\nunreconciled_history=1\nunproven_service=1\nmissing_retirement=1\nmodernization_strategies=8\nworkload_classes=9\ntarget_zones=5\nwave_receipts=10\ndecision_events=10\n","stderr":""}} -->
```python
waves = [
    {"strategy": "replatform", "workloads": {"reporting", "finance"}, "zone": "warehouse", "outcome": True, "dependencies": True, "semantics": True, "history": True, "service": True, "retirement": True},
    {"strategy": "refactor", "workloads": {"exploration", "ml"}, "zone": "lakehouse", "outcome": True, "dependencies": True, "semantics": True, "history": True, "service": True, "retirement": True},
    {"strategy": "retire", "workloads": {"operations"}, "zone": "archive", "outcome": True, "dependencies": True, "semantics": True, "history": True, "service": True, "retirement": True},
    {"strategy": "federate", "workloads": {"partner"}, "zone": "source", "outcome": True, "dependencies": True, "semantics": True, "history": True, "service": True, "retirement": True},
    {"strategy": "archive", "workloads": {"archive", "regulatory"}, "zone": "archive", "outcome": False, "dependencies": True, "semantics": True, "history": True, "service": True, "retirement": True},
    {"strategy": "consolidate", "workloads": {"reporting"}, "zone": "warehouse", "outcome": True, "dependencies": False, "semantics": True, "history": True, "service": True, "retirement": True},
    {"strategy": "rehost", "workloads": {"finance"}, "zone": "warehouse", "outcome": True, "dependencies": True, "semantics": False, "history": True, "service": True, "retirement": True},
    {"strategy": "refactor", "workloads": {"streaming", "operations"}, "zone": "lake", "outcome": True, "dependencies": True, "semantics": True, "history": False, "service": True, "retirement": True},
    {"strategy": "replatform", "workloads": {"ml", "exploration"}, "zone": "lakehouse", "outcome": True, "dependencies": True, "semantics": True, "history": True, "service": False, "retirement": True},
    {"strategy": "retain", "workloads": {"regulatory", "partner"}, "zone": "source", "outcome": True, "dependencies": True, "semantics": True, "history": True, "service": True, "retirement": False},
]

def evaluate(wave):
    if not wave["outcome"]:
        return "missing_outcome"
    if not wave["dependencies"]:
        return "unknown_dependency"
    if not wave["semantics"]:
        return "semantic_gap"
    if not wave["history"]:
        return "unreconciled_history"
    if not wave["service"]:
        return "unproven_service"
    if not wave["retirement"]:
        return "missing_retirement"
    return "admissible"

results = [evaluate(wave) for wave in waves]
print(f"waves={len(waves)}")
for outcome in ["admissible", "missing_outcome", "unknown_dependency", "semantic_gap", "unreconciled_history", "unproven_service", "missing_retirement"]:
    print(f"{outcome}={results.count(outcome)}")
print(f"modernization_strategies={len({wave['strategy'] for wave in waves})}")
print(f"workload_classes={len(set().union(*(wave['workloads'] for wave in waves)))}")
print(f"target_zones={len({wave['zone'] for wave in waves})}")
print(f"wave_receipts={len(waves)}")
print(f"decision_events={len(results)}")
```

The output reports ten waves, four admissible and one of each declared failure, eight modernization strategies, nine workload classes, five target zones, ten receipts, and ten decisions.

The evidence is deliberately narrow. Invented Booleans, labels, and sets establish deterministic gate order and counts only. They do not establish that an outcome matters, dependencies are known, semantics are preserved, history reconciles, service and recovery work, retirement is complete, or any warehouse or lake change is safe, economical, or beneficial. Production assurance requires observed portfolios, owner decisions, contracts, mappings, production-shaped data and workloads, exact platform versions, policy tests, reconciliations, failure injection, consumer evidence, cutover and rollback exercises, recovery tests, costs, adoption, incidents, and outcomes.

## Alternatives and Trade-Offs

**Retain and repair.** Current semantic and operational knowledge remains stable, and change risk is low. Unsupported technology, scarce skills, poor service, manual controls, and opportunity cost may persist. Retention should have evidence and a review trigger rather than becoming neglect.

**Retire.** Cost, risk, complexity, and privacy exposure can disappear without migrating unwanted behavior. Rare, hidden, regulatory, investigative, or recovery consumers can be harmed if disuse evidence is weak. Quarantine and reversible observation may be appropriate before destruction.

**Archive.** Active platforms and compute can close while governed history remains retrievable. Retrieval latency, format decay, key loss, policy drift, legal holds, and future reconstruction complexity increase. An archive needs tested discovery, access, restore, interpretation, and deletion.

**Rehost.** Location, support, or data-center deadlines can be met quickly with limited application change. Existing semantics, operating toil, coupling, inefficiency, and scaling behavior remain. Rehost should be labeled honestly and followed by separate outcome evidence.

**Replatform.** A compatible managed or upgraded service can reduce infrastructure burden and improve selected capabilities. Behavioral differences, extensions, optimizer changes, limits, control-plane dependency, and provider coupling still require testing.

**Replace.** A new product can remove unsupported tooling and add capabilities. Query, procedure, orchestration, identity, policy, semantic-model, driver, operational, and commercial incompatibilities can dominate the visible schema work.

**Refactor.** Pipelines, models, products, and interfaces can exploit better architecture and remove inherited defects. Scope, diagnosis, semantic change, new failure modes, and proof burden increase. Refactor should not silently reproduce every historical quirk or rewrite all behavior at once.

**Consolidate.** Duplicate marts, pipelines, tools, catalogs, or storage can share capabilities and lower support burden. Shared blast radius, queues, governance bottlenecks, cross-domain coupling, and migration contention increase. Consolidate capabilities only where common ownership and service are defensible.

**Federate.** Data can remain near authoritative sources or residency boundaries, reducing copy and synchronization. Source load, network variability, connector behavior, snapshot inconsistency, policy coordination, query limits, and recovery complexity can constrain workload fitness.

**Rebuild.** A clean implementation can align with present outcomes and remove obsolete assumptions. Tacit semantics, edge cases, consumer habits, and operational learning are easily lost, while time and cost are high. Rebuild only bounded capabilities whose desired behavior can be specified and validated.

**Warehouse-centered target.** Conformed history, recurring transformation, governed reporting, workload management, semantic serving, and predictable operation can be strong. Data-science access, unstructured data, direct format access, and engine diversity may be constrained or costly.

**Lake-centered target.** Flexible storage, broad data forms, low-cost retention, and varied processing can support exploration and machine learning. Transactions, small-file management, governance, interactive service, semantic coherence, and operational maturity require explicit mechanisms.

**Lakehouse-centered target.** Open-table protocols can combine direct storage access with transactional and management capabilities. Catalog dependency, protocol versioning, writer compatibility, maintenance, metadata scale, and serving behavior create new coupling.

**Deliberately hybrid target.** Workloads can be placed according to actual fitness while sharing contracts, semantics, identity, policy, lineage, telemetry, and lifecycle. Portfolio governance, interoperability, skill breadth, duplicated capability, and cost attribution become harder.

**Large cutover.** Coexistence time, duplicate operation, and bridge debt may be shorter. Blast radius, late discovery, rollback state, consumer coordination, and resource peaks grow.

**Incremental waves.** Evidence, learning, value, and rollback can be bounded. Adapters, double running, authority complexity, total duration, and transition-debt accumulation grow. Smaller is safer only when dependencies and closure remain bounded.

**Exact parity.** Discrepancy diagnosis and consumer trust are simpler where semantics require identity. Intentional improvement, new algorithms, representation changes, and legitimate time effects can be blocked.

**Versioned semantic change.** Defects and obsolete definitions can be corrected transparently. Consumers may need dual definitions, history restatement, governance decisions, explanation, and longer transition.

**Copy all history.** Consumer compatibility and local query autonomy improve. Transfer, storage, policy exposure, deletion burden, invalid legacy records, and duration increase.

**Selective history and archive.** Active cost and migration scope shrink. Cross-boundary queries, reconstruction, legal evidence, model training, and late corrections become more complex.

**Managed proprietary capability.** Operations, integration, and service may improve quickly. Protocol, control-plane, commercial, skills, and exit coupling can grow.

**Open formats and protocols.** Multiple engines and extraction paths may reduce some lock-in. Integration testing, catalog operation, maintenance, support boundaries, and lowest-common-denominator behavior remain organizational responsibilities.

## Failure Modes and Misconceptions

1. **“Cloud location means modernization.”** Relocation does not establish improved outcomes, semantics, service, economics, or lifecycle.
2. **“The new product is the target architecture.”** Ownership, data products, interfaces, policy, operations, consumers, and closure remain design work.
3. **“Everything should move.”** Retain, repair, retire, archive, or federate may produce more value and less risk.
4. **“Everything should be redesigned while moving.”** Combined semantic, platform, and organizational change can exceed diagnostic and rollback capacity.
5. **“The inventory is the catalog export.”** Hidden queries, files, schedules, caches, reports, notebooks, partners, and manual controls remain.
6. **“No recent query means unused.”** Month-end, quarterly, regulatory, disaster, investigation, and restored workloads can be rare.
7. **“One table is one workload.”** Different consumers and decisions can require different service, policy, and migration paths.
8. **“A dependency graph is complete when parsers finish.”** Dynamic SQL, external tools, human procedures, and recovery paths escape static discovery.
9. **“Unknown dependencies can be handled at cutover.”** They create unbounded blast radius and ambiguous rollback.
10. **“A migration wave is a calendar batch.”** It needs coherent semantics, dependency closure, authority, evidence, rollback, and retirement.
11. **“Smaller waves are automatically safer.”** Shared dimensions, transactions, policies, and consumers can make arbitrary splits inconsistent.
12. **“Start only with easy workloads.”** Architecture-threatening scale, semantic, recovery, and regulatory assumptions remain untested.
13. **“One platform fits every analytical workload.”** Concurrency, latency, update, openness, policy, recovery, and cost shapes differ.
14. **“Hybrid means flexible.”** Without allocation and shared-control rules, it means accidental heterogeneity.
15. **“A warehouse is obsolete.”** Conformed recurring reporting and predictable serving may remain valuable.
16. **“A lake is only cheap storage.”** Governed products, schemas, transactions, quality, service, policy, and lifecycle still apply.
17. **“Lakehouse protocols are interchangeable.”** Versioned features, catalogs, deletes, concurrency, maintenance, and engine support differ.
18. **“Readable files mean writable tables.”** Commit protocols and feature compatibility constrain safe writers.
19. **“Open format eliminates lock-in.”** Catalogs, SQL, procedures, policy, orchestration, semantics, skills, and egress can still couple.
20. **“Storage-compute separation removes shared failure.”** Identity, catalog, policy, metadata, and orchestration can be common-mode dependencies.
21. **“Column names preserve semantics.”** Grain, keys, facts, dimensions, time, nulls, corrections, and aggregation determine answers.
22. **“SQL conversion preserves behavior.”** Types, precision, collation, functions, ordering, transactions, and errors can change.
23. **“Modernization is the right moment to hide metric changes.”** Discrepancy diagnosis and consumer trust collapse.
24. **“Every legacy quirk must be reproduced.”** Defects need explicit disposition, not automatic inheritance.
25. **“A row count proves historical parity.”** Keys, populations, values, deletes, intervals, duplicates, and relationships can differ.
26. **“A checksum proves business equivalence.”** Representation can differ legitimately or match while semantics are wrong.
27. **“Tolerance can be selected after comparison.”** It becomes a way to excuse unexplained divergence.
28. **“A snapshot followed by CDC cannot lose data.”** Boundary gaps, overlaps, retention, offsets, failures, and schema changes remain.
29. **“Change records are domain events.”** Storage mutations may omit intent, transaction meaning, and business identity.
30. **“Replay is deterministic by default.”** Reference data, policy, runtimes, clocks, randomness, external calls, and code versions drift.
31. **“Late data is merely an operational delay.”** It changes periods, dimensions, features, decisions, and correction obligations.
32. **“History can be recomputed whenever needed.”** Sources, code, keys, policy, and lawful retention may no longer exist.
33. **“Archive means copy and forget.”** Discovery, interpretation, access, restore, deletion, keys, formats, and ownership decay.
34. **“If the query runs, the consumer migrated.”** Population, meaning, security, latency, errors, schedules, and human decisions may differ.
35. **“Dashboard screenshots prove equivalence.”** Filters, hidden calculations, exports, refresh timing, and downstream use remain.
36. **“A benchmark query proves platform fitness.”** Ingest, concurrency, skew, maintenance, failure, recovery, and cost are excluded.
37. **“Warm-cache results are representative.”** Cold starts, cache contention, invalidation, and periodic work can dominate.
38. **“Autoscaling guarantees capacity.”** Quotas, ramp time, concurrency, dependencies, budgets, and regional limits constrain it.
39. **“Faster queries compensate for policy gaps.”** Mandatory security and privacy controls are not tradeable.
40. **“Copying to a temporary zone needs weaker controls.”** Temporary paths expand attack, privacy, retention, and supplier exposure.
41. **“Equivalent policy code means equivalent enforcement.”** Identity, input, defaults, coverage, and failure modes differ.
42. **“A lineage graph proves coverage.”** Missing or wrong producers can create a persuasive false map.
43. **“Green pipelines mean the migration is healthy.”** Consumers, semantics, policy, recovery, cost, debt, and outcomes can fail.
44. **“Cutover is a scheduler switch.”** Data authority, semantic layers, consumers, controls, and recovery must move.
45. **“Rollback is a routing reversal.”** Target-only state, corrections, deletions, exports, and decisions require convergence.
46. **“Backups prove recoverability.”** Keys, catalogs, policies, schemas, order, procedures, and business invariants must restore.
47. **“Target run cost is the business case.”** Transition, people, network, controls, commitments, incidents, recovery, and exit count.
48. **“Deployment proves adoption.”** Old reports, extracts, notebooks, caches, and habits can retain real authority.
49. **“Keeping the source is free insurance.”** It preserves cost, attack surface, skill burden, ambiguity, and silent reactivation risk.
50. **“Powered off means closed.”** Credentials, routes, schedules, backups, catalogs, licenses, and restore automation can revive authority.

## Worked Examples

### Example 1

A financial warehouse contains 420 reports, but observed execution, report-server logs, owner interviews, and close-calendar review show only 170 active, 25 rare but mandatory, 160 superseded, and 65 unresolved. The organization retires proven duplicates, quarantines unresolved reports, and avoids translating 160 unwanted consumers. The migration unit is a business process plus its conformed dimensions, not an arbitrary table count.

### Example 2

An order fact table is converted with identical column names, yet monthly revenue differs. The target joins a current customer tier while the source used the tier effective at order time. A versioned semantic contract restores the grain, surrogate-key relationship, valid interval, late-arriving behavior, and correction rules before any report gains authority.

### Example 3

A lake modernization copies a snapshot and later starts change capture. Reconciliation exposes a three-minute gap between snapshot completion and the first durable connector position. The team repeats the copy from a transactionally meaningful boundary, tests overlap deduplication, delete handling, schema change, connector restart, source failover, and resnapshot before admitting the wave.

### Example 4

A lakehouse engine can read an open table but cannot write the delete feature enabled by another engine. Rather than advertise multi-engine write compatibility, the architecture names one authoritative writer, tests reader behavior against exact protocol versions, and controls feature upgrades through compatibility evidence and rollback.

### Example 5

Ten representative queries meet latency objectives individually. During month end, ingestion, dimension processing, exploration, compaction, and backup overlap; queue time violates the close deadline. The platform-fitness scenario adds concurrency, skew, maintenance, cold caches, quota limits, failure, recovery, and full cost before target capacity is approved.

### Example 6

A regulated customer dataset is copied into a temporary conversion zone with broad engineer access and no deletion workflow. The wave stops even though data comparisons pass. Classification, lawful purpose, residency, encryption, least privilege, retention, deletion, audit, supplier access, incident response, and snapshot controls are implemented and tested first.

### Example 7

A report query matches source results for daily data but disagrees after a late correction to a prior fiscal period. The parity envelope requires exact balances by fiscal period and permits only documented presentation rounding. Replay with versioned calendar and reference data corrects the historical partition, and the consumer confirms its filing decision.

### Example 8

A canary cohort moves interactive lake queries to a target and shows lower latency. It has not exercised quarter-end reporting, archival retrieval, disaster recovery, or large partner exports. Expansion remains bounded until those delayed scenarios pass instead of generalizing from convenient traffic.

### Example 9

After target authority begins, an analyst creates a new-only classification and a partner export leaves the enterprise. A rollback drill shows the source cannot represent the classification or retract the export. The runbook partitions authority, replays compatible state, compensates the external effect, and marks a point after which roll-forward is safer than full rollback.

### Example 10

A legacy warehouse is shut down, but an isolated recovery exercise restores an old scheduler, credential, and semantic model. Persistent deny rules and authority tombstones prevent publication and access. The test reveals a forgotten support license and network route, both of which are removed before closure evidence is approved.

## Cross-Program Connections

- [Data Engineering](../../19-data-engineering/ROADMAP.md) implements inventory instrumentation, ingestion, backfill, change capture, transformation, table maintenance, reconciliation, quality, lineage, replay, cutover, and retirement.
- [Database Engineering](../../18-database-engineering/ROADMAP.md) grounds schema conversion, transactions, keys, constraints, replication, query behavior, backup, restore, upgrade, performance, and database retirement.
- [Large-Scale Data Systems Engineering](../../21-large-scale-data-systems-engineering/ROADMAP.md) supplies storage, formats, logs, ordering, consistency, distributed queries, streaming, scaling, failure, metadata, and recovery mechanics.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) governs serving interfaces, compatibility, facades, errors, clients, canaries, traffic shifts, deprecation, and consumer evidence.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) provides self-service environments, deployment, policy, identity, telemetry, capacity, cost controls, support, recovery, paved migration paths, and platform closure.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) governs temporary copies, trust boundaries, identity, encryption, suppliers, incidents, retention, rollback, recovery, and secure disposal.
- [Cloud and Infrastructure Engineering](../../30-cloud-and-infrastructure-engineering/ROADMAP.md) connects hosting, landing zones, identity, storage, network, resilience, recovery, cost, provider limits, migration, and exit.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) explains partial failure, ordering, duplication, consistency, clocks, idempotency, convergence, retries, rollback, and replay.
- [Network Engineering](../../24-network-engineering/ROADMAP.md) grounds transfer capacity, routing, segmentation, latency, egress, source load, failure, and cutover in actual paths.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies baselines, requirements, trade studies, integration, transition, configuration, readiness, verification, validation, risk, lifecycle, and disposal discipline.

## References

1. Kimball Group, [Data Warehouse Bus Architecture](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/kimball-data-warehouse-bus-architecture/), incremental dimensional delivery through business processes and conformed dimensions.
2. Kimball Group, [Four-Step Dimensional Design Process](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/four-4-step-design-process/), business process, grain, dimensions, and facts.
3. Apache Parquet, [Overview](https://parquet.apache.org/docs/overview/), column-oriented storage, compression, encoding, and ecosystem context.
4. Apache Iceberg, [Table Specification](https://iceberg.apache.org/spec/), metadata, snapshots, manifests, evolution, deletes, sequence numbers, and concurrency behavior.
5. Delta Lake, [Transaction Log Protocol](https://github.com/delta-io/delta/blob/master/PROTOCOL.md), versioned actions, table state, features, checkpoints, reader behavior, and writer behavior.
6. Apache Hudi, [Timeline](https://hudi.apache.org/docs/timeline/), ordered actions, instants, table services, and incremental processing.
7. PostgreSQL Global Development Group, [Logical Replication](https://www.postgresql.org/docs/current/logical-replication.html), publications, subscriptions, initial snapshots, changes, ordering, conflicts, monitoring, and security.
8. Debezium, [Architecture](https://debezium.io/documentation/reference/stable/architecture.html), log-based connectors, source offsets, records, schemas, and deployment forms.
9. Google, [Data Integrity](https://sre.google/sre-book/data-integrity/), backups, restores, replication, corruption, validation, and disaster planning.
10. Bitol, [Open Data Contract Standard](https://bitol-io.github.io/open-data-contract-standard/latest/), schema, quality, service, roles, support, and infrastructure obligations.
11. OpenLineage, [Object Model](https://openlineage.io/docs/spec/object-model/), dataset, job, run, event, namespace, name, and facet identities.
12. Open Policy Agent, [Policy Language](https://www.openpolicyagent.org/docs/policy-language), structured policy decisions, inputs, rules, tests, and runtime context.
13. OpenTelemetry, [Specification](https://opentelemetry.io/docs/specs/otel/), signals, resources, context, semantic conventions, sampling, compatibility, and versioning.
14. NASA, [Product Transition](https://www.nasa.gov/reference/5-5-product-transition/), product, site, operator, user, documentation, readiness, delivery, and transition work products.
15. NIST, [SP 800-160 Volume 1 Revision 1](https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final), systems-security engineering and trustworthy secure systems across the lifecycle.
16. FinOps Foundation, [FinOps Framework](https://www.finops.org/framework/), cross-functional ownership, usage, cost, value, optimization, governance, and technology decisions.

## Exercises

### Exercise 1

Create a modernization portfolio for a finance warehouse, departmental marts, an object-store lake, recurring reports, notebooks, feature pipelines, and partner extracts. Define outcomes, baseline evidence, workloads, dependencies, semantic assets, policies, service, recovery, costs, dispositions, target allocation, waves, and closure.

### Exercise 2

Design semantic and historical continuity for moving an order subject area. Include business process, grain, keys, facts, dimensions, time, nulls, late arrivals, corrections, snapshot, change position, mapping versions, reference data, replay, parity envelope, reconciliation, and consumer decisions.

### Exercise 3

Specify a platform-fitness trial comparing a warehouse and lakehouse for recurring reporting, exploration, feature generation, and partner exchange. Cover exact versions, formats, table protocols, catalogs, data shapes, concurrency, maintenance, policy, lineage, failures, recovery, cost, limits, and decision rules.

### Exercise 4

Design a modernization wave from shadow execution through cutover and rollback. Address authority, workload and consumer cohorts, side effects, security, privacy, service, delayed cycles, reconciliation, operator readiness, target-only state, external effects, recovery, stop conditions, and evidence.

### Exercise 5

Write modernization-debt, retirement, and outcome plans for a superseded warehouse and lake. Include pipelines, schemas, tables, reports, semantic models, copies, privileges, credentials, routes, schedules, catalogs, policies, backups, licenses, commitments, support, archive, nonactivation, and value measurement.

## Answers to the Exercises

### Answer 1

Version the observed estate using configuration, queries, lineage, schedules, access, billing, incidents, owner interviews, and consumer confirmation. Describe each workload by user, decision, inputs, transformations, schedule, interface, service, policy, failure, recovery, and cost rather than counting objects. Recover business processes, grain, keys, facts, dimensions, code sets, time, history, corrections, and metric definitions. Map producers, reference data, jobs, reports, extracts, notebooks, models, partners, controls, identity, people, and recovery. Establish outcome and service baselines. Assign each coherent unit an owned retain, repair, retire, archive, rehost, replatform, replace, refactor, consolidate, federate, or rebuild disposition with alternatives and uncertainty. Allocate governed reporting, exploration, features, exchange, and archives to platforms by evidence. Sequence dependency-closed waves and fund coexistence, rollback, recovery, debt removal, old-path nonactivation, and post-closure outcome comparison.

### Answer 2

Declare the order business process and atomic grain before mapping fields. Version natural and surrogate keys, measures and additivity, dimensions and hierarchies, currencies and units, fiscal and event time, null and unknown members, slowly changing intervals, late-arriving facts, deletions, restatements, and correction authority. Capture a consistent snapshot and durable change position; define transaction boundaries, ordering, duplicates, key changes, schema evolution, gaps, overlaps, restart, failover, and resnapshot. Bind transformation code, schemas, reference data, calendar, policy, runtime, and lineage versions. Define exact invariants plus preapproved tolerances based on consumer decision sensitivity. Reconcile named populations and periods by keys, values, relationships, aggregates, distributions, policy, lineage, reports, extracts, and decisions. Attribute, correct, replay, and recheck every divergence class before authority changes.

### Answer 3

Select production-shaped populations covering normal and peak volume, growth, skew, wide and narrow scans, joins, ingest, updates, deletes, late data, concurrent reports, exploration, feature computation, partner exports, compaction, metadata operations, backup, and cold starts. Record exact engines, formats, table-protocol and catalog versions, configuration, identities, policies, schemas, plans, clocks, and prices. Test reader and writer compatibility, concurrency, evolution, deletes, maintenance, lineage, policy enforcement, control-plane failure, network loss, quota exhaustion, recovery, and exit. Measure correctness, freshness, latency distributions, queues, isolation, capacity, operator work, recovery, and full unit economics. Keep mandatory semantic, security, privacy, and recovery gates outside aggregate scoring; choose workload placement only within the scenarios the evidence actually covers.

### Answer 4

Name the wave's outcome, modernization units, closed dependencies, source and target versions, authority, semantic contract, historical boundary, policies, capacity, consumers, owner, evidence horizon, and retirement condition. Shadow production-shaped work with unsafe side effects disabled and controlled data purpose, access, retention, and deletion. Reconcile meaning, history, policy, lineage, service, costs, and decision outputs. Canary representative workload, consumer, data-class, jurisdiction, and schedule cohorts with countermetrics, pause, stop, and expansion rules. Exercise delayed close and regulatory cycles. Prepare operators and consumers through access and recovery drills. Record the cutover position and separate write, transformation, read, semantic, report, and recovery authority as needed. Test rollback with target-only records, corrections, deletions, external exports, compensation, state convergence, and an explicit point of no return.

### Answer 5

Inventory every source and bridge pipeline, mapping, schema, table, file, view, report, semantic model, notebook, extract, sync, comparison, catalog entry, policy, copy, privilege, identity, credential, route, schedule, alert, backup, recovery image, capacity reservation, license, commitment, runbook, and support duty. Give each purpose, owner, dependency, cost, risk, required history, successor, expiry, removal test, and evidence. Confirm all consumers migrated or were authorized to close; archive required history with tested discovery, access, interpretation, restore, retention, deletion, and key custody. Prove target recovery and close divergences, exceptions, contracts, billing, and support. Remove obsolete authority, then restore old automation in isolation to verify tombstones, revoked credentials, deny rules, and removed routes prevent reactivation. Compare adoption, service, risk, lead time, incident burden, recovery, unit cost, legacy closure, and user outcomes with the baseline while recording attribution limits.
