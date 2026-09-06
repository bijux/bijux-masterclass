---
module_id: SARCH-042
program: Software Engineering: Software Architecture
level: 1
module_number: 42
title: Shared Database Versus Database per Service
status: complete
last_verified: 2026-09-06
---

# Shared Database Versus Database per Service

## One-Page Review

### Governing question

When should capabilities share transactional storage, and when should each service control a separate data boundary, given invariants, change, workload, security, reliability, queries, operations, and migration?

### Essential definitions

- A **shared database** is a persistence boundary directly used by multiple modules, services, or teams. Sharing may occur at server, cluster, database, schema, table, account, or transaction level; these are not equivalent.
- **database per service** means each service has exclusive authority over its private persistent model and other services use supported contracts. It does not require one physical database server per service.
- **write authority** is accountability and permission to accept a state transition; **physical write access** is merely a mechanism.
- A **transaction boundary** defines which reads, constraints, and writes can commit atomically under one database protocol.
- A **private schema** is an implementation detail owned by one boundary; a **published data contract** is a supported representation intended for consumers.
- A **distributed transaction** coordinates commit across distinct transactional participants.
- A **projection** is a derived read model maintained from authoritative changes for a consumer purpose.
- A **cross-service query** combines data governed by several authorities through composition, replication, analytical integration, or a deliberately shared read boundary.
- **noisy-neighbor interference** occurs when one workload consumes shared capacity and harms another.
- **polyglot persistence** selects different storage models by workload, accepting additional operational and integration cost.

### Central model, mechanism, or theorem

Separate three decisions:

$$
LogicalOwnership \neq TransactionPlacement \neq PhysicalPlacement.
$$

Two services can have isolated schemas, credentials, migrations, and capacity controls on one cluster; two databases on different servers can still be coupled by shared writes and lockstep releases.

For invariant $I$ over state set $X$, if all elements of $X$ must change atomically, then either place authority for $X$ in one transactional boundary or provide an explicit coordination protocol whose failure and recovery semantics preserve $I$. Network separation does not make the invariant disappear. Choose the smallest data boundary that satisfies required atomicity while enabling justified ownership, change, scaling, security, and failure isolation.

### Critical invariants

- assign every table, document, stream, and business invariant one accountable write authority;
- distinguish shared infrastructure, shared database, shared schema, shared tables, shared credentials, and shared write ownership;
- prevent services from reading or writing another service's private model as an undocumented contract;
- colocate state whose invariants require atomic commit unless a justified coordination protocol exists;
- version published query, command, event, snapshot, and analytical contracts independently of storage schemas;
- make cross-service queries declare authority, freshness, consistency, privacy, and failure behavior;
- account for connection, lock, cache, I/O, CPU, memory, storage, backup, restore, and operator contention;
- isolate credentials and least privilege even on shared infrastructure;
- test mixed service and schema versions, migration order, rollback, failover, restore, and reconciliation;
- avoid dual writes; publish changes through a recoverable outbox or equivalent local-commit protocol;
- give every projection and replica provenance, source position, rebuild, correction, retention, and deletion behavior;
- base separation on forces and evidence, and merge or retain shared boundaries when distribution buys no material benefit.

### Common failures

Frequent failures include interpreting database-per-service as server-per-service; giving every service the same database owner credential; declaring schemas private while consumers query them; splitting tables that enforce one invariant; using distributed transactions to imitate a monolith by default; replacing joins with long synchronous call chains; treating event delivery as immediate consistency; letting analytical jobs saturate operational storage; changing shared schemas without mixed-version rollout; using triggers as hidden integration; creating one backup that cannot restore services consistently; selecting a different database for every team; and measuring isolation by database count rather than authority and change coupling.

### Compact example

Orders and order lines require one atomic total and lifecycle invariant, so one order service owns both in one local database transaction. Inventory owns stock reservations and never permits order code to update its tables. Checkout coordinates a durable workflow: commit order intent, request an idempotent reservation, record its authoritative outcome, and compensate if required. A reporting projection joins order and inventory facts asynchronously with source versions and freshness. Physical databases may share a managed cluster while credentials, schemas, migrations, quotas, and restore procedures remain isolated.

### Connections

[SARCH-032](032-modular-monoliths.md) supplies internal data boundaries; [SARCH-039](039-microservices-architecture.md) supplies service independence; and [SARCH-041](041-system-of-record-boundaries.md) supplies fact-level authority. [SARCH-043](../ROADMAP.md) next examines synchronous request-response integration. Database Engineering owns transaction and storage internals; Data Architecture owns enterprise data topology and governance.

## Governing Question

