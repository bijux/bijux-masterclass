---
module_id: SEPAT-091
program: Software Engineering: Patterns
level: 2
module_number: 91
title: Repository
status: complete
last_verified: 2026-08-29
---

# Repository

## One-Page Review

### Governing question

When a domain model must retrieve and persist aggregate roots, how can it express collection-like domain intent while keeping storage mapping/query machinery outside the model—without hiding transaction, authorization, consistency, latency or query-shape semantics?

### Essential definitions

- A **Repository** mediates between domain and data-mapping layers, presenting a collection-like interface for domain objects or aggregate roots.
- An **aggregate root** is the only external reference/consistency entry point for an aggregate; repository mutation normally operates at that boundary.
- A **Data Mapper** translates between in-memory domain objects and storage representation without making the domain object responsible for persistence.
- A **Unit of Work** tracks/coordin­ates changes and commits a business transaction's storage effects.
- An **Identity Map** ensures one in-memory object instance per storage identity within one unit of work/session.
- A **Specification** expresses a domain predicate that a repository may translate to a query.
- A **query object** represents a particular query/shape/paging contract; it may be preferable to an ever-growing repository.
- A **DAO** often exposes storage/table-oriented operations or records; a domain Repository speaks in aggregate/domain concepts.
- A **persistence port** is an application/domain-owned interface implemented by infrastructure; not every port is a Repository.
- **optimistic concurrency** detects stale mutation through an expected version/conditional write.

### Central model, mechanism, or theorem

For aggregate type \(A\), Repository \(R_A\) approximates a conceptual collection:

\[
R_A.get(id),\quad R_A.add(a),\quad R_A.remove(a),\quad R_A.matching(s).
\]

The illusion is intentionally partial. Storage access has latency, failure, finite query shapes, authorization, isolation and consistency. Correctness requires each operation to define tenant/principal scope, absence semantics, consistency/snapshot, result bounds/order/page, loading depth, version precondition and unit-of-work participation. A Repository preserves domain language and one-way dependency; it cannot make remote/database behavior equal to an in-memory list.

### Critical invariants

- Repository interfaces are owned by the domain/application side; infrastructure depends inward to implement them.
- Methods express aggregate/use-case intent and stable predicates, not arbitrary table/ORM/vendor operations.
- Mutation occurs through aggregate roots and preserves aggregate invariants in one defined transaction.
- Authorization/tenant constraints are applied in the data predicate/transaction; a separate pre-check cannot create a disclosure or time-of-check/time-of-use gap.
- Identity is stable; one unit of work does not materialize conflicting instances silently.
- `save`/update uses expected version or another concurrency rule; last-write-wins is explicit, never accidental.
- Query results define absence, deterministic ordering, pagination bounds, duplicates, consistency and loading shape.
- Repository errors are domain/application/storage-independent categories; transports map them later.
- The interface does not promise storage interchangeability it has not earned; differing consistency/search/transaction capabilities stay visible.
- Test fakes satisfy the same contract—including conflicts, isolation, ordering and transaction behavior—or are labelled limited test doubles.

### Common failures

Common failures include one generic `Repository<T>` with `findAll/save/delete`; one repository per table instead of aggregate; leaking ORM query objects/entities/exceptions; hiding N+1 queries behind property access; loading unbounded collections; performing authorization before an unconstrained lookup; transaction-per-method when the use case needs atomic multi-operation work; putting commits inside every repository call; returning mutable persistence entities as transport DTOs; a fake that ignores uniqueness/version/transaction isolation; mocking repository internals instead of testing contracts; assuming “can swap SQL for NoSQL” despite different query/consistency semantics; using repositories for external APIs; and adding a wrapper over an ORM that already supplies the same abstraction without domain value.

### Compact example

`OrderRepository.open_for_customer(customer_id, page)` returns bounded aggregate roots visible under the authenticated tenant, ordered by `(created_at,id)` with snapshot/paging semantics. `save(order, expected_version=7)` conditionally writes aggregate changes and an outbox event inside the application-owned unit of work. A zero-row update becomes `VersionConflict`, not a vendor exception. Reporting uses a dedicated read projection rather than teaching the Repository arbitrary joins.

