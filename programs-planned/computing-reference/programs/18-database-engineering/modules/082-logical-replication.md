---
module_id: DBE-082
program: Database Engineering
level: 2
module_number: 82
title: Logical Replication
status: complete
last_verified: 2026-09-05
---

# Logical Replication

## One-Page Review

### Governing question

How can a database publish selected committed meaning—not storage bytes—to independently evolving consumers while preserving transaction boundaries, row identity, ordering, schema interpretation, restartability, and explicit conflict policy?

### Essential definitions

**Logical replication** extracts database changes as logical operations or row events and applies or consumes them independently of source page layout. A **publication** declares eligible objects and operations; a **subscription** records consumer intent and progress. A **change event** describes an insert, update, delete, truncate, or schema event. **Replica identity** is the information needed to locate the pre-existing target row for update or delete. A **snapshot** supplies initial state; a **change position** orders later events in one source history. An **origin** identifies where a transaction arose. A **transaction envelope** groups events with one atomic commit decision. A **tombstone** or delete event represents removal. **Apply idempotence** makes a retry converge without duplicating an effect. A **dead-letter path** preserves rejected events for governed diagnosis rather than silently losing them.

### Central model, mechanism, or theorem

Let snapshot $S$ be consistent at source position $p_S$, and let $L(p_S,p]$ be a complete ordered suffix of committed logical transactions after that cut. For a deterministic apply function $A$ and compatible schema mapping $M$,

$$
T_p=A(M(S),M(L(p_S,p]))
$$

is a faithful target projection through $p$ only if the snapshot and stream form one gap-free history, transaction boundaries are preserved at the promised scope, every mutable row has stable identity, transformations are deterministic, retries are idempotent or deduplicated, and conflicts follow an explicit policy. Transporting every event is insufficient if its meaning changes under target schema, collation, constraints, triggers, privileges, or local writes.

### Critical invariants

- The initial snapshot and change stream meet at one declared cut: no committed change is omitted or applied twice semantically.
- A publication includes exactly the intended tables, columns, rows, and operation types; filters are tested at boundaries.
- Updates and deletes carry a stable replica identity valid under the source and target key semantics.
- Events retain source history, transaction identity, per-transaction order, schema version, and commit evidence.
- The durable consumer checkpoint never advances beyond atomically applied or durably staged work.
- Retried transactions converge through idempotent effects or a durable deduplication key.
- Schema changes are gated by compatibility rather than interpreted against whichever target schema happens to exist.
- Local target writes, multiple sources, and loops require ownership, conflict, and origin-suppression rules.
- Acknowledgement, transport, apply, query visibility, and business correctness remain separate frontiers.

### Common failures

Failures include starting a snapshot without retaining its change suffix; using mutable or nullable row identity; splitting a source transaction and exposing half of it; advancing the checkpoint before target commit; assuming delivery means exactly-once effect; retrying non-idempotent increments; applying an event under the wrong schema version; omitting deletes; re-firing unsafe target triggers; filtering parent and child rows inconsistently; allowing writes on both sides without conflict ownership; losing large-transaction spill state; creating a replication loop; logging sensitive before-images unnecessarily; and calling a row-count match semantic equality.

### Compact example

A snapshot represents source position 40 and contains account A with balance 100. Transaction 41 changes A to 80 and inserts ledger row L1; transaction 42 changes A to 70. If a consumer commits transaction 41 atomically and only then checkpoints 41, a crash before transaction 42 can safely resume from 41. If it checkpoints 41 after applying the balance but before L1, restart skips part of the transaction and violates the target invariant even though the position appears current.

### Connections

Retrieve [Write-Ahead Logging](072-write-ahead-logging.md), [Log Sequence Numbers](073-log-sequence-numbers.md), [Physical and Logical Backup](079-physical-and-logical-backup.md), and [Physical Replication](081-physical-replication.md). Continue through [the program roadmap](../ROADMAP.md) to acknowledgement modes, lag and stale reads, failover, sharding, distributed transactions, and consistency trade-offs.

## Governing Question

Physical replication asks whether another compatible engine can replay the same storage history. Logical replication asks a different question: which committed facts or operations should cross a boundary, in what representation, and under whose semantics? That boundary may connect major database versions, platforms, schemas, services, analytics stores, search indexes, caches, or audit processors.

The freedom to transform and select data is valuable precisely because it weakens implicit guarantees. The source page format no longer constrains the target, but row identity, data types, transaction grouping, schema evolution, filtering, triggers, and conflicts become explicit protocol concerns. A sound design names the promised projection and the evidence required to reconstruct it.

