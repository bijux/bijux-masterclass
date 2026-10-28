---
module_id: DE-066
program: Data Engineering
level: 2
module_number: 66
title: Time Travel and Reproducible Reads
status: complete
last_verified: 2026-09-03
---

# Time Travel and Reproducible Reads

## One-Page Review

### Governing question

How can a data product retrieve and prove the same historical logical state after newer commits, schema and partition evolution, compaction, deletes, catalog moves, engine upgrades, policy changes, and retention—without confusing a wall-clock timestamp, mutable branch, backup, restore, or change feed with an immutable reproducibility contract?

### Essential definitions

- A **snapshot/version/instant** is a format-specific immutable table state or completed point on a table timeline.
- **Time travel** selects a historical table state by immutable identity, timestamp resolution, or named reference rather than the current state.
- A **snapshot read** returns the logical rows visible at one table state after applying its schema, files, deletes, and protocol rules.
- **Snapshot isolation** means a read remains bound to its selected state while concurrent commits create newer states.
- A **snapshot ID or table version** is the preferred exact selector when the format guarantees immutable identity within a stable table identity.
- A **timestamp-as-of selector** resolves a wall-clock instant to a version under format/catalog rules; the timestamp itself is not usually the version identity.
- A **tag** is commonly a named reference to one snapshot; a **branch** is commonly a mutable lineage head. Exact semantics and retention are format-specific.
- A **reproducibility capsule** records the complete identities and semantics needed to reconstruct a result, including every input state, code, configuration, dependencies, and execution contract.
- A **consistent cut** is one mutually meaningful selection of states across multiple changing inputs; independently reading each “latest” is not a consistent cut.
- **Event time** says when a domain event occurred; **valid time** says when a fact is true in the modeled world; **system/transaction time** says when a system recorded it; **commit time** orders or timestamps table changes.
- **Bitemporal data** models valid time and system time explicitly. Storage time travel alone does not reconstruct arbitrary business-valid history.
- An **incremental or change query** returns changes between boundaries; it is not the same result as a snapshot at an endpoint.
- **Restore/rollback** changes a current reference or writes a new state resembling an old one; it is operational mutation, not merely a historical read.
- A **reproducibility horizon** is the interval during which required metadata, files, schemas, deletes, keys, code, dependencies, and permissions are guaranteed available.
- **Logical reproducibility** recreates the same declared rows/values; **bitwise reproducibility** recreates identical bytes, ordering, floating-point results, and serialization under a stricter contract.

### Central model, mechanism, or theorem

For table identity $T$ and immutable state identity $v$, define

$$
S(T,v)=(Schema_v,Specs_v,Data_v,Deletes_v,Protocol_v,Properties_v).
$$

Query result $Y$ is a function of more than that state:

$$
Y=Eval(Q,\{S(T_i,v_i)\}_{i=1}^{n},Code,Config,Runtime,External,Policy).
$$

A reproducibility capsule $C$ must bind each relevant argument by immutable identity or archive it. If any argument is resolved from mutable `latest`, a mutable branch, an unversioned UDF, current timezone data, a changing external API, or missing encryption key, equality of rerun results is not guaranteed. For multi-table computation, the vector $(v_1,\ldots,v_n)$ must represent an accepted consistent cut, not merely individually valid versions.

### Critical invariants

- A historical read records stable table identity and exact immutable snapshot/version/instant, not only a table name, path, timestamp, or `latest`.
- Timestamp resolution records timezone, precision, comparison rule, catalog/engine version, and the resolved immutable identity.
- Readers use the historical state's schema, partition specifications, files, delete semantics, protocol, and feature set according to the chosen format/API.
- A pinned read does not drift to newer commits during planning, retries, pagination, or distributed task execution.
- Every table, reference dataset, model, feature view, file set, and external input is versioned or captured.
- Query/code digest, parameters, UDF/library/runtime versions, locale, timezone database, numeric mode, randomness, and nondeterministic functions are controlled.
- Multi-table jobs use an explicit cut or published data-product release whose constituent versions are recorded.
- Retention preserves the complete reachability closure: logs/metadata/checkpoints/manifests, data and delete files, schemas/specs, keys, catalog mapping, and required software/artifacts.
- Tags/branches/savepoints protect history only under explicit lifecycle rules; names alone are not retention proof.
- Snapshot expiration, vacuum, cleaning, key destruction, privacy erasure, and catalog deletion cannot violate promised horizons or active-reader/stream windows.
- Restore is authorized and audited as a new operational change; downstream incremental consumers are assessed for replay/duplicates.
- Reproducibility claims state equality level, scope, tolerance, order semantics, and allowed environmental variation.
- Evidence distinguishes a successful rerun from proof that future reruns remain possible.

### Common failures

Common failures include recording only `TIMESTAMP AS OF`; using local time without offset; assuming commit clocks are unique or monotonic; resolving a mutable branch later; querying several tables at independently observed `latest`; applying today's schema or partition spec to old files; expiring delete files or logs but retaining some data objects; copying a table while changing file timestamps; assuming a backup is queryable; confusing snapshot with incremental/CDC output; treating restore as a read; replaying restored files into streaming consumers; using `CURRENT_TIMESTAMP`, unseeded randomness, unordered limits, floating reductions, or mutable UDFs; omitting reference-data/model versions; losing encryption keys; asserting bitwise identity from equal row counts; and promising permanent history while privacy or legal requirements demand deletion.

### Compact example

A revenue job reads orders snapshot 812 and exchange-rates version 44 using query digest `q7`, UTC timezone, decimal rounding `HALF_EVEN`, runtime image digest `r3`, and code commit `c9`. Its capsule records those identities and an accepted publication barrier connecting the two inputs. Later, `orders` advances to 820, the rates table corrects history, and a branch moves. Rerunning from the capsule still reads 812/44. Rerunning “as of 09:00” or from branch names may resolve differently; retaining only the output count does not prove identical revenue rows.

### Connections

