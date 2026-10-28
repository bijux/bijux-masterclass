---
module_id: SEPAT-057
program: Software Engineering: Patterns
level: 2
module_number: 57
title: Data Mapper
status: complete
last_verified: 2026-08-28
---

# Data Mapper

## One-Page Review

### Governing question

How can a mapping layer translate between a behavior-rich object model and a relational/document schema while preserving identity, units, nullability, invariants, relationships, versions, generated state, query performance, migrations, security, and independent evolution on both sides?

### Essential definitions

- A **Data Mapper** is a layer that moves data between objects and a database while keeping the objects, database, and mapper independent.
- An **object schema** describes classes, identity, values, inheritance, collections, and behavior; a **relational schema** describes tables, rows, columns, keys, constraints, and joins.
- **materialization** decodes rows into managed objects; **decomposition** encodes object state into persistence values/actions.
- A **mapping contract** declares identity, field/type/unit/null conversion, relationship ownership, versions, lifecycle, and errors for one mapped concept.
- A **value converter** translates a domain value such as Money or Instant to/from one or more storage values without losing semantics.
- An **Identity Map** resolves repeated rows/loads to one managed object per scoped identity.
- A **Unit of Work** tracks new/dirty/deleted objects and coordinates ordered transactional writes.
- **optimistic versioning** includes a loaded revision in guarded updates/deletes to detect stale writes.
- A **projection/read model** is purpose-built query data; it need not be a writable domain entity.
- **round-trip law** means decode/encode preserve an explicitly defined semantic equivalence, not necessarily byte/row equality.

### Central model, mechanism, or theorem

Let valid domain states be $O_v$, accepted database rows $R_a$, encoding $e:O_v\to R_a$, decoding $d:R_a\to O_v\cup E$, and semantic equivalence $\simeq$. A sound mapping aims for

$$
\forall o\in O_v:\quad d(e(o))\simeq o,
$$

and, for accepted rows,

$$
\forall r\in R_a:\quad e(d(r))=c(r),
$$

where $c$ is documented canonicalization (normalization, defaults, generated values, representation changes). These laws are conditional on identity, precision, schema version, relationships, and transaction context. Passing one round trip does not prove concurrency, query plans, migration correctness, or domain truth.

### Critical invariants

- Domain objects contain no SQL, table/column, connection/session, or persistence lifecycle knowledge unless an explicit local exception is justified.
- Each mapper declares stable identity, tenant/shard scope, complete/partial shape, required fields, null/absence semantics, types, units, precision, normalization, and schema version.
- Materialization validates rows, resolves Identity Map before construction/population, and never exposes half-valid or duplicate managed entities.
- Decomposition persists only governed attributes, never arbitrary client fields; generated/read-only/derived fields have one authority.
- Values and relationships preserve currency/unit/time zone/order/cardinality/ownership semantics rather than merely compatible primitive types.
- Updates/deletes use keys plus expected version/constraint policy and interpret affected rows; Unit of Work owns transaction/ordering/commit.
- Query shape is deliberate: joins, batching, eager/lazy loading, pagination, projections, and indexes are reviewed for semantics and cost.
- Database constraints back representable invariants; mapper errors distinguish corrupt data, incompatible schema, domain rejection, conflict, and infrastructure failure.
- Migrations support mixed-version deployment, backfill/verification, rollback/forward recovery, and mapper compatibility windows.
- SQL is parameterized, tenant/authorization predicates are server-derived, sensitive fields are minimized/protected, and logs do not expose data.

### Common failures

Common failures include one generic reflection mapper for all semantics, domain annotations/schema names leaking everywhere, mapping tables one-to-one into an anemic model, treating null as empty/zero/unloaded, float money, local time without zone, enum ordinal drift, silent truncation, mutable natural identity, duplicate materialization, constructors bypassed into invalid objects, eager graph explosion, lazy N+1, cartesian join duplication, raw-row pagination, cascade over-delete, last-write-wins without versions, bulk/native SQL bypass, generated fields not refreshed, trigger surprises, arbitrary map mass assignment, interpolated SQL, schema migration flag days, swallowed corrupt rows, and mocks whose type/isolation behavior differs from the database.

### Compact example

An `OrderMapper` translates `{order_id, tenant_id, total_cents, currency, status, row_version}` into a domain `Order` containing immutable `Money`. Repeated load resolves one instance. A guarded save changes 1250 to 1500 SEK and version 3 to 4; a detached revision 3 save reports conflict without overwriting.

### Connections

[SEPAT-056](056-identity-map.md) supplies materialization identity resolution; [SEPAT-058](../ROADMAP.md) contrasts Active Record. Data Mapper connects to [Database Engineering](../../18-database-engineering/ROADMAP.md), [Software Design and Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md), and [Data Engineering](../../19-data-engineering/ROADMAP.md).

