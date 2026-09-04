---
module_id: LSDS-074
program: Large-Scale Data Systems Engineering
level: 2
module_number: 74
title: Schema Evolution at Scale
status: complete
last_verified: 2026-09-04
---

# Schema Evolution at Scale

## One-Page Review

### Governing question

How can a large analytical table change fields, types, requiredness, defaults, and nested structures while historical files remain immutable, concurrent readers and writers use different software versions, metadata statistics remain interpretable, and downstream contracts fail explicitly rather than silently changing meaning?

### Essential definitions

- A **logical schema** is the table-level set of identified fields, types, nullability, defaults, and nesting rules presented to readers and writers.
- A **physical schema** is the column layout encoded in one data file under the rules active when that file was written.
- A **field identity** is a stable ID or mapping token that survives rename and reorder and is never reused for a different semantic field.
- A **writer schema** describes values encoded in an existing file; a **reader schema** describes values requested now.
- **schema resolution** maps writer fields and types into a reader schema, supplying permitted defaults or nulls and applying defined promotions.
- A **compatible change** preserves declared read/write obligations for the supported client population without rewriting all historical data.
- **type widening** moves values into a target type that can represent the source domain under explicit conversion rules.
- A **non-additive change** drops, renames, narrows, reinterprets, or restructures a field rather than only adding an optional field.
- A **protocol feature** advertises required reader/writer capabilities for interpreting table state.
- A **schema epoch** is a governed interval in which one schema version and compatibility policy apply to a producer or consumer cohort.

### Central model, mechanism, or theorem

Let file $f$ carry writer schema $W_f$, snapshot $s$ expose logical schema $R_s$, and $\rho(W_f,R_s)$ be the resolution function. A metadata-only evolution is safe only if every retained file has a defined, meaning-preserving resolution:

$$\forall f\in F_s:\ \rho(W_f,R_s)\text{ is defined and policy-compliant}.$$

Stable field identity makes rename and reorder changes to presentation rather than reassignment of stored values. Adding an optional field resolves historical rows to null or a specified initial default; dropping a field hides it but does not make its physical bytes another field; widening applies only approved value-preserving conversions. Requiredness changes, defaults, nested collections, timestamps, decimals, statistics, partition sources, CDC, and older clients add separate obligations. A schema commit must atomically publish the new schema and required protocol capabilities, then writers refresh before encoding new files.

### Critical invariants

- Every logical and nested field has a stable identity that is never reused for a different field.
- Every file remains bound to the writer schema, field mapping, partition specification, and protocol under which it was written.
- Name and position are presentation attributes unless the format explicitly defines them as physical identity.
- Reader/writer resolution is deterministic, typed, version-aware, and explicit for absent, null, defaulted, promoted, and unsupported values.
- A metadata-only change never mutates historical files or causes their bytes to be interpreted as a different semantic field.
- Type promotion preserves the source value domain under the format's exact rules; narrowing or semantic reinterpretation requires validation and usually rewrite.
- A new required field is not accepted until all historical and incoming rows can supply a valid value under documented default/backfill semantics.
- Pruning statistics are decoded using the type and field identity that produced them; unknown or incompatible metrics weaken pruning rather than exclude data.
- Protocol capability changes prevent unsupported clients from reading or writing instead of silently ignoring semantics.
- Evolution audit connects request, old/new schema IDs, field IDs, compatibility decision, affected clients/files, rollout gates, backfill, and rollback.

### Common failures

Common failures include binding columns by ordinal; dropping `amount` then reusing the name for a different concept; treating rename as drop-plus-add; widening timestamps without defining zone semantics; increasing decimal scale as if it only increased precision; making a field required while old files lack it; confusing read defaults with write defaults; allowing automatic source-driven evolution to ingest misspellings; decoding old min/max bytes as the current physical type; changing map-key equality; enabling a feature before inventorying clients; letting stale writers commit old encodings after evolution; and declaring success because one current engine can read the latest snapshot.

