---
module_id: SEPAT-095
program: Software Engineering: Patterns
level: 2
module_number: 95
title: Command Query Responsibility Segregation
status: complete
last_verified: 2026-08-29
---

# Command Query Responsibility Segregation

## One-Page Review

### Governing question

When do conflicting write-decision and read-retrieval forces justify separate models, and how can the resulting consistency gap remain explicit, bounded, observable and repairable?

### Essential definitions

- **Command Query Responsibility Segregation (CQRS)** uses different models for updating state and reading state.
- A **command** expresses intent to change authoritative state; it is validated, authorized and accepted/rejected, and should not merely expose setters.
- A **query** returns information without changing domain-observable state; infrastructure metrics/caches do not change that semantic rule.
- The **write model** owns command decisions, invariants, authorization and authoritative mutation.
- A **read model** is shaped for a query/audience and may be a direct view or asynchronously maintained projection.
- A **projection** transforms authoritative committed facts into read state.
- **logical separation** means different command/query interfaces or models; **physical separation** adds different schemas, databases, processes or services.
- **projection position/version** identifies how far a read model has incorporated source facts.
- **staleness** is the difference between authoritative state and observed read model at a stated boundary.
- **read-your-writes** means a client can observe its accepted change under a defined token/session/version policy.
- A **rebuild** recreates a read model from authoritative history/snapshot plus deltas into an isolated target.

### Central model, mechanism, or theorem

Let write authority move from (W_v) to (W_{v+1}) after accepting command (c). A projector eventually computes $R_p=project(W_{\le p})$ for source position $p\le v+1$. Query result (Q(R_p)) is correct for position (p), not necessarily for latest write revision. Therefore a CQRS API must expose or internally enforce the freshness required by each decision: accept stale display, wait for $p\ge v+1$, route to an authoritative query, or reject/degrade when the bound cannot be met.

CQRS starts with responsibility/model separation. Separate databases, asynchronous messaging, microservices and Event Sourcing are optional consequences, not defining requirements.

### Critical invariants

- Only the write authority accepts commands and enforces domain invariants against authoritative state.
- Query handlers do not perform domain mutations or smuggle commands through “get-or-create.”
- Each read model has named owner, source, audience, schema, projector version, position and freshness contract.
- Publication from committed write to asynchronous projection is durable; gaps, duplicates and reordering are handled explicitly.
- A query result states or respects its consistency point; stale data is never used where current authorization/safety is mandatory.
- Read-your-writes uses a version/token/fallback protocol, not arbitrary sleep.
- Projection application is idempotent and rebuild-safe; external effects are separated.
- Rebuild occurs in a new versioned target, catches up, reconciles and switches atomically.
- Sensitive read models minimize and authorize fields independently of write storage.
- The complexity budget is justified by measured read/write asymmetry and can be retired if forces disappear.

### Common failures

Failures include calling ordinary CRUD “CQRS”; one command per property setter; queries that mutate domain state; commands returning an entire read projection; using a stale read model for authorization or inventory acceptance; dual-writing two databases; no transactional outbox; assuming global order; dropping deletes; no position token; sleeping after writes; cache invalidation mislabeled as convergence; projection code with email/payment effects; rebuilding in place; sharing a read database as a new integration monolith; exposing secrets for query convenience; deploying two services too early; and assuming Event Sourcing is required.

### Compact example

Command `RenameProject` commits write revision 41 and returns `{project_id, accepted_revision:41}`. The query replica is at 39. A normal dashboard may show version 39 with freshness metadata. A redirect requiring read-your-writes sends token 41; the query waits within 200 ms for projection position ≥41, then falls back to an authoritative minimal status query or returns `202 pending`. It never assumes a 500 ms sleep is universally sufficient.

### Connections

[Command](032-command.md) establishes intent objects; [Event Sourcing](094-event-sourcing.md) can supply authoritative events but is optional. [Transactional Outbox](088-transactional-outbox.md) closes write/publication dual-write gaps, and [Idempotent Consumer](089-idempotent-consumer.md) supports projection replay. The successor [Materialized View](../ROADMAP.md) focuses on maintaining a derived query result whether or not the application uses CQRS.

## Governing Question

How should engineers separate update decisions from query representations only as far as real forces require, while preserving authority, consistency semantics, security and reversibility?