## Why This Matters

Logical replication supports online upgrades, selective read replicas, data integration, service extraction, regional subsets, operational analytics, and change-data-capture pipelines. It can avoid copying physical bloat or engine-private structures and can cross platform or major-version boundaries when the logical type and protocol compatibility permit it.

It is not automatically more correct or more available than physical replication. Decoding consumes retained log; slow consumers can exhaust source storage. A logical stream can omit DDL, large objects, sequences, permissions, or unselected tables. Destination constraints and triggers can stop apply. Two sources can legitimately produce incompatible updates. A consumer can report a high position while its materialized view is wrong because a transform changed, a delete was discarded, or a checkpoint outran commit.

Current PostgreSQL 18 documentation describes publication/subscription logical replication, initial table synchronization, replica identity, conflict reporting, monitoring, security, and cross-version uses. It preserves transactional ordering within a subscription but documents important restrictions and conflict behavior. Current MySQL 8.4 documentation distinguishes statement-, row-, and mixed-format binary logging; row format is the default, and the `binlog_format` control is deprecated in favor of row-based setups for new replication. These are current product facts, not universal definitions of logical replication.

## Prerequisites and Retrieval

Retrieve these concepts before designing a logical stream:

- WAL or another commit log must record enough information to reconstruct the promised logical operation;
- an LSN, GTID, offset, or sequence is meaningful only with its source history and position semantics;
- MVCC defines the snapshot cut and which transaction versions are visible;
- primary, unique, natural, and surrogate keys have different stability and null semantics;
- a transaction is atomic at the source, while a transport batch is merely a delivery unit;
- durability of a source commit, durability of an event, target apply, and target visibility are different events;
- schema constraints, collations, generated columns, triggers, defaults, and permissions participate in apply semantics;
- retries require idempotence or durable deduplication;
- retention is a capacity obligation owned by a named consumer;
- authentication, authorization, encryption, minimization, and audit apply to both snapshots and streams.

[Physical Replication](081-physical-replication.md) established typed receive, flush, replay, and visible frontiers. Logical replication retains that discipline but replaces page/history compatibility with a logical contract over identity, schema, projection, transaction envelopes, and transformations.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish logical row, statement, transaction, and schema events from physical log records;
2. define a publication contract over tables, columns, rows, operations, histories, and security principals;
3. join an initial snapshot to a retained change stream without gaps or semantic duplicates;
4. preserve transaction atomicity and ordering at an explicitly chosen scope;
5. select and validate replica identity for inserts, updates, deletes, and key changes;
6. design checkpoint, retry, deduplication, and poison-event behavior;
7. govern schema evolution, transformations, triggers, constraints, and target-local writes;
8. validate logical replication with independent state, transaction, history, and failure oracles.

## Core Exposition

**Define the replicated contract.** Name the source database and history, publication, selected relations, row predicates, projected columns, operation types, transaction scope, ordering scope, data classification, target mapping, and consumers. “Replicate orders” is incomplete: does it include deletes, line items, sequence state, status-history rows, tenant moves, DDL, and transactions that touch both selected and unselected objects?

A publication is policy, not a copy of source storage. Row filters can reduce scope, but a filter evaluated after an update can make a row appear or disappear and therefore translate one source update into a target insert or delete. Column projection can remove data a target constraint, identity, or transform needs. Treat the publication definition and its version as governed schema.

**Choose the event representation.** Statement events are compact and preserve source intent, but they depend on deterministic functions, session state, SQL semantics, collation, time zone, data, optimizer-independent behavior, and target compatibility. Row events describe before/after values or changed columns and avoid re-evaluating nondeterministic predicates, but can be larger and can conceal the original intent. Operation events at a domain boundary can be durable but require an application-owned outbox and carefully coupled source transaction.

Logical decoding converts physical commit-log information into a plugin/protocol representation. Decoding correctness depends on the log containing sufficient before/after identity, transaction and schema context. Decoding is not the same as publication filtering, network delivery, target apply, or business interpretation; measure each stage.

**Create a gap-free snapshot-to-stream handoff.** Establish a source-consistent snapshot at position $p_S$ while retaining all required change history after $p_S$. Register the consumer or slot before history can be recycled. Export the snapshot or capture tables using the engine's supported protocol. Transfer, transform, and validate it. Then apply the complete committed suffix strictly after the snapshot boundary.

Taking a table dump and later asking for “changes since around then” is not a protocol. Transactions concurrent with the dump can be missed or duplicated across tables. Per-table snapshot workers may complete at different times, so the coordinator must preserve a common logical cut or explicitly model table-specific states and buffered changes.