## Governing Question

What explicit, testable translation contract lets an object model and persistence schema serve their own purposes while every identity, value, relationship, state transition, conflict, and schema change retains its intended meaning?

Data Mapper is anti-corruption between representations. It does not eliminate impedance mismatch; it gives that mismatch an owned place with executable rules and evidence.

## Why This Matters

Relational schemas favor normalized sets, foreign keys, constraints, and set queries. Domain models favor identities, immutable values, encapsulated transitions, aggregates, and polymorphism. Forcing either to mirror the other can degrade both: table-shaped data bags lose behavioral ownership, while object-shaped schemas produce poor constraints and queries.

A mapper allows independent design, but translation becomes real complexity. `amount DECIMAL` to `Money`, nullable timestamp to lifecycle, discriminator to subtype, join rows to ordered collection, and row version to concurrency protocol are semantic decisions—not assignment boilerplate.

Mapping defects are dangerous because ordinary happy-path CRUD may pass. Precision loss, stale writes, cross-tenant identity collision, missing children, partial overwrites, and mixed-version deployment appear under boundaries and change. Graduate-level practice specifies laws, limits, and production evidence.

## Prerequisites and Retrieval

You should understand domain entities/values/aggregates, relational schemas/keys/constraints, SQL/transactions, Unit of Work, Identity Map, optimistic concurrency, inheritance, time/money, migrations, and query plans. Retrieve these facts:

1. In-memory references and relational foreign keys represent relationships differently.
2. SQL null uses three-valued logic and may encode several domain meanings poorly.
3. Decimal scale, integer range, collation, Unicode normalization, and time-zone behavior can differ between language and database.
4. One joined result row is not necessarily one entity; joins multiply cardinalities.
5. A successful update without an expected-version predicate can overwrite a newer revision.
6. Database-generated values and triggers can make in-memory state stale after write.
7. Expand/contract migrations require old and new application versions to coexist safely.

## Learning Objectives

After completing this module, you should be able to:

- distinguish Data Mapper from Active Record, Row Data Gateway, Repository, Unit of Work, Identity Map, DTO, and serializer;
- write explicit mapping contracts for identity, fields, nulls, values, relationships, inheritance, versions, and lifecycle;
- derive and test semantic round-trip/canonicalization laws and corruption behavior;
- materialize cyclic/repeated graphs through Identity Map without invalid partial objects;
- decompose aggregates into ordered, guarded persistence actions under Unit of Work;
- choose eager, lazy, batched, set, and projection query shapes from semantics and cost;
- map money, time, enums, text, encrypted data, generated values, and legacy schemas without silent loss;
- design inheritance/association/ownership strategies and detect cascade or cardinality hazards;
- evolve schema/mappers through compatible migrations with backfill and verification;
- test actual driver/database/ORM behavior, concurrency, failure, security, and performance.

## Core Exposition

### Define both models independently

Start with the domain's identities, invariants, values, transitions, and aggregate boundaries. Separately design storage for integrity, access paths, history, operations, and data lifecycle. Then write the mapping between them.

Do not assume one class per table or field per column. One value can span columns; one entity can span tables; several tables can feed a read projection; a table can support several context-specific models.

### Own mappings by stable concept

Group mapper code/configuration by aggregate/entity/value responsibility, with shared converters for truly shared semantics. Avoid one global utility full of string tables or one file per historical migration. Names should expose domain and storage roles.

Metadata/declarative mapping reduces repetition but does not remove semantic review. Generated mappings must be inspectable and testable; exceptional conversions stay explicit.

### Specify identity first

Declare mapped identity root/type, primary/composite key normalization, tenant/shard/persistence-unit scope, generation strategy, and domain-ID relationship. Identity Map uses this before recursive materialization.

Never infer identity from mutable display/natural attributes unless the domain makes them immutable and scoped. Generated identity must be returned and registered without changing unsafe equality/hash behavior.

### Decode defensively

Validate required columns, runtime types/ranges, schema/discriminator/version, nullability, enum values, units, text encoding, and relationships. Distinguish corrupt/incompatible data from not found and transient infrastructure failure.

Do not silently coerce `"12x"` to 12, unknown enum to default, negative unsigned concept to zero, or invalid date to current time. Quarantine/repair requires an explicit operational workflow with provenance.

### Construct valid objects

Use a reconstitution/factory path that preserves domain invariants while acknowledging historical persisted state. Register a shell with Identity Map before recursive graph population when cycles require it, but never expose the shell until complete validation succeeds.

Avoid public setters/no-argument constructors that application code can use to create invalid objects merely for ORM convenience. Imperative/external mapping can keep domain types persistence-ignorant; carefully configured instrumentation can too.

