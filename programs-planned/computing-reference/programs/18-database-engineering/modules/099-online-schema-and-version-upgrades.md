---
module_id: DBE-099
program: Database Engineering
level: 2
module_number: 99
title: Online Schema and Version Upgrades
status: complete
last_verified: 2026-09-05
---

# Online Schema and Version Upgrades

## One-Page Review

### Governing question

How can a database schema, physical representation, index, partition layout, or engine version change while old and new application versions remain correct, data continues changing, rollback stays meaningful, and capacity/failure risks remain bounded?

### Essential definitions

- An **online change** preserves a declared service and correctness contract during the change; it does not mean zero locks, zero latency impact, or zero unavailable operations.
- **Compatibility** is directional: reader/writer version A may or may not operate safely against schema/storage version B.
- **Expand–migrate–contract** first adds a representation old code tolerates, moves data/traffic, then removes the old representation after evidence.
- A **backfill** transforms existing records into a new representation while foreground writes continue.
- **dual write** updates two representations from one intent; without atomicity or replay it can diverge.
- A **shadow table/index** is a candidate representation built beside the authoritative one.
- A **change capture frontier** identifies the source position through which a candidate has applied mutations.
- A **cutover** changes read/write authority; a **fence** prevents stale owners or code from continuing to mutate old authority.
- **rollback** restores a previously supported behavior/state without discarding post-cutover accepted work.
- An **engine upgrade** changes software and may change wire protocol, disk/WAL format, planner behavior, catalog, replication, defaults, and operational tools.

### Central model, mechanism, or theorem

Treat the database as a versioned protocol among application readers/writers, schema/catalog, stored rows, indexes, replicas, backup/restore, and operational tooling. Build a compatibility matrix before change.

For a representation migration, take source snapshot/frontier $s_0$, copy rows idempotently, capture all changes after $s_0$, apply them by stable identity and source version, validate candidate equivalence at caught-up frontier $s_c$, then cut over with a routing epoch/fence. Contract only after old writers/readers, replicas, backups, and rollback dependencies are gone.

### Critical invariants

- every supported reader interprets every representation it may observe with the intended domain meaning;
- every supported writer preserves invariants when old/new schema versions coexist;
- backfill never overwrites a newer foreground value and can resume/retry by stable identity;
- source and candidate reconcile by keys, values, constraints, and representative queries at a declared frontier;
- cutover yields one authoritative writer path and stale writers are fenced;
- rollback can incorporate or safely reject post-cutover work under an explicit plan;
- migration load, WAL/log retention, temporary storage, locks, and replication lag remain within reserved capacity;
- backup, restore, failover, and disaster recovery are tested for the mixed and final versions.

### Common failures

- deploying a breaking rename or drop before all readers stop using the old field;
- assuming an `ALTER` is metadata-only because the SQL text is short;
- building an index online but ignoring CPU, I/O, WAL, lock-at-finish, and replica impact;
- running an unconditioned backfill that restores stale values over foreground updates;
- dual-writing in application code without stable mutation identity or repair;
- validating only row counts while types, nulls, defaults, ordering, and queries differ;
- calling rollback “deploy old binary” after new writes use an unreadable format;
- cutting over with replicas or caches on incompatible generations;
- retaining change logs too briefly for copy/rebuild/retry;
- upgrading all nodes before testing mixed-version replication, failover, and recovery.

### Compact example

Rename `name` to `display_name`: deploy readers that accept both with explicit precedence; add the new nullable column/field; deploy new writers that write the new representation under one authority; backfill rows only when source version still matches; compare semantics; enforce new constraints; switch reads; wait until no old writer/reader or rollback depends on `name`; then drop it in a separately governed change. One DDL rename cannot provide this application compatibility.

### Connections

The previous module, [Database Observability and Capacity](098-database-observability-and-capacity.md), supplies the evidence and headroom required to govern change. The roadmap's final module, [Conducting a Production Database Reliability and Performance Review](../ROADMAP.md), integrates upgrade evidence into a complete review. Prerequisites include [Schemas, Keys, and Constraints](003-schemas-keys-and-constraints.md), [Data Modification and Upsert](019-data-modification-and-upsert.md), [Physical and Logical Backup](079-physical-and-logical-backup.md), and [Logical Replication](082-logical-replication.md).

## Governing Question

A system must add a non-null attribute, change key format, rebuild a large index, repartition a table, and upgrade the database engine without a maintenance outage. Old application instances can live for hours; replicas lag; backfills take days; traffic and schema change concurrently; rollback is required. Which sequence preserves meaning at every intermediate state?

The answer is not one universal migration recipe. Exact DDL and upgrade mechanisms are product- and version-specific. The durable method is to model compatibility, authority, capture frontiers, capacity, failure boundaries, validation, cutover, and contraction explicitly.

