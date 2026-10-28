---
module_id: DBE-047
program: Database Engineering
level: 1
module_number: 47
title: Snapshot Visibility
status: complete
last_verified: 2026-08-30
---

# Snapshot Visibility

## One-Page Review

### Governing question

Given transaction outcome, snapshot boundaries, in-progress exclusions, creator/deleter metadata, and the reader's own commands, exactly which logical row state may a query observe?

### Essential definitions

A **snapshot** is an immutable description of transaction effects eligible for one statement/transaction, not simply “the current time.” In a high/low-watermark abstraction, `S=(low,high,active)` records a lower boundary, an exclusive upper boundary, and transaction identifiers that were active when S was captured. Transactions below `low` completed before capture but still need committed-versus-aborted status. Identifiers at least `high` are future/uncompleted relative to S. An identifier in `[low,high)` is in-progress if in `active`; otherwise it completed before capture and its outcome decides visibility. A physical tuple version has a **creator** and optionally a **deleter/superseder**. It is visible when its creation is visible and its deletion is not visible. **Read-your-writes** adds the reader's eligible prior commands even though its transaction is uncommitted. A **statement snapshot** can advance between statements; a **transaction snapshot** remains fixed under its policy. A **current/locking read** may intentionally use newer state and locks rather than the consistent snapshot path.

### Central model, mechanism, or theorem

For another transaction X under the teaching snapshot: creation/deletion by X is visible only if X committed and either `X<low`, or `low<=X<high` and `X not in active`. Active-at-capture X remains invisible to that fixed snapshot even if X commits later; `X>=high` is future. Aborted X is never visible. The reader's own prior nonaborted commands use transaction-local command order. A tuple is selected iff `CreatorVisible` and not `DeleterVisible`; among several selected physical versions of one logical key, version ordering must identify exactly one state.

This resembles PostgreSQL's documented `xmin:xmax:xip_list` snapshot representation but is not a complete PostgreSQL tuple-visibility algorithm. Product rules include subtransactions, command IDs, freezing, multitransaction lockers, speculative insertion, recovery, catalog behavior, and different snapshot types. InnoDB read views and SQL Server transaction sequence snapshots encode related boundaries differently.

### Critical invariants

- Snapshot capture is atomic with respect to transaction start/completion publication under the engine's ordering protocol.
- The snapshot remains immutable for its promised lifetime; a later commit cannot retroactively enter it.
- Transaction identifier order is never substituted for committed/aborted/in-progress outcome.
- Creator and deleter decisions use the same snapshot, status source, and command/self rules.
- Other transactions' active/aborted/future candidates remain invisible; eligible own earlier writes/deletes are reflected.
- At most one logical state per key is returned, including updates represented as old-version delete plus new-version create.
- Index and heap/version-chain paths apply equivalent visibility, including recheck of stale/dead index membership.
- Cleanup, status truncation, ID reuse/wraparound, replica import/export, and crash recovery cannot erase metadata needed by a valid snapshot.

### Common failures

Failures include comparing transaction IDs numerically without the active set; assuming “committed now” means visible to an older snapshot; treating every ID below `low` as committed; making the upper bound inclusive; interpreting tuple `xmax != 0` as necessarily deleted; forgetting own-command order; returning both old/new update versions; applying statement snapshot rules to a transaction snapshot; mixing consistent and locking/current reads without a model; exporting a snapshot after dependent work begins; using wall clocks across nodes; reading transaction-status/tuple metadata nonatomically; retaining a snapshot but vacuuming its required status/version; and treating visibility as proof of serializability or business freshness.

### Compact example

Snapshot `S=(low=4, high=7, active={4,6})`. X5 committed before capture, so a version created by X5 is visible. X4 was active at capture, so its later commit does not enter S. Row A old version `(creator=1, deleter=5, value=100)` is invisible because its deletion is visible; new A `(creator=5,value=120)` is visible. Row C `(creator=3,deleter=4,value=300)` remains visible because X4's deletion is invisible to S. X2's aborted insertion and X7's future insertion are invisible. Reader X8 sees its own prior insertion despite `8>=high`.

### Connections

Retrieve [Multi-Version Concurrency Control](046-multi-version-concurrency-control.md), [Read and Write Anomalies](042-read-and-write-anomalies.md), and [Transaction Boundaries](041-acid-and-transaction-boundaries.md). Continue through the Database Engineering [roadmap](../ROADMAP.md) to DBE-048, Isolation Levels, and DBE-049, Serializable Snapshot Isolation.

