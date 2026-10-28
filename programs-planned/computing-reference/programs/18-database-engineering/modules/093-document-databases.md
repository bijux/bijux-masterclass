---
module_id: DBE-093
program: Database Engineering
level: 2
module_number: 93
title: Document Databases
status: complete
last_verified: 2026-09-05
---

# Document Databases

## One-Page Review

### Governing question

How should a database store and query self-describing, nested records while preserving explicit contracts for identity, schema, atomicity, indexing, evolution, distribution, and recovery?

### Essential definitions

- A **document** is a keyed aggregate represented as nested objects, arrays, and scalar values, usually with a database-specific type system richer than plain JSON.
- A **collection** groups documents under common query, validation, index, placement, and lifecycle policy.
- **Embedding** places related state inside one document; **referencing** stores identity links to other documents.
- A **path** identifies a nested field. Missing, explicit null, empty collection, and type mismatch are distinct states unless the application deliberately collapses them.
- A **document identity** is a stable key independent of mutable display fields and physical location.
- A **multikey index** derives multiple index entries from array-valued paths according to engine-specific rules.
- **Schema-on-read** means interpretation is deferred to readers; it does not mean that stored data lacks a schema or constraints.
- **Optimistic concurrency control** accepts an update only if a version precondition still holds.
- A **partition key** maps a document to an ownership domain; it determines transaction locality, fan-out, skew, and movement cost.
- A **materialized aggregate** duplicates data to serve a read shape and therefore needs a refresh and conflict contract.

### Central model, mechanism, or theorem

Model a document as a finite typed tree $d$, with stable identity $id(d)$, schema version $v(d)$, and concurrency version $q(d)$. An operation is correct only if its path semantics, precondition, validation, atomicity boundary, and postcondition are defined. Physical storage may be an LSM tree, B+ tree, heap, columnar representation, or remote service; “document database” names the logical interface and data model, not one storage mechanism.

Embedding and referencing move costs rather than removing them. Embedding makes one aggregate read and atomic update local but can duplicate data, enlarge writes, and create unbounded documents. Referencing normalizes ownership and independent lifecycle but introduces joins, fan-out, and multi-document consistency work.

### Critical invariants

- each logical entity has one stable ownership identity and an explicit uniqueness domain;
- missing, null, empty, false, zero, and type mismatch are handled deliberately in queries and indexes;
- accepted documents satisfy the validator for their declared schema version;
- update preconditions prevent lost writes when required;
- derived index entries and materialized aggregates agree with the authoritative committed version;
- document-level and multi-document atomicity claims match the exact engine, operation, and topology;
- shard routing preserves uniqueness, authorization, and transaction assumptions during movement;
- backups restore documents, indexes or rebuild rules, validators, encryption metadata, and change position coherently.

### Common failures

- treating JSON syntax as the database's complete type and equality contract;
- calling flexible schema “schemaless” and moving failures into every reader;
- embedding an unbounded event history until one hot document becomes a lock, size, and replication bottleneck;
- referencing everything and recreating an application-side distributed join;
- indexing every field, multiplying write, memory, and storage costs;
- confusing atomic update of one document with serializable multi-document transactions;
- choosing a low-cardinality or monotonic shard key that creates hot ownership;
- applying read-modify-write without a version condition;
- changing field meaning in place without mixed-version readers, backfill, and rollback;
- logging entire documents that contain secrets or regulated data.

### Compact example

Two clients read `stock=1, version=7`. Each wants one unit. Unconditional replacements can both write `stock=0` and both report success. A conditional update requiring `version=7` lets one commit `stock=0, version=8`; the other conflicts and must re-read. The document boundary makes the predicate and decrement local, but only the version precondition prevents a lost business decision.

### Connections

The previous module, [LSM-Based Key-Value Stores](092-lsm-based-key-value-stores.md), separates a common physical engine from the document abstraction built above it. The roadmap's next module, [Wide-Column Databases](../ROADMAP.md), examines a different sparse and partition-oriented model. Prerequisites include [Schemas, Keys, and Constraints](003-schemas-keys-and-constraints.md), [Composite and Covering Indexes](035-composite-and-covering-indexes.md), [Multi-Version Concurrency Control](046-multi-version-concurrency-control.md), and [Sharding and Data Placement](086-sharding-and-data-placement.md).

## Governing Question

An application receives objects whose attributes vary by product type, API version, tenant, and time. It wants to preserve nested structure, retrieve aggregates by identity, search selected paths, update parts of a record, distribute load, and evolve without a stop-the-world migration. Should that flexibility be represented as documents, and what must be made explicit so flexibility does not become ambiguity?

A document database answers more than “store JSON.” It chooses a type system, path language, equality rules, identity, validation mechanism, update algebra, atomicity scope, indexes, placement, replication behavior, and recovery format. Sound design begins with those contracts and the workload, not with an assumption that tables are rigid or documents are effortless.

## Why This Matters

Documents fit aggregates such as profiles, catalog entries, policies, device twins, content records, and session state. Related values can be read and changed together without reconstructing them from many rows. Optional and type-specific attributes can evolve without adding one nullable column per variant.