**Preserve transaction envelopes.** An event should carry source history, transaction ID, event sequence, commit position/time, relation identity, schema version, operation, replica identity, before/after values as promised, and origin. Consumers may stream a large transaction incrementally to bound memory, but should not expose it as committed until the source commit decision arrives. Spill buffers must survive crashes or be reconstructible.

The ordering guarantee must be exact. One source stream may promise a total commit order. Parallel apply may preserve conflicts and per-key order while relaxing global completion order. Multiple sources have no inherent total order; timestamps alone do not create one. A target that requires cross-source invariants needs ownership, causal metadata, or a coordination protocol beyond ordinary logical replication.

**Make row identity explicit.** Inserts create a new identity. Updates and deletes must locate the intended current row. A primary key is usually best, but only if immutable enough for the protocol, semantically equal at both ends, and included in the event. A unique index with nullable columns or different collation can fail to identify the same row. Full-row before-images may work when no stable key exists, but are larger, expose more data, and can fail after target-local changes.

A key-changing update needs old identity to locate the row and new identity to establish its next address. Do not model it as an update containing only the new key. Validate duplicate keys, missing target rows, nulls, collation differences, and key reuse after deletion.

**Couple apply and checkpoints.** Let $C_a$ be the greatest source transaction durably and atomically applied to the target and $C_k$ the durable consumer checkpoint. Safety requires $C_k \le C_a$. Advancing the checkpoint first creates omission after crash. Applying first and checkpointing later creates retry; therefore effects must be idempotent or deduplicated.

When the destination supports transactions, write target changes and a source-position/deduplication record in the same target transaction. When it does not, use conditional writes keyed by source event identity, a durable inbox, or a rebuildable idempotent materialization. “Exactly once” must name the boundary: delivery, target transaction, or externally visible side effect. Sending an email or charging a card cannot be rolled back merely because a database checkpoint is transactional.

**Separate correctness from liveness.** A poison event may violate a constraint, reference a missing row, use an unknown schema, exceed a size limit, or fail a transform. Retrying forever preserves order but halts progress. Skipping restores liveness but creates a known hole. A governed dead-letter path retains the original event, source position, error, schema, attempt history, and authorization for replay or compensating repair. Never silently advance across failure.

**Govern schema evolution.** Every event must be interpreted under the schema that encoded it. Classify changes:

- additive nullable columns can often be tolerated by older consumers;
- adding a required target column without a deterministic default can stop apply;
- renames look like drop-plus-add without stable column identity;
- type widening may be safe while narrowing can reject or truncate;
- collation, time-zone, numeric, enum, and encoding changes can alter meaning;
- identity changes require a coordinated transition carrying old and new keys;
- DDL replication support is product-specific and frequently incomplete.

Use schema versions and compatibility gates. A dual-read/dual-write transition or backfill may be needed, but its concurrency cut must be designed like the initial snapshot. Pause, quarantine, or route unknown versions; do not guess.

**Control target semantics.** Decide whether target triggers, generated values, defaults, foreign keys, row-level security, and auditing execute during apply. Re-firing business triggers can duplicate side effects. Disabling all constraints can admit impossible state. The apply identity should have only necessary rights, and permission changes must be tested as part of deployment.

Logical replicas are often independently writable, but then source-of-truth ownership is no longer implicit. Single-writer tables are simplest. Multi-source or bidirectional designs need disjoint ownership or a deterministic conflict policy using versions, origins, and domain rules. Last-writer-wins based on unsynchronized wall clocks can lose valid work. Blind loop prevention based only on payload equality fails when transformations alter payloads; carry origin and causal identity.

**Operate retention and backpressure.** A logical slot or equivalent protects the oldest source history a consumer may need. Track confirmed position, restart position, retained bytes, decode/apply rates, transaction age, spill bytes, last heartbeat, and owner. A stopped consumer can pin log indefinitely. Capacity policy should alert, throttle, archive, invalidate, or reseed explicitly—never discard required log while claiming continuity.

Large transactions, long-running source transactions, wide rows, and bursts can dominate retention and memory. Backpressure at the consumer may propagate to source disk even if ordinary event lag seems small. Exercise full disks, slot loss, consumer replacement, and resnapshot time.

**Secure meaning, not only transport.** A logical event can expose deleted values, before-images, tenant identifiers, secrets, or columns excluded from normal query roles. Minimize publication fields, encrypt transport and retained queues, segregate credentials, audit subscription changes, rotate keys, constrain network paths, and define deletion/retention policy for snapshots, spill files, dead letters, and backups.

