---
module_id: DE-063
program: Data Engineering
level: 2
module_number: 63
title: Table Metadata and Snapshots
status: complete
last_verified: 2026-09-03
---

# Table Metadata and Snapshots

## One-Page Review

### Governing question

How does an analytical table turn independently stored data and delete files into one atomic, reproducible snapshot—then preserve correctness through concurrent commits, retries, planning, time travel, maintenance, protocol evolution, and garbage collection without mistaking a directory listing, catalog entry, checkpoint, or timestamp for the table itself?

### Essential definitions

- **Table metadata** is the authoritative, versioned description of table identity, protocol/features, schemas, partition/sort definitions, properties, snapshots or actions, and references needed to construct table state.
- A **snapshot** is one immutable logical table state: the exact active data/delete-file set plus the schema, partition, ordering, and other semantics required to read it.
- A **catalog pointer/commit point** identifies the current metadata version or table-log version and changes atomically under the table format's commit protocol.
- A **manifest** lists data or delete files with partition facts, statistics, sequence/tracking fields, and status; a **manifest list** indexes manifests for a snapshot.
- A **transaction log** records ordered actions such as add file, remove file, metadata change, protocol feature, or application transaction from which a snapshot can be reconstructed.
- A **timeline/instant** records the requested, inflight, or completed state of table actions under a format-specific protocol.
- A **checkpoint** materializes reconciled log state through a committed version to reduce replay cost; it is an optimization governed by the log protocol, not a free-standing alternate truth.
- A **tombstone/remove action** logically removes a file from later snapshots while physical bytes may remain for retention, recovery, or concurrent readers.
- A **delete file/vector** encodes row-level removals that readers merge with data files according to format sequence and applicability rules.
- **Optimistic concurrency** lets writers create candidate files/metadata without holding a table-wide lock, then detects conflicts at commit and retries or rejects safely.
- **Snapshot isolation** gives a reader one pinned table state despite later commits; exact write isolation and conflict rules are format/operation specific.
- A **branch/tag/reference** is a named pointer to a snapshot with format-specific mutability and retention behavior.
- **Snapshot expiration/vacuum/cleaning** removes historical metadata reachability and later deletes files no retained snapshot or protected operation needs.
- An **orphan file** is an artifact not reachable from any protected table state or active operation; absence from the current snapshot alone does not make a file orphaned.
- **Protocol compatibility** is the set of reader/writer features and versions an engine must support to interpret and mutate the table safely.

### Central model, mechanism, or theorem

Let snapshot $s$ contain active data files $A_s$, active delete artifacts $D_s$, schema $\sigma_s$, partition specification $\pi_s$, sort/order definition $\omega_s$, properties $p_s$, and parent/reference metadata:

$$
S_s=(A_s,D_s,\sigma_s,\pi_s,\omega_s,p_s,parent_s).
$$

For an add set $I$ and logical remove set $R$, a simple file-set transition is

$$
A_{s+1}=(A_s\setminus R)\cup I.
$$

The transition becomes visible only if the writer commits against the still-current base:

$$
commit(base=s,candidate=S_{s+1})=
\begin{cases}
success, & current=s\land validate(S_s,S_{s+1}),\\
conflict, & current\ne s\lor\neg validate.
\end{cases}
$$

Readers resolve and pin one snapshot before planning. Files written by failed contenders are not members of any snapshot and must be retained long enough to avoid racing active work before orphan collection.

### Critical invariants

- Table membership comes from committed metadata/log/timeline state, never from listing all files beneath the table location.
- A reader pins one snapshot, its schema/spec, manifests/actions, and data/delete applicability for the whole operation.
- Exactly one atomic protocol action advances a given table reference from an observed base; concurrent losers are detectable.
- A successful commit references only durable, complete, format-valid metadata and data/delete artifacts.
- Retry identity records table, operation, base snapshot/version, application transaction, candidate artifacts, and intended semantic change.
- A stale writer validates conflicts at the semantic scope of its operation; blind last-writer-wins is not conflict resolution.
- Logical removal is distinct from physical deletion. Retained snapshots, branches/tags, long readers, streams, rollback, holds, and active writers constrain cleanup.
- File statistics and metadata indexes may prune only when their semantics prove irrelevance; missing, truncated, null/NaN, collation, and evolution cases fall back safely.
- Row deletes apply only to the data/file/sequence scope specified by the format; a delete artifact is not a universal predicate over future rows.
- Checkpoints/manifests/timelines remain consistent with the authoritative protocol and exact version; incomplete auxiliary metadata is ignored or repaired under documented rules.
- Snapshot timestamps are evidence, not universally unique commit identities; reproducible reads record snapshot/version IDs.
- Protocol/feature upgrades are gated on every reader, writer, maintenance job, catalog, and recovery tool that may touch the table.
- Garbage collection proves unreachability across every protected reference and active-operation horizon before deletion.
- Catalog/table metadata, encryption keys, authorization, and file bytes are all included in backup and restore evidence.

### Common failures

Common failures include treating the object prefix as the table; reading `latest` between scan tasks; combining files from different snapshots; committing a pointer without compare-and-swap; retrying a mutation as a new untracked transaction; assuming all concurrent appends are conflict-free; ignoring row-delete applicability; using min/max statistics with wrong null/NaN/collation semantics; trusting an incomplete checkpoint; selecting time travel only by ambiguous wall-clock time; assuming history means data files remain; expiring snapshots below query, stream, rollback, audit, or legal horizons; deleting every file absent from current state; running orphan cleanup with a shorter age than writer duration; upgrading table features before older engines are fenced; bypassing catalog authorization through direct storage access; copying only data files without metadata; restoring metadata without keys; and interpreting snapshot diffs as row-level CDC without operation semantics.

### Compact example

Snapshot 41 contains files `a` and `b`. Writers X and Y both load 41. X writes `c` and atomically commits append snapshot 42 containing `a,b,c`. Y has prepared `d` to replace `a`; its commit against 41 fails because current is 42. Y reloads 42, verifies X's append does not conflict with its targeted replacement, and commits snapshot 43 containing `b,c,d`. A reader pinned to 41 continues to read `a,b`. File `a` cannot be physically removed while snapshot 41 or 42 is retained. A candidate file from an abandoned writer is collectible only after active-operation and protected-reference checks.

### Connections