Persistence boundaries are among the strongest architecture decisions because data outlives processes and deployments. A shared database can provide efficient transactions, joins, constraints, backup, and operational economy. It can also let every team depend on private representations, coordinate every migration, interfere with every workload, and bypass domain policy.

Database per service promises ownership and independent change. It also converts local joins and transactions into remote queries, projections, workflows, and reconciliation. It multiplies credentials, migrations, backups, monitoring, and recovery surfaces. The responsible choice separates logical authority from physical infrastructure and follows actual invariants, workloads, organizations, and lifecycle evidence.

## Why This Matters

An interface boundary is weak when consumers can bypass it through storage. A service cannot evolve independently if another service reads its tables or if one schema migration breaks several deployments. Security review cannot bound privilege when a shared credential can modify all domains. Recovery cannot be local when a restore produces mutually inconsistent business state.

Yet forced separation can be equally damaging. Two services coordinating one invariant through fragile distributed calls may be worse than two modules committing locally. A small team can inherit dozens of low-volume databases and on-call obligations. Cross-domain reporting can become a production fan-out operation.

The architecture must therefore answer several distinct questions: who owns meaning and writes, which facts must commit together, which representations are public, which workloads need isolation, which failures may be shared, and which physical consolidation is operationally efficient.

## Prerequisites and Retrieval

Retrieve service, module, schema, table, transaction, atomicity, isolation, constraint, invariant, write authority, credential, lock, connection pool, workload, index, replication, projection, event, outbox, consistency, freshness, query composition, distributed transaction, compensation, backup, restore, migration, version skew, tenancy, and noisy neighbor.

From SARCH-014 retrieve modularity tactics; SARCH-026 provides data views; SARCH-032 provides modular-monolith data ownership; SARCH-035 provides asynchronous changes; SARCH-036 provides remote failure; SARCH-039 provides microservice costs; and SARCH-041 provides system-of-record and authority-transfer discipline.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish logical data ownership, transactional placement, and physical database placement;
2. identify shared-server, database, schema, table, credential, workload, and authority coupling separately;
3. place atomic invariants within appropriate transaction and service boundaries;
4. prevent private-schema access while publishing stable service and data contracts;
5. design cross-service commands, queries, events, projections, and workflows;
6. compare local transactions, distributed transactions, reservations, compensation, and reconciliation;
7. evaluate workload, capacity, security, availability, backup, restore, and operator isolation;
8. evolve schemas and contracts under mixed versions and rollback;
9. migrate from shared writes to owned boundaries without indefinite dual authority;
10. choose consolidation or separation from measured forces rather than database or service counts.

## Core Exposition

**Separate ownership from hardware.** “Database per service” is an ownership constraint: only the service controls its private persistent model and write policy. Several service-owned schemas can share one database cluster with separate roles and quotas. Conversely, different database servers do not create autonomy if applications write each other's tables or deploy in lockstep.

Describe at least these layers: physical host or managed service, cluster, database, schema or namespace, tables/documents/topics, credentials, transaction manager, migration pipeline, backup set, and logical owner. Each layer has different coupling and isolation.

**Start with domain authority and invariants.** Group state that must obey one set of rules and atomically change under one decision. An order and its lines commonly form one aggregate: total, currency, and lifecycle must agree. Separating each table into a service adds a network protocol to one invariant without adding ownership value.

Evans uses aggregates as consistency boundaries in domain design [1]. They inform persistence placement but do not mandate one database or service per aggregate. Several aggregates can share a service and transaction system; cross-aggregate rules may use processes, reservations, or asynchronous reconciliation.

**Make every write owner explicit.** For each table or document, list the service or module authorized to create, update, correct, and delete. Database grants should enforce the design where possible. Shared database owner credentials make architecture diagrams aspirational.

Administrative repairs, ETL, reports, triggers, and migrations are write paths too. Route repairs through governed commands or a break-glass path with the same invariant and audit discipline. Inventory and revoke unused credentials.

**Treat private schemas as implementation.** A service can rename tables, split documents, add indexes, change normalization, archive history, or switch storage only if consumers depend on supported contracts. Direct SQL reads freeze column names, joins, null meanings, and timing as public behavior without ownership.

Published data products can use SQL views, snapshots, files, APIs, or events, but they need version, semantics, availability, privacy, and lifecycle. Calling a view “public” does not make unreviewed underlying change safe; assign it an owner and compatibility tests.

**Understand the shared-database advantages.** One transactional engine offers atomic commit, referential constraints, consistent reads, local joins, one query optimizer, and often simpler backup and operation. These are substantial when modules share invariants, one team owns change, workloads are compatible, and deployment remains cohesive.

Local calls avoid serialization and remote ambiguity. A modular monolith can enforce module-owned schemas and expose internal commands while retaining one database transaction where the domain requires it. Shared physical infrastructure can be efficient for many small workloads.