[DE-004](004-avro-protocol-buffers-and-schema-aware-serialization.md) supplies writer/reader resolution, [DE-030](030-designing-replayable-raw-ingestion.md) preserves replay inputs, [DE-057](057-event-time-and-processing-time.md) distinguishes event time and processing time, [DE-058](058-windows-and-watermarks.md) defines event-time progress, [DE-060](060-handling-late-duplicate-and-out-of-order-events.md) covers late corrections, [DE-063](063-table-metadata-and-snapshots.md) defines atomic table states, [DE-064](064-schema-evolution.md) governs historical schemas, and [DE-065](065-partition-evolution-in-data-pipelines.md) governs mixed specs. DE-067/068 explain physical rewrites that should preserve logical history; DE-069/070 govern catalogs and lifecycle operations.

## Governing Question

“Run the report again” sounds simple until every dependency has moved. The table has new commits. A schema renamed a field. A compactor replaced files. A reference table corrected yesterday's exchange rate. An engine upgraded timezone data. A UDF package changed. A vacuum removed historical objects. The result may differ even if the SQL text is unchanged.

Time travel solves one part: select a historical logical state of one table. Transactional table formats record immutable states and the file/delete/schema metadata needed to reconstruct them. A reader can select by version, snapshot ID, instant, timestamp, tag, or branch according to the format and engine.

Reproducibility is a closure property. The computation depends on every input state, code artifact, configuration, external dependency, identity/authorization context that affects row visibility, and execution semantics that affect values or ordering. Each must be immutable, archived, or incorporated into the result's declared uncertainty.

Timestamp travel is convenient discovery but weak identity. A format maps the supplied time to a commit using its ordering and timestamp rules. Timestamp precision, duplicate timestamps, clock adjustment, timezone parsing, catalog history, and copied file modification times can change or obscure that mapping. Resolve once, then persist the immutable snapshot/version.

Multiple tables add a distributed-systems problem. Snapshot isolation of each table does not create a global transaction across them. Reading table A, then `latest` table B can combine states that never formed an approved release. Reproducible pipelines record a version vector or consume a release manifest published after all constituents are ready.

The governing answer is therefore: time travel is a storage capability; reproducible reading is an end-to-end contract over immutable identities, consistent cuts, deterministic semantics, retention, security, and evidence.

## Why This Matters

Audits, financial close, incident investigations, scientific results, model training, feature generation, customer invoices, and regulatory evidence require more than plausible reruns. They require explaining exactly which facts were visible, under which meaning, and why a later evaluator can reconstruct or verify the result.

Historical table state changes logical answers even when files remain. Deletes can remove rows; updates can replace them; equality or position deletes can alter visibility; schema defaults can synthesize historical values; partition evolution changes planning; row-level feature upgrades change required readers. A raw file list does not encode the full relation.

Retention is part of correctness. Metadata history without data files cannot answer the query. Data files without transaction logs/manifests cannot prove membership. Both without delete files can resurrect records. All without encryption keys are unreadable. A catalog entry without stable table identity can point at a recreated table with the same name.

Time dimensions answer different questions. “What did our system know at quarter close?” uses system/commit history. “What contract was valid on the service date?” uses valid time. “Which records arrived during the outage?” may use ingestion/processing time. Storage time travel cannot invent valid-time history if updates overwrote it before capture.

Restore carries blast radius. Moving the main table back, or creating a new commit that reintroduces old files, changes what current readers and streams observe. A downstream change consumer may process restored rows again. Historical `SELECT` is read-only; restore is production mutation with authorization, notification, and recovery implications.

Exact reproducibility is sometimes impossible or undesirable. Privacy erasure, key destruction, licensing limits, and retention budgets can intentionally close the horizon. The honest design states the horizon and preserves derived evidence or approved aggregates where lawful. “Forever” is not a default.

## Prerequisites and Retrieval

Retrieve table identity and history: catalog namespace, stable table UUID, canonical location, protocol/format, current version, snapshot/commit/instant log, parents, operation types, commit timestamps and timezones, schemas, partition/sort specs, properties, branches/tags/savepoints, and retention rules.

Retrieve the exact historical state: immutable version/snapshot/instant; metadata/log/checkpoint/manifest closure; active data and delete files; schema ID; spec IDs; sort order; sequence numbers; protocol features; statistics; encryption keys; and catalog mapping. Verify that every referenced artifact exists and is readable.

Retrieve selector semantics: `VERSION AS OF`, `TIMESTAMP AS OF`, system-time syntax, branch/tag behavior, timestamp parsing zone/precision, rule for choosing a commit at or before time, name precedence, historical schema selection, and engine/connector limitations.

Retrieve all computation inputs: table versions, stream offsets, object versions, files and checksums, reference/lookup tables, feature definitions, model/embedding versions, secrets/configuration that influence logic, APIs, calendars, timezone database, exchange rates, and manual overrides.

Retrieve computation identity: normalized query and digest, source commit, build artifact/container digest, dependency lock, UDF versions, optimizer/runtime/connector/catalog versions, session properties, timezone, locale/collation, decimal and overflow behavior, ANSI mode, null/NaN semantics, random seeds, concurrency, and hardware accelerators where numerics depend on them.

Retrieve access semantics: user/service principal, row/column policies, masks, views, entitlement snapshot, purpose/consent state, credential/key versions, and whether historical access should apply historical or current authorization policy. Reproducibility never authorizes forbidden access.

Retrieve output contract: logical versus bitwise equality, selected columns/types, ordering, partition/file encoding, tolerance for floating values, duplicate semantics, expected row/key counts, digest algorithm, audit evidence, publication ID, and downstream consumers.

Retrieve retention and recovery: metadata/log retention, data/delete-file retention, tag/branch/savepoint lifecycle, cleaner/vacuum/snapshot-expiration schedule, orphan policy, stream lag, longest reader/job, legal holds, erasure deadlines, backups, catalog backup, key escrow, code/artifact registry retention, and restore drills.