[DE-061](061-object-storage-as-a-data-substrate.md) establishes immutable-object and conditional-pointer publication; [DE-062](062-raw-standardized-and-curated-zones.md) establishes product transitions and pinned lineage. DE-064 and DE-065 attach evolving schemas and partition specifications to snapshots, DE-066 develops time travel and reproducible reads, DE-067/068 rewrite physical files without changing logical results, DE-069 integrates catalogs, and DE-070 operates a transactional table format end to end.

## Governing Question

Object storage provides durable named bytes, not a table transaction. An analytical table can contain thousands or billions of immutable columnar files. Queries need one answer to “which files, deletes, schema, partition meaning, and properties constitute the table now?” Writers need a safe way to replace that answer.

Table formats supply a metadata protocol. Iceberg represents snapshots through table metadata, manifest lists, and manifests. Delta reconstructs versions from an ordered transaction log and checkpoints. Hudi records actions on a timeline and organizes file groups/slices. These are not interchangeable layouts, but each separates physical artifacts from committed logical state.

The table is therefore not the directory and not merely a catalog name. It is the result of resolving a catalog/location through the format protocol to a committed snapshot/version. Directly listing Parquet files bypasses deletes, schema IDs, partition evolution, transaction boundaries, and protocol features.

The hardest boundary is commit. Writers commonly create data files before obtaining the right to publish them. A conflict or lost response can leave complete but unreachable artifacts. Correctness depends on an atomic metadata/log transition, conflict validation, retry identity, and conservative garbage collection.

Readers must pin state. A distributed scan may run while compaction, append, delete, or schema change commits. Every task must derive from one planned snapshot rather than repeatedly resolving “current.” Snapshot identity is part of query provenance.

## Why This Matters

Without metadata-defined membership, partial jobs become visible. A failed overwrite can leave half the replacement files next to all old files. A prefix scan reads duplicates; a cleanup tool may delete data another snapshot still needs.

Concurrency errors are often silent. Two writers can each produce valid Parquet files and still produce an invalid table history. Optimistic commit makes the shared-state transition explicit and forces stale writers to validate whether their logical changes commute.

Metadata enables scalable planning. File-level partition facts, counts, bounds, null information, and indexes can avoid opening irrelevant files. The metadata tree or checkpoint prevents every reader from listing and parsing the entire data directory or replaying history from the beginning.

Snapshots enable repeatability. A model training run, audit, incident reconstruction, and financial report can identify one exact table state. A “read yesterday at noon” request is weaker because clock interpretation, commit timestamps, retention, and concurrent writes may differ.

Logical and physical deletion must be separated. An update often writes replacement files and removes old files from the new snapshot. Old bytes remain necessary for pinned readers, retained history, branches, rollback, or compliance. Premature vacuum corrupts valid references; infinite retention creates cost and privacy exposure.

Feature compatibility is correctness. A writer can add deletion vectors, new type encodings, row lineage, or another protocol feature that an older reader ignores or misreads. Upgrade gates must cover every engine and maintenance path, not just the primary writer.

Finally, metadata itself is production data. Losing catalog pointers, commit logs, manifests, timelines, keys, or permissions can make intact columnar files unusable. Backup and restore must validate the whole graph.

## Prerequisites and Retrieval

Retrieve table identity: catalog, namespace, stable table UUID/ID, location, format and format version, current metadata/log version, current snapshot/instant, branches/tags, ownership, and environment/tenant.

Retrieve protocol semantics: reader/writer feature requirements, commit primitive, isolation level, conflict detection, retry rules, application transaction IDs, catalog responsibilities, object-store assumptions, and behavior after unknown commit outcomes.

Retrieve snapshot contents: parent, sequence/order, timestamp, operation/summary, schema ID, partition-spec ID, sort order, properties, manifest/log/checkpoint references, active data files, delete artifacts, statistics, and provenance.

Retrieve file identity: canonical path or content ID, version/generation where supported, format, size, record count, partition tuple/spec, column metrics, encryption/key metadata, sequence/data sequence, deletion vector/delete-file relation, and checksum where the format records it.

Retrieve operation semantics: append, dynamic/static overwrite, replace partitions, delete, update, merge, rewrite, compaction, clustering, schema/property/spec change, branch/tag operation, rollback, and whether changes are data-changing or metadata-only.

Retrieve reader behavior: snapshot resolution, cache refresh, planning, manifest/log replay, statistics pruning, delete application, split planning, long-query lifetime, retry, missing/corrupt metadata, direct-file fallback, and query provenance.

Retrieve maintenance: commit frequency, checkpoint interval, manifest count/size, metadata-log/timeline archival, snapshot retention, branch/tag retention, streaming offsets, reader duration, rollback/audit/legal holds, orphan age, cleaning/vacuum procedure, and dry-run evidence.

Retrieve security: catalog authentication, metadata and storage authorization, credential vending, direct object access, table/location mutation, branch/tag control, protocol upgrade authority, encryption/KMS, audit, and permanent-delete separation.

Retrieve recovery: catalog backup, metadata/log/manifest inventory, data/delete artifacts, versioning/replication, keys, RPO/RTO, restore ordering, alternate catalog/location behavior, and drills that execute real queries at named snapshots.

Retrieve observability: commit attempts/success/conflict/unknown outcome, operation duration, stale bases, retry count, metadata bytes/depth, manifests/actions/checkpoints, planning latency, files/bytes selected and pruned, delete density, snapshot/reference age, unreachable candidates, cleanup results, missing references, feature versions, and engine fleet.

Distinguish table name from table ID; location from table state; current pointer from snapshot contents; metadata file from manifest; manifest list from manifest; data file from active membership; remove action from physical deletion; row delete from file removal; snapshot timestamp from snapshot ID; snapshot retention from object versioning; checkpoint from commit; compaction from logical change; orphan candidate from proven garbage; and snapshot diff from change-data semantics.

Create a metadata contract:

| Concern | Required decision and evidence |
|---|---|
| Identity | Catalog/name, immutable table ID, location, format/version and current reference |
| Snapshot | ID/version, parent/order/time, schema/spec/order, active data/deletes and summary |
| Commit | Base, candidate artifacts, atomic primitive, conflict validation, retry and unknown outcome |
| Read | Pinned snapshot, planning path, statistics semantics, deletes, cache and provenance |
| Operation | Append/overwrite/delete/update/merge/rewrite scope and logical invariants |
| Compatibility | Reader/writer features, engine inventory, upgrade gate, fence and rollback |
| Retention | Readers/streams/refs/audit/legal/privacy horizons, expiry and physical-delete boundary |
| Maintenance | Checkpoint/manifest/timeline work, compaction, orphan detection and validation |
| Security | Catalog/storage consistency, roles, direct-access controls, encryption and audit |
| Recovery | Metadata plus data graph, keys, catalog reconstruction, RPO/RTO and tested query |

