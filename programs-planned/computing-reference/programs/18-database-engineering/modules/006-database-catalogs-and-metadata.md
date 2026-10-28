---
module_id: DBE-006
program: Database Engineering
level: 1
module_number: 6
title: Database Catalogs and Metadata
status: complete
last_verified: 2026-08-30
---

# Database Catalogs and Metadata

## One-Page Review

### Governing question

How does a database represent its own schemas, objects, dependencies, privileges, and physical choices so that the engine and its operators can reason about change safely?

### Essential definitions

A **system catalog** is engine-owned relational state describing database objects and internal bookkeeping. A **data dictionary** is the governed body of such definitions, often including human descriptions. The SQL **information schema** exposes portable metadata views; an engine catalog exposes richer implementation-specific facts. An **object identifier** is an internal identity distinct from a qualified name. A **dependency graph** records which object requires another. **Introspection** queries metadata; **metadata drift** is an unexplained difference between intended and observed definitions.

### Central model, mechanism, or theorem

Model catalog state as a typed directed graph `G=(V,E)`. Each vertex has stable identity, kind, namespace, owner, definition, and version-visible attributes. Edge `u -> v` means dependent `u` requires referenced object `v`. Creation must resolve every reference; restrictive drop rejects a vertex with dependents; cascading drop computes the transitive reverse-reachable set and orders dependents before referenced objects. A canonical metadata projection can be hashed and compared, but interpretation remains version- and privilege-sensitive.

### Critical invariants

- Internal object identity is not inferred from a mutable or reusable name.
- Namespace plus engine rules resolve a name to at most one intended object.
- Column ordinals, types, defaults, nullability, collation, and generated status form one coherent row definition.
- Every dependency edge points to an existing object and has declared semantics.
- Catalog mutations use supported DDL, not ad hoc writes to engine-owned tables.
- Metadata reads state engine version, transaction/snapshot boundary, database, role, and search path.
- Privilege-filtered absence is not misreported as nonexistence.
- Destructive change plans close over dependents and distinguish restrict, cascade, and engine-implicit ownership.

### Common failures

Common failures include joining catalog rows by names instead of identifiers, ignoring namespaces and quoted-case rules, assuming `information_schema` exposes every engine feature, reading catalogs with an underprivileged role and declaring objects absent, treating column order as alphabetical, editing catalog tables directly, parsing stored DDL text as a universal model, missing dependencies hidden inside dynamic function text, assuming one metadata query works across major versions, and executing a cascade plan without first enumerating its transitive blast radius.

### Compact example

An `order_customer_fk` constraint depends on both `orders` and `customer`; a `customer_read` view and `customer_pk` constraint also depend on `customer`. Restrictive drop of `customer` must fail. A cascade plan drops the three dependents before the table while retaining `orders`. A privilege-filtered analyst view may expose the schema/table/view but not constraints, so its smaller result is not the complete catalog.

### Connections

[DBE-003](003-schemas-keys-and-constraints.md) defines the schema objects catalogs record. [DBE-005](005-denormalization-and-read-models.md) relies on cataloged view definitions and ownership. [DBE-007](../ROADMAP.md) compares deployment architectures whose metadata scope differs. Later modules use catalogs for query planning, statistics, transactions, recovery, replication, observability, and online upgrades.

## Governing Question

A database cannot parse, type-check, optimize, authorize, execute, recover, or evolve queries using table data alone. It must know that `customer_id` is an integer, which relation owns it, which index can search it, which role may read it, which constraint protects it, and which views or functions depend on it. That knowledge is data about data: metadata.

The governing engineering question is how this self-description remains coherent while DDL creates, alters, renames, and drops objects concurrently with ordinary work. Catalogs are not passive documentation. They participate in name resolution, plan construction, dependency enforcement, privilege checks, extension mechanisms, dump/restore, migration tools, and operational diagnosis.

## Why This Matters

Catalog errors are control-plane errors. A missing dependency can let a drop break a view; a stale type descriptor can misinterpret bytes; a leaked function definition can reveal secrets; a version-incompatible introspection query can omit a new object kind. Because tooling often treats metadata as ground truth, one wrong assumption can affect every schema or tenant.