The same shape can hide costly defects. One order document may embed an ever-growing audit log. A predicate on a missing field may accidentally match explicit null. A path index may create thousands of entries for one array. Denormalized customer names may diverge across millions of orders. A cross-shard uniqueness check may not be atomic. Flexible writes can turn schema errors into delayed production failures.

Document design is therefore database engineering: define semantics, bound aggregates, place ownership, validate transitions, measure physical work, and prove recovery. Product syntax is secondary and mutable.

## Prerequisites and Retrieval

Retrieve keys, functional dependencies, normalization, secondary indexes, query planning, MVCC, isolation, write-ahead recovery, replication, sharding, and consistency models. Be able to distinguish logical schema from physical layout, and an atomic operation from a serializable transaction.

Retrieve JSON's grammar from RFC 8259: objects, arrays, strings, numbers, booleans, and null. JSON object member names are strings; implementations differ when names repeat; number interoperability is bounded by parser representations. Database document formats may add dates, binary values, decimals, object identifiers, timestamps, or min/max sentinels. State their exact encoding, comparison, and client-driver mappings.

For a concrete engine, record version, driver, wire protocol, storage engine, validation rules, collation, read/write concern, transaction settings, indexes, shard key, chunk/partition map, balancer state, replication topology, and backup method. Current product behavior must be checked against official documentation for that version.

## Learning Objectives

After completing this module, you should be able to:

1. specify a document model's types, paths, identity, missing/null, equality, and validation semantics;
2. choose embedding, referencing, or materialization from ownership, cardinality, boundedness, and transaction evidence;
3. reason about path and multikey indexes, query implication, and index-entry amplification;
4. design version-conditional updates and state exact atomicity/isolation scope;
5. evolve mixed-schema collections with readers-first rollout, backfill, validation, and rollback;
6. select partition keys and diagnose hot documents, scatter-gather, and cross-shard invariants;
7. test backup, restore, conflict, corruption, and partial-failure behavior with a reference oracle;
8. compare document, relational, key-value, wide-column, and search representations without brand shorthand.

## Core Exposition

**Define the type algebra.** A JSON-like document is a finite tree whose nodes are objects, arrays, or scalars. The database may preserve object member order or ignore it; compare numbers by numeric value or encoded type; normalize strings or use a collation; and distinguish database-specific types. These choices affect equality, unique indexes, sorting, hashing, signatures, and change detection.

Reject duplicate object keys at ingestion even if a parser accepts them. RFC 8259 notes that behavior is unpredictable across implementations when names are not unique. Canonicalization for hashing or signatures requires a defined representation; reserializing through arbitrary clients is not a canonicalization protocol.

**Treat missing as a first-class state.** For path `profile.phone`, at least four cases exist: the path is missing; it exists with null; it exists with a value; or traversal encounters an incompatible type. Query languages vary on whether equality to null matches one or more cases. Validation, partial indexes, defaults, updates, and analytics must use the same intended partition.

Do not infer absence from falsiness. Empty string, zero, false, empty array, and null may carry distinct domain meanings. If the domain intentionally collapses them, normalize at a controlled boundary and record the information loss.

**Give documents stable identity.** Identity should not depend on mutable email, display name, or array position. Define whether uniqueness is global, tenant-scoped, shard-local, or eventually checked. If a generated identifier embeds time or topology, assess information leakage, ordering hotspots, collision domain, and offline generation.

An external idempotency key is different from a document identifier. A request may create several records or retry after an unknown outcome. Persist request identity and result under a defined uniqueness/retention scope so replay does not create duplicate effects.

**Find the aggregate boundary.** Embed values that share ownership, lifecycle, access pattern, cardinality bound, and atomic update need. Reference independently owned, shared, high-cardinality, independently secured, or independently changing entities. These are questions, not immutable rules.

Suppose a product has ten localized names and twenty attributes. Embedding them makes a product read local and an atomic product edit simple. Embedding every view event makes document size and update contention unbounded. Store the bounded description in the product; store events under independent identities and retention/partition policy.

**Quantify growth.** Let base document bytes be $S_0$, an embedded collection receive $r$ elements per day, average encoded element size be $e$, and retention be $h$ days. Ignoring overhead and compression, expected size is $S(h)=S_0+reh$. This elementary model forces a bound. Variance, indexes, allocation, replication, and update copying require measurement beyond it.

Document size limits protect wire, memory, replication, and update paths, but designing just below a hard limit is unsafe. Operational thresholds should leave headroom for schema evolution, retries, metadata, and temporary transformation.

**Make schema explicit.** Flexible physical records still have producer and consumer expectations. A validator can require fields, types, ranges, patterns, conditional branches, and additional-property policy. JSON Schema provides a vocabulary for JSON instances, but a database validator may implement a subset or different language. Record the exact dialect and enforcement mode.