### Connections

[SEPAT-052](052-domain-model.md), [SEPAT-057](057-data-mapper.md), [SEPAT-055](055-unit-of-work.md), [SEPAT-056](056-identity-map.md) and [SEPAT-043](043-specification.md) form the main collaboration. The successor [Data Transfer Object](../ROADMAP.md) defines boundary-specific data carriers that should not be confused with aggregates returned by a Repository.

## Governing Question

How should a Repository preserve domain vocabulary and aggregate boundaries while exposing every storage behavior that affects correctness, performance, security and test parity?

The pattern is valuable when query construction/mapping is substantial and domain clients need to reason as if selecting aggregate roots from a conceptual set. It is harmful when it becomes a generic CRUD ceremony, launders vendor semantics through vague methods, or pretends all data stores are interchangeable.

## Why This Matters

Without a deliberate persistence boundary, domain/application code accumulates SQL, ORM sessions, storage records, query syntax and vendor exceptions. Rules become tied to fetching details; multiple callers duplicate authorization and query logic; tests require infrastructure even for pure decisions. A Repository can concentrate retrieval/persistence knowledge and let clients speak `orders_awaiting_payment`, not `SELECT ... JOIN ...`.

But hiding too much is equally dangerous. An in-memory collection has cheap repeatable iteration; a database query has latency, isolation and resource cost. A `find_all()` interface permits accidental production scans. A fake list makes concurrent writes succeed when production raises uniqueness/version conflict. A repository that accepts arbitrary predicates cannot reliably translate them. Abstraction quality is measured by preserved domain meaning and explicit effects, not by how few database words appear.

Repository is most coherent with a rich Domain Model, Data Mapper and aggregate roots. Transaction Script or simple CRUD systems may be clearer with focused gateways/DAOs or direct ORM use. Query-heavy read models often use CQRS/query services directly. Pattern selection follows forces.

## Prerequisites and Retrieval

Learners should retrieve:

- entities, value objects, aggregate roots and invariant boundaries;
- Domain Model, Transaction Script and Service Layer;
- Data Mapper, Active Record, Unit of Work and Identity Map;
- local transactions, isolation, uniqueness and optimistic concurrency;
- Specification/query objects, indexing, ordering and pagination;
- authentication, authorization predicates, tenant isolation and side channels;
- ports/adapters, dependency inversion and error translation;
- test doubles, contract/integration tests and production observability.

Before continuing, explain why an in-memory `list[Order]` fake that permits two concurrent identical order numbers is not behavioral evidence for a production repository backed by a unique database constraint.

## Learning Objectives

After this module, learners can:

1. distinguish Repository from DAO, mapper, ORM, service and query object;
2. design repository ownership and method vocabulary around aggregate roots/use cases;
3. specify identity, absence, ordering, page, loading and consistency contracts;
4. place authorization and tenant constraints inside repository predicates/transactions;
5. coordinate repositories with Unit of Work, Identity Map and outbox;
6. translate uniqueness/version/storage failures into stable application outcomes;
7. prevent generic CRUD, unbounded-query and persistence-leak abstractions;
8. decide when CQRS/read queries or direct ORM/gateway access are clearer;
9. build contract tests that expose fake/production semantic gaps;
10. review performance, security and evolution evidence for a repository boundary.

## Core Exposition

### Start from the pattern's intent

Fowler describes Repository as mediating between domain and mapping layers with a collection-like interface. Evans places repositories around aggregate roots, supplying the illusion of an in-memory collection so domain design remains focused. Three forces matter:

1. the domain model should not own database/mapping concerns;
2. clients need reusable domain-oriented selection and persistence operations;
3. infrastructure details must implement—not dictate—the domain/application contract.

This does not require every method to look literally like a collection. `of_id`, `add`, `remove`, and `matching(spec)` fit the original form; `orders_ready_to_dispatch(limit)` may better state a bounded use case. The crucial property is domain meaning and explicit semantics.

Do not begin by generating interfaces for every table. Identify aggregate roots that have identity/lifecycle/invariants and actual retrieval needs. Value objects inside an aggregate do not receive independent repositories merely because they occupy tables. Cross-aggregate reporting is usually not aggregate retrieval.

