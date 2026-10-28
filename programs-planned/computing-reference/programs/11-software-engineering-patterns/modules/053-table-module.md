---
module_id: SEPAT-053
program: Software Engineering: Patterns
level: 2
module_number: 53
title: Table Module
status: complete
last_verified: 2026-08-28
---

# Table Module

## One-Page Review

### Governing question

When should business logic be organized as one module over a table or record set, and how can that design preserve relational semantics, domain rules, authorization, transaction isolation, set-based performance, and an evolution path without collapsing into SQL scattered across the application?

### Essential definitions

- A **Table Module** is one object/module that handles the domain logic for all rows in a database table or view.
- A **relation** is a set of tuples over named attributes; SQL tables approximate this model but add nulls, duplicates, ordering conventions, and implementation behavior.
- A **record set** is an in-memory tabular representation, often query-shaped and disconnected or tracked.
- **row identity** is the key by which one logical record is distinguished; it is not object instance identity.
- A **set-based operation** states a transformation over qualifying rows rather than issuing one command per row.
- A **predicate** selects rows; a **projection** chooses/derives attributes; a **join** combines tuples under a condition.
- A **business invariant** is a predicate over one row or a related set of rows that must hold at its declared consistency boundary.
- A **database constraint** is an engine-enforced predicate such as key, reference, check, exclusion, or another supported assertion.
- **affected-row count** is observable evidence of which rows an atomic conditional mutation claimed; it must be interpreted against command semantics.

### Central model, mechanism, or theorem

For relation state \(R\), trusted command \(c\), and context \(x\), a table operation denotes

\[
F(R,c,x)=R' \quad\text{or typed rejection},
\]

where the intended update can be expressed as replacing each tuple \(t\) satisfying authorized predicate \(P(t,c,x)\) with transformation \(g(t,c,x)\):

\[
R'=(R\setminus S)\cup\{g(t,c,x)\mid t\in S\},
\quad S=\{t\in R\mid P(t,c,x)\}.
\]

If \(g\) preserves row invariant \(I\), the database enforces required set constraints, and transaction isolation prevents the relevant anomaly, the committed result preserves the stated invariant. Source-level set notation alone proves none of those premises.

### Critical invariants

- Each module owns one cohesive table/view-centered concept and exposes domain-named operations, not generic CRUD escape hatches.
- Selection predicates include trusted tenant, authorization, lifecycle, version, time, and eligibility conditions required by the action.
- Commands distinguish zero qualifying rows, stale/conflicting state, invalid input, denial/non-disclosure, and successful no-op where semantics require.
- Set transformations preserve units, precision, null semantics, key/reference constraints, and row/set invariants.
- One declared transaction covers consistent reads, governed writes, idempotency, and outbox/audit intent; isolation/locking matches competing operations.
- Bulk operations are bounded, observable, cancellable, and designed for locking, logs, indexes, retries, partial failure, and statement limits.
- SQL is parameterized and least-privileged; dynamic identifiers/operators come only from an allowlisted server-side plan.
- Record sets and caches have explicit identity, freshness, tracking, merge, and conflict semantics.
- Tests use the supported database for SQL, constraints, plans, concurrency, rollback, triggers, and affected-row behavior.

### Common failures

Common failures include one table module for the whole database, generic `save(table, fields)`, UI event handlers as business logic, row-by-row queries and updates, N+1 joins, trusting client tenant/status/price, lost updates, assuming affected rows means authorized success, null/three-valued-logic mistakes, duplicate-sensitive logic on bag results, implicit ordering, unbounded bulk updates, parameterizing values but interpolating identifiers, bypassed constraints, hidden triggers, long locks, retry after external effects, record-set last-write-wins, mapping every join to writable rows, mocks that do not match database semantics, and selecting Table Module merely because tables exist.

### Compact example

One `InvoiceTable` applies a 10% discount to every open invoice for tenant `T1` whose subtotal is at least 10,000 cents. Rows `I1` and `I2` change from 12,000 and 10,000 to 10,800 and 9,000; tenant `T2` and a paid invoice remain unchanged. Repeating the operation changes zero rows because a policy-version marker makes it idempotent.

### Connections