Catalogs also make databases self-describing. Operators can inventory columns, locate missing constraints, generate migrations, estimate change blast radius, review grants, find unused indexes, and document ownership using relational queries. This is powerful precisely because metadata has schemas and relationships rather than an opaque binary registry.

Portability and completeness trade off. Standard `information_schema` views provide stable names and concepts across engines, but cannot expose every product-specific access method, partition bound, policy, extension, storage option, or dependency flavor. Native catalogs expose those details but change with engine versions. Durable tooling deliberately uses a portable core plus small versioned adapters.

## Prerequisites and Retrieval

Retrieve relation schemas, keys, foreign keys, views, indexes, types, functions, roles, privileges, transactions, directed graphs, topological ordering, and cryptographic digests. Distinguish logical schema metadata from physical statistics and runtime telemetry.

You should understand that a metadata query observes a database through a role and transaction. It may not see uncommitted DDL in another session, objects in another database, or definitions hidden by privilege. “The catalog returned no row” is an observation under context, not automatically universal absence.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish system catalogs, information schemas, data dictionaries, system views, and external catalogs;
2. identify tables, columns, constraints, types, indexes, routines, roles, and dependencies by stable keys;
3. explain namespace, qualification, search-path, and quoted-identifier effects;
4. reconstruct a table definition without losing column order or constraint semantics;
5. traverse dependencies and construct restrict/cascade impact plans;
6. account for snapshot, privilege, version, and database scope in introspection;
7. compare portable and engine-specific metadata interfaces;
8. compute and interpret canonical schema fingerprints;
9. design catalog queries that avoid unsafe direct mutation and textual parsing assumptions;
10. audit metadata drift and prepare version-aware migration evidence.

## Core Exposition

A **system catalog** is a set of relations maintained by the database engine. It commonly describes namespaces, relations, attributes, types, constraints, indexes, routines, operators, collations, roles, privileges, dependencies, extensions, and statistics. Some rows are database-local; others may be shared across a cluster. Engine code may rely on exact layouts and reserved identifiers, so the fact that catalog tables are queryable does not make arbitrary updates safe.

A **system view** presents selected catalog or runtime information through a supported interface. A **data dictionary** is a broader term for authoritative definitions and often includes descriptions, ownership, sensitivity, lineage, and stewardship. An enterprise data catalog may index many systems and add search or governance, but it is downstream of each database's transactional catalog and can lag.

The SQL `information_schema` is a standardized collection of metadata views. It is a good first choice for portable inventories of schemas, tables, columns, constraints, routines, and grants. Engines omit unsupported standard features and add native capabilities elsewhere. Therefore “portable” means stable common concepts, not identical row sets or exhaustive visibility.

Catalog design is naturally relational. PostgreSQL, for example, identifies many objects with object identifiers and relates `pg_class`, `pg_attribute`, `pg_type`, `pg_constraint`, `pg_index`, and `pg_depend`. SQLite stores a compact row per table, index, view, or trigger in `sqlite_schema`, including normalized creation SQL and a root page. MySQL exposes dictionary information largely through read-only `INFORMATION_SCHEMA` views. These are different implementation contracts, not interchangeable physical schemas.

An object needs **identity**, **name**, and **namespace**. Identity supports references across renames. A name is user-facing and may be reused after drop. A namespace scopes names and affects resolution. SQL qualification may include catalog, schema, and object; current database and search path fill omitted parts. Quoted identifiers preserve product-defined case and characters, while unquoted identifiers are folded. Tooling should use identifiers returned by the engine and safe identifier-quoting APIs rather than concatenate strings.

Relations and columns usually occupy separate catalog rows. A column record needs parent relation identity, ordinal position, name, type identity plus modifiers, nullability, default/generation expression, collation, and lifecycle flags such as dropped or hidden. Sorting by name corrupts declared order. Filtering dropped/system columns requires documented predicates that can change across versions.