### Compact example

Schema 7 has field ID 12 named `customer_id` with type `int` and optional field ID 19 named `note`. Schema 8 renames ID 12 to `account_id`, widens it to `long`, drops ID 19, and adds optional ID 25 `region`. Old files still encode ID 12 as 32-bit integers and ID 19 bytes. A reader projects ID 12 into `account_id` and promotes each value, ignores ID 19, and returns null or the declared initial default for absent ID 25. A new `note` field must receive a new ID; reusing 19 could expose deleted historical values. Old bounds for ID 12 must be decoded as their writer type before comparison in the widened domain.

### Connections

[LSDS-008](008-serialization-across-workers.md) establishes encoding contracts, [LSDS-020](020-selecting-storage-layouts-for-large-analytical-workloads.md) supplies immutable files, [LSDS-050](050-reprocessing-a-stream-without-double-applying-effects.md) supplies migration replay, [LSDS-069](069-federated-query.md) exposes cross-source type differences, [LSDS-071](071-table-snapshots-and-atomic-commit.md) supplies atomic schema publication, [LSDS-072](072-manifest-and-metadata-trees.md) supplies typed statistics, and [LSDS-073](073-optimistic-concurrency.md) supplies concurrent validation.

## Governing Question

At petabyte scale, rewriting every file to rename a column or add an optional field is usually unacceptable. It consumes enormous I/O, competes with production workloads, creates new failure and correctness surfaces, and may take longer than the business can wait. Metadata-driven tables therefore resolve old physical schemas into a current logical schema.

That convenience hides a distributed protocol. Files may span years of writer versions. Long-running queries pin older snapshots. Streaming jobs cache schemas. Catalogs, query engines, CDC readers, ML feature jobs, BI extracts, and external sharing clients upgrade at different times. A change that works in one engine may break another or alter downstream meaning without a read error.

The governing question is how to preserve field identity and value meaning across this heterogeneity, how to decide which changes are metadata-only versus rewrite-required, how to advertise capability changes, and how to deploy evolution with evidence, concurrency control, and recovery.

## Why This Matters

Schema is both data interpretation and organizational contract. A field name may appear in SQL, but its meaning also lives in IDs, physical encodings, null/default behavior, units, privacy classification, lineage, quality rules, partition transforms, indexes, metrics, and consumer expectations. Updating only a catalog string leaves these dependencies inconsistent.

Silent schema bugs are unusually durable. An ordinal reader can swap two columns and emit plausible values. Name reuse can make old deleted bytes appear under a new definition. A timezone reinterpretation can shift events without type errors. A decimal conversion can round monetary data. Automatic evolution can turn a producer typo into a permanent public field.

Safe evolution improves autonomy when it makes compatible changes cheap and incompatible changes explicit. It requires a compatibility matrix, stable identity, capability inventory, rollout sequencing, data/profile checks, canaries, dual-read comparison, and a plan for historical rewrite when metadata cannot preserve semantics.

## Prerequisites and Retrieval

Review serialization in [LSDS-008](008-serialization-across-workers.md), file layout in [LSDS-020](020-selecting-storage-layouts-for-large-analytical-workloads.md), replay-safe processing in [LSDS-050](050-reprocessing-a-stream-without-double-applying-effects.md), federation in [LSDS-069](069-federated-query.md), snapshot commits in [LSDS-071](071-table-snapshots-and-atomic-commit.md), metadata trees in [LSDS-072](072-manifest-and-metadata-trees.md), and optimistic validation in [LSDS-073](073-optimistic-concurrency.md).

You should understand primitive and nested types, logical versus physical encoding, nullability, defaults, stable IDs, reader/writer schemas, schema resolution, type domains, decimals, timestamps and time zones, lists/maps/structs, column statistics, protocol negotiation, CDC, stream checkpoints, backfills, canary releases, and data contracts.

