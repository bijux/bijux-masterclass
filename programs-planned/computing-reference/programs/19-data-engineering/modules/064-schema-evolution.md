---
module_id: DE-064
program: Data Engineering
level: 2
module_number: 64
title: Schema Evolution
status: complete
last_verified: 2026-09-03
---

# Schema Evolution

## One-Page Review

### Governing question

How can an analytical table change fields, types, nullability, defaults, and nested structure while old and new files, snapshots, writers, readers, catalogs, statistics, partitions, and business meanings coexist—without silently swapping identities, inventing values, truncating data, resurrecting dropped semantics, or declaring a syntactically readable change safe for every consumer?

### Essential definitions

- A **writer schema** describes how stored data was encoded; a **reader schema** describes the shape requested when those bytes are decoded.
- **Schema resolution** maps writer fields/types to a reader projection using a serialization/table-format protocol.
- **Field identity** is the durable identifier used to match a logical field across rename/reorder. Some table formats use numeric field IDs; name-based formats use names/aliases and different hazards.
- A **schema ID/version** identifies one immutable schema definition attached to a table snapshot or record/file context.
- **Backward compatibility** means a new reader can read data written with the old schema.
- **Forward compatibility** means an old reader can read data written with the new schema.
- **Full compatibility** means both directions for the declared versions and rules.
- A **promotion/widening** maps an old type to a new type without losing any old values under exact format rules; it does not prove new values fit old readers.
- A **narrowing** reduces value space or precision and normally requires validation plus rewrite or a new contract.
- **Nullability** states whether a field may be absent/null in the logical contract; missing, null, defaulted, empty, unknown, and redacted remain distinct.
- A **read default** supplies a value when older writer data lacks a reader field. It does not necessarily rewrite stored rows or make a writer omit the field.
- A **write default** is a table/protocol rule for producing new rows when a writer omits a field; its support and materialization are format-specific.
- A **rename** changes the human name while preserving logical identity. Drop-plus-add creates a different field even if the new name matches the old one.
- **Schema enforcement** rejects writes that do not satisfy the current table contract; **schema evolution** changes that contract through an authorized metadata operation.
- **Semantic compatibility** means units, population, time, meaning, privacy, constraints, and consumer behavior remain acceptable—not merely that bytes decode.
- A **mixed-schema snapshot** contains files/records written under multiple historical schemas and is resolved through the snapshot/table protocol.

### Central model, mechanism, or theorem

Represent a schema as a mapping from stable field identity to contract:

$$
\Sigma_v:i\mapsto(name_i,type_i,required_i,default_i,meaning_i).
$$

A reader at schema $r$ interprets a record written at schema $w$ through a versioned resolution function:

$$
decode(bytes,\Sigma_w,\Sigma_r,R_{w\rightarrow r})\rightarrow row_r\ \text{or explicit error}.
$$

Compatibility is directional:

$$
Backward(n,o)\iff \forall x\in Enc(o):decode(x,o,n)\ succeeds,
$$

$$
Forward(n,o)\iff \forall x\in Enc(n):decode(x,n,o)\ succeeds.
$$

These quantify over all encodable values, not a convenient sample. Table change safety further requires storage compatibility, metadata/statistics compatibility, writer/read fleet compatibility, and semantic acceptance:

$$
Safe=Format\land Table\land Fleet\land Semantics\land Operations.
$$

### Critical invariants

- Every committed snapshot names an immutable schema ID; readers resolve each file/record using its writer context and the selected snapshot's reader schema.
- Logical fields retain stable identities across rename/reorder; dropped identities are never silently reused for different meanings.
- Add, drop, rename, reorder, promotion, nullability, default, and nested changes are separate operations with explicit compatibility direction.
- A new required field is not added over historical data without a valid format/table default or complete rewrite/backfill and validation.
- Defaults are deterministic, versioned, semantically justified, and distinguish synthetic values from observed source values where necessary.
- Narrowing, scale/timezone changes, string-to-number parsing, enum contraction, and structural moves use validated migrations or new fields/contracts rather than unsafe metadata edits.
- Compatibility is checked against every retained historical schema and every active/rollback reader and writer required by policy—not only the immediately prior schema.
- Producers do not auto-merge unreviewed source drift into production table schemas.
- Schema metadata, catalog views, file statistics, partitions, deletes, indexes, generated columns, constraints, and downstream code evolve coherently.
- Mixed-schema reads preserve null/default/type/identity semantics across all retained files and snapshots.
- Physical rewrite and logical schema change are published atomically as appropriate; failed migrations leave prior snapshots readable.
- Semantic changes to unit, grain, population, time, privacy, or meaning receive a versioned field/product contract even if physical type is unchanged.
- Protocol feature upgrades are gated across all engines/tools before new encodings are written.
- Backfill, dual-read/write, cutover, rollback, and deprecation have explicit evidence and horizons.

### Common failures

Common failures include matching columns by position; implementing rename as drop-plus-add; reusing a dropped ID/name for a new meaning; adding required fields without historical values; assuming nullable means optional in every serializer; treating a reader default as stored data; changing default values and rewriting history accidentally; narrowing long to int because current samples fit; changing decimal scale as metadata-only; changing timestamp-without-zone to timestamp-with-zone without source authority; converting string IDs to numbers and losing leading zeros; deleting enum symbols still present historically; moving fields across nested structures without format support; enabling automatic merge on typoed columns; checking only newest files; updating a catalog but not table metadata; assuming Parquet physical readability proves table compatibility; allowing old writers after new invariants; enabling field-ID features before all engines support them; and calling a renamed business concept compatible because SQL still executes.

### Compact example

Schema 7 has field ID 1 `order_id:string required`, ID 2 `amount:int required`, and ID 3 `note:string optional`. Schema 8 renames ID 2 to `amount_cents`, promotes it to `long`, drops ID 3, and adds ID 4 `country:string optional` with read default `ZZ`. An old row `{1:o1,2:1250,3:x}` resolves under schema 8 to `{order_id:o1,amount_cents:1250,country:ZZ}`: the rename follows ID 2, promotion preserves the integer, ID 3 is ignored, and ID 4 is synthesized. Reusing ID 3 for `currency` would be corruption. Schema 8 is backward-readable for this path, but an old reader expecting `int` cannot safely read every new `long`; forward compatibility fails.

