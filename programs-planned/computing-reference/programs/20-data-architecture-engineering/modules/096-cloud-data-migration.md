---
module_id: DARCH-096
program: Data Architecture Engineering
level: 2
module_number: 96
title: Cloud Data Migration
status: complete
last_verified: 2026-09-03
---

# Cloud Data Migration

## One-Page Review

### Governing question

How can an organization move data capabilities to, from, or between cloud environments while preserving required meaning, state, policy, service, recovery, economics, authority, and exit—and proving outcomes beyond the fact that bytes arrived?

### Essential definitions

- **Cloud data migration** is the governed movement and transition of data, metadata, schemas, processing, interfaces, controls, operations, and authority between source and cloud locations or between cloud locations.
- A **migration driver** is a named outcome, constraint, or lifecycle event—such as resilience, lead time, capacity, data-center exit, regional presence, service end, cost, or regulation—that justifies change.
- A **cloud foundation** is the receiving environment's resource hierarchy, identity, network, policy, key management, logging, observability, configuration, billing, support, recovery, and deployment capability.
- A **migration unit** is the smallest product, workload, dataset family, service, consumer cohort, tenant, jurisdiction, region, or capability that can move and be governed coherently.
- A **location state** records where each authoritative, derived, staged, cached, backed-up, logged, archived, and recovery copy exists, may execute, and may be accessed at a given time.
- A **transfer path** is the bounded online or offline mechanism—including network, replication, change capture, export/import, managed service, or physical appliance—that moves an identified population under integrity and custody controls.
- A **consistency boundary** binds an initial snapshot or export to subsequent changes through a durable source position, ordering, retry, deduplication, and reconciliation model.
- A **cloud equivalence claim** states which semantics, behaviors, policies, service properties, recovery outcomes, and consumer decisions remain equivalent or deliberately change.
- A **landing constraint** is a mandatory condition on accounts, projects, regions, networks, identities, keys, policies, observability, quotas, suppliers, or operations that must hold before data arrives.
- A **migration wave** is a bounded set of units with a driver, dependency closure, source and target versions, authority, transfer plan, evidence, cutover, rollback, recovery, successor, and closure.
- **Data gravity** is the combined influence of data volume, velocity, dependencies, computation, consumers, policies, locality, network, and cost on feasible placement and movement.
- An **exit path** is a tested means to extract or transfer data, metadata, contracts, policies, keys, logs, and operational capability away from a provider, region, service, or account without losing required meaning or evidence.
- A **migration receipt** binds the driver, baselines, units, locations, contracts, positions, transfer custody, evidence, decisions, authority, costs, incidents, rollback, recovery, retirement, exit, and limitations.

### Central model, mechanism, or theorem

Represent a cloud data migration as:

`C = (O, B, W, P, X, D, G, Q, T, E, K, R, L)`

where `O` is outcomes, users, constraints, and affected decisions; `B` is observed source and approved target baselines; `W` is workloads, data products, consumers, dependencies, and migration units; `P` is provider, service, deployment, region, account, control-plane, and responsibility architecture; `X` is transfer paths, capacity, custody, positions, and integrity; `D` is data, metadata, semantics, state, history, replay, and reconciliation; `G` is ownership, identity, security, privacy, residency, sovereignty, and policy; `Q` is quality, performance, resilience, recovery, support, and operability; `T` is wave, coexistence, authority, cutover, rollback, and retirement; `E` is experiments, telemetry, lineage, consumer acceptance, and outcome evidence; `K` is cost, commitments, suppliers, skills, and organizational capacity; `R` is risk, assumptions, stop conditions, and replanning; and `L` is lifecycle, debt, archive, disposal, exit, and closure. A completed transfer is not a completed migration until authoritative operation, recovery, lifecycle, and user outcomes are accepted.

### Critical invariants

- Provider, tenant, account, project, subscription, region, zone, network, identity, key, dataset, contract, source position, wave, authority, evidence, exception, archive, and exit version have stable identities.
- Source, staged, copied, transformed, replicated, shadowed, authoritative, degraded, recovered, rolled-back, archived, deleted, and closed states remain distinguishable.
- Service and deployment model identify responsibility boundaries; “the provider handles it” is never a control allocation.
- Every data and metadata copy has purpose, owner, classification, jurisdiction, access, encryption, key custody, retention, deletion, lineage, and lifecycle state.
- Snapshot or export and subsequent changes share a durable consistency boundary, ordering model, deduplication identity, replay method, and reconciliation population.
- Semantics, schemas, time, precision, ordering, correction, interfaces, policy, and consumer behavior remain compatible or change through an approved versioned contract.
- Network and offline transfer plans include measured throughput, protocol overhead, retries, checksums, encryption, custody, scheduling, source impact, target ingest, and recovery.
- Cloud foundations, quotas, policies, observability, incident response, support, backup, restore, and failure domains are exercised before production authority moves.
- Cutover changes authority only after state, consumers, policy, capacity, recovery, cost, and operator readiness pass named gates.
- Rollback accounts for target-only state and external effects; recovery reconstructs a coherent business state within accepted loss and time bounds.
- Full economics includes double running, transfer, egress, requests, storage classes, replication, logs, keys, support, commitments, labor, recovery, retirement, and exit.
- Source retirement and provider exit remove obsolete authority while preserving required evidence and proving that restored paths cannot reactivate it.

### Common failures

- Treating a provider account or copied dataset as a migration strategy.
- Selecting region and service before classifying data, residency, sovereignty, latency, recovery, and supplier constraints.
- Copying sensitive data into an unready landing environment with provisional identity, network, keys, policy, or logging.
- Estimating transfer from headline bandwidth while ignoring source read, encryption, protocol, retry, target ingest, and change rate.
- Starting bulk copy and change capture without one durable consistency boundary.
- Assuming compatible SQL, formats, or APIs preserve semantics, ordering, errors, and consumer decisions.
- Testing steady-state queries while omitting quotas, control-plane failure, cross-zone or cross-region loss, restore, and degraded operation.
- Calling provider replication a backup or multi-zone placement a complete disaster-recovery plan.
- Optimizing target run cost while excluding transition, egress, observability, commitments, people, retirement, and exit.
- Deleting the source before successor recovery, rollback, evidence custody, consumer acceptance, and nonactivation are proven.

### Compact example

A regulated customer product moves from an on-premises database to a managed cloud service. The team begins with purpose, data classes, consumers, business-local time, correction rules, residency, recovery, and exit—not a service SKU. A governed account hierarchy, private network path, workload identity, customer-managed key decision, policy tests, logs, quotas, billing, and support are ready before copying. Measured source read and target apply rates define an online snapshot-plus-change plan whose source position, retries, checksums, deletions, schema changes, and custody are explicit. Shadow consumers reconcile identity, consent intervals, decisions, policy, latency, failure, recovery, and unit cost. Authority moves by population after recovery exercises. The old source remains only through a bounded rollback interval, then credentials, routes, replication, backups, licenses, and automation close. An exit exercise exports data, schemas, contracts, positions, and evidence to a neutral environment.

### Connections

[DARCH-003](003-current-state-data-landscape.md), [DARCH-008](008-data-risk-and-criticality.md), [DARCH-027](027-producer-and-consumer-contracts.md), [DARCH-039](039-replication-and-synchronization.md), [DARCH-050](050-mapping-data-workloads-to-platforms-and-serving-systems.md), [DARCH-064](064-lineage-architecture.md), [DARCH-075](075-data-residency-and-sovereignty.md), [DARCH-079](079-audit-and-provenance-architecture.md), [DARCH-092](092-target-state-architecture.md), [DARCH-093](093-transition-architectures.md), [DARCH-094](094-warehouse-and-lake-modernization.md), and [DARCH-095](095-legacy-integration-retirement.md) establish baselines, risk, contracts, movement, placement, location policy, evidence, transition, modernization, and closure. [DARCH-097](../ROADMAP.md) next focuses on migrating data contracts.

## Governing Question

“Move the data to the cloud” compresses dozens of decisions into a destination label. Which user outcome justifies movement? Which service and deployment model changes responsibility? Which data, metadata, workloads, and consumers move together? Which countries and regions may store, process, support, back up, and recover each class? Which identities, networks, keys, policies, quotas, and control planes must exist first? How will an initial copy align with ongoing change? What fails during transfer and cutover? How will the target recover without the source? What does double running cost, and how can the organization leave?