Before changing a production table, retrieve all historical schema IDs, file-format/field mappings, active snapshots and branches, partition source fields, required protocol features, writer/reader versions, long-running jobs, stream checkpoints, views, UDFs, CDC consumers, exports, policy tags, quality constraints, and representative values near type boundaries.

## Learning Objectives

After this module, you should be able to:

1. Separate logical schemas from physical file schemas and reader/writer resolution.
2. Explain why stable field identity makes rename, reorder, and safe deletion possible.
3. Classify add, drop, rename, reorder, requiredness, type, and nested changes.
4. Prove value preservation for an approved widening and reject unsafe conversions.
5. Distinguish initial/read defaults from write defaults and backfilled values.
6. Preserve statistics, partition, delete, and CDC interpretation through evolution.
7. Coordinate schema changes with concurrent and stale writers.
8. Build a client capability inventory and staged rollout plan.
9. Design rewrite migrations when metadata-only evolution is insufficient.
10. Verify evolution using fixtures, dual reads, boundary values, and audit evidence.

## Core Exposition

### Logical, physical, writer, and reader schemas

Snapshot metadata identifies a current logical schema. Each immutable file has a physical schema and a writer schema context. On read, an engine resolves requested logical fields against stored fields. Resolution may project, reorder, rename through identity, supply absent values, and promote types. It must not guess.

For file $f$, define $W_f$ as its writer schema and $R_s$ as the requested schema at snapshot $s$. Resolution $\rho(W_f,R_s)$ produces a conversion plan or a typed incompatibility. A table can contain files written by many schemas; “the table schema” alone is insufficient for debugging an old-file failure.

### Stable identity

Position-based identity treats the first stored field as the first logical field. Reorder then swaps meaning. Name-based identity makes rename look like deletion plus addition and makes name reuse dangerous. Stable field IDs separate identity from presentation.

Adding a field allocates an unused ID, including nested fields. Rename changes the label, not the ID. Reorder changes presentation, not identity. Drop removes an ID from the current schema but does not erase historical bytes. Re-adding the same name allocates a new ID. IDs are never recycled because retained files may still contain the old one.

Identity has to travel through every layer: table metadata, file schema or mapping, manifests and statistics, partition specs, delete files, projections, CDC schema tracking, caches, and connector APIs. One ordinal-only bridge can undo the guarantee.

### Add, drop, rename, and reorder

Adding an optional field is commonly metadata-only. Historical records lack it, so readers return null or an initial default according to the format's resolution semantics. New writers use the new schema. An automatic evolution policy should restrict who may add fields, validate names and types, attach ownership/classification, and detect near-duplicate typo names.

Dropping hides a field from the current logical schema. It does not immediately remove physical bytes, statistics, encryption exposure, or retained-snapshot access. Privacy deletion therefore requires a separate rewrite and retention process. Rename and reorder are metadata-only only when stable mapping exists and every relevant client honors it.

### Defaults and requiredness

Defaults answer different questions. An **initial/read default** supplies a value for historical rows in which the field is absent. A **write default** supplies a value when a new writer omits the field. A backfill materializes values into rewritten files. These are not interchangeable.

Changing optional to required needs proof that every visible row resolves to a non-null value and every active writer supplies one. A default may make resolution syntactically non-null while still violating business meaning. Use profiling, constraint validation, writer rollout, quarantine, and often backfill. Changing required to optional is generally easier for readers but may break consumers whose generated types assume non-null.

### Type evolution

Let $D(T)$ be the representable semantic domain of type $T$. A widening from $T_0$ to $T_1$ is value-preserving when there is injective conversion $g:D(T_0)\rightarrow D(T_1)$ consistent with comparison, equality, hashing, ordering, and serialization obligations relevant to the table.