## Governing Question

How can a database make every creator, updater, deleter, and reader agree on one historically consistent logical state even though transaction identifiers are assigned before outcomes and physical versions coexist?

## Why This Matters

MVCC's storage structures are useful only if visibility is exact. One boundary error can expose uncommitted data, resurrect a deletion, hide a committed row, duplicate an updated row, violate uniqueness, or reclaim history while a reader still needs it. These bugs can be schedule-dependent and survive ordinary tests.

The deceptive case is a lower-numbered transaction that remains active while a higher-numbered transaction commits. Snapshot capture cannot say “all IDs less than my ID are visible.” It needs a boundary plus knowledge of exceptions, or an equivalent commit-order representation. When the lower transaction later commits, a fixed snapshot must remember it was incomplete at capture. Otherwise repeated reads change retroactively.

Visibility also differs from freshness. A transaction snapshot intentionally excludes later commits. It can be perfectly correct and stale. Visibility differs from serializability: two transactions can each read a valid fixed snapshot and still produce write skew. It differs from authorization/audit time: system transaction metadata is internal and may wrap, freeze, or be reclaimed.

Current products expose different pieces. PostgreSQL documents `pg_snapshot` as `xmin:xmax:xip_list` and tuple system columns `xmin/xmax`; InnoDB documents read views and undo-based consistent reads; SQL Server documents active XSNs and statement/transaction row-versioned snapshots. The shared reasoning is eligibility at capture plus outcome and self-command rules, not field-name portability.

## Prerequisites and Retrieval

You should understand MVCC versions/chains, transaction states, half-open intervals, set membership, inserts/updates/deletes, statement versus transaction isolation, WAL/status recovery, and garbage-collection horizons. Retrieve creator/deleter, high-water mark, active set, commit point, own writes, command order, tombstone, subtransaction, index recheck, write skew, and serialization anomaly.

DBE-046 introduced the simplified scalar commit-sequence model and safe reclamation. This module replaces that scalar with snapshot exceptions and tuple decisions. DBE-048 maps snapshot lifetimes/phenomena to isolation levels; DBE-049 adds dependency validation for serializability.

## Learning Objectives

After this module, you can:

1. explain why transaction-ID order alone cannot determine snapshot visibility;
2. construct and interpret low/high/in-progress snapshot representations;
3. derive creator and deleter visibility from outcome, boundaries, active set, and self rules;
4. collapse physical insert/update/delete versions into one logical row state;
5. distinguish statement, transaction, exported/imported, historical, and current/locking reads;
6. handle just-before/at/after capture, commit, abort, and command-order boundaries;
7. reason about subtransactions, frozen/old IDs, wraparound, status retention, indexes, and cleanup without false portability;
8. connect valid snapshots to anomalies that still require locking or serializable validation;
9. diagnose visibility incidents from transaction, snapshot, tuple/version, index, and recovery evidence; and
10. design exhaustive model-based and crash-boundary tests with independent visibility oracles.

## Core Exposition

**Transaction IDs precede outcomes.** Many engines assign an identifier when a transaction first needs one, before it commits or aborts. Suppose X4 begins and stalls; X5 begins and commits; then a reader captures a snapshot. X5 belongs in the reader's past, while X4 does not, although `4<5`. Later X4 commits, but it must stay invisible to that fixed snapshot. Numeric prefix rules cannot represent this history.

An engine can instead assign visibility order at commit, maintain an active exclusion set, or use another proven scheme. This module's abstraction uses `S=(low,high,active)`:

- IDs `<low` completed before capture; status distinguishes committed from aborted.
- IDs `>=high` had not completed by capture and are invisible to S.
- IDs in `[low,high)` listed in `active` were in progress and remain invisible to S.
- IDs in `[low,high)` absent from `active` completed before capture; committed effects are eligible, aborted effects dead.

Use half-open `[low,high)`: `high` itself is not visible. `low` often relates to the oldest active transaction, but a complete production snapshot can contain subtransaction/overflow/recovery details. “Below low visible” still requires commit status; aborted work is never made alive by age.