[SEPAT-052](052-domain-model.md) models behavior per entity/aggregate; [SEPAT-054](../ROADMAP.md) introduces Service Layer as an application boundary. Table Module connects to [Database Engineering](../../18-database-engineering/ROADMAP.md), [Data Engineering](../../19-data-engineering/ROADMAP.md), and [Software Design and Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md).

## Governing Question

When is the natural unit of business behavior a relation or record set rather than an individual object, and what makes a table-centered module correct, cohesive, secure, and operable under production data and concurrency?

Table Module keeps logic in application code while embracing tabular data. Its defining instance represents a table-shaped concept as a whole; identifiers select rows for operations. It is not “put every SQL statement in a utility class.”

## Why This Matters

Many domains contain calculations and state changes naturally expressed over groups: age all receivables, price qualifying lines, allocate capacity, close a settlement batch, or compute risk by portfolio. Relational systems are optimized for predicate-driven operations and constraints. Building thousands of entity objects merely to perform one uniform transformation can add mapping work and round trips without clarifying behavior.

Table Module gives business rules an explicit owner without forcing an object per row. It is particularly useful with record-set-oriented platforms, stored procedures behind a typed boundary, and services whose core work is set transformation.

Its proximity to storage creates risk. SQL dialect, isolation, null semantics, indexes, authorization predicates, and triggers become correctness concerns. Set-based speed can turn one bad predicate into a mass update. Graduate-level design therefore treats query shape and transaction behavior as part of the contract.

## Prerequisites and Retrieval

You should understand relational algebra, SQL, keys and constraints, joins, transactions/isolation, indexes/query plans, authorization, and application layering. Retrieve these facts:

1. A mathematical relation is unordered and contains no duplicate tuples; SQL results can have duplicates and only have guaranteed order with `ORDER BY`.
2. SQL null comparisons use three-valued logic; `x = NULL` is not a null test.
3. One set-based statement can be atomic while still participating in anomalies with other statements/transactions.
4. A predicate should describe domain eligibility and authority, not merely physical row location.
5. Database constraints govern every writer that uses the database; application checks can provide clearer errors but can race.
6. Query-plan cost depends on cardinality, selectivity, distribution, indexes, memory, and engine/version statistics.
7. A rollback cannot undo a nontransactional remote side effect.

## Learning Objectives

After completing this module, you should be able to:

- distinguish Table Module from Transaction Script, Domain Model, Active Record, Gateway, and generic data access;
- select Table Module from domain shape and change pattern rather than database existence;
- define cohesive table-centered operations with typed commands, results, and authority;
- reason about selection, projection, joins, grouping, set transformation, nulls, duplicates, and ordering;
- pair application rules with keys, constraints, versions, locks, and transaction isolation;
- design bounded, restartable, observable bulk operations and durable event publication;
- prevent tenant leakage, mass assignment, SQL injection, and information disclosure;
- test real query semantics, plans, triggers, rollback, concurrency, and record-set merging;
- recognize row-by-row performance traps and the point where a Domain Model or workflow is clearer;
- review financial, clinical, or regulated table operations without overstating automated evidence.

## Core Exposition

### Choose a table-shaped behavioral unit

Use Table Module when operations are most clearly stated over records of one cohesive concept and its related views: invoices, contracts, ledger postings, claims, or inventory positions. A module might expose `overdue_for`, `apply_policy`, and `close_period`, not `execute(sql)`.

The logical module need not correspond one-to-one with one physical base table. A stable updatable view, record set, or table plus closely owned children may define the surface. Document the correspondence and mutation rules; do not call an arbitrary multi-domain query a table merely because it returns rows.

### Contrast the neighboring patterns

Transaction Script organizes around one use case; repeated scripts may each touch several tables. Table Module organizes reusable behavior around one table-shaped concept. Domain Model creates instances for individual entities and distributes behavior among collaborating objects. Active Record attaches persistence and behavior to each row object.

A Gateway or Data Mapper handles persistence mechanics, not business rules. A Service Layer defines application use-case boundaries and may call Table Modules. These roles can coexist if ownership is clear.

### Model relations, not iteration

Start by expressing the qualifying set and result: “all open invoices for this tenant under policy P with subtotal at least threshold.” Separate selection from transformation and result. Think in joins, anti-joins, grouping, windowing, and conditional updates before writing loops.

Set thinking reduces round trips and lets the optimizer choose access paths. It also makes blast radius larger. Preview/count under the same semantics when policy allows, impose tenant and lifecycle predicates, cap or batch work, and require explicit confirmation for unusual cardinality.