Integer-to-wider-integer and float-to-double are common approved promotions, but even apparently wider conversions need exact format rules. Integer-to-float can lose precision. Decimal precision and scale are separate: increasing precision at fixed scale expands range; increasing scale changes the numeric representation and downstream rounding assumptions. String-to-number is parsing, not widening. Timestamp-without-zone to timestamp-with-zone requires an external zone assumption and is semantic reinterpretation.

Narrowing requires evidence that all visible and incoming values fit, a defined overflow/rounding policy, and usually file rewrite. Scan not only row values but statistics, defaults, partitions, indexes, delete keys, and downstream stores.

### Nested collections

Nested struct fields need stable IDs just like top-level fields. Adding an optional struct member can be compatible; moving a field into or out of a struct changes its path and often resolution semantics. Lists need element identity and nullability rules. Maps are especially constrained: changing key structure or equality can make existing entries unreachable, merge distinct keys, or corrupt partition/hash semantics.

Document whether null collection, empty collection, null element/value, and absent field are distinct. Generated client types and JSON exports often collapse these cases differently.

### Statistics and pruning

Manifest and file statistics were encoded under a historical field type. After promotion, a current reader must decode each bound using the writer type, then promote into the comparison domain. Reading four-byte integer bounds as eight-byte long bounds is not safe. Truncated strings, NaN, null counts, signed bytes, decimals, and timestamp units need versioned rules.

If a reader cannot interpret old statistics, it must retain the file and weaken pruning. It may not treat the statistic as empty or compare raw bytes under the new type. After a rewrite, verify new metrics against source values and ensure mixed old/new files prune identically for boundary predicates.

### Partition, sort, delete, and index dependencies

A schema field may source a partition transform, sort key, equality delete, uniqueness key, materialized index, clustering rule, row-level policy, or masking expression. Changing or dropping the field requires inspecting those dependencies. Even an approved primitive promotion may change hashing or transform behavior in some systems.

Do not silently remove an identity merely because it is hidden from projection. Delete application and row matching may still need it. Partition evolution deserves its own metadata mechanics; schema evolution must at least preserve source IDs and reject incompatible transformations.

### Protocol and client capability

Some changes require a table feature, minimum reader/writer version, or column mapping mode. Inventory clients before activation: batch and streaming engines, libraries, query services, CDC, sharing, maintenance, catalog crawlers, backup/restore, and emergency tools. “Main production engine supports it” is not enough.

Gate writers first when their old output would violate the new contract, or gate readers first when new files require new decoding. Often the safe order is deploy capable but inactive clients, verify adoption, block old writers, commit the feature/schema, canary new writes, validate all readers, then expand. Required features should make old clients fail explicitly.

### Concurrency and cached schemas

A schema update is an OCC transaction. It validates the current schema/protocol and publishes atomically. A writer that staged files under schema $k$ must refresh before commit and prove compatibility with schema $k+1$. Appending old-schema files may be safe after an optional addition; it may be unsafe after a required field, mapping, type, or protocol change.

Long-lived streams cache encoders and checkpoints. Define refresh boundaries, schema epoch in checkpoint state, restart/upgrade behavior, and handling of records spanning epochs. A schema registry notification is advisory unless commit validation prevents stale writers.

### Migration when metadata is insufficient

For narrowing, semantic reinterpretation, physical deletion, incompatible nested change, or removal of a protocol feature, build a rewrite migration. Define source snapshot, target schema, row conversion, reject/quarantine policy, deterministic keys, quality constraints, reconciliation, incremental catch-up, cutover, and rollback.

Choose in-place snapshot rewrite or shadow table. In-place preserves identity but increases conflict and rollback complexity. A shadow table isolates work and enables dual reads but needs CDC/catch-up, grants, aliases/views, lineage, and atomic or coordinated cutover. Retain the old representation until audit and rollback windows close.

### Observability and verification

Record schema changes and failures by table, old/new schema ID, operation, field IDs, client/version, snapshot, and error class. Track files/bytes by writer schema, stale-writer rejection, resolution fallback, unknown statistics, cast failure, overflow, null/default rates, reader incompatibility, CDC lag, rewrite progress, reconciliation deltas, and rollback readiness.