**Snapshot capture is a publication protocol.** The system must not miss a transaction that is simultaneously committing. If capture reads the active set before a commit removes itself, then the snapshot must exclude that transaction. If it observes the committed outcome and corresponding ordering before building the set, it may include it. There must be no interleaving where a candidate is absent from active but its committed state is not safely published, or visible without durable/consistent outcome.

This atomicity may use centralized transaction tables, locks/latches, sequence barriers, epochs, commit sequence numbers, or distributed timestamp protocols. Wall-clock timestamps are insufficient without bounds/order guarantees. The proof obligation is a consistent cut of transaction publication, not a timestamp API call.

**Creator visibility.** For physical version v created by X:

1. If X is the reader and v came from a prior eligible command, apply read-your-writes unless that subtransaction/command was rolled back.
2. If X aborted, creation is invisible.
3. If X remains active and is another owner, invisible.
4. If X committed but is in S.active, invisible: it was incomplete at capture.
5. If X committed and `X>=S.high`, invisible: future relative to capture.
6. If X committed and `X<S.low`, visible under retained status/freeze rules.
7. If X committed, `low<=X<high`, and X not active, visible.

The status “committed now” cannot erase rules 4/5. Visibility is a relation among version, reader, snapshot, and transaction-local command state—not a permanent boolean stored on the row.

**Deleter visibility.** A version with visible creation remains logically present unless its deletion/supersession is visible to the same reader/snapshot. If deleting X aborted, was active at capture, or is future, the deletion is invisible and the old version remains. If deleting X committed before the snapshot, the old version is absent. If the reader deleted its own row in a prior command, it normally sees absence.

A nonzero physical deletion field therefore does not necessarily mean invisible. PostgreSQL documents that `xmax` can be nonzero in a visible row version because deletion may be uncommitted or rolled back, and the field can participate in locking/multitransaction state. Other engines encode invalidation differently. Always run the product's full visibility/status logic.

**Updates are paired logical changes.** Conceptually, updating A from 100 to 120 invalidates old v1 and creates new v2. An old snapshot may see v1, a newer snapshot v2, and no correct ordinary snapshot sees both as separate logical A rows. Physical scans/indexes can encounter both. Deduplication is not arbitrary: creator/deleter/version ordering determines the one eligible state.

Key changes are deletion from old index membership plus insertion into new membership. An old snapshot may find old key; new snapshot new key. Secondary indexes can retain both entries until cleanup; heap/version recheck must prevent duplicates, missing rows, or a row under the wrong key. Unique/foreign-key checks can use current/locking conflict rules beyond the reader's snapshot.

**Own-command visibility needs order below transaction granularity.** A transaction sees effects of prior statements so `UPDATE` followed by `SELECT` returns the new value. It must not let an earlier command see a later command. Engines use command IDs, statement sequence, local write sets, or equivalent. Savepoint/subtransaction rollback makes a formerly own candidate dead while the parent continues. Bulk operations, triggers, cascades, speculative inserts, and `RETURNING` need defined command boundaries.

Do not simplify “own transaction always visible.” A deletion executed later should not rewrite the input snapshot of an already running statement; a rolled-back savepoint's insertion is not visible; statement execution may need Halloween protection so its own new versions are not repeatedly reprocessed.

**Statement versus transaction snapshot.** Under statement-level read committed, each statement captures a fresh S; two SELECTs can include a transaction committed between them. Each statement remains internally consistent under its documented rules. Under transaction-level snapshot/repeatable-read policy, successive consistent reads reuse S and exclude later commits. This improves repeatability but increases staleness/history retention.

Snapshot acquisition time can be first data statement rather than textual `BEGIN`. PostgreSQL documents repeatable-read snapshot at the first non-transaction-control statement; InnoDB documents first consistent read for default repeatable read unless explicitly requested; SQL Server assigns/uses transaction sequence state according to its current row-versioning rules. Never infer boundary from application log wording alone.

**Consistent versus current/locking reads.** A historical SELECT answers “what was eligible in S?” A locking read/update often must find a current version and coordinate with concurrent writers so it can make a present-state decision. Mixing them can produce a transaction-local view combining historical untouched rows with its own/current modified rows. InnoDB explicitly warns that mixing locking statements with nonlocking consistent SELECTs under repeatable read can expose difficult-to-interpret table states.