### Give each operation a semantic contract

Specify trusted command fields, actor/tenant/action context, preconditions, affected population, transformation, invariant, transaction/isolation, result algebra, idempotency, events, and resource bounds. A method returning only `true` hides whether zero or ten million rows changed.

Useful results include applied count and stable operation ID, already applied, invalid, denied/non-disclosing, stale/conflict, limit exceeded, retry exhausted, and internal failure. Do not infer denial from zero affected rows unless the disclosure policy intentionally merges not-found, unauthorized, and ineligible cases.

### Put authority inside the mutation predicate

Load actor and tenant from authenticated server context, never request fields. Constrain mutation by tenant and current authorization-relevant state. If policy comes from another table, join or lock/read it consistently, or pass signed/versioned evidence whose semantics are validated.

Use least-privilege database roles and row-level policy where appropriate as defense in depth. Application module cohesion does not prevent a separate writer from bypassing rules.

### Treat null, duplicates, and order explicitly

Define whether absence is unknown, not applicable, not yet recorded, or forbidden. Use `IS NULL`/`IS DISTINCT FROM`-style semantics where appropriate and test truth tables. Avoid `NOT IN` surprises when subqueries can contain null; reason with `NOT EXISTS` under explicit correlation.

Use keys or `DISTINCT` only for justified semantics. A join multiplying invoice rows by line rows can double a sum; preaggregate or group by the correct key. Never rely on physical row order for allocation, pagination, or “first” without a deterministic tie-breaking order.

### Preserve units and numeric semantics

Use explicit currency/unit columns and integer minor units or configured exact decimals. State rounding mode/stage, tax/discount order, overflow behavior, exchange-rate version, and whether aggregate sums can exceed a single-row range.

Database and application numeric types must agree. A table operation over mixed currency cannot `SUM(amount)` meaningfully without grouping or conversion policy.

### Back rules with constraints

Use primary/unique keys for identity and idempotency, foreign keys for governed references, checks for row predicates, and exclusion/other supported constraints for overlapping or cross-row conditions. Constraints close races and protect against alternate writers.

Application logic should still validate for domain-readable results. Catch specific constraint identifiers/states and map them deliberately; never parse locale-dependent error prose. Not every business rule belongs in a constraint, especially external or temporal policy.

### Choose a concurrency mechanism per anomaly

An atomic conditional update can combine decision and write: update only rows with expected version/status/balance. Inspect affected rows. For multi-row predicates, competing inserts or write skew may require key-range/predicate locks, materialized claims, advisory locks, or serializable isolation according to the actual engine.

Document lock order and transaction size. Retrying a serialization failure means rerunning the whole safe unit from fresh reads under a deadline; it does not mean retrying the last statement after external effects.

### Design bulk mutation as an operation

Bulk work needs an operation identity, scope digest, policy version, requested/started/completed timestamps, actor, progress, and outcome. Decide between one atomic statement/transaction and bounded batches. One transaction gives atomic visibility but can hold locks, grow logs, exhaust resources, and block maintenance; batches improve operability but expose intermediate state.

If batching, define stable ordering, watermark/keyset, snapshot membership, idempotency, resume, concurrent insert/update policy, and final reconciliation. “Process 1000 at a time” is not sufficient semantics.

### Avoid row-by-row database traffic

Loading IDs, querying each row, then updating each row creates N+1 latency and race windows. Prefer one guarded `UPDATE`, `INSERT ... SELECT`, merge/upsert with understood engine semantics, or a small bounded number of statements.

Row iteration can be correct when each item invokes heterogeneous external work or complex code, but separate selection/claiming from effects and make progress/idempotency explicit. Do not keep database locks across slow calls.

### Use parameters and allowlisted structure

Bind values through the driver. Parameters ordinarily cannot stand for table names, column names, sort directions, or operators; choose those from a closed server-side map. Limit projection, filters, pagination, and result size.

Avoid accepting arbitrary predicates or field maps. Generic update APIs bypass domain names, authorization, validation, audit, and migration compatibility even if injection-safe.

### Manage record-set identity and state

Disconnected record sets need primary keys, original versions, and a merge policy. A row copied twice is not two domain entities, but edits can conflict. Submit changed columns plus expected version, detect conflicts, and decide whether fields commute or require user resolution.