### Encode only persistent semantics

Map authoritative persistent attributes, not cached/UI/transport/derived fields unless deliberately stored. Restrict columns explicitly so new client/object fields cannot become mass assignment. Canonicalize under documented rules.

Computed domain values may be recomputed or stored with derivation version for query/audit. If database computes a value, treat it as generated/read-only and refresh/return it.

### Map null, absence, and optionality

Domain cases such as unknown, not applicable, withheld, not yet measured, and absent are not always one null. Use explicit sum/status types or companion reason columns when distinctions affect behavior. A nonloaded attribute is metadata, not null.

Make database `NOT NULL`, defaults, and application construction agree. A database default applies only when omitted under engine semantics; sending explicit null is different.

### Map numbers and money

Use integer minor units or exact decimal with declared precision/scale/rounding. Include currency as part of value and constraints. Check domain range against database and language range; aggregates can overflow even if each row fits.

Never use binary float for exact money. Round once at the policy-defined stage and test signs, halves, maximum, mixed currency, and database-driver conversion.

### Map time explicitly

Distinguish instant, local civil time, date, duration, and interval. Store instants with unambiguous UTC/offset semantics; retain zone ID when future civil-time rules matter. Define precision truncation/rounding and effective versus recorded time.

Test DST gaps/overlaps, leap/calendar boundaries, driver/session timezone, server defaults, and serialization. `CURRENT_TIMESTAMP` authority differs from application clock.

### Map text, enums, and identifiers

Declare Unicode normalization, case/collation, length units, whitespace, and comparison semantics. Application validation cannot assume database collation uniqueness behaves identically.

Persist stable enum codes, not ordinal positions or renamed language identifiers without migration. Unknown forward codes should yield explicit incompatible state, not accidental branch selection. External identifiers need format/scope/provenance.

### Map relationships by aggregate semantics

Foreign Key Mapping represents reference; Association Table Mapping represents many-to-many or relationship attributes; dependent objects may use parent key plus local ID. Define ownership, requiredness, uniqueness, ordering, orphan semantics, and cascade separately.

Do not map every navigable relationship bidirectionally. Cross-aggregate references often remain IDs and are loaded by application/query services. Persistence cascade is not automatically domain ownership.

### Materialize joins through Identity Map

Compute keys and resolve objects before population. Repeated parent/child rows reuse instances and relationship membership keys prevent duplicates. Validate repeated scalar columns agree within the expected snapshot.

Avoid paginating a multiplied join as entity pages. Page stable root IDs then load related data, or use an engine/framework strategy whose completeness is tested.

### Choose loading strategy per use case

Eager join can reduce round trips but multiply rows and memory. Lazy Load defers work but creates hidden I/O, N+1, scope/authorization/lifetime failures. Select-in/batch loading often balances. Projections avoid materializing full graphs for reads.

Set query budget and observe actual statements/rows. A default fetch policy is not a performance design for every use case.

### Map inheritance deliberately

Single-table inheritance uses discriminator and nullable subtype columns: fast/simple reads, weaker subtype constraints/wide sparse rows. Joined/class-table uses base/subtype joins: normalized constraints, more joins. Concrete/table-per-class duplicates common fields and complicates polymorphic queries/unions.

Define unknown discriminator behavior, identity root, subtype transitions, constraints, query plan, and migration. Domain composition may avoid awkward persistence inheritance.

### Integrate Unit of Work

Mapper loads/registers through current Unit of Work/Identity Map, captures original persistent projection/version, and registers new/dirty/deleted actions. It never commits. UoW orders parent/child writes, batches, flushes, and handles failure.

Repositories expose domain retrieval/persistence intent and delegate mapping mechanics. Do not allow repository and mapper to each create sessions or duplicate identity maps.

### Enforce concurrency during writes

Encode updates/deletes using scoped key plus expected version and increment/return new version. Exactly one affected row is success; zero is typed stale/missing under the known authorization scope. Database constraints/locks/isolation protect other invariants.

Do not compare a version in application then issue unconditional update. Bulk operations must explicitly preserve/increment version or be isolated from tracked entity writes.

### Handle generated state and triggers

Use returning/generated-key facilities or refresh after flush for IDs, versions, timestamps, computed columns, and trigger changes. Ensure events/results use authoritative post-write values. Generated sequences may have gaps after rollback; do not treat gaplessness as an invariant.

Important business behavior hidden in triggers is invisible to the domain model and mapper unless refreshed/tested. Prefer database constraints for invariants and explicit domain behavior where feasible.

### Distinguish commands from projections

Writable domain entities are optimized for invariant-preserving transitions. Read screens/exports often need joins/aggregates/denormalization. Map them to immutable purpose-specific projections with freshness/disclosure metadata; never flush them back.