CRUD systems often use one model for validation, persistence and display. This is effective when rules and query shapes are simple. Trouble appears when writes require rich invariants and narrow authority while reads demand denormalized joins, full-text search, many audience-specific shapes, different scaling or historical aggregation. Forcing one model to serve both produces leaky domain objects, expensive queries, unsafe setters and constant compromise.

CQRS permits different models. Its minimum form can be two interfaces and two object shapes over one transactionally consistent database. Its maximum form can include separately deployed command and query services, event/outbox propagation and multiple stores. Each added physical boundary introduces latency, failure, versioning, operations and security. Apply only the degree of separation supported by evidence.

## Why This Matters

The write side answers “may this intent become authoritative?” It needs current rules, ownership, concurrency and a small consistency boundary. The read side answers “what information should this audience see efficiently?” It may require flattened cross-aggregate data, search indexes, aggregates and caching. Those are different responsibilities.

Physical separation improves independent scaling, workload isolation and specialized storage, but converts an in-process mapping into a distributed derived-data system. A command may succeed while a query remains stale. A projector may miss a record, process twice, or fail on a new schema. A read store may expose fields the command store protected. Recovery may replay years of facts. If the product cannot explain those states, separate stores make correctness worse.

CQRS should be judged by concrete forces: write/read throughput ratio, invariant complexity, query diversity, latency objectives, independent release needs, source load, data classification and rebuild objectives. “We use events” or “microservices are modern” are not forces.

## Prerequisites and Retrieval

Learners should retrieve:

- Command–Query Separation at method level;
- application service, domain aggregate, repository and transaction boundaries;
- database normalization, indexes, joins, replicas and materialized views;
- asynchronous messaging, outbox, idempotency, ordering and checkpoints;
- eventual consistency, monotonic reads and read-your-writes;
- schema evolution, backfill, reconciliation and versioned deployment;
- authentication, authorization, tenant/data classification and inference risk;
- latency/error budgets and workload/capacity measurement.

Before continuing, explain why a REST API with separate `POST` and `GET` endpoints is not sufficient evidence of CQRS, and why separate databases are not necessary.

## Learning Objectives

After this module, learners can:

1. distinguish method-level CQS, logical CQRS and physically distributed CQRS;
2. model command authority separately from query representation;
3. choose the least physical separation that satisfies measured forces;
4. define projection position, staleness and read-your-writes protocols;
5. close publication gaps and apply derived updates idempotently;
6. design query-specific read models without leaking write internals or secrets;
7. select consistency per use case, including authoritative fallback;
8. rebuild, reconcile, version and atomically promote read models;
9. test lag, gaps, duplicates, reorderings, schema changes and access control;
10. recognize when CQRS complexity should be avoided or removed.

## Core Exposition

### Begin with logical responsibility

Bertrand Meyer's Command–Query Separation says a routine should either return information without observable mutation or change state. CQRS applies a related separation at model/application scale: command code models decisions; query code models retrieval. A command can return acceptance identity/version or validation/conflict information needed to complete the protocol. It should not become an arbitrary query transport returning a huge denormalized screen.

A single deployment and database can implement CQRS. Command handlers load domain state and mutate normalized tables. Query handlers use explicit SQL views/read DTOs optimized for screens and never reuse mutable entities. This yields clearer authority and representation without eventual consistency. Add a separate read store only when workload, availability, query technology, scaling or team ownership requires it.

### Define command authority

A command is named by intent—`ApproveLoan`, not `SetStatus`. The write model authenticates the principal, authorizes action, validates syntax/business preconditions, enforces concurrency and commits one authoritative result. It owns server-derived identifiers, timestamps, tenant and policy outcomes. Command handlers must not trust a read projection for invariants unless staleness is explicitly acceptable.

Return a compact receipt: command ID, resource ID, outcome, authoritative revision/position and perhaps a status URL. A rejected command creates no domain state change, though audit/metrics may record the attempt. Retry uses stable command identity and payload-digest conflict rules. Concurrency control remains necessary even if commands arrive through a queue.

### Design read models per decision/audience

A read model is not “copy every write table.” Begin with query: fields, filters, sort, pagination, audience, authorization, freshness, availability and scale. Denormalize deliberately; precompute only valuable work. One screen may need `ProjectSummary`; finance may need an aggregate; search needs an inverted index. Separate models can evolve independently but multiply schema, projection and operational ownership.