**Understand shared-database coupling.** Consumers can bypass behavior, causing invalid state. Schema changes require coordination. One expensive query, lock, or connection storm harms unrelated work. Backup, restore, maintenance, and regional failover have a shared blast radius. Auditors may struggle to separate access.

Coupling is sometimes acceptable and visible. It becomes a defect when teams claim independent deployment, security, or recovery that the data boundary cannot support. Record the shared fate explicitly.

**Understand database-per-service advantages.** Exclusive data authority strengthens information hiding, independent schema evolution, least privilege, targeted scaling, failure containment, and storage choice. Service contracts become the only supported integration path. Teams can release and operate at different cadences.

These benefits require enforcement. If a reporting team receives credentials to every private store, if shared domain libraries define every schema, or if releases remain synchronized, database count has changed but architecture has not.

**Understand separation costs.** Cross-service queries cannot use one local join. Cross-service transactions require coordination or redesigned semantics. Data appears in projections with lag. Infrastructure and operational work multiply. Debugging a user outcome spans services and stores.

Polyglot persistence adds driver, backup, security, performance, migration, and hiring knowledge. Choose it for a demonstrated workload or semantic fit, not developer novelty. A standard relational store is often sufficient across many services.

**Place transactions around invariants.** A transaction provides atomicity only for participating state under its engine and isolation level. If two values must never disagree, place them under one authority or use a protocol that makes the cross-boundary rule precise. Moving one value to another service does not weaken the business requirement.

Some apparent invariants can be redesigned. Inventory need not atomically decrement with order creation if inventory issues a reservation with expiry and identity. The global process temporarily includes pending states and explicit compensation. That is a domain change, not a database trick.

Gray and Reuter describe transaction processing as a combination of concurrency, recovery, distribution, and system structure [2]. A transaction label alone is insufficient; isolation, durability, participants, timeouts, and failure behavior matter.

**Use distributed transactions selectively.** Two-phase commit can coordinate prepared participants under supported systems. It can preserve atomic decision across them, but holds resources, depends on coordinator recovery, and couples participants and technology. It may be appropriate within one controlled estate with a hard atomicity need.

Do not reject it by slogan or make it the default replacement for local transactions. Compare with moving authority, reservation, escrow, idempotent workflows, compensation, or accepting bounded inconsistency. State what happens under participant crash, network partition, coordinator loss, and heuristic outcomes.

**Use sagas and compensation honestly.** A saga is a sequence of local transactions with coordination and compensating actions for certain failures [3]. Compensation is not rollback. A refund does not erase a charge or notification. Some actions cannot be compensated, and compensation itself can fail.

Persist process identity, step outcome, retry, timeout, compensation eligibility, manual state, and audit. Query unknown remote outcomes before deciding the next step. Do not let a message framework infer business completion.

**Publish changes from local commits.** A service that updates its database then publishes can crash between actions. Use a transactional outbox or change-log mechanism so the publication obligation commits with state. Relays and consumers handle duplicates and preserve source versions.

Change data capture can expose low-level table changes or a curated event stream. Low-level CDC couples consumers to storage representation and can reveal partial internal transitions. Translate into owned domain facts when stable meaning is required.

**Design cross-service queries by purpose.** Options include API composition, batch calls, a query service, event-built materialized views, federated queries, analytical pipelines, or data virtualization. Choose by freshness, latency, volume, consistency, privacy, availability, and ownership.

API composition preserves current authority but adds runtime fan-out and partial failure. A projection offers low-latency local reads but can be stale and needs rebuild and correction. Analytical integration handles large historical queries but should not become a hidden operational dependency.

**Avoid distributed joins on critical paths.** A page that calls ten services by entity ID recreates a database join through the network with worse latency and failure. Design coarse capability queries, denormalized read models, or precomputed views. Mark optional data and degraded behavior.

The query model need not mirror write ownership. Command-query responsibility segregation can use a normalized authoritative write model and several purpose-built read models. Every read model carries source, position, transformation, and freshness.

**Model consistency precisely.** Within one database, isolation level determines which anomalies transactions may observe. Across services and projections, define read-your-writes, monotonic reads, causal order, bounded staleness, or eventual convergence as needed. “Eventually consistent” is not one guarantee.

Consumers making high-consequence decisions may require direct authority or a signed bounded-stale copy. Browsing and analytics may accept lag. State failure when freshness cannot be established: fail closed, show stale timestamp, omit data, queue intent, or use an approved local rule.

**Version database changes for coexistence.** Independent services and rolling deployments mean old and new code overlap. Expand schema first, deploy compatible readers and writers, migrate and verify data, then contract after every old consumer is gone. Avoid renaming or changing meaning in one step.