### Connections

[DE-004](004-avro-protocol-buffers-and-schema-aware-serialization.md) introduces writer/reader schema resolution, [DE-008](008-schemas-nullability-and-type-fidelity.md) defines schema, nullability, and type fidelity, [DE-030](030-designing-replayable-raw-ingestion.md) preserves drifted source evidence, and [DE-063](063-table-metadata-and-snapshots.md) attaches schema IDs to snapshots. DE-065 applies the same stable-identity discipline to partition evolution; DE-066 reads historical snapshots under correct schemas; DE-069/070 cover catalog and format operations. [API-052](../../28-api-and-service-engineering/modules/052-protocol-buffers-and-schema-evolution.md) provides a complementary interface-schema perspective.

## Governing Question

Analytical tables outlive application deployments. A table can hold five years of files written by dozens of producer versions while queries run with current schemas. Historical snapshots may retain old schemas; streams and caches may lag; external engines may interpret metadata differently.

Schema evolution is the controlled relationship among these versions. It is not simply `ALTER TABLE` success. That statement may update only catalog metadata, may commit a table-format schema, may trigger rewrite, or may be unsupported by some readers. Retrieve the exact behavior.

The fundamental distinction is writer versus reader schema. Stored bytes were encoded with one schema. A query requests another. A serialization and table protocol decides how fields match, what types promote, what missing fields do, and whether the read fails.

Stable field identity makes rename and reorder safe in formats that support it. If readers match by position, reorder can exchange meanings. If they match only by name, rename can look like one field disappeared and another appeared. A numeric ID helps only when every writer preserves it and every reader honors it.

Compatibility is directional and scoped. Adding an optional/defaulted field may let new readers consume old data, while old readers ignore the new field only if their protocol allows it. Promoting int to long lets a new long reader consume old ints; a new writer can emit values outside the old int range.

Finally, syntax is not meaning. Renaming `gross_sales` to `revenue` while changing recognition policy needs a new semantic contract, lineage, restatement decision, and consumer migration even if both are decimals.

## Why This Matters

Mixed historical data is normal. Without schema IDs and resolution, a query may read old bytes under new assumptions, producing swapped columns, nulls, truncation, or runtime failures only when it encounters an older partition.

Silent corruption is worse than a rejected change. A position-based reader can interpret yesterday's `amount` as today's `country_code`. A reused field ID can resurrect dropped private data under a public name. A decimal-scale edit can multiply money by 100.

Defaults create facts. Filling missing `country` with `US` can bias every historical analysis. A default should often be `unknown`, with provenance showing it was synthesized. Read-time defaults may also change when queried under different schema versions, harming reproducibility unless snapshot/schema are pinned.

Schema changes affect operations beyond decoding. Partition transforms reference source field IDs; file statistics encode type-specific bounds; equality deletes identify fields; indexes and generated columns depend on expressions; catalogs cache schema; BI extracts and ML features may bind names/order/types.

Automatic schema merge is especially dangerous. A producer typo such as `amout` can become a permanent new column. Unexpected nested payloads can expand catalogs or expose sensitive data. Source drift belongs in raw evidence and a reviewed evolution workflow.

Rollback is asymmetric. After new writers emit a widened long, an old int reader may fail even if metadata is rolled back. After dropping a field, old files may still contain its bytes; after physical rewrite/cleanup, restoration may be impossible. Plan data compatibility, not only metadata reversal.

Good evolution reduces full rewrites and downtime. Additive and identity-preserving changes can coexist across files. Incompatible changes still need deliberate new-field, new-table/product, dual-write, rewrite, or consumer-version strategies.

## Prerequisites and Retrieval

Retrieve table context: stable table ID, format/protocol version, current and retained snapshot/schema IDs, catalog schema, file formats, field IDs, partition/sort specs, properties, constraints, generated columns, deletes/indexes, branches/tags, and retention.

Retrieve every historical schema required by current reads, time travel, rollback, audit, streams, and backups. Do not infer history from the current catalog definition.

Retrieve producer fleet: jobs/connectors/engines and exact versions, writer schema source, schema enforcement/evolution flags, field-ID preservation, null/default behavior, write mode, auto-merge, retry, and rollout/rollback window.

Retrieve consumer fleet: query engines, BI tools, extracts, APIs, notebooks, ML training/serving, exports, stream readers, caches, ORM/code generation, positional/name/ID binding, projections, wildcard use, and refresh behavior.

Retrieve field contracts: stable identity, name/aliases, description/meaning, owner, physical/logical type, required/nullability, read/write/initial defaults, units/scale/precision, timezone/precision, enum/code domain, constraints, classification, and deprecation.

Retrieve proposed change: add/drop/rename/reorder/move/promote/narrow, nested container change, requiredness/default, meaning/unit, generated expression, field-ID assignment, affected schema IDs, and intended compatibility direction/horizon.

Retrieve data evidence: null/missing distribution, min/max and outliers, decimal precision/scale, string parse failures, leading zeros, invalid Unicode, timestamps/zones/ranges, enum symbol frequencies, nested/container shapes, corrupt files, and all retained history—not a sample of current rows alone.

Retrieve downstream dependencies: SQL views, `SELECT *`, ordinal loads, UDFs, partition expressions, statistics/indexes, delete fields, quality rules, lineage, contracts, semantic models, dashboards, features/models, exports, access/masking/retention policies, and documentation.

Retrieve migration mechanics: compatibility checker, canary snapshot/table, dual-read/write, shadow computation, backfill/rewrite, atomic schema/snapshot commit, source freeze/fence, consumer acknowledgments, rollback boundary, deprecation, and physical cleanup.

Distinguish source drift from authorized evolution; writer schema from reader schema; file schema from table schema; catalog display schema from table metadata; name from field identity; absence from null; read default from stored/write default; widening from conversion; physical compatibility from semantic compatibility; old-reader/new-writer forward from new-reader/old-writer backward; metadata rollback from data rollback; and drop from erasure.