Retrieve multi-input coordination: upstream run IDs and version vector, watermark/cutoff, transaction or publication barrier, release manifest, dependency DAG, late/correction policy, retry identity, and whether inputs represent one domain-consistent state.

Distinguish snapshot ID from timestamp; table name from table identity; tag from branch; historical read from restore; snapshot query from incremental/CDC query; storage commit time from event/valid time; reproducible inputs from deterministic execution; logical row equality from byte/order equality; retention intent from verified reachability; and authorization to retain from authorization to read.

Create a reproducibility capsule:

| Dimension | Required binding and evidence |
|---|---|
| Table state | Stable table ID, exact version/snapshot/instant, schema/spec/delete/protocol identities |
| Selection | Original selector, timezone/precision/rule, resolved immutable identity, resolution time/tool |
| Multi-input cut | Version vector, release/barrier ID, dependency graph, event/system cutoffs |
| Computation | Query/code digest, parameters, UDF/build/runtime/dependency identities |
| Semantics | Locale, timezone data, collation, numeric/null/NaN/overflow/order/randomness rules |
| External state | Versioned lookups, models, APIs/captured responses, calendars, secrets that affect logic |
| Access | Principal, policy/mask/view versions, purpose, approvals, key availability |
| Output | Schema, equality level, ordering/tolerance, counts/digests, location/publication ID |
| Lifecycle | Retain-until, hold/erasure constraints, cleanup gates, recovery evidence and owner |

Write a falsifiable claim: “Release `finance-close-2026-08` binds stable tables orders/FX/ledger to versions 812/44/227 under publication barrier 91; query digest Q7, code C9, runtime image R3, UTC timezone data Z12, HALF_EVEN decimal rules, policy snapshot P6, and seed 17 are retained through 2033-01-01; all metadata, files, deletes, keys, schemas/specs, dependencies, and catalog identities pass quarterly restore drills; reruns must match the declared ordered primary-key/value digest and decimal totals exactly, while floating diagnostic columns tolerate 1e-12; no mutable name or latest lookup participates; and approved erasure can supersede the horizon with an auditable non-reproducibility record.”

## Learning Objectives

After completing this module, you should be able to:

1. distinguish snapshot, version, instant, timestamp selector, tag, branch, savepoint, and restore;
2. separate event, valid, ingestion, processing, system, and commit time;
3. select historical table state by exact immutable identity and document timestamp resolution;
4. construct a consistent multi-table version vector or publication release;
5. enumerate the complete reproducibility closure beyond table data;
6. control schema/spec/delete semantics, nondeterminism, ordering, numerics, UDFs, and external dependencies;
7. define logical, ordered, tolerance-based, or bitwise equality and validate it appropriately;
8. design retention across metadata, files, deletes, keys, catalogs, code, policies, and streams;
9. operate read-only time travel, rollback/restore, cleanup, privacy, and legal holds safely; and
10. produce a durable reproducibility capsule and drill it before the promised horizon expires.

## Core Exposition

### Select immutable identity before timestamp convenience

Exact version/snapshot/instant is the strongest table-state selector. Pair it with stable table identity. Version 42 in a dropped and recreated table is not version 42 of the original table; a reused catalog name or path can hide that distinction.

Timestamp-as-of commonly chooses the latest completed state at or before a supplied time. Retrieve the exact rule. Record input text, parsed instant, timezone, precision, and resolved version. Then use the resolved version in the durable capsule.

Commit timestamps are metadata, not universal consensus clocks. Two commits can share coarse timestamps. Client clocks can skew. Formats may use log-file modification times or timeline instants differently. Copying table files can change modification times and break timestamp-based resolution even when version-based travel remains sound.

Named references improve usability but differ. A tag commonly points to one historical snapshot; a branch head moves when new commits arrive. Names can be deleted/recreated or collide with numeric identifiers. Record the resolved immutable target and reference type, and configure retention independently.

### Reconstruct the complete historical table state

A snapshot is not merely a data-file list. It binds or resolves schema, partition specifications, sort orders, table properties, protocol features, data files, delete artifacts, and their sequence/applicability rules. A conforming reader reconstructs the logical visible relation under that state.

Historical schema selection is API- and format-specific. Some snapshot-ID or timestamp reads use the snapshot's schema, while branch reads may project through the table's current schema. Retrieve behavior rather than assuming “old rows imply old schema.” Persist the actual output schema and field identities.

Compaction may replace files without changing logical rows. Time travel to a pre-compaction snapshot needs old files until that snapshot expires. Row deletes may live separately from data files. Reading base files directly can resurrect deleted rows or ignore updates. Transaction metadata is the authority.

Protocol features matter historically. A current engine may read all retained states; an older recovery engine may not read states after a feature upgrade. Archive compatible runtime artifacts or maintain an upgrade matrix. The existence of bytes is not proof of decodability.

### Pin one state for the whole read

Resolve the table state once at job start and distribute that immutable selection to every task. Do not ask each task for `latest`; concurrent commits can produce a fractured result. Pagination, retries, speculative tasks, and query restarts must carry the same snapshot identity.

Snapshot isolation protects one table read when the engine honors the pin. It does not freeze external APIs, UDF lookup services, policy engines, or another table opened later. Treat the complete computation boundary separately.

Record selected state in query/run metadata before expensive execution. If planning fails, the run still explains which state it attempted. On retry, choose deliberately between retrying the same state for reproducibility and selecting a new state for freshness; do not switch silently.

### Distinguish time axes

Event time belongs to the domain event. Ingestion time records arrival. Processing time records computation. Commit/system time records when the table accepted a change. Valid time states when a fact applies in the modeled world. These clocks can disagree.

A time-travel query answers “what table state did this storage system expose at version/time X?” It does not necessarily answer “what facts were valid on X?” A correction committed today may say a contract was valid last month. A bitemporal model records valid interval and system interval so both questions can be expressed.