Put a schema version or otherwise deterministically infer one. Validate on every authoritative write path, including administrative scripts, restores, change consumers, and bulk imports. “Warn only” modes are observation tools, not enforcement guarantees. Monitor rejection by producer/version without logging sensitive payloads.

**Design mixed-version evolution.** For a rename from `name` to `display_name`, deploy readers that understand both, define precedence when both appear, then deploy writers for the new field, backfill idempotently with version preconditions, enforce new validation only after old writers disappear, and remove compatibility after evidence. Rollback remains possible while readers and authoritative history retain the old interpretation.

Semantic changes need more than renaming. Splitting one price number into amount, currency, and tax basis requires a conversion source and uncertainty policy. Never manufacture precision or currency from context that was not recorded.

**Specify path queries.** A path expression must define traversal through objects and arrays, missing-field behavior, type errors, numeric comparison, string collation, and array matching. “An array contains red and large” can mean one element satisfies both predicates or different elements satisfy each. Make element correlation explicit.

Projection also has semantics. Returning selected nested fields may preserve array positions, omit siblings, or reconstruct a new shape. Treat projections as typed API responses rather than byte slicing.

**Derive secondary indexes from values.** A path index maps extracted values plus document identity to candidate documents. It must track inserts, removals, type changes, array changes, collation, missing/null, and transaction visibility. The query planner may use it only when the predicate semantics imply the index's domain.

For document $d$ and indexed path $p$, let extraction yield multiset $E_p(d)$. A simple index emits roughly $|E_p(d)|$ entries, subject to deduplication and engine rules. Across paths or compound indexes, array combinations can create much greater work; concrete engines often restrict or redefine such combinations. Measure entries per document, not just document count.

**Understand multikey indexes.** If `tags=[red, sale, wool]`, a multikey index may emit three key-to-document entries. It must deduplicate document results. A compound index across arrays raises correlation and Cartesian-product questions. MongoDB, for example, documents concrete compound multikey restrictions; do not generalize them to all systems.

Array position is especially fragile. Updating the first item can change the meaning of every position-based path. Give array elements stable sub-identities when updates, authorization, or references target them.

**Use partial, sparse, and covering indexes carefully.** Indexing only documents satisfying predicate $P$ saves space and maintenance. A query is safely answered solely from that index only if its predicate implies $P$, or a residual source covers excluded documents. Missing/null/type rules make implication subtle.

A covering index avoids fetching the base document only if it contains every value needed and preserves required semantics. Large nested projections can make “covering” more expensive than fetching. Include write amplification and cache displacement in the decision.

**State update algebra.** Whole-document replacement is simple but can overwrite concurrent fields read from an old version. Path-level `$set`, increment, append, conditional removal, and array operators reduce payload but still need defined preconditions and conflict behavior. Two operators commute only under their actual domain assumptions.

An atomic increment can preserve a counter update, but “decrement if stock remains nonnegative” needs one atomic predicate-and-update or transaction. Appending to a set requires identity and deduplication. Retrying a non-idempotent increment after an unknown response can double-apply unless request identity is recorded.

**Prevent lost updates.** Store a concurrency version $q$. A replacement or patch carries expected $q$ and commits only if current $q$ matches, then advances it. On conflict, re-read and decide whether to retry, merge, or reject. Automatic fieldwise merge is unsafe for invariants such as balances, permissions, and workflow state.

ETags and conditional HTTP requests can carry this pattern across an API, but the database transaction must bind the precondition to the mutation. Checking in application code and then writing unconditionally leaves a race.

**Name the atomicity boundary.** Many document databases make one document a natural atomic unit. Some support multi-document transactions with configuration and topology constraints. Neither fact proves serializability, strict real-time order, durable acknowledgement, or cross-shard availability. State isolation, conflict detection, retry behavior, commit uncertainty, and read/write concern for exact operations.

Embedding can place an invariant inside one atomic unit, which is powerful. It should not be used to create a single unbounded “tenant document” that serializes unrelated work and cannot move or recover efficiently.

**Separate revision control from business history.** An engine revision token supports concurrency and replication; it may not be a user-visible audit log. CouchDB's documentation, for example, describes MVCC revisions and conflict behavior with specific replication semantics. If the business requires who changed what and why, create an append-only audited event/change record with retention and authorization rather than relying on internal revision garbage.

**Plan denormalization.** Duplicating customer display name into an order can preserve historical presentation or create a materialized current view. Those are different semantics. For historical copy, never “repair” it when the customer changes. For current view, define source authority, change transport, ordering, idempotency, lag objective, replay, reconciliation, and correction.

Record derived version/provenance so a repair can distinguish stale projection from intentional historical value. Periodically compare materialized documents with an authoritative recomputation under a fixed snapshot.

**Choose a partition key from operations.** A partition key should distribute sustained bytes and operations, route dominant queries, bound transactions, and remain stable. Tenant ID can make tenant operations local but creates hot large tenants. Timestamp prefixes can focus all new writes. Random hashes distribute writes but scatter range and tenant queries. Compound or bucketing schemes trade locality for balance.