Logical constraints and their supporting indexes must remain distinct. A primary or unique constraint may own an index; an expression or partial index may not correspond to a constraint. Foreign-key metadata connects referencing and referenced columns in positional order. Joining only by a constraint name is unsafe where names need not be schema-global; use the full engine key.

Definitions may be stored structurally, as text, or both. Text is useful for display and replay but difficult to analyze universally because quoting, defaults, expression trees, qualification, extensions, and version syntax matter. Prefer engine deparser functions or structured catalog joins. Never run catalog text from an untrusted database without review.

Dependencies form a directed graph. If view `v` reads table `t`, then `v -> t`. If constraint `fk` belongs to child `c` and references parent `p`, it may depend on both. A restrictive drop of `t` checks for reverse edges and refuses when surviving objects require it. Cascade computes reverse reachability and applies dependency-type rules. Some dependent objects are internal parts that disappear automatically; others are separately owned and require explicit cascade.

Not every semantic dependency is discoverable. A stored query parsed into an engine expression can record its referenced objects. Dynamic SQL assembled from strings may name a table only at runtime, so static dependency tracking cannot see it. External applications, reports, data exports, and service contracts are also outside the database graph. Catalog impact analysis is necessary but not sufficient.

DDL is a state transition over both catalogs and storage. Transactional behavior varies by engine and operation. Within one transaction, a session may see its catalog changes while other sessions retain earlier snapshots or block. DDL can invalidate plans and caches. Introspection for migration evidence should record before/after transaction boundaries and avoid mixing rows collected at different schema versions.

Metadata visibility is security-sensitive. Standard views often show only objects the current role owns or has privileges on. Routine bodies, role credentials, row policies, storage paths, and connection definitions may require stronger access or redaction. An inventory service should use a purpose-built least-privilege role and label which fields are unavailable, rather than silently substitute null or absence.

Catalog statistics are metadata but not schema truth. Row counts, distinct estimates, histograms, correlation, page counts, and last-analyzed times can be approximate or stale. Query optimizers consume them; governance tools must not present estimates as exact counts. Runtime views for locks, sessions, I/O, and replication are observations, not durable catalog definitions.

Comments and annotations connect technical objects to human meaning. They should identify ownership, grain, units, sensitivity, retention, and deprecation where supported. A comment is not an enforced constraint, authorization policy, or lineage proof. External governance metadata needs synchronization and provenance back to an engine object identity/version.

Schema drift detection begins with a canonical projection. Select semantically relevant fields, normalize ordering, distinguish absent from hidden/unavailable, and include engine/adapter version. Hashing that representation detects difference efficiently; it does not explain the difference, prove authorization, or establish that either side is correct. Retain a human-readable diff and migration record.

Major upgrades can change catalog schemas, identifiers, dependency flavors, or deparser output. Avoid `SELECT *` in durable tooling. Pin supported engine ranges, probe capabilities, query documented interfaces, test fixtures for each supported version, and fail explicitly on unknown object kinds rather than dropping them from inventory.

The safest mutation rule is simple: read catalogs through documented views/tables and change schema through supported DDL. Direct system-catalog writes can bypass validation, storage work, dependency maintenance, cache invalidation, logging, or recovery invariants. A database superuser's ability is not evidence of safety.

## Definitions and Notation

Let catalog graph `G=(V,E)` contain typed objects `V` and directed dependencies `E`.

- Object `o` has internal identity `id(o)`, kind `kind(o)`, namespace `ns(o)`, name `name(o)`, and owner `owner(o)`.
- Qualified name `q(o)` is a presentation/resolution tuple, not a durable substitute for `id(o)`.
- Edge `(u,v)` means dependent `u` requires referenced `v`.
- `dependents(v)={u | (u,v) in E}`.
- Cascade closure is the least set `C` containing target `v` and every object whose dependency reaches an object in `C`, subject to engine dependency semantics.
- A valid drop order is a topological order of the induced reverse dependency graph: dependents precede referenced objects.
- Metadata observation is `M(engine_version,database,role,snapshot,search_path)`.
- Fingerprint `H(Canon(M))` is meaningful only for the declared canonical projection and context.

