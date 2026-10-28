---
module_id: DARCH-093
program: Data Architecture Engineering
level: 2
module_number: 93
title: Transition Architectures
status: complete
last_verified: 2026-09-03
---

# Transition Architectures

## One-Page Review

### Governing question

How can an organization move from an observed current data architecture toward a target through bounded, operable intermediate states that deliver evidence and value while preserving semantics, policy, service, recovery, rollback, and final retirement?

### Essential definitions

- A **transition architecture** is a versioned, temporary but production-grade arrangement of people, ownership, data, interfaces, platforms, controls, operations, and evidence used to move between architecture baselines.
- A **transition increment** is a bounded change with an outcome, scope, authority, prerequisites, affected paths, acceptance evidence, stop conditions, rollback, successor, and retirement condition.
- A **migration unit** is the smallest product, domain slice, workload, consumer cohort, data partition, interface, region, tenant, or capability that can move and be governed coherently.
- A **migration seam** is a boundary at which behavior, reads, writes, events, queries, policy, or consumers can be redirected, translated, observed, and reversed with bounded effects.
- **Authority** identifies which system, product, owner, contract, policy, clock, or evidence source governs each fact and decision during coexistence.
- **Dual operation** means old and new paths both perform part of a capability for a bounded interval under explicit authority, reconciliation, cost, and closure rules.
- A **backfill** creates target state from historical source data under a declared snapshot, ordering, transformation, policy, lineage, and reconciliation model.
- **Change capture** propagates source changes after or alongside a baseline copy using identified ordering, position, transaction, schema, retry, and recovery semantics.
- A **shadow path** executes new behavior or reads against production-shaped inputs without governing the user-visible decision; its outputs are compared under privacy and safety controls.
- A **canary** exposes a bounded production population to a new path, compares it with an appropriate control or baseline, and governs expansion or rollback through declared evidence.
- **Reconciliation** determines whether authoritative and derived states agree under explicit keys, populations, time windows, tolerances, semantic equivalence, and correction rules.
- A **cutover** changes authority, traffic, writes, reads, consumers, or operation from one governed path to another at a recorded boundary.
- **Rollback** restores a previously safe authority and operating state within defined time, loss, policy, service, and reconciliation limits; a routing toggle alone is insufficient.
- A **transition debt** is a temporary adapter, duplicate path, exception, copy, credential, contract, control, or operating burden with owner, cost, risk, successor, and expiry.
- **Closure** proves old and temporary paths cannot write, serve, decide, enforce, charge, recover, or regain authority while required history and evidence remain controlled.

### Central model, mechanism, or theorem

Represent a transition as:

`X = (U, B, A, M, D, I, G, Q, E, C, R, L)`

where `U` is users, outcomes, decisions, and affected parties; `B` current, intermediate, and target baselines; `A` authority and ownership; `M` migration units, seams, ordering, and dependencies; `D` data, semantics, identity, history, and correction; `I` interfaces, consumers, compatibility, and routing; `G` governance, security, privacy, and policy continuity; `Q` quality, service, capacity, resilience, and recovery; `E` evidence, observation, experiments, and reconciliation; `C` cost, staffing, commitments, and organizational change; `R` risk, canaries, stop conditions, rollback, and replanning; and `L` lifecycle, transition debt, retirement, and closure. A smaller increment is safer only when its authority, dependencies, blast radius, evidence, rollback, and closure are bounded.

### Critical invariants

- Transition, version, increment, baseline, migration unit, seam, authority, contract, data position, evidence, exception, rollback, cutover, debt, and retirement have distinct stable identities.
- Current, intermediate, target, deployed, degraded, recovered, rolled-back, and closed states remain distinguishable.
- At every instant and for every fact or decision, authoritative write, read, semantic model, policy, clock, and correction owner are explicit.
- Historical copies and change streams share a defined consistency boundary, ordering model, deduplication identity, and reconciliation method.
- Old and new schemas, semantics, defaults, nulls, code sets, time, identity, and behavior remain compatible or are transformed with explicit loss and consumer evidence.
- Policy, classification, purpose, access, retention, lineage, quality, and deletion obligations survive copying, shadowing, routing, replay, rollback, and recovery.
- Every increment has bounded blast radius, capacity, evidence, expansion, pause, stop, correction, rollback, and retirement rules.
- Dual operation has a declared authority, cost, divergence response, maximum duration, and exit; it is not a steady-state substitute for decision.
- Rollback includes state, contracts, policies, credentials, reference data, capacity, consumers, and reconciliation, not merely code or routing.
- A transition can change or stop when evidence disproves target assumptions; schedule pressure cannot convert failed gates into acceptance.
- Temporary artifacts and exceptions are inventoried as transition debt and cannot outlive their successor or expiry silently.
- Closure prevents stale producers, readers, adapters, copies, slots, topics, routes, caches, credentials, contracts, or restored configurations from reviving retired authority.

### Common failures

Common failures include treating transition architecture as a project schedule; moving the largest shared database first; copying data before defining authority and semantics; using dual writes without atomicity or reconciliation; conflating change capture with domain events; starting change capture after an inconsistent snapshot; comparing row counts without population and time; shadowing sensitive data without lawful purpose; canarying an unrepresentative cohort; using lag as proof of correctness; cutting over reads before backfill convergence; cutting over writes without consumer readiness; declaring rollback while new-only writes cannot return; running old and new paths indefinitely; funding migration but not coexistence; measuring moved tables instead of decisions and outcomes; deleting the source before recovery validation; and retiring an interface while caches, credentials, quarantine, or restore automation remain.

### Compact example

Ten invented transition increments are checked against six mandatory gates. Four are admissible; one each lacks an outcome, owner, bounded coexistence window, reconciliation, tested rollback, or retirement condition. The program also counts eight transition patterns, seven affected products, four authority states, ten transition receipts, and ten decisions. It verifies declared structure and counts only—not migration correctness, data equivalence, policy continuity, rollback safety, cutover readiness, cost, or value.

### Connections

[DARCH-003](003-current-state-data-landscape.md), [DARCH-008](008-data-risk-and-criticality.md), [DARCH-019](019-model-versioning.md), [DARCH-027](027-producer-and-consumer-contracts.md), [DARCH-038](038-federation-and-virtualization.md), [DARCH-067](067-schema-registries.md), [DARCH-079](079-audit-and-provenance-architecture.md), [DARCH-089](089-interoperability-without-a-universal-model.md), [DARCH-091](091-assessing-data-architecture-maturity.md), and [DARCH-092](092-target-state-architecture.md) establish baselines, versioning, contracts, evidence, and target intent. [DARCH-094](../ROADMAP.md) next applies transition reasoning to warehouse and lake modernization.

## Governing Question

A current architecture and a target architecture do not define the route between them. The path may temporarily contain two schemas, three stores, a replicated change stream, a translation service, old and new consumers, split policy enforcement, reconciliation jobs, additional credentials, and double operating cost. Each intermediate arrangement is a system with its own failure modes. Calling it temporary does not make it safe, cheap, or self-removing.