### Establish dependency ownership

The interface lives with the client policy—domain or application layer—using domain/application types. Infrastructure implements it with SQL/ORM/document/event storage. This keeps dependencies pointing inward:

\[
application/domain \leftarrow repository\ interface \leftarrow infrastructure\ implementation.
\]

Do not leak `DbContext`, SQL fragments, ORM `Query`, vendor cursor, database row or HTTP response through the interface. Those make the client depend outward and complicate replacement/testing. Conversely, do not erase capabilities that affect the domain: expected version, consistency requirement, bounded page and lock/lease intent may belong in the contract.

Repository implementations may collaborate with Data Mappers, Unit of Work and Identity Map. Some ORMs already implement repository/unit-of-work-like mechanics. Adding `GenericRepository<T>` that simply forwards every ORM method introduces no domain boundary and can remove useful features/type safety. Add a Repository where it owns domain selection/invariant/persistence semantics.

### Design around aggregate roots

Aggregate roots define transaction consistency boundaries. A repository returns/persists the root; internal entities are reached through root behavior. If clients independently load and mutate line items, they can bypass order invariants.

A common interface has:

- `of_id(scope, id)` with explicit absence/concealment;
- `add(root)` for new aggregate identity/uniqueness;
- `remove(root, expected_version)` only if deletion is a domain operation;
- domain-specific selection/specification methods;
- perhaps no `save` when Unit of Work tracks changes; or explicit `save(root, expected_version)` in persistence styles without tracking.

Avoid a universal base interface forcing meaningless `delete`, unbounded `all`, partial update or arbitrary filter on every aggregate. Shared implementation helpers can reduce plumbing without making a public lowest-common-denominator contract.

Method names should answer why callers retrieve data. `by_customer_with_open_balance` is more stable than `findByCustomerIdAndStatusAndBalanceGreaterThan`. A Specification can compose domain predicates, but only publish supported specifications and translation rules; accepting arbitrary language lambdas creates an impossible portability promise.

### Make query semantics explicit

Every selection operation defines:

- authorized population/tenant scope;
- whether absent and forbidden are concealed/distinguished;
- maximum count/page size and continuation/cursor contract;
- deterministic ordering/tie-breaker;
- consistency/snapshot/staleness;
- aggregate loading depth and lazy-loading policy;
- duplicates and identity-map behavior;
- cancellation/deadline and resource cost where relevant.

`find_all()` hides unbounded memory/database work. `find_by(predicate)` suggests any in-memory predicate can be translated and efficiently indexed. `get(id)` may conceal whether it hits a cache, replica or primary and whether returned data is current enough for mutation. Put correctness-relevant choices in the contract while keeping vendor syntax internal.

For mutation, load from a consistency source that supports versioned write. A stale replica read followed by primary last-write can lose updates. Reporting/search can tolerate stale projections if declared; do not return partial projections masquerading as fully invariant-capable aggregates.

### Authorization belongs in the data operation

A service that first asks `authorize(user, order_id)` then calls `repository.of_id(order_id)` creates duplicated lookup and time-of-check/time-of-use gaps. Worse, unconstrained lookup may reveal existence through timing/error differences before authorization.

Pass an immutable authorized scope/principal/tenant policy and constrain the storage predicate:

\[
WHERE\ id=?\ AND\ tenant=?\ AND\ permitted\_relationship(...).
\]

Under concealment policy, foreign and absent resources both produce `NotFound`. Some use cases deliberately distinguish `Forbidden`, but the policy must be explicit and side channels tested. Mutation predicates include authorization-relevant ownership and expected version in the same transaction/conditional write when authority can change.

Do not make Repository the sole authorization owner. Application policy decides required permission; repository capability enforces data-scoped predicate. Infrastructure must not infer current user from ambient global context, which harms testability and can leak across asynchronous work.

### Coordinate Unit of Work and transactions

Repository methods do not necessarily define transaction boundaries. An application use case may load two aggregates, reserve uniqueness, mutate one, write audit/outbox and commit atomically. A Unit of Work owned by the application coordinates participating repositories/mappers.