Mark query-only projections as read-only. A joined/aggregated row may not map unambiguously back to base tables. Do not let a UI data grid become the sole owner of business validation.

### Separate queries from commands where useful

Queries can return purpose-built immutable records from views/projections. Commands call named Table Module operations. This separation prevents reporting joins from masquerading as writable entities and allows different indexing/scaling/freshness choices.

Do not force CQRS infrastructure where a typed distinction suffices. The durable principle is that read shape should not silently dictate write invariants.

### Publish effects through an outbox

When changed rows imply messages, insert outbox records in the same database transaction. For bulk changes, decide whether one summary event or per-record events preserve consumer semantics, ordering, privacy, and payload limits. Use stable event IDs and schema versions.

The relay may duplicate and delay. Consumers need idempotency and monitoring. Never call a broker or webhook inside a retriable set update and assume rollback can retract it.

### Observe blast radius and cost

Record operation name/version, actor/tenant-safe identity, predicate/policy version, estimated and actual affected rows, duration, lock wait, deadlock/serialization conflicts, batches, retries, query-plan fingerprint, outbox count, and failure category. Avoid sensitive row payloads and unbounded labels.

Use statement/lock/deadline limits and cancellation. Alert on unexpected cardinality, lag, repeated conflicts, plan regression, constraint failure, partial-batch stall, and reconciliation mismatch.

### Test against the real engine

Unit-test pure predicates/calculations, but integration-test supported database/version/schema: null truth tables, duplicates, collation, precision, constraints, triggers, affected-row count, generated SQL, permissions, rollback, isolation, deadlocks, timeout, cancellation, and plan/index behavior at representative distributions.

Coordinate concurrent schedules instead of relying on random timing. Fault-inject before/after operation reservation, each batch, state update, outbox insert, commit acknowledgement, and relay publish. Verify resume and reconciliation.

### Evolve when the shape changes

Table Module strains when one row develops a rich lifecycle, behavior depends on object collaboration, rules cross many tables with awkward signatures, or modules mirror a volatile physical schema. Extract values/policies first; introduce a Domain Model for the complex subset while retaining set-based modules for reporting and bulk operations.

Conversely, a Domain Model may delegate a true bulk calculation to a Table Module/query service. Avoid ideological conversion. Measure change locality, rule clarity, data volume, concurrency, mapping cost, and operational evidence.

## Definitions and Notation

Let \(R\subseteq D_1\times\cdots\times D_n\) be a finite relation with key function \(k\). Let predicate \(P(t,c,x)\) select tuples authorized and eligible for command \(c\) under trusted context \(x\). Let transformation \(g\) preserve the key and return a tuple of the same schema.

Define \(S=\sigma_P(R)\). A conceptual simultaneous update is

\[
U(R)=(R\setminus S)\cup g[S],
\quad g[S]=\{g(t,c,x)\mid t\in S\}.
\]

Key preservation requires

\[
\forall t_1,t_2\in U(R): k(t_1)=k(t_2)\Rightarrow t_1=t_2.
\]

For a percentage discount \(d\in[0,1]\) on nonnegative integer-cent subtotal \(a\), define a specified rounding function \(\rho\) and \(a'=\rho(a(1-d))\). The finite executable model uses integer formula \(a'=\lfloor 9a/10\rfloor\) for exactly 10%; production policy must state whether floor is correct.

## Mechanisms, Invariants, or Proof Structure

### Table Module design procedure

1. Name the cohesive table/view concept and compare Table Module with scripts, entities, and set-oriented SQL.
2. Define keys, units, null/duplicate/order semantics, constraints, and authoritative context.
3. Give each operation a typed command/result, qualifying predicate, transformation, invariant, and cardinality bound.
4. Put tenant/authorization/lifecycle/version conditions in the governed mutation and back rules with constraints.
5. Model competing transactions; choose conditional statements, locks, claims, or isolation for actual anomalies.
6. Design bulk atomicity or batching with identity, snapshot/watermark, resume, idempotency, and reconciliation.
7. Keep external effects outside transactions and atomically record outbox/audit intent.
8. Parameterize values, allowlist structure, apply least privilege, and bound resources.
9. Test real SQL/engine semantics, plans, concurrency, faults, record-set merges, and observability.
10. Extract a richer model or workflow when table-centered ownership stops explaining the rules.

