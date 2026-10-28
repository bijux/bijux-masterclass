---
module_id: DE-069
program: Data Engineering
level: 2
module_number: 69
title: Catalog Integration
status: complete
last_verified: 2026-09-03
---

# Catalog Integration

## One-Page Review

### Governing question

How can many engines discover, authorize, read, and atomically update the same analytical tables through a catalog while names, namespaces, metadata pointers, credentials, schemas, locations, caches, branches, and ownership evolve—without split-brain commits, stale reads, name-reuse confusion, orphaned data, leaked credentials, or treating a search index or metastore projection as the table itself?

### Essential definitions

- A **catalog** resolves a logical identifier such as `prod.sales.orders` to authoritative table identity, location, metadata, and supported operations.
- A **namespace** groups identifiers and may supply ownership, location, policy, or default properties; it is not necessarily a storage directory.
- A **stable table identity** is an immutable UUID or equivalent that distinguishes a table across rename and detects drop/recreation behind the same name.
- A **metadata pointer** identifies the current table metadata/log state used to construct snapshots.
- A **catalog commit** atomically replaces or updates the current pointer after validating requirements against the observed base.
- A **compare-and-swap (CAS)** commit succeeds only when the current generation/pointer still equals the writer's expected base.
- A **requirement** is a precondition such as table-not-exists, UUID-match, reference-head-match, or current-metadata-match checked before updates commit.
- A **catalog adapter/plugin** translates an engine's catalog API into a catalog protocol or implementation.
- A **metastore projection/sync** copies table schema, partitions, properties, or location into another catalog for compatible discovery; it may lag the source table.
- A **REST catalog protocol** provides an engine/language-neutral API for namespace, table, view, commit, configuration, and security interactions.
- **Credential vending** issues scoped, short-lived storage credentials for an authorized table request; **remote signing** authorizes storage requests without distributing long-lived secrets.
- A **catalog cache** stores resolved entries or metadata locally; freshness and invalidation determine when clients observe commits, renames, drops, and policy changes.
- A **purge/drop** can remove catalog identity and, depending on the explicit operation, schedule/delete table contents; dropping a name is not automatically safe physical deletion.
- A **versioned catalog** records changes to multiple content keys under commits/branches/tags, distinct from per-table snapshots.
- A **data discovery catalog** indexes descriptions, owners, lineage, classifications, and usage; it is not automatically the transactional catalog.

### Central model, mechanism, or theorem

Represent a catalog entry as

$$
C[n]=(table\_id,metadata\_location,generation,properties).
$$

A writer reads generation $g$, constructs immutable metadata $m'$, then requests