Create an evolution contract:

| Concern | Required decision and evidence |
|---|---|
| Identity | Stable field ID/name/aliases, nested path, no reuse and ownership |
| Direction | Old writer→new reader, new writer→old reader, retained versions and exact rules |
| Values | Full domain, null/missing/default, bounds, precision/scale/timezone and invalid path |
| Storage | File encodings, mixed-schema resolution, statistics, deletes, partitions and indexes |
| Fleet | Every reader/writer/tool version, binding behavior, feature gate and fence |
| Semantics | Meaning, unit, population, privacy, constraints, metric/model impact and owner |
| Migration | Canary, dual path, rewrite/backfill, atomic publish, validation and rollback |
| Lifecycle | Deprecation, historical schemas/files, erasure, holds and cleanup |

Write a falsifiable claim: “Schema 18 adds nullable `country` ID 41 with explicit unknown read default, renames ID 12 `amount` to `amount_cents`, and promotes ID 12 int→long under the table specification; all retained schemas 1–17 and 23 active/rollback clients pass directional compatibility and mixed-file tests; every writer below release X is fenced before long values exceed int range; snapshots retain exact schema IDs; partition/delete/index dependencies were checked; shadow queries reconcile counts, null/default cohorts, money totals, and consumer outputs; rollback is allowed only before the first out-of-int-range write; and field IDs 7 and 19 remain permanently reserved after drop.”

## Learning Objectives

After completing this module, you should be able to:

1. distinguish writer, reader, file, table, catalog, and consumer schemas;
2. calculate backward, forward, and full compatibility for exact retained versions;
3. preserve stable field identity through add, drop, rename, reorder, and nested evolution;
4. reason precisely about promotions, narrowing, decimals, timestamps, enums, containers, nullability, and defaults;
5. test mixed-schema snapshots, statistics, delete artifacts, partitions, indexes, and generated expressions;
6. prevent unreviewed drift and unsafe automatic schema merge;
7. inventory and gate all writers, readers, tools, and protocol features;
8. choose additive fields, aliases, dual-write, rewrite, new table/product, or breaking-version strategies;
9. execute canary, shadow, backfill, cutover, rollback, deprecation, and cleanup with evidence; and
10. separate syntactic readability from semantic, privacy, and operational compatibility.

## Core Exposition

### Resolve writer and reader schemas explicitly

Every stored record/file has a writer context, whether embedded in an Avro container, stored in Parquet metadata, registered externally, or attached through table metadata. The reader requests a projection under a selected table snapshot/schema.

Resolution matches fields and recursively resolves types under the relevant protocol. Avro is name/alias based and specifies reader/writer resolution and defaults. Iceberg uses stable field IDs throughout table schemas and data files. Delta column mapping can enable metadata-only renames/drops under its feature requirements. Hudi documents its supported write- and experimental read-time evolution paths. Do not generalize one system's rules.

When reading a mixed-schema snapshot, resolve each file/record from its writer schema to the pinned reader schema. Do not assume current schema describes physical column order or presence in every file.

Persist schema IDs/digests in lineage and run evidence. A query result without the selected schema is not reproducible when defaults, aliases, or meanings evolve.

### Define compatibility direction and horizon

Backward means new software/schema reads old data. Forward means old software/schema reads new data. Full means both. Some registries reverse terminology in configuration descriptions or scope it to producers/consumers; always write the actual direction.

Compatibility can be transitive across all retained versions or only adjacent. Checking schema 18 against 17 does not prove it reads schema 3. Retention, rollback, delayed producers, archives, and time travel determine the required version set.

Quantify over the allowed value domain. Long-to-int is not forward compatible merely because current long values fit. A future writer may emit $2^{40}$. Runtime samples support migration validation, not schema-level proof.

Build a matrix with writer versions as rows and reader versions as columns. Mark specification-compatible, implementation-tested, semantically accepted, unsupported, or unknown. Unknown blocks the claimed direction.

### Use stable field identity

Names are for people; IDs are durable identity where the format supports them. A rename preserves ID and changes name. Reorder changes presentation position, not identity. Drop removes the ID from current schema but historical files retain it. Add allocates a never-used ID.

Never implement rename as drop old plus add new. That loses continuity, reads old values as absent/default, and can apply new meaning to old bytes if IDs/positions are reused.

Name-based protocols need aliases and exact implementation support. Aliases can help reader resolution but may be optional in some implementations and do not automatically update SQL, catalogs, BI fields, policies, or semantic meaning.

Nested structures require identity at every level. Moving fields between a parent and nested struct is not generally equivalent to rename/reorder and may be forbidden. Arrays/maps add element/key/value identity and nullability rules.

Reserve dropped IDs and, where collision would confuse old clients, names/aliases. A dropped field may remain in old files, statistics, encryption policies, and snapshots until cleanup.

### Add fields with honest missing semantics

Adding an optional/nullable field is often backward-readable because historical rows lack it. The reader supplies null or a declared default. This does not mean old writers understand the new field or new constraints.

A default is a semantic decision. `country='US'` asserts something about every historical row; `country='UNKNOWN'` may be more honest but still affects groupings. Consider a separate provenance flag or derivation version when synthetic values matter.

Serializer defaults and table defaults differ. Avro defaults are used by readers for missing writer fields and do not make the field optional during encoding. Table formats may distinguish initial defaults for historical rows and write defaults for future omissions. Retrieve exact behavior.

Adding a required field requires all historical reads and writers to supply a valid value. Safe options include add nullable, backfill under a new snapshot, validate no missing values, then strengthen requiredness if supported; or create a new table/product contract.

Default expressions involving current time, random values, mutable lookups, or session state are not reproducible. Materialize them at a defined boundary or pin all dependencies.

### Drop and rename without losing meaning

Dropping hides a field from the current schema. It may not remove bytes from historical files or snapshots, statistics, backups, or logs. Privacy erasure requires reachability/rewrite/retention action beyond metadata drop.

Before drop, find consumers, partitions, sort orders, equality deletes, generated columns, constraints, masks, lineage, and exports. Deprecate and observe usage through the full consumer refresh/rollback horizon.