## Why This Matters

Schema and version changes are among the most dangerous database operations because they combine semantics with large physical work. A type change can rewrite a table and block access. An index build can consume storage and replication bandwidth. A new default can change old-reader behavior. A rolling engine upgrade can leave a topology that cannot fail backward.

The hardest failures occur after apparent success. A lagged replica replays incompatible WAL. An old binary writes the retired field. A backfill races a user correction. A rollback reads new enum values it does not know. A restored backup lacks the migration frontier. The original table is dropped before the candidate survives a failover.

Online change means continuous proof, not optimistic execution. Each state must be coherent, observable, capacity-safe, and recoverable.

## Prerequisites and Retrieval

Retrieve schema, constraints, DDL locks, MVCC, WAL/recovery, indexes, transactions, logical replication, sharding, query plans, SLOs, canaries, idempotency, and backup/restore. Be able to distinguish logical compatibility from physical availability.

Retrieve directional compatibility. **Backward-compatible readers** can consume older stored representations; **forward-compatible readers** tolerate newer ones in the declared subset. Writers have separate compatibility. Terms vary across ecosystems, so always show the concrete matrix rather than relying on labels.

For the exact database, read current official documentation for DDL lock modes, table rewrites, concurrent/online index builds, constraint validation, replication compatibility, upgrade paths, file/WAL formats, extension compatibility, backup/restore, and rollback restrictions. Record engine, extension, driver, operating system, and tool versions.

## Learning Objectives

After completing this module, you should be able to:

1. construct a reader/writer/schema/storage compatibility matrix for every intermediate state;
2. design expand–migrate–contract changes with idempotent, version-conditioned backfill;
3. distinguish metadata, scan, rewrite, index-build, validation, and lock phases from official evidence;
4. maintain candidate representations through transactional change or durable capture and reconciliation;
5. execute fenced cutover and rollback without losing post-cutover writes;
6. plan capacity for WAL/log retention, old/new copies, indexes, replicas, and failure;
7. perform rolling engine upgrades with mixed-version, failover, plan, extension, and restore tests;
8. define completion and contraction gates from measured evidence rather than elapsed time.

## Core Exposition

**Inventory the protocol surface.** A database version is consumed by application binaries, ad hoc tools, jobs, CDC consumers, replicas, backup agents, BI clients, ORMs/drivers, extensions, and operators. List each supported version and owner. Hidden writers are more dangerous than hidden readers.

Inventory schema objects, constraints, generated values, triggers, views, functions, permissions, indexes, partitions, replication publications/subscriptions, slots/log retention, backups, and restore tooling. A column rename can break a view, `SELECT *`, positional decoder, audit trigger, or export even if the main service works.

**Build a state machine, not a script.** Name durable states such as old-only, expanded, dual-readable, backfilling, caught-up, candidate-read canary, new-authoritative, rollback-window, and contracted. For each, specify allowed application/schema versions, writer authority, read precedence, invariants, monitors, failure action, and transition gate.

Delivery order is part of correctness. If old code rejects unknown enum values, new writers cannot emit them while old readers remain. If old writers omit a new required field, the database cannot enforce `NOT NULL` until writers and backfill satisfy it.

**Use expand–migrate–contract.** Expansion adds compatible capacity: nullable field, new table/index, new enum representation, view, or versioned API. Migration moves existing and concurrent data. Cutover changes authority. Contraction removes compatibility only when no supported actor or rollback needs it.

Keep each transition independently observable and reversible where possible. A rename implemented as add-copy-switch-drop is slower but makes compatibility explicit. Direct DDL rename may be safe only when every dependent object/client changes atomically, which is rare in distributed deployment.

**Read the actual DDL path.** `ALTER TABLE` can update only catalog metadata, scan rows, validate, rewrite the entire relation, acquire locks, or combine phases depending on engine/version/type/default. Table size alone does not predict lock duration; waiting for existing transactions and final metadata swaps can dominate.

Test DDL on production-shaped schema/data with concurrent reads/writes, long transactions, replicas, and failure. Inspect official lock and rewrite rules. Set timeouts and a bounded retry policy so an online attempt does not wait indefinitely then acquire a disruptive lock at peak.

**Add required fields safely.** Add the field in a representation old code tolerates. Deploy writers with a default derived from known semantics, not a fabricated placeholder. Deploy readers that distinguish absent from default during transition. Backfill. Validate the invariant. Then enforce not-null/check and remove fallback.

Some engines can add a constant default without rewriting existing rows in current versions; others cannot or have type/default restrictions. Record exact behavior. Even a metadata-only default changes logical reads and future writes, so application compatibility still matters.

