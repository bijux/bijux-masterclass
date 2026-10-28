---
module_id: DARCH-095
program: Data Architecture Engineering
level: 2
module_number: 95
title: Legacy Integration Retirement
status: complete
last_verified: 2026-09-03
---

# Legacy Integration Retirement

## One-Page Review

### Governing question

How can an organization prove that a legacy integration may be retired without losing required business behavior, data, consumers, policy, evidence, service, recovery, or control—and without leaving a path through which obsolete authority can return?

### Essential definitions

- A **legacy integration** is any existing point-to-point connection, shared database, file exchange, batch job, message route, broker topic, API, replication link, virtual query, adapter, hub flow, managed transfer, or human bridge whose continued operation is being reconsidered.
- **Retirement** is the governed end of an integration's authority and service after its purpose terminates or an accepted successor assumes every required obligation.
- A **retirement candidate** is a versioned integration identity with owner, purpose, producers, consumers, contracts, dependencies, state, policy, service, recovery role, costs, evidence, proposed disposition, and closure criteria.
- An **integration edge** is a directional producer-to-consumer relationship carrying named data, commands, events, queries, decisions, policy, or evidence under a contract.
- A **successor obligation map** allocates every required legacy behavior, semantic, state, service, policy, support, recovery, and evidence obligation to a successor or to an authorized termination.
- **Authority transfer** is the recorded change in which path may publish, transform, read, decide, enforce, correct, replay, recover, or serve a named population during a bounded interval.
- **Consumer closure** is evidence that a consumer has migrated, been deliberately terminated, or been accepted as an explicitly retained dependency by an authorized owner.
- **Residual traffic** is any observed request, query, file, message, replication change, scheduled execution, retry, recovery access, or human use of a retirement candidate after an expected quiet boundary.
- A **retirement quarantine** is a reversible state in which production authority is removed while invocation, access, restoration, and unmet dependencies remain observable before destructive closure.
- A **tombstone** is a durable declaration that an integration identity, route, contract, topic, credential, schedule, or authority is retired and must not be recreated or reused without a new governed decision.
- **Sanitization** is the risk-based removal of data from media or services so the required assurance against recovery is achieved; deletion of a logical object is not automatically sanitization.
- **Nonactivation** is tested evidence that restored configurations, backups, credentials, routes, schedules, queues, consumers, or automation cannot make the retired integration authoritative again.
- A **retirement receipt** binds the candidate, obligations, evidence, consumer decisions, state boundary, authority transfer, removals, preserved records, sanitization, costs, risks, exceptions, and approval.

### Central model, mechanism, or theorem

Represent retirement as:

`R = (U, B, N, A, C, D, G, Q, T, E, K, L)`

where `U` is users, purposes, outcomes, and affected decisions; `B` is the observed legacy and accepted successor baselines; `N` is integration nodes, edges, consumers, dependencies, and cycles; `A` is ownership and time-indexed authority; `C` is interface, behavioral, and semantic contracts; `D` is state, history, ordering, replay, correction, archive, and reconciliation; `G` is governance, security, privacy, retention, deletion, and evidence custody; `Q` is quality, service, failure, recovery, and support; `T` is replacement, coexistence, cutover, rollback, quarantine, and removal; `E` is discovery, telemetry, lineage, consumer confirmation, exercises, and limitations; `K` is cost, commitments, skills, suppliers, and organizational capacity; and `L` is lifecycle, tombstones, sanitization, nonactivation, and closure. A shutdown is safe retirement only when required obligations terminate or transfer, no unresolved dependency retains authority, recovery is coherent, and obsolete authority cannot return.

### Critical invariants

- Candidate, producer, consumer, edge, contract, dataset, message, file, route, schedule, credential, authority, successor, evidence, exception, tombstone, and receipt have stable identities.
- Active, shadowed, dual-run, target-authoritative, quarantined, disabled, archived, sanitized, retired, restored, and reactivated states remain distinguishable.
- Every required legacy obligation maps to an accepted successor or an authorized termination; silence and assumption are not mappings.
- At each instant, the authoritative writer, publisher, transformer, reader, semantic definition, policy, clock, correction owner, and recovery path are explicit.
- State transfer preserves or deliberately changes population, keys, semantics, transactions, ordering, duplicates, deletes, time, history, correction, lineage, and consumer decisions.
- Deprecation communicates lifecycle intent but does not prove discovery, consumer migration, safe sunset, or closure.
- Security, privacy, purpose, classification, access, encryption, retention, deletion, legal hold, audit, and evidence custody survive coexistence, quarantine, rollback, archive, and disposal.
- Residual-use evidence covers interactive, batch, event, replication, partner, manual, rare, and recovery paths across a justified observation horizon.
- Cutover and quarantine preserve a bounded rollback or correction strategy until target authority and recovery are proven.
- Removal includes routes, schedules, subscriptions, slots, topics, schemas, files, adapters, credentials, policies, catalogs, monitors, backups, licenses, suppliers, support, and recovery automation as applicable.
- Required records remain discoverable, interpretable, access-controlled, restorable, and disposable after operational integration disappears.
- Nonactivation tests prove restored artifacts cannot publish, consume, enforce, charge, or regain authority under the retired identity.

### Common failures

- Declaring an integration unused because no owner answers or no interactive traffic appears.
- Treating a deprecation notice as consumer migration evidence.
- Replacing transport while silently losing business semantics, ordering, corrections, or error behavior.
- Disabling a scheduler while retries, queues, database links, manual runs, or recovery automation remain.
- Deleting a topic or table before lagging consumers, replay, audit, and retention obligations close.
- Removing credentials without testing break-glass, cached, service, partner, and restored identities.
- Preserving the old path indefinitely “for rollback” without expiry, cost, authority, or nonactivation rules.
- Calling backups archival without testing discovery, interpretation, access, restore, legal hold, and deletion.
- Counting shut-down servers while licenses, commitments, support, monitoring, and supplier access persist.
- Reusing a retired endpoint, topic, schema, or identifier and allowing old consumers to affect new authority.

### Compact example

A nightly customer file appears unused after its reports move to an API. Discovery finds a partner import, a quarterly consent audit, a manual correction procedure, and a disaster-recovery script that still reads it. Each obligation is mapped: the API gains a bulk snapshot and correction contract, the audit receives preserved lineage and reproducible history, the partner migrates under observed confirmation, and recovery is rebuilt and exercised. Source and successor outputs reconcile by identity, consent interval, deletion, and consumer decision. The file exchange enters quarantine for a full quarterly cycle; residual invocations page an owner rather than run. Schedules, service accounts, keys, transfer routes, landing directories, schemas, catalog entries, monitors, backups, vendor charges, and support close. Restoring the old configuration in isolation cannot publish because its credentials and route are revoked and its identity is tombstoned.

### Connections

[DARCH-003](003-current-state-data-landscape.md), [DARCH-027](027-producer-and-consumer-contracts.md), [DARCH-031](031-point-to-point-integration-and-its-costs.md), [DARCH-032](032-hub-and-spoke-integration.md), [DARCH-034](034-api-led-data-access.md), [DARCH-035](035-event-driven-data-integration.md), [DARCH-037](037-batch-and-file-exchange.md), [DARCH-038](038-federation-and-virtualization.md), [DARCH-040](040-choosing-an-integration-style-from-semantics-and-latency.md), [DARCH-064](064-lineage-architecture.md), [DARCH-079](079-audit-and-provenance-architecture.md), [DARCH-093](093-transition-architectures.md), and [DARCH-094](094-warehouse-and-lake-modernization.md) establish discovery, contracts, integration styles, evidence, transition, and modernization. [DARCH-096](../ROADMAP.md) next applies migration discipline to cloud data.

## Governing Question

Turning off a legacy interface is easy. Proving that it no longer carries required authority is difficult. An old nightly file may feed an invisible partner process. A database view may be restored during disaster recovery. A topic with no recent traffic may be a quarterly audit source. A replication slot may retain logs even after its subscriber is gone. A deprecated endpoint may serve a hard-coded client. A shared table may embed correction procedures that no successor contract expresses.

The governing question is not whether a replacement was deployed or whether traffic looks low. It is whether every required purpose and obligation has ended or moved, every consumer and recovery dependency is resolved, state and semantics reconcile, controls and records remain valid, financial and operational burdens close, and restored artifacts cannot reactivate obsolete authority. Retirement is an evidence-backed lifecycle transition, not a power operation.