If every `save` commits immediately, multi-operation invariants and outbox atomicity fail. If Repository hides a long transaction behind an iterator, locks/resources may outlive expectations. State whether calls join an existing unit, start their own short transaction, or are read-only snapshots.

One database transaction cannot generally span independently owned services/stores. Do not label a distributed workflow “Repository transaction.” Use saga/outbox/idempotent boundaries. A repository for one aggregate should not make network calls to assemble a distributed aggregate illusion.

Unit of Work may flush tracked changes; explicit-save architectures can be equally valid. Avoid mixing semantics where some mutations auto-persist and others require save. Tests must show rollback, commit visibility and outbox/audit coupling.

### Identity Map and object identity

Within one unit of work, loading the same aggregate twice should normally return the same in-memory logical instance or merge consistently. Otherwise two copies at version 7 can be independently changed and one overwrites the other. An Identity Map keyed by aggregate type/tenant/id maintains identity.

Across transactions, object instance identity is meaningless; use stable domain ID and version. Do not cache mutable aggregates globally without invalidation/concurrency semantics. A Repository-level cache is observable: staleness, negative caching, authorization scope, transaction interaction and eviction must be specified.

No-tracking reads may materialize copies for performance. Such objects should be immutable/read-model values or clearly not used for mutation. Lazy-loading proxies leak session lifetime and can trigger N+1 calls from domain behavior/serialization; prefer explicit aggregate loading shape.

### Concurrency and error translation

Use expected version/ETag/generation or an atomic domain predicate:

\[
UPDATE\ orders\ SET\ldots,version=8\ WHERE\ id=?\ AND\ tenant=?\ AND\ version=7.
\]

Zero affected rows could mean absent, unauthorized or version conflict; resolve according to the contract without leaking more than policy permits. A database constraint violation maps to `DuplicateOrderNumber`/`UniquenessConflict` if that constraint has domain meaning. Connection timeout/deadlock maps to a retryable infrastructure/application category, not an HTTP response.

Do not parse vendor error strings in handlers. Repository/Data Mapper infrastructure knows stable constraint codes and maps once; application decides retry/terminal outcome; transport adapter maps to HTTP/RPC. Preserve cause for telemetry without exposing secrets.

Last-write-wins can be intentional for low-risk preferences, but name it. Pessimistic locks may support short local critical sections; exposing `lockForUpdate()` widely couples clients to one storage model. Prefer intent such as `claim_next_job(owner, generation)` when locking/lease semantics are domain/application behavior.

### Queries, CQRS and read models

Repositories reconstruct aggregates for behavior. Read screens/reports often need joins, counts, denormalized fields and paging that do not require aggregates. Forcing every query through aggregate repositories creates overfetch, N+1, memory costs and leaky “include” flags.

Use a query service/read-model gateway returning DTOs for those cases. CQRS can be lightweight: command side uses aggregate Repository; query side executes optimized read projections. This is not permission to duplicate business rules or bypass authorization. Read contracts still specify consistency, scope, order, paging and schema.

Specifications help reusable domain predicates where translation is feasible. Query objects own complex query parameters/results. A Repository should not become a universal analytics API. Its interface remains cohesive around aggregate lifecycle.

### Deterministic tenant/version repository model

The following in-memory model demonstrates tenant-scoped selection, stable ordering and optimistic version conflict. It is a semantic illustration, not a storage implementation.