**Backfill by stable chunks.** Select bounded key ranges, record progress, and use a stable source snapshot/version. Each update includes a predicate proving the target is still missing or the source version matches. Commit small transactions, throttle by user impact and replication/maintenance debt, and make retries idempotent.

Avoid offset pagination over a mutating table. Use stable keyset ranges or snapshots. Record examined, changed, skipped-newer, invalid, failed, retry, lag, WAL, locks, latency, and remaining work. A skipped row needs classification and later reconciliation.

Suppose source row has version $q_s$ when transformed. The backfill update must commit only if current relevant version remains $q_s$, or recompute from current state. Otherwise it can overwrite a foreground write at $q_s+1$. This is optimistic concurrency, not merely batching.

**Define dual-representation authority.** During a rename, when both fields exist, specify which wins if they disagree. Prefer one authoritative logical write that atomically derives both inside the database transaction or emits a durable change. Two independent application calls create partial success.

Dual write is temporary complexity with more failure modes. Stable mutation ID/version, idempotent replay, conflict policy, and reconciliation are mandatory. Observe divergence, not only write errors.

**Capture changes around a shadow copy.** For table/key migration, establish snapshot or source frontier $s_0$. Copy source rows as of that boundary into the candidate. Retain WAL/binlog/change events after $s_0$ long enough for the slowest rebuild plus retries. Apply mutations by stable identity/version, including deletes.

When copy reaches end, capture/apply must catch up to $s_c$. Quiesce or fence briefly if needed to establish one cutover point. If the change stream does not include DDL, transactions, before images, or large objects required for correctness, add another mechanism or stop.

**Validate semantics, not counts.** Compare key sets, canonical values/types, null/missing/default distinctions, constraints, generated fields, ordering/collation, timestamps/precision, checksums, and deletes at a fixed frontier. Compare representative queries and plans/results. Counts can match while rows pair incorrectly.

For huge data, deterministic partitioned hashes and risk-based exact samples can provide scalable evidence, but a hash collision means it is not a formal equality proof. Investigate every mismatch and expand sampling by defect class. Validate security and permissions too.

**Build indexes online with constraints.** Concurrent/online index build often scans while writes continue, catches changes, and takes brief coordination locks. It may leave an invalid candidate after failure. It consumes read/write I/O, CPU, memory, temp space, WAL/log, replica apply, and cache.

Separate index creation from constraint attachment when supported. Validate uniqueness against concurrent writes under the documented mechanism. Before use, confirm index validity/readiness, definition, collation/operator class, row coverage, size, replicas, plans, and recovery. Before removal, prove no required query/constraint depends on it.

**Validate constraints progressively.** A new check or foreign-key constraint may be installed for new writes and validated against old rows later in some engines. This bounds lock time while preserving forward integrity. Product syntax and guarantees differ.

Find and repair violations before final validation. An application-only shadow check can measure impact but does not enforce against every writer. After enforcement, keep rejected-write observability without logging sensitive values.

**Manage type changes deliberately.** Widening integer range may be logically compatible but physically rewrite in one engine. Narrowing, precision/scale, collation, time zone, encoding, enum, or JSON structure can lose information. Define total/partial conversion, rounding, invalid values, and rollback.

When conversion is not bijective, rollback cannot reconstruct original data unless it is retained. Use a new field/table plus original, record conversion status, and obtain domain approval for loss. Never hide invalid values under arbitrary defaults.

**Migrate primary and partition keys as ownership changes.** A new key changes identity, routing, locality, uniqueness, foreign references, transactions, and pagination. Build a new layout, capture changes, maintain an ID mapping if logical identity persists, validate, cut over with routing epoch, and fence old ownership.

Dual reads across layouts can duplicate results. Deduplicate by stable logical ID/version and expose consistent pagination. Rollback must carry new writes back or keep old layout current; an abandoned stale layout is not rollback.

**Make cutover explicit.** Preconditions include candidate caught up to declared frontier, zero unexplained divergence, capacity under peak/failure, compatible clients, replicas/backups ready, alerts/runbooks active, and rollback tested. Switch the smallest possible cohort first when routing allows.

Use configuration/versioned routing that changes atomically and is observable. Fence stale writers through schema epoch, lease, permission removal, trigger, or routing rejection. DNS/cache/connection pools can prolong old routing; measure drain.

**Design rollback before crossing the boundary.** Before cutover, rollback may mean stop candidate and continue source. After cutover, new writes exist. Either dual-apply them to source, retain a reverse change stream, or define a forward repair rather than pretending old state is current.

Rollback of an engine binary may be impossible after disk/catalog/WAL format upgrade. Official support matrices govern. Snapshot/backup restore is a separate recovery with RPO/RTO and post-snapshot work loss unless replay compatibility exists.

