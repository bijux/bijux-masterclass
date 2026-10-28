---
module_id: SEPAT-058
program: Software Engineering: Patterns
level: 2
module_number: 58
title: Active Record
status: complete
last_verified: 2026-08-29
---

# Active Record

## One-Page Review

### Governing question

When is it advantageous for one object to wrap one row, encapsulate its persistence, and own row-centered domain behavior—and how can that convenience remain correct under transactions, concurrency, associations, callbacks, bulk operations, authorization, schema evolution, and growing domain complexity?

### Essential definitions

- An **Active Record** is an object that wraps a row in a database table or view, encapsulates database access, and adds domain logic over that data.
- A **row-centered invariant** can be decided and enforced mostly from one record plus explicit evidence/constraints.
- A **finder/query scope** is a class/relation operation that locates records under explicit predicates such as tenant, status, and authorization.
- **persistence lifecycle** includes new/loaded/dirty/saved/deleted/detached-like states and framework callbacks around them.
- **validation** produces application-readable rejection before persistence; a **database constraint** protects representable data rules against every writer and races.
- **optimistic locking** includes a loaded version in an atomic update/delete predicate and rejects stale writes.
- **mass assignment** copies a field map onto a record; it is unsafe when fields are not explicitly allowlisted per use case.
- A **callback** is logic invoked at lifecycle points such as validation, save, commit, or rollback; its timing and transaction semantics are part of the contract.
- A **scope/query object** composes safe relational predicates; it is not continuing authorization merely because it filters rows.
- A **Data Mapper** separates persistence from domain objects and becomes attractive when model/schema complexity diverge.

### Central model, mechanism, or theorem

For record state $a=(k,v,p)$—scoped key $k$, version $v$, persistent fields $p$—and domain command $c$ with trusted context $x$, an Active Record method computes valid candidate $p'=f(p,c,x)$ or rejection, then performs a guarded write:

$$
\mathrm{UPDATE}\;p',v+1\;\mathrm{WHERE}\;k\land v
\rightarrow
\begin{cases}
1,&\text{committed candidate},\\
0,&\text{stale/missing under scope}.
\end{cases}
$$

Correctness requires validation/domain rules, database constraints, tenant/action authorization, a real transaction, and post-failure object-state policy. Combining data and persistence in one class supplies none of these automatically.

### Critical invariants

- Active Record is chosen for cohesive row-centered behavior; rich cross-object rules are not scattered among callback chains and finders.
- Every finder/update/delete is tenant-scoped and parameterized; action authorization is server-derived and checked near mutation.
- Public methods name domain actions (`approve`, `cancel`, `change_address`), not unrestricted generic field writes.
- Required, unique, range, reference, lifecycle, and version rules are backed by appropriate database constraints/guarded statements where representable.
- An application operation owns one transaction across all related records, idempotency, audit, and outbox; individual `save` calls do not create accidental partial commits.
- Expected versions detect stale writes; conflict, invalid, denied, not found, constraint failure, and infrastructure failure remain distinct.
- Callbacks are deterministic, bounded, and local to their stated transaction phase; external effects use durable outbox/workflow rather than fragile callbacks.
- Associations have explicit ownership, cascade, ordering, loading, query-count, and deletion semantics.
- Bulk/native methods that bypass validations/callbacks/versions are isolated and governed explicitly.
- Tests exercise actual database constraints, transactions, locks/versions, callbacks, queries, tenant security, migrations, and query plans.

### Common failures

Common failures include Fat Active Record god models, one record per table mistaken for a rich domain, business logic in controllers/jobs instead, generic `update(fields)`, mass assignment of tenant/role/status/price, unscoped `find(id)`, validation without constraints, callback recursion/order dependence, network/email in save callbacks, after-commit treated as durable delivery, implicit transaction per `save`, partial multi-record operations, stale last-write-wins, cascade over-delete, N+1 association traversal, default-scope surprises, hidden lazy I/O, bulk update bypass, soft-delete inconsistencies, STI discriminator drift, fixtures/mocks unlike real database behavior, and retaining the pattern after rules outgrow row boundaries.

### Compact example

An `InvoiceRecord` wraps a tenant-scoped in-memory row. `approve` checks manager authority and pending state, performs a version-2 guarded save, and advances row/object to approved/version 3. A detached version-2 record conflicts and restores its local pre-attempt state; an unauthorized attempt produces no write.

### Connections

[SEPAT-057](057-data-mapper.md) provides the persistence-separated alternative; [SEPAT-059](../ROADMAP.md) develops Lazy Load. Active Record connects to [Database Engineering](../../18-database-engineering/ROADMAP.md), [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md), and [Security Engineering](../../25-security-engineering/ROADMAP.md).