Model per-key offered rate. If tenant $i$ contributes rate $\lambda_i$ and one partition sustains $\mu$, then any un-splittable key with $\lambda_i\ge\mu$ is hot regardless of total cluster capacity. Splitting requires another routing dimension and a way to execute tenant-wide operations across buckets.

**Route uniqueness honestly.** A unique index that does not include the shard key may require global coordination or may be enforceable only per shard, depending on engine. Application-side “check then insert” races. Use a globally coordinated identity service, shard-key-inclusive uniqueness, deterministic ownership, or an explicit conflict-resolution workflow.

**Treat movement as a concurrent protocol.** Rebalancing copies documents while reads and writes continue, switches routing authority, and deletes old copies later. Stable epochs, catch-up, fencing, idempotent application, and verification prevent lost or double-applied changes. Test cache and client routing during stale metadata, pauses, and retries.

**Distinguish replication models.** Leader-based replication, quorum systems, revision-tree replication, and last-write-wins expose different histories. The Dynamo paper is a useful primary source for highly available versioning and reconciliation, but it is not a description of every modern document database. Define consistency per read, write, transaction, and conflict API.

Last-write-wins may discard concurrent updates and depends on ordering metadata. Multi-value conflicts preserve alternatives but require deterministic business resolution. CRDT-like fields converge only for their defined operation algebra; placing them inside a document does not preserve arbitrary cross-field invariants.

**Account for physical storage.** A document layer may serialize a record into an LSM value, split fields across pages, or maintain columnar projections. Updating one small path can rewrite a full document at some layers plus WAL, indexes, replication, and compaction. Compression can reduce bytes while increasing CPU and update granularity.

Measure logical request bytes, base-document bytes read/written, index entries, WAL, replication, storage-engine compaction, cache, and backup separately. Do not attribute an LSM write stall to “JSON overhead,” or a huge-document copy to the index alone.

**Secure paths and operators.** Never concatenate untrusted field names or operators into a database query. Validate allowed paths and values, preserve type, use driver APIs, and authorize the exact document and subdocument operation. Object-level authorization can fail when a projection leaks a nested secret or an update operator reaches a protected path.

Encrypt transport, storage, backups, and especially sensitive fields under explicit key ownership. Field-level encryption changes which queries and indexes remain possible and can reveal equality or frequency depending on scheme. Logs, traces, rejected validators, change streams, and dead-letter records must redact documents by policy.

**Back up the complete contract.** A restorable state includes document bytes, sequence/transaction boundary, validators, indexes or deterministic rebuild definitions, collation, shard map, encryption metadata and accessible keys, users/roles, change-stream position, and product version. A filesystem copy of live files is not a backup unless the engine documents it as a consistent method.

Restore to isolated infrastructure. Verify counts and keyed digests, sample nested/type semantics, rebuild or validate indexes, exercise queries and updates, confirm authorization, resume changes without gaps/duplicates, and measure RPO/RTO. Include malformed and mixed-version documents in restoration tests.

**Benchmark representative shapes.** Vary document size/depth, field count, arrays, missing/null/type distribution, selectivity, projection width, update locality, conflict, transaction size, tenant/key skew, shard fan-out, cache state, index build, migration, backup, and failure. Run long enough for compaction, rebalancing, TTL, cache turnover, and background validation.

Report latency distributions, throughput at offered load, conflicts, retries, unknown outcomes, index entries and bytes, base fetches, examined/returned documents, scatter count, replication lag, rejected schemas, write amplification, storage, and recovery. A query that returns quickly with the wrong missing/null semantics has failed.

**Use a semantic reference oracle.** Generate bounded typed documents and operations. Compare database results with a deliberately simple model for path existence, equality, element correlation, version preconditions, and snapshots. Differentially test drivers because numeric, date, binary, and absent-value mappings can differ.

Inject concurrent replacements and patches, network loss after commit, primary change, shard move, validator deployment, index build, disk full, corrupt backup, and restore. Verify invariants rather than only process health.

The executable fixture below demonstrates a finite top-level patch plus optimistic version checking. It is not RFC 6902, RFC 7396, a database update language, a transaction engine, schema validator, index, query planner, or concurrency stress test.