The governing question is therefore not how to upload bytes. It is how to move authority and capability through a controlled, evidence-producing transition while preserving meaning and obligations. The answer begins with business drivers and observed baselines, assigns responsibilities and geography, prepares a secure foundation, chooses migration units and transfer paths, proves state and consumer equivalence, exercises failure and recovery, moves authority deliberately, closes the source, and retains a tested exit.

## Why This Matters

NIST [SP 800-145](https://csrc.nist.gov/pubs/sp/800/145/final) defines essential cloud characteristics, service models, and deployment models. The vocabulary distinguishes on-demand self-service, broad network access, resource pooling, rapid elasticity, and measured service as well as software, platform, and infrastructure services. These properties shape migration opportunity and responsibility, but a service-model label does not establish local architecture fitness.

The NIST [Cloud Computing Reference Architecture](https://www.nist.gov/publications/nist-cloud-computing-reference-architecture) identifies cloud consumer, provider, broker, auditor, and carrier roles and describes provider orchestration, service management, security, and privacy. This prevents responsibility from disappearing behind “managed service”; control ownership, evidence, suppliers, and network carriage still require explicit allocation.

NIST [SP 800-210](https://csrc.nist.gov/pubs/sp/800/210/final) provides general access-control guidance for infrastructure, platform, and software cloud service models. Different service models expose different components and control surfaces, so identity, authorization, administration, enforcement, and audit must be mapped to exact provider and consumer responsibilities.

Google Cloud's [migration overview](https://docs.cloud.google.com/architecture/migration-to-gcp-getting-started) presents migration as planning and executing across environments and points to assessment, foundation, transfer, deployment, validation, optimization, and cost concerns. Its [large-dataset transfer guidance](https://docs.cloud.google.com/architecture/migration-to-google-cloud-transferring-your-large-datasets) discusses online and offline transfer choices, bandwidth, time, and transfer mechanisms. Provider guidance offers concrete considerations, but local measurements and other target environments may differ.

Google Cloud's [migration-plan validation guidance](https://docs.cloud.google.com/architecture/migration-to-google-cloud-best-practices#validate_your_migration_plan) emphasizes validation of a plan before migration. A plan can be internally consistent and still fail under production data, policy, failure, or organizational conditions; validation must include falsifiable local evidence.

AWS Prescriptive Guidance on [SQL Server database migration strategies](https://docs.aws.amazon.com/prescriptive-guidance/latest/migration-sql-server/strategies.html) distinguishes online and offline migration and describes copying, propagating changes, validation, synchronization, and cutover. This gives concrete provider-specific patterns without making online movement lossless or offline downtime acceptable for every workload.

PostgreSQL [logical replication](https://www.postgresql.org/docs/current/logical-replication.html) documents publications, subscriptions, initial snapshots, ongoing changes, ordering behavior, conflicts, restrictions, monitoring, and security. Debezium's [architecture documentation](https://debezium.io/documentation/reference/stable/architecture.html) describes log-based change capture, connectors, source offsets, schemas, records, and deployment forms. Both illustrate online state movement while leaving semantic mapping, policy, target correctness, and consumer acceptance to migration design.

Google's SRE chapter on [data integrity](https://sre.google/sre-book/data-integrity/) discusses backups, restores, replication, corruption, validation, and disaster planning. Cloud replication and availability do not eliminate operator error, application corruption, credential compromise, region loss, dependency failure, or the need to test restoration and business invariants.

The Bitol [Open Data Contract Standard](https://bitol-io.github.io/open-data-contract-standard/latest/) expresses schema, quality, service, role, support, and infrastructure obligations. OpenLineage's [object model](https://openlineage.io/docs/spec/object-model/) identifies datasets, jobs, runs, events, namespaces, names, and facets. Contracts and stable lineage can preserve meaning and accountability across location changes, but declarations and emitted events require runtime validation.

The Open Policy Agent [policy-language documentation](https://www.openpolicyagent.org/docs/policy-language) describes structured policy decisions over runtime input. The OpenTelemetry [specification](https://opentelemetry.io/docs/specs/otel/) standardizes signals, resources, context, and semantic conventions. Shared policy and observation can span source, transfer, and target only when identities, clocks, enforcement points, sampling, offline transfers, and failure behavior are designed.

NIST [SP 800-160 Volume 1 Revision 1](https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final) applies systems-security engineering across the lifecycle of trustworthy secure systems. Migration creates temporary interfaces, privileges, copies, tools, suppliers, and operating states, so security and privacy must cover the transition and disposal as well as the target.

The FinOps Foundation's [FinOps Framework](https://www.finops.org/framework/) joins engineering, finance, product, procurement, leadership, and other roles around usage, cost, value, optimization, governance, and technology decisions. Cloud data economics includes metered services, requests, transfer, egress, replication, logs, discounts, commitments, shared cost, forecast uncertainty, and value—not only a monthly target estimate.

Together these sources support explicit cloud roles and access control, assessed foundations, online and offline transfer, replication, integrity, contracts, lineage, policy, telemetry, lifecycle security, and value-aware economics. They do not select a provider or region, make a residency interpretation, measure usable bandwidth, prove semantic equivalence, validate recovery, establish cost advantage, authorize source destruction, or guarantee exit. Those conclusions require local owners, legal and policy authority, observed data and workloads, experiments, reconciliations, drills, invoices, consumer acceptance, and outcome evidence.

## Prerequisites and Retrieval

You should understand cloud service and deployment models, regions and zones, tenants and accounts, identity, networks, DNS, encryption and keys, storage and databases, replication, change capture, batch and streaming, schemas, semantics, contracts, lineage, security, privacy, residency, sovereignty, quality, observability, quotas, resilience, backup and recovery, distributed systems, cost allocation, transition architecture, and retirement.

Retrieve migration driver, cloud foundation, landing constraint, provider, consumer, broker, carrier, auditor, shared responsibility, region, zone, jurisdiction, data location, processing location, support location, key custody, migration unit, transfer path, online transfer, offline appliance, bandwidth-delay product, change rate, consistency boundary, high-water mark, reconciliation, wave, shadow, cutover, rollback, recovery, data gravity, egress, commitment, exit, and receipt.

As a retrieval test, inspect moving a regulated order and customer estate from an on-premises database and warehouse into a cloud region. Ask which outcomes and constraints justify it; which service model allocates database, host, network, identity, key, backup, and audit duties; where primary, replicas, logs, backups, support access, and recovery may exist; how much source read and change volume the network and target can sustain; which snapshot position anchors change capture; how identity, money, status, consent, time, correction, and deletion map; what happens under link, zone, region, key, quota, catalog, and provider failure; which consumers and operators accept the target; what double running and exit cost; and which evidence allows the source to close.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish cloud migration, rehosting, replatforming, refactoring, replication, backup, modernization, and provider exit;
2. translate migration drivers into bounded outcomes, constraints, baselines, migration units, decision rights, and reconsideration triggers;
3. allocate responsibility across consumer, provider, broker, carrier, auditor, platform, domain, security, privacy, finance, and supplier roles;
4. design cloud foundations spanning hierarchy, identity, network, keys, policy, logging, observability, quotas, billing, support, deployment, and recovery;
5. model primary, replica, staged, logged, backed-up, archived, cached, processed, support, and recovery locations under residency and sovereignty rules;
6. choose online, offline, hybrid, replication, change-capture, export/import, and appliance transfer paths from measured constraints;
7. establish consistent snapshot and change boundaries, semantic mappings, reconciliation, consumer parity, cutover, rollback, and correction;
8. validate target service, failure domains, quotas, recovery, security, privacy, operations, and supplier behavior through production-shaped trials;
9. evaluate transition and lifecycle economics, commitments, egress, data gravity, retirement, portability, and exit; and
10. produce migration receipts that make locations, authority, evidence, residual risk, costs, closure, and outcomes auditable.

## Core Exposition

**Begin with the driver.** Name the sponsor, affected users, decisions, current burden, desired outcome, deadline, countermetrics, constraints, evidence horizon, decision authority, and reconsideration trigger. Drivers may include support end, data-center closure, region access, resilience, scale, lead time, security, cost, or new capability. “Cloud first” is a policy preference, not a workload outcome.

**Separate migration strategies.** Retain leaves a workload in place. Retire ends it. Rehost moves with minimal architecture change. Replatform changes managed infrastructure or engine while preserving much behavior. Repurchase adopts a different service. Refactor changes architecture or implementation. Relocate moves an existing virtualized or managed environment. Archive preserves governed history without active operation. Assign a strategy to each bounded workload rather than to the entire estate by slogan.

**Distinguish migration from modernization.** A hosting move may satisfy a facility-exit or support driver without improving semantics, delivery, or operating model. A replatform can reduce toil while introducing service limits. Refactoring can unlock elasticity or data products while expanding scope and risk. Credit only outcomes that are observed after transition and closure.

**Observe the source baseline.** Inventory data products, schemas, tables, files, logs, messages, metadata, transformations, consumers, interfaces, identities, policies, schedules, service, incidents, recovery, networks, hardware, licenses, costs, and human procedures. Measure volume, growth, change rate, read rate, skew, object count, file sizes, concurrency, latency, freshness, maintenance, backup, restore, and peak cycles. Unknown source behavior becomes migration uncertainty.

**Define migration units by coherent authority.** Useful units include a data product and consumers, a transactional aggregate, a subject area, a workload class, a tenant, a regional population, an interface, or a pipeline family. A unit should preserve semantic and policy integrity while bounding blast radius, capacity, evidence, rollback, and closure. Arbitrary table batches can split transactions, keys, dimensions, and correction authority.

**Map dependencies and data gravity.** Include producers, consumers, joins, reference data, models, APIs, events, reports, partners, network paths, identity, keys, policy, catalog, lineage, recovery, support, suppliers, and manual procedures. Data gravity is not volume alone; high change rates, tight latency, many consumers, large compute, jurisdiction, scarce bandwidth, and exit cost can dominate placement.

**Choose service and deployment models explicitly.** Record whether the target is infrastructure, platform, software, or a composed managed service and whether deployment is public, private, community, hybrid, or multi-cloud. Translate the label into exact components, control surfaces, contracts, limits, evidence, and accountable roles.

**Build a responsibility matrix.** For data, schema, runtime, host, storage, network, identity, keys, policy, logging, vulnerabilities, backup, restore, replication, resilience, incidents, support, retention, deletion, audit, and disposal, assign provider, consumer, platform, domain, security, privacy, supplier, and shared duties. “Shared” must name who acts, who verifies, and what happens when either fails.

**Assess provider and service boundaries.** Identify provider legal entities, service regions, control-plane locations, sub-processors, support access, data movement, backup geography, key dependencies, certification evidence, service objectives, maintenance, quotas, change notice, incident process, deletion, audit, contractual remedies, and exit. Marketing region names are not sufficient location or responsibility models.

**Prepare the cloud foundation before data.** Establish organization and resource hierarchy, accounts or projects, ownership, identity federation, workload identities, network topology, private and public paths, DNS, time, secrets, keys, policy, classification, logging, telemetry, configuration, deployment, quotas, billing, budgets, inventory, support, incident response, backup, recovery, and evidence retention. Provisional foundations harden quickly after copies arrive.

**Treat landing constraints as gates.** Express mandatory policies for allowed regions and services, encryption, key custody, public exposure, network routes, identities, tags, logs, retention, deletion, backup, replication, and budgets as testable controls. Include exceptions with owner, reason, scope, compensating control, expiry, and removal. Deny unsafe arrival rather than discovering it after transfer.

**Design identity before access migration.** Map human, workload, service, partner, break-glass, provider-support, automation, and recovery identities. Replace shared credentials with scoped identities where feasible. Define federation, lifecycle, authentication strength, authorization, separation of duties, approval, revocation, logging, and emergency access. Test cached tokens and source credentials through rollback and retirement.

**Design the network path from measurement.** Record source read capacity, available bandwidth, round-trip time, packet loss, protocol concurrency, encryption overhead, compression, egress controls, firewall and proxy behavior, target ingest, quotas, maintenance windows, and competing traffic. Measure sustained usable throughput over representative intervals instead of applying link speed directly.

**Estimate transfer lower bounds honestly.** For `bytes` and sustained useful throughput `rate`, `time >= bytes / rate`. Add verification, retries, transformation, target apply, scheduling, and outage. If source change rate approaches or exceeds net catch-up rate, an online migration cannot converge without reducing change, increasing capacity, partitioning, or changing the plan.

**Choose online, offline, or hybrid movement.** Online network transfer offers rapid repetition and low physical custody burden but depends on bandwidth, stability, source load, and egress. Offline appliances can move large baselines when networks are insufficient but add export time, chain of custody, encryption, shipping, import, and delayed-change catch-up. Hybrid plans often seed offline and apply changes online.

**Select transport by semantics and risk.** Options include native backup and restore, logical export/import, storage copy, block transfer, database replication, log-based change capture, event replay, application dual-write, managed transfer, federation, and physical appliance. State what each preserves: bytes, schema, transactions, order, history, metadata, permissions, lineage, or application meaning. No transport preserves everything automatically.

**Plan custody end to end.** For online paths, control identities, endpoints, routes, encryption, certificates, keys, temporary storage, logs, operators, retries, and failed payloads. For offline paths, record export environment, device identity, capacity, encryption and key custody, sealing, handling, shipping, locations, receipt, import, wipe, return, destruction, and evidence. Apply classification and minimization to transfer artifacts.

**Inventory every location state.** Record primary, replica, staging, quarantine, transform, cache, log, snapshot, backup, archive, disaster-recovery, support, telemetry, and provider-recovery locations. For each, record data classes, purpose, owner, jurisdiction, service, access origin, key, retention, deletion, supplier, lineage, and lifecycle. “Stored in region A” does not cover processing or support.

**Distinguish residency from sovereignty.** Residency constrains location; sovereignty can involve legal jurisdiction, control, ownership, operator access, keys, suppliers, or capability to operate independently. Translate applicable laws, contracts, policy, and risk decisions into testable architecture claims with named authority. An architect should not invent legal conclusions.

**Model cross-border and remote access.** Copies can cross boundaries through replicas, backups, logs, telemetry, support, incident dumps, exports, caches, and machine-learning services. Remote administration or provider support may matter even when storage remains local. Test data paths and access decisions rather than relying solely on configuration declarations.

**Choose key ownership and recovery deliberately.** Provider-managed, customer-managed, and externally held keys allocate control and failure differently. Define creation, access, rotation, versioning, replication, backup, escrow if allowed, revocation, incident use, disaster recovery, deletion, audit, and provider dependency. Stronger customer control can also create self-inflicted unavailability if recovery is weak.

**Bind snapshot to subsequent change.** Capture a consistent snapshot or export and a durable log, sequence, watermark, or replay position. Specify transaction boundaries, ordering, duplicates, deletes, key changes, schema changes, late data, gaps, overlaps, retry, connector restart, source failover, target outage, retention, and resnapshot. A bulk copy plus “start CDC” can lose the boundary.

**Avoid casual dual writes.** Writing independently to source and cloud targets introduces partial failure, ambiguous commit, retry duplication, and ordering conflicts. Prefer one authoritative writer plus change propagation where possible. When dual writes are unavoidable, define transaction identities, idempotency, conflict resolution, reconciliation, compensation, and bounded duration.

**Preserve semantics, not only bytes.** Version grain, keys, types, precision, collation, units, currencies, code sets, nulls, time zones, valid and transaction time, history, deletes, corrections, constraints, reference data, aggregation, and consumer interpretation. Provider conversion tools accelerate syntax and type mapping but do not authorize semantic loss.

**Migrate metadata and control state.** Schemas, catalogs, contracts, lineage, quality rules, policies, tags, classifications, owners, schedules, checkpoints, offsets, secrets, configurations, semantic models, dashboards, alerts, budgets, and recovery procedures are part of the capability. Moving data alone creates an unmanaged copy.

**Make transformations replayable.** Version code, configuration, runtime, dependencies, schemas, reference data, policy, positions, clocks, randomness, inputs, and outputs. Isolate side effects and preserve lineage. Define whether equivalence means identical bytes, identical values, identical invariants, or equivalent consumer decisions.

**Reconcile named populations.** Compare source and target at identified positions and time intervals using keys, exact values, tolerated representations, aggregates, distributions, referential relationships, sequences, deletes, policy decisions, lineage, and consumer outputs. Attribute divergence to lag, source defect, target defect, transformation, approved change, observation error, or unknown; correct and recheck.

**Migrate interfaces and consumers.** Inventory applications, queries, reports, notebooks, models, APIs, events, files, partners, drivers, endpoints, DNS, credentials, caches, schedules, errors, and human procedures. Test meaning, authentication, authorization, latency, failure, retries, and recovery. Observe actual consumer execution through representative business cycles.

**Shadow before authority.** Run target processing or reads on production-shaped data with unsafe side effects disabled. Compare state, decisions, policy, lineage, quality, latency, capacity, cost, maintenance, incidents, and operator behavior. Shadow copies remain governed data with purpose, access, retention, deletion, and residency obligations.

**Test production-shaped load.** Include normal and peak volume, growth, change rate, object count, skew, concurrency, ingest, queries, maintenance, backup, compaction, metadata, cold starts, caches, failures, retries, autoscaling, and quotas. Measure complete workload and decision latency, not only target CPU or one query.

**Treat quotas and control planes as dependencies.** Account, region, API, request, connection, object, throughput, key, log, policy, catalog, and support limits can prevent scaling or recovery. Test quota discovery, increase lead time, exhaustion, throttling, retries, failover, degraded operation, and billing consequences. A data plane can be healthy while its control plane blocks change.

**Map failure domains.** Distinguish process, node, rack, zone, region, account, identity, key, network, DNS, control plane, provider, supplier, and operator failure. Multi-zone service does not automatically protect against region, account, policy, credential, or application corruption. Document which mechanisms address which faults and which remain.

**Separate availability, replication, backup, and recovery.** Replication can improve availability while propagating corruption or deletion. Backups preserve selected historical states but require keys, catalogs, software, and restore procedures. Disaster recovery adds alternate capacity, dependencies, authority, and operation. Exercise business recovery rather than inferring it from a provider feature.

**Define loss and recovery objectives by decision.** Set acceptable data loss and recovery time for each product, workload, and business process, including metadata, identity, policy, and consumer recovery. Verify actual restore, replay, validation, catch-up, traffic shift, degraded service, and return. Provider objectives and internal objectives are different claims.

**Prepare cutover as authority transfer.** Record exact source and target positions, clocks, schemas, policies, credentials, owners, freeze or buffer behavior, consumer cohorts, capacity, communication, stop conditions, rollback limit, and approval. Separate writes, reads, transformations, interfaces, reports, and recovery authority when needed.

**Plan rollback around cloud-only state.** After target authority begins, new data, corrections, deletes, identities, policies, external messages, and consumer decisions may not fit the source. Decide whether to replay target changes, partition authority, compensate effects, retain target operation, or cross a point after which roll-forward is safer. Test convergence, not only connection-string reversal.

**Exercise recovery during every transition state.** Test source-only, copying, change catch-up, shadow, canary, target-authoritative, rollback, and source-retired configurations. Restore data, metadata, identity, keys, network, DNS, policy, lineage, orchestration, consumers, and evidence in dependency order. Verify authority and business invariants after restore.

**Prepare operators and support.** Domain owners, database and data engineers, platform and network teams, security, privacy, legal, finance, procurement, service desk, incident responders, provider support, partners, and consumers need access, skills, runbooks, decision rights, escalation, capacity, and exercises. Certificates and training attendance do not prove readiness.

**Instrument the migration.** Track bytes and objects discovered, read, sent, received, verified, transformed, applied, rejected, retried, quarantined, reconciled, corrected, and deleted; positions and lag; transfer and target rates; policy decisions; consumer use; service; incidents; costs; and outcomes. Stable identities and clocks connect evidence across environments.

**Count full lifecycle economics.** Include assessment, foundation, connectivity, appliances, egress, ingress where charged, requests, transfer tooling, duplicate storage and compute, replication, logs, keys, observability, support, discounts, commitments, engineering, security, privacy, legal, incidents, recovery, retirement, and exit. Compare against an observed source baseline and normalize by useful workload and outcome.

**Model price uncertainty and behavior.** Unit rates, tiers, discounts, currencies, demand, data growth, architecture, query efficiency, retries, and provider changes affect cost. Autoscaling can reduce idle resources or amplify unconstrained use. Use ranges and sensitivity rather than one precise forecast, and keep mandatory security and residency gates outside cost tradeoffs.

**Manage commitments and double running.** Sequence provider, network, license, support, facility, hardware, and service commitments with migration waves and rollback windows. Premature source closure increases risk; indefinite coexistence destroys economics. Assign each duplicate burden an owner, cost, expiry, successor, and removal test.

**Design portability as tested scenarios.** Identify data and metadata formats, table protocols, schema representations, API and event contracts, SQL and procedures, orchestration, identity, policy, keys, logs, semantic models, network, and operational knowledge needed to leave. Test extraction rate, completeness, egress cost, provider limits, target reconstruction, recovery, and required evidence.

**Distinguish theoretical from operational exit.** An export API can exist while rate limits, data volume, proprietary metadata, unavailable keys, egress cost, contract timing, or skill loss make exit infeasible. Exercise a bounded representative exit and record unsupported features, transformations, duration, cost, supplier action, and residual risk.

**Retire the source by evidence.** Prove consumers migrated, required history and records are preserved, target recovery succeeds without source, divergences and exceptions close, rollback expires safely, and location obligations transfer. Remove writers, readers, replicas, slots, connectors, routes, credentials, keys, schedules, monitors, backups, hardware, licenses, support, facilities, and automation as applicable.

**Test nonactivation.** Restore source configuration, credentials, schedules, routes, and recovery images in isolation. Durable authority tombstones, revoked trust, removed network paths, denied publication, and unique target identities should prevent old data or logic from becoming authoritative. Record and remove every escape path.

**Measure realized outcomes.** Compare service, recovery, incidents, security and privacy exposure, lead time, elasticity, user decisions, unit cost, operator toil, source closure, and exit readiness with the baseline. Record demand shifts and other confounders. If outcomes fail, revisit target and operating assumptions rather than calling byte transfer success.

**Preserve a migration receipt.** Bind drivers, baselines, responsibilities, provider and service versions, foundations, locations, units, contracts, transfer custody, positions, mappings, tests, reconciliations, consumer acceptance, policies, costs, incidents, authority, rollback, recovery, retirement, nonactivation, exit, outcomes, dissent, residual risk, and limitations.

## Definitions and Notation

Let a cloud data migration be:

`C = (O, B, W, P, X, D, G, Q, T, E, K, R, L)`.

`O` contains users, affected parties, decisions, drivers, present burdens, intended outcomes, mandatory constraints, countermetrics, and observation horizons. A migration is justified by a versioned outcome claim, not by destination alone.

`B = (b_s, b_t)` contains observed-source and approved-target baselines. Each baseline records data, workloads, topology, versions, responsibilities, locations, policy, service, recovery, costs, operations, and evidence time. Target diagrams remain hypotheses until deployed and observed.

`W` contains workloads, products, consumers, dependencies, migration units, and selected strategies. A unit:

`u = (identity, population, workloads, consumers, dependencies, authority, policy, service, lifecycle)`

must be coherent enough to reconcile and small enough to bound transfer, exposure, rollback, and closure.

`P` contains provider, consumer, broker, carrier, auditor, service model, deployment model, account hierarchy, regions, zones, services, control planes, contracts, versions, limits, and responsibility allocations.

A responsibility assignment is:

`responsible(component, action, state) -> (actor, verifier, evidence, failure_response)`.

Labeling a responsibility “shared” without these fields leaves it unresolved.

`X` contains online and offline transfer paths, source read, network or device capacity, encryption, custody, protocol, retries, checksums, target ingest, positions, schedules, and evidence. An optimistic lower bound is:

`transfer_time >= bytes / sustained_useful_rate`.

Real duration adds preparation, queuing, export, verification, retry, import, transformation, target apply, change catch-up, and outage. Headline link or device capacity is not sustained useful rate.

Let source change rate be `change_rate` and target net apply above new change be `catchup_rate`. Online convergence requires `catchup_rate > 0` for the affected population. If target apply merely equals incoming change, existing lag cannot close.

`D` contains data, metadata, semantics, schemas, state, history, snapshots, changes, transformations, replay, lineage, reconciliation, and consumer equivalence. An intended target state at position `p` is:

`target(p) = transform(snapshot_at_p0, changes_(p0,p], schemas, references, policy)`.

The expression requires a durable boundary and versioned inputs; it does not claim every source provides a total order or exact replay.

`G` contains governance, owners, decision rights, identity, access, encryption, keys, purpose, classification, residency, sovereignty, minimization, retention, deletion, legal hold, audit, incident response, suppliers, and exceptions.

A location record:

`loc(copy, state, region, jurisdiction, access_origin, key, purpose, retention, supplier, time)`

covers primary, replica, staging, logs, caches, backups, archives, support, telemetry, and recovery. Region labels alone do not prove these properties.

`Q` contains correctness, quality, freshness, latency, delivery, availability, capacity, quotas, isolation, scaling, failure domains, resilience, support, recovery time, data-loss bounds, and business invariants.

`T` contains migration waves, authority states, shadowing, canaries, coexistence, cutover, rollback, source retirement, and nonactivation. Define:

`authority(fact, population, consumer, time) -> (writer, reader, semantics, policy, clock, correction, recovery)`.

`E` contains inventories, experiments, checksums, reconciliations, policy tests, telemetry, lineage, consumer acceptance, exercises, incidents, costs, outcome observations, and limitations.

`K` contains source, foundation, transfer, transition, target, recovery, retirement, and exit economics; supplier commitments; skills; support; and organizational capacity. Lifecycle cost is:

`cost_lifecycle = cost_source + cost_foundation + cost_transfer + cost_overlap + cost_target + cost_risk + cost_exit - avoided_cost`.

Terms require time horizons and uncertainty ranges. Adding them does not make unlike outcomes commensurable.

`R` contains assumptions, dependencies, threats, uncertainty, countermetrics, thresholds, pause and stop conditions, rollback limits, points of no return, dissent, and replanning triggers.

`L` contains transition debt, retention, archive, deletion, source closure, provider commitments, portability, exit, tombstones, nonactivation, evidence custody, and supersession.

A migration wave `w` is admissible only if:

`Admit(w) = outcome and foundation and geography and continuity and recovery and exit`.

`outcome` binds the driver and affected users; `foundation` proves the receiving control environment is ready; `geography` proves authorized location and access; `continuity` covers transfer capacity, consistent state, semantics, and consumers; `recovery` proves service and restoration; and `exit` provides funded closure and portability. These are necessary gates in this model, not universal proof that a cloud migration will succeed.

## Mechanisms, Invariants, or Proof Structure

The assurance argument moves from driver and responsibility to tested target authority, source closure, and bounded exit.

**Driver gate.** Bind sponsor, users, decisions, baseline burden, desired outcome, deadline, mandatory constraints, countermetrics, evidence horizon, authority, and reconsideration triggers.

**Baseline gate.** Observe source data, metadata, workloads, consumers, dependencies, topology, identity, policy, service, recovery, network, suppliers, people, costs, and incident history.

**Strategy gate.** Assign retain, retire, archive, rehost, replatform, repurchase, refactor, relocate, or another explicit strategy to each bounded unit with alternatives and evidence.

**Unit gate.** Define population, products, workloads, consumers, dependencies, semantics, policy, authority, service, risk, rollback, and closure for every migration unit.

**Responsibility gate.** Allocate consumer, provider, broker, carrier, auditor, platform, domain, security, privacy, finance, supplier, verifier, evidence, and failure-response duties for each component and transition state.

**Provider gate.** Evaluate service and deployment models, legal entities, sub-processors, locations, control planes, support, service objectives, maintenance, quotas, changes, incidents, deletion, audit, contracts, and exit.

**Foundation gate.** Verify hierarchy, accounts, ownership, identity, network, DNS, time, secrets, keys, policy, classification, logging, telemetry, configuration, deployment, quotas, billing, budgets, support, incidents, backup, recovery, and evidence retention.

**Location gate.** Record primary, replica, stage, quarantine, transform, cache, log, snapshot, backup, archive, support, telemetry, provider-recovery, and disaster locations with purpose and controls.

**Residency gate.** Translate authorized residency, sovereignty, access, operator, key, supplier, cross-border, retention, and deletion conclusions into testable controls and evidence.

**Identity gate.** Govern human, workload, partner, automation, provider-support, recovery, and break-glass identity lifecycle, authentication, authorization, approval, separation, revocation, and logging.

**Network gate.** Measure source read, sustained throughput, latency, loss, protocol, concurrency, encryption, compression, proxies, firewalls, egress, target ingest, quotas, competing traffic, and failure.

**Transfer gate.** Select online, offline, hybrid, export/import, replication, change capture, event replay, backup restore, managed service, federation, or appliance mechanisms by properties preserved and risks introduced.

**Custody gate.** Control endpoints, device identity, keys, encryption, sealing, handling, shipping, staging, failed payloads, operators, receipt, wipe, return, destruction, logs, and evidence as applicable.

**Boundary gate.** Bind snapshot or export to log, sequence, watermark, or replay position with transactions, ordering, duplicates, deletes, changes, late data, retry, gaps, overlaps, failover, outage, retention, and resnapshot.

**Semantic gate.** Version grain, keys, types, precision, collation, units, codes, nulls, time, history, corrections, constraints, reference data, aggregation, interfaces, behavior, and consumer interpretation.

**Metadata gate.** Transfer schemas, catalogs, contracts, lineage, quality, policy, tags, classifications, owners, schedules, checkpoints, offsets, secrets, semantic models, alerts, budgets, and recovery procedures.

**Reconciliation gate.** Define population, positions, time, keys, exactness, tolerances, invariants, aggregates, distributions, order, deletes, policy decisions, lineage, consumer outputs, divergence classes, correction, and recheck.

**Consumer gate.** Verify applications, queries, reports, models, APIs, events, files, partners, drivers, DNS, credentials, caches, schedules, errors, procedures, support, and actual decisions.

**Exposure gate.** Bound shadow or canary populations, workloads, data classes, jurisdictions, side effects, control, duration, countermetrics, expansion, pause, stop, and rollback.

**Capacity gate.** Exercise volume, growth, change, objects, skew, concurrency, ingest, query, maintenance, backup, metadata, cold starts, cache, autoscaling, quota, and interference.

**Failure gate.** Test process, node, zone, region, account, identity, key, network, DNS, control-plane, provider, supplier, operator, corruption, and deletion failures with explicit containment.

**Recovery gate.** Restore data, metadata, identity, keys, networks, DNS, policy, lineage, orchestration, consumers, and evidence; replay and validate business invariants within accepted loss and time.

**Service gate.** Verify correctness, freshness, latency, delivery, availability, capacity, isolation, dependencies, degraded behavior, support, incidents, recovery objectives, and user outcomes.

**Economics gate.** Count foundation, connectivity, transfer, egress, requests, tooling, overlap, replication, logs, keys, support, commitments, labor, risk, recovery, retirement, and exit against the observed baseline.

**Readiness gate.** Prepare domain, data, database, platform, network, security, privacy, legal, finance, procurement, support, incident, supplier, partner, and consumer roles, access, skills, runbooks, exercises, and decisions.

**Wave gate.** Bind units, dependencies, resources, source and target versions, transfer, authority, positions, consumers, evidence, change window, stop conditions, cutover, rollback, recovery, retirement, and exit.

**Authority gate.** Move writes, reads, transformations, semantics, policy, correction, evidence, and recovery at recorded positions and intervals after all mandatory gates pass.

**Rollback gate.** Preserve a bounded safe source, target-only-state treatment, mappings, missed changes, contracts, policy, identity, routes, capacity, compensation, correction, and point of no return.

**Source-closure gate.** Prove consumer migration, preserved history, target recovery without source, closed divergence and exceptions, expired rollback, removed resources, commitments, trust, and restored-path nonactivation.

**Exit gate.** Extract representative data, metadata, contracts, policies, keys where applicable, logs, positions, and operational procedures; measure rate, completeness, fidelity, cost, reconstruction, and residual dependency.

**Outcome gate.** Compare service, recovery, incidents, exposure, lead time, elasticity, decisions, cost, toil, source closure, and exit readiness with baseline while recording confounders and countermetrics.

**Receipt gate.** Bind drivers, baselines, strategies, responsibilities, provider versions, foundations, locations, units, transfers, custody, positions, semantics, tests, policies, costs, incidents, authority, rollback, recovery, closure, exit, outcomes, risk, dissent, and limitations.

### Executable evidence: cloud-migration wave admission

The following program classifies ten invented migration waves against six mandatory gates.

<!-- bijux-verify: {"id":"cloud-migration-wave-admission","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"waves=10\nadmissible=4\nmissing_outcome=1\nunready_foundation=1\ninvalid_geography=1\nunproven_continuity=1\nunready_recovery=1\nmissing_exit=1\nmigration_patterns=8\ndata_classes=7\nlocation_states=5\nmigration_receipts=10\ndecision_events=10\n","stderr":""}} -->
```python
waves = [
    {"pattern": "online-replication", "classes": {"orders", "customer"}, "location": "region-a", "outcome": True, "foundation": True, "geography": True, "continuity": True, "recovery": True, "exit": True},
    {"pattern": "offline-appliance", "classes": {"finance"}, "location": "transfer", "outcome": True, "foundation": True, "geography": True, "continuity": True, "recovery": True, "exit": True},
    {"pattern": "export-import", "classes": {"catalog"}, "location": "region-b", "outcome": True, "foundation": True, "geography": True, "continuity": True, "recovery": True, "exit": True},
    {"pattern": "retain-federate", "classes": {"risk"}, "location": "on-prem", "outcome": True, "foundation": True, "geography": True, "continuity": True, "recovery": True, "exit": True},
    {"pattern": "archive", "classes": {"telemetry"}, "location": "archive", "outcome": False, "foundation": True, "geography": True, "continuity": True, "recovery": True, "exit": True},
    {"pattern": "replatform", "classes": {"customer"}, "location": "region-a", "outcome": True, "foundation": False, "geography": True, "continuity": True, "recovery": True, "exit": True},
    {"pattern": "cross-region", "classes": {"finance", "risk"}, "location": "region-b", "outcome": True, "foundation": True, "geography": False, "continuity": True, "recovery": True, "exit": True},
    {"pattern": "hybrid-seed", "classes": {"orders", "catalog"}, "location": "transfer", "outcome": True, "foundation": True, "geography": True, "continuity": False, "recovery": True, "exit": True},
    {"pattern": "online-replication", "classes": {"partner"}, "location": "region-a", "outcome": True, "foundation": True, "geography": True, "continuity": True, "recovery": False, "exit": True},
    {"pattern": "replatform", "classes": {"telemetry", "partner"}, "location": "region-b", "outcome": True, "foundation": True, "geography": True, "continuity": True, "recovery": True, "exit": False},
]

def evaluate(wave):
    if not wave["outcome"]:
        return "missing_outcome"
    if not wave["foundation"]:
        return "unready_foundation"
    if not wave["geography"]:
        return "invalid_geography"
    if not wave["continuity"]:
        return "unproven_continuity"
    if not wave["recovery"]:
        return "unready_recovery"
    if not wave["exit"]:
        return "missing_exit"
    return "admissible"

results = [evaluate(wave) for wave in waves]
print(f"waves={len(waves)}")
for outcome in ["admissible", "missing_outcome", "unready_foundation", "invalid_geography", "unproven_continuity", "unready_recovery", "missing_exit"]:
    print(f"{outcome}={results.count(outcome)}")
print(f"migration_patterns={len({wave['pattern'] for wave in waves})}")
print(f"data_classes={len(set().union(*(wave['classes'] for wave in waves)))}")
print(f"location_states={len({wave['location'] for wave in waves})}")
print(f"migration_receipts={len(waves)}")
print(f"decision_events={len(results)}")
```

The output reports ten waves, four admissible and one of each declared failure, eight migration patterns, seven data classes, five location states, ten receipts, and ten decisions.

The evidence is deliberately narrow. Invented Booleans, labels, and sets establish deterministic gate order and counts only. They do not establish outcome value, foundation readiness, lawful geography, state or semantic continuity, service or recovery fitness, feasible exit, provider suitability, security, privacy, cost advantage, or safe source closure. Production assurance requires authorized requirements, observed baselines, exact provider contracts and versions, measured networks and transfers, location inventories, production-shaped data, contracts, mappings, reconciliations, policy tests, failure injection, consumer acceptance, cutover and rollback exercises, recovery drills, invoices, retirement evidence, exit trials, and outcomes.

## Alternatives and Trade-Offs

**Retain in place.** Migration risk, transfer, and immediate change are avoided. Support end, facility cost, capacity limits, skills, resilience, or opportunity costs remain. Retention needs ownership and reconsideration triggers.

**Rehost.** Facility or support deadlines can be met with limited application change. Existing coupling, operating toil, sizing, licensing, and failure assumptions persist; elasticity and modernization outcomes are unproven.

**Replatform.** Managed services or new engines can reduce selected operational burden. Limits, behavior, extensions, identity, network, backup, observability, provider coupling, and skills change.

**Refactor.** Architecture can use cloud elasticity, eventing, managed data products, or new operating models. Scope, semantics, failure modes, transition duration, diagnosis, and rollback burden increase.

**Repurchase.** A software service can replace operated capability. Data extraction, configuration, semantics, integration, access, contractual, residency, recovery, audit, and exit constraints grow.

**Archive.** Active infrastructure closes while required history remains. Retrieval latency, format decay, key custody, interpretation, policy, and future reconstruction require durable controls.

**Online migration.** Source operation continues and downtime can be small. Sustained bandwidth, source load, change rate, lag, retention, connector behavior, and longer coexistence constrain convergence.

**Offline migration.** A bounded outage simplifies final state and authority. Downtime and business impact can be unacceptable, while large exports and imports still require custody and validation.

**Offline seed plus online changes.** Large baselines can bypass limited networks while change catch-up reduces downtime. Device custody, delayed import, boundary alignment, and dual mechanisms increase complexity.

**Native backup and restore.** Engine fidelity and large-copy efficiency may be strong. Version, platform, encryption, extension, topology, and provider compatibility can be narrow.

**Logical export and import.** Portability and transformation control improve. Duration, load, transaction boundaries, permissions, metadata, precision, and large-object behavior can differ.

**Replication or change capture.** Online catch-up and fine-grained progress become possible. Logs, retention, ordering, duplicates, schema changes, unsupported objects, conflicts, and source burden remain.

**Application dual write.** Business context may be available at the producer. Partial failure, idempotency, ordering, retries, external effects, and competing authority create high proof burden.

**Public network transfer.** Setup and elasticity may be convenient. Exposure, unpredictable paths, throughput, policy, egress, and denial risks grow.

**Private dedicated connectivity.** Predictability, isolation, and policy can improve. Lead time, fixed cost, capacity commitments, routing complexity, and common carrier failure remain.

**Single-region target.** Cost and consistency can be simpler. Regional failure, user latency, residency, and recovery objectives may not be met.

**Multi-zone target.** Node and zone resilience can improve with lower application complexity. Region, account, identity, key, policy, control-plane, and corruption failures remain.

**Multi-region target.** Geographic resilience and user proximity can improve. Consistency, replication, cost, policy, sovereignty, failover, correction, and operation become harder.

**Hybrid authority.** Data can remain near sources or regulated locations while selected capabilities move. Network, identity, policy, consistency, observability, support, and recovery span environments.

**Multi-cloud placement.** Provider concentration and regional coverage can improve for selected workloads. Lowest-common-denominator design, duplicated platforms, skill breadth, data movement, identity, policy, cost, and recovery complexity grow.

**Provider-managed keys.** Integration and recovery can be simpler. Control, jurisdiction, supplier, separation, and exit concerns may be weaker for some risks.

**Customer-managed or externally held keys.** Control and separation can improve. Availability, rotation, recovery, replication, incident handling, and self-inflicted denial require stronger operation.

**Big cutover.** Overlap and transition debt may be shorter. Transfer peaks, consumer coordination, state ambiguity, blast radius, and rollback complexity grow.

**Incremental waves.** Learning, evidence, capacity, and rollback can be bounded. Double running, bridges, dependency management, duration, and cost can accumulate.

**Provider-native design.** Managed capability and speed may improve. APIs, formats, operations, semantics, skills, costs, and exit can couple deeply.

**Portable interfaces and formats.** Some provider and engine substitution becomes easier. Control-plane, policy, orchestration, semantics, performance, support, and true exit still need testing.

## Failure Modes and Misconceptions

1. **“Cloud is the migration strategy.”** Service, deployment, region, responsibility, workload, and transition decisions remain.
2. **“A copied dataset is a migrated capability.”** Metadata, consumers, policy, operations, recovery, and authority may remain behind.
3. **“Cloud migration automatically modernizes.”** Rehosting can preserve every legacy burden.
4. **“Everything should use one strategy.”** Workloads need retain, retire, archive, rehost, replatform, repurchase, or refactor decisions.
5. **“The target diagram is an observed baseline.”** Deployment, configuration, service, and outcomes require evidence.
6. **“Shared responsibility means the provider handles security.”** Component, action, verifier, and failure response must be allocated.
7. **“Managed service removes operations.”** Capacity, policy, identity, recovery, cost, incidents, and supplier management remain.
8. **“A region name proves residency.”** Replicas, backups, logs, support, telemetry, control planes, and provider recovery may differ.
9. **“Residency and sovereignty are synonyms.”** Legal control, operator access, keys, ownership, and independent operation can matter.
10. **“Provider certification authorizes every workload.”** Local purpose, configuration, contracts, controls, and risk acceptance remain.
11. **“The landing environment can mature after copying.”** Provisional identity, networks, keys, policy, logs, and ownership harden.
12. **“A policy declaration proves enforcement.”** Inputs, identities, defaults, coverage, exceptions, and failure behavior require tests.
13. **“Customer-managed keys eliminate provider dependency.”** Key services, recovery, software, regions, and support can remain coupled.
14. **“External keys are always safer.”** Lost availability or recovery can destroy the service.
15. **“Link speed equals transfer rate.”** Source read, latency, loss, encryption, protocol, retry, target apply, and contention reduce it.
16. **“Compression always shortens migration.”** CPU, data entropy, target decompression, and change catch-up can dominate.
17. **“An appliance avoids network concerns.”** Export, import, custody, shipping, keys, timing, and online deltas remain.
18. **“Offline transfer means no copies in transit.”** Devices, staging, manifests, logs, and provider import paths hold data.
19. **“Online replication guarantees convergence.”** Change rate can equal or exceed net catch-up capacity.
20. **“A snapshot followed by CDC cannot lose data.”** Gaps, overlaps, offsets, retention, failover, and schema change remain.
21. **“Change capture preserves business meaning.”** Storage mutations may omit intent, transaction context, and semantic identity.
22. **“Dual write is the simplest migration.”** Partial failure, ordering, retries, and competing authority create divergence.
23. **“Checksums prove semantic parity.”** Representations may differ legitimately or match while meanings are wrong.
24. **“Row counts prove completeness.”** Keys, deletes, duplicates, values, intervals, and relationships can differ.
25. **“Conversion tools preserve behavior.”** Types, precision, collation, functions, errors, transactions, and time can change.
26. **“Metadata can be recreated later.”** Contracts, lineage, policies, offsets, schedules, and ownership determine usability.
27. **“A running query proves consumer migration.”** Authentication, semantics, latency, errors, schedules, and decisions may differ.
28. **“Shadow copies are exempt from policy.”** They retain purpose, residency, access, retention, and deletion obligations.
29. **“A synthetic benchmark proves capacity.”** Skew, concurrency, ingest, maintenance, control planes, quotas, and failure remain.
30. **“Autoscaling removes capacity planning.”** Ramp time, quotas, budgets, dependencies, and regional supply constrain it.
31. **“Multi-zone means disaster recovery.”** Region, account, identity, key, corruption, policy, and provider failures remain.
32. **“Replication is backup.”** Corruption and deletion can propagate immediately.
33. **“Backups prove recoverability.”** Keys, catalogs, schemas, policy, order, consumers, and procedures must restore.
34. **“Provider recovery objectives are ours.”** Application dependencies, validation, replay, and decisions add time and loss.
35. **“Cloud control planes do not affect data availability.”** Identity, keys, DNS, policy, catalog, and configuration can block operation.
36. **“Quota exhaustion is only performance degradation.”** It can block writes, recovery, telemetry, keys, or failover.
37. **“Cutover is a connection-string change.”** State, consumers, authority, policy, recovery, and clocks must move.
38. **“Writes and reads should switch together.”** Versioned consumers, caches, and derived state may require separate boundaries.
39. **“Rollback is always safer.”** Cloud-only state and external effects can make source return harmful.
40. **“Rollback is route reversal.”** State convergence, contracts, policies, credentials, capacity, and correction must return.
41. **“Operators can learn after cutover.”** Access, decisions, incidents, degraded modes, and recovery must be exercised.
42. **“Target monthly cost proves savings.”** Foundation, transfer, overlap, egress, logs, people, incidents, and exit count.
43. **“Ingress is free, so migration is free.”** Source, tooling, network, requests, transformation, verification, and labor remain.
44. **“Commitment discounts always reduce cost.”** Forecast error and migration delay can strand spend.
45. **“Data gravity means data can never move.”** It is a constraint model requiring measured alternatives, not a veto.
46. **“Open files prove exit.”** Catalogs, SQL, policies, keys, metadata, orchestration, semantics, rate limits, and skills remain.
47. **“An export API proves portability.”** Volume, limits, fidelity, cost, time, and target reconstruction require exercise.
48. **“Source shutdown proves migration completion.”** Consumer, recovery, records, obligations, and nonactivation may fail.
49. **“Keeping the source is free rollback.”** It preserves cost, attack surface, ambiguity, drift, and reactivation risk.
50. **“A successful transfer proves the outcome.”** Authority, service, recovery, cost, closure, exit, and user results remain.

## Worked Examples

### Example 1

A data-center exit deadline justifies rehosting a finance database before later refactoring. The receipt credits facility closure and support continuity, not unobserved elasticity or cost reduction. The source workload, license, network, recovery, and consumer baseline remains available for post-migration comparison.

### Example 2

A customer dataset is configured in an allowed primary region, but provider support dumps and backups may cross a prohibited boundary. The location model expands beyond primary storage, contracts and controls are reviewed by authorized policy and legal owners, and the wave pauses until support, backup, key, logging, and deletion paths satisfy the decision.

### Example 3

A one-gigabit circuit is expected to move a petabyte quickly. Sustained tests expose source read limits, protocol loss, encryption CPU, competing traffic, and slower target apply. The plan uses an encrypted offline seed with recorded custody, then change capture over the circuit from a durable source position.

### Example 4

An initial snapshot finishes at noon, while change capture begins from a position recorded at 12:04. Reconciliation detects missing order corrections. The team repeats from a transactionally meaningful position, tests overlap deduplication, deletes, schema changes, connector restart, source failover, target outage, retention, and resnapshot.

### Example 5

A conversion tool maps money to a floating type and timestamps to UTC without preserving original zone and business cutoff. Row counts match, but month-end balances change. A semantic contract restores decimal precision, currency, fiscal calendar, valid time, rounding, and consumer decision parity before authority moves.

### Example 6

A target meets query latency at normal load. During month end, ingestion, reporting, compaction, backup, and catalog operations overlap and exhaust a regional quota. A production-shaped trial adds concurrency, cold caches, control-plane calls, throttling, quota-increase lead time, degraded operation, recovery, and full cost.

### Example 7

Provider-managed cross-zone replication keeps service available after a node loss but immediately propagates an operator deletion. Independent versioned backups, isolated restore, replay, policy, keys, schemas, consumer validation, and business recovery exercises establish a distinct recovery claim.

### Example 8

After target authority begins, new customer identities and deletion decisions exist only in the cloud service. A rollback drill shows the source cannot represent them. The runbook keeps that population on the target, replays compatible state for remaining consumers, compensates external effects, and defines a point after which roll-forward is mandatory.

### Example 9

A cost forecast excludes logs, inter-zone replication, private connectivity, support, duplicate operation, and egress for partner delivery. Metered trial evidence and allocation tags reveal a higher unit cost than baseline. The design changes retention, workload placement, commitments, and query patterns before expanding the wave.

### Example 10

An exit exercise exports a representative product but loses policy tags, lineage, contract history, and one unsupported type. The team versions conversion, validates target reconstruction and recovery, measures extraction limits and egress, and records remaining provider dependencies instead of claiming portability from open files.

## Cross-Program Connections

- [Cloud and Infrastructure Engineering](../../30-cloud-and-infrastructure-engineering/ROADMAP.md) provides service and deployment models, responsibility, organizations, landing zones, regions, identity, networks, keys, quotas, billing, resilience, recovery, and provider exit.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) implements inventory, export, import, replication, change capture, transformation, metadata movement, reconciliation, lineage, quality, replay, cutover, and source retirement.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) supplies governed foundations, paved migration paths, self-service environments, deployment, policy, telemetry, support, cost controls, recovery, and lifecycle automation.
- [Network Engineering](../../24-network-engineering/ROADMAP.md) grounds throughput, latency, loss, routing, private connectivity, DNS, segmentation, encryption, carrier failure, transfer capacity, and cutover.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) governs identity, access, keys, secrets, suppliers, logs, threats, incidents, recovery, sanitization, and secure disposal across shared responsibility.
- [Database Engineering](../../18-database-engineering/ROADMAP.md) owns schema behavior, transactions, replication, backup, restore, performance, migration tooling, compatibility, cutover, and database retirement.
- [Large-Scale Data Systems Engineering](../../21-large-scale-data-systems-engineering/ROADMAP.md) explains storage, logs, ordering, consistency, replication, streaming, distributed queries, scaling, metadata, failure, and recovery.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) provides partial failure, duplication, ordering, consistency, idempotency, convergence, clocks, retries, rollback, and replay reasoning.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) governs serving contracts, clients, identity, errors, versioning, canaries, traffic shifts, resilience, deprecation, and endpoint migration.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies baselines, requirements, trade studies, integration, transition, configuration, readiness, verification, validation, risk, lifecycle, and disposal discipline.

## References

1. NIST, [SP 800-145: The NIST Definition of Cloud Computing](https://csrc.nist.gov/pubs/sp/800/145/final), essential characteristics, service models, and deployment models.
2. NIST, [Cloud Computing Reference Architecture](https://www.nist.gov/publications/nist-cloud-computing-reference-architecture), consumer, provider, broker, auditor, carrier, orchestration, management, security, and privacy roles.
3. NIST, [SP 800-210: General Access Control Guidance for Cloud Systems](https://csrc.nist.gov/pubs/sp/800/210/final), access-control characteristics and guidance across infrastructure, platform, and software service models.
4. Google Cloud, [Migrate to Google Cloud: Get Started](https://docs.cloud.google.com/architecture/migration-to-gcp-getting-started), migration assessment, foundation, transfer, deployment, validation, optimization, and cost context.
5. Google Cloud, [Migrate to Google Cloud: Transfer Large Datasets](https://docs.cloud.google.com/architecture/migration-to-google-cloud-transferring-your-large-datasets), online and offline transfer, bandwidth, duration, and transfer mechanisms.
6. Google Cloud, [Best Practices for Validating a Migration Plan](https://docs.cloud.google.com/architecture/migration-to-google-cloud-best-practices#validate_your_migration_plan), migration-plan validation and evidence.
7. AWS, [SQL Server Database Migration Strategies](https://docs.aws.amazon.com/prescriptive-guidance/latest/migration-sql-server/strategies.html), online and offline migration, copy, change synchronization, validation, and cutover.
8. PostgreSQL Global Development Group, [Logical Replication](https://www.postgresql.org/docs/current/logical-replication.html), publications, subscriptions, snapshots, changes, ordering, conflicts, monitoring, and security.
9. Debezium, [Architecture](https://debezium.io/documentation/reference/stable/architecture.html), log-based change capture, source offsets, records, schemas, and deployment forms.
10. Google, [Data Integrity](https://sre.google/sre-book/data-integrity/), backups, restores, replication, corruption, validation, and disaster planning.
11. Bitol, [Open Data Contract Standard](https://bitol-io.github.io/open-data-contract-standard/latest/), schema, quality, service, roles, support, and infrastructure obligations.
12. OpenLineage, [Object Model](https://openlineage.io/docs/spec/object-model/), dataset, job, run, event, namespace, name, and facet identities.
13. Open Policy Agent, [Policy Language](https://www.openpolicyagent.org/docs/policy-language), structured policy decisions, inputs, rules, tests, and runtime context.
14. OpenTelemetry, [Specification](https://opentelemetry.io/docs/specs/otel/), signals, resources, context, semantic conventions, sampling, compatibility, and versioning.
15. NIST, [SP 800-160 Volume 1 Revision 1](https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final), systems-security engineering and trustworthy secure systems across the lifecycle.
16. FinOps Foundation, [FinOps Framework](https://www.finops.org/framework/), cross-functional ownership, usage, cost, value, optimization, governance, and technology decisions.

## Exercises

### Exercise 1

Design a cloud data migration charter and target for a regulated customer and order estate. Include drivers, outcomes, source baseline, migration units, strategies, service and deployment models, provider roles, responsibility, foundations, locations, residency, sovereignty, suppliers, constraints, and exit.

### Exercise 2

Create an online and offline transfer comparison for a one-petabyte baseline with ongoing change. Cover source read, sustained network rate, target ingest, change catch-up, duration, encryption, custody, appliances, checksums, retries, positions, gaps, overlaps, failure, cost, and selection criteria.

### Exercise 3

Specify semantic, metadata, state, and consumer continuity for a database and warehouse move. Include schemas, types, precision, time, keys, history, correction, contracts, catalogs, policy, lineage, snapshots, changes, reconciliation, applications, reports, models, and partners.

### Exercise 4

Design service, cutover, rollback, and recovery validation for a cloud migration. Address production load, quotas, zones, regions, accounts, identity, keys, network, DNS, control plane, provider, corruption, cloud-only state, external effects, operators, and business invariants.

### Exercise 5

Build the economic, source-retirement, nonactivation, and provider-exit portions of a migration receipt. Include metered costs, commitments, double running, egress, records, credentials, routes, replicas, backups, licenses, restored automation, export rate, metadata fidelity, reconstruction, outcomes, and limitations.

## Answers to the Exercises

### Answer 1

State the sponsor, customer and operator outcomes, baseline burdens, facility or capability driver, deadline, countermetrics, mandatory security, privacy, residency, sovereignty, service, recovery, and cost constraints, evidence horizon, and decision authority. Observe source data, workloads, consumers, dependencies, semantics, locations, identities, policies, networks, recovery, suppliers, incidents, costs, and procedures. Partition coherent products, populations, consumers, or workloads and assign retain, retire, archive, rehost, replatform, repurchase, refactor, or relocate strategies. Select service and deployment models by workload evidence. Allocate consumer, provider, broker, carrier, auditor, platform, domain, security, privacy, finance, and supplier duties with verifiers and failure responses. Require the account hierarchy, identity, network, keys, policy, telemetry, quotas, billing, support, and recovery foundation before arrival. Record every primary, replica, log, backup, support, and recovery location under authorized conclusions. Define a tested exit for data, metadata, contracts, policy, evidence, and operation.

### Answer 2

Measure source read, sustained useful network throughput, latency, loss, encryption and compression overhead, competing traffic, target import and apply, provider quotas, failure, and the source change rate. Compute only a lower bound from bytes divided by sustained rate, then add export, verification, retries, scheduling, import, transformation, change catch-up, and outage. For online transfer, define identities, routes, encryption, positions, retries, source load, retention, and convergence; require net catch-up above new change. For offline transfer, define device identity, export environment, capacity, encryption, key custody, sealing, handling, shipment, locations, receipt, import, wipe, return or destruction, and evidence. A hybrid may seed offline and catch up online, but must bind both at one consistent position. Select using downtime, duration, custody, policy, recoverability, source impact, target capacity, repeatability, and full cost.

### Answer 3

Version grain, keys, types, precision, collation, units, currencies, code sets, nulls, event and business time, valid and transaction history, deletes, corrections, constraints, reference data, aggregation, error behavior, and consumer interpretation. Move schemas, contracts, catalog identities, classifications, quality rules, lineage, policies, schedules, checkpoints, offsets, semantic models, alerts, and recovery procedures with data. Capture a consistent snapshot and durable change position; handle transactions, ordering, duplicates, key and schema changes, late data, gaps, overlaps, restart, failover, target outage, and resnapshot. Reconcile named populations and positions by exact values, justified tolerances, relationships, sequences, aggregates, policy, lineage, and consumer outputs. Test applications, reports, models, APIs, events, files, partners, credentials, caches, schedules, errors, and actual decisions through representative cycles before authority changes.

### Answer 4

Exercise normal and peak volume, growth, change, skew, concurrency, ingest, queries, maintenance, backup, metadata, cold starts, caches, autoscaling, throttling, quota exhaustion, and shared workload interference. Inject process, node, zone, region, account, identity, key, network, DNS, control-plane, provider, supplier, operator, corruption, and deletion faults according to risk. Measure correctness, freshness, latency, delivery, availability, degraded service, support, accepted data loss, and complete recovery time. Record the cutover position, authority, consumers, policies, capacity, communication, freeze or buffer, stop conditions, approval, and rollback limit. Test rollback with cloud-only identities, state, corrections, deletions, messages, and external effects; define compensation and a point of no return. Recover data, metadata, identity, keys, network, policy, lineage, orchestration, consumers, and evidence without source dependence and validate business invariants.

### Answer 5

Measure foundation, private connectivity, transfer, appliances, egress, requests, storage, compute, replication, logs, keys, support, discounts, commitments, engineering, security, privacy, legal, incidents, recovery, retirement, and exit against the observed source baseline using ranges and unit drivers. Align overlap with rollback and commitment windows. After consumer acceptance and successor recovery, remove source writers, readers, replicas, slots, connectors, routes, credentials, keys, schedules, monitors, backups, hardware, licenses, support, facilities, and automation while preserving required records. Restore source artifacts in isolation and verify tombstones, revoked trust, removed network paths, and denied publication prevent authority. Exercise representative export of data, metadata, contracts, policy, logs, positions, and procedures; measure rate, completeness, fidelity, egress, target reconstruction, recovery, and remaining dependencies. Compare service, incidents, exposure, lead time, elasticity, decisions, toil, unit cost, source closure, and exit readiness with baseline, recording confounders and limitations.