Rollback is a data problem. Old code must tolerate state written by new code or rollback must be roll-forward. Test old-code/new-schema, new-code/old-state, interrupted backfill, duplicate migration, and restored backups.

**Separate schema migration ownership.** Each service owns its migration sequence and applies it through a controlled pipeline. A global migration repository can provide ordering and visibility but often recreates lockstep release. Shared tables need one migration owner even if several teams read them.

Migration tools execute DDL; they do not decide semantic compatibility, backfill correctness, lock impact, or rollback. Measure on production-like data and bound locks and log growth.

**Analyze workload interference.** Shared clusters share CPU, memory, buffer cache, I/O, transaction logs, connections, locks, storage, maintenance windows, and quotas. One service's batch query can evict another's hot pages. Connection pools sized independently can exceed server capacity.

Use workload classes, per-role limits, admission, statement deadlines, resource groups, replicas, or physical separation. Observe both per-service and aggregate saturation. Logical schemas alone do not isolate resources.

**Choose physical consolidation deliberately.** Many low-volume services can share a managed cluster to reduce cost and operator count while preserving separate databases, roles, migrations, and logical backups. High-throughput, regulated, noisy, or failure-critical services may warrant separate clusters or accounts.

Physical isolation is not free. More clusters multiply patching, certificates, networking, monitoring, failover, and cost. Platform automation can make a finite set of supported service classes safe without giving every team arbitrary infrastructure.

**Design connection and admission budgets.** If 30 services each configure a pool of 50 against a server allowing 500 useful sessions, theoretical demand is 1,500 connections before failover or jobs. Pools do not create database capacity. Allocate global and per-service budgets, queue or reject early, and include administrative reserve.

Proxies can multiplex connections but do not remove transaction concurrency or query cost. Measure active work, wait events, cache, log, and I/O rather than only open connections.

**Separate security boundaries.** Give each service a workload identity and least-privilege role. Restrict schemas, operations, network paths, and administrative capabilities. Encrypt connections and backups. Audit privileged access. Shared database ownership credentials defeat accountability.

Row-level controls can support tenancy but are easy to bypass through privileged roles or misconfigured queries. Defense combines domain authorization, database constraints, identity, tests, and monitoring. Database separation can reduce blast radius but multiplies secrets and policy surfaces.

**Plan backup and restore by business boundary.** One cluster backup may contain several services at one storage-consistent point. Restoring only one service can break cross-service workflows and projections. Separate backups allow local recovery but may lose a consistent estate-wide point.

Record log positions, event offsets, authority epochs, external effects, and projection rebuild sources. After restore, reconcile commands and messages. Recovery point and time objectives do not prove business state is correct.

Test restore, not only backup creation. Include key access, schema versions, data volume, point-in-time recovery, replay, duplicate messages, downstream projections, and privacy deletions.

**Model availability and blast radius.** Sharing a cluster creates common-cause failure even with isolated schemas. Separate clusters can fail independently but may share region, identity, network, or control plane. Cross-service synchronous calls can make a separate store's outage part of another service's availability.

Choose replication and failover per authority and consequence. Do not promote several writable copies without fencing. A service using a stale read replica must declare freshness and failover behavior.

**Treat analytics separately from operational authority.** Analytical workloads benefit from historical joins and scans across domains. Feeding a warehouse or lake from service-owned changes preserves operational authority while enabling governed cross-domain analysis. The analytical platform owns derived datasets and metrics, not source writes.

Avoid querying production service databases directly for routine analytics. It couples schemas, exposes sensitive data, and competes for resources. Publish purpose-limited data contracts with lineage and correction.

**Govern data sharing.** A consumer requesting data states purpose, fields, freshness, retention, volume, security, and support needs. The provider chooses API, event, snapshot, or governed view. Catalog ownership and usage so contracts can evolve and retire.

Data minimization is architectural. Replicating whole records for one field expands breach and deletion scope. Purpose-specific projections can reduce exposure but still require lineage.

**Migrate away from shared writes incrementally.** Inventory readers, writers, triggers, jobs, stored procedures, credentials, and reports. Choose one domain boundary. Put a supported interface in front of its writes while the existing database remains authoritative. Separate schema ownership and remove bypass access.

Then move physical data if needed. Backfill target state, consume one authoritative change stream, compare, cut over with one writer, fence old paths, and reconcile. Do not begin with application dual writes; partial failure makes divergence inevitable without a protocol.

**Merge when separation lacks value.** If two services always deploy together, share one team and invariant, perform chatty calls, and gain no independent scaling or security, merging their data and runtime can be a sound repair. Preserve module boundaries so internal ownership remains clear.

Do not merge independently regulated or high-blast-radius data solely to reduce database count. Compare recurring operations with the value of actual isolation.