<!-- bijux-verify: {"id":"finite-document-update","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"first_update=committed\nstale_update=conflict\nversion=8\nname=Ada\nphone_missing=true\ntags=database,distributed\nsource_unchanged=true\nevidence=finite_document_update\n","stderr":""}} -->
```python
def apply_patch(document, expected_version, patch):
    if document["version"] != expected_version:
        return False, document.copy()
    updated = document.copy()
    for key, value in patch.items():
        if value is None:
            updated.pop(key, None)
        else:
            updated[key] = value[:] if isinstance(value, list) else value
    updated["version"] += 1
    return True, updated

source = {
    "id": "u-17",
    "version": 7,
    "name": "Ada",
    "phone": "+46-000",
    "tags": ["database"],
}
committed, current = apply_patch(
    source, 7, {"phone": None, "tags": ["database", "distributed"]}
)
stale, ignored = apply_patch(current, 7, {"name": "stale writer"})

print(f"first_update={'committed' if committed else 'conflict'}")
print(f"stale_update={'committed' if stale else 'conflict'}")
print(f"version={current['version']}")
print(f"name={current['name']}")
print(f"phone_missing={str('phone' not in current).lower()}")
print(f"tags={','.join(current['tags'])}")
print(f"source_unchanged={str(source['version'] == 7 and 'phone' in source).lower()}")
print("evidence=finite_document_update")
```

## Definitions and Notation

- $d$ is a finite typed document tree; $id(d)$ is its stable identity; $v(d)$ is its schema version; $q(d)$ is its concurrency version.
- A **path** is an engine-defined traversal expression through object members and possibly arrays.
- **Missing** means a path has no value; **null** is an explicit scalar value. Neither is automatically equivalent to empty or false.
- A **schema** is the set of permitted representations and semantic constraints, whether enforced on write or assumed by readers.
- A **validator** checks a document or mutation against declared structural and semantic rules.
- An **aggregate** is state deliberately owned and changed as one consistency boundary.
- A **reference** is a stored identity relation whose referential and consistency behavior must be implemented.
- A **materialized aggregate** is redundant derived state optimized for a read shape.
- $E_p(d)$ is the multiset of values extracted from path $p$ in document $d$ for a specified index definition.
- A **multikey index** may emit more than one index entry per document from arrays or repeated paths.
- A **partial index** covers only documents satisfying a declared predicate.
- An **optimistic version precondition** accepts a mutation only when current version equals an expected version.
- $S_0$ is base document size, $r$ embedded elements per day, $e$ bytes per element, and $h$ retained days in a simple growth estimate.
- $\lambda_i$ is offered operation rate for routing key $i$; $\mu$ is a simplified sustainable rate of one ownership partition.
- **Scatter-gather** sends one logical query to multiple ownership partitions and combines results.
- **Revision metadata** supports concurrency or replication; **business history** records domain-significant change under audit policy.

## Mechanisms, Invariants, or Proof Structure

**Conditional-update invariant.** Assume version $q$ changes on every relevant committed mutation and comparison plus update is atomic. At most one writer expecting $q$ can commit a successor $q+1$. Later writers either observe the successor or conflict. This prevents silent overwrite; it does not decide how a conflicting business intent should merge.

**Partial-index implication.** Let index $I_P$ contain exactly documents satisfying predicate $P$. A query predicate $Q$ can use $I_P$ as its sole candidate source only if $Q(d)$ implies $P(d)$ for every permitted document. If missing/null/type semantics yield a counterexample, the plan can omit valid results. A union with another complete source may still be correct.

**Materialization convergence.** Let authoritative version for entity $x$ be $q_x$ and materialized version be $m_x$. An idempotent updater that applies only changes newer than $m_x$, plus a complete replay or reconciliation source, can converge to $m_x=q_x$ after delivery quiesces. This is not instantaneous consistency; deletion, ordering, gaps, and semantic transforms must be included.

**Aggregate-boundary reasoning.** Embedding makes a set of fields local only while the document remains one atomic and placement unit. If cardinality is unbounded, the design eventually violates a size, contention, transfer, or movement bound. Therefore every embedded collection needs either a proven maximum or a spill/reference transition with stable semantics.

**Hot-key bound.** Under an unsplittable routing key and simplified single-partition service $\mu$, if $\lambda_i\ge\mu$, no amount of unrelated partition capacity stabilizes that key's queue. The solution must reduce offered work, increase that ownership unit's service, cache safely, batch, or split the key while accepting cross-bucket costs.

**Evolution preservation obligation.** During mixed-version rollout, each supported reader must map every accepted stored version to the same intended domain meaning, or surface an explicit incompatibility. A backfill must be idempotent, version-conditioned, observable, and reversible until old writers and readers are retired. Syntactic parse success is insufficient.

**Restore invariant.** At restore point $s$, documents, indexes or rebuild rules, validators, shard metadata, and change position must describe one coherent state. Replaying after $s$ must be ordered and idempotent under transaction boundaries. Counts alone cannot prove this; compare identities, versions, hashes, queries, constraints, and change continuity.

## Alternatives and Trade-Offs

**Document versus relational.** Documents make aggregate locality and variant attributes direct. Relations make shared facts, constraints, joins, and independent updates explicit. Modern relational systems can store JSON, and document systems can support references and transactions. Choose per invariant and workload, not category mythology.

**Embedding versus referencing.** Embedding optimizes bounded local reads and atomic writes. Referencing supports independent ownership and unbounded cardinality. Materialization offers read locality with controlled duplication. Many sound models combine all three by relationship.

**Strict versus permissive validation.** Strict validation catches bad writes early but requires coordinated evolution. Permissive ingestion accepts heterogeneous data but burdens every consumer. A staged validation rollout can observe, repair, then enforce, provided the permissive interval and rejected cases are owned.

**Replacement versus operators.** Replacement yields a clear complete state but transfers and conflicts on unrelated fields. Operators reduce payload and can express atomic predicates, yet their algebra and retry behavior are more complex. Version-conditioned replacement is often safer than an unguarded patch.

**Secondary index versus materialized collection.** An index preserves one authoritative document and supports selected predicates. A materialized collection can reshape, prejoin, or precompute but creates freshness and repair work. Full-text search may belong in a search engine with explicit change and reconciliation contracts.

**Global versus local transactions.** Global transactions simplify some invariants at coordination, latency, and failure cost. Local transactions plus escrow, ownership, saga, or compensating workflow can improve availability but expose intermediate states. Choose from invariant and recovery semantics.

**Natural versus hashed partition keys.** Natural keys route domain operations but risk skew. Hashing balances exact-key traffic but destroys ordered locality. Bucketing a natural key offers a middle ground and forces fan-out for whole-entity queries.

**Native document store versus JSON in SQL.** Native stores may integrate path operations, multikey indexing, and distribution. SQL systems may combine strong relational constraints and joins with JSON fields. Evaluate exact query plans, update granularity, validation, transactions, and operations rather than syntax aesthetics.

## Failure Modes and Misconceptions

- **“Document databases are schemaless.”** Every producer and consumer assumes structure; absent enforcement merely decentralizes it.
- **“JSON is one universal type system.”** Databases and drivers differ on numeric widths, decimals, dates, binary, ordering, and duplicate keys.
- **“Embedding removes joins.”** It replaces runtime joins with duplication, larger transfer/update, or bounded aggregate ownership.
- **“References behave like foreign keys.”** They do so only if existence, deletion, update, authorization, and transaction rules enforce it.
- **“One document equals one business entity.”** Some entities are shared or unbounded; some documents materialize several entities.
- **“Atomic document update prevents all races.”** The operation must include the correct predicate and business invariant.
- **“Patch is safe because it touches one field.”** Concurrent semantics, array positions, retries, and validation still matter.
- **“Null means missing.”** Query and index behavior can differ; collapsing them loses information.
- **“An index on an array is one entry.”** It may emit many entries and require result deduplication.
- **“Every query should have an index.”** Maintenance, memory, cache, build, and storage can exceed its benefit.
- **“Transactions make embedding irrelevant.”** Placement, contention, latency, availability, and growth still differ.
- **“A random shard key solves scale.”** It can force scatter-gather and cross-shard invariants.
- **“Revision history is an audit log.”** Internal revisions may compact, omit actor intent, and expose different retention.
- **“A backup of document bytes is complete.”** Validators, indexes/rebuilds, shard state, keys, roles, and replay position matter.
- **“Flexible schema makes migration unnecessary.”** Readers and stored meaning still need controlled evolution.

## Worked Examples

### Example 1

**Situation.** Documents contain `{"x": null}`, `{}`, `{"x": 0}`, and `{"x": false}`. A feature wants only records where the user explicitly declined.

A predicate based on “not truthy” matches all four in many application languages, which is too broad. Define explicit decline as boolean false, require path existence and boolean type, and index/validate that domain. Null can mean unknown; missing can mean not yet asked; zero is a numeric value.

**Conclusion.** Path existence, type, and value are separate predicates.

### Example 2

**Situation.** A customer has five addresses shared across orders and 50,000 historical orders. Should every order embed the current address list?

No single rule fits both semantics. An order may embed the shipping address used at purchase as an immutable historical fact. The customer's current address book belongs in a referenced customer-owned aggregate. Copying all current addresses into every order creates massive fan-out and ambiguous history.

**Conclusion.** Embed historical snapshots deliberately; reference independently changing shared state.

### Example 3

**Situation.** A device document starts at 2 KB and embeds 144 measurements per day, each averaging 40 encoded bytes. Estimate size after 365 days, ignoring overhead.

$S=2{,}048+144\times40\times365=2{,}104{,}448$ bytes, about 2.10 MB decimal. Replication, indexes, keys, array overhead, variance, and update copying add cost. Multi-year retention and bursts can violate limits.

**Conclusion.** Even small elements create unbounded aggregate growth; measurements need an independent time-series lifecycle.

### Example 4

**Situation.** Two clients read profile version 12. One changes locale; the other changes legal name. Both replace the full document unconditionally.

The later replacement can restore the old value of the other field. Requiring expected version 12 makes one commit version 13 and the other conflict. A safe retry re-reads version 13 and reapplies business intent; automatic merge is allowed only if ownership and validation show the fields commute.

**Conclusion.** Field independence does not excuse an unguarded stale replacement.

### Example 5

**Situation.** A path index covers documents where `status="active"`. Can a query for `tenant=7` use it as its only source?

No. `tenant=7` does not imply active status; inactive tenant-7 documents would be missing. The index can solely answer `tenant=7 AND status="active"` if its path, missing, collation, and type semantics match. A broader query needs another complete source or union plan.

**Conclusion.** Partial-index use requires predicate implication, not superficial field overlap.

### Example 6

**Situation.** One document has `tags` with 80 values and `regions` with 40 values. A proposed compound array index conceptually pairs every tag with every region.

The naive Cartesian product is $80\times40=3{,}200$ entries for one document before metadata. Some engines prohibit or constrain parallel arrays; others define different extraction. Inspect exact rules. Often separate indexes, a bounded array of meaningful tag-region pairs, or a different model is safer.

**Conclusion.** Index-entry fan-out is a document-shape property and can dominate logical write size.

### Example 7

**Situation.** Tenant A produces 18,000 operations/s, a partition safely sustains 15,000, and 1,000 other tenants together produce 60,000 across many partitions. Routing solely by tenant ID is proposed.

Tenant A is unstable on one unsplittable ownership unit because $18{,}000>15{,}000$, regardless of spare cluster total. Add an intra-tenant bucket derived from stable object identity or workload dimension, then define fan-out, ordering, uniqueness, and transaction changes.

**Conclusion.** Aggregate cluster capacity cannot repair a hot routing key.

### Example 8

**Situation.** A service renames `name` to `display_name`. Old writers remain for one week, and a backfill runs concurrently.

Deploy dual readers first with a deterministic precedence rule. New writers write the new representation, optionally dual-writing only under a bounded protocol. The backfill updates only documents at the version it read and records schema version. Observe old-writer traffic, reconcile conflicts, then enforce the new validator and retire compatibility. Rollback keeps dual readers until evidence is complete.

**Conclusion.** Flexible storage enables mixed representations; it does not make their meaning self-reconciling.

### Example 9

**Situation.** A denormalized `customer_tier` in orders is five hours stale after a change-stream outage.

The system must know whether the field is historical or current. If current, compare each materialized source version with the authoritative customer version, replay from a gap-free position, apply idempotently, and reconcile a fixed snapshot. Until caught up, expose freshness or route decisions requiring current tier to authority.

**Conclusion.** Materialized documents need provenance, lag semantics, replay, and repair.

### Example 10

**Situation.** A restored cluster has the expected document count, but queries on decimal prices differ and change consumption restarts from an approximate timestamp.

Count equality misses type conversion and replay gaps. Compare keyed canonical digests under a specified numeric representation, validate indexes and query results, restore exact change coordinates and transaction boundaries, then replay idempotently. Verify validators, collation, roles, shard map, and encryption keys before serving.

**Conclusion.** Restore correctness is semantic and continuous, not merely a file or count check.

## Cross-Program Connections

[Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) connects aggregate ownership, bounded contexts, APIs, and evolution. A document boundary should reflect durable responsibility rather than convenient serialization.

[API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) connects JSON representations, conditional requests, idempotency, compatibility, pagination, and authorization. API documents and stored documents may deliberately differ.

[Data Engineering](../../19-data-engineering/ROADMAP.md) owns change streams, replay, schema evolution, materialization, and reconciliation pipelines. A database change feed still needs retention and consumer correctness.

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) contributes replication, conflict resolution, shard movement, membership, and partition reasoning. Document shape does not supply those guarantees.