Build golden files for every historical schema and boundary values. Run old/new readers where policy permits, current readers over old/new/mixed files, and current writers against pre/post-change heads. Compare row counts, keyed values, aggregates, null/default distributions, predicate results, partition pruning, delete application, and CDC output. Test unsupported clients for explicit failure.

## Definitions and Notation

Let:

- $S_k$ be logical schema version/ID $k$;
- $F_s$ be files reachable from snapshot $s$;
- $W_f$ be file $f$'s writer schema and physical mapping;
- $R_s$ be the reader schema exposed by snapshot $s$;
- $\rho(W_f,R_s)$ be schema resolution;
- $id(x)$ be stable field identity;
- $D(T)$ be a type's semantic value domain;
- $g_{a\rightarrow b}$ be a conversion from type $T_a$ to $T_b$;
- $C_r$ and $C_w$ be supported reader and writer client sets;
- $cap(c)$ be capabilities of client $c$;
- $req(S_k)$ be required capabilities of schema/protocol $S_k$;
- $N_{null}$, $N_{default}$, $N_{cast}$, and $N_{reject}$ be observed null, default, cast, and rejected records in a defined cohort;
- $H_k$ be files written with schema $k$.

Client compatibility requires $req(S_k)\subseteq cap(c)$ for every client claimed supported. Value-preserving widening requires an injective, defined conversion for every source value, plus preservation of the operations the table contract relies upon. File compatibility requires $\rho(W_f,R_s)$ for every retained file, not merely the latest writer cohort.

Metrics require scopes. A null rate may include true source nulls, absent historical fields resolved to null, failed parses coerced to null, or masked values; report these separately. Cast success on sampled recent files does not prove all historical values are representable.

## Mechanisms, Invariants, or Proof Structure

### Identity-preservation argument

Suppose logical field $x$ retains ID $i$ through rename/reorder. Every file mapping and statistic identifies stored values by $i$, so reader projection changes only presentation. Dropping $i$ removes it from the current projection. A later same-name field receives $j\ne i$, so historical $i$ values cannot resolve into $j$. Reusing $i$, or resolving by name/position, breaks the proof.

### Widening argument

For promotion $T_a\rightarrow T_b$, establish that $g$ is defined and injective over all $D(T_a)$ values admitted by the table and preserves required equality/order/hash semantics. Historical values are decoded as $T_a$, converted by $g$, and compared in $T_b$. If any value collapses, overflows, rounds, changes zone meaning, or hashes inconsistently where hashing matters, the change is not a metadata-only widening under that contract.

### Add-field resolution

Let new field $j$ be absent from $W_f$. Resolution returns null or declared initial default $d_j$ for historical row $r$. New writer schemas encode $j$ or apply a write default. The table must distinguish absence-derived $d_j$ from a materialized source value when lineage or future default changes matter. A required claim needs proof that resolution never yields null.

### Mixed-schema equivalence

For a migration, define canonical projection $P$ into target semantics. For every source file/row $r$, compare $P(\rho(W_f,R_{new})(r))$ with the rewritten target row. Reconcile keyed multisets and important aggregates, not just counts. Exercise boundary values, nulls, defaults, nested values, delete keys, and predicates. Sampling supports confidence; only full-domain constraints or complete scans prove universal value fit.

### Rollout safety argument

Before schema activation, every client in supported set has required capabilities, stale writers are fenced or commit-validated, and recovery tools can interpret both old and new states. Atomic metadata publication creates the schema serialization point. Canaries prove observed behavior for selected cohorts, while compatibility fixtures cover historical encodings. Rollback must account for new files already written; reverting only the schema pointer may not make them readable by old clients.

## Alternatives and Trade-Offs

**ID-based mapping** makes rename/reorder safe and name reuse unambiguous but requires IDs across formats and connectors. **Name mapping** is readable but makes rename and case rules risky. **Ordinal mapping** is compact and fast but fragile under reorder and insertion.