<!-- bijux-verify: {"id":"sepat-091-repository-contract","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"tenant-a-open=o-1,o-3\nversion-conflict=o-1:expected-1:actual-2\ntenant-b-visible=o-2\ntenant-a-visible=o-1,o-3\n","stderr":""}} -->
```python
rows = {
    "o-1": {"tenant": "tenant-a", "state": "open", "version": 2},
    "o-2": {"tenant": "tenant-b", "state": "open", "version": 1},
    "o-3": {"tenant": "tenant-a", "state": "open", "version": 4},
}

def visible_ids(tenant, state=None):
    matches = []
    for order_id, row in rows.items():
        if row["tenant"] == tenant and (state is None or row["state"] == state):
            matches.append(order_id)
    return sorted(matches)


def check_version(tenant, order_id, expected):
    row = rows.get(order_id)
    if row is None or row["tenant"] != tenant:
        return "not-found"
    if row["version"] != expected:
        return order_id + ":expected-" + str(expected) + ":actual-" + str(row["version"])
    return "accepted"


print("tenant-a-open=" + ",".join(visible_ids("tenant-a", "open")))
print("version-conflict=" + check_version("tenant-a", "o-1", 1))
print("tenant-b-visible=" + ",".join(visible_ids("tenant-b")))
print("tenant-a-visible=" + ",".join(visible_ids("tenant-a")))
```

This execution proves exact dictionary filtering, sort and version-branch behavior for fixed inputs. It has no database, transaction, concurrency, isolation, authorization proof, paging, mapper, identity map, unit of work, failure, latency, cache or durable effect.

### Testing the boundary

Write implementation-independent contract tests and run them against the production adapter and any fake:

- add/get/remove lifecycle and stable ID;
- absent versus forbidden concealment and tenant predicates;
- unique constraint and conflicting fingerprint/input;
- optimistic version success/conflict under concurrent writers;
- deterministic order, page boundary, cursor stability and maximum size;
- transaction rollback/commit visibility and multi-repository unit;
- identity-map repeated load and loading shape/no lazy N+1;
- domain/storage mapping round-trip including value types/time/precision;
- errors, cancellation/deadline and connection/deadlock recovery;
- outbox/audit atomicity and restore/migration compatibility.

An in-memory fake often cannot reproduce isolation, SQL collation, precision, constraint timing, lazy loading or transaction abort. Use it for fast application tests only if limitations are known; integration tests against the real engine are completion evidence. Prefer a behaviorally small fake over emulating a database badly.

Performance tests verify query plans/indexes and bounded result size with representative data/skew. Observability records repository operation—not raw sensitive SQL by default—duration, rows/bytes, page size, consistency source, cache, conflict/absence/error and transaction ID, with bounded labels.

### Evolution and pattern removal

Repository contracts evolve with domain language. Adding arbitrary methods endlessly signals multiple responsibilities. Split by aggregate/bounded context or extract query services. Changing aggregate boundary may require data migration and staged adapters; do not expose storage schema as the stable API.

A switch from SQL to document/event storage is not automatically easy. Re-evaluate atomicity, consistency, query, version and migration semantics. Preserve the contract only where both implementations truly satisfy it; otherwise change the application design explicitly.

Remove Repository when it provides no domain vocabulary or policy, merely duplicates an ORM API, and makes advanced queries/transactions harder. Direct ORM use inside a well-owned infrastructure/application boundary can be clearer. Patterns are justified by forces and evidence, not layer count.

## Definitions and Notation

Let aggregate type be \(A\), root identity \(id\), tenant/authorization scope \(\sigma\), version \(v\), Repository \(R_A\), Specification \(s:A\to\{true,false\}\), Unit of Work \(U\), Identity Map \(M_U[(A,\sigma,id)]\), ordered bounded page \(P=(items,cursor,snapshot)\), and conditional mutation \(write(id,\sigma,v\to v+1)\).

The collection metaphor is observational: clients express domain selection/mutation without mapping syntax. It does not imply in-memory complexity, infinite enumeration, local failure semantics, one consistency model or arbitrary predicate translation.

## Mechanisms, Invariants, or Proof Structure

**Dependency direction.** Domain/application owns \(R_A\); infrastructure implements it. If vendor types escape, the intended one-way dependency fails.

**Aggregate safety.** Repository mutation exposes roots; root behavior and one local transaction preserve internal invariant assumptions. Independent child repositories bypass the boundary.

**Authorization safety.** Constraining ID and scope in one storage predicate prevents returning a foreign row before authorization. Separate pre-checks admit races/disclosure.

**Concurrency safety.** Conditional `version=v` update lets at most one conflicting writer advance from v under adequate local transaction isolation. Zero-match interpretation remains policy-sensitive.

**Identity consistency.** Identity Map returns one logical instance per `(type,scope,id)` within U. Without it, conflicting copies can diverge before flush.

**Bounded query.** Deterministic order plus maximum page and stable cursor/snapshot bounds resource/result semantics. A page contract cannot guarantee cheap execution without indexes/plan evidence.

**Test substitution.** A fake is substitutable only for properties it shares with production. Passing application tests over weaker semantics cannot prove production constraints/concurrency.

## Alternatives and Trade-Offs

| Alternative | Prefer when | Limitation relative to Repository |
|---|---|---|
| direct ORM in application boundary | domain is simple and ORM semantics are acceptable | persistence concerns/types can spread |
| Active Record | record-centric CRUD with modest domain logic | domain object couples persistence and model |
| DAO/table gateway | storage/table operations and records are the useful boundary | weaker aggregate/domain collection vocabulary |
| Data Mapper only | mapping isolation is enough and queries are few | query construction may duplicate across clients |
| domain Repository | rich aggregate behavior and reusable domain selection | design/mapping/testing/transaction complexity |
| query service/read model | optimized reporting/search/page DTOs | not aggregate behavior/mutation boundary |
| Specification | reusable composable domain predicate is translatable | translation/performance capability limits |
| event-sourced repository | event stream is authoritative aggregate history | replay/evolution/snapshot/consistency burden |
| external service gateway/port | data/effects are owned by another service | collection illusion and transaction control are false |

## Failure Modes and Misconceptions

- **Repository means any database wrapper.** Its distinctive intent is domain collection/mapping mediation.
- **One repository per table.** Aggregate roots, not storage layout, define the domain boundary.
- **Generic CRUD maximizes reuse.** It erases use-case semantics and permits invalid operations.
- **Persistence independence means any store swaps freely.** Consistency/query/transaction capabilities differ.
- **The repository owns every transaction.** Application Unit of Work often owns use-case atomicity.
- **Authorization can happen before lookup.** Unconstrained later access can leak/race.
- **`find_all` is collection-like elegance.** It is an unbounded production contract.
- **Arbitrary lambdas are specifications.** Most cannot be translated/indexed portably.
- **Returning ORM entities is harmless.** Tracking/proxy/session/vendor semantics leak.
- **Lazy loading is transparent.** It changes I/O, failure and complexity during domain/serialization access.
- **A fake list proves the repository.** It rarely models constraints, isolation or mapping.
- **Mocking every call improves tests.** It often tests implementation choreography, not the contract.
- **Repository is mandatory in DDD.** Use it where aggregate retrieval/persistence forces justify it.
- **Read reports should load aggregates.** Query projections are often safer and cheaper.
- **External APIs are repositories.** They are gateways/ports with remote ownership and failure semantics.

## Worked Examples

### Example 1

`GenericRepository<Order>.getAll()` is used for a monthly report and loads two million aggregates with lines. A query service instead returns a bounded projection streamed/page-wise from indexed aggregation. Repository remains focused on behavioral aggregate retrieval. The pattern boundary follows purpose, not uniform API aesthetics.

### Example 2

Order lines have their own repository because they have a table. A caller deletes a line without rechecking minimum-order/price invariants. Removing that repository and mutating through `Order` root restores aggregate control; mapping still persists line rows internally.

### Example 3

An authorization service confirms user can view order `o-1`, then ownership changes before unconstrained repository lookup. The result leaks. `of_id(authorized_scope,o-1)` constrains tenant/relationship in the query; concealment returns not found for absent/foreign rows.

### Example 4

Two units load order version 7. Both update. `save(order)` last-write-wins loses one change. `save(order,expected=7)` uses conditional update; one advances to 8, the other gets `VersionConflict`, reloads and applies domain conflict policy. Repository translates database row-count/constraint evidence.

### Example 5

A fake stores orders in a dictionary and allows case-sensitive duplicate order numbers; production collation/unique constraint rejects them. Shared contract tests expose the difference. The fake either implements the declared normalization/uniqueness or stops being evidence for that behavior; real-engine integration remains required.

### Example 6

Serializing an aggregate traverses lazy `lines`, issuing one query per order after the request's transaction closed. The repository exposes an explicit loading contract for the aggregate use case; read endpoint uses a DTO query. Metrics/test query counts catch N+1 rather than calling lazy I/O transparent.

### Example 7

An application saves order, commits, then inserts outbox through another repository transaction. Crash loses publication. One application Unit of Work coordinates aggregate mapping and outbox insertion atomically; repository methods join it and do not auto-commit.

### Example 8

A universal `find(predicate)` accepts language lambdas. An in-memory implementation handles any function; SQL cannot translate a domain method and falls back to client evaluation. The contract is narrowed to named specifications/query objects with explicit indexed translation and bounded results.

### Example 9

A team wraps an ORM's set/session with identical add/find/save methods, adding mapping files and mocks but no domain semantics. Advanced queries require escape hatches. They remove the wrapper, keep ORM confined to infrastructure/application boundary, and add focused repositories only for aggregates with reusable domain retrieval/concurrency rules.

### Example 10

A medical record repository returns “not found” for foreign records but logs raw identifiers and caches negative results across tenants. The data predicate is tenant/relationship constrained, cache keys include authorization scope, telemetry is minimized, and emergency-access paths are distinct/audited. Named privacy, clinical, security and legal reviewers verify concealment/break-glass policy; unit tests alone do not establish compliance.

## Cross-Program Connections

- [Software Design and Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md): aggregate roots, domain language and bounded contexts define repository ownership.
- [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md): dependency direction, ports/adapters, transaction boundaries and CQRS separation.
- [Software Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md): fake/adapter contract tests, real-engine integration and concurrency evidence.
- [Database Engineering](../../18-database-engineering/ROADMAP.md): transactions, isolation, constraints, indexes, plans, mapping and pagination.
- [Security Engineering](../../25-security-engineering/ROADMAP.md): authorization predicates, tenant isolation, side channels, caches and audit privacy.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md): DTO/error/pagination translation without leaking aggregates or storage types.