Watermarks describe confidence/progress for event-time arrival; they are not table-version selectors. Late events committed after a historical close will not appear in the old snapshot even if their event time precedes the close. The business must decide whether a report is as-known-at-close, restated-with-late-data, or valid-time reconstruction.

Document the policy in output metadata. An unlabeled “August revenue” is ambiguous if late corrections can restate it.

### Build consistent cuts across inputs

Suppose a job reads orders at version $v_o$ and rates at $v_r$. Each read is internally consistent, but the pair may be semantically invalid if the rate release expected a later correction or if orders refer to currencies absent from that version.

Use one of four mechanisms:

1. a storage/catalog transaction spanning inputs, where genuinely supported;
2. an upstream publication barrier that records every constituent version after validation;
3. an orchestrator that resolves all versions under an agreed cutoff and publishes a version vector before consumers run;
4. immutable output releases that materialize the joined product and record its source lineage.

The version vector

$$
V_R=((T_1,v_1),\ldots,(T_n,v_n))
$$

is the minimum identity. Add cutoff/watermark and validation evidence so the vector has domain meaning. A vector observed sequentially is reproducible but may still be an inconsistent business cut; reproducibility and semantic validity are distinct.

Retries reuse the same release ID unless the run is explicitly superseded. If one input version expires, the release is no longer reproducible even if other inputs remain.

### Close over code, configuration, and external state

SQL text alone is insufficient. Views can change beneath the same name. UDF packages, dependency resolution, optimizer behavior, default timezone, collation, decimal overflow, parser modes, and environment variables can change results.

Bind source and built artifact. A source commit does not prove which compiler flags or dependency graph produced the runtime. Prefer content-addressed container/package digests, lockfiles, build attestations, and archived UDF binaries. Record connector and table-format library versions.

Version views and semantic models or expand them into captured definitions. Version lookup tables and model artifacts. For mutable APIs, capture signed responses where lawful or use a provider version with a durable retrieval contract. Current API results cannot reproduce historical computation.

Secrets usually should not be archived as plaintext. Record secret/key identity and preserve controlled access or escrow if it affects decryption or computation. Rotation must not destroy promised read capability without an authorized horizon change.

### Control nondeterminism and ordering

Functions such as current time, random, UUID, unversioned network calls, and approximate algorithms can vary. Replace current time with an explicit parameter. Seed pseudorandom generators and record algorithm/runtime. Capture external responses. State approximation confidence and implementation.

Relational results are unordered without an explicit order. `LIMIT 100` without total order can return different rows; ordering by a nonunique key leaves ties unconstrained. For ordered reproducibility, define a stable total order including a tie-breaker.

Parallel floating-point reductions can differ because addition is not associative under finite precision. Require decimal/exact arithmetic for money, or declare tolerance and aggregation strategy. Record NaN, signed zero, overflow, rounding, and locale/collation behavior.

Hashes require canonicalization: field order, null marker, encoding, Unicode normalization, numeric representation, row order, duplicate handling, and digest algorithm. A hash without its canonicalization contract is not portable evidence.

### Define the equality claim

Several claims are useful:

- **membership equality:** the same stable keys and duplicate multiplicities;
- **logical value equality:** the same typed values after declared projection;
- **aggregate equality:** selected controls match, useful but not sufficient for row equality;
- **ordered equality:** logical equality plus a declared total row order;
- **tolerance equality:** numeric differences stay within absolute/relative bounds;
- **bitwise equality:** serialized output bytes and metadata are identical.

Let canonical projection/order be $K$ and digest $H$. A strong logical check is

$$
H(canon_K(Y_{original}))=H(canon_K(Y_{rerun})),
$$

plus schema equality, row count, key multiplicities, and independent aggregates. Collision resistance supports evidence but does not repair a faulty canonicalization or omitted fields.

Bitwise identity demands pinned serialization libraries, compression, metadata timestamps, file partitioning, task ordering, and often hardware. Do not demand it when logical equivalence is the actual requirement; do not claim it from logical checks.

### Make retention a reachability contract

For every promised state, retain the metadata/log chain or checkpoint needed to reconstruct it and all referenced data/delete files. Keep historical schemas/specs/protocol definitions, catalog identity mapping, and decryption keys. Preserve code/runtime/dependencies and every other input version.

Retention must exceed the longest query, retry, streaming lag, audit horizon, rollback window, and hold. Cleanup systems need awareness of active readers and in-progress writers. A zero- or very-short retention can delete files still required by a concurrent job.

Tags, branches, or savepoints can protect selected states, but their reference and snapshot/file retention properties must be configured and tested. A tag scheduled to expire next week does not satisfy a seven-year audit promise.

Maintain a retention ledger mapping release/capsule to required state identities and retain-until dates. Before vacuum/expiration/cleaning/key destruction, calculate impacted capsules and require policy authorization. After cleanup, verify expected historical selectors fail and current states remain healthy.

Storage cost is

$$
Cost\approx\sum_{f\in ReachableHistory}size(f)\times duration(f)+metadata+keys+runtime\ artifacts.
$$

Deduplication through shared immutable files can reduce cost, but one retained snapshot can keep large old files reachable.

### Separate time travel, changes, and restore

A snapshot query at $v_2$ returns visible state $S_{v_2}$. An incremental query between $v_1$ and $v_2$ returns format-defined changes, which may be latest states, added files, or CDC before/after rows. It is not generally $S_{v_2}-S_{v_1}$ under ordinary set subtraction.

Restore changes current operational state. Some systems move a reference; others create a new commit whose active files resemble an old version. The latter appears as new add/remove actions to downstream streams, potentially replaying previously processed rows.

Before restore, identify affected current commits, streams, caches, materializations, foreign keys, privacy deletions, and newer legitimate data. Prefer repairing a bounded predicate when full rollback would discard unrelated writes. Preserve the incident state as evidence if lawful.

After restore, record the new current identity and its ancestry/operation. Never relabel it as the original old version; history has advanced.

### Handle privacy, security, and policy evolution