## Governing Question

When do row identity, persistence access, and domain behavior form one cohesive abstraction, and what transaction, concurrency, security, query, callback, and evolution boundaries keep that abstraction from becoming a convenient source of hidden coupling?

Active Record is not synonymous with every ORM or with an anemic generated model. Its object combines one record's persistent data, access operations, and meaningful domain behavior. It is often the clearest pattern for simple business logic closely aligned to rows.

## Why This Matters

For CRUD-heavy applications and row-local rules, a separate mapper/repository/domain-object stack can add more indirection than value. Active Record makes discovery and mutation direct: find the invoice, ask it to approve, save under a transaction.

That directness couples object shape and lifecycle to persistence. As rules span several records, services, temporal histories, or alternative stores, callbacks and associations can hide essential behavior. The right question is not whether Active Record is “enterprise enough,” but whether its row-centered ownership keeps changes and guarantees clear.

Framework productivity can obscure real database semantics. Validation races, callback timing, per-call transactions, bulk bypasses, query explosions, and stale instances occur beneath concise methods. Production-grade use makes them explicit.

## Prerequisites and Retrieval

You should understand objects, relational schemas/keys/constraints, transactions/isolation, optimistic locking, authorization, SQL injection, associations, callbacks, Unit of Work, Data Mapper, outbox, and migrations. Retrieve these facts:

1. Application validation before an insert/update can race; a unique/check/reference constraint is authoritative for representable data integrity.
2. Several individually successful saves are not one atomic use case unless enclosed in one transaction.
3. An object instance is not a database lock and another process can update the row.
4. After-commit code runs after database state is committed; its failure cannot roll the transaction back.
5. Loading an association in a loop may issue one query per record.
6. Bulk SQL often bypasses object validation, callbacks, dirty tracking, and optimistic versions.
7. Authentication does not authorize every record/action, and numeric IDs are guessable.

## Learning Objectives

After completing this module, you should be able to:

- distinguish Active Record from Data Mapper, Row Data Gateway, Transaction Script, Table Module, and Domain Model;
- decide whether domain behavior is sufficiently row-centered for the pattern;
- design domain-named record APIs, scoped finders, validations, constraints, and typed outcomes;
- establish transaction ownership across several Active Records without hidden partial commits;
- implement optimistic/pessimistic concurrency and recover object state after failure;
- use associations, scopes, eager/lazy loading, batching, and projections without query or cardinality traps;
- govern callbacks, outbox, idempotency, bulk/native operations, soft deletion, and audit;
- prevent mass assignment, cross-tenant access, SQL injection, over-disclosure, and authorization bypass;
- evolve schema and extract richer domain/persistence boundaries incrementally;
- verify behavior using the real framework, driver, database, concurrency, faults, and representative data.

## Core Exposition

### Choose Active Record by behavior shape

It fits when one record is the natural identity/lifecycle unit, rules are mostly row-local, associations are modest, schema and model change together, and persistence convenience outweighs independence. Examples include content pages, simple invoices, configuration entries, catalog records, and administrative workflows.

It strains when invariants span large graphs, calculations compose many values/policies, one domain concept spans several storage shapes, multiple persistence technologies are plausible, or object behavior must run without database/framework infrastructure.

### Keep row wrapping explicit

One instance represents one row/view identity. Class/relation methods find/query; instance methods change/delete itself. Values can still be rich types; the record need not expose raw primitives for money/time.

Do not pretend a joined report row is a mutable entity. Use immutable projections for reports/aggregates, and Table Module/set SQL for bulk rules.

### Name domain actions

Expose `invoice.approve(actor, policy)` rather than `invoice.update(status: "approved")`. The action validates current lifecycle, domain evidence, and intended transition. Restrict direct writers for protected fields.

Simple attribute editing is appropriate for genuinely descriptive data, but transport parameters still map through use-case allowlists. Generated `save` APIs are persistence mechanisms, not the whole domain API.

### Separate trusted context from record fields

Actor, tenant, authority, request/idempotency, authoritative time, policy, and deadline come from server-side context, not client-mutable columns/parameters. A record's `owner_id` does not prove the current actor owns it.

Avoid global/current-user ambient state inside model methods when it hides premises or leaks across jobs/tasks. Pass minimal trusted evidence or authorize in a Service Layer immediately before the action.

### Scope every lookup

Use tenant/organization and disclosure predicates from trusted context: `tenant.invoices.find(id)`, not global `Invoice.find(id)` followed by a hopeful check. Default scopes can be bypassed or surprise administrative/association queries; make critical tenant scope structural and tested.