The governing question is how to design each intermediate state as deliberately as the target. The transition must preserve a single understandable authority for every decision, expose divergence, constrain blast radius, produce evidence, permit safe stopping, and retire every temporary mechanism. Incremental change is not automatically low risk: a tiny change at an unbounded shared interface can be catastrophic, while a large isolated migration can be controllable. The architecture—not the amount of work—determines the risk boundary.

## Why This Matters

NASA's [Product Integration](https://www.nasa.gov/reference/5-2-product-integration/) guidance treats integration as engineering subsystem interactions and environments so elements function as a whole. It calls for early integration and closeout planning, including de-integration or disposal. Transition architecture likewise must plan coexistence, system effects, and removal before implementation.

NASA's [Product Transition](https://www.nasa.gov/reference/5-5-product-transition/) guidance covers preparation, readiness evaluation, documentation, destination readiness, delivery, and captured work products for verified and validated products. Data transition needs the same distinction between building a new path and making users, operators, environments, and evidence ready to accept it.

NASA's [Configuration Management](https://www.nasa.gov/reference/6-5-configuration-management/) guidance emphasizes known baselines, version distinction, product-information consistency, beneficial change, and avoidance of adverse consequences. A migration must identify exact source, target, contract, mapping, policy, configuration, and recovery versions rather than rely on labels such as old and new.

Martin Fowler's [Strangler Fig](https://martinfowler.com/bliki/StranglerFigApplication.html) describes gradual legacy modernization through seams, bounded replacement, earlier value, learning, transitional architecture, and organizational change. It also warns that serious replacement remains difficult. The pattern is a strategy, not proof that a particular seam or increment is safe.

Danilo Sato's [Parallel Change](https://martinfowler.com/bliki/ParallelChange.html) describes expanding an interface, migrating consumers, and then contracting away the old form. It highlights incremental compatibility and the danger of never completing contraction. Data schemas and product contracts require the same consumer evidence and explicit closure.

Google's SRE Workbook chapter [Canarying Releases](https://sre.google/workbook/canarying-releases/) defines a canary as a partial, time-limited production deployment evaluated against the rest of the service and discusses reproducible, automated, tested, small releases. A data canary needs extra attention to persistent state, delayed consumers, privacy, correction, and irreversible decisions.

Google's SRE book chapter [Data Integrity](https://sre.google/sre-book/data-integrity/) covers backups, restores, validation, replication, corruption, and disaster planning. Transition mechanisms can amplify data loss or silent corruption, so backup existence cannot substitute for restored-state and application-level validation.

PostgreSQL's [Logical Replication](https://www.postgresql.org/docs/current/logical-replication.html) documentation describes publish-subscribe change propagation, initial snapshots, transactional ordering within a subscription, security, monitoring, restrictions, and possible conflicts when other writes occur. It supplies implementation context for one migration mechanism, not portable guarantees across systems.

Debezium's [Architecture](https://debezium.io/documentation/reference/stable/architecture.html) documents change-data-capture connectors, logs, source offsets, records, schemas, Kafka Connect, and alternative deployment forms. Capturing database changes can support transition, but mutation records are not automatically domain events and connector positions do not prove semantic convergence.