**Contract only on evidence.** Remove the old column/table/index/protocol after telemetry shows no old reads/writes, fleet inventory confirms no old versions, rollback window closes, backups/restores no longer require old tooling, replicas and CDC consumers advance, and legal/audit retention permits.

Contraction is destructive and often hard to reverse. Take a governed backup or export where policy allows, validate restoration, then execute bounded DDL. Removal can itself rewrite or lock.

**Plan migration capacity.** Include old and new table/index copies, shadow generation, WAL/binlog retained during backfill, change queues, temp sort/spill, MVCC old versions, replication, backups, growth during duration, and reserve. Estimate rate and completion range under throttling.

If source size is $B$, candidate multiplier is $c$, retained change/log rate is $r$ bytes/s for duration $T$, temporary workspace is $W$, growth is $G$, and reserve is $R$, a first storage check is existing usage plus $cB+rT+W+G+R$. Avoid double counting by naming boundaries. The estimate is not a substitute for measured peaks.

Migration must survive one required node/AZ failure while backfill/replication runs. Limit background service from live SLO and debt, not a fixed rows/s. Pause safely before saturation; ensure log retention does not expire while paused.

**Upgrade database software as a protocol change.** Read supported direct paths, rolling compatibility, replica direction, catalog/disk/WAL format, extension/driver/OS dependencies, deprecated behavior, default changes, and downgrade limits. Pin exact packages/images and checksums.

Two common strategies are in-place upgrade and logical/physical replication to a new cluster. In-place can be fast but has format/downtime/rollback constraints. Replication permits online validation and cutover but costs duplicate capacity, catch-up, unsupported-object handling, and sequence/large-object/schema synchronization.

**Test mixed-version topology.** During rolling upgrade, old and new nodes exchange protocol/log/state. Verify supported order, leader election/failover in both directions, writes/reads/transactions, schema changes, backup, repair, and monitoring. Do not let an upgraded node write a format old nodes cannot read unless the upgrade contract allows no rollback.

Quorum availability can shrink during upgrade. Capacity must include one upgrading node plus one failure if required. Upgrade one failure domain at a time and wait for health/debt convergence, not a fixed sleep.

**Expect planner and semantic change.** New versions change optimizer rules, statistics, parallelism, collation libraries, type behavior, keywords, error codes, defaults, security, and resource use. Replay representative production query fingerprints with parameter classes, compare results and plans, and measure tails under mixed load.

Plan changes are not automatically regressions, and identical plans can perform differently. Keep reversible per-query mitigations only when supported and avoid freezing every old plan. Validate application error handling and drivers.

**Canary and observe.** Canary a shard, replica-read cohort, tenant, or shadow query where isolation and representativeness are defensible. Compare correctness first, then latency/error/abort, query plans, CPU/memory/storage/network, locks, WAL/log, replication lag, maintenance debt, and backup.

Canarying one empty shard does not represent hot/large data. Include risk-based cohorts and stop conditions. Shadow reads must avoid external effects, protect data, and account for double load.

**Test failures at every boundary.** Kill backfill workers before/after commit; lose change acknowledgements; restart index build; fill disk; delay replica; fail leader during mixed version; restore a pre-expansion backup into new tooling; cut network during cutover; retry stale client writes; and roll back after new writes.

Oracles cover invariants, key/value equivalence, constraint enforcement, query results, no duplicate/lost mutations, one writer authority, durability, and recovery. Preserve exact versions/configuration and histories. Passing finite tests bounds evidence only.

The executable fixture below models a finite idempotent version-conditioned backfill. It skips a row changed by a foreground writer and succeeds after recomputing from current state. It is not a database transaction, change stream, schema validator, migration tool, or concurrency test.