### Executable finite model

This in-memory `InvoiceTable` is one module instance over all invoice rows. It applies a versioned tenant-scoped policy as a conceptual set transformation. It demonstrates qualification, arithmetic, unaffected rows, and repeat idempotency in serialized memory—not SQL nulls, transactions, indexes, locks, authorization, persistence, or crash recovery.

<!-- bijux-verify: {"id":"table-module-discount","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"first=2 I1=10800 I2=9000 I3=15000 I4=20000\nrepeat=0 I1=10800 I2=9000 I3=15000 I4=20000\n","stderr":""}} -->
```python
class InvoiceTable:
    def __init__(self, rows):
        self.rows = rows

    def apply_discount(self, tenant_id, minimum_cents, policy_version):
        eligible = [
            row for row in self.rows
            if row["tenant"] == tenant_id
            and row["status"] == "open"
            and row["subtotal_cents"] >= minimum_cents
            and row["discount_policy"] != policy_version
        ]
        for row in eligible:
            row["subtotal_cents"] = row["subtotal_cents"] * 9 // 10
            row["discount_policy"] = policy_version
        return len(eligible)


rows = [
    {"id": "I1", "tenant": "T1", "status": "open", "subtotal_cents": 12000, "discount_policy": None},
    {"id": "I2", "tenant": "T1", "status": "open", "subtotal_cents": 10000, "discount_policy": None},
    {"id": "I3", "tenant": "T2", "status": "open", "subtotal_cents": 15000, "discount_policy": None},
    {"id": "I4", "tenant": "T1", "status": "paid", "subtotal_cents": 20000, "discount_policy": None},
]
invoices = InvoiceTable(rows)
changed = invoices.apply_discount("T1", 10000, "P-7")
values = " ".join(f'{row["id"]}={row["subtotal_cents"]}' for row in rows)
print(f"first={changed} {values}")
changed = invoices.apply_discount("T1", 10000, "P-7")
values = " ".join(f'{row["id"]}={row["subtotal_cents"]}' for row in rows)
print(f"repeat={changed} {values}")
```

### Finite invariant argument

**Base.** Each row has a unique ID, nonnegative subtotal, recognized status, tenant, and no applied policy.

**Selection.** Only rows satisfying tenant `T1`, open status, threshold \(a\ge10000\), and different policy marker enter \(S\). Thus `I3` and `I4` cannot change.

**Transformation.** For each selected integer \(a\ge0\), \(a'=\lfloor9a/10\rfloor\ge0\); identity, tenant, and status remain unchanged; policy becomes `P-7`. IDs remain unique because keys do not change.

**Repeat.** No transformed row satisfies `discount_policy != "P-7"`, while originally ineligible rows remain ineligible, so the second qualifying set is empty.

The argument assumes no concurrent mutation, unique valid input rows, exact integer arithmetic, no leaked mutation during iteration, and one fixed 10% policy. A production SQL claim additionally depends on constraints, atomic transaction behavior, isolation, authorization, and documented rounding.

### Evidence classification

The snippet report is empirical evidence for two serialized calls. Arithmetic and set membership are independently recomputable; the finite preservation argument is reviewable. Query-plan, concurrency, database, security, financial-policy, and operational claims require separate evidence.

## Alternatives and Trade-Offs

| Approach | Organizing center | Best fit | Main risk |
|---|---|---|---|
| Transaction Script | Use case | Few simple workflows | Duplicated table rules |
| Table Module | Table/view/record set | Set-oriented business logic | Schema coupling and mass-update blast radius |
| Domain Model | Entity/value/aggregate | Rich lifecycle and collaboration | Mapping and boundary complexity |
| Active Record | One row object | Simple CRUD with row-local behavior | Persistence coupling/N+1 |
| Stored procedure | Database routine | Data-intensive atomic work near storage | Portability, deployment, test/ownership split |
| Functional transformation | Immutable collections/relations | Deterministic batch calculation | Persistence/concurrency remains external |
| Workflow/saga | Long-running process | Cross-system coordination | Intermediate states and compensation |

Table Module can invoke database routines through a typed contract or implement transformations in application memory. Location is secondary to cohesive ownership and explicit guarantees.

## Failure Modes and Misconceptions

- **“One class per table is automatically Table Module.”** It must own business behavior, not generic persistence.
- **“A singleton is required.”** The conceptual module is single per table role; instances may carry transaction/session dependencies safely.
- **“Set-based means correct.”** A concise statement can have the wrong predicate, isolation, units, or authority.
- **“Rows changed proves success.”** Counts need command-specific interpretation and disclosure policy.
- **“A preview count makes a later update safe.”** State can change unless both share an adequate transaction/snapshot/claim.
- **“SQL tables are mathematical relations.”** Nulls, duplicate results, and ordering require explicit treatment.
- **“Constraints replace domain errors.”** They protect data but need deliberate mapping and cannot express every rule.
- **“Application checks prevent races.”** Check-then-update can race without guarded mutation or isolation.
- **“Bulk batches are equivalent to one transaction.”** Intermediate visibility and concurrent membership change semantics.
- **“Offset pagination is a stable work queue.”** Inserts/deletes can skip or repeat rows; use stable keysets/claims.
- **“Parameters can represent arbitrary SQL structure.”** Dynamic structure requires a server-side allowlist.
- **“Record sets merge themselves.”** Disconnected edits need identity/version/conflict rules.
- **“ORM bulk update fires entity hooks.”** Many bulk paths bypass loaded objects, validations, and callbacks.
- **“The fastest query is the right model.”** Correctness and semantic ownership precede tuning.
- **“Mocks prove database behavior.”** Engine-specific null, isolation, trigger, constraint, and plan behavior needs real integration tests.

## Worked Examples

### Example 1

**Situation.** Pricing 50,000 independent open invoice rows uses one object load/update per row.

**Reasoning.** The rule is uniform and predicate-driven. One Table Module operation can calculate/set values with a guarded set statement or bounded set batches, avoiding N+1 traffic. It still records policy version, tenant, rounding, count, conflicts, and events.

**Conclusion.** Set-shaped rules favor Table Module when individual object collaboration adds no meaning.

### Example 2

**Situation.** A `NOT IN` query should select customers without blocked identifiers, but the blocked list contains null.

**Reasoning.** Comparisons against null yield unknown; `NOT IN` can therefore select no rows unexpectedly. Use a correctly correlated `NOT EXISTS` and define whether null identifiers are invalid or absent. Test the truth table in the supported engine.

**Conclusion.** SQL three-valued logic is part of business-operation correctness.

### Example 3

**Situation.** Joining invoices to lines and payments before summing duplicates both child sets.

**Reasoning.** An invoice with two lines and three payments produces six joined rows. Summing directly multiplies values. Aggregate each child relation by invoice key before joining, or use separate subqueries with key guarantees.

**Conclusion.** Join cardinality must be derived before trusting aggregates.

### Example 4

**Situation.** A bulk approval request includes tenant ID supplied by the client.

**Reasoning.** A malicious actor substitutes another tenant. Derive tenant and actor from authenticated context; put tenant, allowed lifecycle, and action authority into selection/update; use least privilege and audit. Decide whether zero results disclose existence.

**Conclusion.** Tenant/authorization predicates belong in the governed mutation, not only UI filters.

### Example 5

**Situation.** Two workers select the same 1,000 pending rows and both send effects.

**Reasoning.** Selection did not claim work. Atomically claim rows with operation/lease/owner under appropriate locking, commit, then perform idempotent external work; record outcomes and reclaim expired leases. Do not hold row locks during network calls.

**Conclusion.** Bulk processing requires explicit claim and effect idempotency semantics.

### Example 6

**Situation.** A job updates ten million rows in one transaction and blocks production.

**Reasoning.** Atomicity may not justify lock/log/resource cost. Use stable keyset batches with operation identity, captured membership or declared concurrent policy, idempotent marker, checkpoints, cancellation, reconciliation, and a maintenance/backpressure plan.

**Conclusion.** Batching trades atomic visibility for operability and must define intermediate correctness.

### Example 7

**Situation.** A disconnected record set overwrites a newer status when saving an edited description.

**Reasoning.** Whole-row last-write-wins lost the concurrent update. Submit intended field change with original version; conditional update detects conflict. Merge only if field-level commutativity is a declared rule; otherwise return conflict.

**Conclusion.** Record-set convenience does not remove identity/version semantics.

### Example 8

**Situation.** A module accepts `sort_column` and concatenates it into SQL after value parameters are bound.

**Reasoning.** Value binding does not protect identifiers. Map a small external enum to fixed quoted SQL fragments and fixed directions; reject everything else, bound page size, and use deterministic key ties.

**Conclusion.** Dynamic SQL structure must come from a closed server-side plan.

### Example 9

**Situation.** Updating rows and then publishing one message per row crashes midway through broker calls.

**Reasoning.** Database and broker are a dual write. Insert per-row or summary outbox intents atomically with updates according to consumer semantics; relay later with stable IDs. Consumers deduplicate and monitor lag.

**Conclusion.** A Table Module needs the same durable-effect boundary as other write models.

### Example 10

**Situation.** A clinical table operation discontinues all “inactive” prescriptions based on a stale projection.

**Reasoning.** Define inactivity, effective/recorded time, pending administrations, clinician authority, legal hold, patient scope, and stale-data limit. Revalidate under the write transaction, bound/preview the population, require appropriate confirmation, retain audit/rollback plan, and obtain named clinical/safety review.

**Conclusion.** Set-oriented efficiency magnifies semantic error; high-stakes bulk actions need domain and operational controls beyond tests.

## Cross-Program Connections

- [Database Engineering](../../18-database-engineering/ROADMAP.md) develops relational algebra, SQL, indexing, constraints, query planning, transactions, and isolation.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) covers bounded batch processing, watermarks, idempotency, reconciliation, and data-quality evidence.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) supplies authorization, tenant isolation, injection defense, audit, and least privilege.
- [Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) develops database integration, property, concurrency, and fault testing.
- [SEPAT-052](052-domain-model.md) provides the entity-centered alternative; [SEPAT-054](../ROADMAP.md) places domain-logic components behind a use-case service boundary.