[Security Engineering](../../25-security-engineering/ROADMAP.md) connects query injection, field authorization, encryption, secret-bearing telemetry, tenant isolation, and deletion. Nested flexibility increases the paths that policy must cover.

[Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md) connects authoritative ownership, semantic models, operational stores, materialized views, governance, and lifecycle. A document model is one representation within that system.

## References

- Tim Bray, editor, [RFC 8259: The JavaScript Object Notation (JSON) Data Interchange Format](https://www.rfc-editor.org/rfc/rfc8259), December 2017. JSON grammar, interoperability, duplicate-name, number, and encoding considerations.
- JSON Schema project, [JSON Schema Specification](https://json-schema.org/specification), current specification index checked 2026-09-05. Versioned JSON validation dialects and vocabularies.
- Paul Bryan, Kris Zyp, and Mark Nottingham, [RFC 6902: JavaScript Object Notation (JSON) Patch](https://www.rfc-editor.org/rfc/rfc6902), April 2013. A standardized patch operation model and its precondition/error concerns.
- MongoDB, [Documents](https://www.mongodb.com/docs/manual/core/document/), current manual checked 2026-09-05. Concrete BSON document, field, size, and structure behavior.
- MongoDB, [Multikey Indexes](https://www.mongodb.com/docs/manual/core/indexes/index-types/index-multikey/), current manual checked 2026-09-05. Concrete array index behavior and compound restrictions.
- MongoDB, [Transactions](https://www.mongodb.com/docs/manual/core/transactions/), current manual checked 2026-09-05. Concrete transaction scope, deployment, and operational considerations.
- MongoDB, [Sharding](https://www.mongodb.com/docs/manual/sharding/), current manual checked 2026-09-05. Concrete shard-key, distribution, routing, and balancing mechanisms.
- Apache CouchDB, [Eventual Consistency](https://docs.couchdb.org/en/stable/intro/consistency.html), current stable documentation checked 2026-09-05. MVCC, revisions, replication, and conflict behavior in a distinct document system.
- PostgreSQL Global Development Group, [JSON Types](https://www.postgresql.org/docs/current/datatype-json.html), current documentation checked 2026-09-05. JSON and `jsonb` representation, indexing, containment, and relational/document coexistence.
- Giuseppe DeCandia et al., [Dynamo: Amazon's Highly Available Key-Value Store](https://www.amazon.science/publications/dynamo-amazons-highly-available-key-value-store), SOSP 2007. Primary source for partitioned versioning, availability, and reconciliation that influenced later document/key-value systems.

## Exercises

### Exercise 1

Define document, missing, null, aggregate, embedding, reference, materialized aggregate, and multikey index. Explain why “a document is a JSON row” is insufficient.

### Exercise 2

A document starts at 6 KB and embeds 500-byte events at 2,000 events per day for 90 days. Derive the simplified final size. Then identify at least five omitted physical or operational costs and propose a bounded model.

### Exercise 3

Two workers process one payout document. Both read state `pending`, version 21; each calls an external payment provider and then conditionally changes the document to `paid`. Diagnose why document optimistic concurrency alone may still double-pay and design an idempotent workflow.

### Exercise 4

Design a model for a marketplace product with shared seller identity, bounded variants, unbounded reviews, current inventory, historical order lines, and searchable free text. Choose embedding, referencing, materialization, and index/search ownership for each, with transaction and repair implications.

### Exercise 5

A global document collection is sharded by tenant. One tenant becomes 40% of writes, usernames must be unique within a tenant, profile reads are by user ID, tenant exports scan all users, and tenant deletion must be auditable. Redesign routing and invariants without claiming unavailable global guarantees.

## Answers to the Exercises

### Answer 1

A **document** is a keyed, finite typed aggregate with engine-defined path and value semantics. **Missing** is absence of a path; **null** is an explicit value. An **aggregate** is state deliberately owned and changed under one consistency boundary. **Embedding** stores related state inside that aggregate; a **reference** stores another identity and needs explicit integrity/lifecycle behavior. A **materialized aggregate** duplicates derived state for a read shape and needs freshness/reconciliation. A **multikey index** may create multiple entries per document from repeated/array values. “JSON row” omits identity, database-specific types, duplicate-key handling, missing/null, paths, arrays, validation, update algebra, atomicity, indexes, placement, and recovery.

### Answer 2

The simplified result is $6{,}144+500\times2{,}000\times90=90{,}006{,}144$ bytes, about 90.0 MB decimal. Omitted costs include field/key and array encoding, allocation slack, compression, WAL, replication, secondary-index entries, cache and network transfer, whole-document rewrites, backups, variance, and temporary migration space. A bounded model stores a fixed recent window or summary in the document and places events under independent stable IDs in time/identity partitions with retention. The document stores a cursor/count and perhaps bounded latest items. Cross-boundary reads and updates then need explicit snapshot/freshness semantics.

### Answer 3

Both workers can call the external provider before either conditional database write; one database update conflicts, but both payments may already exist. Assign a durable payout operation/idempotency key under a uniqueness constraint before calling the provider. Transition `pending` to `dispatching` with version 21 and owner/lease or outbox record atomically. The dispatcher calls the provider with the same idempotency key, records the exact response, and retries safely after uncertainty. Reconciliation queries provider status by that identity. A final conditional transition records paid/failed state. Leases are fenced so stale workers cannot publish authority. Database optimistic concurrency protects state transitions; provider idempotency and reconciliation protect the external effect.

### Answer 4

Reference the independently owned seller identity; materialize only display fields with source version if product reads require them. Embed bounded variants when they share product lifecycle, but keep inventory in a transactionally updated per-variant ownership record if contention or independent reservation demands it. Store unbounded reviews separately by product/user/time with moderation and pagination; materialize count/rating summaries with replay and reconciliation. Embed historical product description, price, and seller display snapshot in each order line so history does not change with catalog edits. Keep authoritative product text in the product aggregate and project it into a search index through a gap-aware, idempotent change stream with freshness and rebuild procedures. Exact indexes cover product identity, seller/product listing, variant lookup, and review pagination. Transactions enforce inventory reservations and order publication at their actual placement scope; denormalized/search state is repaired from authority.

### Answer 5

Tenant-only routing is unsplittable and cannot absorb the hot tenant. Use `(tenant_id, bucket(user_id))` for user documents, with a directory/configuration version defining bucket count and movement. Profile reads compute the bucket locally; tenant export fans out across a fixed bucket set under a snapshot or explicit per-bucket consistency boundary. Enforce username uniqueness through deterministic username-hash ownership records keyed by `(tenant_id, bucket(username), normalized_username)` and a transaction only if the database can atomically include the profile owner; otherwise use a reservation workflow with explicit pending/conflict states and reconciliation. Record stable user IDs so username changes do not move identity. Tenant deletion creates an auditable fenced deletion epoch, blocks new writes, scans every declared bucket, writes tombstones/deletion evidence, reconciles indexes/materializations/backups under retention policy, and proves completion per bucket. The answer does not promise one global atomic delete unless the deployed transaction system supplies it.