Read models should carry source version/position and projector version. A row version can support per-entity monotonicity; a global checkpoint can describe a projection shard. Beware claiming global freshness from one partition. Authorization can require current authority: do not grant access from a stale membership projection after revocation. Either query the authority, use short-lived signed grants with explicit revocation bounds, or wait for the required version.

### Choose a propagation mechanism

If both models share one database, the command transaction can update write tables and a local materialized/read table atomically, at the cost of write coupling. Database-generated materialized views may refresh synchronously or asynchronously under engine semantics. A separate store requires durable facts.

Naïve dual write—commit write database, then update read database—has failure windows. Use a transactional outbox, an event-sourced commit stream or log-based CDC with an explicit translation boundary. The projector consumes at least once and atomically records an event/change identity or source version with its mutation. It detects gaps, handles duplicates and defines ordering per entity/partition. Events must contain stable query-relevant facts or the projector must perform governed lookups; unbounded synchronous fan-out recreates coupling.

### Make consistency a product contract

“Eventually consistent” is incomplete. Specify:

- maximum normal and degraded lag by use case;
- position/version exposed in command receipt and query response;
- whether reads are monotonic in a client session;
- how read-your-writes works and its wait budget;
- authoritative fallback or `pending/unavailable` behavior;
- which decisions categorically cannot use stale projections;
- how conflict/correction is communicated when an accepted command is later compensated.

Common read-your-writes protocol: command returns source position (v); client sends `minimum_version=v`; query service serves only when its applicable projection/shard position is at least (v). It waits within a deadline, routes to an authoritative minimal query, or reports pending. Sleeping is neither load-aware nor a correctness guarantee. Sticky primary reads can work in replicated databases but must use actual replication/session semantics.

### Scale and isolate with evidence

CQRS can isolate expensive search/analytics from transactional writes and scale reads independently. It can also double stores, schemas, monitoring and on-call surfaces. Before physical split, measure slow query plans, lock/contention, replica capacity, read/write ratio and domain-model leakage. Indexes, caching, read replicas, SQL views or a reporting database may solve the force more cheaply.

Separate deployment is stronger than separate model. It introduces API/event contracts, version skew, network failure and team coordination. Do not split merely to draw two boxes. A modular monolith with explicit command/query packages can preserve boundaries and offer a migration seam. Extract only if independent scaling/release/availability is real.

### Evolve and rebuild projections safely

Projector code is a long-lived interpreter of history/change records. Maintain input schema fixtures and deterministic transformations. A new read schema/projector version should build `read_v2` separately, from an explicit start and upper position. Rate-limit replay, isolate resources, suppress external effects, checkpoint, stop on unsupported events/gaps and observe catch-up.

At upper position (q), reconcile `read_v2` against authoritative semantics: keyed counts/digests, missing/extra entities and domain/query invariants. Continue live changes, wait until promotion freshness, then switch readers atomically. Retain `read_v1` for rollback. In-place truncate-and-rebuild creates long outages and an ambiguous mixture of versions.

Projection correction can replay from zero, from a verified snapshot, or compensate targeted rows when correctness is provable. Record lineage and projector version. Never “fix” read rows manually without a reproducible repair source, because next replay will undo the repair.

### Secure every copy

Read optimization is data replication. Each projection needs classification, field minimization, tenant isolation, authorization, encryption, retention and deletion propagation. A broad analytics/search read store may create more exposure than the write database. Prejoined fields can enable inference even if individual columns seem harmless.

Commands and queries have different abuse profiles. Commands need authorization, idempotency, concurrency and rate controls. Queries need row/field policy, complexity/pagination bounds, cache partitioning and resistance to enumeration/inference. Do not share a “read-only” database credential that can see all tenants and assume the API layer is the only boundary.

### Observe correctness, not just lag

Monitor command success/reject/conflict/deduplication, outbox age, projection source-to-observed lag in time and positions, gaps, duplicate/stale application, poison records, checkpoint progress, query latency/error/staleness, rebuild ETA and source impact. Zero lag only proves progress through inputs, not correct mapping.

Reconcile independently. Inject a projection defect in staging and prove alarms/digests detect it. Test broker loss/duplicate/reorder, projector crash before/after checkpoint, schema evolution, delete, tenant authorization, source failover and rebuild promotion. Define who owns the write-to-read correctness incident; otherwise each team reports its component green.

### Deterministic projection and minimum-version reads

This pure model applies versioned project events idempotently, detects a gap, and evaluates whether a query can satisfy a minimum version.