Choose deliberately. Use consistent reads for historical analysis/repeatability. Use locking/current reads or atomic constraints for decisions that must reserve current state. Serializable MVCC may retain consistent reads while tracking dependencies and aborting dangerous histories. Do not switch read type as a performance tweak without restating the invariant.

The executable model applies the teaching snapshot to inserts, update, delete, abort, future commit, and own write. Current status says X4 eventually committed, but membership in the captured active set keeps both X4's deletion of C and insertion of D invisible to this snapshot.

<!-- bijux-verify: {"id":"snapshot-creator-deleter-visibility","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"snapshot=(4, 7, (4, 6))\nvisible_rows=(('A', 120), ('C', 300), ('F', 600))\naborted_insert_visible=False\npost_snapshot_commit_visible=False\nin_progress_delete_keeps_row=True\nown_future_write_visible=True\ninvariants=True\n","stderr":""}} -->
```python
snapshot = {"low": 4, "high": 7, "active": {4, 6}}
status = {
    1: "committed",
    2: "aborted",
    3: "committed",
    4: "committed",
    5: "committed",
    6: "active",
    7: "committed",
    8: "active",
}
viewer = 8
versions = (
    {"key": "A", "value": 100, "creator": 1, "deleter": 5},
    {"key": "A", "value": 120, "creator": 5, "deleter": None},
    {"key": "B", "value": 200, "creator": 2, "deleter": None},
    {"key": "C", "value": 300, "creator": 3, "deleter": 4},
    {"key": "D", "value": 400, "creator": 4, "deleter": None},
    {"key": "E", "value": 500, "creator": 7, "deleter": None},
    {"key": "F", "value": 600, "creator": 8, "deleter": None},
)

def transaction_visible(transaction):
    if transaction == viewer:
        return status[transaction] != "aborted"
    if status[transaction] != "committed":
        return False
    if transaction < snapshot["low"]:
        return True
    if transaction >= snapshot["high"]:
        return False
    return transaction not in snapshot["active"]

def version_visible(version):
    creation_visible = transaction_visible(version["creator"])
    deletion = version["deleter"]
    deletion_visible = deletion is not None and transaction_visible(deletion)
    return creation_visible and not deletion_visible

visible_rows = tuple(
    sorted((version["key"], version["value"]) for version in versions if version_visible(version))
)
aborted_insert_visible = version_visible(versions[2])
post_snapshot_commit_visible = version_visible(versions[4])
in_progress_delete_keeps_row = version_visible(versions[3])
own_future_write_visible = version_visible(versions[6])
invariants = (
    visible_rows == (("A", 120), ("C", 300), ("F", 600))
    and not aborted_insert_visible
    and not post_snapshot_commit_visible
    and in_progress_delete_keeps_row
    and own_future_write_visible
)

print(f"snapshot={(snapshot['low'], snapshot['high'], tuple(sorted(snapshot['active'])))}")
print(f"visible_rows={visible_rows}")
print(f"aborted_insert_visible={aborted_insert_visible}")
print(f"post_snapshot_commit_visible={post_snapshot_commit_visible}")
print(f"in_progress_delete_keeps_row={in_progress_delete_keeps_row}")
print(f"own_future_write_visible={own_future_write_visible}")
print(f"invariants={invariants}")
```

**Imported/exported and distributed snapshots.** Exporting a snapshot allows another transaction to use a compatible visibility cut, but import has ordering/isolation/read-only and lifecycle constraints. The exporter must remain valid as required; transaction-status/version cleanup must respect imports. A snapshot identifier is capability-like internal state, not a reusable business timestamp. Confirm current product rules before parallel backup/analytics.

Across replicas/shards, a local snapshot does not automatically form a global consistent cut. Replica apply position, causality, safe timestamps, clock uncertainty, or distributed transaction metadata determine what is observable. A follower can serve a correct local historical snapshot that is stale relative to a client's prior write. Session guarantees and distributed consistency are separate from tuple visibility.

**Status retention, wraparound, and freezing.** Old tuple creator/deleter IDs may outlive ordinary transaction-status entries. Engines summarize old committed state, freeze versions, use larger epochs, or retain status until safe. PostgreSQL's internal 32-bit XIDs wrap and maintenance/freeze prevents old committed tuples from appearing future; its exposed `xid8` snapshot functions have different lifetime properties. Never persist raw internal transaction IDs as globally unique audit identifiers.

Cleanup uses the oldest snapshot/status obligations. If a version or commit/abort status is reclaimed while a valid snapshot can ask about it, visibility becomes unknowable. Conversely, retaining every status/version forever is unbounded. Prove a horizon covering local snapshots, exported/imported readers, replicas, backups, recovery, online operations, and temporal policy.

**Isolation anomalies survive correct visibility.** A snapshot may be transactionally self-consistent yet stale. Two transactions can see the same valid predicate, write disjoint rows, and violate it. A range scan can miss a later insert by design. A locking update may see a newer row than earlier consistent SELECT. These are isolation-policy outcomes, not necessarily visibility bugs. Diagnose by reconstructing promised snapshot lifetime and conflict rules before calling a result corrupt.

**Observability.** Capture engine/version/configuration/isolation, transaction and command identity, snapshot acquisition time/lifetime, low/high/active or equivalent sequence/exclusions, transaction outcome/publication, tuple/version creator/deleter/link, logical key/index path, current versus consistent read type, subtransaction/savepoint, replica/apply position, cleanup horizon, and recovery state. Protect sensitive row data.

Do not run expensive tuple/page/status inspection casually in production. Monitoring views race and may expose current status, while the question concerns status at snapshot capture. Retain transaction/query traces and reproduce in an isolated environment. A row's system columns alone are not a verdict.

**Testing.** Build a reference model independent of engine code. Enumerate transaction state `{active,committed,aborted}`, ID regions `<low`, `[low,high)` active/not-active, `>=high`, own/other, creation/deletion, prior/current/later command, and no/one/multiple physical versions. Assert one logical state. Test every just-before/at/after capture and commit publication interleaving with barriers, not sleeps.

Integration-test statement/transaction snapshots; active lower ID plus committed higher ID; later commit excluded; abort; read-your-writes/delete; savepoint rollback; update/key change; unique/foreign key; range/phantom; locking versus nonlocking reads; snapshot export/import; index-only/secondary path; cleanup while pinned; freeze/wrap harness; failover/replica; and crash around tuple/index/status/commit. Compare exact rows and transaction outcomes, then run invariants. Finite schedule tests do not replace the capture/publication proof.

## Definitions and Notation

- `S=(low,high,A)`: teaching snapshot with half-open ID interval and active-at-capture exclusion set A.
- `status(X) in {active,committed,aborted}`: transaction outcome/status known to the engine.
- `CV(X,T,S,c)`: whether creator transaction X's command c is visible to reader T under S.
- `DV(X,T,S,c)`: corresponding deleter/superseder visibility.
- `Visible(v,T,S) = CV(creator(v),T,S) and not DV(deleter(v),T,S)` when a deleter exists.
- **Command ID/order:** within-transaction boundary separating earlier, current, and later modifications.
- **Fixed snapshot:** eligibility cut that later external commits do not retroactively change.
- **Statement snapshot:** newly captured/selected for a statement according to isolation policy.
- **Transaction snapshot:** reused across transaction statements according to isolation policy.
- **Consistent/historical read:** selects snapshot-visible version without necessarily locking current row.
- **Current/locking read:** coordinates against current eligible state for modification/reservation.
- **Visibility map/summary:** optimization proving broader visibility/freeze facts; not source truth if stale/inconsistent.
- **Snapshot pin:** obligation retaining versions/status needed by a snapshot.

## Mechanisms, Invariants, or Proof Structure

**Eligibility partition.** For other transaction X, integer IDs fall into disjoint regions: `<low`, `[low,high)` active, `[low,high)` completed, and `>=high`. After checking committed outcome, only committed `<low` and completed-not-active middle IDs are creation/deletion-visible. The cases are exhaustive and mutually exclusive. X's later state transition cannot change membership in S.active or region, so S remains fixed.

**Tuple rule.** A physical version represents a logical state from visible creation until visible deletion. If creation is not visible, the version never existed for this reader. If creation is visible and deletion is not, it exists. If both are visible, it has already ended. Aborted/active/future deletion therefore leaves an earlier committed version visible. Own command ordering substitutes transaction-local eligibility where applicable.

**One-logical-version proof obligation.** For each logical key, version intervals/order must not overlap under one snapshot except transient physical candidates excluded by creator/deleter rules. An update's successor becomes eligible exactly where predecessor invalidation becomes eligible. If the storage/index algorithm can return two selected versions, metadata/publication/order is defective or the query is intentionally exposing history.

**Boundary proof.** Snapshot capture and commit publication must be linearized. A committing transaction is either observed as completed with durable outcome/version publication before capture, or remains represented as active/future in S. No third state—absent from active yet unpublished—may be visible. Recovery must recreate the same classification after crash.

**Independent verification plan.** Build a truth table over region, active membership, status, owner, command order, creator/deleter role; derive interval histories independently; enumerate snapshot cuts; compare index/heap paths; and inject publication crashes. Validate model and product separately, and state configuration/version.

## Alternatives and Trade-Offs

- **Active-set snapshot versus commit sequence:** active sets represent out-of-order completion but grow with concurrency; commit sequences simplify scalar comparisons but require coordinated assignment/publication.
- **Statement versus transaction snapshot:** fresh statements reduce staleness/pin duration but allow changing results; fixed transaction snapshots improve repeatability at retention/stale-decision cost.
- **Consistent versus locking/current read:** historical reads reduce row blocking; current reads reserve/validate present state but wait/deadlock and can differ from earlier snapshot results.
- **Inline status versus transaction table:** inline metadata speeds some decisions but bloats/changes tuples; central status supports outcome updates but adds lookup/cache/retention dependencies.
- **Explicit active list versus compressed/overflow representation:** explicit sets are exact; compression/overflow controls memory but can require conservative checks and status access.
- **Exported snapshot versus materialized copy:** export shares one cut cheaply but pins source history/lifecycle; materialization pays copy/storage and then decouples retention.
- **Local snapshot versus distributed safe timestamp:** local capture is cheap/exact for one engine; global cuts need coordination/uncertainty handling and can wait or be stale.
- **Visibility optimization versus recheck:** all-visible/index-only summaries avoid tuple checks; conservative recheck costs I/O but protects correctness when certainty is absent.
- **Snapshot isolation versus serializable validation:** fixed visibility gives consistent reads; dependency tracking/locks/validation add serializability at abort/block/tracking cost.

## Failure Modes and Misconceptions

- “Lower transaction ID means visible.” A lower transaction can still be active or aborted.
- “It committed before my SELECT returned.” Visibility depends on capture, not return time.
- “Committed now means visible now.” A fixed older snapshot retains its active/future exclusions.
- “Below low means committed.” It can be aborted; consult retained outcome/freeze semantics.
- “High is included.” The teaching interval is half-open; `X>=high` is future.
- “Nonzero deleter means row absent.” The delete may be active, aborted, future, or only a lock marker.
- “Own transaction is always visible.” Only eligible prior nonrolled-back commands are.
- “Update versions can both be returned.” One ordinary logical read must select one state.
- “Repeatable read snapshot begins at BEGIN everywhere.” Acquisition timing is engine/policy-specific.
- “Locking read is a fresher snapshot.” It may follow a different current/locking algorithm, not merely a later S.
- “A correct snapshot is serializable/fresh.” Neither follows from visibility alone.
- “Exported snapshot is a timestamp string.” It is lifecycle-bound engine state with import constraints.
- “System columns are portable/audit IDs.” They are engine internals with wrap/freeze/reuse and complex meanings.
- “Replica snapshot includes my prior write.” Only if apply/session consistency guarantees establish it.
- “Cleanup can discard old status after commit.” Valid snapshots may still need the outcome.

## Worked Examples

### Example 1

X4 starts, X5 commits, then S captures with X4 active and X5 absent from active. Conclusion: X5 can be visible while lower X4 is excluded; ID prefix is insufficient.

### Example 2

X4 commits after S. A new snapshot includes it, but S still lists X4 active. Conclusion: fixed snapshot membership does not retroactively change.

### Example 3

Version created by aborted X2 has ID below low. Outcome is aborted, so it is invisible. Conclusion: age does not convert dead work into committed history.

### Example 4

Old A was created by X1 and deleted by visible X5; new A was created by X5. S returns new A exactly once. Conclusion: update creation/invalidation must move together logically.

### Example 5

C was created by visible X3 and deleted by X4, active at capture. S returns C. Conclusion: an in-progress/later-committed deletion does not erase an older snapshot's row.

### Example 6

T inserts F then SELECTs F in a later command before commit. The base snapshot excludes T's high ID, but self-command rule includes F. Conclusion: read-your-writes overlays external snapshot eligibility.

### Example 7

T inserts G inside a savepoint and rolls back to it; later SELECT does not see G. Conclusion: “own” must include subtransaction/command outcome, not transaction identity alone.

### Example 8

Under statement read committed, SELECT1 excludes X9; X9 commits; SELECT2 captures new S and includes it. Under a transaction snapshot both exclude it. Conclusion: isolation policy chooses snapshot lifetime.

### Example 9

An InnoDB transaction performs historical SELECT, then locking UPDATE against current state. Its own next SELECT combines own new value with older untouched snapshot rows. Conclusion: mixed read modes require an explicit semantic model.

### Example 10

A secondary index contains old/new key entries. Heap/version recheck admits only the snapshot-correct tuple. Premature cleanup of old membership breaks an older reader. Conclusion: index and cleanup paths are part of visibility correctness.

## Cross-Program Connections

- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) supplies interval/set partitions, persistent versions, indexes, reachability, and garbage collection.
- [Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) supplies atomic snapshot capture, publication, epochs, read-copy-update, and ABA/reclamation reasoning.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies consistent cuts, logical clocks, safe timestamps, replica/session guarantees, and clock uncertainty.
- [Operating Systems](../../22-operating-systems/ROADMAP.md) supplies page visibility/cache metadata, epochs, crash consistency, and background reclamation.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) supplies consistent extraction, CDC positions, watermarks, late data, and snapshot-plus-log handoff.