Differentiate not found and denied according to disclosure policy. Database row-level security and least-privilege roles can add defense in depth but require integration tests.

### Validate for people, constrain for data

Record validations provide immediate field/domain errors and can depend on object behavior. Database `NOT NULL`, check, unique, foreign/exclusion constraints protect every writer and concurrency. Use both for important representable invariants.

Map named constraint violations to typed results without parsing localized prose. Never rely on `validates_uniqueness`-style precheck alone. Cross-record/external rules may require guarded SQL, locks, or domain/workflow policy.

### Own transactions above individual records

One record save may open/participate in a transaction, but use cases updating invoice, ledger, idempotency, audit, and outbox need one explicit application transaction. The Service Layer/operation owns it; record methods must not commit independently.

Keep remote calls and user think time outside locks. Nested transaction APIs may use savepoints rather than independent commits; know the framework semantics.

### Implement optimistic locking

Load version $v$; update/delete with tenant/key/version predicate; increment version; require one affected row. Framework lock columns help only when all write paths honor them. Bulk/native updates, direct SQL, imports, and callbacks must preserve version policy.

On stale error, roll back, expire/reload, and re-run the domain decision or return conflict. Never copy current version onto stale fields and retry blindly.

### Use pessimistic locks for the actual invariant

Row locks can serialize hot record decisions; stable lock order reduces deadlocks. They do not automatically protect absent rows, arbitrary predicates, or external systems. Constraints, advisory/predicate locks, or serializable transactions may be needed.

Bound lock time, propagate deadline, classify deadlock/timeout, and retry only a whole safe transaction with fresh instances.

### Understand object state after failure

If a record mutates in memory before a guarded write fails, the object can now claim a state not committed. Restore known pre-state, expire/reload, or discard the transaction/context. Framework rollback policies vary.

Do not return or publish an object as saved after validation/constraint/version/commit failure. Generated IDs/versions/callback flags/events also need cleanup semantics.

### Treat associations as query and ownership design

Declare cardinality, optionality, inverse, ownership, cascade, dependent deletion, ordering, uniqueness, and loading. A `has_many`-style declaration does not prove aggregate ownership or safe cascade.

Avoid broad bidirectional navigation. Cross-aggregate references can remain IDs/query services. Review delete behavior against foreign keys and soft-deletion policy.

### Prevent N+1 and join explosion

Lazy associations are convenient until a loop issues N queries. Preload/batch when the use case needs related data; count/assert statements. Eager joins can multiply parent/child rows, memory, and pagination semantics.

Page stable root IDs/records, then load associations. Use projections/set queries for dashboards and aggregates rather than hydrating thousands of Active Records.

### Use scopes as composable queries, not policy alone

Named scopes express reusable predicates such as overdue, active, tenant-owned. Keep them side-effect-free and test combination/order/null semantics. Unbounded chainable query APIs can expose expensive or sensitive fields.

Authorization still evaluates actor-resource-action and possibly current record state. A filtered collection is useful enforcement but not sufficient if other find paths exist.

### Bound callbacks

Callbacks suit local invariant normalization, derived values, and persistence bookkeeping when ordering is explicit. Too many callbacks create invisible control flow, recursion, conditional skipping, and tests coupled to lifecycle magic.

Prefer direct domain methods/application orchestration for meaningful business transitions. Document which APIs bypass callbacks and avoid calling `save` recursively inside callbacks.

### Distinguish callback transaction phases

Before/after-save callbacks may run within the transaction and can abort it; after-commit runs once commit has already succeeded and cannot undo it. Callback ordering and behavior for multiple instances of one row can be framework-specific.

Do not perform email/payment/broker calls in precommit callbacks. After-commit avoids publishing uncommitted facts but can still crash and lose delivery. Store an outbox record transactionally and relay idempotently.

### Implement idempotent commands

Retrying `record.approve` after response loss can duplicate audit/messages even if status is already approved. Scope request identity by tenant/operation, bind digest, and store outcome plus state/outbox in one transaction.

An “already approved” domain result is not necessarily the same request duplicate. Preserve distinctions for audit and clients.

### Govern mass assignment

Never pass request maps directly to record constructors/update. Define per-use-case permitted fields and derive protected tenant, ownership, price, role, status, version, audit, and generated fields server-side. Nested assignment expands blast radius and cascade risk.

Type coercion and validation do not authorize fields. Test unexpected, duplicated, encoded, and nested parameters.

### Parameterize queries