Cycles can exist through mutually dependent constructs or faulty external metadata. Destructive planning must detect them and apply engine-specific grouped-drop or rejection rules rather than recurse forever.

## Mechanisms, Invariants, or Proof Structure

An introspection workflow should:

1. record engine/version, database, role, transaction, and search path;
2. enumerate namespaces and objects with stable identities;
3. join attributes and definitions using catalog keys and ordinal positions;
4. enumerate ownership, privileges, constraints, indexes, and dependencies;
5. mark unavailable fields and product-specific extensions;
6. validate references, uniqueness, order, and dependency cycles;
7. derive impact plans without executing them;
8. compare a canonical snapshot with intended migrations;
9. retain readable diffs and evidence;
10. mutate only through reviewed DDL and re-introspect afterward.

The finite model below validates unique object identities and qualified `(namespace,name,kind)` keys, contiguous column ordinals, existing dependency targets, and acyclicity. It derives a dependency-safe cascade plan, produces a privilege-filtered analyst view, and verifies that a canonical digest is stable but changes after a rename.

<!-- bijux-verify: {"id":"finite-catalog-graph","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"catalog_valid=True\ncolumn_ordinals_valid=True\ncycle_free=True\ndrop_plan=('customer_pk', 'customer_read', 'order_customer_fk', 'customer')\nanalyst_visible=('app', 'customer', 'customer_read')\ndigest_stable=True\ndigest_changes=True\ninjected_cycle_detected=True\n","stderr":""}} -->
```python
import hashlib


objects = (
    {"id": 1, "kind": "schema", "namespace": "", "name": "app", "columns": (), "depends": (), "visible": ("owner", "analyst")},
    {"id": 10, "kind": "table", "namespace": "app", "name": "customer", "columns": ((1, "customer_id", "integer"), (2, "email", "text")), "depends": (1,), "visible": ("owner", "analyst")},
    {"id": 11, "kind": "constraint", "namespace": "app", "name": "customer_pk", "columns": (), "depends": (10,), "visible": ("owner",)},
    {"id": 20, "kind": "view", "namespace": "app", "name": "customer_read", "columns": ((1, "customer_id", "integer"), (2, "email", "text")), "depends": (10,), "visible": ("owner", "analyst")},
    {"id": 30, "kind": "table", "namespace": "app", "name": "orders", "columns": ((1, "order_id", "integer"), (2, "customer_id", "integer")), "depends": (1,), "visible": ("owner",)},
    {"id": 31, "kind": "constraint", "namespace": "app", "name": "order_customer_fk", "columns": (), "depends": (30, 10), "visible": ("owner",)},
)


def catalog_valid(catalog):
    identities = [item["id"] for item in catalog]
    qualified = [(item["namespace"], item["name"], item["kind"]) for item in catalog]
    known = set(identities)
    references = all(set(item["depends"]) <= known for item in catalog)
    return len(identities) == len(set(identities)) and len(qualified) == len(set(qualified)) and references


def ordinals_valid(catalog):
    for item in catalog:
        ordinals = [column[0] for column in item["columns"]]
        if ordinals != list(range(1, len(ordinals) + 1)):
            return False
    return True


def has_cycle(dependencies):
    visiting = set()
    visited = set()

    def visit(node):
        if node in visiting:
            return True
        if node in visited:
            return False
        visiting.add(node)
        if any(visit(required) for required in dependencies.get(node, ())):
            return True
        visiting.discard(node)
        visited.add(node)
        return False

    return any(visit(node) for node in dependencies)


def drop_plan(catalog, target):
    by_id = {item["id"]: item for item in catalog}
    reverse = {item["id"]: [] for item in catalog}
    for item in catalog:
        for required in item["depends"]:
            reverse[required].append(item["id"])
    planned = []
    seen = set()

    def plan(node):
        if node in seen:
            return
        seen.add(node)
        for dependent in sorted(reverse[node], key=lambda value: by_id[value]["name"]):
            plan(dependent)
        planned.append(by_id[node]["name"])

    plan(target)
    return tuple(planned)


def digest(catalog):
    rows = []
    for item in sorted(catalog, key=lambda value: value["id"]):
        columns = ",".join(f"{position}:{name}:{kind}" for position, name, kind in item["columns"])
        dependencies = ",".join(str(value) for value in sorted(item["depends"]))
        rows.append(f"{item['id']}|{item['kind']}|{item['namespace']}|{item['name']}|{columns}|{dependencies}")
    return hashlib.sha256("\n".join(rows).encode()).hexdigest()


dependencies = {item["id"]: item["depends"] for item in objects}
analyst = tuple(item["name"] for item in objects if "analyst" in item["visible"])
renamed = tuple(({**item, "name": "client"} if item["id"] == 10 else dict(item)) for item in objects)

print(f"catalog_valid={catalog_valid(objects)}")
print(f"column_ordinals_valid={ordinals_valid(objects)}")
print(f"cycle_free={not has_cycle(dependencies)}")
print(f"drop_plan={drop_plan(objects, 10)}")
print(f"analyst_visible={analyst}")
print(f"digest_stable={digest(objects) == digest(objects)}")
print(f"digest_changes={digest(objects) != digest(renamed)}")
print(f"injected_cycle_detected={has_cycle({10: (20,), 20: (10,)})}")
```

The graph is intentionally small. The cycle checker and drop planner treat every edge uniformly, whereas real engines distinguish normal, automatic, internal, extension, partition, shared, and pinned dependencies. The digest model omits privileges and definitions, so it cannot serve as a production schema fingerprint. The analyst view is a fixture, not a simulation of an engine's grant closure.

## Alternatives and Trade-Offs

**Information schema:** Prefer for portable inventory and common tooling. It is privilege-filtered and incomplete for product-specific features.

**Native catalogs:** Prefer for exact engine operations, dependency analysis, planner metadata, partitions, policies, and extensions. Pin engine versions and isolate queries behind adapters.

**CLI describe commands:** Useful interactively, but formatted output is unstable for automation. Trace the documented catalog/deparser interfaces they use.

**DDL text parsing:** Sometimes required for offline files or engines exposing only text. Use a versioned parser and preserve quoting; do not replace structured catalog facts with regular expressions.

**External enterprise catalog:** Adds cross-system search, lineage, stewardship, and classification. It is a replicated metadata product with freshness, identity mapping, and reconciliation obligations.

**Polling versus DDL events/logs:** Polling is simple but detects change late and can be expensive. DDL event capture is timely but product-specific and still needs snapshots, retention, replay, and gap recovery.

**Name-based versus identifier-based state:** Names make reviews readable and migrations portable; internal identifiers make same-instance joins and rename tracking precise. Durable tooling records both and defines how drop/recreate breaks identity.

## Failure Modes and Misconceptions

1. Treating catalogs as optional documentation rather than engine state.
2. Mutating system catalogs directly because they look like ordinary tables.
3. Joining objects only by unqualified name.
4. Persisting internal identifiers as cross-cluster portable identity.
5. Assuming names survive rename, drop/recreate, or namespace moves.
6. Sorting columns alphabetically instead of by ordinal position.
7. Confusing constraints with their supporting indexes.
8. Losing composite-column order in keys and foreign keys.
9. Parsing stored DDL text without engine/version grammar.
10. Assuming `information_schema` exposes every extension or policy.
11. Treating privilege-filtered absence as nonexistence.
12. Running inventory with unnecessary superuser access and leaking definitions.
13. Mixing catalog rows from different transactions or schema versions.
14. Assuming runtime estimates are exact durable metadata.
15. Ignoring dynamic SQL and external consumers in dependency analysis.
16. Executing `CASCADE` before enumerating reverse transitive closure.
17. Recursing forever on a dependency cycle.
18. Treating a digest mismatch as proof that production is wrong.
19. Treating a matching digest as proof of semantic or data equivalence.
20. Using `SELECT *` against version-changing system catalogs.
21. Silently ignoring unknown object kinds after upgrade.
22. Forgetting comments, grants, policies, collations, generated expressions, or extensions during reconstruction.
23. Assuming DDL transactional visibility is identical across engines.
24. Trusting an external catalog without source position and reconciliation status.

## Worked Examples

### Example 1

**Situation:** Two schemas contain a table named `events`. **Reasoning:** A join by table name conflates them; use catalog/database identity plus schema and object key. **Conclusion:** Names require namespace context.

### Example 2

**Situation:** A table is renamed but retains its engine object identity. **Reasoning:** Identifier-based dependencies continue to point to it while a name-only diff shows delete/add. **Conclusion:** Report rename and identity separately; do not assume every engine preserves identity across every DDL path.

### Example 3

**Situation:** A reconstructed table lists columns alphabetically. **Reasoning:** Positional inserts, composite definitions, and human review change. Catalog ordinal position is authoritative for declared order. **Conclusion:** Order metadata is semantic for reconstruction even when relational predicates use names.

### Example 4

**Situation:** `customer_read` depends on `customer`. **Reasoning:** Restrictive drop finds a reverse dependency and refuses. Cascade must remove the view first. **Conclusion:** Dependency direction and reverse reachability govern destructive change.

### Example 5

**Situation:** A SQL function constructs `SELECT * FROM ` plus a runtime table name. **Reasoning:** The engine cannot necessarily record that table dependency from stored text. **Conclusion:** Catalog closure under-approximates dynamic and external dependencies.

### Example 6

**Situation:** An analyst's `information_schema.tables` query omits payroll. **Reasoning:** The view filters by accessible objects; a privileged inventory confirms payroll exists. **Conclusion:** Record observation role and distinguish hidden from absent.

### Example 7

**Situation:** A unique constraint and unique index both mention email. **Reasoning:** The constraint declares integrity and may own the index; another unique expression index has different null, predicate, and foreign-key eligibility semantics. **Conclusion:** Do not collapse object kinds because their storage mechanism overlaps.

### Example 8

**Situation:** A schema hash changes after an engine upgrade with no intended DDL. **Reasoning:** Deparser formatting or adapter fields may have changed. Compare structured semantic fields and adapter versions before declaring drift. **Conclusion:** Fingerprints are contracts over canonicalization, not universal object identities.

### Example 9

**Situation:** A migration wants to drop a type. **Reasoning:** Traverse columns, routines, casts, defaults, and views that depend on it; inspect dynamic/external uses; produce a reviewed topological plan. **Conclusion:** The affected set is larger than tables named in the migration.

### Example 10

**Situation:** An enterprise catalog shows yesterday's owner after an emergency transfer. **Reasoning:** The database catalog is transactionally authoritative; external ingestion watermark reveals lag. Reconcile and alert according to metadata freshness SLO. **Conclusion:** Catalogs about catalogs also need provenance and freshness.

## Cross-Program Connections

- [Programming Languages and Semantics](../../01-programming-languages-and-semantics/ROADMAP.md) explains symbol tables, names, types, binding, and reflection.
- [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) connects dependency graphs, ownership, and migration boundaries.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) governs metadata visibility, least privilege, secrets, and policy discovery.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) consumes schemas, lineage, watermarks, and external catalogs.
- Later DBE modules use catalogs for plans, statistics, storage, constraints, transactions, recovery, replication, and upgrades.