Historical snapshots can preserve data a current delete hides. Access control must cover time-travel APIs, metadata tables, direct object paths, branches/tags, backups, and keys. “Cannot query current column” is not erasure.

Decide whether historical reads apply current authorization/purpose policy, historical policy, or a controlled audit policy. Current policy is usually safer for user access; regulated audit may require preserved policy evidence. Record the choice without resurrecting revoked access.

Erasure can intentionally make an old snapshot incomplete or inaccessible. Rewrite or expire reachable histories and backups as required, destroy keys when authorized, and update capsules to state that exact reproduction is no longer possible. Preserve non-sensitive proofs or aggregates only when permitted.

Legal hold can override ordinary expiration but needs scoped access and review. A hold on one snapshot may retain shared files for other snapshots; account for actual reachability rather than labels.

### Verify before depending on the horizon

Creation-time evidence is not enough. Schedule restore-and-rerun drills from isolated infrastructure. Resolve exact versions, verify metadata/file/delete/key closure, execute with archived runtime, and compare under the declared equality contract.

Test old schemas, partition specs, deletes, compaction boundaries, timestamp collisions, branch movement, catalog rename/recreation, copied table locations, expired nonprotected snapshots, revoked credentials, dependency registry outage, and disaster-region restore.

Monitor oldest reconstructible state, protected releases, bytes retained per release, missing referenced objects, key expiry, tag/reference expiry, log/checkpoint continuity, cleanup candidates, active-reader age, stream lag, and drill success/latency.

Alert before a promise breaks, not after an audit request arrives. Ownership belongs jointly to the data product, platform/catalog, security/key management, runtime registry, and governance retention system.

## Definitions and Notation

Let $T$ be a stable table identity and $V_T$ its immutable versions. $S(T,v)$ is the logical table state at $v$. Let $time_T(v)$ be recorded commit time and $resolve_T(t)$ the format-specific timestamp resolver.

An example resolver is

$$
resolve_T(t)=\arg\max_{v\in V_T}\{order_T(v):time_T(v)\le t\},
$$

but production formats may impose different rules. If timestamps tie, version order must disambiguate. Persist $resolve_T(t)$, not just $t$.

For input set $I$, version vector $V_R$ maps each identity to one version. Let $D$ be code/runtime dependency identities, $G$ deterministic configuration, $E$ external captured state, and $A$ access/policy context. Then

$$
Y_R=Eval(Q,V_R,D,G,E,A).
$$

A capsule is $C_R=(Q,V_R,D,G,E,A,Contract,RetainUntil,Evidence)$.

Define closure $Closure(C_R)$ as every artifact transitively required to evaluate the capsule. Reproducibility at time $t$ requires

$$
Available_t(Closure(C_R))\land Compatible_t(Closure(C_R))\land Authorized_t(C_R).
$$