**Strict enforcement** rejects unexpected producer fields/types and protects contracts. **Automatic evolution** accelerates ingestion but can publish typos, unowned data, incompatible types, or sensitive fields. Constrain automation to approved additive cases with budgets and alerts.

**Metadata-only evolution** is cheap and preserves historical files but depends on resolution capability and may increase mixed-schema complexity. **Rewrite evolution** normalizes physical data and enables incompatible changes but consumes I/O, creates migration risk, and delays completion.

**In-place rewrite** preserves table identity and grants. **Shadow-table migration** offers isolation and dual validation but requires catch-up and coordinated cutover. Select based on size, write rate, rollback, lineage, and consumer topology.

**Backward compatibility** lets new readers consume old data. **Forward compatibility** lets old readers handle new data. **Full compatibility** requires both and limits change. Choose and document obligations for reader/writer directions rather than using “compatible” without a subject.

**Defaults** avoid nulls for historical rows but may invent business facts. **Null** preserves absence but burdens consumers. **Backfill** materializes a derived or authoritative value but needs provenance and recomputation rules.

## Failure Modes and Misconceptions

1. **“Rename is cosmetic.”** It is safe only when identity does not depend on name.
2. **“Reorder is harmless.”** Ordinal readers can swap values.
3. **ID reuse after drop.** Historical bytes reappear as a different field.
4. **Add-required without history.** Old rows cannot resolve a valid value.
5. **Default equals backfill.** A read-time substitution is not stored evidence.
6. **Any larger type is wider.** Precision, scale, zone, comparison, and hashing can change.
7. **String conversion is promotion.** Parsing introduces invalid and ambiguous values.
8. **Latest files prove compatibility.** Old schema cohorts may contain boundary cases.
9. **Current schema decodes old statistics.** Historical bound encodings can differ.
10. **Unknown metrics mean no values.** They require conservative pruning.
11. **Dropping removes sensitive bytes.** Files and retained snapshots still contain them.
12. **Nested moves are renames.** Path and collection semantics may change.
13. **Map-key evolution is ordinary.** Equality changes can collapse or lose entries.
14. **Main engine defines the ecosystem.** CDC, streams, maintenance, and recovery clients also matter.
15. **A protocol flag upgrades software.** It only advertises or enforces requirements.
16. **Notification prevents stale writers.** Commit validation or fencing is required.
17. **Schema rollback is pointer rollback.** New physical encodings may remain.
18. **Automatic evolution is always resilient.** It can make producer defects permanent contracts.
19. **Counts prove migration equality.** Substitutions and value corruption preserve counts.
20. **One successful query completes rollout.** Mixed snapshots, old files, boundary values, and all supported clients require evidence.

## Worked Examples

### Example 1

Field ID 7 is renamed from `zip` to `postal_code`. ID-aware readers project old and new files into `postal_code`. A name-based export sees a removal and addition; it needs an explicit mapping or versioned downstream contract.

### Example 2

Field `age:int` becomes `age:long`. Old files and four-byte bounds are decoded as integers, then promoted. Decoding raw bounds directly as eight-byte longs is invalid even though the logical type is now long.

### Example 3

An optional `country` field is added with initial default `UNKNOWN`. Historical reads return that value, but it does not mean the country was observed. Governance records provenance as default-derived until a validated backfill supplies source facts.

### Example 4

A producer emits `custmer_id`. Unrestricted automatic evolution adds it beside `customer_id`, splitting data. An allowlist and similarity alert quarantine the batch instead of changing the public schema.

### Example 5

Decimal `(10,2)` to `(14,2)` expands range at fixed scale. `(10,2)` to `(12,4)` adds fractional precision but reduces integer digits from eight to eight—not a general range expansion—and changes rounding expectations. Follow the format's exact permitted rule.

### Example 6