<!-- bijux-verify: {"id":"sepat-095-projection-version","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"apply=1:created,2:renamed,duplicate-2,gap-4\nproject=Atlas version=2\nminimum-2=ready\nminimum-3=pending\n","stderr":""}} -->
```python
project = None
version = 0
trace = []
events = [
    (1, "created", "Aster"),
    (2, "renamed", "Atlas"),
    (2, "renamed", "Atlas"),
    (4, "renamed", "Aurora"),
]

for incoming, kind, name in events:
    if incoming <= version:
        trace.append("duplicate-" + str(incoming))
        continue
    if incoming != version + 1:
        trace.append("gap-" + str(incoming))
        continue
    project = name
    version = incoming
    trace.append(str(incoming) + ":" + kind)

def readiness(minimum):
    return "ready" if version >= minimum else "pending"

print("apply=" + ",".join(trace))
print("project=" + project + " version=" + str(version))
print("minimum-2=" + readiness(2))
print("minimum-3=" + readiness(3))
```

The run proves this sequential projection model only. It does not implement command authority, durable publication, transactions, broker ordering, concurrent projectors, persistence, wait/fallback protocols, authorization, reconciliation or rebuild promotion.

## Definitions and Notation

Let (W_v) be authoritative write state at revision (v), $F=\langle f_1,\ldots\rangle$ committed facts/change records, (P_j) projector version (j), (R_{j,p}) its read state through source position (p), and (Q_x(R)) query (x). Let (receipt(c)=(id,outcome,v)) be a command receipt.

**Write correctness** is validation/authorization/invariant preservation at authoritative revision. **Projection completeness through (p)** means every applicable fact through (p) is reflected exactly under (P_j)'s semantics. **Freshness lag** may be measured in positions and elapsed time, but only within a valid source/shard coordinate. **Read-your-writes for receipt (v)** means the subsequent query is evaluated on state incorporating that accepted write or an authoritative equivalent—not simply that time elapsed.

If projectors are deterministic and idempotent, replay of the same ordered unique facts gives the same (R_{j,p}). That does not prove that (P_j) implements intended meaning; reconciliation needs an independent oracle. Multiple sources generally lack one scalar (p); use a version vector/watermarks or explicitly weaker guarantee.

## Mechanisms, Invariants, or Proof Structure

1. **Record forces.** Measure command invariant complexity, query diversity/cost, workload and independent scaling/availability needs.
2. **Separate logically.** Give command and query interfaces/models explicit ownership in one deployment/store first where sufficient.
3. **Define authority.** Commands authenticate, authorize, validate, dedupe, enforce concurrency and return compact receipts with revision.
4. **Design query contracts.** Specify audience, fields, shape, authorization, pagination, latency and acceptable consistency.
5. **Choose physical topology.** Same transaction, replica/view or independent store; enumerate new failure modes.
6. **Publish durably.** Use one transaction/outbox/event log/CDC contract; never rely on uncoordinated dual writes.
7. **Project defensively.** Stable identity, per-scope order, duplicate/gap detection, idempotent checkpoint and poison-record policy.
8. **Negotiate freshness.** Minimum-version tokens, deadlines, authoritative fallback and explicit pending/degraded behavior.
9. **Rebuild/version.** Isolated target, bounded replay, reconciliation, catch-up, atomic switch and rollback.
10. **Govern copies.** Security/privacy, capacity, SLOs, recovery ownership and evidence for eventual retirement/simplification.

For read-your-writes, if a command receipt proves accepted source revision (v), and the relevant projector proves complete through $p\ge v$ in the same ordering scope, a query from that projection incorporates the write—assuming deterministic correct mapping and no later authorized change obscures it. The claim fails if versions are incomparable, a gap was skipped, the write is outside the projection, or the requested semantics require latest state beyond (v). Thus version tokens are stronger than delay but not universal linearizability.

## Alternatives and Trade-Offs

**Single CRUD/domain model** minimizes types, stores and latency. Prefer for simple domains/queries; use explicit DTOs and query SQL before splitting architecture.

**Separate query objects in one database** provide logical CQRS and optimized SQL while retaining transaction consistency. They may be the durable endpoint.

**Read replicas** offload reads with replication lag but preserve similar schema/query model; route freshness-critical reads carefully.

**Cache-aside** accelerates hot reads with invalidation/staleness concerns. It is lighter than a fully owned projection for simple keys.

**Database views/materialized views** centralize derived query logic; refresh and index constraints are engine-specific.

**Reporting warehouse/search index** is a specialized read model when latency and semantics permit, whether or not labeled CQRS.

**Event Sourcing plus CQRS** gives rich replay facts and projections but compounds permanent history/schema/operations. Use only when each pattern is independently justified.

**API composition/federated query** reads owners synchronously instead of copying state; freshness improves while latency/availability coupling and fan-out grow.

Choose per query. A strongly consistent payment authorization can read authority while a dashboard uses an asynchronous model. Consistency is not one service-wide switch.

## Failure Modes and Misconceptions

- **“Separate endpoints equal CQRS.”** The models/responsibilities must differ meaningfully.
- **“CQRS means two databases.”** Logical separation may share one store/transaction.
- **“CQRS requires Event Sourcing.”** Conventional write tables can publish outbox/CDC facts.
- **“Commands never return anything.”** They can return outcome, identity and revision; they should not become arbitrary queries.
- **“Queries cannot touch caches/metrics.”** The semantic rule forbids domain-observable mutation, not infrastructure bookkeeping.
- **“Eventually consistent is enough.”** Every use case needs a bound/fallback and forbidden-staleness decisions.
- **“Sleep after POST.”** Time delay does not prove projection position.
- **“Read store can authorize.”** Revocation/inventory/funds may require current authority.
- **“Dual writes are reliable.”** Partial failure creates divergence; use transactional publication.
- **“At-least-once is harmless.”** Only idempotent projection/effect boundaries make duplicates neutral.
- **“One checkpoint proves all shards.”** Positions have scopes; gaps can hide behind aggregate lag.
- **“Rebuild production in place.”** Mixed versions/outage prevent clean validation and rollback.
- **“Zero lag proves equality.”** Mapping/filter/delete defects need independent reconciliation.
- **“Read-only means low risk.”** Denormalized copies expand privacy, inference and tenant-isolation risks.
- **“More projections are free.”** Each is a product with schema, ownership, SLO, repair and retirement cost.

## Worked Examples

### Example 1

**Situation.** A monolith uses rich order aggregates for writes and ten expensive dashboard joins.

**Reasoning.** Add explicit query SQL/DTOs and indexed views in the same database while commands continue through aggregates. This is logical CQRS: models differ, transactions remain local, no projection lag is introduced.

**Conclusion.** Start with the smallest separation that resolves model conflict; separate stores are optional.

### Example 2

**Situation.** `ApproveRefund` returns a 200-field customer dashboard.

**Reasoning.** The command receipt only needs outcome, refund ID and revision. Returning a query projection couples write availability/latency to read assembly and obscures eventual freshness. Client can query the dashboard with minimum revision when needed.

**Conclusion.** A command may return protocol evidence without becoming a query facade.

### Example 3

**Situation.** Access is revoked at revision 73, but a document read model remains at 72.

**Reasoning.** Serving from it can disclose data after revocation. The endpoint must wait for ≥73, validate authorization against authority, or use a grant with a documented revocation bound. A stale badge count may be acceptable; access control is not.

**Conclusion.** Consistency policy belongs to each decision, not to CQRS globally.

### Example 4

**Situation.** A command commits, then the process dies before updating the read database.

**Reasoning.** This is dual-write loss. Put a projection fact in an outbox in the command transaction or derive via governed CDC. The projector consumes it at least once and applies idempotently.

**Conclusion.** Physical CQRS requires durable write-to-read propagation, not best-effort callbacks.

### Example 5

**Situation.** A client sleeps one second after renaming a project but occasionally sees the old name.

**Reasoning.** Lag is load/failure-dependent. Return accepted revision 41; query waits for the matching shard to reach 41 within deadline, then falls back or reports pending. This is falsifiable and observable.

**Conclusion.** Position-based read-your-writes replaces timing folklore with an explicit protocol.

### Example 6

**Situation.** Projector receives versions 18, 20, then 19 for one entity.

**Reasoning.** Applying 20 immediately may make 19 stale; skipping 19 might lose a non-overwriting fact. Pause/buffer and repair the gap, or use a source/version model where applying the latest full image is provably safe. Do not silently sort unrelated global events.

**Conclusion.** Ordering/gap policy depends on event semantics and version scope.

### Example 7

**Situation.** Search read-model version 2 needs a new tokenizer.

**Reasoning.** Build a new index, replay to bounded position, verify counts/search fixtures and tenant isolation, catch up, then switch alias atomically. Keep v1 for rollback. Updating documents gradually in one index mixes tokenization semantics.

**Conclusion.** Versioned build-and-switch makes projection evolution reviewable and reversible.

### Example 8

**Situation.** A query service owns local copies from four services and begins defining their business status.

**Reasoning.** It has become an integration/data monolith. Preserve owner facts and source versions, keep derived labels explicitly derived, avoid commands based on inferred truth, and consider API composition for freshness-critical fields.

**Conclusion.** Read convenience must not silently transfer domain authority.

### Example 9

**Situation.** Read traffic is only 20 requests per minute and queries are indexed under 30 ms, yet a team proposes Kafka and Elasticsearch.

**Reasoning.** There is no measured scaling/query force. New infrastructure adds lag, security copies, on-call and rebuild paths. Separate query DTO/SQL is sufficient and easier to verify.

**Conclusion.** Reject physical CQRS when complexity cost exceeds evidence-backed benefit.

### Example 10

**Situation.** A credit-decision projection joins income, debts and risk flags and is used for regulated denials.

**Reasoning.** The team must specify source ownership, freshness/version vector, missing/late data, correction, model/policy version, explanation and authoritative fallback. Reconciliation needs decision-level fixtures, not only row counts. A named human credit-risk, compliance, security and domain review must approve which stale states are permissible and how adverse decisions are corrected.

**Conclusion.** High-stakes read models require explicit provenance, bounded consistency and human-governed decision evidence.

## Cross-Program Connections

- **Domain Modeling:** commands and aggregates define authoritative decisions; read DTOs must not replace domain invariants.
- **Database Engineering:** indexes, replicas, views, transactions and isolation may solve read/write forces before multiple stores.
- **Distributed Systems:** eventual consistency, ordering, idempotency, version vectors and failure boundaries govern projections.
- **Data Engineering:** backfill, watermarks, lineage, quality and reconciliation turn read models into operated data products.
- **Security Engineering:** replicated, denormalized data needs independent classification, tenant policy and revocation semantics.
- **API Engineering:** command receipts, polling/status resources and minimum-version query contracts expose consistency honestly.
- **Reliability Engineering:** lag budgets, poison records, rebuild RTO and atomic promotion require runbooks and ownership.
- **Testing and Quality:** fault injection and oracle-independent reconciliation validate more than component uptime.

## References

- Martin Fowler, [CQRS](https://martinfowler.com/bliki/CQRS.html), 2011, retrieved 2026-08-29. Defines separate update/read models, warns about complexity and distinguishes Event Sourcing.
- Greg Young, [CQRS Documents](https://cqrs.files.wordpress.com/2010/11/cqrs_documents.pdf), 2010, retrieved 2026-08-29. Foundational CQRS, command, event and read-model material.
- Microsoft Azure Architecture Center, [CQRS Pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/cqrs), retrieved 2026-08-29. Current guidance on separate models/stores, synchronization, benefits, challenges and materialized views.
- Bertrand Meyer, *Object-Oriented Software Construction*, second edition, Prentice Hall, 1997. Source of Command–Query Separation at routine/object design level.
- Martin Kleppmann, *Designing Data-Intensive Applications*, O'Reilly Media, 2017, chapters 5, 11 and 12. Durable foundations for replicas, derived data, streams and consistency.
- Eric Evans, *Domain-Driven Design*, Addison-Wesley, 2003. Establishes aggregate/domain-service boundaries relevant to command authority.
- Pat Helland, [Life Beyond Distributed Transactions: An Apostate's Opinion](https://www.cidrdb.org/cidr2007/papers/cidr07p15.pdf), CIDR 2007, retrieved 2026-08-29. Explains entity-local transactions, uncertainty and identity in distributed workflows.
- Chris Richardson, [CQRS Pattern](https://microservices.io/patterns/data/cqrs.html), Microservices.io, retrieved 2026-08-29. Concise pattern forces and result for query replicas in service architectures.

## Exercises

### Exercise 1

Distinguish CQS, logical CQRS, physical CQRS, read replica and Event Sourcing. Give one topology where CQRS uses one database.

### Exercise 2

A command returns revision 88. A partitioned read model reports entity version 87 but global checkpoint 92. Decide whether it can satisfy `minimum_version=88` and explain required metadata.

### Exercise 3

Diagnose a CQRS system with zero reported lag, missing deleted users, duplicate welcome emails after rebuild and occasional cross-tenant search results.

### Exercise 4

Choose among same-database query DTOs, read replica, asynchronous projection and API composition for product detail, checkout authorization, search and monthly finance reporting.

### Exercise 5

Design CQRS boundaries for an unfamiliar emergency-dispatch platform. Include consistency tiers, degradation, propagation, rebuild, privacy, incident evidence and simplification criteria.

## Answers to the Exercises

### Answer 1

CQS separates mutating commands from observation queries at method semantics. Logical CQRS uses distinct write-decision and read-retrieval models, possibly in one process/database: for example commands update normalized order tables through aggregates while query handlers execute read-only SQL into screen DTOs in the same transactionally consistent database. Physical CQRS places models in different schemas/stores/processes and introduces propagation/staleness. A read replica is a physical copy with similar model and replication semantics; it may support CQRS queries but is not itself proof of model separation. Event Sourcing makes events authoritative history; CQRS can use ordinary current-state tables, and Event Sourcing can exist without broadly separate read infrastructure.

### Answer 2

Global checkpoint 92 does not establish that this entity's partition incorporated revision 88; partitions may progress independently and the checkpoint may describe another scope. Entity version 87 cannot satisfy a receipt explicitly comparable in the same entity revision domain. The service should wait for entity/source partition position ≥88, consult authoritative state, or return pending within its contract. Required metadata includes source/aggregate identity, partition/shard lineage, accepted revision or event position, projector version, gap status and whether receipt/read coordinates are comparable. If revision 88 was a command revision but projections use an unrelated global offset, maintain a mapping/watermark produced by the commit rather than compare bare numbers.

### Answer 3

Zero lag may reflect advanced checkpoints despite defective projection logic. Missing users indicate dropped/expired/mis-keyed delete facts. Duplicate emails show external effects coupled to replay or missing effect idempotency. Cross-tenant search indicates a security mapping/index/filter defect. Stop high-risk reads/effects, preserve evidence and identify affected positions/tenants. Rebuild an isolated corrected projection from authoritative facts with delete tests and tenant-keyed routing, while effect handlers remain disabled. Reconcile missing/extra keys and tenant-scoped digests, test authorization at query and storage layers, and use an atomic alias switch. Add delete counters, per-shard gap/lag, effect ledger, projector-version metadata and cross-tenant negative tests. Notify/security-review according to incident policy; advancing offsets is not exonerating evidence.

### Answer 4

Product detail can use same-database query DTOs or a read replica if schema and load are modest; a search index is justified for full-text/facets with acceptable staleness and rebuild. Checkout authorization for price, inventory and entitlement must use authoritative state or a reservation/grant protocol with explicit bounds, not a stale search projection. Monthly finance reporting fits asynchronously governed warehouse/materialized views with period-close reconciliation and lineage. API composition can fetch a few freshness-critical owner facts but adds latency/availability fan-out; use it selectively in product detail, not as an unbounded join engine. Selection is per query/decision, with measured load and consistency, not one universal CQRS topology.

### Answer 5

Commands such as `AssignUnit` and `CloseIncident` go to authoritative incident/unit aggregates with authenticated dispatcher identity, current availability rules, concurrency and stable command IDs. Return incident ID and accepted revision. A dispatch operational view may be asynchronous only if its lag bound meets safety; assignment conflict/authorization queries use authority or wait on minimum revision. Public status can tolerate more lag and expose fewer fields. If projection health or position confidence fails, degrade to authoritative minimal views/manual operations rather than display plausible stale availability.

Publish committed facts through outbox/event authority, partition/order per incident or unit as required, and project idempotently with duplicate/gap detection. Maintain per-source/version vectors where several authorities contribute. Build new projections in isolated targets, replay to a bound without notifications, reconcile incident/unit assignments, catch up and switch atomically. Encrypt/minimize location and medical data, segregate roles/tenants/agencies, audit emergency access and define retention/deletion. Test network partitions, out-of-order reassignment, duplicate commands, revocation, poison records, regional failover and full rebuild under incident load. Named human dispatch-domain, safety, privacy and security reviewers must approve degraded modes. Retire separate stores if measured scale/query benefits disappear and same-database models can meet latency/availability; simplification is an explicit success criterion.