The [OpenAPI Specification](https://spec.openapis.org/oas/latest.html) gives a language-agnostic description for HTTP APIs, operations, parameters, responses, schemas, security schemes, and versions. Old and new data access interfaces can be described and tested explicitly, while runtime behavior and consumer decisions remain outside the document alone.

The Bitol [Open Data Contract Standard](https://bitol-io.github.io/open-data-contract-standard/latest/) includes schema, quality, service, roles, support, and infrastructure sections. It can express transition-era product obligations and compatibility expectations. Contract publication does not demonstrate producer, pipeline, or consumer conformance.

OpenLineage's [object model](https://openlineage.io/docs/spec/object-model/) represents datasets, jobs, runs, events, namespaces, names, and facets. Transition receipts can bind backfills, replications, comparisons, cutovers, and corrections to exact inputs and outputs if identities and instrumentation remain consistent across both architectures.

The Open Policy Agent [policy language documentation](https://www.openpolicyagent.org/docs/policy-language) describes policy decisions over structured inputs. Versioned policy bundles and decision evidence can support equivalent old and new enforcement, but only when inputs, decision points, defaults, exceptions, and failure behavior are aligned.

The OpenTelemetry [specification](https://opentelemetry.io/docs/specs/otel/) standardizes telemetry concepts and signals across implementations. Shared trace and resource identities can connect old and new paths, yet sampling, delayed data, batch jobs, and persistent outcomes require transition-specific evidence beyond request traces.

NIST [SP 800-160 Volume 1 Revision 1](https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final) applies systems-security engineering across the system lifecycle. Transition expands attack surface through extra interfaces, identities, credentials, copies, operators, and suppliers, so security and privacy must cover temporary paths from introduction through removal.

The FinOps Foundation's [FinOps Framework](https://www.finops.org/framework/) connects engineering, finance, product, leadership, procurement, security, and other roles to usage, cost, value, optimization, and governance. Migration economics must include coexistence, network transfer, duplicate storage and compute, commitments, support, incident risk, and exit—not only target run cost.

Together these sources support planned integration and product transition, controlled baselines, gradual displacement, parallel compatibility, canaries, data integrity, replication, change capture, explicit interfaces and contracts, lineage, policy, telemetry, lifecycle security, and economics. They do not choose a migration unit, establish equivalence, make dual writes safe, validate rollback, guarantee consumer readiness, or prove value. Those conclusions require local semantics, production-shaped evidence, reconciliation, cutover drills, affected stakeholders, and operational results.

## Prerequisites and Retrieval

You should understand current- and target-state architecture, domains, data products, schemas, semantics, APIs, events, batch and streaming, transactions, consistency, change capture, lineage, policy, privacy, security, quality, observability, reliability, backups, recovery, distributed systems, economics, migration, and retirement.

Retrieve architecture baseline, transition state, transition increment, migration unit, seam, authority, expand and contract, strangler fig, branch by abstraction, facade, adapter, backfill, snapshot, high-water mark, change capture, replication position, shadow path, canary, dual read, dual write, reconciliation, cutover, rollback, roll forward, compatibility, transition debt, successor, expiry, and closure.

As a retrieval test, inspect a move from a legacy order database to domain-owned products on a new platform. Ask which facts and decisions the source owns; which product and consumer moves first; where reads and writes can be intercepted; how the baseline snapshot aligns with subsequent changes; how schema, money, time, identity, and correction map; which policies apply to temporary copies; how divergence is reconciled; which cohort can be canaried; what stops expansion; whether new-only writes can roll back; how recovery behaves during cutover; what double running costs; and which proof allows every old route and restore path to close. “Replicate, switch traffic, decommission” is not enough.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish project schedules, target states, transition architectures, deployment states, and closure evidence;
2. select migration units and seams according to authority, semantics, coupling, blast radius, value, and reversibility;
3. design backfill and change capture with explicit snapshot, ordering, identity, schema, policy, replay, and recovery semantics;
4. evaluate strangler, facade, adapter, expand-contract, shadow, canary, dual-read, dual-write, replication, and cutover patterns;
5. define authoritative reads, writes, policies, contracts, clocks, corrections, and evidence throughout coexistence;
6. reconcile old and new states using bounded populations, keys, windows, equivalence, tolerances, exceptions, and correction;
7. specify production-shaped validation, expansion, pause, stop, roll-forward, rollback, recovery, and replanning conditions;
8. operate transition debt, capacity, support, security, privacy, cost, incidents, and organizational change;
9. create transition receipts that trace increments to baselines, outcomes, evidence, decisions, risks, and retirement; and
10. close old and temporary paths without losing required history or allowing recovery to revive retired authority.

## Core Exposition

**Start from two governed baselines.** Verify the observed current architecture and the approved target version. Record scope, owners, outcomes, semantics, interfaces, policies, deployments, service, costs, recovery, assumptions, and open decisions for each. A transition between vague endpoints cannot be verified.

**Define the transition outcome.** State whose decision or service improves, what risk declines, what capability becomes available, what old burden can close, how it is measured, and by when. “Migrate table X” is an activity unless its outcome and retirement consequence are explicit.

**Treat each intermediate state as production.** Give it architecture views, owners, contracts, threat model, privacy analysis, service objectives, capacity, runbooks, costs, incident response, recovery, and closure. Short duration can justify proportionate rigor, not missing responsibility.

**Choose a migration unit.** Evaluate product semantics, consumers, write authority, read paths, transaction boundaries, shared keys, historical volume, policy, service, failure consequence, deployment coupling, and team ownership. Smaller units reduce some blast radius while multiplying boundaries and coordination.

**Find a seam.** Candidate seams include an API gateway, query router, event subscription, database view, change log, file landing boundary, product contract, domain facade, namespace, tenant, region, consumer cohort, or decision workflow. Test whether the seam truly controls traffic and state, including bypasses and recovery paths.

**Map dependencies before ordering.** Include data, schema, semantics, identity, reference data, policy, network, compute, catalog, lineage, consumers, operators, contracts, finance, procurement, skills, and recovery. Distinguish hard prerequisites from assumptions and conveniences; cycles require joint migration or a temporary bridge.

**Define authority as a time-indexed function.** For every data item and decision, state which version owns creation, change, read, correction, policy, and evidence before, during, after, and after rollback. Do not use “both are sources of truth.” If authority is split, partition it by an explicit key, population, operation, or interval.

**Preserve semantic authority.** Copying data does not transfer the right to redefine it. Bind source and target models, mappings, units, codes, nulls, identity, valid time, transaction time, provenance, loss, and correction. Name which domain approves interpretation and which consumers validate fitness.

**Design the historical boundary.** Choose a source snapshot or consistent cut, capture its position, and define how changes before, at, and after that boundary are included exactly as intended. A table-by-table timestamp is not a consistent boundary for cross-table invariants.

**Design backfill as a replayable product.** Record input identities, snapshot, extraction, schema, mapping, reference versions, policy, partitioning, ordering, deduplication, validation, output identity, lineage, errors, retries, cost, and retention. Re-running must not create silent duplicates or different meaning.

**Design change capture explicitly.** Define mutation source, log retention, offsets, transaction boundaries, key and before-image availability, schema changes, ordering scope, duplicates, deletes, snapshots, retries, backpressure, poison events, resnapshot, failover, and monitoring. A connector being alive proves little.

**Distinguish change records from domain events.** A row update reports storage mutation; a domain event reports an owned occurrence. Do not infer business meaning, intent, correction, or authorization solely from a database operation. Translate only through governed semantics and preserve source evidence.

**Align backfill and change capture.** Prevent gaps and overlaps by binding a durable position to the snapshot and defining buffering, application order, duplicate handling, and catch-up. Test connector restart, log truncation, schema change, publisher failover, target outage, and resnapshot.

**Use expand-contract for interfaces.** Add a new compatible schema, operation, field, or product without removing the old one; migrate and observe every consumer; then remove the old form only after usage, recovery, and restore paths are closed. Set an expiry at expansion time.

**Use adapters to protect bounded models.** Translate old contracts at a controlled boundary rather than importing legacy semantics into the target core. Give each adapter a directional mapping, loss ledger, tests, owner, telemetry, service, cost, exception policy, and retirement condition.

**Use a facade to control routing.** A facade can direct operations between old and new implementations while preserving a consumer contract. It becomes a critical availability, security, semantic, and observability boundary. Inventory bypasses; otherwise traffic reports understate remaining dependence.

**Use gradual displacement by outcome slice.** Introduce new capabilities at seams, move bounded behavior, learn, and retire replaced paths. Prefer slices that can deliver outcome evidence and reduce old-system scope. Avoid rebuilding unwanted behavior merely to match historical accidents.

**Use shadow execution carefully.** Send production-shaped inputs to the new path without letting it govern the visible decision. Prevent side effects, duplicate notifications, unauthorized data use, retention breaches, and hidden cost. Compare semantics and downstream decisions, not only bytes or latency.

**Design a canary population.** Choose a representative but bounded cohort by tenant, region, product, data class, workload, or consumer. Include expected diversity and exclude high-consequence populations only with a later assurance plan. Define control, exposure, duration, sample sufficiency, delayed effects, and rollback.

**Separate expansion gates.** Contract validity, data equivalence, policy decisions, quality, service, cost, operator load, consumer outcome, and incident risk are different gates. A fast canary cannot compensate for wrong semantics or unlawful access.

**Beware delayed data effects.** Batch close, month-end reporting, late corrections, retention, model training, downstream caches, partner extracts, and recovery may reveal harm long after a request-level canary looks healthy. Hold or revisit expansion until relevant outcome windows close.

**Prefer one authoritative writer.** Route writes to one system and propagate changes when possible. If dual write is unavoidable, define atomicity boundary, order, idempotency, partial failure, retry, compensation, conflict, visibility, and recovery. Application-level best effort is not atomic.

**Use dual read for evidence, not ambiguity.** One result governs the decision; the other is shadowed or compared. Define query equivalence, time alignment, nondeterminism, ordering, precision, policy, caching, and side-effect behavior. Never choose whichever answer is convenient.

**Define reconciliation before migration.** State population, keys, expected cardinality, snapshot or interval, semantic equivalence, tolerances, aggregation, ordering, missingness, duplicates, late data, exclusions, and correction. Row count is one weak signal.

**Reconcile invariants and decisions.** Test balances, conservation, referential rules, uniqueness, state transitions, temporal ordering, access outcomes, retention, deletion, downstream reports, alerts, model features, and user decisions. A data copy can match fields and still change behavior.

**Classify divergence.** Distinguish expected lag, transformation difference, source correction, target defect, mapping ambiguity, missing event, duplicate, out-of-order change, unauthorized mutation, policy mismatch, clock issue, and observation error. Each needs an owner and bounded response.

**Make correction idempotent and attributable.** Record who authorized correction, input and output identities, mapping and policy versions, affected consumers, replay position, evidence, and outcome. Avoid manual patches that create a third unexplained truth.

**Design cutover as a state transition.** Define entrance conditions, freeze or coordination window, final synchronization, authority handoff, routing, consumer confirmation, monitoring, decision log, rollback boundary, communication, and exit evidence. Record exact clocks and positions rather than “around midnight.”

**Separate read and write cutovers.** Writers, readers, batch jobs, reports, caches, APIs, partners, and recovery systems may move at different times. Model which combinations are safe. Old readers can misinterpret new writes even when APIs remain reachable.

**Freeze only what is necessary.** A write freeze simplifies final convergence but creates service cost and can hide queued external changes. Define affected operations, maximum duration, user behavior, exception authority, buffered input, abort rule, and recovery.

**Define roll forward.** Some failures are safer to correct on the new path than to restore the old one. State which conditions permit repair, isolation, replay, or delayed consumer migration, and compare risk with rollback. “Always roll back” is as weak as “never roll back.”

**Design rollback before exposure.** Preserve old capacity, compatible inputs, missed-change capture, contracts, policies, identities, credentials, reference data, schema, operator access, and consumer routes. Define permitted data loss, reconciliation, recovery objective, decision authority, and latest safe point.

**Test rollback with new-only state.** Create records, updates, corrections, identities, access decisions, and side effects available only in the new path, then demonstrate how they return, remain isolated, or are compensated. A routing reversal that loses them is not safe rollback.

**Distinguish rollback from recovery.** Rollback responds to a harmful change by returning authority or behavior. Recovery restores service and state after failure. During transition either may need old, new, or combined components. Exercise their interaction and prevent recovery from undoing a cutover.

**Maintain configuration integrity.** Version source and target schemas, mappings, connector positions, policies, routes, flags, jobs, secrets, infrastructure, runbooks, and receipts. Ensure deployed state matches the transition baseline and that rollback artifacts remain trustworthy until their expiry.

**Model security expansion.** Temporary replicas, topics, adapters, gateways, credentials, broad connector privileges, operators, logs, and vendor tools expand attack surface. Apply least privilege, segmentation, encryption, integrity, monitoring, incident response, expiration, and deletion to every transition asset.

**Model privacy across copies.** Establish lawful purpose, minimization, data-subject or equivalent obligations, jurisdiction, retention, masking, access, shadow-use limits, deletion propagation, and evidence. “Nonproduction output” does not make production data free to duplicate.

**Preserve policy continuity.** Compare authoritative policy inputs, bundle versions, decision semantics, enforcement points, failures, exceptions, logs, and appeals on both paths. During rollback, ensure a revoked permission or deletion request does not revert.

**Preserve lineage and audit continuity.** Bind source snapshot, change position, backfill run, mapping, target data, comparison, correction, cutover, and consumer result. Keep identities stable across renames while preserving distinct old and new artifacts.

**Observe the migration control plane.** Monitor backfill progress, change lag, log retention, retries, dead letters, divergence, reconciliation age, consumer adoption, old-path traffic, policy mismatch, incidents, costs, and expiry. A green target service can coexist with a failing migration.

**Measure outcomes and countermetrics.** Track decision delay, correctness, risk, consumer effort, reconciliation toil, incident impact, and retired burden alongside migrated objects. Countermetrics include duplicate storage, network cost, domain toil, exception growth, cognitive load, and legacy scope that fails to shrink.

**Budget coexistence.** Price old and new run costs, replication, storage, network, adapters, observability, security, support, incident response, recovery, licenses, commitments, training, and retirement. A delayed cutover can erase the target business case.

**Treat operator readiness as architecture.** Prepare access, training, runbooks, ownership, support hours, capacity, dashboards, alerts, decision authority, incident coordination, and recovery exercises. Software readiness without people and operating conditions is incomplete.

**Prepare consumers.** Inventory direct and indirect readers, reports, extracts, caches, notebooks, models, APIs, partners, scheduled jobs, and recovery tools. Communicate contracts and dates, supply test environments or fixtures, observe real adoption, and address consumers that cannot change safely.

**Govern exceptions.** Record scope, owner, rationale, risk, compensating control, cost, dependency, successor, expiry, and rollback effect. An exception cannot silently turn a temporary path into the architecture.

**Maintain a transition-debt ledger.** Include adapters, duplicate schemas, flags, replication slots, topics, copies, manual reconciliations, expanded privileges, compatibility promises, extra capacity, vendor commitments, and temporary teams. Review cost and risk until each item closes.

**Set stop conditions.** Pause or abort on semantic divergence, policy violation, data loss, unsupported consumer behavior, recovery failure, unsafe operator load, cost threshold, or invalidated target assumption. Delivery pressure does not lower an invariant.

**Replan from evidence.** A transition may show that the target contract, platform, domain boundary, workload placement, or governance model is wrong. Preserve the observation, revisit alternatives, version the target, and redirect safely rather than forcing conformance to a disproved design.

**Keep increments independently coherent.** Each completed increment should leave a supportable state and useful outcome even if later work stops. Avoid sequences whose value and safety appear only after every migration unit completes.

**Use a dependency-aware portfolio.** Multiple product migrations can contend for source logs, networks, platform capacity, domain experts, policy reviews, support, and cutover windows. Model common-mode failure and total cognitive load, not only local plans.

**Record transition receipts.** Bind baseline versions, increment, authority, units, contracts, positions, evidence, divergences, decisions, cutover, rollback, costs, incidents, target changes, debt, and closure. Receipts allow later reconstruction without treating logs as self-explanatory.

**Define retirement entrance criteria.** Require zero or authorized residual traffic, migrated consumers, reconciled state, preserved history, completed retention and deletion, closed quarantine, tested target recovery, resolved exceptions, and approved authority handoff. Low observed traffic is not zero dependence.

**Revoke the old path deliberately.** Stop writers and readers, remove routes, credentials, firewall rules, jobs, slots, topics, adapters, caches, shares, catalog entries, policies, dashboards, alerts, runbooks, support, billing, and provider commitments according to controlled evidence.

**Test nonactivation.** Restore backups, old configurations, disaster-recovery environments, cached clients, queued events, and automation in isolation. Verify retired systems cannot publish, consume, authorize, bill, or become authoritative. Tombstones and deny rules may need to outlive deletion.

**Preserve required history.** Archive controlled contracts, mappings, positions, receipts, lineage, decisions, incidents, reconciliations, and evidence needed for audit, replay, explanation, or legal obligations. Historical evidence must not remain a live operational path.

## Definitions and Notation

Let `X = (U, B, A, M, D, I, G, Q, E, C, R, L)` be the transition architecture defined in the review. Let `b_0` be the governed current baseline, `b_t` the approved target, and `b_1 ... b_n` intermediate baselines. Each edge is an approved transition increment, not merely elapsed time.

Represent an increment as:

`J = (id, outcome, source, destination, unit, owner, prerequisites, changes, evidence, stop, rollback, successor, retire)`

An increment is admissible only when every mandatory field is actionable and its source and destination are coherent operating states.

Define authority `Auth(f, op, p, t) -> (system, owner, contract, policy, clock)` for fact or decision `f`, operation `op`, population `p`, and interval `t`. An overlap is safe only when partition, arbitration, and correction are explicit; an unplanned gap or collision is a transition defect.

Represent a historical boundary as `(snapshot_id, source_position, contract_version, policy_version, reference_versions, clock)`. Change application must define whether records before, at, and after that position are included, buffered, deduplicated, ordered, or rejected.

Define reconciliation result:

`Rec(P, K, W, Eq, Tau) = (matched, missing_source, missing_target, divergent, excluded, unknown)`

where `P` is population, `K` keys, `W` time or position window, `Eq` semantic equivalence, and `Tau` tolerances. Counts without these parameters are not a reconciliation claim.

Define cutover `Cut(Auth_before, Auth_after, position, time, evidence, decision)` and rollback `Back(C_safe, delta, reconcile, t, loss, policy, service)`. Rollback is supported only when new-state delta and irreversible effects have defined treatment.

Let blast radius `BR(J)` include users, decisions, products, data, regions, tenants, consumers, privileges, dependencies, costs, and recovery paths affected by increment `J`. Small code size does not imply small `BR`.

Represent transition debt `TD = (artifact, purpose, owner, cost, risk, successor, expiry, evidence, closure)`. The debt ledger is complete only relative to observed paths and inventories; unknown bypasses remain risk.

Define `Closed(old)` to require no live or recoverable writer, reader, job, route, adapter, slot, topic, copy, cache, credential, policy, contract, exception, support path, bill, or automated authority can reactivate `old`, while required history remains controlled.

## Mechanisms, Invariants, or Proof Structure

Use the following assurance gates.

**Baseline gate.** Verify current and target versions, outcomes, ownership, semantics, interfaces, policies, deployments, service, costs, recovery, assumptions, and open decisions.

**Increment gate.** Define outcome, migration unit, source, destination, owner, prerequisites, affected paths, acceptance, expansion, pause, stop, rollback, successor, and retirement.

**Authority gate.** Allocate writes, reads, semantics, policy, clocks, correction, evidence, cutover, rollback, and incident decisions for every population and interval.

**Historical-boundary gate.** Bind snapshot, change position, schema, mappings, reference data, policy, clocks, ordering, gaps, overlaps, replay, and recovery.

**Contract gate.** Test producer, consumer, schema, semantics, behavior, compatibility, errors, service, policy, evidence, change, and closure on both paths.

**Reconciliation gate.** Define population, keys, interval, equivalence, tolerance, exclusions, divergence classes, owners, correction, replay, and decision consequences.

**Exposure gate.** Bound shadow or canary cohort, purpose, side effects, privacy, control, duration, sample, delayed effects, expansion, pause, and stop.

**Security and privacy gate.** Govern temporary copies, credentials, routes, privileges, vendors, logs, jurisdictions, purposes, retention, deletion, response, and expiry.

**Service gate.** Verify capacity, freshness, latency, availability, dependency behavior, backpressure, support, incidents, degraded mode, recovery, and consumer outcomes.

**Rollback gate.** Preserve old capacity, missed changes, contracts, policies, identities, credentials, reference data, routes, operators, state reconciliation, and latest safe boundary.

**Recovery gate.** Exercise source, bridge, target, control plane, policy, lineage, state, consumers, and retired-path nonactivation in dependency order.

**Economics gate.** Fund backfill, transfer, duplicate storage and compute, adapters, observation, security, support, incidents, recovery, commitments, training, and retirement.

**Readiness gate.** Prepare producers, consumers, operators, domains, platforms, security, privacy, finance, partners, support, sites, documentation, and decision authority.

**Evidence gate.** Preserve configurations, positions, traces, lineage, policy decisions, comparisons, divergences, corrections, costs, incidents, outcomes, and limitations.

**Portfolio gate.** Control shared logs, networks, platform capacity, expertise, policy review, support, cutover windows, common-mode risk, and total transition debt.

**Replanning gate.** Stop when invariants fail, distinguish implementation defect from target defect, preserve evidence, revisit alternatives, and version changed intent.

**Retirement gate.** Prove consumer migration, reconciled authority, preserved history, target recovery, closed exceptions, removed paths and commitments, and recovery nonactivation.

**Receipt gate.** Bind baselines, increment, authority, contracts, positions, evidence, divergence, decisions, exposure, rollback, cutover, cost, debt, target changes, and closure.

### Executable evidence: transition-increment admission

The following program classifies ten invented transition increments against six mandatory gates.

<!-- bijux-verify: {"id":"transition-increment-admission","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"increments=10\nadmissible=4\nmissing_outcome=1\nmissing_owner=1\nunbounded_coexistence=1\nmissing_reconciliation=1\nuntested_rollback=1\nmissing_retirement=1\ntransition_patterns=8\naffected_products=7\nauthority_states=4\ntransition_receipts=10\ndecision_events=10\n","stderr":""}} -->
```python
increments = [
    {"pattern": "strangler", "products": {"orders"}, "authority": "source", "outcome": True, "owner": True, "bounded": True, "reconcile": True, "rollback": True, "retire": True},
    {"pattern": "expand-contract", "products": {"customer", "orders"}, "authority": "split", "outcome": True, "owner": True, "bounded": True, "reconcile": True, "rollback": True, "retire": True},
    {"pattern": "replicate-cutover", "products": {"ledger"}, "authority": "target", "outcome": True, "owner": True, "bounded": True, "reconcile": True, "rollback": True, "retire": True},
    {"pattern": "shadow", "products": {"risk"}, "authority": "source", "outcome": True, "owner": True, "bounded": True, "reconcile": True, "rollback": True, "retire": True},
    {"pattern": "backfill", "products": {"catalog"}, "authority": "source", "outcome": False, "owner": True, "bounded": True, "reconcile": True, "rollback": True, "retire": True},
    {"pattern": "dual-read", "products": {"inventory"}, "authority": "compare", "outcome": True, "owner": False, "bounded": True, "reconcile": True, "rollback": True, "retire": True},
    {"pattern": "facade", "products": {"customer"}, "authority": "split", "outcome": True, "owner": True, "bounded": False, "reconcile": True, "rollback": True, "retire": True},
    {"pattern": "change-capture", "products": {"orders", "inventory"}, "authority": "source", "outcome": True, "owner": True, "bounded": True, "reconcile": False, "rollback": True, "retire": True},
    {"pattern": "expand-contract", "products": {"partner"}, "authority": "target", "outcome": True, "owner": True, "bounded": True, "reconcile": True, "rollback": False, "retire": True},
    {"pattern": "replicate-cutover", "products": {"ledger", "risk"}, "authority": "target", "outcome": True, "owner": True, "bounded": True, "reconcile": True, "rollback": True, "retire": False},
]

def evaluate(increment):
    if not increment["outcome"]:
        return "missing_outcome"
    if not increment["owner"]:
        return "missing_owner"
    if not increment["bounded"]:
        return "unbounded_coexistence"
    if not increment["reconcile"]:
        return "missing_reconciliation"
    if not increment["rollback"]:
        return "untested_rollback"
    if not increment["retire"]:
        return "missing_retirement"
    return "admissible"

results = [evaluate(increment) for increment in increments]
print(f"increments={len(increments)}")
for outcome in ["admissible", "missing_outcome", "missing_owner", "unbounded_coexistence", "missing_reconciliation", "untested_rollback", "missing_retirement"]:
    print(f"{outcome}={results.count(outcome)}")
print(f"transition_patterns={len({increment['pattern'] for increment in increments})}")
print(f"affected_products={len(set().union(*(increment['products'] for increment in increments)))}")
print(f"authority_states={len({increment['authority'] for increment in increments})}")
print(f"transition_receipts={len(increments)}")
print(f"decision_events={len(results)}")
```

The output reports ten increments, four admissible and one of each declared failure, eight transition patterns, seven affected products, four authority states, ten receipts, and ten decisions.

The evidence is deliberately narrow. Invented Booleans, labels, and sets establish deterministic gate order and counts only. They do not establish that an outcome matters, an owner has authority, coexistence is truly bounded, reconciliation is semantically valid, rollback works, retirement is complete, or any migration is safe, economical, or beneficial. Production assurance requires governed baselines, contracts, mappings, positions, representative state, policy tests, reconciliations, failure injection, consumer evidence, cutover and rollback exercises, recovery tests, costs, incidents, and outcomes.

## Alternatives and Trade-Offs

**One-time cutover.** Coexistence cost and split authority are minimized. Blast radius, downtime, unresolved behavior, rollback complexity, and late learning increase.

**Incremental displacement.** Value and evidence arrive in bounded slices. Adapters, routing, duplicated operation, dependency management, and total duration increase.

**Migration by technical component.** Infrastructure ownership and deployment can be simple. User outcomes, domain semantics, and end-to-end retirement may remain fragmented.

**Migration by product or capability.** Authority and consumer value stay coherent. Shared transactions, reference data, and platform dependencies may make slices difficult.

**Copy then cut over.** The target is populated before authority changes. Change lag, historical boundary, final convergence, and source freeze require control.

**Continuous change capture.** Downtime can shrink and comparison can continue. Logs, offsets, ordering, schema evolution, backpressure, conflicts, and recovery add complexity.

**Application dual write.** Both states update with low apparent lag. Partial failure, ordering, retry, atomicity, compensation, and divergence can corrupt authority.

**One writer plus propagation.** Authority and correction are clearer. Replication lag and source dependency may constrain target testing and cutover.

**Dual read comparison.** Semantic and query divergence become visible. Cost, nondeterminism, cache, time alignment, privacy, and decision authority need controls.

**Shadow path.** Production-shaped evidence is gathered without visible decisions. Side effects, sensitive duplication, incomplete cohorts, and hidden cost remain risks.

**Canary cohort.** Production exposure and rollback are bounded. Persistent data, delayed downstream effects, and unrepresentative selection can outlive the cohort.

**Blue-green data environments.** Deployment isolation and routing are clear. Stateful synchronization, cost, write authority, external consumers, and rollback dominate.

**Expand-contract.** Consumers move independently under compatible interfaces. Duplicate schema, long-tail clients, confusing defaults, and incomplete contraction accumulate.

**Compatibility adapter.** Legacy consumers are isolated from target changes. Translation loss, latency, criticality, ownership, and retirement burden grow.

**Write freeze at cutover.** Final synchronization and authority are simpler. Business interruption, queued input, exception pressure, and maximum duration matter.

**Online cutover.** Service interruption is reduced. Coordination, change ordering, partial states, and recovery are more complex.

**Rollback-first policy.** Harm can be contained quickly when state remains reversible. New-only state and irreversible external effects may make return worse.

**Roll-forward-first policy.** Target state and consumer progress are preserved. Diagnosis and repair under incident conditions can prolong harm.

**Retain old system for safety.** Recovery confidence and investigation options may improve briefly. Cost, attack surface, stale authority, and indefinite dependence grow.

**Destroy old path promptly.** Ambiguity and cost end quickly. Audit, recovery, correction, rollback, and missed-consumer needs may be lost.

## Failure Modes and Misconceptions

1. **“A transition architecture is a project plan.”** Dates do not define operating authority, interfaces, policy, or recovery.
2. **“Temporary systems need less architecture.”** Short-lived paths can carry production consequences.
3. **“Smaller increments are always safer.”** A small change at a shared boundary can have unbounded blast radius.
4. **“The easiest table should move first.”** A useful migration unit follows outcomes, authority, and dependencies.
5. **“The largest database should move first.”** Shared coupling may make it the worst learning boundary.
6. **“A gateway is automatically a seam.”** Bypasses, batch jobs, direct reads, and recovery paths may avoid it.
7. **“Both systems can be sources of truth.”** Authority must be partitioned or arbitrated explicitly.
8. **“Copying data transfers ownership.”** Semantic and decision authority do not follow bytes.
9. **“A timestamp defines a consistent snapshot.”** Transactions and cross-table invariants may straddle it.
10. **“Backfill is a one-time script.”** Replay, identity, ordering, policy, lineage, and correction matter.
11. **“Change capture cannot lose data.”** Retention, offsets, failover, schema, and poison records can create gaps.
12. **“A change record is a domain event.”** Storage mutation lacks guaranteed business meaning and intent.
13. **“Connector lag proves convergence.”** Applied changes can be wrong, duplicated, or semantically stale.
14. **“Initial copy plus streaming prevents overlap.”** A durable consistency boundary is required.
15. **“Expand means compatibility.”** Defaults, unknowns, closed readers, signatures, and behavior can break.
16. **“Deprecation notices migrate consumers.”** Actual traffic and decision evidence are required.
17. **“An adapter is harmless temporary code.”** It becomes a semantic and operational authority.
18. **“A facade sees every dependency.”** Direct paths and restored clients can remain.
19. **“Gradual displacement means rebuild everything.”** Unwanted legacy behavior should not be preserved blindly.
20. **“Shadow execution has no impact.”** Reads, compute, logs, privacy, and side effects can harm production.
21. **“Any small cohort is a canary.”** Representativeness, consequence, exposure, and control matter.
22. **“A successful request canary proves data safety.”** Delayed batches, corrections, models, and retention remain.
23. **“Fast performance compensates for semantic divergence.”** Mandatory gates are not tradeable.
24. **“Dual writes keep databases synchronized.”** Partial failure and ordering create divergence.
25. **“Retries make dual writes reliable.”** Non-idempotent effects and conflicting order can worsen state.
26. **“Dual reads improve availability automatically.”** Competing answers can make decisions ambiguous.
27. **“Row counts prove equality.”** Population, keys, time, semantics, and values can differ.
28. **“Checksums prove semantic equivalence.”** Representation may differ legitimately or match incorrectly.
29. **“Zero divergence proves correctness.”** Both paths can reproduce the same defect.
30. **“Every difference is a target bug.”** Lag, source correction, mapping, policy, and observation may explain it.
31. **“Manual repair is faster.”** Unattributed patches create a third truth and break replay.
32. **“Cutover is a DNS change.”** Authority, state, consumers, policy, and recovery must move.
33. **“Reads and writes can switch together safely.”** Versioned consumers and caches may require separation.
34. **“A write freeze has no data semantics.”** Buffered and rejected actions affect outcomes and time.
35. **“Rollback is always safest.”** New-only state and external effects may make return harmful.
36. **“Rollback is a routing toggle.”** State, contracts, policy, capacity, and reconciliation must return.
37. **“Recovery and rollback are the same.”** They respond to different conditions and can conflict.
38. **“Old configuration remains trustworthy.”** Secrets, policies, schemas, and dependencies drift.
39. **“Temporary copies need weaker security.”** More paths expand attack surface and privilege.
40. **“Shadow data is not a privacy concern.”** Production-derived data retains obligations.
41. **“Equivalent policy code means equivalent enforcement.”** Inputs, points, defaults, and exceptions differ.
42. **“Tracing both paths proves continuity.”** Sampling and identity gaps can hide lost work.
43. **“A green target means migration is healthy.”** Backfill, change capture, consumers, and debt can fail.
44. **“Moved-table count measures progress.”** Outcomes and retired legacy scope matter.
45. **“Target run cost is the migration cost.”** Coexistence, people, network, incidents, and exit dominate.
46. **“Operators can learn after cutover.”** Access, authority, procedures, and recovery must be ready.
47. **“All consumers are in the catalog.”** Extracts, caches, notebooks, models, and old clients hide.
48. **“Exceptions disappear at project end.”** They require owners, successors, expiry, and closure.
49. **“Low old-path traffic permits deletion.”** Rare recovery or regulatory dependencies can remain critical.
50. **“A powered-off source cannot return.”** Backups, automation, credentials, routes, and queued work can revive it.

## Worked Examples

### Example 1

An order API is placed behind a facade. New creation routes to the target while historical reads remain on the source. Authority is split by order creation boundary, the facade records which system owns each identity, and no consumer chooses between conflicting answers.

### Example 2

A customer backfill captures a database snapshot and its exact log position. Change capture buffers later mutations, applies them after each partition, deduplicates by transaction and key, and reconciles identities, consent, merges, splits, and valid time—not only rows.

### Example 3

A legacy status string expands into a versioned code object. Producers write both forms through one mapping, consumers migrate under telemetry, and the old field remains until traffic, replay, cached schemas, recovery images, and external clients show zero authorized dependence.

### Example 4

A fraud model shadows the target feature product. It cannot send decisions or notifications, and sensitive outputs have short retention. Comparisons cover features, missingness, time alignment, decisions, subgroup effects, cost, and delayed labels before a bounded canary receives authority.

### Example 5

Inventory dual writes succeed on the source and time out on the target. Blind retry changes ordering and duplicates a stock decrement. The design moves to one authoritative writer plus change propagation and records divergence correction through idempotent transaction identities.

### Example 6

A reporting migration matches row counts but changes the month-end cutoff from business-local time to UTC. Reconciliation of balances by valid interval and consumer report exposes the semantic error. Cutover stops until the mapping and historical replay are corrected.

### Example 7

A regional canary performs well for interactive queries. Month-end batch and disaster restoration have not occurred within its window. Expansion pauses for those delayed scenarios instead of treating ten days of request telemetry as complete evidence.

### Example 8

A target begins accepting a new-only identifier before rollback is tested. The exercise shows the old platform cannot represent it. The team either retains target authority for that partition during rollback or introduces a reversible mapping before broader exposure.

### Example 9

Five domain migrations independently schedule backfills and saturate the source log, network, platform, and policy-review team. A portfolio view sequences high-load windows, reserves recovery capacity, and limits total transition debt even though every local plan looked safe.

### Example 10

After cutover, an isolated disaster-recovery test restores an old route and replication slot. Persistent deny rules and authority tombstones prevent publication; the test reveals and removes an obsolete credential before source destruction and final closure approval.

## Cross-Program Connections

- [Data Engineering](../../19-data-engineering/ROADMAP.md) implements backfills, change capture, schema conversion, reconciliation, lineage, quality, replay, cutover, correction, and retirement.
- [Large-Scale Data Systems Engineering](../../21-large-scale-data-systems-engineering/ROADMAP.md) grounds transition design in logs, snapshots, ordering, consistency, streaming state, backpressure, scaling, replication, and recovery.
- [Database Engineering](../../18-database-engineering/ROADMAP.md) owns transaction boundaries, replication identity, schema evolution, dual access, constraints, backup, restore, upgrade, and cutover mechanics.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) supplies facades, compatibility, expand-contract interfaces, routing, canaries, errors, idempotency, client migration, and deprecation evidence.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) owns paved migration paths, environments, deployment, flags, policy, telemetry, capacity, support, rollback, recovery, and platform retirement.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) governs expanded trust boundaries, privileges, credentials, copies, vendors, incident response, rollback, recovery, and secure closure.
- [Network Engineering](../../24-network-engineering/ROADMAP.md) grounds replication, routing, proxies, segmentation, throughput, latency, egress, failure, and cutover in actual paths.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) provides reasoning for partial failure, ordering, duplication, consistency, clocks, idempotency, convergence, rollback, and replay.
- [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) connects seams, facades, adapters, gradual displacement, branch by abstraction, evolutionary design, and architectural fitness.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies integration, transition, configuration, readiness, verification, validation, technical risk, lifecycle, and disposal discipline.

## References

1. NASA, [Product Integration](https://www.nasa.gov/reference/5-2-product-integration/), subsystem interactions, environments, integration planning, de-integration, disposal, and whole-system behavior.
2. NASA, [Product Transition](https://www.nasa.gov/reference/5-5-product-transition/), readiness, documentation, receiving environments, users, delivery, and captured transition work products.
3. NASA, [Configuration Management](https://www.nasa.gov/reference/6-5-configuration-management/), baselines, version distinction, integrity, controlled change, and product-information consistency.
4. Martin Fowler, [Strangler Fig](https://martinfowler.com/bliki/StranglerFigApplication.html), seams, gradual legacy displacement, bounded delivery, learning, transitional architecture, and organizational change.
5. Danilo Sato, [Parallel Change](https://martinfowler.com/bliki/ParallelChange.html), expand-contract interface evolution, consumer migration, incremental compatibility, and contraction risk.
6. Google, [Canarying Releases](https://sre.google/workbook/canarying-releases/), partial time-bounded exposure, controls, evaluation, automation, rollout, and rollback.
7. Google, [Data Integrity](https://sre.google/sre-book/data-integrity/), backups, restores, replication, corruption, validation, and disaster planning.
8. PostgreSQL Global Development Group, [Logical Replication](https://www.postgresql.org/docs/current/logical-replication.html), publications, subscriptions, initial snapshots, changes, ordering, conflicts, monitoring, and security.
9. Debezium, [Architecture](https://debezium.io/documentation/reference/stable/architecture.html), log-based change capture, connectors, source offsets, records, schemas, and deployment forms.
10. OpenAPI Initiative, [OpenAPI Specification](https://spec.openapis.org/oas/latest.html), HTTP API operations, parameters, responses, schemas, security, extensions, and versions.
11. Bitol, [Open Data Contract Standard](https://bitol-io.github.io/open-data-contract-standard/latest/), schema, quality, service, roles, support, and infrastructure obligations.
12. OpenLineage, [Object Model](https://openlineage.io/docs/spec/object-model/), dataset, job, run, event, namespace, name, and facet identities.
13. Open Policy Agent, [Policy Language](https://www.openpolicyagent.org/docs/policy-language), structured policy decisions, inputs, rules, tests, and runtime context.
14. OpenTelemetry, [Specification](https://opentelemetry.io/docs/specs/otel/), signals, resources, context, semantic conventions, sampling, compatibility, and versioning.
15. NIST, [SP 800-160 Volume 1 Revision 1](https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final), systems-security engineering and trustworthy secure systems across the lifecycle.
16. FinOps Foundation, [FinOps Framework](https://www.finops.org/framework/), cross-functional ownership, usage, cost, value, optimization, governance, and technology decisions.

## Exercises

### Exercise 1

Design transition architecture from a legacy order database to domain-owned order products. Define baselines, outcomes, migration units, seams, dependencies, authority, contracts, historical boundary, backfill, change capture, reconciliation, exposure, cutover, rollback, recovery, and retirement.

### Exercise 2

Create an expand-contract migration for a schema that replaces local money fields and status strings with governed types. Include old and new consumers, mappings, defaults, compatibility, telemetry, errors, historical replay, policy, adoption evidence, contraction, and restore paths.

### Exercise 3

Specify a shadow and canary program for a new analytical product. Address cohort selection, control, side effects, privacy, quality, decision equivalence, delayed outcomes, service, cost, stop conditions, expansion, rollback, and evidence limitations.

### Exercise 4

Design reconciliation, cutover, and rollback for a database replication migration. Include snapshot position, transactions, keys, ordering, duplicates, deletes, schema, reference data, write freeze, new-only state, policy, consumer readiness, recovery, and correction.

### Exercise 5

Create a transition-debt and closure plan for an enterprise modernization portfolio. Cover adapters, schemas, flags, copies, slots, topics, routes, credentials, exceptions, support, capacity, costs, commitments, old consumers, quarantine, evidence, recovery, and nonactivation.

## Answers to the Exercises

### Answer 1

Version the observed current and approved target baselines and state the user outcomes and legacy burden to close. Partition migration by a coherent order product or consumer decision rather than arbitrary tables. Place a facade at a verified seam and inventory direct database, batch, partner, cache, and recovery bypasses. Define authority by operation, order population, and time. Bind source and target contracts, money, identity, status, valid time, correction, and policy mappings. Capture a consistent snapshot and log position, run replayable backfill, buffer and deduplicate changes, and reconcile state transitions, balances, lineage, policy, and downstream decisions. Shadow before a representative canary. Define separate read and write cutovers, capacity, stop conditions, new-only-state rollback, recovery, consumer confirmation, debt expiry, and old-path nonactivation.

### Answer 2

Expand the producer contract to carry old money amount and currency fields plus a new governed money object, and old status strings plus a versioned code. Preserve source values, define exact units, precision, rounding, code-set mappings, unknowns, nulls, valid intervals, and loss. Make one implementation authoritative and derive both forms rather than independently writing them. Test old and new readers, defaults, unknown fields, signatures, caches, policy, errors, historical events, and replay. Observe each consumer identity and decision, not only endpoint traffic. Provide fixtures, deadlines, support, and expiring exceptions. Contract only after live, cached, batch, partner, quarantine, rollback, and restored consumers no longer require old fields; then remove derivation, schema, documentation, policy, and recovery support.

### Answer 3

Run the target on production-shaped inputs with side effects disabled and one old-path result governing decisions. Establish lawful purpose, minimization, access, retention, and deletion for shadow data. Compare population, grain, features, missingness, time, quality, policy decisions, reports or model outputs, latency, load, cost, and consumer interpretation. Select a canary stratified by workload, data class, region, consumer, and edge cases while limiting consequence. Define an appropriate control, exposure window, sample sufficiency, delayed batch and correction windows, expansion gates, countermetrics, pause and stop conditions, rollback of persistent state, and decision authority. State that a successful bounded cohort does not prove portfolio-wide safety or causal value.

### Answer 4

Capture a transactionally meaningful snapshot and durable source position. Define how changes at the boundary are buffered, ordered, deduplicated, and applied; test inserts, updates, deletes, key changes, schema changes, connector restart, log retention, failover, target outage, and resnapshot. Reconcile a named population by keys, source position and time, semantic equivalence, exact and bounded tolerances, duplicates, missing records, invariants, policy, lineage, and consumer decisions. Before cutover verify lag, divergence closure, consumer and operator readiness, target recovery, capacity, and old rollback capacity. Bound any write freeze and queued input. Test rollback with target-only records and side effects. Record authority handoff, final position, clocks, decisions, corrections, and recovery behavior.

### Answer 5

Inventory every facade, adapter, mapping, duplicate schema, flag, snapshot, replica, topic, slot, connector, comparison job, temporary policy, credential, network path, expanded privilege, exception, runbook, support role, capacity reservation, license, and provider commitment. Give each purpose, owner, dependencies, cost, risk, successor, expiry, evidence, rollback role, and removal test. Track old consumers through traffic, lineage, inventories, interviews, scheduled execution, and recovery drills. Close quarantine and reconcile authoritative history. Remove writers, readers, routes, access, catalogs, monitoring, billing, and support only after target recovery passes. Restore old configurations in isolation and verify tombstones and deny controls prevent publication, consumption, authorization, charging, or return of retired authority while required receipts remain controlled.