This separation does not require elaborate CQRS infrastructure. It avoids distorting the domain or loading graphs for reports.

### Parameterize and authorize

Bind values; choose identifiers/operators/order from a closed server-side mapping. Derive tenant/actor scope from trusted context and include it in selects/updates/deletes. Reauthorize action at the Service/Domain boundary; mapper possession is not permission.

Select only allowed columns, minimize decrypted sensitive data, use least-privilege credentials, and prevent query/projection endpoints from becoming arbitrary SQL or data-exfiltration interfaces.

### Protect sensitive fields

Decide plaintext, encrypted, tokenized, hashed, or external-vault representation based on use. Encryption changes equality/index/query/key-rotation semantics; hashes need purpose-appropriate algorithms/salts/peppers. Mapper/converter may coordinate cryptographic ports but must not log secrets.

Record key/version/provenance as required. Test rotation and mixed ciphertext versions; never imply encryption supplies authorization or integrity unless the construction/policy does.

### Design schema evolution with mapper evolution

Use expand/migrate/contract: add backward-compatible columns/tables, deploy code that reads old/new and writes compatible forms, backfill idempotently with checkpoints, verify constraints/data, switch reads, then remove old after every producer/consumer is migrated.

Dual writes can diverge; state authority and reconciliation. Avoid destructive rename/type changes in one flag day. Version events/exports separately from internal schema.

### Map legacy data explicitly

Legacy rows may violate new invariants, use sentinel values, composite natural keys, nullable contradictions, or encoded enums. Write an anti-corruption mapper that surfaces `LegacyUnknown`/repair requirements rather than contaminating the domain with arbitrary conventions.

Measure and classify invalid data before migration. Do not silently “fix” legally/audit-significant history on read.

### Observe and optimize

Record mapper/query name/version, statement count, rows, materializations, identity hits, relationship cardinality, bytes, duration, plan fingerprint, lazy loads, batch size, conversion/corrupt-row failures, conflicts, generated refreshes, and migration fallback usage. Bound labels and redact values.

Optimize from query plans/cardinality and service objectives. Denormalization/projections may be better than clever object loading; preserve correctness evidence during tuning.

### Test mapping as a contract

Unit-test pure converters and property/round-trip laws over boundary values. Fixture/golden rows test compatibility and canonicalization. Integration-test actual schema, driver, database, ORM/mapping configuration, constraints, generated values, triggers, timezone/collation/precision, relationships, inheritance, queries, and transaction failures.

Concurrency tests race versions. Query tests assert results plus bounded statement/row plans at representative distributions. Migration tests run old/new mixed versions, backfill, verification, rollback/forward recovery. Security tests cover tenant same-ID, column disclosure, mass assignment, and injection.

## Definitions and Notation

Let $O_v$ be valid domain states, $R_a$ accepted row states, $E$ mapping errors, $e:O_v\to R_a$ encoding/decomposition, and $d:R_a\to O_v\cup E$ decoding/materialization. Semantic equivalence $\simeq$ ignores representation-only differences but preserves all behaviorally relevant identity, value, relationship, and version facts.

Object round trip requires

$$
d(e(o))\simeq o\quad\forall o\in O_v.
$$

Row canonicalization requires, when $d(r)\notin E$,

$$
e(d(r))=c(r),
$$

not necessarily $r$, because defaults, normalized text, canonical enum code, generated values, column order, and equivalent representations may differ. For lossy mappings, define observation $\pi$ and require only $\pi(d(e(o)))=\pi(o)$; never hide loss behind full equivalence.

## Mechanisms, Invariants, or Proof Structure

### Data Mapper procedure

1. Define domain and storage models independently; name identity, invariant, access, history, and lifecycle needs.
2. Specify mapped key/type/tenant/shard, schema version, complete/partial shape, fields, nulls, types, units, precision, normalization, and errors.
3. Define pure value converters and semantic round-trip/canonicalization laws including documented loss.
4. Materialize lookup-first through Identity Map; validate before exposure and deduplicate graph relationships.
5. Decompose only governed persistent state; capture originals/versions and register actions with Unit of Work.
6. Map relationships/inheritance/loading/projections with cardinality, ownership, ordering, scope, and query-cost evidence.
7. Apply scoped parameterized guarded writes, constraints, generated-value refresh, and singular transaction ownership.
8. Protect tenant/authorization/sensitive fields; synchronize alternate bulk/trigger writers.
9. Evolve mapper/schema through compatible expand/backfill/verify/contract and explicit legacy repair.
10. Test converters, round trips, real schema/driver/ORM, plans, concurrency, faults, migrations, and security.

### Executable finite model