Logical reproducibility under canonicalization $canon$ is $canon(Y_R)=canon(Y'_R)$. Tolerance equality for numeric vector $x$ may require

$$
|x_i-x'_i|\le \epsilon_{abs}+\epsilon_{rel}|x_i|
$$

for every declared field/index. State behavior for NaN and infinity separately.

The reproducibility horizon is the maximum interval over which availability, compatibility, and lawful authorization are guaranteed—not simply the configured data-file retention.

## Mechanisms, Invariants, or Proof Structure

Proof sketch for snapshot-read stability:

1. A reader resolves stable table $T$ to immutable version $v$ before planning.
2. Version $v$ determines one committed metadata/log state and its schema/spec/protocol semantics.
3. That state determines active data and delete artifacts and their applicability.
4. Tasks receive $v$ or a plan derived only from $v$, never a later `latest` resolution.
5. Concurrent commits create versions $v'>v$ but do not mutate the committed definition of $v$.
6. Therefore those commits cannot change the reader's logical input state.
7. If all referenced artifacts and keys remain available and the conforming reader semantics remain fixed, a later read of $(T,v)$ reconstructs the same logical state.

This proof does not establish full computation reproducibility: query code, other inputs, policies, runtime semantics, or nondeterminism may differ. It also fails after required metadata/files/deletes/keys are removed.

For multiple tables, individual stability proves each $S(T_i,v_i)$ is repeatable, not that the vector is a valid business cut. A release barrier or transactional coordination supplies that separate premise.

The executable models exact version selection, timestamp resolution with version-order tie-breaking, mutable branch movement, a two-table release vector, and retention failure. Integer timestamps avoid timezone parsing and the model is not an implementation of Iceberg, Delta Lake, Hudi, Spark, catalogs, or storage cleanup.

<!-- bijux-verify: {"id":"pinned-version-reproducibility","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"timestamp_resolved=103\npinned_rows=(('a', 10), ('b', 20))\nlatest_rows=(('a', 10), ('b', 25), ('c', 30))\nbranch_before=102\nbranch_after=103\npinned_unchanged=True\nrelease_vector=(('orders', 102), ('rates', 44))\nrelease_total=30\nclosure_available=True\nafter_expiration=False\n","stderr":""}} -->
```python
versions = {
    101: (1000, (("a", 10),)),
    102: (1010, (("a", 10), ("b", 20))),
    103: (1010, (("a", 10), ("b", 25), ("c", 30))),
}


def resolve_as_of(timestamp):
    candidates = [
        version for version, (commit_time, _) in versions.items()
        if commit_time <= timestamp
    ]
    return max(candidates)


resolved = resolve_as_of(1010)
pinned_version = 102
pinned_rows = versions[pinned_version][1]
branch = {"close": 102}
branch_before = branch["close"]
branch["close"] = 103
branch_after = branch["close"]

rates = {44: {"USD": 1, "EUR": 2}}
release_vector = (("orders", pinned_version), ("rates", 44))
release_total = sum(amount * rates[44]["USD"] for _, amount in pinned_rows)
retained = {("orders", 102), ("rates", 44), ("runtime", 3)}
required = {("orders", 102), ("rates", 44), ("runtime", 3)}

print(f"timestamp_resolved={resolved}")
print(f"pinned_rows={pinned_rows}")
print(f"latest_rows={versions[max(versions)][1]}")
print(f"branch_before={branch_before}")
print(f"branch_after={branch_after}")
print(f"pinned_unchanged={pinned_rows == versions[102][1]}")
print(f"release_vector={release_vector}")
print(f"release_total={release_total}")
print(f"closure_available={required <= retained}")
retained = retained - {("orders", 102)}
print(f"after_expiration={required <= retained}")
```

Versions 102 and 103 deliberately share timestamp 1010; the teaching resolver uses version order and selects 103. The durable capsule pins 102, so branch movement and timestamp ambiguity do not alter it. Removing one closure element makes the reproducibility promise false even though the capsule still exists.

## Alternatives and Trade-Offs

**Exact version versus timestamp.** Versions are unambiguous within stable table identity. Timestamps are human-friendly for discovery but depend on resolution, precision, timezone, and preserved timestamp metadata. Resolve and record both when users start from time.

**Tag versus branch.** A tag can name one retained state; a branch supports continuing lineage. Both improve discoverability, but branches move and both need retention configuration. Always record the immutable target.

**Retain every version versus selected releases.** Full history maximizes investigation flexibility and costs storage/metadata/privacy exposure. Selected audited releases bound cost but cannot answer arbitrary intermediate questions.

**Logical versus bitwise reproducibility.** Logical equality survives benign file layout and engine changes. Bitwise equality helps cryptographic distribution and exact artifact provenance but greatly constrains execution and serialization.

**Materialized release versus virtual capsule.** Materialization simplifies future reads and isolates upstream cleanup, at duplicate storage cost. A virtual capsule reuses immutable inputs but depends on their full transitive retention and compatible runtime.

**Current versus historical schema projection.** Historical schema recreates original meaning/shape. Current projection helps modern consumers but may add defaults, hide fields, or change names. Declare and persist the chosen output schema.

**Global transaction versus release manifest.** A genuine multi-table transaction supplies a strong cut but is not universally available. A release manifest is portable and auditable, though orchestration must establish domain consistency.

**Deterministic exact arithmetic versus tolerance.** Exact decimals and canonical algorithms support strict equality but can cost performance. Floating/tolerant computation is appropriate when numerically justified and the tolerance is explicit.

**Restore versus compensating repair.** Full restore rapidly returns an old relation but can discard legitimate newer data and replay downstream changes. A bounded repair preserves unrelated commits but requires careful diagnosis and reconciliation.

**Long retention versus privacy minimization.** Longer history aids audit and rollback but increases cost and exposure. Purpose-limited selected retention, access controls, erasure workflows, and explicit horizons balance obligations.

**Archive runtime versus forward-compatible reader.** Archiving the original runtime reduces semantic drift but can preserve vulnerabilities and obsolete infrastructure. A maintained reader with conformance fixtures is safer operationally but may not guarantee bitwise behavior.

**Captured API response versus provider version.** Capturing makes the exact input durable where lawful. Provider versioning avoids copying sensitive/licensed data but makes reproducibility depend on external availability and contract.

## Failure Modes and Misconceptions

1. **“Time travel means reproducible.”** It pins one table state, not all computation inputs and semantics.
2. **“The timestamp is the version.”** It is usually resolved to a version under format-specific rules.
3. **“Commit time equals event time.”** Late and corrected events make them diverge.
4. **“System time answers valid-time questions.”** Business validity must be modeled explicitly.
5. **“A branch name is immutable.”** Branch heads move; record the resolved state.
6. **“A tag retains data forever.”** Reference and snapshot/file retention require explicit policy.
7. **“Table name identifies history.”** Names and paths can be reused after drop/recreation.
8. **“Every task may read latest.”** Concurrent commits can fracture the result.
9. **“Two latest snapshots form one cut.”** They may never have been an approved joint release.
10. **“Same SQL means same computation.”** Views, UDFs, defaults, dependencies, and session settings drift.
11. **“A source commit identifies runtime.”** Builds and dependency resolution can differ.
12. **“ORDER BY one column is deterministic.”** Duplicate sort keys need a stable tie-breaker.
13. **“LIMIT is repeatable.”** Without a total order, selected rows are unspecified.
14. **“A seed controls all randomness.”** Algorithm, runtime, concurrency, and hardware can still matter.
15. **“Floating totals must match bits.”** Parallel reduction order can change low bits; define numeric policy.
16. **“Equal count proves equal result.”** Substitutions and duplicate changes preserve counts.
17. **“A checksum is self-describing.”** Canonicalization, fields, order, encoding, and algorithm must be recorded.
18. **“Data files are enough.”** Metadata, schemas, specs, deletes, protocols, and keys construct visibility.
19. **“Logs are enough.”** Referenced files and keys must also survive.
20. **“Backup equals queryable history.”** Recovery requires catalog, metadata, keys, software, and drills.
21. **“Vacuum only saves space.”** It can close time-travel and active-reader horizons.
22. **“Restore is a historical SELECT.”** It mutates current state and can replay downstream changes.
23. **“CDC equals endpoint snapshot difference.”** Change-feed semantics and update/delete representation differ.
24. **“Current authorization should be bypassed for reproducibility.”** Reproduction remains subject to lawful access.
25. **“Drop from current schema erases history.”** Old states and files may retain the field.
26. **“Forever is safe.”** Cost, privacy, legal, key, and software lifecycles require explicit review.

## Worked Examples

### Example 1

An analyst asks for `TIMESTAMP AS OF '2026-08-31 23:59:59'`. The platform parses UTC, resolves orders table UUID O to version 812, and records both. The durable notebook uses version 812; the timestamp remains explanatory metadata rather than the only selector.

### Example 2

Two commits share millisecond timestamp 1010. Engine rules select the later table version. Another connector truncates to seconds and could resolve differently. The test exposes the difference, and the release capsule stores the chosen version plus engine/connector identity.

### Example 3

A branch named `monthly-close` points to snapshot 700 during validation and later advances to 708. A report storing only the branch name drifts. The corrected report stores table UUID and snapshot 700; branch name remains a human label with its observed target.

### Example 4

A model-training job reads features, labels, and consent policy. Each table is individually pinned, but the label version predates a correction assumed by the feature release. A publication manifest validates and binds the three versions; model lineage records the manifest rather than three opportunistic latest reads.

### Example 5

A financial query uses decimal for booked amounts and floating point for a diagnostic score. The contract requires exact ordered key/amount equality and $10^{-12}$ absolute-plus-relative tolerance for scores. It records rounding, overflow, NaN, and total-order rules instead of making one vague “same output” claim.

### Example 6

Compaction replaces ten files with one at version 91 without logical change. Version 90 remains queryable because its metadata and old files are retained. A direct directory scan sees both generations and double counts; the table reader selects only files active in the pinned version.

### Example 7

A position delete hides a customer row in snapshot 120. An archive saved data files but omitted the delete artifact. Its recovered count is one too high. The retention ledger is corrected to traverse all data/delete metadata and the drill fails closed when any referenced object is absent.

### Example 8

A table restore makes state similar to version 50 current again through a new version 74. A streaming consumer sees add actions for files it processed earlier. Operators coordinate checkpoints/deduplication and label version 74 as a restore commit; they do not claim the timeline returned to 50.

### Example 9

A privacy erasure requires removing a subject from historical snapshots that supported a model release. Governance rewrites/expires affected history and updates the capsule: exact retraining is no longer lawful/possible after the erasure date. Approved aggregate validation evidence remains, but inaccessible raw identity is not silently retained.

### Example 10

A disaster drill restores object data but the catalog points to a recreated table UUID and the original key version is disabled. The drill correctly fails. The recovery plan adds catalog metadata backup, UUID verification, key escrow/rotation policy, archived runtime, and quarterly end-to-end query comparison.

## Cross-Program Connections

- **Database Systems:** MVCC, system-versioned tables, transaction time, valid time, snapshot isolation, recovery, and temporal SQL ground historical state selection.
- **Distributed Systems:** consistent cuts, logical clocks, atomic publication, immutable logs, version vectors, stale reads, and coordinated snapshots govern multi-input releases.
- **Programming Languages:** referential transparency, explicit effects, deterministic evaluation, floating semantics, serialization, and dependency identity explain rerun stability.
- **Software Engineering:** hermetic builds, lockfiles, content addressing, provenance, release manifests, semantic versioning, and contract tests close the computation surface.
- **Systems Engineering:** configuration baselines, traceability, evidence, lifecycle guarantees, hazard review, interface control, and verification drills turn reproducibility into an operated capability.
- **Reliability Engineering:** backup/restore, recovery objectives, canaries, incident forensics, long-running readers, cleanup safety, and game days test the claimed horizon.
- **Security Engineering:** key lifecycle, catalog/object authorization, audit trails, artifact integrity, supply-chain provenance, and break-glass access protect historical state.
- **Privacy Engineering:** minimization, consent/purpose change, erasure, legal hold, inference, and retention can intentionally bound reproducibility.
- **Statistics and ML:** dataset/model/feature lineage, seed control, numerical tolerance, late labels, leakage, and train-serving consistency depend on exact release identity.
- **API and Service Engineering:** idempotency keys, immutable resource versions, ETags, pagination snapshots, deprecation, and replay contracts parallel table-version reads.
- **Cloud Engineering:** object versioning, regional recovery, lifecycle rules, catalogs, key management, artifact registries, and request/storage cost determine availability.
- **Governance and Audit:** evidence chains, record disposition, legal holds, approvals, policy versions, and reproducibility exceptions define lawful historical access.

## References

1. Apache Iceberg. [Table specification](https://iceberg.apache.org/spec/). Accessed 2026-09-03. Primary specification for snapshots, snapshot logs and references, schemas/specs, manifests, files, sequence semantics, retention, and commit behavior.
2. Apache Iceberg. [Spark queries](https://iceberg.apache.org/docs/latest/spark-queries/). Accessed 2026-09-03. Primary engine documentation for timestamp, snapshot-ID, branch, tag, system-time, and historical-schema query behavior.
3. Apache Iceberg. [Branching and tagging](https://iceberg.apache.org/docs/latest/branching/). Accessed 2026-09-03. Primary documentation for mutable branches, snapshot tags, schema selection, audit branches, and reference retention.
4. Apache Iceberg. [Maintenance](https://iceberg.apache.org/docs/latest/maintenance/). Accessed 2026-09-03. Primary documentation for snapshot expiration, time-travel loss, referenced-file deletion, old metadata, and orphan safety.
5. Apache Iceberg. [Reliability](https://iceberg.apache.org/docs/latest/reliability/). Accessed 2026-09-03. Primary documentation for atomic metadata operations, reader isolation, optimistic concurrency, and retry guarantees.
6. Delta Lake. [Table utility commands](https://docs.delta.io/delta-utility/). Accessed 2026-09-03. Primary documentation for history, vacuum retention, historical availability, restore semantics, and downstream replay consequences.
7. Delta Lake. [Delta Transaction Log Protocol](https://github.com/delta-io/delta/blob/master/PROTOCOL.md). Accessed 2026-09-03. Primary protocol specification for versions, actions, checkpoints, snapshots, tombstones, time travel, protocol features, and transaction identity.
8. Delta Lake. [Table properties reference](https://docs.delta.io/table-properties/). Accessed 2026-09-03. Primary documentation for log, deleted-file, transaction, reader, writer, and checkpoint retention/compatibility properties.
9. Delta Lake. [Quick start](https://docs.delta.io/quick-start/). Accessed 2026-09-03. Primary documentation demonstrating version-based historical queries and transactional table use.
10. Delta Kernel. [Time travel and snapshot management](https://docs.delta.io/kernel/rust/reading/time_travel.html). Accessed 2026-09-03. Primary kernel documentation for building exact-version snapshots and explicitly refreshing held snapshot state.
11. Apache Hudi. [SQL queries](https://hudi.apache.org/docs/sql_queries/). Accessed 2026-09-03. Primary documentation for snapshot, time-travel, incremental, and change-data-capture query forms and boundaries.
12. Apache Hudi. [Timeline](https://hudi.apache.org/docs/timeline/). Accessed 2026-09-03. Primary documentation for instants, action states, atomic timeline transitions, savepoints, restore, compaction, and clustering.
13. Apache Hudi. [Table and query types](https://hudi.apache.org/docs/table_types/). Accessed 2026-09-03. Primary documentation distinguishing snapshot, read-optimized, incremental, CDC, and as-of-instant configurations.

## Exercises

### Exercise 1

Design a reproducibility capsule for a monthly financial close joining orders, refunds, exchange rates, and account hierarchy. Include selector resolution, consistent cut, schema/spec/delete state, code/runtime, numerical rules, access policy, output equality, retention, and evidence.

### Exercise 2

A user supplies local timestamp `2026-11-01 01:30` and a branch called `close`. Explain all ambiguity and mutability hazards. Define a resolution workflow that produces one durable selector and remains auditable after branch movement, timezone-database updates, and table copying.

### Exercise 3

Design a seven-year retention and quarterly drill plan for 200 selected releases while ordinary snapshots expire after 30 days. Cover references, metadata/logs, data/deletes, catalogs, keys, runtimes, dependencies, legal holds, erasure, cost, failures, and ownership.

### Exercise 4

An incident team wants to restore a table to version 900 while two streams, three materialized views, a privacy deletion at version 905, and legitimate writes through version 912 exist. Decide between historical read, full restore, and bounded repair; specify safety and validation steps.

### Exercise 5

A model rerun has the same row count and nearly identical accuracy but a different prediction file. Build a diagnosis covering table versions, multi-input cut, schemas, policies, code/build, dependencies, UDFs, randomness, floating reductions, row order, canonical hashes, and external features.

## Answers to the Exercises

### Answer 1

Assign a release ID and bind stable table UUIDs to exact orders/refunds/rates/hierarchy versions through a close publication barrier, not sequential latest reads. Record resolved original timestamps, schema/spec/delete/protocol identities, query and code digests, built runtime/container and dependencies, UDF/view definitions, UTC/timezone-data version, decimal scale/rounding/overflow, parameters, policy/principal/key identities, and late/restatement policy. Define output schema, primary-key multiplicity, total ordering, canonical digest, exact financial totals, and any tolerated diagnostics. Retain the complete metadata/file/delete/key/runtime closure through the legal horizon, attach holds/erasure rules, and run isolated restore/recompute comparisons. Evidence includes source vector, barrier, counts, key diffs, totals, digests, approvals, and drill results.

### Answer 2

The wall time occurs in a daylight-saving fold in some zones and has no unique instant without zone/offset and fold policy. Parser precision and timezone database can change interpretation. The branch is mutable, can be deleted/recreated, and its name may conflict with identifier parsing. Require source zone/offset or reject/quarantine ambiguity; record input text, parsed UTC instant, zone database, parser/engine, and timestamp-resolution rule. Resolve stable table UUID plus branch target and timestamp to the chosen immutable snapshot/version, then persist that identity and historical schema behavior. After branch movement, use the immutable ID. When copying, preserve authoritative transaction metadata/timestamps or continue using version identity; verify copied table identity rather than assuming path equivalence.

### Answer 3

Create durable tags/savepoints or archive packages for only the 200 releases and maintain a retention ledger from each release to its full closure. Preserve reconstructible metadata/log/checkpoints, manifests, active data/delete files, schemas/specs/protocols, catalog UUID mapping, keys, release manifests, query/code/runtime/dependencies, policy evidence, and checksums through seven years. Ordinary unprotected states may expire at 30 days. Quarterly, restore a sample and every high-risk release in isolated infrastructure, validate identity and object closure, decrypt/read using archived or maintained compatible runtime, rerun controls, and compare declared digests. Forecast shared-file reachability and storage/key/artifact cost. Holds extend scoped retention; lawful erasure can rewrite/expire history and records an authorized break in reproducibility. Data product, platform, security/key management, artifact registry, and governance each own explicit checks and alerts.

### Answer 4

First perform a read-only query of version 900 for diagnosis; it has no current-state blast radius. Full restore would discard or mask legitimate 901–912 work, can reintroduce data erased at 905, and can replay file additions to both streams and materializations. Unless the entire later interval is proven invalid and privacy authorizes it, prefer a bounded repair: identify erroneous logical keys/predicate, derive corrected values from pinned versions while excluding erased subjects, reconcile concurrent commits, and publish a new atomic version. Fence affected writers, coordinate stream checkpoints/idempotency and view refresh, preserve incident evidence, validate key multiplicities/deletes/totals/policies, canary readers, and retain pre-repair state for rollback. If full restore is mandated, treat it as a new commit with explicit downstream replay and privacy controls.

### Answer 5

Compare stable table identities and exact version vectors for labels, features, lookups, consent/policy, and models; verify the vector was one accepted release. Compare historical output schemas, field IDs/defaults, partition/delete semantics, query/view/UDF definitions, source commit, build and dependency digests, runtime/connector versions, parameters, timezone/locale/numeric modes, external responses, and authorization filtering. Confirm seeds plus algorithms, thread/GPU determinism, approximate operations, and floating reduction order. Row count and accuracy can hide substitutions. Canonicalize typed rows with a stable total key order and duplicate/null/NaN/Unicode/numeric rules; compare schema, key multiplicity, per-field diffs, exact and tolerance columns, aggregates, and cryptographic digests. The first divergent dependency or intermediate materialization narrows the cause; if all logical rows match but bytes differ, inspect ordering, serialization, compression, and metadata before escalating the equality claim.