Use framework binding for values. Dynamic columns, directions, operators, joins, and raw fragments must come from a closed server-side map. Avoid string interpolation even in scopes/admin tools.

Limit filters, joins, sort, page size, and time. An ORM API can still produce injection or denial-of-service when raw fragments/arbitrary query shapes are exposed.

### Handle deletion and retention

Hard delete, soft delete, archive, and redaction have different semantics. Soft-delete default scope can hide rows from uniqueness, associations, audit, or admin paths while they still exist. Include deletion state/generation in constraints and authorization.

Define cascade, legal hold, restoration, identifier reuse, events, and cache invalidation. High-value histories often use state transition or append-only correction instead of destroy.

### Treat inheritance cautiously

Single-table inheritance is common but couples discriminator/type names, leaves nullable subtype columns, and can let renames break stored rows. Use stable discriminator codes and constraints; test unknown forward types in rolling deployment.

Composition or separate records may better fit. Do not put unrelated variants into one huge Active Record hierarchy solely because framework support is easy.

### Handle bulk/native methods explicitly

Bulk update/delete/import paths often skip instantiation, validations, callbacks, timestamps, versions, events, and authorization. Use them only with explicit predicates, constraints, version/audit/event handling, operation identity, batching, and reconciliation.

Expire/clear stale loaded objects. Test the exact framework method; similarly named APIs can have different lifecycle semantics.

### Make schema coupling intentional

Active Record convention reduces configuration when schema and class align. Renaming/splitting columns or moving behavior affects class/API together. Use compatible expand/backfill/contract migrations and deploy sequencing.

Do not hide a highly divergent legacy schema behind endless model callbacks/aliases. A Data Mapper/anti-corruption layer may restore clarity.

### Test without erasing persistence semantics

Unit-test pure value calculations and row-local transitions, but do not replace the record/database everywhere with mocks. Integration-test actual framework/driver/database for validations versus constraints, transactions/rollback, versions/locks, associations/cascades, callbacks/order, bulk bypass, generated values, scopes, tenant access, and query plans.

Coordinate concurrent writes, fault-inject before/after commit/outbox, and assert query/row budgets at representative cardinality. Test migration compatibility with old/new app versions.

### Observe model behavior

Record operation/model name, outcome, validation/constraint/version/deadlock category, transaction duration, statement/row count, association loads, callback duration/failure, bulk affected count, outbox count/lag, and migration fallback. Bound labels and redact record attributes.

Monitor god-model dependency growth, callback count/churn, N+1 regressions, high conflict, bypass writes, and changes touching many models/controllers/jobs.

### Know when to evolve

Extract value objects/policies first. Move multi-record orchestration into Service Layer/Transaction Script, rich lifecycle/invariants into Domain Model aggregates, set operations into Table Module, and persistence translation into Data Mapper when model/schema diverge.

Migrate one use case at a time behind characterization tests. Active Record can remain for simple areas; architecture need not be uniform. Evidence is duplicated rules, callback tangles, cross-row transactions, hard testing, schema friction, and change coupling—not class size alone.

## Definitions and Notation

Let a record be $a=(k,v,p)$, with scoped key $k$, loaded version $v\in\mathbb{N}$, and persistent field vector $p$. Domain transition is partial:

$$
f(a,c,x)=a'\in A_v\quad\text{or}\quad r\in R,
$$

where $A_v$ is valid record state and $R$ typed rejection. Persistence function $w$ must apply key/tenant/version predicate:

$$
w(a',v)=
\begin{cases}
(a'[v\leftarrow v+1],1),&\text{exactly one current row matches},\\
(a',0),&\text{stale or missing under authorized scope}.
\end{cases}
$$

If an operation changes records $a_1,\ldots,a_n$, per-record correctness does not imply atomic use-case correctness. A transaction must provide all-or-none durability for the governed write set, idempotency, audit, and outbox under its assumptions.

## Mechanisms, Invariants, or Proof Structure

### Active Record design procedure

1. Determine whether identity, lifecycle, and rules are truly row-centered; compare Data Mapper/Domain Model/Table Module alternatives.
2. Define stable scoped key, values, fields, lifecycle, version, constraints, and protected attributes.
3. Expose domain-named methods and per-use-case allowed inputs; supply trusted context explicitly.
4. Scope finders by tenant/disclosure, authorize actor-resource-action, and parameterize/allowlist query structure.
5. Back application validation with database constraints and atomic version/conditional writes.
6. Let the application own multi-record transaction, idempotency, audit, and outbox; restore/discard objects on failure.
7. Define associations, cascades, loading, query budgets, pagination, deletion, and inheritance semantics.
8. Keep callbacks local/bounded; move external effects to durable workflows and govern bypass/bulk APIs.
9. Evolve schema compatibly and observe conflicts, callbacks, query counts, bulk paths, and model coupling.
10. Test the real framework/database, concurrency, failures, security, migrations, and representative data; extract richer boundaries when evidence demands.

### Executable finite model

The example implements one row-wrapping `InvoiceRecord` with tenant-scoped lookup, action authorization, lifecycle validation, guarded version save, and local-state restoration on conflict. It demonstrates serialized in-memory behavior—not SQL, transactions, constraints, concurrent atomicity, callbacks, associations, or secure authentication.

<!-- bijux-verify: {"id":"active-record-invoice","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"first=approved status=approved version=3\nstale=conflict local_status=pending row_status=approved row_version=3\ndenied=denied row_status=pending row_version=1\n","stderr":""}} -->
```python
class InvoiceRecord:
    def __init__(self, rows, tenant_id, invoice_id, status, version):
        self.rows = rows
        self.tenant_id = tenant_id
        self.invoice_id = invoice_id
        self.status = status
        self.version = version

    @classmethod
    def find(cls, rows, tenant_id, invoice_id):
        row = rows[(tenant_id, invoice_id)]
        return cls(rows, tenant_id, invoice_id, row["status"], row["version"])

    def save(self, expected_version):
        key = (self.tenant_id, self.invoice_id)
        row = self.rows[key]
        if row["version"] != expected_version:
            return "conflict"
        self.rows[key] = {"status": self.status, "version": expected_version + 1}
        self.version = expected_version + 1
        return "saved"

    def approve(self, actor, expected_version):
        if actor != "manager-3":
            return "denied"
        if self.status != "pending":
            return "invalid-state"
        original_status = self.status
        self.status = "approved"
        result = self.save(expected_version)
        if result == "conflict":
            self.status = original_status
            return "conflict"
        return "approved"


rows = {
    ("T1", "I-7"): {"status": "pending", "version": 2},
    ("T1", "I-8"): {"status": "pending", "version": 1},
}
invoice = InvoiceRecord.find(rows, "T1", "I-7")
result = invoice.approve("manager-3", 2)
print(f"first={result} status={invoice.status} version={invoice.version}")
stale = InvoiceRecord(rows, "T1", "I-7", "pending", 2)
result = stale.approve("manager-3", 2)
row = rows[("T1", "I-7")]
print(f"stale={result} local_status={stale.status} row_status={row['status']} row_version={row['version']}")
other = InvoiceRecord.find(rows, "T1", "I-8")
result = other.approve("intruder", 1)
row = rows[("T1", "I-8")]
print(f"denied={result} row_status={row['status']} row_version={row['version']}")
```

### Finite invariant argument

**First approval.** Trusted actor and pending state pass. Candidate becomes approved; stored version 2 matches expected; replacement writes approved/version 3 and object becomes version 3.

**Stale approval.** Detached candidate starts pending/version 2 while row is already version 3. It passes local domain checks but guarded save returns conflict before row replacement; method restores local status to pending. Row remains approved/version 3.

**Denied approval.** Actor check returns before mutation/save, so I-8 remains pending/version 1.

For these calls, only authorized pending current record transitions, stale/denied calls do not write, and versions increase only on success. The proof assumes serial calls and immutable tenant/key. A real implementation requires an atomic `UPDATE ... WHERE tenant/id/version`, transaction rollback, trusted authentication/authorization, and database constraints; checking a dictionary version is only a model.

### Evidence classification

The snippet report is empirical evidence for one success, stale conflict, and denial. State/version traces can be recomputed. It provides no evidence for real database atomicity/isolation, callback behavior, framework security, query performance, or business approval policy.

## Alternatives and Trade-Offs

| Approach | Persistence location | Best fit | Main risk |
|---|---|---|---|
| Active Record | On row object | Simple row-centered logic | Schema/domain coupling |
| Data Mapper | Separate mapping layer | Rich independent model/schema | More mapping machinery |
| Row Data Gateway | Row wrapper, little domain logic | Scripts/Table Modules | Behavior elsewhere |
| Table Data Gateway | One table access object | Set-oriented operations | No per-record domain owner |
| Transaction Script | Use-case procedure | Simple multi-table workflow | Rule duplication |
| Domain Model + Repository | Aggregate/value behavior | Rich interacting rules | Mapping/boundary complexity |

An application can combine these by bounded context: Active Record for administrative/configuration records, Domain Model for core rules, projections for reads, and Table Module for bulk work.

## Failure Modes and Misconceptions

- **“Active Record is only CRUD.”** It includes row-centered domain logic; generated accessors alone are anemic records.
- **“Active Record is always an anti-pattern.”** It is effective when behavior/schema are simple and aligned.
- **“Model class means domain model.”** Persistence lifecycle/callback methods do not equal rich domain behavior.
- **“Validation guarantees uniqueness.”** Concurrent inserts require a database unique constraint and typed violation handling.
- **“Each save is enough transactionality.”** Multi-record use cases need one encompassing transaction.
- **“Object instance prevents stale writes.”** Another context/process has another instance; use versions/locks.
- **“After-commit guarantees delivery.”** Crash/failure can lose the effect; use outbox/relay.
- **“Callbacks centralize all rules.”** They often hide ordering, bypass paths, recursion, and transaction phase.
- **“Association cascade means aggregate ownership.”** Persistence convenience can delete shared/unrelated data.
- **“Default scope is security.”** Alternate finders/unscoped paths and stale authority can bypass it.
- **“Strong parameters/allowlists authorize the action.”** Field admission differs from actor-resource-action permission.
- **“Eager loading always fixes N+1.”** Join multiplication, memory, and pagination can worsen.
- **“Bulk update is a faster save loop.”** It may bypass every record lifecycle mechanism.
- **“Schema conventions remove migration risk.”** Rolling versions still need compatible evolution.
- **“Unit tests with in-memory records prove persistence.”** Constraints, isolation, callbacks, query plans, and drivers require real integration tests.

## Worked Examples

### Example 1

**Situation.** A content page has title, slug, body, publication state, and simple transitions.

**Reasoning.** One row is natural lifecycle unit; `publish` plus unique slug/check/version constraints fit Active Record. A separate aggregate/mapper stack may add little value.

**Conclusion.** Simple row-aligned behavior is a strong fit.

### Example 2

**Situation.** An invoice approval must atomically update invoice, ledger entries, request record, and outbox.

**Reasoning.** `invoice.approve` can own row lifecycle, but Service Layer owns one transaction and coordinates other records. Independent `save` calls are insufficient.

**Conclusion.** Active Records still need an application transaction boundary.

### Example 3

**Situation.** Two users create the same tenant-scoped username after both validation queries pass.

**Reasoning.** Race allows both attempts. A unique `(tenant, normalized_username)` constraint selects one winner; map violation to typed conflict and ensure normalization/collation agree.

**Conclusion.** Validation improves errors; constraints enforce concurrent integrity.

### Example 4

**Situation.** Request mass-assigns `{role: "admin", tenant_id: "T2", status: "approved"}`.

**Reasoning.** Type-valid fields are unauthorized. Per-use-case allowlist admits only intended descriptive inputs; server derives tenant/actor and protected transitions run through named methods/authorization.

**Conclusion.** Field filtering and action authorization are separate mandatory controls.

### Example 5

**Situation.** `after_save` charges payment; later transaction rollback occurs.

**Reasoning.** Charge cannot roll back and retry can duplicate. Persist payment intent/outbox in transaction, then workflow calls provider with idempotency and reconciliation.

**Conclusion.** External effects do not belong in save callbacks.

### Example 6

**Situation.** Listing 500 posts calls `post.author.name` and issues 501 queries.

**Reasoning.** Lazy loading creates N+1. Preload/batch authors or return a joined projection; assert query/row budget. A wide eager join may also multiply rows.

**Conclusion.** Association convenience needs use-case query design.

### Example 7

**Situation.** Bulk status update bypasses lock versions and callbacks, then stale instances save.

**Reasoning.** Stale writes can revert status and events/audit vanish. Use explicit bulk operation with version policy/outbox/reconciliation and expire contexts, or perform guarded per-record workflow.

**Conclusion.** Bulk paths are separate persistence protocols.

### Example 8

**Situation.** Soft-deleted email row still blocks uniqueness but default scope hides it.

**Reasoning.** Decide reuse/restoration policy and encode it in partial/compound unique constraint supported by engine; explicit scopes include deleted where needed. Authorization prevents accidental restoration.

**Conclusion.** Soft deletion changes identity, constraints, queries, and lifecycle semantics.

### Example 9

**Situation.** Pricing rules now span customer tier, contract version, tax jurisdiction, and hundreds of lines.

**Reasoning.** Callbacks/scopes on `OrderRecord` become tangled. Extract Money/TaxPolicy and a Domain Model/Table Module as appropriate, leaving Active Record behind a repository/mapper or converting incrementally.

**Conclusion.** Interacting cross-record rules are evidence to evolve beyond row-centered ownership.

### Example 10

**Situation.** A clinical record callback auto-releases a result whenever status changes to verified.

**Reasoning.** Release depends on patient consent, critical-result workflow, correction state, reviewer authority, time, and notification safety. Model an explicit authorized operation/workflow with version/audit/outbox and named clinical/privacy review.

**Conclusion.** High-stakes transitions must not hide in generic lifecycle callbacks.

## Cross-Program Connections

- [Database Engineering](../../18-database-engineering/ROADMAP.md) develops constraints, transactions, locks, indexes, plans, and migrations beneath Active Record.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) develops commands, typed outcomes, idempotency, and operation boundaries.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) supplies tenant/action authorization, injection defense, disclosure, and audit.
- [Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) provides integration, concurrency, fault, mutation, and performance evidence.
- [SEPAT-057](057-data-mapper.md) contrasts persistence independence; [SEPAT-059](../ROADMAP.md) analyzes deferred association/data loading.

## References

1. Martin Fowler, [“Active Record”](https://martinfowler.com/eaaCatalog/activeRecord.html), *Patterns of Enterprise Application Architecture* catalog, 2003.
2. Martin Fowler, *Patterns of Enterprise Application Architecture*, Addison-Wesley, 2002. Active Record and neighboring domain/data-source patterns.
3. Ruby on Rails, [“Active Record Basics”](https://guides.rubyonrails.org/active_record_basics.html), current guide accessed 2026-08-29. Concrete framework implementation of the pattern.
4. Ruby on Rails, [“Active Record Query Interface”](https://guides.rubyonrails.org/active_record_querying.html), accessed 2026-08-29. Querying, eager loading, transactions, and locking mechanisms.
5. Ruby on Rails, [“Active Record Callbacks”](https://guides.rubyonrails.org/active_record_callbacks.html), accessed 2026-08-29. Lifecycle/transaction callback semantics and cautions.
6. Ruby on Rails, [“Securing Rails Applications”](https://guides.rubyonrails.org/security.html), accessed 2026-08-29. Parameter, record-access, injection, and logging security guidance.
7. Jim Gray and Andreas Reuter, *Transaction Processing: Concepts and Techniques*, Morgan Kaufmann, 1992.
8. Eric Evans, *Domain-Driven Design: Tackling Complexity in the Heart of Software*, Addison-Wesley, 2004. Domain/application/infrastructure boundaries and rich models.
9. Martin Kleppmann, *Designing Data-Intensive Applications*, O’Reilly, 2017. Transactions, concurrency, events, and distributed-failure limits.
10. OWASP Foundation, [“Authorization Cheat Sheet”](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html), accessed 2026-08-29.

## Exercises

### Exercise 1

Trace the executable model if `stale.approve("manager-3",3)` is used instead of expected version 2. State local/row outcome and identify the caller error the compact model permits.

### Exercise 2

Design an Active Record for tenant-scoped document publication. Specify fields/values, domain methods, protected attributes, validations, constraints, versions, scopes, transaction/outbox, callbacks, soft deletion, and query tests.

### Exercise 3

Diagnose a model with 70 callbacks, 40 associations, 12 concerns, network calls, and bulk admin updates. Produce an incremental extraction plan and evidence gates without a flag-day rewrite.

### Exercise 4

Compare Active Record, Data Mapper plus Domain Model, Transaction Script, and Table Module for a catalog item, insurance claim adjudication, and nightly fee accrual. Justify a hybrid architecture.

### Exercise 5

Review a high-stakes Active Record design for approving a laboratory result. Cover transaction authorization, lifecycle, corrections, versions, constraints, callbacks, outbox, notification workflow, privacy, query/access paths, bulk corrections, tests, and external review.

## Answers to the Exercises

### Answer 1

The stale object has pending/version 2 locally, but caller supplies expected 3. Actor/state pass; status becomes approved; `save(3)` finds row version 3, succeeds, writes approved/version 4, and changes stale object version to 4. It treats an object loaded from revision 2 as if based on revision 3, bypassing optimistic intent.

Production API should not accept arbitrary expected version separate from the record's captured version; `save` uses `self.version` as the predicate, and incoming command expected version must match it/current loaded context. Reloading revision 3 then re-running domain decision would reveal it is already approved and reject/idempotently classify. This shows optimistic locking requires trustworthy version provenance, not merely a number in `WHERE`.

### Answer 2

`DocumentRecord` fields: tenant/id, immutable slug or versioned rename policy, title/body values with length/normalization, state draft/scheduled/published/withdrawn, scheduled/published times, author/editor IDs, row version, deletion state, timestamps. Methods include `revise_content`, `schedule(at,zone,actor)`, `publish(actor,policy,expected_version)`, `withdraw`, and explicit restore; status/time setters are protected.

Validate readable errors; database enforces tenant/key, tenant/normalized slug uniqueness under deletion policy, not-null/check state-time combinations, foreign keys, and version. Finders always tenant-scoped; named public scopes are bounded/paginated and authorization is actor-resource-action specific. Service Layer owns transaction over document, idempotency, audit, and outbox; publication relay/search notification occurs after commit via outbox, not callbacks. Callbacks may normalize title/slug deterministically but cannot publish or recurse.

Soft deletion defines slug reuse, restoration, associations, retention, and authorization. Optimistic updates guard tenant/id/version; stale conflicts reload/redecide. Tests cover state table, same-slug race, tenant same ID/slug, version race, rollback/outbox, callback-bypass methods, deletion/restoration, scheduled time/DST, unauthorized IDs, injection, N+1 author listing, pagination/query budget, and old/new migration compatibility.

### Answer 3

Inventory every callback by phase, trigger APIs, dependencies, database/external effects, idempotency, transaction assumptions, and bypass paths; map associations/cascades and admin bulk methods. Add characterization/integration tests and telemetry for callback order/count/time, SQL/query count, effects, versions, constraints, and failure points. Stop adding new hidden callbacks.

First move network calls to transactionally stored outbox plus durable workflows, preserving stable event IDs and reconciling existing effects. Introduce explicit domain-named application operations for the riskiest lifecycle; move authorization/transaction/idempotency there. Extract pure value/policy rules from concerns/callbacks. Replace broad associations with IDs/query projections and explicit ownership; move reports/bulk work to Table Module/query services with versions/audit/reconciliation. Add database constraints before removing validation callbacks where safe.

Migrate one caller/use case at a time behind compatible APIs, compare outcomes/telemetry, and remove the old callback only when all triggering/bypass paths are covered. If core behavior becomes rich, introduce aggregate plus Data Mapper/repository incrementally; retain Active Record for simple tables. Gates include real database concurrency/rollback tests, effect fault injection, query budgets, authorization matrix, data reconciliation, canary metrics, and tested rollback/forward plan.

### Answer 4

A catalog item with row-local name/price/availability and modest associations fits Active Record, backed by Money, constraints, versions, tenant scope, and projections. Insurance claim adjudication has evidence, parties, decisions, policy versions, lifecycle and cross-record invariants; use Domain Model plus Data Mapper/repository and Service Layer/workflow. Nightly fee accrual is set-oriented over many accounts; use Table Module/set SQL with policy version, batching, idempotency, audit/outbox, and reconciliation. A Transaction Script can coordinate simple catalog import or one administrative use case.

The hybrid shares transaction/security/outbox standards but chooses behavioral owner by shape. Active Record remains for simple identity units, Data Mapper protects the rich claim model from storage, and Table Module avoids hydrating millions of records. This minimizes uniformity theater while keeping boundaries explicit.

### Answer 5

Use an explicit `approve_result(command, trusted_context)` application operation, not a generic status update/callback. The record lifecycle distinguishes preliminary, verified, corrected, withheld, approved/released; domain methods require current expected version, reviewer qualifications/assignment, significant patient/result data bound to transaction authorization, policy/time, and correction state. Database constraints enforce tenant/patient/result identity, version, required reviewer/timestamps, status combinations, and immutable correction/audit relationships.

One transaction reauthorizes actor-resource-action/purpose/consent, guarded-updates result, writes idempotency and protected audit/correction lineage, and inserts privacy-minimized outbox. Callbacks may set deterministic local timestamps only under defined authority; they never release/notify. Notification is an idempotent workflow after commit with consent/channel rules, delay/duplicate/unknown outcome, escalation, and reconciliation. All finders/projections are tenant/patient/purpose scoped; admin/bulk correction is separately authorized, versioned, batched, audited, reconciled, and expires stale instances.

Tests cover lifecycle/property boundaries, corrected/withheld/critical results, actor/patient/tenant matrix, guessed IDs, significant-data binding/replay, version races, constraints, rollback/outbox/commit uncertainty, callback/bulk bypass, notification failures, privacy/redaction, query scope/N+1, migration compatibility, and operational recovery. Named laboratory medicine, treating clinicians, patient safety, privacy/legal/regulatory, security, human-factors/accessibility, database/SRE, and operations reviewers approve real rules/workflow; green Active Record tests cannot establish clinical or regulatory correctness.