A timestamp without zone is reinterpreted as UTC. Historical values created in Stockholm local time shift meaning. This is a semantic migration requiring a zone rule and validation, not a metadata-only widening.

### Example 7

A field used as an equality-delete key is hidden from user projection. Dropping its identity from delete planning makes deleted rows visible. Dependency analysis retains its interpretation until deletes and affected files are rewritten or expired safely.

### Example 8

A streaming writer cached schema 11 before optional field 30 was added in schema 12. Its old-schema append may remain compatible. If schema 12 activates a required writer feature, commit validation rejects it and directs the job to refresh/restart.

### Example 9

A shadow migration converts strings to integers. Rows `"17"`, `"0017"`, `"+17"`, `"17.0"`, empty, and out-of-range values test parsing policy. Keyed reconciliation records rejected and normalized variants; row-count equality alone would conceal substitutions.

### Example 10

The executable fixture resolves old field IDs through rename, drop, widening, and an added optional field.

<!-- bijux-verify: {"id":"schema-id-resolution","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"account_id=42\naccount_type=long\nregion=null\nnote_visible=no\nreused_id=no\n","stderr":""}} -->
```python
writer_row = {12: 42, 19: "legacy note"}
reader_schema = {
    12: {"name": "account_id", "type": "long"},
    25: {"name": "region", "type": "string", "default": None},
}

resolved = {
    spec["name"]: writer_row.get(field_id, spec.get("default"))
    for field_id, spec in reader_schema.items()
}

print(f"account_id={resolved['account_id']}")
print(f"account_type={reader_schema[12]['type']}")
print(f"region={'null' if resolved['region'] is None else resolved['region']}")
print(f"note_visible={'yes' if 19 in reader_schema else 'no'}")
print(f"reused_id={'yes' if 19 in reader_schema else 'no'}")
```

## Cross-Program Connections

- **Type systems:** subtyping, coercion, optionality, variance, and refinement help state compatibility precisely.
- **Database systems:** catalog schemas, MVCC, DDL transactions, constraints, generated columns, and online migration supply operational patterns.
- **Serialization:** Avro-style reader/writer resolution, Parquet physical types, logical annotations, and field IDs govern file interpretation.
- **Distributed systems:** atomic publication, OCC, stale clients, epochs, fencing, capability negotiation, and rollback govern rollout.
- **Streaming:** checkpoints, schema registries, CDC events, long-running encoders, and replay make evolution stateful.
- **API engineering:** backward/forward compatibility, deprecation, consumer-driven contracts, and versioning mirror table evolution.
- **Data governance:** classifications, lineage, deletion, defaults, semantic ownership, and audit determine whether a technically readable change is acceptable.
- **Testing and reliability:** golden fixtures, boundary generation, dual reads, reconciliation, canaries, fault injection, and SLOs provide evidence.

## References

1. Apache Iceberg, [Table Format Specification](https://iceberg.apache.org/spec/). Current. Defines stable field IDs, schema evolution, promotion, defaults, and statistics decoding.
2. Apache Iceberg, [Schemas](https://iceberg.apache.org/docs/1.9.0/schemas/). Versioned. Describes logical types, field identity, and supported promotions.
3. Apache Iceberg, [Evolution](https://iceberg.apache.org/docs/1.5.0/evolution/). Versioned. Explains add, drop, rename, reorder, update, and correctness goals.
4. Apache Iceberg, [Spark DDL](https://iceberg.apache.org/docs/latest/spark-ddl/). Current. Documents schema-changing operations and catalog constraints.
5. Delta Lake, [Column Mapping](https://docs.delta.io/delta-column-mapping/). Current. Documents rename/drop without rewrite, protocols, and streaming limitations.
6. Delta Lake, [Type Widening](https://docs.delta.io/delta-type-widening/). Current. Defines supported promotions, feature requirements, and compatibility limits.
7. Delta Lake, [Table Batch Reads and Writes](https://docs.delta.io/delta-batch/). Current. Documents schema enforcement and automatic evolution behavior.
8. Delta Lake, [Feature Compatibility](https://docs.delta.io/versioning/). Current. Defines reader/writer protocols and table features.
9. Delta Lake, [Change Data Feed](https://docs.delta.io/delta-change-data-feed/). Current. Documents schema behavior and non-additive-change limitations.
10. Apache Hudi, [Schema Evolution](https://hudi.apache.org/docs/schema_evolution/). Current. Documents schema-on-read evolution support and constraints.
11. Apache Avro, [Specification](https://avro.apache.org/docs/current/specification/). Current. Defines schema resolution, aliases, defaults, and type promotion.
12. Apache Parquet, [Logical Types](https://github.com/apache/parquet-format/blob/master/LogicalTypes.md). Current. Defines physical/logical representations and compatibility expectations.
13. Protocol Buffers, [Updating a Message Type](https://protobuf.dev/programming-guides/proto3/#updating). Current. Provides a contrasting stable-field-number compatibility model.

## Exercises

### Exercise 1

A field ID 8 named `cost` is dropped. A year later, a new business concept is also named `cost`. What identity must it receive, and what should historical files return for the new field?

### Exercise 2

Classify these proposed changes: `int` to `long`, `long` to `double`, `decimal(12,2)` to `decimal(16,2)`, `decimal(12,2)` to `decimal(16,4)`, and local timestamp to UTC timestamp. State what evidence is required.

### Exercise 3

A new field is declared required with read default `0`. Explain why this may satisfy mechanical resolution yet fail the business contract. Design a safer rollout.

### Exercise 4

An old file stores lower bound for field 5 as a four-byte integer. The current schema says field 5 is long. Describe correct pruning and fallback behavior.

### Exercise 5

Design a verification matrix for a rename plus type widening while batch writers, a streaming reader, CDC, and a legacy recovery tool use the table.

## Answers to the Exercises

### Answer 1

The new field receives a fresh never-used ID, say 27, not 8. Historical files contain no value for 27, so resolution returns null or the new field's explicit initial default. Old bytes for ID 8 remain associated only with the dropped historical concept and may be visible through retained old schemas/snapshots according to policy.

### Answer 2

`int` to `long` and fixed-scale decimal precision expansion are common value-preserving widenings when the table format permits them. `long` to `double` can lose integer precision. Increasing decimal scale changes representation and must follow the format's exact precision/scale rule plus downstream rounding contract. Local-to-UTC timestamp requires a zone interpretation and is a semantic migration. Verify all values/bounds/defaults, comparison/equality/hash use, partition/delete dependencies, client capabilities, and the authoritative format rules rather than relying on type names.

### Answer 3

Resolution can emit non-null `0` for every old row, yet zero may mean a measured value rather than unknown. Inventory semantics, add the field optional, deploy capable writers, populate authoritative new values, distinguish default-derived provenance, backfill historical rows, validate non-null and domain constraints, update consumers, then make required if the format and all clients support it. Preserve rollback across new physical writes.

### Answer 4

Decode the four bytes using the historical writer type `int`, promote the resulting number to `long`, then compare in the current predicate domain. Do not decode the raw bytes as an eight-byte long. If writer type or encoding cannot be established, mark the bound unusable and retain the file; correctness takes priority over pruning.

### Answer 5

Inventory versions and capability requirements for all four client classes. Test every historical writer-schema fixture with old and new names/types; new files with upgraded readers; mixed snapshots; min/max integer values and old statistics; stream checkpoint restart across the epoch; CDC output and schema tracking; and explicit rejection by the unsupported recovery tool. Deploy support inactive, gate stale writers, commit the atomic schema/protocol change, canary writes, compare keyed rows/aggregates/predicates, monitor fallbacks/errors, then expand. Upgrade or deliberately retire the recovery tool before claiming the supported client set is compatible.