**Validate with independent oracles.** Verify publication membership, snapshot cut, complete transaction sequences, identities, schema versions, transformations, constraint behavior, origin handling, and checkpoint coupling. Compare keyed rows and normalized values rather than counts alone. Recompute aggregates and referential invariants. Trace sample source transactions end to end.

Cut processes and connectivity before and after decode, delivery, staging, target write, target commit, and checkpoint. Inject duplicates, gaps, reordering, unknown schemas, key changes, deleted/missing rows, constraint conflicts, target-local writes, loops, full disks, slot invalidation, long and huge transactions, and credential rotation. State exactly which failure model and projection passed.

The executable model below applies transaction envelopes to a small target and atomically advances its checkpoint. Duplicate delivery converges because each transaction ID is recorded with the state update. It is a finite semantic model, not a database, decoder, network, or external-side-effect test.

<!-- bijux-verify: {"id":"logical-transaction-apply","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"snapshot_position=40\ncheckpoint=42\naccount_A=70\nledger_rows=1\napplied_transactions=2\nduplicate_effect=false\nunknown_schema_rejected=true\nevidence=finite_logical_transaction_apply\n","stderr":""}} -->
```python
target = {"accounts": {"A": 100}, "ledger": {}, "checkpoint": 40, "seen": set()}

transactions = [
    {"id": "tx-41", "position": 41, "schema": 3,
     "events": [("set_balance", "A", 80), ("insert_ledger", "L1", 20)]},
    {"id": "tx-42", "position": 42, "schema": 3,
     "events": [("set_balance", "A", 70)]},
]

def apply_transaction(state, tx):
    if tx["schema"] != 3:
        raise ValueError("unknown schema")
    if tx["id"] in state["seen"]:
        return False
    # Copying models one atomic destination transaction.
    accounts = dict(state["accounts"])
    ledger = dict(state["ledger"])
    for operation, key, value in tx["events"]:
        if operation == "set_balance":
            accounts[key] = value
        elif operation == "insert_ledger":
            if key in ledger:
                raise ValueError("duplicate ledger identity")
            ledger[key] = value
        else:
            raise ValueError("unknown operation")
    state["accounts"] = accounts
    state["ledger"] = ledger
    state["seen"].add(tx["id"])
    state["checkpoint"] = tx["position"]
    return True

for transaction in transactions:
    apply_transaction(target, transaction)
duplicate_effect = apply_transaction(target, transactions[0])
try:
    apply_transaction(target, {"id": "tx-43", "position": 43,
                               "schema": 4, "events": []})
    unknown_schema_rejected = False
except ValueError:
    unknown_schema_rejected = True

print("snapshot_position=40")
print(f"checkpoint={target['checkpoint']}")
print(f"account_A={target['accounts']['A']}")
print(f"ledger_rows={len(target['ledger'])}")
print(f"applied_transactions={len(target['seen'])}")
print(f"duplicate_effect={str(duplicate_effect).lower()}")
print(f"unknown_schema_rejected={str(unknown_schema_rejected).lower()}")
print("evidence=finite_logical_transaction_apply")
```

## Definitions and Notation

- $H$: one source history or database incarnation.
- $S$: consistent initial snapshot.
- $p_S$: source change position associated with $S$.
- $L(p_S,p]$: complete ordered committed transaction suffix after the snapshot through position $p$.
- $M$: declared schema and data transformation from source events to target meaning.
- $A$: deterministic target apply function under the declared conflict policy.
- $C_a$: greatest source transaction durably and atomically applied.
- $C_k$: durable consumer checkpoint; safety requires $C_k \le C_a$.
- **Publication:** governed selection of objects, rows, columns, and operations exposed by a source.
- **Subscription:** consumer identity, publication binding, start state, configuration, and progress.
- **Replica identity:** stable old-row information used to find the target of update or delete.
- **Transaction envelope:** ordered events plus source transaction identity and commit decision.
- **Origin:** identity of the system or stream where a change first arose.
- **Idempotence:** repeating an operation has the same relevant effect as applying it once.
- **Deduplication key:** durable event or transaction identity used to suppress a retry.
- **Projection oracle:** independent comparison of the promised target subset and transformation, not all source storage.

## Mechanisms, Invariants, or Proof Structure

**Snapshot-suffix theorem.** Assume $S$ is a consistent snapshot of the selected source projection at $p_S$; retention preserves every committed transaction after that cut; decoding and filtering are complete for the declared publication; $M$ is deterministic and compatible; and $A$ preserves required transaction boundaries. Applying exactly the suffix $L(p_S,p]$ yields the declared projection through $p$. Removing the common cut permits omissions or duplicates, so a dump plus an approximate timestamp does not satisfy the premises.

**Checkpoint safety.** If $C_k>C_a$, a crash can resume after unapplied work, causing permanent omission. If $C_k<C_a$, retry occurs; idempotence or deduplication is therefore required. Atomic target state plus checkpoint commit establishes both inequalities at transaction granularity for that destination, but says nothing about nontransactional external effects.

**Identity invariant.** An update/delete event is deterministic only if its old identity selects exactly the intended target row under target equality semantics. Missing, multiple, or semantically different matches are conflicts, not permission to guess. A changing key requires both old lookup identity and new value.

**Ordering invariant.** Events within one transaction preserve source program order, and visibility follows the source commit decision. Parallelism is safe only when dependency analysis proves commutativity or preserves all conflicting-key and transaction constraints. Commit timestamps from multiple sources do not establish a trusted total order by themselves.

**Schema interpretation invariant.** Payload fields are decoded and transformed according to their recorded schema/protocol version. Compatibility is a predicate over source encoding, publication, consumer, target schema, types, constraints, and transformations—not merely matching column names.

**Loop and conflict invariant.** A change crossing multiple writable systems retains origin/causal identity. Each table or domain has an ownership/conflict policy. Suppression prevents re-emission of the same causal change without discarding a later legitimate update that happens to have equal values.

## Alternatives and Trade-Offs

| Design | Advantage | Cost or risk | Required evidence |
| --- | --- | --- | --- |
| Statement events | compact; preserves intent | nondeterminism and environment coupling | deterministic replay tests |
| Full row before/after images | simple consumer reconstruction | bandwidth and sensitive-data exposure | identity and minimization review |
| Changed columns plus key | smaller events | target needs compatible prior state | divergence and missing-row tests |
| Database-native publication | transactional source integration | engine-specific semantics and limits | versioned vendor protocol tests |
| Transactional outbox | domain-shaped events coupled to commit | application/schema ownership burden | commit and relay failure cuts |
| One ordered apply worker | straightforward transaction order | throughput bottleneck | backlog and recovery benchmarks |
| Parallel apply | higher throughput | dependency and visibility complexity | conflicting-key/transaction tests |
| Target transaction plus checkpoint | strong local retry boundary | unavailable for some sinks | crash-cut tests |
| Durable inbox/deduplication | supports nontransactional apply | storage, retention, key design | duplicate and expiry tests |
| Read-only subscriber | avoids local data conflicts | less autonomy | write-prevention evidence |
| Bidirectional writes | locality and availability | conflicts, loops, ownership ambiguity | partition/merge adversarial tests |
| Resnapshot after history loss | restores a known base | cost and replacement cut | snapshot-stream handoff drill |

## Failure Modes and Misconceptions

- **“Logical means SQL statements.”** Logical streams may carry rows, operations, or domain events; statement replay is only one representation.
- **“A primary key always solves identity.”** Key changes, collation differences, null semantics, partial indexes, or omitted columns can still break lookup.
- **“At-least-once delivery duplicates data.”** It duplicates delivery; a correct idempotent or deduplicating apply can preserve one semantic effect.
- **“Exactly once is end to end.”** A transactional sink boundary does not include an email, payment, cache, or downstream system unless those effects share a proven protocol.
- **“The snapshot can finish before the slot starts.”** Without retaining the suffix from the snapshot cut, concurrent commits can be lost.
- **“Global position proves every table is current.”** A table can be unsynchronized, filtered, blocked by conflict, or interpreted under the wrong schema while another worker advances.
- **“Row counts prove equality.”** Counts miss wrong values, swapped identities, missing deletes balanced by extra inserts, constraint drift, and transformation errors.
- **“DDL follows DML automatically.”** Schema propagation is product-specific; incompatible target DDL can stop or corrupt meaning.
- **“Target triggers are harmless.”** They can duplicate derived rows and external effects or reject valid source operations.
- **“Last writer wins resolves conflicts.”** It discards one write and depends on a trustworthy order; wall-clock timestamps commonly fail that requirement.
- **“A dead-letter queue fixes poison events.”** It preserves evidence; the target remains incomplete until governed repair/replay closes the hole.
- **“Deleting a stalled slot is cleanup.”** It may destroy incremental continuity and force a resnapshot.
- **“A logical replica is a backup.”** It may omit objects, history, deletes, permissions, or corruption-free recovery evidence.
- **“Encryption protects all copies.”** Snapshot files, decoder spill, queues, logs, dead letters, and target storage also require controls.

## Worked Examples

### Example 1

**Situation.** Snapshot $S$ is exported at position 500. Transactions 501 and 502 commit while the copy runs. Which events are applied after loading $S$?

**Reasoning.** The snapshot already contains all selected commits visible at 500 and none after it. The source must retain the suffix while copying. Apply transactions with positions in $(500,p]$, beginning at 501, in declared order. Starting at 502 loses transaction 501; starting at 500 and interpreting the boundary inclusively can duplicate the transaction represented by 500.

**Conclusion.** A typed exclusive snapshot boundary plus retained complete suffix prevents the snapshot/change race.

### Example 2

**Situation.** A source update changes customer email from `a@example.test` to `b@example.test`. The stream contains only the new row, and email is the target lookup key.

**Reasoning.** Looking up the new email finds no row, so the consumer cannot know which old row to update. Treating the event as insert may create a duplicate. The event needs an immutable customer ID or both old and new identity. A full before-image is an expensive fallback and still depends on equal target values.

**Conclusion.** Mutable after-values alone do not provide replica identity for a key-changing update.

### Example 3

**Situation.** One transaction debits account A by 20 and inserts ledger row L1. The target exposes the debit before the ledger insert arrives.

**Reasoning.** Transport frames may split the transaction, but target visibility must follow the promised transaction envelope. Stage both events, validate the source commit, apply them in one target transaction, then advance the checkpoint. Otherwise a reader observes a balance without its audit fact and a crash can make the split permanent.

**Conclusion.** Streaming a large transaction incrementally is compatible with bounded memory only if commit visibility remains atomic.

### Example 4

**Situation.** Transaction 41 commits at the target, but the consumer crashes before writing a separate checkpoint. Delivery resumes at 41.

**Reasoning.** The event is expected to repeat. If the target transaction also wrote deduplication key `(source-H, tx-41)`, the retry sees it and performs no second effect. If the event said “increment balance by 20” without deduplication, retry corrupts state. An absolute row image may be naturally idempotent only if no conflicting target write occurred.

**Conclusion.** Apply-before-checkpoint requires durable idempotence or deduplication; retry is not exceptional.

### Example 5

**Situation.** Schema 3 records `amount_cents` as integer. Schema 4 replaces it with decimal `amount` in currency units. A schema-3 consumer receives a schema-4 payload containing `12.50`.

**Reasoning.** Interpreting the field as integer cents either fails or silently changes 12.50 currency units into 12.5 cents. The consumer must reject/quarantine unknown schema 4 or route it through a tested converter. Column-name similarity is not compatibility evidence.

**Conclusion.** Schema identity is part of an event's meaning and must gate apply.

### Example 6

**Situation.** A publication includes orders where `region='EU'`. An update moves order 7 from `US` to `EU`; another moves order 8 from `EU` to `US`.

**Reasoning.** Evaluating only post-update rows emits order 7 but could omit the removal of order 8. The logical protocol must define transition semantics: nonmember-to-member becomes insert, member-to-nonmember becomes delete, and member-to-member becomes update. It needs old membership information to decide correctly.

**Conclusion.** Row filters are state-transition rules, not merely predicates over emitted after-images.

### Example 7

**Situation.** Subscriber table already contains local row key 9. The source sends an insert for key 9 with different values.

**Reasoning.** Applying violates uniqueness. Blind overwrite hides a local/source ownership conflict; blind skip creates a missing source fact. Stop or quarantine according to policy, retain source position and both versions, identify the authorized owner, repair state, then replay. PostgreSQL 18 documents `insert_exists` and other logical-replication conflict classes and reports them through subscription statistics/logging.

**Conclusion.** A uniqueness error is semantic conflict evidence and needs governed resolution.

### Example 8

**Situation.** Source executes `UPDATE jobs SET token = random()` for 1,000 rows.

**Reasoning.** Replaying the statement independently produces different random values and can select a different affected set under changed data or semantics. Row events carry the resulting values and identities, increasing log volume but preserving the source outcome. MySQL documents nondeterministic-statement hazards and uses row-based logging by default in 8.4.

**Conclusion.** Row events trade size for independence from re-evaluating nondeterministic source execution.

### Example 9

**Situation.** A consumer is down for six hours. The source produces 40 GiB/hour, the slot already retains 30 GiB, and only 220 GiB of safe headroom remains.

**Reasoning.** Six more hours produce about $6\times40=240$ GiB, so headroom exhausts before recovery if the rate persists. Time to exhaustion is $220/40=5.5$ hours. Operators must restore consumption sooner, add governed capacity, use an independent archive, or invalidate and resnapshot. Silently recycling the slot's history violates continuity.

**Conclusion.** Consumer liveness creates a quantified source-storage obligation; current lag alone is not sufficient.

### Example 10

**Situation.** Systems A and B both publish the same table. A-origin transaction x reaches B, whose capture process sees the applied row and republishes it to A.

**Reasoning.** Payload equality is unreliable because transforms and later legitimate equal-valued writes exist. Preserve origin `A` and causal transaction ID `x`; B records the apply origin and excludes re-emission of the same causal change. Independently, ownership/conflict rules decide whether B-origin edits to that row are permitted. Loop suppression does not resolve concurrent writers.

**Conclusion.** Origin tracking prevents causal echo; deterministic ownership or conflict resolution is still required.

## Cross-Program Connections

- Data Engineering owns downstream pipeline orchestration, delivery operations, and analytical data-product processing; this module owns the database's logical publication and apply contract.
- Data Architecture Engineering owns enterprise data semantics, governance, lineage, and modeled integration boundaries; logical events must carry enough identity and schema lineage to support them.
- Distributed Systems owns general causal order, consensus, replicated-state-machine, and failure-detector theory; database logical replication instantiates narrower guarantees over committed changes.
- API and Service Engineering owns public service contracts and idempotency keys at request boundaries; logical replication uses analogous identities but must preserve database transaction and schema semantics.
- Software Delivery and Reliability Engineering owns deployment orchestration and rollback practice; schema compatibility gates turn those practices into safe producer/consumer evolution.
- Security Engineering owns broader threat models and control systems; logical streams add sensitive before-images, retained histories, apply privileges, and cross-boundary data minimization concerns.

## References

1. PostgreSQL Global Development Group. [PostgreSQL 18: Logical Replication](https://www.postgresql.org/docs/18/logical-replication.html), including architecture, publications, subscriptions, restrictions, conflicts, monitoring, security, and upgrade guidance. Current major-version documentation checked 2026-09-05.
2. PostgreSQL Global Development Group. [PostgreSQL 18: Logical Decoding Concepts](https://www.postgresql.org/docs/18/logicaldecoding-explanation.html). Current documentation checked 2026-09-05.
3. PostgreSQL Global Development Group. [PostgreSQL 18: Publication](https://www.postgresql.org/docs/18/sql-createpublication.html) and [Subscription](https://www.postgresql.org/docs/18/sql-createsubscription.html) commands. Current filter, identity, privilege, and option semantics checked 2026-09-05.
4. PostgreSQL Global Development Group. [PostgreSQL 18: Logical Replication Conflicts](https://www.postgresql.org/docs/18/logical-replication-conflicts.html). Current conflict categories and resolution behavior checked 2026-09-05.
5. PostgreSQL Global Development Group. [PostgreSQL 18: Monitoring Logical Replication](https://www.postgresql.org/docs/18/logical-replication-monitoring.html). Current worker and subscription views checked 2026-09-05.
6. Oracle. [MySQL 8.4 Reference Manual: Binary Logging Formats](https://dev.mysql.com/doc/refman/8.4/en/binary-log-formats.html) and [Replication Implementation](https://dev.mysql.com/doc/refman/8.4/en/replication-implementation.html). Current row/statement/mixed behavior checked 2026-09-05.
7. Oracle. [MySQL 8.4 Reference Manual: Binary Logging Options and Variables](https://dev.mysql.com/doc/refman/8.4/en/replication-options-binary-log.html). Current row-format default and `binlog_format` deprecation checked 2026-09-05.
8. Jim Gray and Andreas Reuter. *Transaction Processing: Concepts and Techniques*. Morgan Kaufmann, 1993. Transaction, recovery, logging, and replication foundations.
9. Philip A. Bernstein and Eric Newcomer. *Principles of Transaction Processing*, 2nd ed. Morgan Kaufmann, 2009. Transactional messaging, recovery, and distributed transaction foundations.
10. Pat Helland. [Life beyond Distributed Transactions: An Apostate's Opinion](https://dl.acm.org/doi/10.1145/3012426.3025012). CIDR 2007; ACM Queue reprint, 2016. Identity, idempotence, and application-level consistency perspective.

## Exercises

### Exercise 1

Distinguish publication, subscription, replica identity, transaction envelope, and checkpoint. For each, state one correctness failure caused by omitting it.

### Exercise 2

A snapshot at position 90 contains row K=`old`. Transaction 91 changes K to `new`; transaction 92 inserts J. The consumer applies 91 and commits it but crashes before its separate checkpoint (still 90). It has a durable transaction deduplication table. Trace safe recovery through position 92.

### Exercise 3

A pipeline advances its source checkpoint when it places individual row events on a queue. It applies four workers in parallel, fires ordinary target triggers, and records no transaction ID, schema version, or origin. Identify at least five independent failure modes and propose a minimum corrective design.

### Exercise 4

Compare statement events and row before/after events for cross-major-version replication of a workload containing nondeterministic functions, large bulk updates, sensitive columns, and frequent schema changes. Recommend a default and define exceptions and evidence.

### Exercise 5

Design a logical replication contract from an orders database to a search index that has no multi-document transaction and may return success before replicas expose a write. Include snapshot handoff, identity, deletes, schema evolution, retry, checkpoint, external visibility, poison events, and validation.

## Answers to the Exercises

### Answer 1

A **publication** selects the source objects, rows, columns, and operations; omitting it permits accidental overexposure or an incomplete projection. A **subscription** binds a consumer to a publication and records start/configuration/progress; omitting it loses durable consumer intent and restart state. **Replica identity** locates the old target row for update/delete; omitting it makes those operations ambiguous or turns them into duplicate inserts. A **transaction envelope** groups ordered events under one source commit; omitting it exposes partial transactions. A **checkpoint** records the durable consumed position; omitting it forces uncontrolled replay or loss. Full credit distinguishes these responsibilities rather than describing all five as “offset metadata.”

### Answer 2

On restart, read checkpoint 90 and request the suffix beginning after 90. Transaction 91 is delivered again. In one target transaction, check the durable deduplication key for its source history and transaction ID. Because 91 is present, perform no row mutation and advance the checkpoint safely to 91 (or confirm that the existing atomic record already associates its state with 91). Then apply transaction 92, record its deduplication key and checkpoint 92 atomically, and commit. Verify K=`new`, J exists once, both source transaction IDs exist once, and checkpoint=92. Deduplication must be retained long enough to cover every possible retry; expiring 91 before the source can no longer resend it reintroduces risk.

### Answer 3

Independent failures include: queue acknowledgement can outrun target apply and lose work; row-level publication destroys source transaction atomicity; parallel workers can reorder conflicting keys; retries cannot be deduplicated without transaction/event identity; unknown payloads can be interpreted under the wrong schema; target triggers can duplicate derived rows or external effects; missing origin permits loops; and a poison event can be skipped invisibly if the queue offset advances.

A minimum correction carries source history, transaction ID, event order, commit position, schema version, identity, operation, and origin in transaction envelopes. Stage complete transactions, partition/serialize conflicts, apply each target transaction with its deduplication record and checkpoint atomically, suppress causal re-emission, gate schemas, explicitly control triggers/constraints, and quarantine poison events without advancing the contiguous completed frontier. If the queue cannot represent transactions, add a durable coordinator/inbox that can.

### Answer 4

Row events are the safer default because they preserve chosen source results rather than re-evaluating nondeterministic functions under different versions, data, sessions, collations, or optimizers. They can make a large bulk update expensive and may expose sensitive before-images; minimize columns, encrypt/authorize retention, and use changed-column images where identity and prior-state assumptions are proven. Statement events may be acceptable for narrowly classified deterministic, version-compatible operations when replay tests cover functions, session state, collation, time zone, and failure retries. Frequent schema change requires versioned payloads and compatibility gates in either design; row format does not solve DDL evolution. Evaluation should include byte/event rates, semantic state comparison, nondeterministic cases, schema transitions, retry cuts, and data-exposure review.

### Answer 5

Register retention and capture a consistent orders snapshot at position $p_S$; bulk-index that projection while buffering the complete suffix after $p_S$. Use immutable order ID as document identity and source history plus transaction/event ID as the deduplication key. Translate inserts/updates into conditional document versions and deletes into durable tombstones so retries converge and late events cannot resurrect removed orders.

Because the index lacks multi-document transactions, define the promise as per-document convergence, not source-transaction atomic visibility. Persist events in an inbox and advance the source checkpoint only after every event in the transaction is durably accepted with a conditional version; separately track the index's query-visible frontier because write acceptance is not search visibility. Carry schema version, route only compatible events, and quarantine unknown or rejected events with their positions while blocking the contiguous completion frontier. Validate with a snapshot/suffix reconciliation, keyed document/value comparison, delete tests, duplicate/reordering and crash injection, schema-transition tests, poison-event replay, and queries proving visibility through a declared bound. An acceptable alternative rebuilds the whole index generation and atomically swaps an alias, provided it retains the suffix and proves the swap cut.