## References

1. Hieatt, Edward, and Rob Mee. “Repository.” In Fowler, *Patterns of Enterprise Application Architecture*. <https://martinfowler.com/eaaCatalog/repository.html>
2. Fowler, Martin. *Patterns of Enterprise Application Architecture*. Addison-Wesley, 2003.
3. Evans, Eric. *Domain-Driven Design: Tackling Complexity in the Heart of Software*. Addison-Wesley, 2004.
4. Evans, Eric. “Domain-Driven Design Reference: Definitions and Pattern Summaries.” 2015. <https://www.domainlanguage.com/ddd/reference/>
5. Fowler, Martin. “Data Mapper.” <https://martinfowler.com/eaaCatalog/dataMapper.html>
6. Fowler, Martin. “Unit of Work.” <https://martinfowler.com/eaaCatalog/unitOfWork.html>
7. Fowler, Martin. “Identity Map.” <https://martinfowler.com/eaaCatalog/identityMap.html>
8. Evans, Eric, and Martin Fowler. “Specifications.” <https://martinfowler.com/apsupp/spec.pdf>
9. Vernon, Vaughn. *Implementing Domain-Driven Design*. Addison-Wesley, 2013.
10. Microsoft. “Design the Infrastructure Persistence Layer.” *.NET Microservices Architecture*. <https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/infrastructure-persistence-layer-design>
11. Cockburn, Alistair. “Hexagonal Architecture.” 2005. <https://alistair.cockburn.us/hexagonal-architecture/>
12. Gamma, Erich, et al. *Design Patterns*. Addison-Wesley, 1994.