Rename preserves identity only under table/format support and compatible clients. Old name-bound consumers break even if file reads remain correct. Provide compatibility views/aliases or dual-name product versions, but avoid two writable names for one field without clear authority.

A name can be reused only if no retained schema, reader, cache, query, or exported contract can confuse it. Permanent reservation is often cheaper than proving universal absence.

### Promote numeric types by exact rule

Widening is protocol-specific. Common safe examples include int→long and float→double; decimal precision can sometimes increase only with unchanged scale. Check table format, file encoding, statistics, engine, and vectorized reader support.

Mathematically, old value domain must embed in the new domain without changing meaning:

$$
V_{old}\subseteq V_{new},\qquad convert(x)=x\ \forall x\in V_{old}.
$$

Floating promotion preserves representable old float values when decoded to double but does not make approximate arithmetic exact. Integer→float can lose precision at large magnitudes even when a serialization spec permits promotion.

Narrowing needs a predicate over all retained/new values, failure/quarantine policy, and usually rewrite or new field. Even if values fit, old file statistics and encodings may remain incompatible with metadata-only change.

Prevent old writers after widening if they could truncate or reject new-domain values on read-back. Rollback horizon ends when new values exceed the old domain unless a reverse transformation exists.

### Treat decimals, time, and strings as semantic types

Decimal is $(precision,scale)$ plus currency/unit/rounding meaning. Increasing precision at the same scale may preserve values; changing scale changes representation and possibly rounding. Validate physical encodings and every engine.

Timestamp types encode instant/local/calendar semantics, unit precision, and sometimes timezone adjustment. Converting timestamp-without-zone to instant/timestamp-with-zone requires source zone and ambiguity rules. Metadata cannot recover missing authority.

Date→timestamp adds time-of-day assumptions. Millisecond→microsecond can represent old values, while reverse loses precision. Calendar reform, daylight folds/gaps, leap handling, and engine session zones can change observed values.

String→numeric is parsing, not widening. Leading zeros, signs, whitespace, locale separators, overflow, invalid values, identifiers, and privacy classification need explicit disposition. Prefer a new typed field plus retained raw value during migration.

Binary↔string requires encoding and Unicode validity. UUID, JSON, variant, geometry, and interval logical types require protocol-specific metadata and reader support.

### Evolve enums, unions, and containers carefully

Adding an enum symbol may let new readers consume old data, but old readers may fail on the new symbol. Removing a symbol breaks historical data that contains it unless aliases/default rules explicitly cover the case.

Union evolution depends on branch ordering/matching rules. Nullable union conventions are not identical to table nullability. Test every writer branch and reader implementation.

Arrays/maps have element/key/value types and nullability. Promoting an element type may be supported while changing map key type or moving a nested field is forbidden. Stable nested IDs are necessary but not sufficient.

Changing `array<item>` to `struct<items:array<item>>` is structural migration, not reorder. Use a new field/schema/product and backfill unless the format explicitly defines resolution.

### Coordinate schema with table metadata

Schema evolution commits a new schema ID in table metadata and associates snapshots with their schemas. Historical snapshots retain their original schema context for correct time travel according to format rules.

Partition specs reference source fields/transforms. A rename with stable ID can preserve partition meaning; drop of a partition source may be restricted or require spec evolution. DE-065 treats this in detail.

Column statistics encode values by type and field identity. Type promotion can require bound reinterpretation. Iceberg's specification, for example, includes explicit qualifications for certain promotions and existing bounds. Use format libraries.

Equality deletes, deletion vectors, indexes, bloom filters, generated columns, constraints, clustering, sort orders, masks, and row-level policies may refer to fields. Inventory and validate them before commit.

Catalog synchronization must not create competing truth. Update the authoritative table protocol first through supported operations, then verify catalog/engine views. A crawler that infers schema from a sample can regress intentional definitions.

### Enforce writes and control drift

Schema enforcement rejects mismatched writers; evolution changes the accepted contract. Keep these permissions separate. Most producers should not have authority to evolve production tables.

Capture unexpected source fields/types in raw/quarantine as defined in DE-062. Generate a proposed diff with producer, sample, classification, semantics, compatibility, and owner. Review before table change.

Disable broad automatic merge or constrain it to an approved schema artifact/digest. A typo, nested explosion, or attacker-controlled keys must not allocate unbounded columns or expose data.

Validate writer schemas at job start and commit. Long-running streams need a policy for refreshing schema, checkpoint/state compatibility, and coordinated restart. A writer that loaded schema 17 cannot blindly commit after schema 18 changes requiredness or types.

### Test the whole reader and writer fleet

Inventory exact engine/library/connector versions and access paths. Include batch/stream writers, query engines, BI extracts, notebooks, export tools, ML, catalogs, optimizers, compactors, vacuum, scanners, replication, and restore utilities.

Test actual old/new files in mixed snapshots. Exercise vectorized and row readers, predicate pushdown/statistics, null/default projection, nested fields, deletes, partition pruning, caches, wildcard/ordinal selection, and round trips.

Static compatibility checkers encode only their protocol. Add semantic contract tests, historical profile scans, consumer query diffs, performance, and policy checks. Record unsupported/unknown results explicitly.

Fence incompatible writers before new schema commit or before new-domain values appear, depending on the transition. Upgrade readers first when forward compatibility is not guaranteed.

### Migrate incompatible changes deliberately

Prefer additive replacement: add a new field with a new ID/name, dual-write from one authoritative transformation, backfill historical rows, validate, migrate readers, stop old writers, deprecate old field, then drop/hide and later clean.

For broad semantic changes, create a new table/data-product version. This avoids pretending two meanings share one identity and gives consumers explicit cutover.

Backfill uses pinned input snapshot, transformation/rule/reference versions, isolated output generation, count/identity/control-total reconciliation, and atomic publication. Never rewrite current files in place.

Dual-write can diverge. Define authority, deterministic mapping, reconciliation, repair, and end date. Dual-read shadowing compares values and performance without serving production decisions.