**Test architecture claims.** Enforce forbidden cross-schema dependencies in builds and database grants. Test concurrent invariants, deadlocks, retries, lost responses, outbox recovery, projection replay, staleness, version compatibility, migration interruption, workload interference, credential compromise, failover, restore, deletion, and cutover rollback.

Observe coordinated releases, cross-database access, shared locks, pool saturation, query latency, migration duration, projection lag, reconciliation drift, restore success, and operator toil. These are evidence about the chosen boundary, not proof of universal correctness.

## Definitions and Notation

Let services or modules be $S$, persistent objects $D$, and invariants $I$. Write-owner function $owner:D\rightarrow S$ assigns one logical authority to every governed object. For invariant $i$, $scope(i)\subseteq D$ lists state that must be reasoned about together.

Transaction placement $tx:D\rightarrow T$ maps objects to transactional participants, while physical placement $phys:D\rightarrow P$ maps them to clusters or servers. Equal $phys$ does not imply equal owner; unequal $phys$ does not imply independent ownership.

For cross-service projection $r$, record source positions $pos_s(r)$ for each authority $s$, transformation version $v_t(r)$, build time, and freshness contract. A join result has no stronger authority or freshness than its declared sources and transformation.

For connection budgets, service $s$ has maximum admitted sessions $c_s$, shared administrative reserve $c_a$, and server safe bound $C$. A necessary configuration condition is

$$
\sum_{s\in S}c_s+c_a\le C.
$$

It does not guarantee performance because active query cost, pools, memory, I/O, locks, and workload correlation also matter.

## Mechanisms, Invariants, or Proof Structure

**Ownership invariant.** Every governed persistent object and domain transition has one accountable writer. Physical access by another service is denied or explicitly governed as the same authority.

**Atomicity placement argument.** If invariant $i$ must hold after every accepted transition and all $scope(i)$ participates in one serializable local transaction, the authority can validate and commit it atomically. Splitting state across participants removes that mechanism; preserving $i$ then requires another protocol or a changed invariant.

**Information-hiding invariant.** Consumers depend on supported contracts, not private storage representation. Indexes, normalization, and internal migrations can change without coordinated consumer release within that contract.

**Connection-budget invariant.** Configured aggregate admissions plus reserve do not exceed the safe server bound. Passing the inequality is necessary but not sufficient for workload safety.

**Publication invariant.** Authoritative state and publication obligation commit together or have a declared reconciliation mechanism. Consumers remain idempotent and version-aware.

**Projection invariant.** Derived data retains source authority, positions, transformation, freshness, rebuild, correction, privacy, and deletion semantics. A projection does not acquire write authority by being convenient.

**Compatibility invariant.** Old and new service code, schema, messages, projections, and backups coexist only in a tested supported matrix. Migration success is not inferred from DDL completion.

**Recovery invariant.** Restore and failover reestablish one authority and reconcile logs, messages, external effects, and derived copies before correctness is claimed.

**Migration invariant.** One scoped write authority exists at every cutover state. Shadow copies compare but do not decide; old credentials are fenced after transfer.

**Evidence invariant.** Database count, transaction success, replica health, message delivery, and passing tests are bounded observations. None alone proves data ownership, business consistency, or independent deployment.

## Alternatives and Trade-Offs

| Choice | Advantages | Costs and risks | Prefer when |
|---|---|---|---|
| One shared schema | efficient joins, constraints, transactions, and operations | maximum representation and release coupling | one owner and deployment govern cohesive invariants |
| Schema per service on one database | logical ownership and credential separation with local infrastructure economy | shared resource and maintenance blast radius | many modest workloads share an operating platform |
| Database per service on one cluster | stronger namespace and migration isolation | shared cluster capacity, failover, and administration | logical independence matters more than physical fault isolation |
| Separate cluster/account per service | strong resource, privilege, and failure isolation | cost and operational multiplication | workload, regulation, or consequence justifies it |
| Local ACID transaction | simple atomic invariant enforcement | limited to one participant and engine | state belongs to one authority |
| Distributed transaction | coordinated atomic decision | blocking/resource and technology coupling | hard atomicity across controlled participants is justified |
| Saga/compensation | service autonomy and long-running processes | intermediate states and fallible compensation | domain permits corrective effects |
| API composition | current authoritative reads | latency, fan-out, and partial failure | few bounded current facts are required |
| Event-built projection | fast purpose-specific reads and isolation | lag, duplicates, replay, and rebuild | freshness is bounded and current authority is unnecessary |
| Analytical copy | historical cross-domain joins | delayed data and separate governance | reporting and analysis tolerate pipeline semantics |
| One storage technology | lower cognitive and operating load | imperfect fit for specialized workloads | standard capabilities satisfy requirements |
| Polyglot persistence | workload-specific semantics and performance | skills, tooling, migration, and support burden | measured benefit repays lifecycle cost |