Write a falsifiable claim: “Table `orders` pins readers to immutable snapshot IDs; every commit records base snapshot, operation ID, exact additions/removals, schema/spec IDs, engine/protocol features, source/run provenance, and control totals; the catalog compare-and-swap is the only current-reference transition; stale writers revalidate operation conflicts; streaming readers retain their starting snapshots; snapshot expiration honors 14-day query, 45-day rollback, tagged audit, and legal-hold constraints; orphan deletion uses a seven-day minimum age greater than maximum write duration; and quarterly restore reconstructs the catalog/metadata/data/key graph and validates named snapshot queries within RTO.”

## Learning Objectives

After completing this module, you should be able to:

1. distinguish table identity, metadata, snapshots, manifests, logs, timelines, checkpoints, files, deletes, and catalog pointers;
2. reconstruct and pin one logical snapshot without listing a data prefix;
3. design optimistic commits with explicit bases, conflict validation, retries, and unknown-outcome reconciliation;
4. reason about append, overwrite, delete, merge, and rewrite changes as metadata/file-set transitions;
5. apply file statistics and delete artifacts conservatively during scan planning;
6. separate logical removal, snapshot expiration, orphan proof, and physical deletion;
7. manage checkpoints, manifests, histories, branches/tags, and streaming commit frequency;
8. gate protocol features across all readers, writers, maintenance tools, and catalogs;
9. protect and recover catalog, metadata, data, delete files, authorization, and encryption keys as one graph; and
10. fault-test snapshot isolation, commit concurrency, cleanup safety, and reproducibility with finite oracles.

## Core Exposition

### Treat metadata as the table's authority

A table location may contain current files, files removed from current state, abandoned candidate files, temporary outputs, metadata versions, indexes, checkpoints, and artifacts owned by active operations. Listing them does not reveal table membership.

Resolve the table through its supported catalog or root metadata protocol. Confirm stable table identity as well as name and location; drop/recreate can reuse a name while representing a different table. Record format/protocol version before parsing artifacts.

The authoritative structure is format-specific. Iceberg table metadata embeds snapshot records and points to a manifest list per snapshot; manifests list data/delete files. Delta defines a serial history of log versions whose actions reconcile into a snapshot, with checkpoints accelerating replay. Hudi's completed timeline actions and file groups/slices define table state. Do not mix one format's invariants into another.

Never hand-edit metadata artifacts. Use a conforming library/catalog operation that validates schema, sequence, checksums, atomicity, and feature rules. A syntactically valid JSON edit can violate reachability or protocol invariants irreparably.

### Pin one snapshot for every read

At planning start, resolve the chosen branch/reference and capture snapshot/version ID, schema/spec, and metadata roots. Every distributed task receives that pinned plan or identity. Refreshing current mid-query would combine states.

Snapshot $s$ represents active file membership and deletion semantics at one logical point. Later commits create new states without changing $s$'s meaning while its required artifacts remain retained.

Cache rules must preserve this distinction. A catalog cache can delay discovery of a newer current snapshot, which may be acceptable under freshness SLO; it must not make the already resolved snapshot internally inconsistent. Cache invalidation cannot substitute for snapshot identity.

For reproducibility, store table ID, snapshot/version, reference, resolved-at time, engine/reader version, projection/filter, and relevant session/timezone/configuration. Snapshot identity fixes table state, not nondeterministic query functions or external joins.

### Understand metadata trees and logs

Metadata scales by summarizing immutable components. In an Iceberg-style tree, current table metadata selects a snapshot; its manifest list summarizes manifests; manifests list individual data/delete files and statistics. Readers prune at each level.

In a Delta-style log, ordered add/remove/metadata/protocol/transaction actions reconcile into a version snapshot. A checkpoint contains resolved state through a committed version, then readers apply later log entries. The checkpoint must not be newer than a requested historical version.

In a Hudi-style timeline, completed actions define visible state while requested/inflight instants support operation coordination. File groups and slices organize base/log file versions; cleaning, compaction, clustering, and archival are timeline actions with specific semantics.

These structures are indexes and histories simultaneously. Corruption, missing artifacts, inconsistent catalog pointers, or unsupported feature actions must fail closed. Falling back to “read every Parquet file” invents a different table.

### Model file-set transitions

For an append, $R=\varnothing$ and new files join the active set. For file rewrite, old files enter $R$ and replacement files enter $I$ while the logical row multiset should remain equal. For overwrite/delete/update/merge, both membership and row semantics change under an explicit predicate and conflict scope.

File-level add/remove is not always row-level change. Compaction can remove files `a,b` and add `c` containing the same rows. Conversely, a delete file can change visible rows without removing the referenced data file.

Record the semantic operation, not only file counts. Include predicate/partition scope, row/control totals, source transaction, application transaction ID, and whether the operation is data-changing. This enables audit and safe incremental consumption.

Logical removal normally writes metadata/tombstones first. Physical files remain until no protected snapshot or operation needs them. This multi-version design lets readers finish on older states.

### Commit optimistically and validate conflicts

A writer loads base $s$, writes candidate data/delete/metadata artifacts, validates them, then tries to advance the catalog/log from $s$. The atomic step linearizes the commit. If current changed, the writer is stale.

A stale append may be safely rebased when format rules and isolation validate no conflicting change. A predicate overwrite, delete, merge, schema update, or partition replacement can conflict even when output file names differ. Use the format library's semantic validation; do not implement “retry latest” blindly.

Conflict detection needs a scope: changed partitions, files matching a predicate, row identities, schema/spec/properties, or table reference. State the isolation level and anomaly prevented for each operation. Marketing-level “ACID” is insufficient.

Persist application transaction identity so crash retry does not commit the same batch twice. For streaming, couple source offsets/batch IDs with the table transaction mechanism documented by the format/engine.

If the commit response is lost, outcome is unknown. Refresh current/history and locate the transaction/snapshot/candidate identity. Adopt the existing success when exact; retry the same logical transaction only under supported rules; quarantine ambiguity. Never delete candidate files until the outcome and active-writer horizon are resolved.

### Plan with statistics safely

Manifest/action metadata may record partition tuples, row counts, lower/upper bounds, null/NaN counts, value counts, column sizes, bloom/index information, and sort order. Planning uses them to prove a file cannot match.