The finite mapper explicitly translates a row into `Order` plus `Money`, resolves repeated load through an Identity Map, encodes a guarded update, increments the version, and rejects a stale detached revision. It does not use SQL, transactions, relationships, partial loads, migrations, authorization, or a real driver/database.

<!-- bijux-verify: {"id":"data-mapper-order","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"loaded=O-7 total=1250 SEK version=3 same=True reads=1\nsave=updated row_total=1500 version=4\nstale=conflict row_total=1500 version=4\n","stderr":""}} -->
```python
class Money:
    def __init__(self, cents, currency):
        if cents < 0 or currency not in {"SEK", "EUR"}:
            raise ValueError("invalid-money")
        self.cents = cents
        self.currency = currency


class Order:
    def __init__(self, tenant_id, order_id, total, status, version):
        if status not in {"draft", "confirmed"}:
            raise ValueError("invalid-status")
        self.tenant_id = tenant_id
        self.order_id = order_id
        self.total = total
        self.status = status
        self.version = version

    def revise_total(self, total):
        if self.status != "draft" or total.currency != self.total.currency:
            return "rejected"
        self.total = total
        return "revised"


class OrderMapper:
    def __init__(self, rows):
        self.rows = rows
        self.identity_map = {}
        self.reads = 0

    def key(self, tenant_id, order_id):
        return (tenant_id, "Order", order_id)

    def load(self, tenant_id, order_id):
        identity = self.key(tenant_id, order_id)
        if identity in self.identity_map:
            return self.identity_map[identity]
        self.reads += 1
        row = self.rows[identity]
        total = Money(row["total_cents"], row["currency"])
        order = Order(tenant_id, order_id, total, row["status"], row["row_version"])
        self.identity_map[identity] = order
        return order

    def save(self, order, expected_version):
        identity = self.key(order.tenant_id, order.order_id)
        row = self.rows[identity]
        if row["row_version"] != expected_version:
            return "conflict"
        replacement = {
            "total_cents": order.total.cents,
            "currency": order.total.currency,
            "status": order.status,
            "row_version": expected_version + 1,
        }
        self.rows[identity] = replacement
        order.version = replacement["row_version"]
        return "updated"


rows = {
    ("T1", "Order", "O-7"): {
        "total_cents": 1250,
        "currency": "SEK",
        "status": "draft",
        "row_version": 3,
    }
}
mapper = OrderMapper(rows)
order = mapper.load("T1", "O-7")
same_order = mapper.load("T1", "O-7")
print(f"loaded={order.order_id} total={order.total.cents} {order.total.currency} version={order.version} same={order is same_order} reads={mapper.reads}")
order.revise_total(Money(1500, "SEK"))
result = mapper.save(order, 3)
row = rows[("T1", "Order", "O-7")]
print(f"save={result} row_total={row['total_cents']} version={row['row_version']}")
stale = Order("T1", "O-7", Money(900, "SEK"), "draft", 3)
result = mapper.save(stale, 3)
row = rows[("T1", "Order", "O-7")]
print(f"stale={result} row_total={row['total_cents']} version={row['row_version']}")
```

### Finite invariant argument

**Decode/load.** Row values satisfy Money/status constructors; tenant/type/ID key registers one order. Repeat returns same instance with no second read.

**Encode/update.** Domain transition accepts same-currency draft total 1500. Stored version equals expected 3, so mapper emits canonical replacement preserving identity/currency/status, sets total 1500, advances row/object version to 4.

**Stale rejection.** Detached revision expects 3 while row is 4. Mapper returns conflict before replacement, so total/version remain 1500/4.

For represented fields, decoding the canonical saved row yields an order semantically equivalent to the saved managed order. The proof assumes serial calls, valid complete row, unlimited integers, no storage failure, and no external mutation between version check and replacement. Production requires an atomic guarded database statement/transaction; the finite precheck alone can race.

### Evidence classification

The snippet report is empirical evidence for one load/repeat/save/conflict trace. Values, identity, version, and round-trip facts can be recomputed. It gives no evidence for SQL atomicity, driver conversions, query plans, relationship mapping, migrations, authorization, or real domain correctness.

## Alternatives and Trade-Offs

| Approach | Persistence knowledge | Best fit | Main risk |
|---|---|---|---|
| Data Mapper | Separate mapper layer | Rich independent domain/schema | Mapping complexity |
| Active Record | Entity knows persistence | Simple row-centered logic | Domain/storage coupling |
| Row Data Gateway | One row wrapper | Transaction Scripts/Table Module | Behavior split/data centricity |
| Table Data Gateway | Gateway handles table operations | Set-oriented scripts/modules | Rich object graphs absent |
| ORM declarative mapper | Metadata/instrumentation | Standard mappings/productivity | Hidden query/lifecycle semantics |
| Handwritten SQL mapper | Explicit code/SQL | Critical/complex tuned mappings | Repetition/maintenance |
| Immutable projection | One-way query mapping | Reads/analytics/exports | Not writable domain state |
| Event store mapper | Aggregate↔event stream | Event-sourced domains | Schema/replay/order/privacy cost |

Mix approaches by bounded context/use case. A rich aggregate may use Data Mapper while reporting uses projections and simple administrative tables use scripts/gateways.

## Failure Modes and Misconceptions

- **“Data Mapper means ORM.”** ORMs implement mapper mechanisms; handwritten or generated mappers also qualify.
- **“Persistence ignorance means storage semantics do not matter.”** Precision, constraints, isolation, plans, and generated values remain correctness concerns.
- **“One class should match one table.”** Independent models often require different shapes.
- **“Round trip must reproduce identical row bytes.”** Canonicalization/generated/default representation may differ; semantic equivalence must be defined.
- **“Null maps naturally to optional.”** Unknown, absent, withheld, unloaded, and inapplicable may differ.
- **“A successful constructor proves historical data valid.”** Legacy/corrupt states need explicit classification/repair.
- **“Every relationship should be navigable and cascading.”** Aggregate ownership and query needs should decide.
- **“Eager avoids performance problems.”** Large joins multiply rows; lazy creates N+1; measure per use case.
- **“Version check before update prevents races.”** The datastore mutation must be guarded atomically.
- **“Database trigger automatically updates objects.”** Generated/trigger state requires return/refresh.
- **“Annotations remove mapper coupling.”** Schema/configuration still shapes classes/tooling and needs review.
- **“Generic reflection handles all types.”** Money, time, enums, encrypted data, legacy values, and identity need semantic converters.
- **“Bulk SQL and ORM stay synchronized.”** Bulk paths often bypass identity, versions, events, and snapshots.
- **“Migration is a schema-only concern.”** Mapper compatibility and mixed-version behavior are integral.
- **“Mocks prove mapping.”** Real driver/database collation, precision, isolation, constraints, and plans require integration evidence.

## Worked Examples

### Example 1

**Situation.** Database decimal money maps to binary float and `0.1+0.2` differs from exact 0.3.

**Reasoning.** Use integer minor units or exact decimal with declared scale/rounding, map currency, enforce ranges, and test driver conversion at boundaries.

**Conclusion.** Primitive compatibility is not semantic preservation.

### Example 2

**Situation.** Nullable `released_at` means not released, withheld, or unknown after import.

**Reasoning.** One null collapses behaviorally distinct states. Persist explicit release status/reason plus timestamp constraints, and map to a sum/state type.

**Conclusion.** Optionality mapping must preserve domain distinctions.

### Example 3

**Situation.** An instant loses offset/precision through database session timezone and microsecond truncation.

**Reasoning.** Define UTC instant storage/driver settings, expected precision canonicalization, and retain zone separately for civil scheduling. Round-trip tests include DST and precision boundaries.

**Conclusion.** Time mapping requires kind, zone, and precision contracts.

### Example 4

**Situation.** Joining orders, lines, and tags produces duplicate lines/tags.

**Reasoning.** Resolve each identity once and attach relationship members by identity; recognize cartesian multiplication. Use separate batched loads or aggregation where the join is excessive.

**Conclusion.** Graph materialization depends on row cardinality reasoning.

### Example 5

**Situation.** A partial list projection is materialized as writable orders with missing address set null.

**Reasoning.** Later flush erases addresses. Return immutable `OrderSummary` or track unloaded attributes rigorously; command load uses full aggregate mapping.

**Conclusion.** Read projections should not masquerade as complete writable entities.

### Example 6

**Situation.** Enum ordinals change when a new source-code member is inserted.

**Reasoning.** Existing rows acquire wrong meaning. Store stable versioned codes with check/reference constraints; unknown codes produce incompatible-data outcome and staged migration.

**Conclusion.** Persist semantic codes, not incidental language ordering.

### Example 7

**Situation.** Two writers update version 8 after application-side checks.

**Reasoning.** Both checks can pass; unconditional updates lose one change. Use `WHERE id/tenant/version=8`, set version 9, require one affected row, and roll back Unit of Work on zero.

**Conclusion.** Concurrency belongs in the atomic mapped write.

### Example 8

**Situation.** Single-table inheritance sees unknown discriminator `crypto_invoice` during rolling deployment.

**Reasoning.** Old code must not instantiate base/default silently. Plan compatibility: deploy tolerant non-writable unknown representation or gate producer, then mapping, backfill/constraints, and activation.

**Conclusion.** Inheritance mapping and deployment versioning are one contract.

### Example 9

**Situation.** Column encryption is added, but equality query and key rotation stop working.

**Reasoning.** Randomized encryption prevents direct equality; deterministic forms leak patterns. Design token/blind-index policy, key version, dual-read/write rotation, authorization, integrity, and reconciliation with security review.

**Conclusion.** Sensitive-field mapping includes query and lifecycle semantics, not only ciphertext conversion.

### Example 10

**Situation.** A clinical mapper converts an unknown dosage unit to milligrams by default.

**Reasoning.** This fabricates a dangerous meaning. Reject/quarantine unknown unit, retain original/provenance, require explicit clinically approved conversion, and test units/ranges/history with named clinical and safety reviewers.

**Conclusion.** High-stakes mapping must fail visibly on semantic uncertainty.

## Cross-Program Connections

- [Database Engineering](../../18-database-engineering/ROADMAP.md) develops schemas, constraints, SQL, indexing, plans, transactions, and migrations.
- [Software Design and Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md) defines identities, values, aggregates, bounded contexts, and anti-corruption layers.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) develops schema evolution, backfill, quality, provenance, and reconciliation.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) supplies tenant authorization, injection defense, sensitive-data protection, and cryptographic lifecycle review.
- [SEPAT-056](056-identity-map.md) resolves repeated entities during decode; [SEPAT-058](../ROADMAP.md) contrasts placing persistence operations on row-centered objects.