## Failure Modes and Misconceptions

1. **“Database per service means server per service.”** Ownership can be isolated on shared infrastructure.
2. **“Separate servers mean independent services.”** Shared writes, schemas, and releases can preserve coupling.
3. **“Shared database means no modularity.”** One owner can enforce strong module schemas and commands.
4. **“Private schema is private if documented.”** Grants, queries, jobs, and tests must enforce it.
5. **“Foreign keys define service boundaries.”** They express database relationships, not organizational authority.
6. **“Every aggregate needs a database.”** Aggregates guide consistency; physical placement has other forces.
7. **“Distributed transactions are always wrong.”** They can fit controlled hard-atomicity needs, with costs.
8. **“Sagas give rollback.”** Compensation is another fallible domain action.
9. **“Events replace joins.”** Projections add lag, duplicate, schema, rebuild, and privacy obligations.
10. **“CDC is a stable domain contract.”** Raw changes often expose storage representation.
11. **“Connection pooling solves database capacity.”** Pools can multiply admitted demand beyond the server.
12. **“A shared cluster isolates schema workloads.”** CPU, cache, I/O, logs, locks, and failover remain shared.
13. **“Independent backup means independent recovery.”** Workflows, events, and external effects need reconciliation.
14. **“Polyglot persistence proves autonomy.”** It may only multiply operational burden.
15. **“Dual writes simplify extraction.”** Partial failure creates two disagreeing copies.
16. **“More databases improve reliability.”** Dependency and common-cause structure determine outcomes.

## Worked Examples

### Example 1

**Situation.** Order headers and lines are proposed as separate services because they are separate tables.

**Reasoning.** Order total, currency, lifecycle, and line membership must agree in one accepted transition. Separate services would require remote coordination for every edit and add no team, scale, security, or lifecycle independence. Keep one order authority and local transaction, with internal modules if complexity warrants. Publish coarse order outcomes to other capabilities.

**Conclusion.** Tables that participate in one aggregate invariant belong under one transactional authority unless a justified protocol replaces it.

### Example 2

**Situation.** Twelve small services share one managed PostgreSQL cluster, and an auditor asks whether this violates database per service.

**Reasoning.** Each service has its own database or schema, credential, migration owner, tables, logical backup, connection budget, and no cross-write grant. The cluster, maintenance window, I/O, and failover are shared and recorded as common-cause risk. The arrangement realizes logical database-per-service ownership but not physical fault isolation. One regulated service moves to a separate account because its access and recovery boundary differs.

**Conclusion.** Logical ownership and physical consolidation can coexist when their different guarantees are explicit.

### Example 3

**Situation.** Thirty services each configure 50 connections to a shared database whose safe session bound is 500, with 40 reserved for administration.

**Reasoning.** Configured service demand is $30\times50=1{,}500$. Including reserve yields 1,540, exceeding the bound by 1,040. Even if pools rarely fill, simultaneous restart or latency can create a connection storm. Allocate per-service budgets whose sum plus 40 is at most 500, reject or queue before saturation, and measure active query cost. A proxy may reduce physical sessions but not underlying work.

**Conclusion.** Local pool defaults must satisfy a global admission model on shared infrastructure.

### Example 4

**Situation.** A dashboard needs order, inventory, and shipment status with 300 ms latency but can tolerate 30-second freshness.

**Reasoning.** Three synchronous authoritative calls add fan-out and availability coupling. Build a dashboard projection from versioned domain events, recording source positions and timestamps. Serve locally within the latency target and display data age. For a user action such as cancel shipment, call the current shipment authority with expected version; the projection never decides writes.

**Conclusion.** A purpose-built projection trades bounded freshness for predictable queries without transferring authority.

### Example 5

**Situation.** Checkout must create an order and reserve stock across two service-owned databases.

**Reasoning.** If the domain permits pending orders, commit order intent locally, send idempotent reservation `res-72`, and record inventory's authoritative outcome. On rejection, mark order unavailable; on unknown, reconcile; on later cancellation, release a known reservation with a new operation identity. If business truly requires no visible order without stock, either keep both within one authority or justify a distributed transaction. A saga does not make the steps atomic.

**Conclusion.** Transaction choice follows domain states and failure semantics, not a blanket ban or mandate.

### Example 6

**Situation.** A service commits a payment but crashes before sending its event.

**Reasoning.** Store payment and outbox publication obligation in one local transaction. A relay retries event delivery with stable event and payment versions. Ledger projection deduplicates by event identity and verifies monotonic account sequence. If publication remains delayed, operations can reconcile committed payments against outbox state. This does not prove a downstream shipment completed.