Pruning must be conservative. Missing statistics mean “unknown,” not “empty.” Truncated bounds, string/binary collation, signed zero, NaN, null semantics, timezone conversion, decimal scale, and schema/partition evolution can make naive comparisons unsafe.

Statistics are not constraints. A bound says what the writer reported for a file under the format rules; it does not prove business validity. Protect sensitive statistics because bounds may reveal names, identifiers, or values even without file access.

Measure selectivity at every metadata level: total versus selected manifests, data files, delete files, rows estimates, and bytes. High planning time can result from excessive snapshots, tiny manifests, delete density, or stale/missing stats even when scan bytes are small.

### Apply row-level deletes by format rules

Analytical formats may represent deletes as rewritten data files, equality/position delete files, deletion vectors, log records, or record-key merges. Readers must implement the exact feature and sequence rules advertised by table metadata.

A position delete typically identifies row positions in a specific data file; rewriting that file changes positions. Equality deletes match declared fields under applicability/sequence rules. A deletion vector is associated with a logical data file identity under its protocol. None should be applied indiscriminately to future files.

Delete density affects planning and execution. Many small delete artifacts can dominate open/merge work. Rewrites can materialize deletes into new files, but must preserve concurrent changes and historical snapshots.

Snapshot-to-snapshot file changes do not automatically form row-level CDC. Rewrites can remove/add every file with zero logical row change; updates can appear as delete-plus-insert; some protocols expose explicit change-data features. Consumers need an operation-aware change contract.

### Use checkpoints and metadata rewrites as optimizations

Long logs and many manifests increase planning latency. Checkpoints materialize reconciled state; manifest rewrites regroup file metadata; metadata tables/indexes avoid expensive listings; timeline archival bounds active metadata.

An optimization must preserve snapshot semantics. A checkpoint corresponds to an exact committed version. A manifest rewrite should retain the same data/delete membership and sequence facts. Compaction of log metadata must not erase protocol actions still required to reconstruct retained states.

Writers/readers must tolerate missing optional checkpoints or incomplete candidate optimizations according to format rules. Publish auxiliary artifacts atomically or with discoverability rules that distinguish complete from partial.

Track metadata amplification: metadata bytes and objects per data byte/file/commit, replay depth since checkpoint, manifests per snapshot, entries per manifest, and planning latency. Streaming micro-batches can create metadata faster than data volume suggests.

### Manage branches, tags, and references

A named reference can support audit retention, experimental writes, write-audit-publish, rollback, or development isolation. Its mutability, fast-forward/merge semantics, schema behavior, and retention are format-specific.

A tag commonly pins a historical snapshot; a branch commonly has a movable head and independent lineage/retention. Do not assume Git semantics or cross-format equivalence. Record exact snapshot IDs behind references.

References expand reachability. A snapshot absent from `main` history may remain protected by an audit tag or branch. Cleanup must traverse every retained reference under catalog policy.

Promotion moves a reference or commits validated changes; copying files into `main` paths is not promotion. Consumer acceptance, conflicts, and rollback evidence remain required.

### Expire history without corrupting readers

Snapshot/log/timeline history grows with every commit. Retention must cover maximum query duration, streaming reader/checkpoint lag, rollback, backfill, audit, legal hold, incident investigation, replication, backup, and consumer reproducibility requirements.

Expiration first removes historical states from supported reachability/time travel. Physical deletion follows only for artifacts no retained snapshot/reference needs. Some tools combine these phases operationally; keep the conceptual evidence separate.

An active reader pinned to an expired snapshot can fail when its files are deleted. Coordinate leases or choose retention safely above measured tail query duration with margin. External engines and manually pinned workloads must be included.

Privacy may require shorter retention and deletion propagation. Tags must not become accidental indefinite holds. Catalog every reference owner, purpose, expiry, legal basis, and last use.

### Prove orphans conservatively

Compute protected reachability from every retained snapshot, branch/tag, metadata history required for recovery, active transaction, staging contract, and legal/operational hold. Only files outside that graph and older than the maximum active-writer/visibility horizon are candidates.

Use canonical path semantics. Equivalent paths with different authorities, encoding, case, or normalization can cause false orphan classification. Provider version IDs and table IDs help distinguish replacement/recreation.

Dry-run and inventory candidates by type, age, owner/run, bytes, and reason. Sample/validate against metadata APIs. Apply rate limits, deletion manifests, retry identity, audit, and post-delete reconciliation.

Never use “not in current snapshot” as the predicate. That would delete every file needed solely by history, branches, or pinned readers.

### Gate protocol and feature evolution

Table metadata advertises minimum versions or named reader/writer features. An upgrade can alter delete semantics, types, checkpoints, row IDs, indexes, or commit behavior. Once written, older clients may be unable to read or may be prohibited from writing.

Inventory all query engines, ingestion jobs, stream processors, optimizers, compactors, vacuum tools, catalogs, replication/export jobs, governance scanners, restore tooling, and ad hoc clients. Test exact versions against representative snapshots and failure cases.

Fence unsupported writers before enabling a feature. Dual-read/validate, canary tables, publish acceptance, and preserve rollback only where the protocol permits downgrade. Some feature changes are irreversible without full rewrite.

Unknown metadata/action fields must follow the format's compatibility rules. Ignoring a required delete feature can return deleted rows; rejecting safely is preferable to silent misread.

### Secure catalog and storage together

Catalog authorization controls discovery and often commit; object storage controls bytes. If a principal can bypass the catalog and list/read/delete metadata or data directly, table-level row/column policies and atomic commit guarantees may be bypassed.

Separate read, data-write, metadata-commit, branch/tag administration, protocol upgrade, maintenance, snapshot expiration, orphan deletion, location change, and permanent-delete roles. Query engines generally need only time-bounded access to the files in an authorized snapshot.

Protect metadata confidentiality and integrity. Paths, partition values, statistics, schemas, properties, summaries, and lineage can reveal sensitive facts. Audit catalog resolution and commits as well as object access.

Encryption recovery includes every metadata, data, and delete artifact. Key rotation/destruction must respect retained snapshots. A historical snapshot whose files exist but cannot be decrypted is not recoverable.

### Back up and restore the graph

Backup scope includes catalog table ID/name/reference state, metadata/log/timeline artifacts, manifests/checkpoints/indexes, data files, delete files/vectors, protocol features, branches/tags, authorization policy, encryption keys, and external transaction/lineage evidence.