Rollback has a data boundary. Metadata rollback works only while new files/values/features remain readable by the old contract or can be excluded safely. State the last reversible point.

### Observe, deprecate, and clean safely

Record schema proposal/approval, old/new schema IDs/digests, operation, field-ID changes, compatibility matrix, data profiles, fleet results, commit snapshot, writers fenced, consumer acknowledgments, backfill, cutover, rollback boundary, and owner.

Metrics include schema-change frequency/failures; unexpected drift; files/rows by schema; mixed-schema planning/read errors; default/null cohorts; old-writer attempts; compatibility failures; cast overflow/parse quarantine; catalog divergence; consumer use of deprecated fields; and backfill/rewrite progress.

Deprecation needs a date, owner, replacement, dependent inventory, communication, usage evidence, rollback horizon, and policy for ad hoc consumers. `SELECT *` and positional exports must be treated as dependencies even when column-level lineage misses them.

Physical cleanup follows snapshot retention and privacy policy. Dropped field bytes can remain until old files/snapshots/backups are rewritten or expired. Validate that cleaning does not invalidate retained time travel.

## Definitions and Notation

For schema version $v$, define:

- $\Sigma_v$: mapping from stable field identity to its contract.
- $i$: stable field identity; $n_i$ is current name/aliases.
- $\tau_i$: physical/logical type and parameters.
- $q_i$: required/nullability rule.
- $d_i$: read/write/initial default semantics.
- $m_i$: business meaning, unit, time, privacy, and owner.
- $Enc(v)$: all records/values validly encodable under writer schema $v$.
- $R_{w\rightarrow r}$: resolution rules from writer $w$ to reader $r$.
- $W$: required writer schema/version fleet.
- $C$: required reader/consumer schema/version fleet.
- $H$: retained historical schema/snapshot set.

Schema representation is

$$
\Sigma_v:i\mapsto(n_i,\tau_i,q_i,d_i,m_i).
$$

Backward compatibility is

$$
Backward(n,o)\iff \forall x\in Enc(o),\ decode(x,\Sigma_o,\Sigma_n,R_{o\rightarrow n})\ succeeds.
$$

Forward compatibility is

$$
Forward(n,o)\iff \forall x\in Enc(n),\ decode(x,\Sigma_n,\Sigma_o,R_{n\rightarrow o})\ succeeds.
$$

Full compatibility requires both. Transitive compatibility across retained history requires the chosen direction for every $h\in H$, not only the immediate predecessor.

A lossless type promotion requires

$$
V_{old}\subseteq V_{new}
$$

and an identity-preserving conversion for every old value. A narrowing validation over observed set $X$,

$$
\forall x\in X:x\in V_{new},
$$

does not prove compatibility for all future values in $V_{old}$.

Overall safe evolution is

$$
Safe=Format\land TableMetadata\land Fleet\land Data\land Semantics\land Operations\land Governance.
$$

The identity invariant is:

> Rename and reorder preserve stable field identity; drop retires identity; add allocates a new never-reused identity.

The resolution invariant is:

> Every value read from a mixed-schema snapshot is resolved from its actual writer schema to the pinned reader schema under explicit format rules or fails visibly.

The semantic invariant is:

> Physical readability never authorizes an unreviewed change in meaning, unit, time, population, privacy, or consumer decision behavior.

## Mechanisms, Invariants, or Proof Structure

Use this review sequence:

1. **Pin scope.** Record table ID/format/protocol, current and retained snapshots/schemas, rollback, stream, archive, and backup horizons.
2. **Inventory identity.** Capture every field ID/name/alias/nested path, type, null/default, meaning, dependency, and reserved identity.
3. **State direction.** Write old-writer→new-reader and new-writer→old-reader claims for all required versions and values.
4. **Check format/table rules.** Validate file encoding, schema metadata, statistics, partitions, deletes, indexes, constraints, catalogs, and features.
5. **Check fleet.** Test every reader/writer/tool version and binding mode with old/new/mixed files and snapshots.
6. **Check semantics/data.** Profile all retained history; validate units, domains, times, nulls, defaults, privacy, measures, and consumer outputs.
7. **Choose migration.** Use safe metadata evolution, additive field, alias/view, dual path, rewrite/backfill, or new product/version.
8. **Canary and publish.** Isolate, shadow, reconcile, approve, fence incompatible actors, commit atomically, and observe.
9. **Bound rollback/deprecation.** State last reversible point, retain old paths, migrate dependents, measure use, and communicate removal.
10. **Clean and audit.** Expire/rewrite historical bytes only under snapshot/legal/privacy policy and preserve change evidence.

Proof sketch for identity-safe rename:

1. Old schema maps stable ID $i$ to name `amount` and type $\tau$.
2. Evolution changes only the name metadata for $i$ to `amount_cents`; it does not allocate or retire an ID.
3. Every stored file identifies the physical field as $i$, and every conforming reader binds by $i$.
4. The snapshot's new schema projects $i$ under the new name.
5. Therefore old values for $i$ appear under `amount_cents`, not as a missing field or another column.
6. Reorder cannot affect this mapping because position is not identity.
7. A drop/add would fail step 2 and is not equivalent.

This proof applies only to formats/files/readers that preserve and honor stable field IDs. It does not prove semantic compatibility of the new name or compatibility for name/position-bound external consumers.

The executable demonstrates add-optional-with-default, identity-preserving rename, int→long promotion, drop, mixed-schema projection, directional compatibility, and ID-reuse rejection. It is a teaching model, not an implementation of Avro, Parquet, Iceberg, Delta, Hudi, nested types, or engine-specific defaults.