**Conclusion.** Local atomic publication machinery closes one gap while retaining separate delivery and business outcomes.

### Example 7

**Situation.** A reporting job queries every service's private schema nightly with one superuser credential.

**Reasoning.** The job freezes storage models, expands privilege, bypasses service capacity controls, and makes schema releases coordinate with reporting. Replace it with purpose-limited snapshots or event/CDC-derived analytical contracts owned by each service. Ingest into an analytical platform with lineage, source positions, correction, retention, and reconciliation totals. Revoke cross-store superuser access.

**Conclusion.** Cross-domain analytics needs governed publication, not privileged operational coupling.

### Example 8

**Situation.** A search service's batch reindex evicts hot pages and doubles checkout latency on the shared cluster.

**Reasoning.** Separate schemas did not isolate buffer cache, I/O, CPU, or logs. First throttle and schedule reindex, cap its connections and statements, and use a read replica if consistency permits. If peak workload still violates checkout scenarios, move search to a separate resource boundary. Compare measured interference and recurring cost before physical separation.

**Conclusion.** Physical isolation is a response to demonstrated shared-resource contention, not a consequence of service naming.

### Example 9

**Situation.** A new service needs a column rename while old and new instances coexist during rollout.

**Reasoning.** Renaming directly breaks old code. Add the new column or compatible view, deploy code that can read old and new representation and writes under one transition policy, backfill idempotently, verify counts and semantics, then switch readers. Only after old versions and rollback window end may the old column be removed. Backups and messages are tested with both versions.

**Conclusion.** Independent deployment requires expand-compatible-contract evolution beyond successful DDL.

### Example 10

**Situation.** Two services were extracted but always release together, share writes, call each other six times per request, and have one team and workload.

**Reasoning.** The split produced a distributed monolith. No independent scale, privilege, acquisition, or failure boundary is required. Merge into one deployment and transaction system, assign table ownership to internal modules, replace network calls with explicit module contracts, and retain events only for genuine external facts. Migration reconciles both stores and chooses one authority before retiring the other.

**Conclusion.** Recombining unjustified services can restore simpler correctness while preserving modular design.

## Cross-Program Connections

- **Database Engineering:** owns isolation levels, constraints, logging, locking, replication, distributed transactions, query planning, backup, and recovery internals.
- **Distributed Systems Engineering:** owns partial failure, consensus, replication, consistency, idempotency, coordination, and partitions across data authorities.
- **Data Architecture Engineering:** owns data domains, systems of record, integration, canonical models, analytical platforms, governance, lineage, and master data.
- **Data Engineering:** owns CDC, outbox relays, pipelines, projections, backfills, data quality, reconciliation, and deletion propagation.
- **API and Service Engineering:** owns command, query, event, schema, versioning, error, security, and reliability contracts between services.
- **Software Design and Domain Modeling:** aggregates, invariants, bounded contexts, repositories, and domain services inform logical data boundaries.
- **Software Delivery and Reliability Engineering:** schema delivery, progressive rollout, capacity, failover, restore, incidents, and rollback test independence.
- **Security Engineering:** workload identity, database roles, least privilege, audit, encryption, tenancy, and data minimization govern shared and separate stores.

## References

1. Eric Evans, *Domain-Driven Design: Tackling Complexity in the Heart of Software*, Addison-Wesley, 2003.
2. Jim Gray and Andreas Reuter, *Transaction Processing: Concepts and Techniques*, Morgan Kaufmann, 1992.
3. Hector Garcia-Molina and Kenneth Salem, “Sagas,” *Proceedings of the 1987 ACM SIGMOD International Conference on Management of Data*, 1987. <https://doi.org/10.1145/38713.38742>
4. Martin Kleppmann, *Designing Data-Intensive Applications*, O'Reilly Media, 2017.
5. Chris Richardson, *Microservices Patterns*, Manning, 2018.
6. Sam Newman, *Building Microservices: Designing Fine-Grained Systems*, 2nd ed., O'Reilly Media, 2021.
7. Martin Fowler, *Patterns of Enterprise Application Architecture*, Addison-Wesley, 2002.
8. Gregor Hohpe and Bobby Woolf, *Enterprise Integration Patterns: Designing, Building, and Deploying Messaging Solutions*, Addison-Wesley, 2003. <https://www.enterpriseintegrationpatterns.com/>

## Exercises

### Exercise 1

Define shared database, database per service, write authority, transaction boundary, private schema, published data contract, projection, noisy neighbor, and polyglot persistence. Explain why database count does not establish ownership.

### Exercise 2

A cluster has a safe bound of 900 sessions and reserves 60 for administration. Eighteen services each configure a maximum pool of 55. Apply the necessary connection-budget inequality, show the arithmetic, and state three limitations.