The official Fowler/Evans pattern material and current Microsoft implementation guidance were checked on 2026-08-29. ORM tracking, query translation, transaction, lock, concurrency and error behavior are provider/version/configuration specific and require deployed-adapter verification.

## Exercises

### Exercise 1

Design a Repository contract for an Order aggregate: identity, authorized lookup, add/save, version conflict, bounded selection, loading shape and transaction ownership.

### Exercise 2

Trace two concurrent writers loading version 5 and saving different changes. Show the conditional-write outcomes and application choices after conflict.

### Exercise 3

Diagnose a generic repository that exposes ORM queries/entities, supports `all`, commits every method, authorizes before lookup, lazy-loads lines and is tested only with mocks. Redesign and specify evidence.

### Exercise 4

Decide which of these belong in aggregate Repository versus query service: load order for cancellation; dashboard revenue by region; search orders by free text; claim next job; export one million invoices; save order plus outbox.

### Exercise 5

Design a repository boundary for multi-tenant regulated records, including concealment, break-glass access, versioning, audit/outbox, caching, migration, tests and named review.

## Answers to the Exercises

### Answer 1

Own `OrderRepository` beside domain/application types; infrastructure implements it. Provide `of_id(scope,order_id,load_shape)` returning root or policy-defined not-found; `add(order)` participating in current Unit of Work; `save(order,expected_version)` or tracked flush with explicit conflict; and a few named bounded selectors such as `ready_to_dispatch(scope,page)` with maximum, deterministic `(ready_at,id)` order, stable cursor/snapshot and defined consistency. Lines are internal to root, not separate repository.