<!-- bijux-verify: {"id":"finite-versioned-backfill","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"first_changed=1\nfirst_skipped=1\nrow_a_display=Ada\nrow_b_display=Grace Hopper\nrow_b_version=3\nretry_changed=1\nall_migrated=true\nidempotent_retry=true\nevidence=finite_versioned_backfill\n","stderr":""}} -->
```python
rows = {
    "a": {"name": "Ada", "display_name": None, "version": 1},
    "b": {"name": "Grace", "display_name": None, "version": 1},
}
snapshot_versions = {key: row["version"] for key, row in rows.items()}
rows["b"].update(name="Grace Hopper", version=2)

def backfill(expected):
    changed = skipped = 0
    for key, expected_version in expected.items():
        row = rows[key]
        if row["display_name"] is not None:
            continue
        if row["version"] != expected_version:
            skipped += 1
            continue
        row.update(display_name=row["name"], version=row["version"] + 1)
        changed += 1
    return changed, skipped

first_changed, first_skipped = backfill(snapshot_versions)
retry_expected = {"b": rows["b"]["version"]}
retry_changed, _ = backfill(retry_expected)
before_idempotent = {key: row.copy() for key, row in rows.items()}
backfill({key: row["version"] for key, row in rows.items()})
print(f"first_changed={first_changed}")
print(f"first_skipped={first_skipped}")
print(f"row_a_display={rows['a']['display_name']}")
print(f"row_b_display={rows['b']['display_name']}")
print(f"row_b_version={rows['b']['version']}")
print(f"retry_changed={retry_changed}")
print(f"all_migrated={str(all(row['display_name'] for row in rows.values())).lower()}")
print(f"idempotent_retry={str(rows == before_idempotent).lower()}")
print("evidence=finite_versioned_backfill")
```

## Definitions and Notation

- A **schema version** identifies the logical representation accepted/produced by a component; a **storage/catalog version** identifies engine representation.
- A **compatibility matrix** lists whether each reader/writer/tool version safely interoperates with each database state.
- **Expand–migrate–contract** adds compatible representation, moves state/authority, then removes old representation.
- A **backfill** transforms preexisting rows; **foreground mutation** is live application work during it.
- $q_s$ is a row's relevant source version at transformation; later versions must not be overwritten by stale work.
- A **frontier** $s$ is a totally or partition-ordered source/change position under named semantics.
- A **shadow representation** is a candidate table/index/layout built beside authority.
- **Cutover** switches authority; a **fence** rejects stale-epoch mutations; **contraction** removes the old contract.
- **Dual read/write** consults or mutates two representations under explicit precedence and failure semantics.
- **Reconciliation** compares candidate and authority at a declared version/frontier and repairs explainable differences.
- $B$ is source bytes, $c$ candidate multiplier, $r$ retained change-log bytes/s, $T$ duration, $W$ workspace, $G$ growth, and $R$ reserve in a scoped capacity estimate.
- A **mixed-version topology** contains nodes/clients with different software versions under a supported compatibility window.
- A **forward fix** repairs the new state when true rollback cannot preserve accepted work.

## Mechanisms, Invariants, or Proof Structure

**Reader/writer compatibility.** For every transition state $S_j$, each live reader $R_i$ must map every representation reachable in $S_j$ to intended domain meaning or reject explicitly; every live writer $W_i$ must produce a representation accepted by constraints and all required readers. One incompatible cell in the matrix blocks that deployment order.

**Version-conditioned backfill.** Read row and relevant version $q_s$, compute candidate, then atomically update only if current version remains $q_s$ and target is not already authoritative. If predicate fails, re-read/recompute or classify. Therefore stale backfill cannot overwrite a newer foreground mutation under the version premise.

**Snapshot-plus-change completeness.** Copy every source identity as of $s_0$; capture every committed mutation after $s_0$; apply in source order/idempotently through $s_c$. The candidate at $s_c$ equals source if transform is deterministic, identity mapping total, deletes represented, and no event gap exists. Each premise needs evidence.

**Cutover authority.** Atomic routing epoch selects source before boundary and candidate after boundary. Fencing rejects old-epoch writes after switch. Candidate is caught up through the switch position. Thus each accepted write has one authority; caches/connections must honor epoch or be drained/validated.

**Rollback preservation.** Post-cutover writes must exist in the rollback target or be reproducibly transferable before routing back. Merely retaining old files preserves pre-cutover state, not current authority. Non-bijective conversion further requires original data or accepted irreversible loss.

**Capacity inequality.** Under named non-overlapping boundaries, available capacity must exceed current usage plus $cB+rT+W+G+R$. Duration $T$ depends on throttling and failures; log rate $r$ can grow with the migration itself. Use ranges and pause/retention safety.

**Contraction safety.** An old representation may be removed only when no supported actor reads/writes it, no rollback/restoration path needs it, candidate constraints/equivalence/recovery pass, and retention permits destruction. Time elapsed is not proof of these predicates.

## Alternatives and Trade-Offs

**Direct DDL versus expanded representation.** Direct DDL is simple and may be atomic/metadata-only but couples all clients and can lock/rewrite. Expansion costs temporary complexity/storage but permits staged compatibility and rollback.

**In-place versus shadow copy.** In-place change preserves one identity and avoids duplicate storage when supported, but failure/rollback can be constrained. Shadow copy enables independent validation and cutover at duplicate capacity/change-capture cost.

**Trigger/database dual write versus change stream.** Transactional database derivation can give immediate atomicity but adds write latency and coupling. Change streams scale asynchronously but expose lag and need replay/reconciliation. Application dual calls are usually the weakest choice.

**Online versus offline index build.** Online preserves writes at more complexity, resource interference, and perhaps longer duration. Offline maintenance can be safer/faster when a bounded outage is acceptable. “Online” still needs lock and failure evidence.

**Rolling versus blue-green engine upgrade.** Rolling reduces duplicate fleet cost but operates mixed versions and may constrain rollback. Blue-green/new cluster gives isolation and query comparison but needs replication, double capacity, cutover, and data synchronization.

**Physical versus logical upgrade path.** Physical paths preserve representation efficiently but have strict version/platform compatibility. Logical export/replication translates across versions and enables transformation but may omit objects, reorder, or take longer.

**Dual read versus shadow read.** Dual read can compare user-path results but doubles load and needs conflict precedence. Shadow read does not affect response but can leak data or create side effects unless queries are safe. Offline snapshot comparison is isolated but misses live behavior.

**Rollback versus forward fix.** Rollback is valuable before irreversible representations/new writes. After the boundary, a forward repair may be safer and faster. Decide thresholds and practice both rather than promising rollback universally.

## Failure Modes and Misconceptions

- **“Online means no locks.”** coordination locks may occur at start/end or wait behind long transactions.
- **“Metadata-only means risk-free.”** application interpretation and replicas can still break.
- **“Nullable now, not-null later is enough.”** old writers, invalid defaults, backfill races, and hidden writers remain.
- **“Dual write keeps copies equal.”** partial success and retry reorder them without atomicity/replay.
- **“Backfill can overwrite because it is authoritative.”** foreground changes are newer authority.
- **“Equal row counts prove migration.”** keys, values, types, deletes, ordering, and constraints can differ.
- **“Caught up once means safe cutover.”** a final frontier and writer fence are required.
- **“Keeping the old table is rollback.”** it is stale after new-only writes.
- **“Concurrent index build is free.”** it consumes full-system capacity and can leave invalid state.
- **“Adding a node version is reversible.”** disk/WAL/catalog formats may prevent downgrade.
- **“Replicas prove backup.”** topology failure/corruption and point-in-time needs differ.
- **“One canary proves fleet safety.”** size, skew, extensions, plans, and failure domains differ.
- **“Pause migration indefinitely.”** retained logs, dual-write divergence, and temporary capacity may expire.
- **“Drop is cleanup.”** contraction is a destructive protocol boundary.
- **“Successful startup proves upgrade.”** semantics, plans, failover, restore, and mixed load remain unverified.

## Worked Examples

### Example 1

**Situation.** New writers emit enum `archived`; 20% of old readers crash on unknown enum values.

The compatibility matrix blocks writer rollout. First deploy readers that preserve or explicitly handle unknown/new values, verify fleet inventory, then enable new writers by canary. A database enum addition alone does not make applications forward-compatible.

**Conclusion.** Reader compatibility gates new data, not merely new schema installation.

### Example 2

**Situation.** A backfill reads `name=Grace, version=4`. A user changes it to `Grace Hopper, version=5` before backfill writes `display_name=Grace`.

An unconditional update creates stale derived data. Require version 4 and missing target in the update predicate; it conflicts. Re-read version 5 and derive `Grace Hopper`, or let the new foreground writer atomically maintain the target.

**Conclusion.** Version-conditioned backfill preserves newer foreground authority.

### Example 3

**Situation.** A 4 TB table gets a “concurrent” index. The index is 1.5 TB, WAL grows 300 MB/s for four hours, workspace is 0.4 TB, growth/reserve 0.8 TB.

WAL retention alone is $0.3\times14{,}400=4{,}320$ GB, or 4.32 TB decimal. Extra requirement is about $1.5+4.32+0.4+0.8=7.02$ TB before replicas and overlap. The operation can exhaust a volume despite online query access.

**Conclusion.** Online is an availability mode, not a storage/capacity adjective.

### Example 4

**Situation.** A shadow copy reports 100 million rows, equal to source, but 10,000 deletes were missed and 10,000 duplicate stale rows were inserted.

Counts cancel. Compare stable key sets and versions, deletion/tombstone state, partitioned canonical hashes, exact risk samples, constraints, and representative query results at one frontier. Repair capture gaps before cutover.

**Conclusion.** Aggregate counts cannot establish row-level equivalence.

### Example 5

**Situation.** An online index build fails after its data scan and remains marked invalid.

Do not assume automatic use or delete blindly. Inspect official engine state, locks, disk/WAL, replicas, and supported retry/drop path. Ensure no constraint attached and no query hint/tool references it. Rebuild from a clean candidate if integrity cannot be established.

**Conclusion.** Candidate lifecycle needs explicit invalid/failure cleanup.

### Example 6

**Situation.** Read routing switches to a new table, but connection pools cache old prepared statements and one worker continues writing the old table.

Version routing and writer fence must be enforced at database/protocol authority, not only a feature flag. Drain or invalidate old pools, reject old schema epochs, monitor attempted stale writes, and reconcile any accepted during the gap.

**Conclusion.** Cutover includes long-lived clients and stale writer fencing.

### Example 7

**Situation.** After cutover, 50,000 new rows exist only in the candidate. Error rate rises and the team points reads back to the old table.

This loses or hides accepted work. Before rollback, replay candidate changes back under stable identity/version or repair forward. If reverse compatibility was not maintained, declare rollback unavailable past the boundary and execute the tested forward fix.

**Conclusion.** Post-cutover state determines whether rollback is real.

### Example 8

**Situation.** A rolling engine upgrade has three nodes. One upgraded node becomes leader and writes a log feature old nodes cannot replay.

If unsupported, downgrade/failback is already broken. Follow documented upgrade order and feature gates; prevent incompatible format activation until every node passes. Test leadership/failover in mixed state and retain compatible backups.

**Conclusion.** Binary coexistence does not prove bidirectional replication or downgrade safety.

### Example 9

**Situation.** Query p99 regresses only for one parameter class after upgrade, while average latency improves.

Compare fingerprints by bind/selectivity class, plans, estimates/actuals, collation/statistics, cache, and resource waits. Canary a reversible plan/statistics/config mitigation and verify results. Do not roll back the whole engine from fleet mean alone.

**Conclusion.** Upgrade review must stratify queries and preserve semantic/result checks.

### Example 10

**Situation.** A pre-expansion backup restores under the new engine, but the application expects the new field and migration-progress table.

Startup success is insufficient. Restore must replay schema and data migrations from a known state, recreate progress/frontiers idempotently, then validate constraints, queries, indexes, permissions, and application compatibility. Alternatively retain version-matched restoration tooling/images.

**Conclusion.** Disaster recovery must span historical schema and engine states.

## Cross-Program Connections

[Software Delivery and Reliability Engineering](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) connects compatibility, canaries, feature flags, deployment order, rollback, and SLO gates. Database state makes rollback data-dependent.

[API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) connects versioned representations, tolerant readers, idempotency, conditional updates, and deprecation. Schema is an internal API with persistent clients: stored records.

[Data Engineering](../../19-data-engineering/ROADMAP.md) connects backfills, change capture, replay, dual pipelines, data validation, and cutover. Database migrations use the same provenance and reconciliation discipline.

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) connects epochs, fencing, replication, consensus, partial failure, and ownership movement. Cutover is a distributed authority transition.