## References

1. Martin Fowler, [“Data Mapper”](https://martinfowler.com/eaaCatalog/dataMapper.html), *Patterns of Enterprise Application Architecture* catalog, 2003.
2. Martin Fowler, *Patterns of Enterprise Application Architecture*, Addison-Wesley, 2002. Data Mapper and object-relational behavioral/structural patterns.
3. SQLAlchemy Project, [“ORM Mapped Class Overview”](https://docs.sqlalchemy.org/en/21/orm/mapping_styles.html), SQLAlchemy 2.1 documentation, accessed 2026-08-28.
4. Hibernate ORM, [*Hibernate ORM User Guide*](https://docs.jboss.org/hibernate/orm/current/userguide/html_single/Hibernate_User_Guide.html), accessed 2026-08-28. Concrete type, association, inheritance, generated-value, and version mappings.
5. Jakarta Persistence Team, [*Jakarta Persistence 3.2 Specification*](https://jakarta.ee/specifications/persistence/3.2/jakarta-persistence-spec-3.2.html), April 2024.
6. Eric Evans, *Domain-Driven Design: Tackling Complexity in the Heart of Software*, Addison-Wesley, 2004. Domain model independence and anti-corruption concepts.
7. Hector Garcia-Molina, Jeffrey D. Ullman, and Jennifer Widom, *Database Systems: The Complete Book*, 2nd ed., Pearson, 2008.
8. Jim Gray and Andreas Reuter, *Transaction Processing: Concepts and Techniques*, Morgan Kaufmann, 1992.
9. Martin Kleppmann, *Designing Data-Intensive Applications*, O’Reilly, 2017. Encoding/evolution, transactions, and data-system limits.
10. OWASP Foundation, [“SQL Injection Prevention Cheat Sheet”](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html), accessed 2026-08-28.

## Exercises

### Exercise 1

Trace the executable mapper if `order.revise_total(Money(1500, "EUR"))` is called and its return value is ignored before `save(order,3)`. State result/row and explain which layer failed.

### Exercise 2

Specify encode/decode/canonicalization laws for a `Money` value stored as decimal amount plus ISO currency. Include precision, rounding, negative/maximum, unknown currency, null, and database-driver evidence.

### Exercise 3

Design mappings and query plans for `Order` with ordered lines, product references, shipping address value, discounts, and polymorphic payment instruments. Include identity, ownership, loading, pagination, versions, cascades, and projections.

### Exercise 4

Plan an expand/migrate/contract evolution from `full_name` to structured names while two application versions, an export job, and a reporting replica coexist. Include authority, dual writes, backfill, verification, rollback/forward recovery, and privacy.

### Exercise 5

Review a high-stakes medication mapper translating prescriptions, doses, units, routes, schedules, corrections, and provenance between a clinical model and a legacy schema. Separate automated evidence from required clinical/regulatory/security review.

## Answers to the Exercises

### Answer 1

`revise_total` returns `rejected` because EUR differs from current SEK and leaves `order.total` at 1250 SEK. Ignoring the result then calling `save(order,3)` succeeds, writes the unchanged total/currency with version 4, and returns `updated`. The mapper preserved its inputs and version protocol; the application incorrectly treated a rejected domain command as successful and caused a no-op version advance.

The Service Layer must inspect the typed domain result and avoid registering/saving on rejection. Unit of Work may also avoid updates when persistent projection is unchanged. This demonstrates that mapping correctness cannot substitute for application/domain control flow.

### Answer 2

Let domain Money use exact integer minor units or arbitrary exact decimal plus validated ISO currency; choose one. For decimal columns define precision $P$, scale $S$, accepted range, and rounding mode/stage. Encode currency as stable uppercase code with reference/check constraint. Decode rejects null (unless domain type is optional), unknown code, excess scale not canonically representable, out-of-range, NaN/infinite driver values, and malformed data.

Define $d(e(m))=m$ for every representable Money. For accepted rows, $e(d(r))=c(r)$, where canonicalization may uppercase code and quantize only under declared non-lossy/approved rounding. If rounding is allowed, define observation/error bound explicitly rather than claim full equality. Tests cover zero, signs if allowed, half cases, max/min, each currency exponent policy, mixed currency prohibition, null, unknown code, excess precision/scale, and aggregate overflow. Integration tests use the real driver/database for decimal binding/result types, constraints, locale independence, and round trip; finance/domain reviewers approve rounding semantics.

### Answer 3

Map Order root by `(tenant,Order,id,version)`. Lines are owned children keyed `(order_id,line_id)` with unique `(order_id,position)` and positive quantity/exact Money fields; Unit of Work inserts root then lines and deletes children before root. Product is a cross-aggregate ID/reference, not cascade-owned. ShippingAddress is immutable columns or owned value table with explicit null/normalization. Discounts are ordered/versioned values or association entities if identity/audit is required. Payment instruments should usually be external tokens/references; if polymorphic persisted domain values are necessary, choose discriminator/joined strategy with unknown-code failure and privacy controls.

Command loading uses Identity Map and aggregate-appropriate batched/select-in relationships, not one huge cartesian join. Page root IDs deterministically then load lines; projections serve lists/reports without being writable. Guard root/owned updates with expected version and database constraints; define whether child changes increment root version. Cascade only owned lines/address, never Product/payment provider records. Test order preservation, duplicate/missing lines, pagination completeness, N+1/query budget, version races, orphan/delete, unknown payment subtype, and actual plans at representative cardinalities.

### Answer 4

Add nullable structured columns plus schema metadata without removing `full_name`. Declare authority during transition: preferably new structured fields are authoritative when present and legacy full name is a derived compatibility rendering; acknowledge that parsing arbitrary names is lossy. Deploy mapper capable of reading structured-or-legacy and writing both from one canonical command, with telemetry/reconciliation. Update export/report readers or provide compatible view before switching writes.

Backfill idempotently in bounded keyset batches with algorithm/provenance/confidence, never fabricate uncertain components; route ambiguous records to review or retain legacy-only state. Verify counts, null/length/Unicode/collation, sampled/domain-reviewed renders, dual representation consistency, replica lag, and privacy/minimized logs. Then switch reads to structured, stop old writers after inventory proves none remain, enforce appropriate constraints, and later remove legacy column only after export/report/rollback window closes.

Rollback before contract can switch readers to legacy while preserving new fields; after destructive contract use forward repair/restoration, not assumed rollback. Monitor mixed-version writes and reconcile divergence. Test old/new binaries against expanded schema, concurrent updates, backfill retries, replica/export behavior, and international names. Privacy/legal review covers data minimization and exposure of new components.

### Answer 5

Define stable prescription/order identity plus assigning organization/tenant and immutable revision/correction lineage. Map dose as exact amount plus controlled unit, medication concept/version, route code, frequency/schedule with time-zone and effective/recorded time, status, author/verifier, provenance, and expected version. Never default unknown unit/route/code, collapse prescribed/administered, overwrite correction history, infer zone, or convert without a versioned clinically approved rule.

Decode validates schema/code sets, units/ranges/precision, required combinations, temporal consistency, signatures/provenance, and distinguishes unknown/withheld/not-applicable/corrupt. Invalid legacy rows are quarantined/read-only with original evidence. Encode uses parameterized tenant-scoped guarded writes, immutable audit/correction records, generated authoritative timestamps, and outbox intent; sensitive fields follow disclosure/encryption/key lifecycle policy. Migrations use compatible code sets, backfill provenance, verification, and no silent history rewrite.

Automated evidence covers converter round trips, boundary/unit properties, known fixtures, schema/constraints, temporal/DST cases, versions/races, generated fields, migration/backfill reconciliation, tenant/column security, fault rollback, and query plans. It cannot establish clinically correct dose conversions, code interpretation, correction workflow, regulatory compliance, usability, or safe operational response. Named pharmacists/clinicians, terminology/informatics, patient safety, privacy/legal/regulatory, security, human-factors, data governance, database, and operations reviewers must approve those claims and retain review records.