$$
CAS(n,expected=(id,m,g),new=(id,m',g+1)).
$$

Exactly one contender can replace the observed state when CAS is linearizable. A loser refreshes, validates semantic conflicts, and retries only when safe. Readers load one committed pointer and pin the table snapshot. Rename changes the name-to-entry mapping without changing table identity. Drop and recreation allocate a new identity, so stale clients must reject an unexpected UUID even if name and location appear familiar.

### Critical invariants

- Every resolved table has a stable identity; rename preserves it and recreation never reuses it.
- The transactional catalog points to authoritative table metadata/log state; directory listing, search indexes, and synchronized schemas do not define membership.
- A commit validates expected identity/base/reference plus operation-specific requirements and advances atomically.
- Failed/stale writers cannot overwrite a newer pointer; retries refresh and revalidate semantic scope.
- Metadata files and data/delete files are durable before publication and remain immutable afterward.
- Reader operations pin the loaded metadata/snapshot; cache refresh changes only later operations.
- Catalog cache bounds, explicit refresh, and event invalidation are documented and safe for reads, writes, rename, drop, and policy revocation.
- Namespace and table location policies create unique, collision-resistant storage paths and never infer ownership solely from prefixes.
- Rename, register, relocate, drop, purge, restore, and namespace deletion have explicit, independently authorized semantics.
- All engines use one write authority or compatible atomic commit protocol; dual catalogs do not concurrently own the same table pointer.
- Synced schema/partition metadata is identified as a projection with source version and lag; consumers can detect staleness.
- Authentication, authorization, credential vending/signing, storage IAM, KMS, and row/column policy are coherent and least-privileged.
- Catalog state, table metadata, storage, keys, policies, and audit logs are backed up and restored as a tested consistency set.
- Protocol/table features are gated across every reader, writer, maintenance, catalog, sync, and recovery tool.
- Metrics expose resolution, cache, commit, conflict, sync, authorization, credential, and recovery health.

### Common failures

Common failures include using a table name as permanent identity; registering two names as independent writable authorities over one location; allowing Hive, REST, and path writers to commit through incompatible locks; treating metastore schema as current table metadata; setting an infinite cache TTL for writers; retrying a CAS failure without semantic validation; creating new metadata before durable data exists; reusing a dropped location; implementing rename as copy; letting namespace deletion purge unknown tables; embedding long-lived storage keys in engine configs; granting catalog access but not storage/KMS access; granting storage access that bypasses table policies; losing the catalog database in backup; restoring pointers without referenced files or keys; and declaring multi-engine compatibility after testing only reads.

### Compact example

Two writers load `sales.orders` at UUID `T1`, pointer `m1`, generation 1. Writer A commits `m2` with expected generation 1 and wins, producing generation 2. Writer B's attempt to commit `m3` from generation 1 fails. B refreshes `m2`, checks whether its append is still compatible, builds new metadata, and can attempt generation 2. Later the catalog renames the entry to `commerce.orders`; UUID `T1` persists. If that table is dropped and the old name is reused, the new table receives `T2`, causing stale UUID `T1` clients to fail safely.

### Connections

[DE-008](008-schemas-nullability-and-type-fidelity.md) establishes schema fidelity, [DE-023](023-file-arrival-and-manifest-processing.md) separates manifests from discovery, [DE-049](049-run-metadata-and-operational-state.md) records operational identities, [DE-061](061-object-storage-as-a-data-substrate.md) defines storage semantics, [DE-063](063-table-metadata-and-snapshots.md) defines atomic table state, and [DE-064](064-schema-evolution.md) through [DE-068](068-clustering-and-data-skipping.md) define metadata a catalog must preserve. DE-070 integrates these pieces into complete table-format operations.

## Governing Question

An analytical table needs a rendezvous point. A query engine has a human-readable name, not the location of the newest metadata file. A writer needs to publish a new state without racing another writer. A governance system needs ownership and policy. A maintenance job needs the same identity and commit semantics as ingestion.

The catalog supplies that control plane. At minimum it maps names to table identity and current metadata state and implements create, load, commit, rename, and drop. Rich catalogs add namespaces, views, functions, branches, multi-table commits, credential vending, policy, events, metrics, and discovery integration.

The table format and catalog divide authority. In snapshot formats, table metadata describes schemas, partition specs, snapshots, manifests, and files. The catalog atomically chooses the current metadata location. In log formats, the table log may reside at a location while a metastore primarily enables name resolution and schema/partition discovery. Retrieve the exact architecture.

Catalog integration fails when two systems believe they own the pointer. A path-based writer, Hive-metastore writer, and REST-catalog writer can each appear correct alone while racing through different locking primitives. The table then has divergent histories or lost commits.

The governing requirement is one coherent identity and commit authority per writable table, with explicit projections to other catalogs, end-to-end security, bounded caching, and tested recovery.

## Why This Matters

Catalog errors are control-plane errors with data-plane consequences. A lost pointer can make all data seem absent. A stale pointer can hide committed rows. A last-writer-wins update can discard another writer's snapshot. A recreated name can send an old job into a different table.

Multi-engine lakehouses amplify risk. Spark, Flink, Trino, Hive, maintenance services, and custom clients may ship different catalog adapters, table-format libraries, cloud SDKs, and cache rules. Read interoperability does not prove commit interoperability. Every writer must participate in the same conflict protocol.

Metadata synchronization is often eventually consistent. A Hudi table may be authoritative at its timeline while a Hive metastore receives the latest schema and partitions after a write. A lagging sync affects discovery or query planning in engines that depend on it; it should not be mistaken for an independent writable table history.

Security spans services. The catalog authenticates callers and authorizes logical operations; storage validates object operations; KMS releases keys; policy engines filter rows or columns. If users can bypass the catalog with broad storage credentials, catalog authorization is not a complete boundary.

Recovery depends on catalogs. Object backups without namespace/table entries, metadata pointers, stable IDs, credential policies, and keys may be unusable. Catalog backup without immutable metadata/data objects is equally incomplete. Drills must restore the consistency relationship.

## Prerequisites and Retrieval

Retrieve catalog topology: implementation/protocol/version, endpoints, regions, replicas, databases, namespaces, warehouses, backing stores, load balancers, TLS, identity provider, policy engine, credential service, KMS, event bus, caches, and disaster-recovery targets.

Retrieve table mapping: fully qualified name, stable UUID, table type/format/version, current metadata pointer or base location, warehouse/location policy, namespace properties, owner, creation identity, current generation/version, and aliases.

Retrieve commit semantics: CAS/check-and-put/lock/transaction primitive, linearizability/isolation, expected requirements, timeout, retry/backoff, lock lease/heartbeat, staged create, data/metadata durability ordering, conflict classification, idempotency, and orphan handling.

Retrieve client fleet: engines/connectors/libraries and exact versions; configured catalog name/type/URI/warehouse/FileIO; session/default namespaces; cache TTL/invalidation; supported table features; read/write/maintenance role; and direct-path capabilities.

Retrieve catalog operations: namespace create/drop/properties; table create/register/load/exists/list/rename/drop/purge/replace/relocate; views/functions; branches/tags; multi-table transactions; transaction staging; and operation-specific authorization.

Retrieve synchronized projections: target metastore/discovery systems, schema/type/partition/property mapping, source version marker, trigger, retry, ordering, lag, reconciliation, deletion/rename behavior, writer ownership, and consumer dependency.

Retrieve security: caller identity, tokens/scopes, service accounts, table/namespace policies, storage credential vending/remote signing, credential TTL, storage prefix/actions, KMS key policy, network boundary, row/column filters, masks, audit events, and break-glass access.

Retrieve failure/recovery behavior: catalog database backup and point-in-time recovery, replication lag/failover, metadata/data replication, key availability, DNS/endpoint failover, RPO/RTO, split-brain prevention, restored table UUID validation, and reconciliation tools.

Retrieve observability: request/operation latency and error codes, loads, cache hits/staleness, commits/conflicts/retries, locks, metadata sizes, sync lag/failures, authorization denials, token/credential issuance, unknown UUID/pointer changes, and referenced-file health.

Distinguish name from UUID; namespace from directory; catalog pointer from table snapshot; transactional catalog from discovery catalog; authoritative metadata from synchronized projection; load cache from pinned read; retryable transport failure from commit outcome unknown; drop from purge; rename from copy; table location from storage authorization; and single-table snapshots from versioned multi-table catalog commits.

Create an integration contract:

| Concern | Required decision and evidence |
|---|---|
| Identity | Catalog/namespace/name, stable table UUID, metadata pointer, location and generation |
| Authority | One write catalog/protocol, table metadata authority, permitted projections/direct reads |
| Commit | Preconditions, CAS/lock/transaction, durability order, conflicts, retry/idempotency |
| Operations | Create/register/rename/drop/purge/relocate/branch behavior and permissions |
| Fleet | Every reader/writer/tool version, feature matrix, cache/refresh and failure fixtures |
| Sync | Source/target, version marker, type mapping, lag SLO, reconciliation and ownership |
| Security | Authentication, authorization, storage/KMS credential scope, policy and audit |
| Recovery | Catalog+metadata+data+key consistency, backup, failover, restore and UUID checks |
| Operations | SLOs, quotas, metrics, alerts, capacity, runbooks and accountable owners |

Write a falsifiable claim: “Catalog `prod` maps `sales.orders` to immutable UUID T1 and metadata M918; all eight writers commit only through REST protocol P7 with UUID/current-pointer requirements and server-side conflict handling; 14 readers refresh within 30 seconds while each query pins a loaded snapshot; short-lived credentials allow only T1's resolved prefixes and KMS key; Hive/discovery projections publish source pointer and remain below two-minute lag; rename preserves T1, drop never purges without separate approval, name reuse allocates a new UUID/location; regional restore reconstructs catalog, metadata, objects, keys, and policy within RTO/RPO and passes quarterly drills.”

## Learning Objectives

After completing this module, you should be able to:

1. separate transactional catalogs, table metadata, storage, metastores, and discovery systems;
2. model names, stable table identities, metadata pointers, locations, and generations;
3. explain CAS/check-and-put commits, requirements, conflicts, safe retries, and outcome uncertainty;
4. evaluate filesystem, Hive/metastore, JDBC, REST, cloud, and versioned catalog architectures;
5. design cache, refresh, rename, drop, purge, registration, and location semantics safely;
6. govern authoritative-to-projection schema/partition synchronization and lag;
7. integrate authentication, authorization, credential vending/signing, storage IAM, and KMS;
8. qualify every reader, writer, maintenance, sync, and recovery client for protocol features;
9. back up, fail over, restore, and reconcile catalog/table state as a consistency set; and
10. operate catalog integrations with SLOs, quotas, metrics, alerts, runbooks, and audits.

## Core Exposition

### Separate the control plane from table state

The transactional catalog resolves a name to a table object. For metadata-pointer formats, it returns the current metadata location plus table/configuration information. The referenced table metadata then defines snapshots, schemas, partition/sort specs, manifests, and data/delete membership.

A catalog listing is not a data-file listing. A warehouse directory is not the namespace. A discovery search result is not an authoritative pointer. These layers can be cached or stale without changing committed table truth, but clients depending on them need explicit consistency expectations.

Stable table identity closes an important hole. If `sales.orders` is dropped and recreated, the name can be identical while history and ownership differ. Readers and writers that loaded UUID T1 must reject T2 rather than silently continuing.

Record catalog identity, endpoint, namespace, table UUID, metadata pointer, snapshot/version, and client version in run lineage. “Read orders” is not reproducible evidence.

### Make commit atomic and conditional

A typical writer reads pointer $m$, writes data/delete files, builds new immutable metadata $m'$, then asks the catalog to swap $m\rightarrow m'$ if $m$ is still current and requirements hold. The new files must be durable before the pointer makes them visible.

Two writers can create candidates concurrently. One wins the atomic swap. The loser receives conflict, refreshes, and determines whether its operation can be replayed. Append may be compatible with a disjoint append; overwrite/update/delete needs predicate/file/sequence conflict validation.

The catalog's storage primitive matters. A relational/JDBC backing store needs atomic transactions and suitable isolation. A metastore may use locks or conditional update. Object-store/path schemes need a valid mutual-exclusion/CAS mechanism; rename assumptions unsafe on the storage cannot be wished into correctness.

A timeout after request transmission creates unknown outcome. Before retrying, the client checks idempotency/transaction identity or reloads state to determine whether the commit succeeded. Blind retry can duplicate effects or leak candidates.

### Use requirements as executable preconditions

Requirements prevent updates from applying to an unexpected base. Useful examples include table must not exist for create, UUID must match, current metadata location must match, reference head must match, schema/spec/sort IDs must still be current, or sequence/snapshot conditions must hold.

Server-side validation reduces client races. The request describes requirements and updates; the catalog validates and commits them together. Change-based updates also let servers perform safe deconfliction or retries where the protocol defines it.

Preconditions are not business conflict logic by themselves. A writer must choose requirements appropriate to append, overwrite, schema change, rewrite, or branch update. Weak requirements lose updates; unnecessarily broad requirements create avoidable conflicts.

Log rejected requirement, observed/current identity, operation, retry choice, and final outcome without leaking secrets.

### Compare catalog architectures

Filesystem/Hadoop catalogs derive names from warehouse paths and use storage operations for table tracking. They are simple and portable but depend heavily on filesystem semantics and make rename/location governance difficult on object stores.

Hive/metastore catalogs store table records and metadata pointers in a shared service. They integrate broad SQL ecosystems but inherit metastore locks, availability, namespace conventions, type mappings, and version compatibility.

JDBC catalogs use relational transactions. They can offer strong atomicity when the database supports it, but connection pools, schema migration, credentials, isolation, failover, and database capacity become table-control-plane concerns.

REST catalogs expose a common language/engine-neutral protocol. The server can centralize commit validation, configuration, credential vending/signing, policy, and new features while clients share one interface. Network/API versioning, availability, auth, quotas, and server correctness become critical.

Cloud-managed catalogs integrate provider identity and governance, but account/region, SDK version, conditional-update support, quotas, and proprietary behaviors must be explicit. Versioned catalogs add branches/tags and multi-table commit contexts; they do not eliminate per-table file/snapshot semantics.

### Configure names and locations durably

Use fully qualified catalog, namespace, and table identifiers in production jobs. Session defaults are convenient interactively but can send the same SQL to different environments. Record current catalog/namespace at run start.

Namespace properties can supply warehouse roots, owners, defaults, or policies. Treat defaults as creation-time behavior unless documented otherwise; changing a default need not rewrite existing tables.

Allocate unique table locations, ideally including durable identity/randomness, so drop/recreate cannot collide with retained files. Never use name reuse plus the same prefix while old snapshots, streams, backups, or cleanup may exist.

The table's base location and metadata locations may have absolute or relative semantics by format version. Relocation requires a supported protocol and verification; editing pointers/paths by hand can strand references.

Registering an existing table attaches a catalog name to existing authoritative metadata. Validate format, UUID, ownership, location, history, keys, and absence of another write authority. Registration is not conversion or copying.

### Define rename, drop, purge, and namespace deletion

Rename should atomically move the name mapping while retaining table UUID and metadata pointer. Old clients using the former name may fail or follow aliases according to policy; clients holding a loaded table can continue under pinned semantics.

Drop removes catalog reachability. Purge additionally authorizes data/metadata deletion under format and retention rules. Keep them separate, require stronger permission/confirmation for purge, and record impact on snapshots, streams, backups, shares, and legal holds.

After drop without purge, files may be registered/recovered if policy permits, but recovery is not guaranteed without recorded identity and metadata closure. After purge, physical deletion can be irreversible.

Namespace deletion should fail when governed objects remain unless a separately authorized recursive process inventories exact targets. Prefix-based deletion is unsafe when locations are shared or external.

Tombstone names/UUIDs/locations through the rollback and cleanup horizon. A recreated table receives a new UUID and unique location.

### Bound caches and refresh explicitly

Catalog caches lower load and latency. They also delay observation of commits, schema changes, rename/drop, credential changes, and policy revocation. Cache table handles, metadata, credentials, and negative lookups separately because safe lifetimes differ.

A query should pin one loaded snapshot. Refresh between queries is normal; refresh during a query must not fracture its state. Writers refresh before commit and rely on conditional validation even if their cache is stale.

Use finite TTLs, explicit refresh APIs, event-driven invalidation where trustworthy, and generation/ETag validation. Negative caching must not hide a newly created table too long. Policy and credential revocation may require shorter TTL or push invalidation than metadata freshness.

Measure actual staleness. A configured 30-second TTL plus layered engine/proxy caches can produce longer lag.

### Govern metastore and discovery synchronization

Some table formats are authoritative in table metadata/timeline while external metastores need latest schema, location, or partition registrations. Sync is a derived projection. It should identify source table UUID and metadata/timeline version, sync run, timestamp, mapping version, and status.

Type systems differ. Complex types, nullability, logical annotations, partition transforms, field IDs, and names can lose information in a metastore round-trip. Document lossy mappings and prevent the projection from becoming a writer of authoritative schema.

Sync after the table commit; do not block table truth on an unrelated discovery index unless the product explicitly makes publication atomic across both. If sync fails, table commit remains known and lag alert/retry/reconciliation repairs the projection.

Handle rename/drop deliberately. Creating the new name before removing the old can expose aliases; removing first can cause a discovery gap. Preserve UUID/version markers so consumers detect which is authoritative.

Periodically reconcile source and projection: names, location, UUID, schema digest, partitions, properties, source version, and extra/missing entries. Do not infer equality from successful last run alone.

### Integrate security end to end

Authenticate engine/service identity using short-lived tokens or workload identity. Authorize namespace/table operations: list/load/create/commit/rename/drop/purge/branch/view. Avoid making `list` permission an accidental prerequisite for a permitted exact table load unless policy intends it.

Catalog authorization does not automatically enforce storage. Credential vending can issue scoped, short-lived credentials for resolved metadata/data prefixes and allowed operations. Remote signing can keep storage credentials server-side. Validate TTL, refresh, revocation, delegation, audit, and confused-deputy controls.

Storage access must not let users bypass row/column policy or tamper with metadata. Separate trusted writer/maintenance roles from read roles. KMS policy must align with table identity and historical access.

Never place long-lived passwords or cloud keys in shared Spark configuration, logs, catalog properties checked into source, or error messages. Secret references and workload identity are preferable.

For encrypted tables, the catalog may participate in trusted metadata/key management and must protect integrity as required by the format. Back up key identity and policy, not plaintext secrets.

### Qualify multi-engine compatibility

Build a matrix of catalog adapter, engine, table-format library, FileIO/cloud SDK, protocol/table format, and operation. Test reads and writes separately. Include create, append, overwrite, update/delete/merge, schema/partition/sort evolution, compaction, time travel, branches/tags, rename, drop, and recovery.

Test concurrency across heterogeneous writers, not just same-library threads. Verify one winner, detectable loser, semantic rebase, no lost data, correct cleanup, and unknown-outcome recovery.

Feature defaults/overrides applied by the catalog can enable formats old clients cannot read. Gate table properties and protocol upgrades against the full fleet. Catalog-config negotiation is evidence, not a substitute for actual conformance fixtures.

Direct path reads may work for diagnosis but can bypass catalog identity, credentials, branches, policy, current pointer, or relative-location resolution. State whether they are supported and never allow path writes to compete with catalog writes.

### Design availability and recovery

Catalog availability is on the read/write critical path unless clients can safely use cached pinned metadata. Define separate load and commit SLOs. During outage, reads of already loaded immutable snapshots may continue; new loads, refreshes, credentials, or commits may fail.

Failover must preserve one write leader or linearizable conditional store. DNS-switching to a lagging writable replica risks split brain. Prefer fail closed for commits when current pointer is uncertain.

Back up catalog records, namespaces, UUIDs, metadata pointers, generations, properties, views, references, policies, audit/configuration, and backing-store schema. Coordinate with table metadata/data/delete objects, KMS, credential systems, and artifact versions.

Restore into isolation, validate UUID/pointer and every referenced artifact/key, then reconcile with storage. Do not select “highest-looking metadata filename” as current. Only catalog/log history establishes the committed pointer.

Drill loss of catalog database, region, identity provider, KMS, event bus, and sync target. Record RPO/RTO and writes accepted near failure.

### Observe and operate the control plane

Measure load/list/create/commit/rename/drop latency and error rate by catalog/engine/operation; active tables/namespaces; metadata payload; cache hit/miss/staleness; request/connection/lock saturation; commit success/conflict/retry/unknown outcome; and orphan candidates.

Measure sync lag by source version/time, failures, retries, mapping errors, extra/missing objects, and consumer impact. Measure authorization denials, unusual list/purge actions, token failures, credential issuance/TTL/refresh, signing errors, and KMS denials.

Alert on UUID mismatch, pointer regression, conflicting authorities, high CAS failure beyond workload baseline, expired locks, unknown commit outcome, cache staleness SLO, sync divergence, unauthorized purge, location collision, missing referenced metadata, replica lag near RPO, or failed restore drill.

Runbooks name the table/catalog owner, platform operator, security responder, and data product approver. They specify read-only degradation, writer fencing, cache flush, conflict triage, sync replay, pointer recovery, credential outage, rollback, and evidence preservation.

## Definitions and Notation

Let catalog state $C$ map fully qualified name $n$ to entry $e=(u,m,g,l,p)$: table UUID $u$, metadata pointer $m$, generation $g$, location $l$, properties $p$.

A conditional transition is

$$
commit_C(n,e_{expected},e_{new})=
\begin{cases}
success,& C[n]=e_{expected}\land Requirements(C),\\
conflict,& otherwise.
\end{cases}
$$

On success, $C'[n]=e_{new}$ and all other mappings are unchanged except explicit atomic multi-object operations.

Rename from $n_1$ to $n_2$ preserves identity:

$$
C'[n_2]=C[n_1],\quad n_1\notin dom(C'),\quad UUID(C'[n_2])=UUID(C[n_1]).
$$

For authoritative state $a(t)$ and projection $q(t)$, sync lag can be measured by time $L_t=t_{projected}-t_{source}$ or version distance $L_v=version(a)-version(q)$ where ordering is defined.

Availability of a table read requires $CatalogResolve\land MetadataRead\land DataRead\land KeyAccess\land PolicyAllow$. Commit additionally requires conditional atomicity and write credentials.

## Mechanisms, Invariants, or Proof Structure

Proof sketch for lost-update prevention:

1. Writers A and B both load entry $e_1=(T1,m1,1)$.
2. Each constructs immutable candidate metadata from $m1$.
3. The catalog serializes/linearizes conditional swaps on the entry.
4. A's swap from expected $e_1$ to $e_2$ succeeds first.
5. Catalog state no longer equals $e_1$, so B's conditional swap cannot succeed.
6. B observes a conflict rather than overwriting $e_2$.
7. B may refresh, test its operation-specific compatibility with $e_2$, and build a new candidate; it cannot publish the stale candidate as though A never committed.
8. Therefore the pointer has no silent lost update, assuming linearizable CAS and all writers use this authority.

The proof does not prevent semantic conflicts under weak requirements, split brain between different catalogs, or incorrect retry logic. Those premises require fleet and operation-level validation.

The executable models CAS, refresh, rename preserving UUID, and drop/recreate allocating a new UUID. It is a teaching abstraction, not an implementation of Iceberg REST/Hive/JDBC/Glue/Nessie, Delta, Hudi, storage, locks, authentication, or networking.

<!-- bijux-verify: {"id":"catalog-conditional-commit","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"initial=('T1', 'm1', 1)\nwriter_a_commit=True\nafter_a=('T1', 'm2', 2)\nwriter_b_stale_commit=False\nwriter_b_retry=True\nafter_b=('T1', 'm3', 3)\nrenamed_name=commerce.orders\nrenamed_identity=T1\nold_name_present=False\nrecreated_identity=T2\nstale_identity_rejected=True\n","stderr":""}} -->
```python
catalog = {"sales.orders": ("T1", "m1", 1)}


def commit(name, expected, new_metadata):
    current = catalog.get(name)
    if current != expected:
        return False
    table_id, _, generation = current
    catalog[name] = (table_id, new_metadata, generation + 1)
    return True


base_a = catalog["sales.orders"]
base_b = catalog["sales.orders"]
print(f"initial={base_a}")
print(f"writer_a_commit={commit('sales.orders', base_a, 'm2')}")
print(f"after_a={catalog['sales.orders']}")
print(f"writer_b_stale_commit={commit('sales.orders', base_b, 'm3-stale')}")
base_b = catalog["sales.orders"]
print(f"writer_b_retry={commit('sales.orders', base_b, 'm3')}")
print(f"after_b={catalog['sales.orders']}")

catalog["commerce.orders"] = catalog["sales.orders"]
catalog = {name: entry for name, entry in catalog.items() if name != "sales.orders"}
print("renamed_name=commerce.orders")
print(f"renamed_identity={catalog['commerce.orders'][0]}")
print(f"old_name_present={'sales.orders' in catalog}")

stale_identity = "T1"
catalog = {name: entry for name, entry in catalog.items() if name != "commerce.orders"}
catalog["commerce.orders"] = ("T2", "n1", 1)
print(f"recreated_identity={catalog['commerce.orders'][0]}")
print(f"stale_identity_rejected={catalog['commerce.orders'][0] != stale_identity}")
```

## Alternatives and Trade-Offs

**Filesystem versus service catalog.** Filesystem catalogs reduce services and can suit strongly consistent rename-capable stores. Service catalogs centralize atomicity, policy, and discovery but add availability, scaling, auth, and recovery dependencies.

**Hive/metastore versus REST.** Metastores have broad ecosystem support and mature SQL namespaces. REST offers language-neutral evolution, server-side commits, configuration, and credentials; client/server compatibility and network operations must be governed.

**JDBC versus managed catalog.** JDBC uses familiar transactions and portable databases but exposes database operations/capacity/security. Managed catalogs reduce operations and integrate cloud identity at provider/version/region coupling cost.

**Catalog cache versus freshness.** Caching lowers latency/load and enables pinned-read continuity. Short TTL/invalidation is needed for fast commit, rename, drop, and policy visibility.

**One authoritative catalog versus dual registration.** One authority prevents split-brain writes. Read-only projections improve interoperability but add sync lag and type-mapping ambiguity.

**Credential vending versus broad engine roles.** Vending/signing narrows privilege and centralizes policy at latency/availability complexity. Broad roles are simple but magnify bypass and blast radius.

**Drop versus purge.** Drop is recoverable while metadata/objects remain but leaves storage/cost. Purge reclaims data and may satisfy erasure but requires stronger reachability, hold, and authorization evidence.

**Name reuse versus tombstoning.** Quick reuse is convenient but confuses stale jobs and cleanup. Tombstoning plus unique UUID/location makes lifecycle safer.

**Synchronous versus asynchronous projection sync.** Synchronous publication can provide one visibility gate but couples table writes to metastore outages. Async sync preserves table availability but needs versioned lag and reconciliation.

**Single-table versus versioned multi-table catalog commit.** Single-table protocols are simpler and scalable. Multi-table commits support consistent release branches but add conflict, retention, merge, and governance complexity.

**Client-side versus server-side conflict retry.** Client retry exposes control and operation semantics. Server-side change-based deconfliction reduces round trips but must preserve transparent requirements and audit evidence.

## Failure Modes and Misconceptions

1. **“The table name is its identity.”** Drop/recreate can reuse a name; verify UUID.
2. **“The warehouse path is the namespace.”** Logical grouping and physical placement are separate policies.
3. **“Catalog schema is the table.”** Authoritative table metadata/timeline may contain richer/current semantics.
4. **“Listing storage reconstructs current state.”** It includes orphans/history and lacks transactional membership.
5. **“Any metastore can safely commit.”** Atomic conditional semantics and compatible locks are required.
6. **“Two catalogs improve availability.”** Concurrent write authorities create split brain.
7. **“Read compatibility proves write compatibility.”** Commit, conflict, delete, evolution, and maintenance paths differ.
8. **“Last-writer-wins is acceptable.”** It silently loses table state.
9. **“CAS failure just retries the same pointer.”** Refresh and semantic revalidation are required.
10. **“Timeout means failure.”** The commit may have succeeded; resolve unknown outcome.
11. **“Metadata can be published before data.”** Readers can observe missing/incomplete files.
12. **“Infinite cache is fastest.”** Writers and policy/schema/drop visibility become stale indefinitely.
13. **“Refresh during query improves freshness.”** It can fracture snapshot consistency.
14. **“Rename copies the table.”** Correct rename preserves identity and pointer mapping.
15. **“Drop deletes files.”** Only explicit purge/cleanup under policy authorizes physical deletion.
16. **“A dropped location is free.”** History, streams, backups, or cleanup may still refer to it.
17. **“Register converts data.”** It attaches a name to compatible existing metadata.
18. **“Sync success proves equality forever.”** Projection can lag or mappings can be lossy.
19. **“Projection may update authoritative schema.”** That creates two schema authorities.
20. **“Catalog authorization protects objects.”** Broad direct storage access can bypass it.
21. **“Long-lived keys are simpler.”** They leak, outlive sessions, and enlarge compromise scope.
22. **“Failover to any replica is safe.”** A lagging writable replica can regress pointers/split brain.
23. **“Object backup is enough.”** Catalog identity/pointers, keys, policy, and software are required.
24. **“Newest filename is current.”** Only committed catalog/log state identifies the pointer.
25. **“Discovery catalog owns commits.”** Search/lineage indexes are usually derived control metadata.
26. **“One green client qualifies the fleet.”** Every reader, writer, maintenance, sync, and recovery path must pass.

## Worked Examples

### Example 1

Spark and Flink append through one REST catalog. Both submit current-pointer and UUID requirements. A simultaneous append produces one winner; the loser refreshes and safely rebases its append. No path writer is permitted.

### Example 2

A Hive metastore sync lags an authoritative Hudi timeline by three commits. The entry records source instant and writer version. Trino consumers alert on the lag rather than assuming absent new columns mean the table did not evolve.

### Example 3

`sales.orders` is renamed to `commerce.orders`. The catalog atomically moves the mapping and retains UUID T1/location. A compatibility alias is read-only and expires after consumers migrate; it cannot become a second writer authority.

### Example 4

A table is dropped without purge, then its old name is recreated. The new table receives UUID T2 and a unique location. A stale job expecting T1 fails before writing, preventing old candidate files from entering the new history.

### Example 5

A commit request times out after reaching the server. The client reloads UUID/pointer and checks transaction identity. It discovers the commit succeeded and records success; blind retry would have created a duplicate snapshot.

### Example 6

A JDBC catalog runs on a database whose failover briefly weakens transaction assumptions. A concurrency drill detects two successful stale swaps. Writes are fenced until the database configuration provides required atomic isolation; apparent endpoint availability is not enough.

### Example 7

A REST catalog vends a 15-minute credential limited to the table's resolved metadata/data prefixes and read actions. KMS access is scoped separately. The query renews safely; logs contain credential ID/expiry, never token material.

### Example 8

A schema with stable field IDs and a complex logical type syncs to a name-based metastore representation. The projection stores source schema ID/digest and documents loss. Writers cannot infer authoritative field identity from the projection.

### Example 9

Regional recovery restores catalog records but one metadata object and a KMS key are missing. UUID checks pass but closure validation fails, so the catalog remains isolated/read-only. Recovery does not publish a pointer to unreadable state.

### Example 10

A discovery index shows owner, lineage, quality, and popularity for a table. It links stable catalog/UUID/version evidence and reports freshness. Search outage does not alter table commits; transactional catalog outage does not authorize search data as a replacement pointer.

## Cross-Program Connections

- **Database Systems:** catalogs, namespaces, transactions, compare-and-swap, locks, serializability, DDL, MVCC, and recovery underpin the control plane.
- **Distributed Systems:** linearizability, consensus, leases, retries, idempotency, split brain, replication lag, consistent cuts, and fencing govern commits/failover.
- **API and Service Engineering:** REST contracts, requirement/update requests, authentication, pagination, error taxonomy, versioning, quotas, and observability shape catalog protocols.
- **Platform Engineering:** self-service namespaces, golden clients, policy, credential brokering, multi-tenancy, SLOs, capacity, and runbooks turn catalogs into shared products.
- **Security Engineering:** workload identity, least privilege, token exchange, remote signing, KMS, confused deputy, audit, and tamper resistance span catalog and storage.
- **Cloud Engineering:** object semantics, managed metastores, account/region identity, SDK versions, IAM, endpoints, quotas, and cross-region recovery affect implementations.
- **Software Engineering:** adapters, stable identity, plugin compatibility, conditional APIs, migrations, cache invalidation, dependency pinning, and conformance tests keep fleets coherent.
- **Formal Methods:** state machines, preconditions, atomic transitions, invariants, linearization points, refinement, and counterexamples expose lost-update risks.
- **Reliability Engineering:** availability modes, RPO/RTO, backups, failover, chaos drills, alerting, incident fencing, and outcome reconciliation protect control state.
- **Privacy Engineering:** purpose/consent policies, metadata minimization, erasure, legal holds, access logging, and lifecycle govern catalog exposure and purge.

## References

1. Apache Iceberg. [Table specification](https://iceberg.apache.org/spec/). Accessed 2026-09-03. Primary specification for table UUID, metadata locations, snapshots, immutable files, optimistic commits, metastore check-and-put, retries, and location semantics.
2. Apache Iceberg. [REST catalog specification](https://iceberg.apache.org/rest-catalog-spec/). Accessed 2026-09-03. Primary specification overview for the common API, change-based commits, compatibility, configuration, credential vending/remote signing, caching, and multi-table capabilities.
3. Apache Iceberg. [REST catalog OpenAPI](https://raw.githubusercontent.com/apache/iceberg/main/open-api/rest-catalog-open-api.yaml). Accessed 2026-09-03. Primary machine-readable protocol for configuration, namespaces, tables, views, commit requirements/updates, transactions, OAuth, and errors.
4. Apache Iceberg. [Spark configuration](https://iceberg.apache.org/docs/latest/spark-configuration/). Accessed 2026-09-03. Primary engine documentation for Hive, Hadoop, REST, Glue, JDBC, Nessie/custom catalogs, namespaces, caches, FileIO, defaults, and overrides.
5. Apache Iceberg. [Catalog properties](https://iceberg.apache.org/docs/latest/catalog-properties/). Accessed 2026-09-03. Primary documentation for warehouse, URI, client/cache, unique-location, KMS, REST, locking, and Hive catalog behavior.
6. Apache Iceberg. [JDBC catalog](https://iceberg.apache.org/docs/latest/jdbc/). Accessed 2026-09-03. Primary documentation requiring atomic database transactions and serializable isolation for JDBC catalog commits.
7. Apache Iceberg. [Custom catalog](https://iceberg.apache.org/docs/latest/custom-catalog/). Accessed 2026-09-03. Primary documentation for TableOperations, custom Catalog/FileIO/location providers, create/load/rename/drop, and encryption responsibilities.
8. Apache Iceberg. [Encryption](https://iceberg.apache.org/docs/latest/encryption/). Accessed 2026-09-03. Primary documentation for catalog KMS integration, key identity, trusted metadata integrity, and encrypted table catalog requirements.
9. Apache Iceberg. [AWS integration](https://iceberg.apache.org/docs/latest/aws/). Accessed 2026-09-03. Primary documentation for Glue/DynamoDB/RDS catalogs, account/region, optimistic locking, SDK qualification, warehouses, FileIO, and lock management.
10. Apache Hudi. [Metastore synchronization](https://hudi.apache.org/docs/syncing_metastore/). Accessed 2026-09-03. Primary documentation for synchronizing table schema/partitions into Hive Metastore, sync modes, base paths, mappings, and query-engine integration.
11. Apache Hudi. [SQL DDL and catalog integration](https://hudi.apache.org/docs/sql_ddl/). Accessed 2026-09-03. Primary documentation for catalog configuration, persisted table definitions, Hive Metastore and filesystem modes, and engine integration.
12. Project Nessie. [Apache Iceberg integration](https://projectnessie.org/iceberg/iceberg/). Accessed 2026-09-03. Primary project documentation distinguishing Iceberg table snapshots from Nessie's multi-table versioned commits and branches.
13. Apache Hive. [Metastore administration](https://hive.apache.org/docs/latest/admin/adminmanual-metastore-administration/). Accessed 2026-09-03. Primary documentation for metastore service architecture, remote/embedded modes, backing database, configuration, and operations.

## Exercises

### Exercise 1

Two Spark writers, one Flink writer, and a maintenance job currently use REST, Hive, and direct-path configurations for one Iceberg table. Design a migration to one write authority. Include inventory, fencing, UUID/pointer verification, client rollout, concurrency fixtures, rollback, and removal of alternate write paths.

### Exercise 2

Specify create, staged create, register, rename, drop, purge, and recreate semantics for a governed catalog. Include identities, locations, preconditions, authorization, caches, projections, histories, streams, legal holds, and name/location reuse.

### Exercise 3

Design an authoritative Hudi-to-Hive/discovery synchronization service for schemas, partitions, and properties. Define version markers, type mapping, triggers, ordering, retries, lag SLO, rename/drop, reconciliation, and consumer behavior during lag.

### Exercise 4

Create a security design for a REST catalog serving five engines across tenants with short-lived object access and encrypted tables. Cover authentication, authorization, credential vending/signing, storage prefixes/actions, KMS, policy bypass, caching/revocation, audit, and failure modes.

### Exercise 5

Design a regional catalog disaster-recovery drill. Include backup/replication, write fencing, RPO/RTO, catalog generations, table UUIDs/pointers, metadata/data/delete files, KMS, identity/policy, DNS, unknown commits, validation, and failback.

## Answers to the Exercises

### Answer 1

Inventory every engine/library/catalog endpoint/FileIO/SDK, cached table UUID/pointer, operation, lock, and credential. Declare REST the sole target authority only after confirming it references the exact UUID/current metadata and supports all live features. Fence direct/path and Hive writes through IAM and configuration; pause or drain jobs. Migrate readers first, then canary writers and maintenance, using short cache TTL and explicit refresh. Concurrency fixtures run heterogeneous append, overwrite, delete, schema change, and compaction: exactly one stale-pointer winner occurs, losers refresh and semantically revalidate, no snapshot is lost, and unknown outcomes reconcile. Rollback restores client routing without permitting two authorities. Remove old write credentials/configurations and mark Hive, if retained, as versioned read-only projection with reconciliation.

### Answer 2

Create allocates fresh UUID and unique location under not-exists requirement; staged create remains invisible until one commit. Register validates existing format/UUID/metadata closure, ownership, keys, and absence of another authority without copying. Rename atomically moves mapping and preserves UUID/pointer; invalidate caches and version projections. Drop removes mapping but not bytes; purge is separate stronger authorization after snapshot/stream/backup/hold impact analysis. Recreate allocates a new UUID/location and observes a tombstone horizon, so stale clients reject it. Every operation records actor, requirements, before/after generations, result, and cleanup plan. Namespace recursive deletion fails unless exact inventory and explicit authorization cover every table. Legal holds block purge; cache and sync behavior is defined for each transition.

### Answer 3

Treat the Hudi timeline/table config as authoritative and Hive/discovery as projections. After completed table commits, enqueue idempotent sync keyed by table UUID and source instant. Map schema types/nullability/logical annotations and partition extraction under a versioned mapping; record lossy cases, Hudi writer/mapping version, source instant, digest, run, and timestamp in target properties. Process per table in source order, retry transport failures, supersede obsolete runs safely, and reconcile names/location/schema/partitions/properties plus extra/missing entries. Publish measurable lag and alert before its SLO; consumers either tolerate the documented version, refresh, or fail closed for newly required fields. Rename uses coordinated alias/move policy; drop never causes unreviewed purge. Projection clients remain read-only and cannot feed schema changes back into Hudi.

### Answer 4

Authenticate workload identities with short-lived tokens and tenant/audience binding. Authorize exact namespace/table/list/load/commit/DDL/purge operations; policy maps stable table UUID, not only name. Vend or remotely sign short-lived credentials scoped to resolved metadata/data/delete prefixes and permitted read/write/delete actions; prevent caller-selected prefixes and confused delegation. KMS grants align with table/key/operation and historical policy. Deny broad storage routes that bypass catalog row/column enforcement, separate writer/maintenance/read principals, and protect unencrypted metadata integrity. Cache metadata, policy, and credentials with different TTLs; push revocation where possible and fail safely. Audit identity, UUID, operation, pointer generation, credential ID/scope/expiry, KMS decisions, denials, and purge without logging token material. Test issuer/catalog/storage/KMS outage, expiry during reads, replay, cross-tenant requests, and revoked policy.

### Answer 5

Continuously replicate/backup the catalog backing store and schema plus namespaces, UUIDs, pointers/generations, properties, refs/views, policies, and audit/configuration; coordinate object metadata/data/delete replication, KMS keys/policy, identities, and required clients. During regional loss, fence primary and secondary writers and establish whether any timed-out commit outcome is unknown. Restore secondary into isolation at the declared RPO, validate monotonic generations and each UUID/pointer against immutable metadata, snapshot closure, file existence/checksums, and keys; never infer current from filenames. Restore identity/policy and test authorized/denied reads, time travel, then controlled writes with CAS concurrency. Switch DNS only after one writable leader is proven and record lost/uncertain commits against RPO; measure RTO. Failback repeats reconciliation and fencing in reverse, with no simultaneous writers and full evidence retained.