Order matters. Restore bytes and keys, validate checksums/reachability, reconstruct catalog pointers without inventing a newer state, then run format-native validation and named snapshot queries. Avoid registering a data directory as a new table if stable identity matters.

Test partial-loss cases: current metadata missing but older versions present; checkpoint missing; manifest corrupt; one data/delete file absent; catalog restored behind object replication; key unavailable; branch reference absent; and feature-capable engine unavailable.

Recovery point and time claims need exact snapshot evidence and representative query/control totals. “Objects replicated” is not a table restore drill.

### Observe table metadata as an operational system

Record commit operation/application IDs, base/current/result snapshot, additions/removals/deletes, schema/spec/features, retries/conflicts, duration, source/run, control totals, and unknown-outcome resolution.

Measure snapshot rate/age; active/expired/retained references; metadata/log/checkpoint/manifest objects and bytes; replay depth; planning latency; selected/pruned files/bytes; data/delete file sizes; delete density; commit conflicts by operation; stale bases; orphan candidates/deletions; missing/corrupt references; protocol version fleet; and restore results.

Reconcile each snapshot's reachable graph. Verify unique table identity, valid parent/reference relationships, required metadata, exact file existence/size where feasible, schema/spec IDs, and operation/control summaries. Compare logical query oracles across rewrites.

Alert on trends before hard failure: accelerating metadata growth, old inflight commits, checkpoint lag, tiny manifests, high delete merge ratio, references without owners, cleanup blocked by one stale reader, engines below required feature level, or catalog/object divergence.

## Definitions and Notation

For table $T$, define:

- $s$: immutable snapshot/version identity.
- $current(T)$: currently published snapshot/reference result.
- $A_s$: active data-file identities in snapshot $s$.
- $D_s$: active row-delete artifacts and applicability metadata.
- $\sigma_s$: schema and stable field identities.
- $\pi_s$: partition specification and transform identities.
- $\omega_s$: sort/order definition.
- $p_s$: properties/protocol features required by the snapshot.
- $parent_s$: parent snapshot/version where the format records one.
- $I$: new file identities introduced by a candidate operation.
- $R$: prior file identities logically removed by that operation.
- $B$: base snapshot loaded by a writer.
- $P$: set of protected snapshots/references and active operations.
- $Reach(P)$: transitive set of metadata, data, and delete artifacts required by $P$.
- $U$: authoritative inventory of table-owned artifacts at a compatible cut.

Snapshot state is

$$
S_s=(A_s,D_s,\sigma_s,\pi_s,\omega_s,p_s,parent_s).
$$

A simple file membership transition is