## References

1. Martin Fowler, [“Table Module”](https://martinfowler.com/eaaCatalog/tableModule.html), *Patterns of Enterprise Application Architecture* catalog, 2003.
2. Martin Fowler, *Patterns of Enterprise Application Architecture*, Addison-Wesley, 2002. See Table Module and the neighboring domain-logic and data-source patterns.
3. Martin Fowler, [“Record Set”](https://martinfowler.com/eaaCatalog/recordSet.html), *Patterns of Enterprise Application Architecture* catalog, 2003.
4. E. F. Codd, [“A Relational Model of Data for Large Shared Data Banks”](https://doi.org/10.1145/362384.362685), *Communications of the ACM* 13(6), 1970, pp. 377–387.
5. C. J. Date, *An Introduction to Database Systems*, 8th ed., Addison-Wesley, 2003. Durable relational-model foundations.
6. Hector Garcia-Molina, Jeffrey D. Ullman, and Jennifer Widom, *Database Systems: The Complete Book*, 2nd ed., Pearson, 2008. Relational, SQL, storage, optimization, and transaction foundations.
7. Jim Gray and Andreas Reuter, *Transaction Processing: Concepts and Techniques*, Morgan Kaufmann, 1992. Transaction, recovery, locking, and operational foundations.
8. PostgreSQL Global Development Group, [“Transaction Isolation”](https://www.postgresql.org/docs/current/transaction-iso.html), current documentation accessed 2026-08-28. Official concrete semantics; other engines differ.
9. OWASP Foundation, [“SQL Injection Prevention Cheat Sheet”](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html), accessed 2026-08-28. Parameterization and allowlist guidance.
10. Martin Kleppmann, *Designing Data-Intensive Applications*, O’Reilly, 2017. Transactions, streams, batches, and distributed consistency limits.

## Exercises

### Exercise 1

Trace the executable module if `I2` starts at 9,999 cents and `I4` is open. State both outputs and explain membership in the qualifying set.

### Exercise 2

Derive the correct invoice total query shape when invoices have many lines and many payments. Explain why a direct three-way join is wrong, how keys/nulls affect the result, and what constraints/tests support the derivation.

### Exercise 3

Design a restartable operation that expires up to 20 million sessions while live traffic creates and refreshes sessions. Specify membership, time capture, batches, claims/versions, idempotency, concurrency, indexes, events, progress, cancellation, and reconciliation.

### Exercise 4

Compare Transaction Script, Table Module, and Domain Model for (a) simple invoice entry, (b) portfolio-wide interest accrual, and (c) a single insurance claim with a rich adjudication lifecycle. Justify a hybrid architecture.

### Exercise 5

Review a proposed bulk financial fee correction that will update two million accounts. Produce a release/evidence plan covering rule version, units/rounding, authorization, preview, isolation, batching/atomicity, rollback/compensation, outbox, customer communication, privacy, observability, and human approvals.

## Answers to the Exercises

### Answer 1

With `I2=9999`, it fails the inclusive `>=10000` threshold. With `I4` open, it now satisfies tenant, status, threshold, and policy-marker predicates. First output reports two changes: `I1=10800`, `I2=9999`, `I3=15000`, `I4=18000`. On repeat, `I1` and `I4` carry `P-7`; other rows remain ineligible, so zero change and identical values. Unique row identity and nonnegative totals remain unchanged.

### Answer 2

Directly joining invoice, line, and payment rows forms each line-payment pair: \(m\) lines and \(n\) payments yield \(mn\) rows, multiplying both sums. Compute `line_totals` grouped by invoice key and `payment_totals` grouped by invoice key, then left-join each one-row-per-invoice result to invoices. Coalesce missing aggregate results to zero only if “no children means zero” is the domain rule; do not coalesce unknown amounts.

Primary/foreign keys support identity/references; nonnegative/units/currency constraints support valid components. Group by currency unless conversion is explicit. Tests cover no children, one/many on each side, duplicate source keys, nulls, mixed currency, large totals/overflow, and representative plans. Recompute small fixtures manually and compare ledger authority where applicable.

### Answer 3

Capture one authoritative cutoff \(T\) and operation ID/policy digest. Membership is sessions with `expires_at < T`, not legally retained, and not already completed by this operation. Use a selective `(status, expires_at, id)`-style index suited to the engine. Process stable keyset batches ordered by `(expires_at,id)`; atomically claim/version rows or conditionally update only if `expires_at < T` still holds, so a concurrent refresh wins rather than being expired.

Record checkpoints, attempted/changed/conflicted counts, deadlines, lock waits, and errors. Each change stores operation marker and outbox intent atomically; repeat is idempotent. Decide whether new already-expired sessions after snapshot belong to this run or the next. Support cancellation between batches, expired-claim recovery, bounded retry, and final queries reconciling eligible, changed, refreshed/conflicted, excluded, and failed populations. Load-test plans/locks/log growth and fault-inject at batch and commit boundaries.

### Answer 4

(a) Simple entry fits Transaction Script: validate, insert invoice/lines, commit/outbox. Extract values for money/tax even without a rich model. (b) Portfolio-wide accrual fits Table Module because eligibility and calculation operate over a relation; it needs policy version, currency/rounding, guarded bulk updates, batching, and reconciliation. (c) Rich claim adjudication fits Domain Model when evidence, decisions, state transitions, roles, and invariants interact around one claim aggregate, with workflow for external parties.

A Service Layer can expose all three use cases. Repositories persist claim aggregates; Table Modules serve accrual and projections; scripts coordinate simple entry. Database constraints, outbox, authorization, and typed results cross the approaches. The hybrid is justified by rule shape, not one architectural style per application.

### Answer 5

Freeze a named correction policy with account population, effective time, currency, exact-decimal/minor-unit arithmetic, rounding stage/mode, caps, tax/jurisdiction, examples, and independently recomputed totals. Obtain named finance/accounting, product, legal/compliance, security/privacy, database/SRE, and release approvals; automated tests cannot substitute for them. Derive actor/tenant authority and use dual control for execution.

Run a read-only preview from the same predicate/version, reporting count and bounded aggregates by currency/jurisdiction without leaking customer data; independently reconcile against ledger sources. Choose one transaction only if proven operationally safe, otherwise stable idempotent batches with operation ID, snapshot/membership policy, conditional versions, checkpoints, and final reconciliation. Test representative volume, indexes/plans, lock/log/replication impact, concurrent account changes, constraint failures, cancellation, and commit uncertainty.

Persist old/new amount, reason, policy/operation version, actor, and outbox intent atomically. Prefer compensating ledger entries over destructive history rewrites; rehearse pause/rollback/compensation and customer-support communication. Relay versioned events idempotently, monitor affected/conflicted/failed totals, money reconciliation, lock wait, lag, and customer-impact signals, then obtain post-run sign-off. Protect audit and messages under retention/disclosure policy.