[Platform Engineering](../../29-platform-engineering/ROADMAP.md) connects fleet/version inventory, automated rollout, policy gates, capacity, secrets, and standardized recovery. Automation must encode product-specific preconditions.

[Security Engineering](../../25-security-engineering/ROADMAP.md) connects privilege changes, extension/supply-chain integrity, audit, encryption keys, sensitive migration telemetry, and destructive contraction.

## References

- PostgreSQL Global Development Group, [Modifying Tables](https://www.postgresql.org/docs/current/ddl-alter.html), current documentation checked 2026-09-05. Concrete add/remove/default/constraint/type and table-alter behavior.
- PostgreSQL Global Development Group, [CREATE INDEX](https://www.postgresql.org/docs/current/sql-createindex.html), current documentation checked 2026-09-05. Concurrent builds, validity, transaction, locking, and partition considerations.
- PostgreSQL Global Development Group, [pg_upgrade](https://www.postgresql.org/docs/current/pgupgrade.html), current documentation checked 2026-09-05. Concrete major-version in-place upgrade preparation, compatibility, modes, and post-upgrade work.
- PostgreSQL Global Development Group, [Logical Replication](https://www.postgresql.org/docs/current/logical-replication.html), current documentation checked 2026-09-05. Publication/subscription, snapshot copy, change application, and restrictions.
- Oracle, [MySQL 8.4 InnoDB Online DDL Operations](https://dev.mysql.com/doc/refman/8.4/en/innodb-online-ddl.html), current documentation checked 2026-09-05. Product-specific in-place/copy/instant algorithms, locks, and operation support.
- SQLite, [ALTER TABLE](https://www.sqlite.org/lang_altertable.html), current documentation checked 2026-09-05. A contrasting product's rename/add/drop behavior and compatibility controls.
- GitHub, [gh-ost](https://github.com/github/gh-ost), current repository documentation checked 2026-09-05. Triggerless online schema migration using replication logs, throttling, cutover, and control mechanisms.
- Vitess, [Schema changes](https://vitess.io/docs/user-guides/schema-changes/), current documentation checked 2026-09-05. Managed online DDL strategies, lifecycle, and migration operations.
- Cockroach Labs, [Online schema changes](https://www.cockroachlabs.com/docs/stable/online-schema-changes), current documentation checked 2026-09-05. Transactional distributed schema-change behavior, limitations, and operational guidance.
- Google SRE authors, [Canarying Releases](https://sre.google/workbook/canarying-releases/), in *The Site Reliability Workbook*, 2018. Canary selection, evaluation, and rollout evidence.

## Exercises

### Exercise 1

Define compatibility matrix, expand–migrate–contract, backfill, frontier, shadow representation, cutover, fence, rollback, contraction, and mixed-version topology. Explain why “online” alone is not a guarantee.

### Exercise 2

A 6 TB source requires a candidate at 0.7 times source size, change logs grow 180 MB/s, migration duration is 18 hours, workspace is 0.8 TB, growth is 0.5 TB, and reserve is 1 TB. Compute the first-order extra capacity in decimal units and state uncertainty.

### Exercise 3

A backfill and new writer disagree on precedence between old `amount_float` and new decimal `{amount,currency}` fields. Diagnose the semantic and concurrency hazards and design a safe transition.

### Exercise 4

Design a rolling major-engine upgrade for five nodes with synchronous replication, one node of failure tolerance during maintenance, incompatible extension versions, planner changes, nightly backup, and a no-data-loss acknowledgement contract.

### Exercise 5

A sharded primary-key migration has copied 99.99%, but change-log retention will expire in six hours, a hot shard is 12 hours behind, and product demands cutover today. Decide whether to proceed and give the smallest safe recovery plan and evidence gates.

## Answers to the Exercises

### Answer 1

A **compatibility matrix** evaluates each reader/writer/tool against each database state. **Expand–migrate–contract** adds compatible state, moves data/authority, then removes old state. A **backfill** transforms existing rows. A **frontier** is a source/change position. A **shadow representation** is a candidate beside authority. **Cutover** switches authority; a **fence** rejects stale writers. **Rollback** returns to a supported state while preserving accepted work; **contraction** destroys old compatibility. A **mixed-version topology** contains interoperating software versions. “Online” says only that some service continues; it does not specify locks, affected operations, latency, semantics, resource impact, failure, or rollback.

### Answer 2

Candidate bytes are $0.7\times6=4.2$ TB. Duration is $18\times3{,}600=64{,}800$ seconds; logs are $0.18\times64{,}800=11{,}664$ GB, or 11.664 TB decimal. Extra capacity is $4.2+11.664+0.8+0.5+1=18.164$ TB, in addition to current usage under this accounting. Uncertainty includes migration-generated log changes, compression, indexes/replicas, old versions, duration under throttling/failure, log cleanup, temp peaks, source growth, and double-counted boundaries. Use a range and monitor retention time, not this point estimate alone.

### Answer 3

Float cannot exactly represent many decimal amounts and lacks currency; converting without source meaning can manufacture precision. Define the new domain representation and conversion policy with explicit invalid/unknown cases. Deploy readers that understand both and deterministic precedence keyed by schema version, not whichever field happens to exist. New writers atomically write authoritative decimal plus transitional old value only when a loss policy permits. Backfill reads old value/version, uses a documented rounding/currency source, and conditionally writes only if unchanged; ambiguous rows go to review. Reconcile amounts, currencies, rounding, nulls, and business totals. Keep original float for rollback/audit until no old writer/reader remains and loss is accepted; then enforce decimal constraints and contract.

### Answer 4

Inventory exact engine, WAL/protocol, extension, driver, OS, backup, and downgrade support. Resolve incompatible extensions or create a new-cluster logical path; do not start rolling if nodes cannot interoperate. Prove six? No—there are five nodes: with one upgrading and one additional failure, three remaining must preserve the required synchronous quorum and capacity. Test that placement, cold failover, writes, reads, transactions, lag, and acknowledged-history recovery. Take and restore a version-compatible backup. Canary one noncritical but representative node, keep incompatible features disabled, validate mixed-version leader/follower in supported order, plans/results by query class, SLOs/resources, and backup. Advance one failure domain at a time only after lag/debt convergence. Enable new formats/features after every rollback-dependent old node is gone. Verify failover, no acknowledged-write loss, and restore on the final version before contraction.

### Answer 5

Do not cut over: 0.01% unexplained and a hot shard behind the retention horizon violate completeness, and pressure does not make stale authority safe. Immediately protect the source/change log by expanding retention/storage or pausing optional work; throttle foreground/migration only within service policy; prioritize the hot shard; checkpoint exact frontier and diagnose service/skew. If retention cannot be extended, restart that shard from a newer consistent snapshot while retaining overlapping changes, not from a gap. Cutover gates are complete key/version/delete reconciliation for every shard at a declared frontier, hot-shard catch-up, no impending log expiry through rollback, capacity and failure tests, fenced old writers, representative query equivalence, and tested rollback/forward repair. The smallest missing resource may be temporary log/storage capacity; if unavailable, the honest outcome is delayed cutover.