$$
A_{s'}=(A_s\setminus R)\cup I.
$$

For pure rewrite with no logical row change, the required semantic invariant is

$$
Rows(S_{s'})=Rows(S_s),
$$

under the same schema projection and delete semantics, despite $A_{s'}\ne A_s$.

Optimistic publication is

$$
CAS(current(T),B,S_{s'})=
\begin{cases}
committed, & current(T)=B\land validate(B,S_{s'}),\\
conflict, & otherwise.
\end{cases}
$$

At reader resolution time $t_0$:

$$
plan(q,T,t_0)=plan(q,S_{resolve(T,t_0)}),
$$

and later current changes do not alter this plan's snapshot identity.

Conservative orphan candidates at inventory cut $c$ and minimum safe age $H$ are

$$
O_{candidate}=\{f\in U_c:f\notin Reach(P_c)\land age_c(f)>H\}.
$$

The table-membership invariant is:

> An artifact contributes to a read only through the pinned snapshot and protocol-defined reachability/applicability graph, never merely because it exists under a location.

The commit invariant is:

> One atomic protocol transition publishes a validated candidate against an observed base; stale or ambiguous writers cannot silently replace current state.

The cleanup invariant is:

> Physical deletion occurs only after proving an artifact is unreachable from every protected snapshot/reference and active operation for longer than the conservative safety horizon.

## Mechanisms, Invariants, or Proof Structure

Use this review sequence:

1. **Resolve identity.** Record catalog/name, stable table ID, location, format/protocol/features, reference, and current snapshot/version.
2. **Pin and traverse.** Resolve one snapshot; follow only protocol-defined metadata/log/timeline, manifests/actions, data, and deletes.
3. **Define the operation.** State append/overwrite/delete/merge/rewrite semantics, base, scope, additions/removals, schema/spec, totals, and transaction identity.
4. **Validate commit.** Persist artifacts, validate format/content, atomically advance the commit point, detect stale base, and reconcile unknown outcomes.
5. **Plan conservatively.** Apply stats/deletes only under correct types, sequences, null/NaN/evolution, and feature rules; unknown means scan or fail safely.
6. **Manage metadata.** Bound logs/manifests/checkpoints/timelines while preserving exact retained snapshot reconstruction.
7. **Protect history.** Inventory readers, streams, rollback, branches/tags, audit/legal/privacy, backup, and key horizons before expiration.
8. **Collect safely.** Compute protected reachability, active-writer age, canonical paths, dry-run, delete by manifest, and reconcile.
9. **Gate compatibility/security.** Inventory engines/tools, test features, fence old clients, align catalog/storage policy, and preserve audit/keys.
10. **Fault-test recovery.** Inject concurrency, timeout, partial artifacts, corrupt metadata/data/delete, stale caches, cleanup races, catalog/key loss, and restore named snapshots.

Proof sketch for reader snapshot isolation from concurrent commits:

1. Reader R resolves table T once to committed snapshot $s$.
2. $s$ and every metadata/data/delete artifact reachable from it are immutable for the protected read horizon.
3. R derives every task from $S_s$ and never refreshes current membership mid-read.
4. Writer W creates new immutable artifacts without modifying those reachable from $s$.
5. W atomically advances current from $s$ (or a later base) to $s'$.
6. New readers may resolve $s'$, but R retains $s$ and its plan.
7. Cleanup cannot delete $Reach(s)$ while R's protected horizon/lease applies.
8. Therefore W's commit cannot make R observe a mixture of $s$ and $s'$.

This proof is conditional on conforming clients, atomic reference publication, artifact immutability, and retention of the pinned graph. It does not establish a particular format's write isolation or protect readers that bypass metadata.

The executable model demonstrates pinned reads, file-set snapshots, optimistic conflict, semantic rebase, history reachability, and orphan classification. It uses integer versions and sets; it does not model row deletes, schemas, manifests, catalog failures, object versions, security, or a real table-format specification.

<!-- bijux-verify: {"id":"snapshot-file-set-commit","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"snapshots=((1, ('a', 'b')), (2, ('a', 'b', 'c')), (3, ('b', 'c', 'd')))\npublish_append=('committed', 2)\nstale_replace=('conflict', 2)\nrebased_replace=('committed', 3)\npinned_reader_1=('a', 'b')\ncurrent_reader=('b', 'c', 'd')\nprotected_reachable=('a', 'b', 'c', 'd')\norphan_candidates=('loser',)\nhistory_reconciles=True\n","stderr":""}} -->
```python
class Table:
    def __init__(self):
        self.snapshots = {1: frozenset(("a", "b"))}
        self.current = 1
        self.inventory = {"a", "b"}

    def prepare(self, *files):
        self.inventory.update(files)

    def commit(self, base, additions=(), removals=()):
        if base != self.current:
            return ("conflict", self.current)
        before = self.snapshots[base]
        if not set(removals).issubset(before):
            return ("invalid_remove", self.current)
        after = (before - set(removals)) | set(additions)
        if not after.issubset(self.inventory):
            return ("missing_file", self.current)
        new_id = self.current + 1
        self.snapshots[new_id] = frozenset(after)
        self.current = new_id
        return ("committed", new_id)


table = Table()
reader_snapshot = 1
writer_append_base = table.current
writer_replace_base = table.current

table.prepare("c")
publish_append = table.commit(writer_append_base, additions=("c",))

table.prepare("d", "loser")
stale_replace = table.commit(writer_replace_base, additions=("d",), removals=("a",))
rebased_replace = table.commit(table.current, additions=("d",), removals=("a",))

protected = (1, 2, 3)
reachable = set().union(*(table.snapshots[snapshot] for snapshot in protected))
orphans = table.inventory - reachable
expected = {
    1: frozenset(("a", "b")),
    2: frozenset(("a", "b", "c")),
    3: frozenset(("b", "c", "d")),
}

print(f"snapshots={tuple((key, tuple(sorted(value))) for key, value in sorted(table.snapshots.items()))}")
print(f"publish_append={publish_append}")
print(f"stale_replace={stale_replace}")
print(f"rebased_replace={rebased_replace}")
print(f"pinned_reader_1={tuple(sorted(table.snapshots[reader_snapshot]))}")
print(f"current_reader={tuple(sorted(table.snapshots[table.current]))}")
print(f"protected_reachable={tuple(sorted(reachable))}")
print(f"orphan_candidates={tuple(sorted(orphans))}")
print(f"history_reconciles={table.snapshots == expected}")
```

File `loser` is only a candidate. A production cleaner also proves ownership, age, absence from branches/tags and active writers, canonical path equivalence, retention/hold state, and compatible inventory cuts.

## Alternatives and Trade-Offs

**Manifest tree versus ordered action log.** Trees provide hierarchical pruning and reuse; logs express incremental history naturally and use checkpoints to bound replay. Their commit and recovery rules differ, so choose ecosystem/semantics rather than file-count aesthetics.

**Copy-on-write versus merge-on-read.** Copy-on-write materializes updates into new base files for simpler/faster reads at write amplification. Merge-on-read appends deltas/delete logs for faster writes while shifting merge, compaction, and operational complexity to readers/services.

**File rewrite versus delete artifacts.** Rewrites reduce delete-merge overhead but touch more bytes and conflict scope. Delete files/vectors make row changes cheap but add feature compatibility, planning, retention, and compaction obligations.

**Serializable versus snapshot isolation.** Stronger conflict validation prevents more anomalies but can reject/retry concurrent work. Weaker scopes improve throughput only when allowed anomalies match the operation contract. Use format-specific guarantees.

**Central catalog pointer versus location-derived log.** Catalog commits can provide atomicity, identity, authorization, and multi-table services. Location-based discovery improves portability/self-description but depends on storage/log listing and locking semantics.

**Snapshot ID versus timestamp selection.** IDs are exact and reproducible. Timestamps are convenient for humans but can be ambiguous and disappear under retention; resolve once and record the resulting ID.

**Frequent versus coarse commits.** Frequent snapshots reduce freshness latency and incremental unit size but amplify metadata, conflicts, and maintenance. Coarse commits improve file/metadata shape but increase latency and retry blast radius.

**Full replay versus checkpoints.** Log replay preserves simple append-only authority but grows planning cost. Checkpoints accelerate state reconstruction while adding completion, compatibility, and cleanup rules.

**Long history versus aggressive expiration.** Long retention supports rollback, audit, reproducibility, and lagging streams at storage/privacy/metadata cost. Aggressive expiry bounds cost but can fail readers and eliminate recovery evidence.

**Branches/tags versus separate table copies.** References reuse files and express lineage efficiently but couple lifecycle and feature/schema context. Copies isolate blast radius and ownership at storage, synchronization, and provenance cost.

**Automatic versus scheduled maintenance.** Inline maintenance can keep metadata healthy continuously but adds write latency/conflicts. Scheduled services isolate resources and policy but can fall behind and need ownership/SLOs.

**Format-native metadata versus external index/catalog cache.** Native metadata preserves portable authority. External indexes accelerate discovery/planning and governance but must declare freshness and never override committed membership.

**Direct storage access versus credential-vended access.** Direct roles simplify some engines but can bypass catalog policy and expose broad locations. Vended/scoped credentials improve control while adding catalog availability and integration dependencies.

## Failure Modes and Misconceptions

1. **“The table is its folder.”** The folder contains more and less than the current logical state; metadata defines membership.
2. **“Parquet readers can bypass the format.”** They miss deletes, schema/spec IDs, transaction boundaries, and feature semantics.
3. **“Latest can be resolved per task.”** Concurrent commits then create mixed snapshots. Resolve once at planning.
4. **“Optimistic means no coordination.”** Writers coordinate at the atomic commit point and validate stale-base conflicts.
5. **“All appends commute.”** Schema, partition, properties, overwrite predicates, uniqueness, or application semantics can conflict.
6. **“Retry latest is always safe.”** A stale delete/merge/overwrite can erase concurrent changes. Revalidate semantic scope.
7. **“A timeout is a failed commit.”** It is unknown until current/history and transaction identity are reconciled.
8. **“Remove action deletes bytes.”** It changes later logical state; physical cleanup is separate.
9. **“Absent from current means orphan.”** History, references, readers, streams, or active writers may require it.
10. **“Old data is safe while metadata exists.”** Vacuum may delete files; verify complete reachability, not snapshot records alone.
11. **“A checkpoint is an independent backup.”** It is a protocol optimization at one version and may omit provenance/change actions.
12. **“Missing statistics means no matches.”** Missing means unknown; unsafe pruning loses rows.
13. **“Min/max is obvious.”** Nulls, NaN, truncation, collation, decimals, timestamps, and evolution alter comparisons.
14. **“A delete predicate applies forever.”** Delete artifacts have file/sequence/applicability scope.
15. **“File diffs equal CDC.”** Rewrites change files without changing rows; use an explicit change contract.
16. **“Compaction is metadata-only.”** It rewrites physical files and can conflict, fail, or alter results if implemented badly.
17. **“Timestamp uniquely names a snapshot.”** Clocks/ties/interpretation and retention make IDs safer.
18. **“Tags are free labels.”** They may retain large graphs and block deletion/privacy obligations.
19. **“Vacuum defaults fit our workload.”** Query, stream, rollback, audit, and legal horizons are local evidence.
20. **“Orphan cleanup can use a tiny age.”** It may race writers whose files precede commit.
21. **“Feature enablement is reversible.”** Older clients may be fenced permanently or require full rewrite to downgrade.
22. **“Catalog policy controls direct object reads.”** Broad storage permissions can bypass integrated controls.
23. **“Replicating data files restores a table.”** Catalog, logs/manifests/deletes, features, keys, and permissions are required.
24. **“Green commits prove healthy metadata.”** Planning debt, stale references, cleanup risk, and incompatible clients can accumulate silently.

## Worked Examples

### Example 1

A directory contains files `a`, `b`, `c`, and abandoned `x`. Snapshot 9's manifest includes `a,b` plus a delete file. A raw Parquet glob reads four data files and ignores the delete; the format-native reader resolves exactly snapshot 9 and applies its delete semantics.

### Example 2

Two writers load version 20. An append commits version 21. A partition overwrite from version 20 must check whether version 21 added files matching its target predicate. It rebases only if format validation proves no conflicting rows/files; different output names are insufficient.

### Example 3

A commit request times out after publishing application transaction `source-A/batch-77`. On restart, the writer finds that transaction in snapshot history and adopts its result. Recommitting as batch 78 would duplicate effects.

### Example 4

A query pins snapshot 100 for four hours while snapshot 101 compacts its files. The query continues reading old files. A vacuum horizon of one hour could delete them mid-query; measured tail duration plus margin and active-reader policy must exceed four hours.

### Example 5

A manifest records lower/upper string bounds truncated to a format-defined length. A predicate comparison that treats the truncated upper bound as an exact full value can prune a matching file. A conforming evaluator applies the specified inclusive/truncation semantics or scans.

### Example 6

A position-delete artifact marks row 17 in file `f`. Compaction rewrites surviving rows into `g`; the old position delete does not apply to row 17 of `g`. The new snapshot removes `f` and its applicable delete relationship and publishes `g` consistently.

### Example 7

Delta-style version 480 is reconstructed from checkpoint 450 plus log actions 451–480. A time-travel query for 440 cannot start from checkpoint 450; it uses an older valid checkpoint/log path. A partial candidate checkpoint is not treated as committed state.

### Example 8

An audit tag pins snapshot 75 while main advances to 120. Snapshot 75's unique files remain reachable and cannot be garbage-collected. The tag has owner, legal basis, expiry review, and size attribution so retention is deliberate.

### Example 9

A new writer enables a row-delete feature. One forgotten export engine cannot interpret it. The upgrade gate fails, the engine is upgraded or fenced, and only then is the feature committed. Silent fallback to base-file reads would resurrect deleted rows.

### Example 10

A disaster restore copies all data files but omits the catalog pointer and two manifest files. Listing and registering the location produces an invented table that ignores deletes/history. The valid recovery restores metadata graph and keys, verifies reachability, then runs snapshot-specific control queries.

## Cross-Program Connections

- **Database Systems:** MVCC, snapshots, serializability, write sets, tombstones, indexes, WAL/checkpoints, catalogs, and vacuum provide direct conceptual foundations.
- **Distributed Systems:** compare-and-swap, immutable artifacts, optimistic concurrency, uncertain outcomes, leases, consensus-backed catalogs, and partial failure define commit safety.
- **Data Structures Engineering:** persistent trees, logs, manifests, reachability graphs, set difference, indexes, and compaction explain metadata scaling.
- **Operating Systems:** filesystem directory/inode semantics contrast with object storage; copy-on-write and page/version reclamation illuminate snapshot retention.
- **Software Engineering:** protocol compatibility, feature flags, semantic versioning, adapters, transaction identity, invariants, and migration gates prevent cross-engine corruption.
- **Reliability Engineering:** SLOs, fault injection, RPO/RTO, cleanup safety, restore drills, metadata debt, and reconciliation make table state operable.
- **Information Security:** catalog/storage authorization, metadata confidentiality, audit, encryption keys, least privilege, and destructive-role separation protect the graph.
- **Privacy Engineering:** history, branches/tags, backups, delete files, retention, legal holds, and derived snapshots complicate erasure evidence.
- **Formal Methods:** state transitions, linearization points, reachability, invariants, and conflict predicates permit precise safety arguments.
- **Streaming Systems:** micro-batch transaction identity, source offsets, frequent snapshots, incremental reads, late correction, and retention horizons intersect table metadata.

## References

1. Apache Iceberg. [Table specification](https://iceberg.apache.org/spec/). Accessed 2026-09-03. Primary specification for table metadata, snapshots, manifest lists, manifests, data/delete files, sequence fields, and optimistic concurrency.
2. Apache Iceberg. [Reliability](https://iceberg.apache.org/docs/latest/reliability/). Accessed 2026-09-03. Primary project documentation for atomic commits, snapshot isolation, optimistic concurrency, retry, and concurrent-write validation.
3. Apache Iceberg. [Maintenance](https://iceberg.apache.org/docs/latest/maintenance/). Accessed 2026-09-03. Primary documentation for snapshot expiration, metadata cleanup, orphan-file hazards, compaction, and manifest rewriting.
4. Apache Iceberg. [Branching and Tagging](https://iceberg.apache.org/docs/latest/branching/). Accessed 2026-09-03. Primary documentation for snapshot references, branch/tag semantics, write-audit-publish, and independent retention.
5. Apache Iceberg. [Spark queries](https://iceberg.apache.org/docs/latest/spark-queries/). Accessed 2026-09-03. Primary documentation for inspecting history, snapshots, files, manifests, references, and other metadata tables.
6. Apache Iceberg. [Structured Streaming](https://iceberg.apache.org/docs/latest/spark-structured-streaming/). Accessed 2026-09-03. Primary documentation for per-batch snapshots and streaming-table snapshot, file, and manifest maintenance.
7. Delta Lake. [Delta Transaction Log Protocol](https://github.com/delta-io/delta/blob/master/PROTOCOL.md). Accessed 2026-09-03. Primary specification for MVCC snapshots, ordered actions, atomic versions, tombstones, protocol features, checkpoints, transaction IDs, and cleanup.
8. Delta Lake. [Concurrency control](https://docs.delta.io/latest/concurrency-control.html). Accessed 2026-09-03. Primary documentation for optimistic concurrency, write stages, isolation, conflicts, retries, and operation interactions.
9. Apache Hudi. [The Hudi Stack](https://hudi.apache.org/docs/hudi_stack/). Accessed 2026-09-03. Primary documentation for timelines, file groups/slices, and the metadata table.
10. Apache Hudi. [Timeline](https://hudi.apache.org/docs/next/timeline/). Accessed 2026-09-03. Primary documentation for requested, inflight, and completed instants and commit, replace, clean, compaction, and rollback actions.
11. Apache Hudi. [Table and Query Types](https://hudi.apache.org/docs/table_types/). Accessed 2026-09-03. Primary documentation for copy-on-write, merge-on-read, base/log files, snapshots, read-optimized, and incremental queries.
12. Apache Hudi. [Table Metadata](https://hudi.apache.org/docs/metadata/). Accessed 2026-09-03. Primary documentation for file/statistics metadata indexing and cleaner, compaction, and timeline-archival coordination.

## Exercises

### Exercise 1

Starting from snapshot 12 with files `{a,b,c}`, model: writer X appends `{d}`; writer Y, from the same base, overwrites `{b}` with `{e}`; a compactor later rewrites `{a,c}` into `{f}` without logical row change. Give snapshot file sets, commit/conflict decisions, semantic validations, and which files remain physically protected while snapshots 12–15 are retained.

### Exercise 2

Design a snapshot reader that supports exact version and timestamp selection, manifest/log/checkpoint planning, statistics pruning, row-delete application, caching, distributed tasks, and provenance. Explain safe behavior for missing stats, unsupported features, an incomplete checkpoint, and current changing during execution.

### Exercise 3

Specify an idempotent optimistic write protocol for a streaming batch. Include source position/batch identity, base snapshot, candidate files, validation, atomic commit, stale-base conflict, lost commit response, checkpoint coupling, and abandoned-file ownership.

### Exercise 4

Create a retention and garbage-collection policy for a table with six-hour queries, a stream that may lag three days, 30-day rollback, annual audit tags, privacy deletion, seven-hour worst-case writers, and cross-region replication. State protected references, minimum age, dry-run, canonical-path, deletion, and reconciliation evidence.

### Exercise 5

Plan a table-feature upgrade enabling row-level deletes across five engines and three maintenance tools. Include inventory, compatibility tests, fencing, canary, concurrent write/read faults, rollback limits, catalog/storage authorization, backup/restore, and acceptance criteria.

## Answers to the Exercises

### Answer 1

Snapshot 12 is `{a,b,c}`. X commits append snapshot 13 `{a,b,c,d}`. Y's commit against 12 conflicts because current is 13. Y reloads 13 and validates whether X touched its overwrite predicate; if not, it commits 14 `{a,c,d,e}`. Compaction loads 14, writes `f`, proves `Rows(a)+Rows(c)` equals `Rows(f)` under the same schema/delete semantics, and commits 15 `{d,e,f}`. With 12–15 retained, reachability is `{a,b,c,d,e,f}`: even files absent from current remain protected. Any failed contender artifacts outside all protected references remain candidates only after writer and retention safety checks.

### Answer 2

Resolve stable table ID and format features, choose exact version or map timestamp once to a version, and pin it. Select the newest complete checkpoint no newer than the target when the protocol permits, replay required actions or traverse table metadata/manifest lists/manifests, then plan active data and applicable delete artifacts under the snapshot schema/spec. Missing stats cause scan, not prune; unsupported required features fail closed; incomplete auxiliary metadata is ignored under format rules; cached metadata is keyed by immutable version. Every task receives the same snapshot/file/delete plan. Provenance records catalog, table ID, reference, exact version, resolved time, reader/features, query/config, and input files/control totals.

### Answer 3

Use stable transaction identity `(source, partition-set, start/end positions, batch)` and record it in supported table transaction metadata. Load base snapshot and features, deterministically create unique candidate data/delete files, validate size/schema/stats/control totals, and attempt the format's atomic commit against base. If stale, inspect intervening operations and rebase only when semantic conflict validation passes. If response is lost, refresh history and find the exact transaction/candidate snapshot; adopt success or retry the same logical transaction under protocol rules. Advance the external/source checkpoint only when the table commit identity is durably recoverable. Persist abandoned-file ownership and retain beyond maximum writer/recovery duration before orphan consideration.

### Answer 4

Protected reachability includes current/main history for at least 30 days, stream starting snapshots/positions for at least three days plus recovery margin, active six-hour readers, annual audit-tag graphs, legal holds, in-flight replication, restore points, and active writers. The orphan minimum age must exceed seven-hour worst-case writer duration plus observation/replication margin; it does not shorten snapshot protection. Catalog each reference owner/expiry and coordinate privacy requests against lawful holds, derived snapshots, replicas, and backups. Use compatible-cut inventory, canonical paths/version IDs, a dry-run grouped by reason/age/run/bytes, approval and deletion manifests, rate-limited idempotent deletes, and post-delete reachability/query reconciliation. Never delete from current-only difference.

### Answer 5

Inventory exact versions of all query, batch, stream, export, compact, optimize, vacuum, catalog, scanner, replication, and restore clients. Test feature parsing, deleted-row correctness, sequence/applicability, old/new snapshot reads, writes, compaction, cleanup, and recovery. Fence every unsupported writer and deny/bypass-proof direct file readers before enabling. Canary a representative table, run concurrent append/delete/rewrite and lost-response faults, compare control queries, and validate catalog/storage authorization. Capture pre-upgrade snapshots and backups but document whether protocol downgrade is actually supported; rollback may require rewriting into a new compatible table. Accept only when every required client passes, unsupported paths are fenced, restore succeeds with keys/metadata/deletes, monitoring recognizes the feature, and owners approve irreversible consequences.