### Exercise 3

Two services claim independent deployment, but one reads the other's tables and both use a shared migration repository and owner credential. Diagnose the coupling and propose an incremental enforcement plan.

### Exercise 4

Compare API composition, an event-built projection, federated SQL, and an analytical copy for a customer-support screen and a quarterly regulatory report. Define authority, freshness, security, and failure behavior.

### Exercise 5

Design data boundaries for a rail network containing ticketing, seat inventory, train control, maintenance, passenger information, and finance. Place invariants and transactions, choose shared or separate physical storage where justified, define integrations, partitions, security, recovery, migration, and evidence. Identify one boundary where eventual consistency is unacceptable.

## Answers to the Exercises

### Answer 1

A **shared database** is directly used by multiple modules, services, or teams at some physical or logical layer. **Database per service** gives each service exclusive authority over its private persistent model, not necessarily a separate server. **Write authority** is accountability and permission to accept state changes. A **transaction boundary** defines state that can commit atomically. A **private schema** is implementation; a **published data contract** is supported consumer behavior. A **projection** is derived purpose-specific data. A **noisy neighbor** consumes shared capacity and harms others. **Polyglot persistence** uses several storage models for workload fit. Database count says where bytes reside; it does not say who can write, which contracts consumers use, whether releases coordinate, or which failures and operators are shared.

### Answer 2

Configured service demand is $18\times55=990$ sessions. Including 60 administrative sessions gives $1{,}050$, which exceeds the 900 bound by 150. The necessary inequality fails. Limitations include that configured pools may not be simultaneously full; sessions have unequal memory and query costs; a proxy can multiplex physical connections; workload, locks, I/O, and cache may saturate before session count; and failover can change the safe bound. Any three with correct arithmetic earn full credit. Repair requires explicit per-service allocations whose sum plus reserve is at most 900, followed by workload measurement and admission controls.

### Answer 3

Direct reads make the provider's tables a public undocumented contract; the shared owner credential defeats write and audit isolation; the global migration sequence couples releases. First inventory queries, writes, jobs, tests, and credentials. Assign the provider one schema and migration owner, prohibit consumer writes immediately, and publish a supported query contract or purpose-built projection for the consumer. Migrate reads, add contract and mixed-version tests, then revoke cross-schema select. Issue service identities with least-privilege roles. Split migration pipelines and use expand-compatible-contract changes with a catalog of dependencies. Physical separation can follow if resource or recovery forces justify it, but it is not needed to establish initial logical ownership.

### Answer 4

For an interactive support screen needing a few current account decisions, API composition can query authoritative services with bounded fan-out, deadlines, field authorization, and optional degradation. Frequently used descriptive context can come from an event-built support projection with source versions and visible freshness; sensitive actions still call authority. Federated SQL is useful for controlled investigation but couples availability, schemas, and query load and should use governed read endpoints rather than private stores. A quarterly regulatory report belongs in an analytical copy with period snapshots, lineage, definitions, reconciliation, access control, correction, and sign-off; it need not query operations live. Failure behavior differs: the screen omits optional stale data or reports unavailable current authority, while the report blocks certification until required inputs reconcile. No option transfers source write authority.

### Answer 5

Ticketing owns fares, ticket lifecycle, payment references, and passenger entitlements; seat inventory owns carriage/run capacity and atomic reservations; train control owns movement authority, signal state, and safety interlocks; maintenance owns asset work orders and release-to-service evidence; passenger information owns derived displays; finance owns ledgers and period reports. Ticket and seat reservation can use a durable workflow with stable identities, reservation expiry, unknown-outcome inquiry, and compensation; train movement and safety interlocks must remain in one local high-assurance transactional/control authority and cannot rely on eventually consistent cloud data. Passenger displays use event-built projections with timestamps and safe stale messaging. Finance ingests governed events and reconciles to source positions.

Train control uses physically isolated regional storage and local fail-safe operation. Ticketing and passenger services may use separate logical databases on a shared managed cluster if quotas, credentials, backup, and blast radius meet scenarios. Maintenance may separate by regulatory and offline-depot needs. Service contracts and durable events replace cross-writes. Identities and roles enforce least privilege; passenger data is minimized. Partition behavior preserves local movement safety, queues ticket intent within bounded rules, and marks information freshness. Recovery fences writers, restores log positions, reconciles external payment and movement outcomes, and rebuilds projections. Migrations use one authority, backfill, versioned change feed, comparison, fenced cutover, and tested rollback. Evidence includes invariant/concurrency tests, lost-response and duplicate-event tests, partition drills, capacity interference, schema coexistence, credential attacks, point-in-time restore, safety cases, and end-to-end reconciliation.