## Why This Matters

NASA's [Product Integration](https://www.nasa.gov/reference/5-2-product-integration/) treats integration as management of subsystem, environmental, software, hardware, and human interactions through the lifecycle, and explicitly connects closeout with de-integration, disposal, and archiving. This systems view exposes why retirement must be engineered: connections include enabling products, procedures, people, records, and recovery assets, not only runtime code.

NASA [Product Transition](https://www.nasa.gov/reference/5-5-product-transition/) emphasizes readiness of products, sites, operators, users, documentation, support, recovery, disposal environments, acceptance, and captured work products. A successor integration is not accepted merely because it runs; receiving consumers and operators must be ready, and retirement evidence must survive handoff.

Martin Fowler's [Strangler Fig](https://martinfowler.com/bliki/StranglerFigApplication.html) describes gradual displacement through seams and explicitly frames the intermediate design as transitional architecture. Danilo Sato's [Parallel Change](https://martinfowler.com/bliki/ParallelChange.html) separates expand, migrate, and contract, warning through the mechanism itself that compatibility work is incomplete until contraction removes the old interface. These patterns support bounded retirement but do not discover hidden consumers or prove closure.

IETF [RFC 9745](https://www.rfc-editor.org/rfc/rfc9745.html) standardizes an HTTP `Deprecation` response header and a link relation for lifecycle information while noting that deprecation does not itself change resource behavior. IETF [RFC 8594](https://www.rfc-editor.org/rfc/rfc8594.html) defines the `Sunset` response header to communicate that a resource is expected to become unresponsive at a future time. Signaling is valuable, but retirement still requires client discovery, migration evidence, compatibility, support, cutover, and removal.

The OpenAPI Initiative's [OpenAPI Specification](https://spec.openapis.org/oas/latest.html) describes HTTP interfaces including operations, schemas, parameters, responses, security, extensions, and deprecation markers. The AsyncAPI Initiative's [current specification](https://www.asyncapi.com/docs/reference/specification/latest) describes asynchronous interfaces including channels, operations, messages, servers, security, and bindings. Machine-readable contracts can locate obligations and successors, yet declarations do not prove runtime coverage, consumer behavior, or absence.

The Bitol [Open Data Contract Standard](https://bitol-io.github.io/open-data-contract-standard/latest/) expresses schema, quality, service, roles, support, and infrastructure obligations. Retiring an integration requires deciding whether each obligation transfers, changes, or terminates; publishing a successor contract is only the beginning of that evidence.

PostgreSQL [logical replication](https://www.postgresql.org/docs/current/logical-replication.html) documents publications, subscriptions, initial snapshots, ongoing changes, conflicts, monitoring, restrictions, and security. Debezium's [architecture documentation](https://debezium.io/documentation/reference/stable/architecture.html) describes log-based connectors, source offsets, schemas, records, and deployment forms. Retiring these paths includes source-side state such as publications, slots, offsets, credentials, and log-retention consequences—not only stopping a target process.

OpenLineage's [object model](https://openlineage.io/docs/spec/object-model/) identifies datasets, jobs, runs, events, namespaces, names, and facets. Stable lineage identities support impact analysis and residual-use discovery, but incomplete instrumentation can make an attractive graph false evidence of absence.

The Open Policy Agent [policy-language documentation](https://www.openpolicyagent.org/docs/policy-language) describes structured decisions over runtime input. The OpenTelemetry [specification](https://opentelemetry.io/docs/specs/otel/) standardizes signals, resources, context, and semantic conventions. Policy decisions and telemetry can span old and new paths, provided identities, enforcement points, sampling, batch correlation, and retention are designed for retirement evidence.

NIST [SP 800-88 Revision 1](https://csrc.nist.gov/pubs/sp/800/88/r1/final) provides guidance for media sanitization through risk-based methods and verification. Logical object deletion, encryption-key destruction, provider deletion, media reuse, and physical disposition have different assurances; the applicable method depends on confidentiality, media, custody, and risk.

The FinOps Foundation's [FinOps Framework](https://www.finops.org/framework/) joins engineering, finance, business, procurement, leadership, and other roles around usage, cost, value, optimization, governance, and technology decisions. Integration retirement closes value only when duplicate compute, storage, network, monitoring, licenses, minimum commitments, vendor access, support, and organizational toil actually end.

Together these sources support planned de-integration and transition, gradual contraction, lifecycle signaling, explicit interface and data contracts, replication cleanup, lineage, policy, telemetry, sanitization, and economic closure. They do not identify every consumer, prove semantic replacement, authorize termination, establish an observation horizon, validate recovery, demonstrate secure erasure, or prove savings. Those conclusions require local ownership, production evidence, consumer acceptance, state reconciliation, drills, disposal records, billing, and nonactivation tests.

## Prerequisites and Retrieval

You should understand current-state discovery, point-to-point and hub integration, shared databases, batch and file exchange, APIs, events, brokers, replication, change capture, federation, contracts, schemas, semantics, lineage, telemetry, identity, policy, privacy, security, quality, service objectives, distributed systems, transition architecture, recovery, archives, cost allocation, and disposal.

Retrieve legacy integration, retirement candidate, node, edge, producer, consumer, dependency, contract, successor, obligation map, authority transfer, deprecation, sunset, expand-migrate-contract, residual traffic, quiet period, consumer closure, state boundary, reconciliation, replay, cutover, rollback, quarantine, tombstone, archive, retention, deletion, sanitization, nonactivation, retirement debt, and receipt.

As a retrieval test, inspect a shared customer database feeding batch extracts, an API, change capture, a broker topic, virtual queries, reports, partner files, and disaster-recovery jobs. Ask who owns each fact and correction; which consumers are observed and which are merely registered; which contracts cover identity, consent, time, deletion, ordering, and errors; which source positions and replays exist; which policies apply to old copies; which rare and manual paths remain; how target recovery works without the source; which credentials, slots, subscriptions, schedules, routes, backups, licenses, and suppliers persist; and which isolated restore proves the retired path cannot publish again.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish shutdown, deprecation, sunset, quarantine, archive, sanitization, retirement, and closure;
2. inventory point-to-point, hub, shared-database, file, API, event, replication, federation, and human integration edges;
3. discover consumers and dependencies using configuration, traffic, lineage, schedules, billing, access, recovery, interviews, and active probes;
4. map every required semantic, state, policy, service, support, evidence, and recovery obligation to a successor or authorized termination;
5. define time-indexed authority and reconcile state, ordering, history, correction, and consumer decisions before cutover;
6. design deprecation, migration support, residual-use observation, quarantine, rollback, and removal mechanisms;
7. preserve records while enforcing retention, deletion, legal hold, access, sanitization, and disposal assurance;
8. remove source and target artifacts, credentials, routes, subscriptions, costs, suppliers, and recovery paths safely;
9. test nonactivation and prevent retired identifiers or restored automation from regaining authority; and
10. write retirement receipts with evidence, decisions, residual risk, exceptions, preserved records, costs, and closure.

## Core Exposition

**Define the retirement decision.** Name the candidate, sponsor, technical and business owners, current purpose, affected users and decisions, retirement driver, intended successor or termination, scope, deadline, risk tolerance, evidence horizon, rollback limit, and approval authority. “Old middleware” is not a candidate identity; use exact environments, routes, endpoints, topics, jobs, files, tables, credentials, and versions.

**Separate lifecycle states.** Active paths carry authority. Deprecated paths remain available while warning consumers. Sunset announces expected unavailability. Shadowed paths observe without governing results. Quarantined paths have production authority removed but remain recoverable and observable. Disabled paths may still be restorable. Archived records remain governed. Sanitized media or services meet a selected assurance. Retired paths have no required operation or authority. Closed paths also pass nonactivation and evidence-preservation checks.

**Build an integration graph.** Represent applications, databases, warehouses, lakes, brokers, APIs, schedulers, transfer services, identity systems, policy engines, catalogs, humans, and suppliers as nodes. Represent queries, writes, events, commands, files, replication changes, credentials, policy decisions, manual procedures, and recovery actions as typed directed edges. Record contract, owner, frequency, population, authority, criticality, service, policy, evidence, and confidence for every edge.

**Use multiple discovery channels.** Combine code and configuration scans, database dependency metadata, network flows, proxy and gateway logs, broker metrics, topic and subscription inventories, scheduler history, file-transfer logs, object access, lineage, catalog entries, identity decisions, secrets, billing, support tickets, incident records, recovery procedures, owner interviews, consumer surveys, and contract registries. Each channel has blind spots; agreement improves confidence but never proves universal absence.

**Distinguish declared from observed dependency.** A catalog entry may be stale; traffic may be sampled; an owner may not know restored or downstream use. Label each dependency as declared, configured, observed, inferred, confirmed, rejected, or unknown with time and evidence. A retirement decision should expose uncertainty rather than converting missing evidence into “unused.”

**Find rare and dormant consumers.** Observe complete business and operational cycles: day-end, month-end, quarter-end, year-end, regulatory filings, model retraining, partner settlement, incident investigation, disaster recovery, legal discovery, and reconciliation. A quiet period is justified by workload periodicity and risk, not a universal number of days.

**Trace transitive consumers.** A file may feed a staging table that feeds a semantic model that exports spreadsheets. A topic may populate a cache whose users never contact the broker. Discover downstream decisions, not only direct technical subscribers. Stable lineage and consumer identities make transitive closure more defensible.

**Treat humans as integration nodes.** Operators may run manual exports, edit mapping tables, resend files, correct records, approve exceptions, or bridge failures by email. Retirement must replace or terminate these procedures and preserve segregation of duties, evidence, support, and escalation.

**Recover the actual contract.** Inventory structure, semantics, behavior, ordering, delivery, idempotency, timing, errors, retries, authentication, authorization, service, support, change, recovery, retention, and termination. Compare written declarations with observed behavior and consumer assumptions. Legacy quirks may be required behavior, tolerated defects, or obsolete behavior; assign each an explicit disposition.

**Name semantic authority.** For every fact and decision, record authoritative producer, identity, grain, code set, unit, null rule, valid time, transaction time, correction rule, policy, and consumer interpretation. Retiring transport without transferring semantic authority produces a newer but ambiguous integration.

**Build a successor obligation map.** List every purpose, producer, consumer, schema, semantic, behavior, state, history, timing, ordering, error, service, security, privacy, retention, deletion, audit, support, recovery, and evidence obligation. Map each to a successor artifact and owner, an authorized changed obligation, or an authorized termination. Unmapped obligations block retirement.

**Version deliberate change.** A successor need not clone every legacy behavior. Publish changed semantics, error behavior, timing, delivery, availability, data scope, and policy with applicability intervals, mappings, consumer impact, tests, approvals, and sunset. Hidden change cannot be distinguished from retirement loss.

**Model authority through coexistence.** At each interval and for each population, specify which path may write, publish, transform, read, decide, enforce, correct, replay, recover, and supply evidence. Prefer one authoritative writer or publisher where possible. If authority is split, partition it by explicit keys, operations, consumers, or time rather than allowing both paths to compete.

**Choose a retirement seam.** Intercept at a facade, gateway, broker, scheduler, transfer route, view, contract, adapter, or product boundary where traffic and authority can be observed and redirected. A seam is useful only if bypass paths are inventoried, controlled, and tested.

**Use expand, migrate, and contract deliberately.** Expand the successor or interface to support old and new consumers. Migrate producers, consumers, state, and operations under evidence. Contract removes old fields, endpoints, topics, files, tables, adapters, and support. A program that never contracts has created a permanent compatibility architecture.

**Signal deprecation without confusing it with proof.** Publish machine-readable and human-readable lifecycle state, effective date, successor, migration guide, differences, support, telemetry, exceptions, sunset, and contact. Keep behavior compatible until the declared boundary unless a security or safety response requires otherwise. Measure receipt and adoption; a response header or documentation page does not migrate a client.

**Tailor signaling to integration style.** APIs can expose lifecycle headers and contract annotations. Events require schema, channel, producer, and consumer notices. Files require manifests, route metadata, schedules, and partner confirmation. Shared databases need view, permission, query, and owner evidence. Replication needs source and subscriber inventories. Human procedures need approved operational change.

**Provide a real successor.** Consumers need contracts, fixtures, credentials, environments, migration tooling, mappings, capacity, service objectives, error handling, observability, support, and time. A replacement that exists but cannot meet volume, schedule, jurisdiction, semantics, or recovery is not an accepted successor.

**Preserve stable identities during migration.** Correlate old and new dataset, message, job, run, consumer, contract, and decision identities. If identifiers must change, provide a versioned mapping with cardinality, applicability, collision, and correction rules. Identity continuity supports reconciliation, policy, lineage, and residual-use detection.

**Bind state transfer to a durable boundary.** Capture population, snapshot, log or sequence position, queued messages, in-flight files, retries, schedules, and clocks. Define ordering, duplicates, deletes, key changes, late arrivals, schema changes, poison records, failure, restart, gaps, overlaps, and resnapshot. Retiring the source before boundary reconciliation can make missing state irrecoverable.

**Reconcile by meaning and decision.** Compare named populations, positions, keys, semantics, values, transactions, sequences, aggregates, distributions, policy decisions, lineage, errors, and consumer outcomes. Classify divergences as lag, legacy defect, successor defect, mapping, approved change, observation error, or unknown. Every class needs an owner, correction, recheck, and consequence for retirement.

**Observe residual traffic.** Record requests, queries, writes, files, messages, subscriptions, offsets, replication changes, scheduler invocations, retries, restores, credentials, manual actions, and downstream decisions. Use stable candidate and consumer identities. Sampling, aggregation, missing telemetry, and clock mismatch can hide low-frequency critical use, so report coverage and limitations.

**Turn residual use into governed work.** Unexpected traffic creates an event with candidate, consumer, contract, timestamp, purpose, payload class, authority impact, owner, response, deadline, and decision. Do not silently serve forever or immediately break the consumer. Resolve, migrate, terminate, except with expiry, or replan.

**Test negative discovery.** Disable or deny the candidate for a bounded low-risk cohort or interval, route invocations to a controlled sink, expire a noncritical credential, or require explicit renewal. Observe who fails and which manual work appears. Active probes can reveal dependencies that passive telemetry misses, but require safety, privacy, support, rollback, and approval.

**Quarantine before destructive closure.** Remove production authority and normal routing while preserving a bounded, access-controlled ability to inspect or restore. Page on attempted use rather than automatically executing it. Define duration, data controls, support, costs, rollback, evidence, exceptions, and exit. Quarantine is a decision instrument, not indefinite limbo.

**Treat queues and retries as state.** Drain, transfer, expire, dead-letter, reconcile, or deliberately discard each message population under contract. Check producer retry windows, consumer lag, delayed delivery, poison messages, scheduled redelivery, transaction coordination, and replay. Deleting an apparently idle topic can erase unprocessed authority.

**Retire replication at both ends.** Stop and verify target consumption, record final source position, reconcile state, resolve conflicts, close subscriptions and connectors, remove publications and slots, release retained logs, revoke credentials, remove network access, close alerts, and test source failover and recovery configuration. A stopped connector may still impose source retention and security burden.

**Retire shared-database access explicitly.** Discover queries, writes, views, procedures, triggers, database links, users, roles, connection strings, reporting tools, and recovery scripts. Migrate semantics and transactions behind governed products or interfaces. Revoke paths gradually under telemetry and prevent restored clients from reconnecting.

**Retire files and batch exchange end to end.** Close producer schedules, manifests, transfer accounts, encryption keys, routes, landing zones, scanners, parsers, archives, acknowledgments, retries, partner procedures, and downstream loads. Reconcile final files and acknowledgment state. A landing directory with no new files can still contain sensitive history and active credentials.

**Retire APIs as consumer contracts.** Inventory operations, versions, clients, SDKs, gateways, routes, DNS, caches, credentials, quotas, policies, documentation, examples, tests, monitors, and support. Verify successor behavior, client migration, and error handling. Preserve a tombstone response or controlled denial where silent identifier reuse would be dangerous.

**Retire event channels as shared protocols.** Inventory producers, direct and transitive consumers, schemas, keys, partitions, ordering, delivery, retention, replay, dead letters, connectors, ACLs, quotas, and disaster procedures. Move authority and consumer offsets deliberately. Decide whether the channel is deleted, sealed, archived, or tombstoned.

**Retire hub and adapter logic by behavior.** A central broker, enterprise service bus, or integration platform may transform, route, enrich, sequence, validate, retry, correlate, authorize, and audit. Mapping only destinations loses behavior. Decompose flows into explicit contracts and successor obligations, then remove shared runtime and management-plane dependencies.

**Retire federation without losing source protection.** Identify virtual objects, connectors, pushdowns, cached results, source credentials, query policies, network paths, and dependent semantic models. Verify successor materialization or alternate access, source-load changes, consistency, policy, and cost. Remove cached and credentialed remnants as well as the virtual definition.

**Preserve required records separately from runtime.** Determine which contracts, schemas, mappings, positions, messages, files, lineage, policy decisions, logs, reconciliations, incidents, approvals, and source data remain needed for audit, correction, legal hold, recovery, or explanation. Store them in governed archival forms with owner, meaning, access, integrity, retention, deletion, and tested retrieval.

**Do not confuse backup with archive.** Backups optimize recovery of a system state; archives preserve selected records for governed retrieval and disposition. A proprietary backup may be inaccessible after license or skill retirement. Test catalog discovery, interpretation, key custody, restore tooling, dependencies, cost, and deletion at the required horizon.

**Apply risk-based sanitization.** Identify every copy on databases, object stores, filesystems, caches, logs, queues, snapshots, backups, replicas, endpoints, appliances, removable media, and suppliers. Select clear, purge, cryptographic erase, provider deletion, destruction, or another approved method according to confidentiality, technology, custody, reuse, threat, and policy. Preserve verification and disposition records.

**Distinguish deletion planes.** Deleting a table may leave snapshots, transaction logs, replicas, caches, search indexes, exports, backups, and provider recovery copies. Deleting encryption keys may not cover alternate keys or plaintext copies. Define scope, propagation, delay, exceptions, legal holds, confirmation, and residual risk across every plane.

**Revoke identities and trust.** Remove service accounts, API keys, certificates, secrets, tokens, roles, groups, grants, trust relationships, allowlists, firewall rules, tunnels, private links, partner identities, and break-glass paths. Check cached credentials and long-lived sessions. Identity removal must not destroy access to preserved evidence that still has an authorized purpose.

**Close control-plane artifacts.** Remove catalog entries or mark them durably retired, close schemas and contracts, disable schedulers, delete or seal routes and topics, remove policies, flags, dashboards, alerts, runbooks, tests, deployment definitions, infrastructure code, and automatic repair. Keep only controlled tombstones and records needed to prevent accidental recreation or support audit.

**Handle identifiers as hazardous assets.** Reusing an endpoint, topic, queue, dataset, file path, client ID, certificate name, contract version, or schedule can awaken cached clients and old automation. Maintain namespaces, tombstones, deny rules, and governance that distinguish intentional new creation from restoration of retired authority.

**Plan rollback before retirement authority changes.** Preserve the latest safe position, source capacity, contracts, policies, identities, mappings, operator access, and correction procedures for a bounded interval. Account for successor-only state and external effects. Define a point after which roll-forward or partitioned authority is safer than reviving the source.

**Separate rollback from recovery.** Rollback responds to a bad change by returning authority or behavior. Recovery responds to loss or corruption by reconstructing a coherent state. A retirement may make old recovery tooling invalid before rollback expires, or preserve old restore automation after authority has ended. Design both against the same state and authority model.

**Exercise successor recovery without legacy help.** Restore data, messages, contracts, schemas, identity, policy, lineage, orchestration, consumers, keys, and evidence in dependency order. Inject loss of the old integration and old operators. Validate business invariants, consumer decisions, service, and authority. If recovery still reads the legacy route, retirement is premature.

**Test nonactivation using restored artifacts.** In isolation, restore old backups, infrastructure definitions, scheduler state, consumer configuration, cached routes, and credentials. Durable tombstones, revoked trust, removed network paths, denied publication, sealed topics, and unique successor identities should prevent old behavior from escaping. Record every attempted reactivation and corrective removal.

**Close financial and supplier obligations.** Terminate compute, storage, network, transfer, broker, database, monitoring, licenses, support, minimum spends, reservations, vendor accounts, managed-transfer contracts, and professional services attributable to the integration. Verify invoices and allocation after closure. Cost avoidance is realized evidence, not an estimate copied from the retirement plan.

**Transfer operational ownership.** Ensure successor producers, consumers, platform operators, security, privacy, support, partners, finance, procurement, compliance, and incident responders accept contracts, access, procedures, escalation, capacity, and decision rights. Preserve contact paths for archived evidence while closing obsolete support rotations.

**Measure retirement outcomes.** Compare reduced incidents, attack surface, privacy exposure, change lead time, consumer reliability, operator toil, spend, dependency count, recovery performance, and business outcomes with the baseline. Countermetrics include migration defects, unmet consumers, new coupling, target concentration, and support burden. A deleted server count is not an outcome.

**Record residual risk and exceptions.** Some consumers, records, suppliers, or legal holds may remain. Give each scope, owner, authority, rationale, control, cost, expiry, review, and successor. An exception without expiry is a retained architecture and must be represented honestly.

**Preserve the retirement receipt.** Bind candidate identity, observed graph, evidence coverage, successor obligations, contract versions, state boundary, reconciliations, consumer decisions, authority changes, deprecation and sunset, residual traffic, quarantine, rollback, recovery, removals, archives, sanitization, costs, exceptions, outcome evidence, nonactivation, approval, and limitations. Future investigators should be able to explain what ended and why it cannot silently return.

## Definitions and Notation

Let a retirement architecture be:

`R = (U, B, N, A, C, D, G, Q, T, E, K, L)`.

`U` contains purposes, users, affected parties, decisions, termination rationale, intended outcomes, countermetrics, and observation horizons. A purpose can end, transfer, narrow, or change; each outcome must be judged from the affected user's perspective.

`B = (b_l, b_s)` contains versioned observed-legacy and accepted-successor baselines. The legacy baseline includes runtime, control plane, consumers, semantics, state, human procedures, service, recovery, suppliers, costs, and evidence confidence. The successor baseline includes deployed capability and accepted obligations, not aspirational diagrams.

`N = (V, E)` is a typed directed integration graph. A node `v in V` may be a producer, consumer, store, broker, API, scheduler, catalog, identity system, policy engine, person, supplier, or recovery asset. An edge:

`e = (id, from, to, kind, contract, population, schedule, authority, policy, service, evidence)`

identifies a query, write, command, event, file, replication flow, policy decision, manual action, or recovery dependency.

A dependency assertion is:

`dep(e, state, observed_at, source, confidence)`,

where `state` is declared, configured, observed, inferred, confirmed, rejected, or unknown. Confidence never converts incomplete coverage into proof of absence.

`A` contains owners and authority. Define:

`authority(fact, population, consumer, time) -> (publisher, reader, semantics, policy, clock, correction, recovery)`.

Retirement requires the legacy candidate to map to `none` for operational authority after closure while preserved evidence retains a separate, access-controlled custodian.

`C` contains structural, semantic, behavioral, service, support, change, and termination contracts. A successor obligation:

`map(obligation_l) -> obligation_s | changed_approved | terminated_approved`

must exist for every required legacy obligation. An unresolved or merely assumed mapping blocks retirement.

`D` contains populations, state, history, snapshots, positions, queued work, ordering, duplicates, deletes, late data, corrections, replay, lineage, reconciliation, archive, and disposal. At final boundary `p`, the successor claim is:

`successor_state(p) = transform(legacy_snapshot, changes_to_p, mappings, reference_data, policy)`.

The expression names necessary inputs; it does not prove total ordering, transformation determinism, or semantic equivalence.

`G` contains ownership, governance, security, privacy, purpose, classification, identity, access, encryption, residency, retention, deletion, legal hold, audit, exception, supplier, sanitization, and evidence custody.

`Q` contains quality, correctness, freshness, latency, delivery, availability, capacity, failure, degraded mode, support, data-loss bounds, recovery-time bounds, and business recovery invariants.

`T` contains deprecation, sunset, expand-migrate-contract, shadowing, dual run, exposure, cutover, rollback, quarantine, removal, and nonactivation. A lifecycle state transition is:

`active -> deprecated -> sunset_pending -> quarantined -> retired -> closed`.

Some candidates legitimately skip signaling or quarantine because of urgent security, safety, or legal conditions, but the deviation and authority must be recorded.

`E` contains configuration discovery, traffic, lineage, schedules, access, billing, incidents, interviews, consumer confirmation, active probes, reconciliations, exercises, outcomes, and limitations. Negative evidence is:

`quiet(candidate, channels, horizon, coverage)`,

not simply zero counted requests. The channels, periodicity, sampling, clocks, and missing coverage determine what the observation supports.

`K` contains compute, storage, network, licensing, support, commitments, supplier accounts, people, skills, operational toil, retirement cost, and realized savings.

`L` contains successors, exceptions, archives, tombstones, identifier controls, removal inventories, sanitization, receipts, review, nonactivation, and closure.

A retirement candidate `r` is admissible only if:

`Retire(r) = S_r and D_r and A_r and X_r and Q_r and N_r`,

where `S_r` means required obligations have an accepted successor or authorized termination, `D_r` means dependencies and consumers are resolved, `A_r` means legacy authority has ended or is bounded for transition, `X_r` means state and decisions reconcile, `Q_r` means successor recovery no longer depends on the legacy path, and `N_r` means nonactivation and removal evidence exists. These are necessary gates for this model, not universal proof of safe disposal.

Let residual exposure be recorded as:

`residual = active_paths + recoverable_paths + unresolved_consumers + retained_data + open_costs + exceptions`.

The terms are heterogeneous and should not be collapsed into a misleading scalar. Closure requires each term to be empty, deliberately retained under explicit control, or accepted by authorized risk ownership.

## Mechanisms, Invariants, or Proof Structure

The assurance structure begins with a named candidate and ends with a tested absence of obsolete authority.

**Decision gate.** Bind candidate, purpose, owner, sponsor, retirement driver, successor or termination, affected users, scope, deadline, risk tolerance, evidence horizon, approval, and review trigger.

**Identity gate.** Record exact endpoints, routes, channels, topics, files, directories, tables, views, jobs, schedules, database objects, credentials, versions, environments, suppliers, and recovery assets.

**Graph gate.** Model producer, consumer, store, broker, scheduler, gateway, identity, policy, catalog, person, supplier, and recovery nodes with typed, directional, authoritative edges.

**Discovery gate.** Combine configuration, code, database metadata, network, gateway, broker, scheduler, file, object, lineage, catalog, identity, secrets, billing, incidents, support, recovery, interviews, and consumer evidence with coverage limits.

**Periodicity gate.** Observe daily, close, quarterly, annual, regulatory, partner, model, incident, recovery, legal, and correction cycles appropriate to candidate criticality.

**Contract gate.** Version structure, semantics, behavior, ordering, delivery, idempotency, timing, errors, retries, authentication, authorization, quality, service, support, change, recovery, retention, and termination.

**Obligation gate.** Map every purpose, producer, consumer, contract, semantic, state, policy, service, support, recovery, and evidence obligation to an accepted successor, approved change, or authorized termination.

**Authority gate.** Allocate publish, write, transform, read, decide, enforce, correct, replay, recover, and evidence custody by population, consumer, and time.

**State gate.** Bind snapshot, final position, queued work, in-flight requests, retries, files, messages, ordering, duplicates, deletes, schema, late data, corrections, replay, lineage, and archive.

**Reconciliation gate.** Define population, position, keys, semantics, values, transactions, sequences, aggregates, policy, errors, lineage, consumer decisions, divergence classes, owners, correction, and recheck.

**Successor gate.** Verify contracts, fixtures, credentials, environments, capacity, policy, telemetry, support, failure behavior, recovery, and consumer acceptance for the actual workload.

**Signaling gate.** Publish lifecycle state, dates, successor, migration guide, differences, support, contact, exceptions, sunset, and machine-readable annotations appropriate to integration style.

**Consumer gate.** Identify direct, transitive, cached, scheduled, manual, partner, rare, restored, and disaster consumers; record migration, termination, exception, or unresolved status under an owner.

**Residual-use gate.** Observe requests, queries, writes, files, messages, offsets, replication, schedules, retries, credentials, restores, manual acts, and decisions with stable identities, clocks, coverage, and limitations.

**Probe gate.** Use approved low-risk denial, sink routing, credential renewal, or bounded outage to expose hidden dependencies while preserving safety, privacy, support, rollback, and evidence.

**Policy gate.** Preserve purpose, classification, ownership, identity, access, encryption, residency, minimization, retention, deletion, legal hold, audit, response, supplier, and exception controls through retirement.

**Service gate.** Verify successor correctness, freshness, latency, delivery, availability, capacity, failure, degraded operation, support, data-loss bounds, and recovery-time bounds.

**Rollback gate.** Preserve a bounded safe position, state convergence, source capacity, contracts, policy, identities, mappings, operator access, corrections, external-effect compensation, and point of no return.

**Recovery gate.** Restore successor state, messages, metadata, contracts, identity, policy, lineage, orchestration, consumers, keys, records, and business invariants without legacy authority or operators.

**Quarantine gate.** Remove normal authority and execution, page on attempted use, limit access and duration, preserve bounded inspection or rollback, fund cost, and define destruction and exception exits.

**Style-specific gate.** Close source and target artifacts for database, replication, API, event, file, batch, hub, adapter, federation, shared-store, partner, and human flows according to their distinct state and control planes.

**Record gate.** Preserve required contracts, schemas, mappings, positions, messages, lineage, policy decisions, logs, reconciliations, incidents, approvals, and source data with interpretation, integrity, access, retention, deletion, and tested retrieval.

**Sanitization gate.** Inventory all copies, choose an approved assurance for confidentiality and media or provider conditions, execute, verify, preserve disposition evidence, and record residual limitations.

**Trust-removal gate.** Revoke service accounts, keys, certificates, tokens, roles, groups, grants, allowlists, tunnels, links, partner identities, cached sessions, and break-glass paths not needed for controlled records.

**Control-plane gate.** Remove or tombstone catalogs, contracts, schemas, schedules, routes, topics, policies, flags, dashboards, alerts, runbooks, tests, deployments, infrastructure definitions, and automatic repair.

**Economic gate.** Close compute, storage, network, transfer, database, broker, monitoring, licenses, support, reservations, minimum spends, vendor accounts, and attributable operational toil; verify realized invoices.

**Identifier gate.** Prevent reuse or collision of retired endpoints, topics, datasets, paths, client identities, certificates, contract versions, and schedules without a new governed decision.

**Nonactivation gate.** Restore old configuration, backups, schedules, consumers, routes, and credentials in isolation; verify tombstones, denied publication, revoked trust, removed paths, and unique successor identity contain every attempt.

**Outcome gate.** Compare incidents, exposure, lead time, reliability, toil, spend, dependency count, recovery, and user outcomes with the baseline while monitoring migration defects, new coupling, concentration, and support burden.

**Receipt gate.** Bind identity, graph, coverage, obligations, versions, state, reconciliation, consumer decisions, authority, signaling, residual use, quarantine, rollback, recovery, removal, archive, sanitization, costs, exceptions, nonactivation, outcomes, approval, and limitations.

### Executable evidence: retirement-candidate admission

The following program classifies ten invented retirement candidates against six mandatory gates.

<!-- bijux-verify: {"id":"retirement-candidate-admission","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"candidates=10\nretirable=4\nmissing_successor=1\nunknown_consumer=1\nauthority_active=1\nunreconciled_state=1\nrecovery_dependency=1\nreactivation_path=1\nintegration_styles=8\naffected_domains=7\nauthority_states=4\nretirement_receipts=10\ndecision_events=10\n","stderr":""}} -->
```python
candidates = [
    {"style": "point-to-point", "domains": {"orders"}, "authority_state": "target", "successor": True, "dependencies": True, "authority_closed": True, "reconciled": True, "recovery_independent": True, "nonactivation": True},
    {"style": "api", "domains": {"customer", "orders"}, "authority_state": "none", "successor": True, "dependencies": True, "authority_closed": True, "reconciled": True, "recovery_independent": True, "nonactivation": True},
    {"style": "event", "domains": {"risk"}, "authority_state": "target", "successor": True, "dependencies": True, "authority_closed": True, "reconciled": True, "recovery_independent": True, "nonactivation": True},
    {"style": "file-exchange", "domains": {"partner"}, "authority_state": "none", "successor": True, "dependencies": True, "authority_closed": True, "reconciled": True, "recovery_independent": True, "nonactivation": True},
    {"style": "shared-database", "domains": {"catalog"}, "authority_state": "source", "successor": False, "dependencies": True, "authority_closed": True, "reconciled": True, "recovery_independent": True, "nonactivation": True},
    {"style": "hub-spoke", "domains": {"inventory", "orders"}, "authority_state": "split", "successor": True, "dependencies": False, "authority_closed": True, "reconciled": True, "recovery_independent": True, "nonactivation": True},
    {"style": "federation", "domains": {"customer"}, "authority_state": "source", "successor": True, "dependencies": True, "authority_closed": False, "reconciled": True, "recovery_independent": True, "nonactivation": True},
    {"style": "replication", "domains": {"finance"}, "authority_state": "split", "successor": True, "dependencies": True, "authority_closed": True, "reconciled": False, "recovery_independent": True, "nonactivation": True},
    {"style": "event", "domains": {"risk", "finance"}, "authority_state": "target", "successor": True, "dependencies": True, "authority_closed": True, "reconciled": True, "recovery_independent": False, "nonactivation": True},
    {"style": "file-exchange", "domains": {"partner", "inventory"}, "authority_state": "none", "successor": True, "dependencies": True, "authority_closed": True, "reconciled": True, "recovery_independent": True, "nonactivation": False},
]

def evaluate(candidate):
    if not candidate["successor"]:
        return "missing_successor"
    if not candidate["dependencies"]:
        return "unknown_consumer"
    if not candidate["authority_closed"]:
        return "authority_active"
    if not candidate["reconciled"]:
        return "unreconciled_state"
    if not candidate["recovery_independent"]:
        return "recovery_dependency"
    if not candidate["nonactivation"]:
        return "reactivation_path"
    return "retirable"

results = [evaluate(candidate) for candidate in candidates]
print(f"candidates={len(candidates)}")
for outcome in ["retirable", "missing_successor", "unknown_consumer", "authority_active", "unreconciled_state", "recovery_dependency", "reactivation_path"]:
    print(f"{outcome}={results.count(outcome)}")
print(f"integration_styles={len({candidate['style'] for candidate in candidates})}")
print(f"affected_domains={len(set().union(*(candidate['domains'] for candidate in candidates)))}")
print(f"authority_states={len({candidate['authority_state'] for candidate in candidates})}")
print(f"retirement_receipts={len(candidates)}")
print(f"decision_events={len(results)}")
```

The output reports ten candidates, four retirable and one of each declared failure, eight integration styles, seven affected domains, four authority states, ten receipts, and ten decisions.

The evidence is deliberately narrow. Invented Booleans, labels, and sets establish deterministic gate order and counts only. They do not establish that the successor is accepted, consumers are known, authority has ended, state reconciles, recovery is independent, nonactivation works, sanitization is sufficient, or any integration is safe to retire. Production assurance requires observed graphs, contracts, consumer and owner decisions, production state, positions, reconciliations, policy tests, traffic coverage, active probes, cutover and rollback exercises, successor recovery, removal inventories, disposal evidence, invoices, and isolated restoration tests.

## Alternatives and Trade-Offs

**Immediate shutdown.** Exposure and operating burden can end quickly when a security, safety, legal, or corruption threat dominates. Hidden consumers, in-flight state, evidence loss, and uncontrolled manual work can create harm. Use explicit authority, incident coordination, preservation, and correction.

**Deprecate then sunset.** Consumers receive time, documentation, and lifecycle signals. Coexistence, support, ambiguity, and attack surface persist, while notices may be ignored. Admission requires observed migration rather than elapsed calendar alone.

**Expand, migrate, contract.** Compatibility and consumer movement can be bounded and observable. Adapters and dual support can become permanent if contraction lacks ownership, expiry, and removal gates.

**Facade or strangler.** Routing and observation at a seam can reduce blast radius and expose bypasses. The facade becomes a critical semantic, policy, and service component and must itself have a retirement path.

**Parallel operation.** Old and new outputs can be compared before authority moves. Duplicate processing, privacy exposure, capacity, divergence, and operational ambiguity grow. Prefer one governing result and explicit comparison semantics.

**Consumer-by-consumer retirement.** Evidence and support can match each client's constraints. Total duration, compatibility burden, exception handling, and coordination cost increase.

**One-time ecosystem cutover.** Coexistence and split authority may be shorter. State, client, partner, schedule, and recovery coordination create large blast radius and rollback complexity.

**Quarantine.** Hidden invocations and restoration needs can be discovered before destruction. Cost and ambiguity remain, and quarantine can become indefinite without expiry and authority controls.

**Retain as explicit exception.** A rare regulatory, partner, or recovery dependency can remain safely when owner, scope, controls, service, cost, and review are explicit. The exception can preserve legacy coupling and block broader closure.

**Archive the interface evidence.** Contracts, messages, mappings, lineage, decisions, and state can remain interpretable after runtime closes. Storage, key custody, format decay, access, legal hold, and deletion obligations continue.

**Delete logical objects.** Normal use can end quickly and recoverable rollback may remain. Snapshots, replicas, logs, caches, backups, and provider copies can preserve sensitive state and reactivation.

**Cryptographic erase or purge.** Stronger confidentiality assurance and rapid large-scale disposal may be possible. Key scope, copies, alternate encryption, provider control, media technology, evidence, and regulatory acceptance must be established.

**Tombstone identifiers.** Cached consumers and restored automation fail safely rather than connecting to a new service. Namespace remains occupied and operating controls must preserve the tombstone.

**Reuse identifiers.** Naming and migration convenience improve. Old clients, routes, credentials, caches, or recovery automation can silently act on new authority; proof burden is high.

**Automated discovery.** Broad inventories can be updated repeatedly at scale. Dynamic, human, external, rare, encrypted, sampled, and recovery paths remain incomplete.

**Active negative probes.** Hidden dependencies become observable. Even bounded denial can affect users, trigger unsafe manual work, or violate service and policy; approval and rollback are mandatory.

**Preserve source recovery temporarily.** Early rollback remains possible. Obsolete authority, credentials, cost, policy drift, and restore risk persist. Define an explicit point of no return and final nonactivation test.

**Roll forward only.** New-only state and simplified authority can avoid dangerous legacy restoration. Correction tooling, target resilience, operator skill, and evidence requirements increase.

**Central retirement program.** Common discovery, tombstones, controls, evidence, tooling, and commercial closure can improve consistency. Central queues may lack domain meaning and become a bottleneck.

**Domain-owned retirement.** Semantic and consumer knowledge stays near the work. Cross-domain edges, shared infrastructure, policy, supplier contracts, and portfolio risk need federated oversight.

## Failure Modes and Misconceptions

1. **“Turned off means retired.”** Configuration, credentials, queues, backups, consumers, and recovery can restore authority.
2. **“Old means unnecessary.”** Age says nothing about purpose, correctness, criticality, or replacement.
3. **“A replacement deployment proves obligation transfer.”** Consumers, semantics, policy, service, and recovery require acceptance evidence.
4. **“No owner means no consumer.”** It often signals weak inventory and accountability.
5. **“No recent traffic means unused.”** Rare close, regulatory, incident, legal, and disaster workloads remain.
6. **“Gateway logs show every API consumer.”** Caches, bypass routes, batch clients, partners, and sampled telemetry escape.
7. **“Broker membership lists every event consumer.”** Republishers, sinks, caches, and offline replay create transitive use.
8. **“Static parsing finds every dependency.”** Dynamic SQL, configuration, humans, suppliers, and restored systems remain.
9. **“A catalog graph proves absence.”** Missing or stale instrumentation can create false confidence.
10. **“A universal quiet period is safe.”** Observation must span the candidate's actual periodicity and risk.
11. **“An integration is one edge.”** Control, data, identity, policy, evidence, support, and recovery edges coexist.
12. **“Transport replacement preserves meaning.”** Grain, identity, time, ordering, correction, and error semantics can change.
13. **“Matching schemas prove contract parity.”** Behavior, delivery, service, policy, and support obligations remain.
14. **“Every legacy quirk must survive.”** Defects and obsolete behavior need explicit disposition, not automatic preservation.
15. **“A successor may change semantics silently.”** Hidden change is indistinguishable from retirement loss.
16. **“Deprecation changes behavior.”** It communicates lifecycle state; consumers can continue operating.
17. **“A sunset date authorizes shutdown.”** Readiness and risk owners must accept evidence at the boundary.
18. **“Documentation migrates clients.”** Credentials, code, tests, deployment, capacity, and observed use must move.
19. **“Consumer acknowledgment proves execution.”** Cached or dormant deployments can retain the old path.
20. **“A facade captures every bypass.”** Direct database, network, file, and restored routes can remain.
21. **“Parallel operation means both paths are authoritative.”** Competing truth creates ambiguity and divergence.
22. **“A final row count reconciles state.”** Keys, values, time, transactions, ordering, deletes, and decisions can differ.
23. **“A checksum proves semantic equivalence.”** Representation can change legitimately or match with shared defects.
24. **“Every difference is a successor bug.”** Lag, legacy defects, approved changes, and observation errors exist.
25. **“Manual repair closes divergence.”** Unrecorded patches create a third truth and break replay.
26. **“A stopped connector releases source burden.”** Slots, publications, offsets, logs, credentials, and alerts may persist.
27. **“An empty queue is safe to delete.”** Delayed producers, retries, replay, dead letters, and retained contracts remain.
28. **“Zero consumer lag means all events were correct.”** Wrong schemas, keys, policy, and handlers can converge incorrectly.
29. **“A landing directory with no new file is closed.”** History, keys, accounts, schedules, retries, and partner procedures persist.
30. **“Revoking one service account closes trust.”** Cached tokens, certificates, groups, break-glass, and supplier paths remain.
31. **“Removing the endpoint removes the API.”** DNS, gateways, caches, SDKs, documentation, monitors, and identifiers persist.
32. **“Deleting a topic removes event state.”** Replicas, archives, dead letters, offsets, connectors, and schemas remain.
33. **“Dropping a view closes database integration.”** Direct queries, procedures, links, roles, and restore scripts remain.
34. **“Removing a virtual object removes federation.”** Connectors, caches, credentials, policies, and semantic dependencies remain.
35. **“Disabling a hub flow removes its behavior.”** Transform, route, sequence, retry, correlate, authorize, and audit obligations remain.
36. **“Humans are outside the architecture.”** Manual correction, resend, approval, and exception procedures are integration.
37. **“Backup is archive.”** Recovery images may be undiscoverable, uninterpretable, licensed, overbroad, or impossible to delete selectively.
38. **“Delete means sanitized.”** Logs, snapshots, replicas, caches, media, and provider recovery copies can retain data.
39. **“Key deletion covers every copy.”** Alternate keys, plaintext exports, logs, and downstream stores can survive.
40. **“Sanitization needs no verification.”** Scope, method, execution, custody, result, and residual assurance require evidence.
41. **“Quarantine can run indefinitely.”** It preserves cost, access, ambiguity, and accidental restoration risk.
42. **“Rollback is always safer.”** Successor-only state and external effects can make legacy return destructive.
43. **“Rollback and recovery are the same.”** They address different events and may require conflicting authority.
44. **“A source backup proves successor recovery.”** Retirement requires recovery without obsolete dependency.
45. **“Infrastructure code is harmless history.”** Automatic repair or redeployment can recreate retired authority.
46. **“Identifier reuse is only naming.”** Cached consumers and old credentials can attach to new behavior.
47. **“Removing runtime closes cost.”** Licenses, commitments, storage, monitoring, vendors, and support can continue billing.
48. **“Server count measures retirement value.”** Outcomes, incidents, risk, toil, spend, and dependency closure matter.
49. **“An exception without expiry is temporary.”** It is a retained architecture with hidden ownership and cost.
50. **“A clean shutdown proves nonactivation.”** Only restored-artifact tests expose dormant automation and trust paths.

## Worked Examples

### Example 1

A point-to-point order feed appears redundant after an event product launches. Network flow, scheduler, lineage, and consumer interviews expose a fraud cache and a manual replay script. Both gain successor contracts and tests before the direct feed enters quarantine; the replay procedure is rebuilt against the event archive and exercised.

### Example 2

An HTTP endpoint emits standardized deprecation and sunset metadata plus a migration link. Telemetry identifies clients by credential and operation, but a cached mobile version remains invisible until a bounded denial probe. Its owner receives a time-limited exception, successor SDK, test environment, and explicit final decision rather than an unexamined calendar extension.

### Example 3

A shared customer table has identical target columns, yet a stored procedure applies consent corrections in business-local valid time. The obligation map captures that behavior, versions its semantics, and tests target correction, audit, deletion, and consumer decisions before direct write roles are revoked.

### Example 4

A replication connector is stopped after target cutover, but source log storage continues growing. Investigation finds an active publication and slot plus a disaster script that recreates the subscription. The team records the final position, reconciles data, rebuilds target recovery, removes both ends, revokes credentials, and verifies source failover no longer restores them.

### Example 5

A broker topic has zero lag and no recent production. A quarterly settlement consumer and a delayed dead-letter replay still depend on its schema and retention. Retirement waits through the settlement cycle, migrates offsets and archives required messages, drains or resolves dead letters, and tombstones the topic name.

### Example 6

A nightly partner file is replaced by an API. Final reconciliation includes manifest, record identities, acknowledgments, retries, corrections, and partner decisions. Schedules, SFTP account, SSH keys, firewall rule, landing directory, parser, archive, monitor, and vendor charge close only after the partner executes the successor in production.

### Example 7

A federation view is removed, yet dashboard latency and source load spike because its cached materialization also disappeared. The dependency graph had modeled only the virtual definition. The team restores the cache temporarily, records its service obligation, provisions a governed successor product, and reruns retirement gates.

### Example 8

A quarantined batch job pages whenever invoked instead of processing. During a year-end close rehearsal, an undocumented operator procedure calls it. The procedure is replaced, segregation of duties is preserved, and the observation horizon extends through the relevant close before destructive removal.

### Example 9

A successor begins accepting a new identifier that the legacy hub cannot represent. Rollback testing reveals that returning all traffic would lose target-only state. The authority model keeps the new population on the successor, replays compatible changes to the old path for remaining consumers, and defines a near-term roll-forward correction.

### Example 10

After final shutdown, an isolated exercise restores an old infrastructure definition, scheduler backup, endpoint name, and certificate. The certificate is revoked, the route absent, the endpoint tombstoned, and publication denied, so no behavior escapes. The exercise discovers one surviving monitoring license and provider snapshot, which close before the receipt is approved.

## Cross-Program Connections

- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) provides interface contracts, versioning, deprecation, sunset, gateways, compatibility, client migration, traffic evidence, errors, and endpoint retirement.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) owns paved retirement workflows, catalogs, identity, secrets, deployment, policy, telemetry, support, cost controls, recovery, tombstones, and infrastructure removal.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) implements dependency discovery, pipelines, state transfer, change capture, reconciliation, lineage, replay, quality, archive, and job retirement.
- [Database Engineering](../../18-database-engineering/ROADMAP.md) grounds shared-database dependencies, queries, procedures, triggers, replication, slots, constraints, backup, restore, access removal, and disposal.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) explains partial failure, ordering, duplication, delivery, idempotency, convergence, retries, queues, rollback, and replay.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) governs identity, credentials, trust, attack surface, logs, suppliers, incidents, sanitization, recovery, and secure disposal.
- [Network Engineering](../../24-network-engineering/ROADMAP.md) supplies flow evidence, routes, DNS, gateways, tunnels, firewalls, segmentation, partner paths, failure, and actual connectivity removal.
- [Cloud and Infrastructure Engineering](../../30-cloud-and-infrastructure-engineering/ROADMAP.md) connects provider resources, infrastructure definitions, storage, snapshots, identity, networking, billing, recovery, supplier closure, and exit.
- [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) contributes seams, facades, adapters, gradual displacement, parallel change, coupling, architecture decisions, and evolutionary structure.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies baselines, integration, de-integration, transition, configuration, readiness, verification, validation, risk, closeout, and disposal discipline.

## References

1. NASA, [Product Integration](https://www.nasa.gov/reference/5-2-product-integration/), system interactions, integration planning, de-integration, disposal, closeout, and archiving.
2. NASA, [Product Transition](https://www.nasa.gov/reference/5-5-product-transition/), product, site, operator, user, support, recovery, disposal, acceptance, and transition work products.
3. Martin Fowler, [Strangler Fig](https://martinfowler.com/bliki/StranglerFigApplication.html), seams, gradual displacement, transitional architecture, bounded change, and organizational learning.
4. Danilo Sato, [Parallel Change](https://martinfowler.com/bliki/ParallelChange.html), expand-migrate-contract compatibility and interface contraction.
5. IETF, [RFC 9745: The Deprecation HTTP Response Header Field](https://www.rfc-editor.org/rfc/rfc9745.html), deprecation dates, lifecycle signaling, documentation links, and resource behavior.
6. IETF, [RFC 8594: The Sunset HTTP Header Field](https://www.rfc-editor.org/rfc/rfc8594.html), communicating expected future unavailability of resources.
7. OpenAPI Initiative, [OpenAPI Specification](https://spec.openapis.org/oas/latest.html), HTTP operations, schemas, parameters, responses, security, versions, and deprecation.
8. AsyncAPI Initiative, [Specification](https://www.asyncapi.com/docs/reference/specification/latest), asynchronous channels, operations, messages, servers, security, and bindings.
9. Bitol, [Open Data Contract Standard](https://bitol-io.github.io/open-data-contract-standard/latest/), schema, quality, service, roles, support, and infrastructure obligations.
10. PostgreSQL Global Development Group, [Logical Replication](https://www.postgresql.org/docs/current/logical-replication.html), publications, subscriptions, snapshots, changes, ordering, conflicts, monitoring, and security.
11. Debezium, [Architecture](https://debezium.io/documentation/reference/stable/architecture.html), log-based connectors, source offsets, records, schemas, and deployment forms.
12. OpenLineage, [Object Model](https://openlineage.io/docs/spec/object-model/), dataset, job, run, event, namespace, name, and facet identities.
13. Open Policy Agent, [Policy Language](https://www.openpolicyagent.org/docs/policy-language), structured policy decisions, inputs, rules, tests, and runtime context.
14. OpenTelemetry, [Specification](https://opentelemetry.io/docs/specs/otel/), signals, resources, context, semantic conventions, sampling, compatibility, and versioning.
15. NIST, [SP 800-88 Revision 1: Guidelines for Media Sanitization](https://csrc.nist.gov/pubs/sp/800/88/r1/final), risk-based clearing, purging, destruction, verification, and disposition.
16. FinOps Foundation, [FinOps Framework](https://www.finops.org/framework/), cross-functional ownership, usage, cost, value, optimization, governance, and technology decisions.

## Exercises

### Exercise 1

Build a retirement case for a shared customer database used by direct queries, batch files, an API, change capture, an event topic, federated views, reports, partners, operators, and recovery. Define identities, graph, evidence, confidence, purposes, contracts, consumers, successor obligations, authority, state, policy, service, costs, and closure.

### Exercise 2

Design deprecation, sunset, migration, and consumer-closure mechanisms for an API and event channel. Include machine-readable signals, documentation, contracts, SDKs, schemas, credentials, client identity, transitive consumers, residual traffic, periodicity, active probes, exceptions, support, and final removal.

### Exercise 3

Specify final-state transfer and reconciliation for a replication link and file exchange. Address snapshot and positions, queues, messages, files, acknowledgments, retries, ordering, duplicates, deletes, schema change, corrections, lineage, policy, archives, and consumer decisions.

### Exercise 4

Create rollback, recovery, quarantine, and nonactivation plans for a legacy integration hub. Cover transformations, routing, state, target-only data, external effects, operators, control plane, credentials, identifiers, infrastructure definitions, restored automation, stop conditions, and points of no return.

### Exercise 5

Write the removal, record-preservation, sanitization, economic-closure, and outcome portions of a retirement receipt. Include every runtime and control-plane artifact, copy, supplier, commitment, legal hold, archive test, disposal assurance, invoice, exception, countermetric, and approval.

## Answers to the Exercises

### Answer 1

Give every database, view, procedure, job, route, endpoint, channel, connector, file, credential, schedule, contract, consumer, human procedure, and recovery artifact a stable identity. Build a typed directed graph from configuration, code, queries, flows, gateway and broker telemetry, schedulers, transfers, object access, lineage, identity, billing, incidents, recovery exercises, interviews, and consumer confirmation; record coverage and confidence. State every purpose and consumer decision. Recover structural, semantic, behavioral, policy, service, support, and recovery contracts. Map every required obligation to an accepted successor, approved change, or authorized termination. Define authority by fact, population, consumer, and time; reconcile state and decisions at a durable boundary. Preserve privacy, security, retention, deletion, legal hold, audit, and evidence. Count transition and closure costs. Retire only after consumer, successor recovery, removal, archive, sanitization, invoice, and nonactivation gates pass.

### Answer 2

Publish deprecation date, expected sunset, successor, migration guide, behavioral and semantic differences, support, contact, exceptions, and machine-readable contract annotations. Provide successor contracts, fixtures, SDKs, schemas, credentials, test environments, capacity, errors, and operational support. Identify clients and consumers from gateway credentials, message subscriptions, offsets, lineage, republishers, caches, code, billing, partners, and owner confirmation. Observe a justified cycle covering rare versions and scheduled work. Use approved denial, sink routing, or credential renewal to expose hidden paths. Turn every residual use into owned migration, termination, or expiring exception work. Verify deployed execution rather than acknowledgment. At closure remove routes, DNS, gateways, topics, schemas, ACLs, credentials, SDK guidance, monitors, support, replay state, and identifiers or leave durable tombstones where reuse could reactivate clients.

### Answer 3

Record the final consistent snapshot, source log or sequence position, queued changes, producer retry windows, consumer offsets, in-flight files, manifests, acknowledgments, dead letters, schedules, and clocks. Define transaction boundaries, ordering, duplicates, deletes, key and schema changes, late data, poison records, gaps, overlaps, restart, failover, and resnapshot. Reconcile named populations by keys, values, semantics, sequences, aggregates, policy decisions, lineage, errors, acknowledgments, and consumer decisions. Attribute every divergence, correct through replayable governed mechanisms, and recheck. Preserve required messages, files, schemas, mappings, positions, and decisions in an archive with tested discovery, interpretation, access, integrity, retention, deletion, and restore. Remove publications, slots, connectors, accounts, keys, routes, directories, parsers, schedules, alerts, and source retention only after recovery no longer depends on them.

### Answer 4

Inventory every hub transformation, route, enrichment, sequence, retry, correlation, authorization, audit, schema, credential, operator procedure, deployment, and recovery path. Define source, bridge, and successor authority at each interval. Preserve a bounded safe state position and test state convergence, mappings, contracts, policies, identities, capacity, corrections, and external-effect compensation. Identify successor-only state and a point after which partitioned authority or roll-forward is safer than legacy restoration. Exercise recovery of data, messages, contracts, identity, policy, lineage, orchestration, consumers, keys, and evidence without the hub. In quarantine, deny normal production execution and page on invocation while retaining bounded inspection under access and expiry controls. Restore old infrastructure, scheduler, routes, identifiers, and credentials in isolation; tombstones, revoked trust, removed network paths, and denied publication must contain every attempt.

### Answer 5

List producers, consumers, stores, jobs, routes, endpoints, topics, queues, subscriptions, slots, files, directories, schemas, contracts, mappings, credentials, policies, catalogs, dashboards, alerts, runbooks, tests, deployments, infrastructure definitions, backups, replicas, caches, logs, supplier accounts, licenses, support, reservations, and commitments. Separate operational removal from preservation of required contracts, positions, lineage, policy decisions, reconciliations, incidents, approvals, and source records. Give archives owner, meaning, integrity, access, keys, retention, deletion, legal hold, cost, and tested retrieval. Inventory every copy and choose risk-based clear, purge, cryptographic erase, provider deletion, destruction, or other approved assurance with verification and disposition evidence. Confirm bills and allocations close. Record exceptions with expiry. Compare incidents, exposure, lead time, reliability, toil, spend, recovery, and user outcomes with baseline and countermetrics. Bind evidence, limitations, risk acceptance, nonactivation results, and final authority in the approved receipt.