## References

1. PostgreSQL Global Development Group, [PostgreSQL 18 System Catalogs](https://www.postgresql.org/docs/18/catalogs.html), official documentation, checked 2026-08-30. Catalog-as-relations architecture and engine-owned metadata scope.
2. PostgreSQL Global Development Group, [PostgreSQL 18 Information Schema](https://www.postgresql.org/docs/18/information-schema.html), official documentation, checked 2026-08-30. Standardized portable views, feature limits, and privilege-sensitive metadata.
3. PostgreSQL Global Development Group, [`pg_depend`](https://www.postgresql.org/docs/18/catalog-pg-depend.html), official documentation, checked 2026-08-30. Native object identifiers and dependency flavors used for drop semantics.
4. PostgreSQL Global Development Group, [Dependency Tracking](https://www.postgresql.org/docs/18/ddl-depend.html), official documentation, checked 2026-08-30. Restrict/cascade behavior and limits involving function bodies.
5. SQLite Project, [The Schema Table](https://www.sqlite.org/schematab.html), official documentation, checked 2026-08-30. Compact `sqlite_schema` representation, stored DDL, root pages, and mutation warnings.
6. Oracle, [MySQL 8.4 `INFORMATION_SCHEMA` Introduction](https://dev.mysql.com/doc/refman/8.4/en/information-schema-introduction.html), official documentation, checked 2026-08-30. Read-only metadata views, privilege filtering, portability, extensions, and performance.
7. PostgreSQL Global Development Group, [`pg_description`](https://www.postgresql.org/docs/18/catalog-pg-description.html), official documentation, checked 2026-08-30. Object/column description identity and human-facing catalog annotations.

## Exercises

### Exercise 1

Explain why `(schema_name, table_name, column_name)` is useful for presentation but may be unsafe as durable same-instance identity across rename and drop/recreate.

### Exercise 2

Given edges `view_v -> table_t`, `index_i -> table_t`, `constraint_c -> table_t`, and `report_r -> view_v`, derive a valid cascade drop order for `table_t`.

### Exercise 3

An inventory query returns no row for `secret.payroll`. Design checks that distinguish true absence, wrong database/search path, privilege filtering, uncommitted DDL, and adapter incompatibility.

### Exercise 4

Compare `information_schema` and native catalogs for a cross-engine schema-diff tool that must understand portable columns plus PostgreSQL partial indexes.

### Exercise 5

Design a production metadata snapshot and drift audit, including canonical fields, observation context, security, version handling, reconciliation, and evidence required before repair.

## Answers to the Exercises

### Answer 1

The qualified names are readable and often portable, but rename changes the tuple without changing the object, while drop/recreate can reuse the same tuple for a different object. Same-instance dependency joins should use documented internal identities and retain qualified names for display. Cross-instance migration needs a logical identity mapping because internal identifiers are not portable. Record operation history to classify rename versus replacement.

### Answer 2

The report depends transitively on the view, so one valid order is `report_r`, `view_v`, `constraint_c`, `index_i`, then `table_t`; the independent constraint/index order may swap. Every dependent precedes the object it references. Real execution must apply engine dependency flavors because owned indexes or constraints may drop automatically and external `report_r` may not appear in the engine catalog.

### Answer 3

Query an explicitly selected database with fully qualified identifiers; record engine/version, transaction, role, and search path. Use a purpose-built privileged inventory role or compare with an authorized administrator without exposing sensitive definitions. Check whether another session's DDL is committed and whether the observation snapshot predates it. Probe expected catalog columns/object kinds and fail on unsupported versions. Return states such as present, absent-with-authoritative-scope, hidden, snapshot-stale, and adapter-unsupported rather than one empty result.

### Answer 4

Use `information_schema` for common schemas, tables, columns, types, nullability, and constraints, mapping standard fields into a portable model. Add a versioned PostgreSQL adapter joining native relation/index catalogs for predicate, expression, access method, included columns, and validity. Preserve extension fields in a namespaced section and compare them only between compatible engines/versions. Unknown fields or kinds are explicit unavailable results, not equality.

### Answer 5

Observe inside a deliberate transaction and record engine build, database, role, search path, snapshot/position, adapter version, and unavailable fields. Canonicalize stable object identities plus qualified names, kinds, ordered columns, types/modifiers, defaults/generation, constraints, indexes, dependencies, owners, grants, policies, comments, and extensions; redact secrets. Sort by stable keys, serialize deterministically, hash, and retain the readable snapshot. Compare against the approved migration output at the same semantic scope, classify changes, inspect dynamic/external dependencies, and require reviewed DDL plus backup/rollback evidence before repair. Re-introspect after DDL and never repair through direct catalog writes.