Application service owns transaction: authorize intent, construct immutable scope, load/mutate root, save/flush and insert outbox/audit in one unit. Repository constrains tenant/relationship and version in data predicates. Map unique/version/not-found/transient storage failures to stable application categories. State no lazy loading, identity-map behavior within unit, and which source supports mutation. Contract plus real-adapter tests cover mapping, constraints, conflicts, paging, rollback and query count.

### Answer 2

Both load `(id,version=5)`. Writer A conditionally updates `WHERE id=? AND version=5`, changes state and sets version 6; one row changes, commit succeeds. Writer B's identical version predicate changes zero rows after A commits. It must not silently overwrite.

Repository returns `VersionConflict` (subject to absence/concealment resolution). Application may reload version 6, re-evaluate command/invariants and merge/retry under a bounded policy; reject conflict to caller; or apply an explicitly commutative operation. It preserves original idempotency/effect identity. A fake must model this arbitration or cannot validate concurrency behavior. Pessimistic local locking is an alternative if short contention/availability trade-offs justify it.

### Answer 3

ORM query/entity leakage reverses dependency and exposes tracking/session/vendor behavior. `all` is unbounded. Per-method commits break use-case atomicity/outbox. Pre-authorization plus unconstrained lookup leaks/races. Lazy lines cause hidden I/O/N+1/session failure. Mock-only tests assert choreography without mapping/constraints/isolation.

Define focused aggregate-root repository owned inward with domain methods/named specifications, bounded ordered pages, explicit loading, authorized tenant predicates, expected versions and stable error categories. Application Unit of Work coordinates calls/commit/outbox. Reporting/search uses DTO query services; ORM stays in adapter. Test shared contract against fake and real engine, plus concurrent conflicts, constraints/collation/precision, transaction rollback, identity map, no lazy loads/query counts, paging/cursors, tenant concealment and fault mapping.

### Answer 4

Load order for cancellation belongs in Order Repository because it reconstructs an aggregate for behavior/versioned mutation. Dashboard revenue, free-text search and million-row export are read/query-service contracts returning bounded/streamed DTOs; loading aggregates would overfetch and imply behavior unnecessarily.

`claim_next_job` can be a repository/application persistence capability if Job is an aggregate and claim/version/lease is domain behavior; its atomic selection/lock/fencing semantics must be explicit rather than a generic query. Saving order plus outbox is coordinated by the application Unit of Work: Order Repository maps/persists the root while an outbox collaborator inserts intent in the same local transaction. One repository need not own messaging semantics, but per-method auto-commit is forbidden.

### Answer 5

Repository operations take immutable authenticated tenant/relationship scope; queries/mutations constrain scope, record ID and expected version atomically. Conceal foreign/absent under normal policy with timing/error tests. Break-glass is a distinct authorized use case requiring reason, short-lived authority, dual control where required and immutable audit—not a flag hidden in generic lookup. Cache keys include tenant/authorization/version; sensitive negative caching and invalidation are bounded.

Application Unit of Work couples record mutation, audit and outbox. Mapper encrypts/minimizes classified fields and preserves precision. Migrations use dual-compatible readers/writers or staged backfills with invariant/reconciliation evidence; repository contract changes only when domain semantics change. Tests cover tenant attacks, authority revocation races, conflicts, rollback, cache leakage, mapping/encryption, failover/restore and audit/outbox atomicity against real storage.

Named domain/clinical, privacy, security, legal/compliance, database and operations reviewers approve concealment, break-glass, retention, audit and migration evidence. Automated repository tests prove implemented mechanics in tested conditions, not legal/clinical adequacy.