## References

1. Philip A. Bernstein and Nathan Goodman, [“Multiversion Concurrency Control—Theory and Algorithms”](https://www.cs.cmu.edu/afs/cs.cmu.edu/academic/class/15712-f17/www/papers/bernstein83.pdf), *ACM Transactions on Database Systems* 8(4), 1983; DOI `10.1145/319996.319998`.
2. Hal Berenson et al., [“A Critique of ANSI SQL Isolation Levels”](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr-95-51.pdf), Microsoft Research Technical Report MSR-TR-95-51, 1995, snapshot-isolation definitions and anomalies.
3. PostgreSQL Global Development Group, [System Information Functions and Operators](https://www.postgresql.org/docs/current/functions-info.html), current `pg_snapshot` `xmin:xmax:xip_list`, status, and visibility function semantics.
4. PostgreSQL Global Development Group, [System Columns](https://www.postgresql.org/docs/current/ddl-system-columns.html), current tuple-version `xmin`, `xmax`, command ID, physical-location, and wraparound caveats.
5. PostgreSQL Global Development Group, [Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html), current statement/transaction snapshot acquisition, own writes, locking, anomalies, and retries.
6. Oracle, [MySQL 8.4 Consistent Nonlocking Reads](https://dev.mysql.com/doc/refman/8.4/en/innodb-consistent-read.html), current read-view lifetime, committed/own state, and DDL/mixed-read caveats.
7. Oracle, [MySQL 8.4 Transaction Isolation Levels](https://dev.mysql.com/doc/refman/8.4/en/innodb-transaction-isolation-levels.html), current repeatable/read-committed snapshots and locking/current behavior.
8. Oracle, [MySQL 8.4 InnoDB Multi-Versioning](https://dev.mysql.com/doc/refman/8.4/en/innodb-multi-versioning.html), current transaction/roll-pointer metadata, undo reconstruction, deletion, secondary indexes, and purge.
9. Microsoft, [Transaction Locking and Row Versioning Guide](https://learn.microsoft.com/en-us/sql/relational-databases/sql-server-transaction-locking-and-row-versioning-guide?view=sql-server-ver17), current XSN, active-transaction exclusions, RCSI/SNAPSHOT, version chains, and schema locks.
10. Microsoft, [`sys.dm_tran_transactions_snapshot`](https://learn.microsoft.com/en-us/sql/relational-databases/system-dynamic-management-objects/sys-dm-tran-transactions-snapshot-transact-sql?view=sql-server-ver17), current observation of snapshot transaction sequence numbers and transactions active at capture.

## Exercises

### Exercise 1

Build the full creator/deleter truth table for IDs below, inside-active, inside-completed, and at/above snapshot boundaries, including committed, aborted, active, own-prior, own-later, and rolled-back savepoint cases.

### Exercise 2

Prove the teaching eligibility partition and tuple rule, then identify which facts a complete product algorithm needs beyond `(low,high,active)`.

### Exercise 3

Design a deterministic model-based visibility test harness with snapshot/commit barriers, command IDs, updates/deletes, indexes, cleanup, and crash points plus an independent oracle.

### Exercise 4

Compare statement, transaction, current/locking, exported, and replica snapshots for an order-allocation service and an analytical export. State freshness, blocking, anomaly, and retention tradeoffs.

### Exercise 5

Diagnose an incident where one query sees a deleted row, another misses a committed insert, a locking update uses newer state, and cleanup/version storage grows. Decide expected behavior versus defect and propose evidence/remediation.

## Answers to the Exercises

### Answer 1

For another owner, first require committed. Committed `<low` is eligible; aborted is dead. In `[low,high)`, active-set membership excludes even if the transaction later commits; absence plus committed includes; aborted excludes. `>=high` excludes even if now committed. For a creator, eligible means the version began; for a deleter, eligible means the version ended, so the tuple result is creator-eligible AND NOT deleter-eligible. Own prior command creation is visible and own prior deletion removes the row; later/current-command eligibility follows the engine's command semantics; rolled-back subtransaction work is dead. Boundary tests include `low-1`, `low`, every active/nonactive middle ID, `high-1`, and `high`, with just-before/after outcome publication.

### Answer 2

The numeric regions are disjoint and exhaustive. After committed-status check, the model admits exactly past completed transactions: below low or middle-not-active; it excludes active-at-capture and future. Fixed active membership ensures later commits do not alter S. A tuple exists precisely after visible creation and before visible deletion; other combinations yield never-created or already-ended state. A product additionally needs transaction/subtransaction status and overflow, command IDs/self rules, commit/publication ordering, speculative insert, multitransaction/lock markers, freezing/epochs/wraparound, special snapshots/catalogs, recovery state, version ordering/linkage, index recheck, exported snapshot lifecycle, and cleanup/status retention. PostgreSQL names cannot be copied onto InnoDB/SQL Server algorithms.

### Answer 3

Generate a truth table over regions, active membership, status, creator/deleter role, owner, command order, savepoint outcome, and index path. Maintain a separate interval/reference history from transaction events rather than calling the implementation predicate. Use barriers: hold X4 active, commit X5, capture, commit X4, then assert fixed/new snapshot differences. Cover inserts, update old/new pair, delete, abort, own write/delete, rollback, key change, unique/range constraints, current read, statement/transaction reuse, and snapshot import. Pin snapshot while cleanup runs and assert required tuple/status/index state survives; then release and assert eventual cleanup. Crash before/after tuple, index, commit/status, active-set removal, and cleanup publication; restart and compare oracle. Avoid sleeps and bound hung tests externally without calling timeout a visibility result.

### Answer 4

Order allocation decisions requiring present stock use an atomic constraint/update or locking/current/serializable path; a historical snapshot alone can make stale or write-skewed decisions. Statement snapshots give fresher successive reads but the order view can change; transaction snapshot repeats one cut but pins history and remains stale. Current locking reads wait/deadlock yet reserve relevant rows/ranges. Exported snapshots can coordinate parallel analytical workers at one source cut but require import ordering and keep the exporter/pin alive. Replica snapshots offload reads but need apply/safe-position and read-your-writes/session guarantees; otherwise they are correct locally yet stale. For a long export, consider materializing a point-in-time copy or replica safe timestamp to release primary history, while recording snapshot/log handoff for completeness.

### Answer 5

Reconstruct each query's engine/version, isolation, snapshot capture/lifetime, transaction/command, read type, creator/deleter/outcomes at capture, index/plan, replica position, and own writes. The deleted row can be expected if deleter was active/future in its snapshot. The committed insert can be correctly absent if commit followed capture. The locking update may intentionally read current state, yielding a mixed local view. Those are defects only if they violate the configured promise or tuple/status/index paths disagree. Growth may follow the long snapshot/export/replica pin. Validate native status/graph/version evidence carefully because current monitoring races with historical capture. If expected but harmful, choose fresher/locking/serializable semantics, shorten/materialize snapshots, and bound pins. If defective, preserve evidence, stop unsafe cleanup, repair publication/status/index/recovery logic, and test exact boundary schedule. Across PostgreSQL, InnoDB, and SQL Server map native fields separately; verify final business invariants and no required version was reclaimed.