<!-- bijux-verify: {"id":"schema-identity-resolution","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"base=((1, 'order_id', 'string', True, None), (2, 'amount', 'int', True, None), (3, 'note', 'string', False, None))\nevolved=((1, 'order_id', 'string', True, None), (2, 'amount_cents', 'long', True, None), (4, 'country', 'string', False, 'ZZ'))\nchanges=('add_country', 'rename_amount', 'promote_amount', 'drop_note')\nold_as_evolved=(('order_id', 'o1'), ('amount_cents', 1250), ('country', 'ZZ'))\nbackward_compatible=True\nforward_compatible=False\nreuse_id_rejected=True\n","stderr":""}} -->
```python
base = {
    1: ("order_id", "string", True, None),
    2: ("amount", "int", True, None),
    3: ("note", "string", False, None),
}
evolved = {
    1: ("order_id", "string", True, None),
    2: ("amount_cents", "long", True, None),
    4: ("country", "string", False, "ZZ"),
}
promotions = {("int", "long"), ("float", "double")}


def can_read(writer, reader):
    for field_id, (_, reader_type, required, default) in reader.items():
        if field_id not in writer:
            if required and default is None:
                return False
            continue
        writer_type = writer[field_id][1]
        if writer_type != reader_type and (writer_type, reader_type) not in promotions:
            return False
    return True


def project(row_by_id, writer, reader):
    if not can_read(writer, reader):
        raise ValueError("incompatible")
    result = []
    for field_id, (name, _, required, default) in reader.items():
        if field_id in row_by_id:
            value = row_by_id[field_id]
        elif default is not None:
            value = default
        elif required:
            raise ValueError("missing_required")
        else:
            value = None
        result.append((name, value))
    return tuple(result)


old_row = {1: "o1", 2: 1250, 3: "fragile"}
retired_ids = set(base) - set(evolved)
new_ids = set(evolved) - set(base)
reuse_id_rejected = 3 in retired_ids and 3 not in new_ids

print(f"base={tuple((key,) + value for key, value in sorted(base.items()))}")
print(f"evolved={tuple((key,) + value for key, value in sorted(evolved.items()))}")
print(f"changes={('add_country', 'rename_amount', 'promote_amount', 'drop_note')}")
print(f"old_as_evolved={project(old_row, base, evolved)}")
print(f"backward_compatible={can_read(base, evolved)}")
print(f"forward_compatible={can_read(evolved, base)}")
print(f"reuse_id_rejected={reuse_id_rejected}")
```

The model treats an absent optional field without default as readable null and only recognizes two promotions. Production behavior must follow the exact serialization, file, table, and engine specifications.

## Alternatives and Trade-Offs

**Field IDs versus names/aliases.** IDs make rename/reorder durable across files but require end-to-end preservation and compatible tools. Names/aliases are human-friendly and common in serializers but make rename/tool behavior implementation-dependent.

**Metadata-only evolution versus rewrite.** Metadata changes avoid expensive rewrites for supported compatible changes. Rewrites can implement narrowing, structural, privacy, or encoding changes but cost compute/storage and require snapshot-safe migration.

**Nullable add versus required add after backfill.** Nullable add is operationally easy but propagates null handling. Backfill then strengthen provides a stronger contract at migration cost and may still require old-writer fencing.

**Null versus explicit default.** Null preserves unknown/missing distinction when consumers handle it. A default simplifies reads but can invent biased historical facts and obscure provenance.

**Rename versus compatibility view/alias.** Native rename preserves field identity for capable readers. Views/aliases support name-bound consumers temporarily but add dual-contract complexity and need an end date.

**Promotion versus new field.** Supported widening keeps one identity and avoids backfill. A new field is safer when unit, precision, parser, or meaning changes, at the cost of dual-write/migration.

**In-place semantic change versus versioned product.** In-place reduces visible interfaces but corrupts historical interpretation. A new product/version makes breaking meaning explicit and lets consumers migrate deliberately.

**Automatic merge versus governed proposal.** Auto-merge reduces ingestion interruption for trusted additive changes. Governed review prevents typo, sensitive-field, unbounded-nesting, and incompatible evolution; raw can preserve drift meanwhile.

**Backward-only versus full compatibility.** Backward supports upgrading readers before writers and is often sufficient for stored history. Full supports mixed rollout/rollback but restricts useful new value domains and changes.

**Transitive versus adjacent checks.** Adjacent checks are cheaper but can miss incompatibility with old retained data. Transitive checks match long history at increasing registry/test cost.

**Dual-write versus offline rewrite.** Dual-write enables gradual migration but creates divergence and reconciliation work. Offline rewrite is conceptually simpler but can require downtime or large batch cost.

**Lazy read-time conversion versus materialized backfill.** Lazy resolution avoids rewrite and preserves old files. Backfill moves cost earlier, stabilizes performance, and may be needed for unsupported/narrowing changes.

**One enterprise schema versus domain schemas.** A global schema promotes interoperability but can freeze contested meanings. Domain-owned schemas evolve faster but require explicit mappings for cross-domain products.

## Failure Modes and Misconceptions

1. **“ALTER succeeded, so the change is compatible.”** It proves one control path accepted metadata, not that files, engines, consumers, or semantics work.
2. **“Current files are enough to test.”** Old snapshots, archives, lagging streams, and rollback writers expand the compatibility horizon.
3. **“Backward and forward are obvious.”** Always write writer→reader direction; terminology is frequently reversed in conversation.
4. **“A sample proves widening.”** Schema compatibility covers all encodable values; samples only characterize observed data.
5. **“Rename equals drop/add.”** Drop retires identity and add creates another; old values can disappear or be misbound.
6. **“Position is stable identity.”** Reorder/add can swap meanings for positional readers.
7. **“Field IDs solve everything.”** Clients must preserve/honor them; semantic and name-bound dependencies still break.
8. **“Dropped ID can be reused.”** Historical bytes and readers can map it to the new meaning.
9. **“Nullable and missing are identical.”** Serializer, table, SQL, and business semantics distinguish absence, explicit null, and default.
10. **“Default is stored history.”** It may be synthesized only at read and can vary by selected reader schema.
11. **“Defaults are harmless.”** They create analytical cohorts and can invent facts.
12. **“Long values currently fit int.”** New writers may use the wider domain; old readers then fail/truncate.
13. **“Decimal scale change is widening.”** It changes representation/meaning and may require conversion/rounding.
14. **“Timestamp type change adds information.”** Missing source timezone/precision cannot be recovered by metadata.
15. **“String to numeric is a cast.”** Parsing policy, invalids, locale, overflow, leading zeros, and identifier semantics make it a migration.
16. **“New enum symbols are fully compatible.”** Old readers may not recognize values emitted by new writers.
17. **“Nested move is reorder.”** Parent/container structure affects identity and encoding; many formats forbid it.
18. **“Auto-merge prevents incidents.”** It can make typo/sensitive/unbounded drift permanent.
19. **“Catalog schema is the table.”** It may be cached/inferred/stale relative to authoritative table metadata.
20. **“Physical decode proves semantic compatibility.”** Unit, population, recognition, privacy, and consumer expectations can change while type stays constant.
21. **“Metadata rollback restores compatibility.”** New files/values/features may already be unreadable by old clients.
22. **“Drop erases data.”** Historical files, snapshots, backups, statistics, and logs can retain bytes.
23. **“SELECT * adapts automatically.”** Column count/order changes can break exports, hashes, unions, and positional consumers.
24. **“Compactors do not matter.”** Maintenance writers can rewrite with stale/incorrect schemas and must pass the same gate.

## Worked Examples

### Example 1

Add nullable field ID 41 `country_code`. Old files lack it and new readers project null; new writers can populate it. Old readers ignore it only if their protocol/tool permits extra writer fields. Backward passes; forward remains an explicit test.

### Example 2

Add required `tenant_id` without a default to a table with historical rows. New readers cannot construct the field. The team first adds it nullable, backfills from authoritative lineage, quarantines unresolved rows, validates, fences old writers, and only then considers requiredness.

### Example 3

Rename ID 12 `amount` to `amount_cents`. ID-aware readers map old bytes correctly. A BI extract bound to column name `amount` fails, so a compatibility view exists through its refresh/migration horizon. Semantic review confirms the field was already cents.

### Example 4

Drop `ssn` from current schema. Queries stop projecting it, but old files and snapshots retain bytes. Privacy erasure rewrites or expires every reachable historical file and backup under legal policy; metadata drop alone is not evidence.

### Example 5

Promote `count:int` to `long`. New readers consume old int files. Once a writer emits 4,000,000,000, old int readers cannot return safely and metadata rollback is no longer sufficient. The rollout fences old readers/writers first.

### Example 6

Change `amount decimal(12,2)` to `decimal(18,2)`. Old values embed exactly if supported. Changing to `decimal(18,4)` is not treated as the same promotion; conversion, rounding/display, statistics, and consumer totals are tested separately.

### Example 7

Local timestamp `2026-11-01 01:30` is migrated to an instant. Because the source zone enters a daylight fold, there are two possible instants. Rows without offset/source authority are quarantined or retain a new ambiguity status; the migration does not assume UTC.

### Example 8

Source field `customer_id` changes from string to integer. Values `0017`, `17`, and `A17` show that cast would collapse identity and reject valid domain values. A new numeric surrogate field is added while the string business ID remains authoritative.

### Example 9

A typo `amout` appears in one source batch. Raw captures it and schema-drift monitoring raises a proposal. Production auto-merge is disabled, so the standardized table does not gain a misleading column; remediation maps or rejects under an approved rule.

### Example 10

An engine can read new column mapping but the vacuum tool cannot. The feature gate remains closed because maintenance is a writer/destructive client. After tool upgrade, mixed-file, rename, delete, restore, and rollback tests pass before enablement.

## Cross-Program Connections

- **API and Service Engineering:** protobuf field numbers/reservation, request compatibility, additive rollout, consumer-driven contracts, and versioning mirror durable data fields.
- **Programming Languages:** structural/nominal typing, subtyping, variance, sum/product types, coercion, and total versus partial functions clarify compatibility direction.
- **Database Systems:** catalog schemas, constraints, defaults, nulls, type casts, views, online DDL, MVCC snapshots, and generated columns shape table evolution.
- **Distributed Systems:** rolling upgrades, mixed-version fleets, atomic publication, stale writers, retries, and irreversible feature gates make evolution a protocol change.
- **Information Security:** classification, masking, dropped sensitive bytes, metadata leakage, schema-change authority, and direct access affect every field lifecycle.
- **Privacy Engineering:** minimization, purpose change, inference, retention, erasure, and provenance constrain adds, semantic reuse, defaults, and drops.
- **Software Engineering:** semantic versioning, deprecation, adapters, dual-write, compatibility matrices, contract tests, and rollback boundaries govern migration.
- **Formal Methods:** domain inclusion, resolution totality, identity invariants, and quantified compatibility expose sample-based false proofs.
- **Statistics and ML:** default/null cohorts, feature distribution drift, training-serving skew, unit changes, and historical restatement can invalidate models.
- **Reliability Engineering:** canaries, shadow reads, fleet inventory, fault injection, monitoring, and recovery drills turn schema claims into evidence.

## References

1. Apache Iceberg. [Table specification](https://iceberg.apache.org/spec/). Accessed 2026-09-03. Primary specification for field IDs, schema IDs, add/drop/rename/reorder, type promotion, defaults, nested evolution, statistics, and snapshot association.
2. Apache Iceberg. [Schema evolution](https://iceberg.apache.org/docs/latest/evolution/). Accessed 2026-09-03. Primary documentation for metadata-only evolution, column identity, nested changes, type promotion, and correctness guarantees.
3. Apache Avro. [Specification 1.12.0](https://avro.apache.org/docs/1.12.0/specification/). Accessed 2026-09-03. Primary specification for writer/reader schema resolution, field matching, aliases, defaults, unions, enums, and primitive promotions.
4. Apache Parquet. [Logical types](https://github.com/apache/parquet-format/blob/master/LogicalTypes.md). Accessed 2026-09-03. Primary format specification for decimal, timestamp, integer, string, enum, JSON, UUID, and related logical annotations.
5. Delta Lake. [Delta Transaction Log Protocol](https://github.com/delta-io/delta/blob/master/PROTOCOL.md). Accessed 2026-09-03. Primary specification for table metadata/schema serialization, protocol features, column mapping, defaults, type widening, and reader/writer requirements.
6. Delta Lake. [Update table schema](https://docs.delta.io/latest/delta-batch.html#update-table-schema). Accessed 2026-09-03. Primary documentation for explicit/automatic schema updates, merge behavior, overwrite schema, and operational qualifications.
7. Delta Lake. [Delta column mapping](https://docs.delta.io/latest/delta-column-mapping.html). Accessed 2026-09-03. Primary documentation for metadata-only rename/drop, physical names, IDs, protocol upgrades, and compatibility implications.
8. Delta Lake. [Type widening](https://docs.delta.io/latest/delta-type-widening.html). Accessed 2026-09-03. Primary documentation for supported type changes, feature enablement, automatic evolution, and reader/writer compatibility.
9. Apache Hudi. [Schema Evolution](https://hudi.apache.org/docs/schema_evolution/). Accessed 2026-09-03. Primary documentation for supported write-time changes, type promotions, nullable additions, ordering hazards, and experimental schema-on-read scope.
10. Apache Hudi. [Technical Specification](https://hudi.apache.org/learn/tech-specs/). Accessed 2026-09-03. Primary specification for table-version reader/writer compatibility and upgrade ordering.
11. Confluent. [Schema Evolution and Compatibility](https://docs.confluent.io/platform/current/schema-registry/fundamentals/schema-evolution.html). Accessed 2026-09-03. Primary product documentation defining backward, forward, full, transitive, and format-specific compatibility modes.
12. Protocol Buffers. [Updating a Message Type](https://protobuf.dev/programming-guides/proto3/#updating). Accessed 2026-09-03. Primary guidance for safe field additions/removals, number reservation, wire-type compatibility, and rollout cautions in another schema system.

## Exercises

### Exercise 1

Given schema A `{1:id string required, 2:amount int required, 3:note string optional}` and proposed B `{1:id string required, 2:amount_cents long required, 4:country string optional default UNKNOWN}`, classify add, drop, rename, and promotion. Evaluate backward and forward compatibility under the module's simple rules, list semantic dependencies, and identify the rollback boundary.

### Exercise 2

Design an additive migration from `event_time_local:string` to `event_time_utc:timestamp` for data from six time zones with daylight folds/gaps and missing offsets. Include schema, authority, ambiguity, quarantine, backfill, lineage, validation, consumer cutover, and deprecation.

### Exercise 3

Create a transitive compatibility test plan for 40 retained schemas, 12 readers, 8 writers, two compactors, a vacuum tool, BI extracts, and a stream lagging seven days. State matrix dimensions, fixtures, data profiles, feature gates, and pass/fail evidence.

### Exercise 4

A team must remove a sensitive field from current and historical access while preserving a legal-hold snapshot. Design metadata drop, policy/mask, consumer migration, file rewrite, snapshot/backup handling, hold exception, erasure evidence, and prevention of ID/name reuse.

### Exercise 5

Plan a breaking unit change from meters to centimeters and a decimal change from `(12,2)` to `(18,4)`. Decide whether to evolve in place, add fields, or version the product; include dual-write, reconciliation, backfill, old-client fencing, rollback, and semantic communication.

## Answers to the Exercises

### Answer 1

ID 1 is unchanged. ID 2 is renamed while preserving identity and promoted int→long. ID 3 is dropped/reserved. ID 4 is a new optional field with read default. A new reader can read old rows: it matches IDs 1/2, promotes amount, ignores 3, and synthesizes 4, so backward passes under the model. An old reader cannot read every new long at ID 2 as int, so forward/full fail even though it may ignore ID 4 and tolerate absent optional ID 3. Check SQL/BI name dependencies, amount unit, defaults, partitions/deletes/stats/indexes, positional readers, and privacy. Rollback to int ceases to be metadata-safe once a new writer emits outside int domain or an irreversible protocol feature is used.

### Answer 2

Keep the string field and add new IDs for UTC instant, source zone/offset, parse status, and rule version. Define zone authority per source; resolve folds only with offset/source policy, handle gaps explicitly, preserve precision, and quarantine/mark ambiguity rather than assuming UTC. Backfill from a pinned snapshot with parser/timezone-database version, produce counts by status/zone/fold/gap, compare known control events, and retain row lineage. Dual-write from one deterministic function, shadow consumer queries, then migrate readers to the UTC field. Fence old writers, deprecate but retain the string through rollback/audit, and never overwrite the source evidence.

### Answer 3

Build writer-schema rows across all 40 retained versions and reader/tool columns for every required deployment/rollback version, explicitly testing old→new and new→old directions. Fixtures cover each add/drop/rename/reorder, min/max/out-of-domain numerics, null/missing/default, enums, nested containers, decimals, timestamps, stats pruning, deletes, partitions, mixed files, wildcard/ordinal BI extracts, compaction, cleanup, and stream checkpoint restart. Static format checks plus actual engine runs, semantic query/control totals, and historical full-domain profiles produce evidence. Unknown or unsupported required cells fail the gate; upgrade/fence readers first, then writers, while preserving seven-day stream and rollback horizons.

### Answer 4

Commit an authorized metadata drop with the old ID permanently reserved, remove name/alias exposure, update policies/masks/views, and migrate consumers. Enumerate every snapshot/file/statistic/index/delete/log/replica/backup containing the field. Rewrite reachable non-held histories into new files with the sensitive column removed, atomically publish, expire eligible old snapshots, and delete verified unreachable bytes/keys. The legal-hold snapshot remains protected and accessible only to the hold role; erasure status explicitly records this lawful exception and future review. Audit every artifact and prevent crawlers/auto-merge from reintroducing the name or ID.

### Answer 5

Meters→centimeters changes unit/meaning even if both use decimal, so add a new `length_cm` field/ID or publish a new product version; do not rename the old identity. `(12,2)`→`(18,4)` may change scale/rounding and is not assumed metadata-safe. Define exact conversion and rounding, dual-write from one authoritative expression, preserve original meters, backfill pinned history, reconcile identities/nulls/min/max and `cm = 100*m` within declared rounding, shadow consumers, and communicate units in catalog/metrics. Fence old clients before serving only new fields, publish atomically, state rollback before old paths stop or incompatible values appear, then deprecate under measured usage and retention.
