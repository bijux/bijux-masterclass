---
module_id: DBE-019
program: Database Engineering
level: 1
module_number: 19
title: Data Modification and Upsert
status: complete
last_verified: 2026-08-30
---

# Data Modification and Upsert

## One-Page Review

### Governing question

How can a database modification select exactly the intended rows, enforce identity and transition invariants atomically, survive concurrency and retries, and return evidence of what actually changed?

### Essential definitions

An **affected-row set** is the target rows actually inserted, updated, or deleted. An **arbiter** is the unique constraint or index that decides whether a proposed insert conflicts. An **upsert** atomically chooses an insert or conflict action under a named identity rule. **Idempotency** means repeating the same logical request has the same durable effect; an idempotency key must be bound to the request payload and result. **Optimistic concurrency control** updates only a row at an expected version. A **lost update** occurs when one writer overwrites another without detecting the intervening change. `RETURNING`-like facilities expose database-computed post-action evidence where supported.

### Central model, mechanism, or theorem

Treat a write as a guarded state transition `W:(S,request)->(S',outcome)`. The guard includes authorization, tenant, identity, expected version, lifecycle state, and constraints. Atomicity requires the guard and transition to occur in one database statement or transaction. An upsert is correct only if the arbiter equals business identity and its update function is valid for conflicts. Retry safety requires a unique token `k` with a canonical request digest: the first committed request records `(k,digest,outcome)`; an identical retry returns the recorded outcome; token reuse with another digest fails.

### Critical invariants

- Every modification has an explicit target table, column list, tenant scope, and expected affected cardinality.
- Database constraints enforce business identity; a read-then-write precheck is not concurrency control.
- Upsert names or deliberately infers the correct arbiter and defines insert, update, no-op, stale, and conflict outcomes.
- Version/state predicates are evaluated atomically with the update.
- Retry tokens are unique and payload-bound; “duplicate key” is not automatically a successful replay.
- Defaults, generated values, triggers, cascades, and partition routing are included in returned/audit evidence.
- Multirow source duplicates cannot affect one target ambiguously.
- Deadlocks, serialization failures, timeouts, uncertain commits, and retries have bounded documented handling.

### Common failures

Failures include omitting a WHERE clause, trusting a pre-count that races, updating by nonunique business fields, using an upsert arbiter unrelated to domain identity, overwriting newer versions with stale events, incrementing a counter through read-modify-write, treating MySQL `REPLACE` as an update, assuming affected-row counts have portable meanings, using one idempotency token for different payloads, allowing duplicate source keys in one batch, emitting an external event before commit, retrying an uncertain write without deduplication, and overlooking row-security, trigger, cascade, or partition effects.

### Compact example

Stored `(tenant=t1,key=a,version=2,value=10)`. Event `e1` with version 3 updates it to 15. Repeating identical `e1` is a replay and changes nothing. Event `e2` at version 2 is stale. New key c at version 1 inserts. A different value at the same stored version is a version conflict, not an update. Tenant t2/key a is a distinct identity. The database transaction must serialize these outcomes against a unique `(tenant,key)` constraint and a unique payload-bound event token.

### Connections

[DBE-009](009-life-of-a-read-query.md) defines snapshots and query evidence. [DBE-010](010-life-of-a-transactional-write.md) defines atomicity, commit, rollback, and uncertain outcomes. [DBE-018](018-null-and-three-valued-logic.md) governs nullable guards and comparisons. Later modules cover storage, indexes, concurrency control, logging, replication, and recovery.

## Governing Question

Reading asks which facts are visible. Modification changes the facts that later transactions will observe. A syntactically valid statement can alter too many rows, overwrite a concurrent writer, route to an unintended partition, trigger cascades, or be applied twice after a timeout. Correctness must bind row selection, transition rules, database constraints, isolation behavior, retry protocol, and evidence.

Upsert is especially easy to oversimplify. “Insert if absent, otherwise update” leaves unanswered: absent by which identity, which unique conflict, update from which existing version, what if two input rows target one stored row, what if the request is stale, what if it is a replay, and what if another writer commits between decisions? An engine primitive provides atomic mechanics only within its documented contract; the application still owns domain semantics.

## Why This Matters

Modifications implement money movement, inventory, account state, access policy, deployment records, event ingestion, and derived read models. A lost update can discard an approved change. A duplicate retry can charge twice. A broad delete can destroy a tenant. An upsert can resurrect a tombstoned entity or move a value backward in event time. These failures often appear only under concurrency or recovery.

Operationally, writes acquire locks, modify indexes, generate log records, fire triggers, validate constraints, and may wait or deadlock. A client timeout does not prove rollback; the server may commit after the client loses the response. Retrying blindly can duplicate effects. A production write path needs an outcome protocol, stable identifiers, bounded retries, cancellation semantics, and reconciliation.

Portability is limited. PostgreSQL `ON CONFLICT`, SQLite UPSERT, MySQL `ON DUPLICATE KEY UPDATE`, SQL-style `MERGE`, and MySQL `REPLACE` have different arbiters, action ordering, concurrency guarantees, affected-row counts, trigger behavior, and return facilities. Shared design principles should not be presented as identical syntax or behavior.

## Prerequisites and Retrieval

Retrieve keys and constraints, bag semantics, null and equality, INSERT/UPDATE/DELETE, joins and subqueries, transactions, isolation, locks, deadlocks, unique indexes, generated columns, defaults, triggers, foreign keys and cascades, partitions, write-ahead logging, retries, idempotency, APIs, and audit/outbox patterns.

Distinguish proposed row from existing row; matched conflict from authorized update; insert/update/no-op from stale/conflict/replay; statement success from transaction commit; client timeout from database outcome; affected-row count from business outcome; logical delete from physical delete; deterministic repetition from payload-bound idempotency; and database atomicity from external side-effect atomicity.

## Learning Objectives

After this module, you should be able to:

1. specify insert, update, delete, and upsert as guarded state transitions;
2. prove target identity, tenant scope, and affected-cardinality expectations;
3. choose and enforce an upsert arbiter from business identity;
4. distinguish replay, stale version, same-version conflict, insert, update, and no-op;
5. prevent lost updates with atomic version/state predicates;
6. design payload-bound idempotency and uncertain-commit recovery;
7. reason about multirow sources, MERGE action order, and duplicate target matches;
8. account for defaults, generated columns, triggers, cascades, partitions, and return values;
9. design transactionally coupled audit/outbox evidence; and
10. test locks, deadlocks, isolation, retries, privileges, plans, and upgrades.

## Core Exposition

`INSERT` creates rows from explicit values, defaults, or a query. Always enumerate target columns in durable code. Omitting the list couples meaning to schema order and makes additive evolution dangerous. Define which values are supplied, defaulted, generated, overridden, nullable, or derived by triggers, and validate types, units, time zones, and tenant ownership before the statement.

Multirow INSERT is one statement but error and atomicity behavior depends on engine, constraints, conflict clauses, and transaction mode. Do not assume partial success or all-or-nothing without documentation and a live test. Record proposed count, accepted count, rejected/conflicted count, returned identities, and warnings. MySQL's `IGNORE` can turn errors into adjusted or skipped rows; such behavior demands explicit warning inspection and is unsuitable where silent coercion is unacceptable.

`INSERT ... SELECT` transfers a query result into a target. State source snapshot, input/output grain, column mapping, deduplication, and expected count. Source duplicates may violate identity or be silently routed through conflict handling. Validate the source relation independently and ensure the transaction/isolation gives the intended as-of view.

`UPDATE` selects target rows with its predicate and computes new values. The safety contract names target key, tenant, lifecycle state, expected version, and expected affected cardinality. A preflight SELECT is useful for review but cannot replace the guarded write because rows can change between statements. Put the critical guard in UPDATE and verify the returned/affected rows.

For single-entity commands, “exactly one affected” is often an invariant. Zero can mean absent, unauthorized, already changed, stale version, or a no-op under engine counting rules; distinguish these using safe evidence. More than one means the identity predicate was not unique or the source join multiplied candidates. Never treat all non-one outcomes as the same application error.

Lost updates arise when two transactions read version v, calculate replacements, and both write; the later overwrites the earlier. Optimistic control uses `WHERE id=? AND version=?`, writes `version=version+1`, and requires exactly one success. A zero-row outcome triggers reread/conflict logic, not unconditional retry. Pessimistic locking is an alternative when contention and transaction scope justify it, but it increases waits and deadlock risk.

Counters and accumulators should be modified relative to the current database row in one guarded statement, such as `balance=balance+delta`, subject to overflow, units, and domain constraints. Reading 10 in the application and later writing 11 loses a concurrent increment. Relative updates still need idempotency: retrying the same delta twice adds it twice unless the logical operation is uniquely recorded.

`DELETE` physically removes selected rows and can trigger foreign-key actions, triggers, index work, logging, and replication. State whether absence is an error or idempotent success and verify affected identities. Soft delete updates lifecycle fields instead, preserving history but requiring every read, unique rule, FK policy, retention job, and resurrection rule to understand tombstones. Soft deletion is a data model, not a safer spelling of delete.

Before a broad modification, prove the predicate with a same-snapshot method where possible, use bounded batches with stable key order when required, and retain progress/restart evidence. A LIMIT without deterministic key progression can skip or repeat rows. Long batches increase lock duration, log volume, replication lag, and recovery work. Commit boundaries change atomicity and must be part of the migration contract.

An upsert needs a unique arbiter that represents business identity, such as `(tenant_id,external_id)`. A nonunique precheck followed by INSERT races: two sessions can both see absence. The unique constraint serializes the conflict, and the documented upsert primitive chooses its alternative atomically. If the schema lacks the identity constraint, the upsert design is incomplete.

PostgreSQL documents `ON CONFLICT DO UPDATE` as guaranteeing an atomic insert-or-update outcome absent another error. A conflict target may infer a unique index or name a constraint. Existing target values and proposed `excluded` values are separately addressable. An update-side WHERE can decline the update after locking the conflict row; such a row is not necessarily returned. These specifics must be tested rather than generalized to all engines.

The update function is a domain merge, not “copy every proposed column.” Immutable identity, creation metadata, source provenance, version, tombstone, counters, and server-generated fields need individual rules. A stale event must not overwrite a newer row. Equal-version different-payload input signals conflict/corruption. An identical replay should return the previously committed outcome without advancing version or timestamp.

PostgreSQL also requires a deterministic `ON CONFLICT DO UPDATE` statement: one existing row cannot be affected more than once by the same command. Batch inputs that duplicate arbiter keys can fail. Prevalidate or deterministically consolidate source rows according to an owned policy; never let input order choose a winner accidentally.

SQLite UPSERT evaluates conflict clauses in order and executes at most one applicable clause for a row, with decisions made per input row in a multirow insert. MySQL `ON DUPLICATE KEY UPDATE` can be triggered by a duplicate primary or unique key; tables with several unique indexes require special caution because which conflict identifies the row can diverge from the intended business arbiter. Use target-specific tests and keep identity unambiguous.

MySQL affected-row counts for duplicate-key insert/update have special values and can change with client flags. PostgreSQL command tags and returned rows have different meanings. An ORM abstraction that reports “rows affected” cannot serve as a portable business outcome. Return or record an explicit action and authoritative row where supported, or derive it transactionally under a tested dialect protocol.

MySQL `REPLACE` is not a synonym for in-place update. Its documented semantics are replacement associated with delete-and-insert behavior even if a storage engine can implement it differently. This can change generated identity, defaults, trigger/cascade effects, child references, creation metadata, and privileges. Avoid it when the domain requires preserving row identity; use a deliberate update/upsert.

SQL `MERGE` matches source candidate rows to a target and evaluates ordered action clauses. It supports richer insert/update/delete classification, but source uniqueness and match stability are critical. If several source rows map to one target or a join condition includes mutable target columns, outcomes can error or surprise. Deduplicate/reject sources by the target identity and keep match identity separate from action predicates.

`MERGE` and vendor upsert primitives do not have identical concurrency promises. PostgreSQL documentation distinguishes `MERGE` from `INSERT ... ON CONFLICT`, noting that MERGE does not universally guarantee one of insert/update when concurrent change occurs. Test isolation-level behavior with interleavings, unique conflicts, row movement, and retries for the exact engine/version.

Idempotency begins with a stable logical-operation key supplied or derived at the correct boundary. Store a unique `(scope,key)` plus canonical request digest, state, and final response/reference in the same transaction as the domain effect. On retry, identical digest returns the recorded result; different digest under the same key fails. A unique entity key alone does not make a counter increment or payment idempotent.

An idempotency state may be pending, committed, failed-retryable, or permanently rejected, but stale pending recovery needs ownership/lease rules and transaction evidence. Avoid holding database transactions open while calling external systems. If an external effect must follow commit, write an outbox row transactionally, publish it asynchronously with its own deduplication, and reconcile delivery.

A timeout or broken connection creates an uncertain outcome. The client must not infer rollback. Reconnect, query by idempotency key or operation ID, and return the stored result if committed. If no durable record exists, retry according to a bounded policy. Preserve database error classes: unique violation, serialization failure, deadlock, timeout, constraint failure, and connection loss need different decisions.

Retries for serialization failures and deadlocks rerun the entire transaction from a fresh snapshot. They must be bounded, jittered where appropriate, observable, and safe for all included effects. Do not retry arbitrary constraint errors. Do not reuse transaction-local state or assume sequences have no gaps after rollback; generated identifiers usually promise uniqueness, not contiguity.

`RETURNING` in PostgreSQL can expose rows after defaults and triggers, and PostgreSQL 18 documents old/new values for data modification. Other engines differ in support and restrictions. Return the stable identity, version, generated fields, action, and audit correlation needed by the caller, not necessarily every sensitive column. Returned data proves a statement result inside the transaction; the caller still needs commit outcome.

Triggers, generated columns, rules, cascades, and row-level security expand the effective write surface. An upsert may require INSERT, UPDATE, and SELECT privileges; policies may check proposed and existing rows differently. Audit direct and indirect table changes, trigger order, recursion, transition values, and failure behavior. Hidden side effects are still part of the state transition.

Partitioned targets add routing constraints. Insert values choose a partition; updates may move rows where supported; conflicts and unique constraints can be limited by partitioning rules. The logical business key must be enforceable at the required scope. A locally unique key in each partition does not prove global identity.

Deadlocks result from conflicting lock order, not necessarily incorrect transactions. Modify multiple entities in a stable key order, keep transactions short, index predicates and foreign-key checks, avoid user/network waits inside transactions, and handle victim errors with full-transaction retry. Lock waits, deadlocks, and timeouts must be measured separately.

Isolation determines which anomalies remain. A version guard prevents overwriting an intervening change to one row but may not protect cross-row invariants or write skew. Unique/exclusion constraints, serializable isolation, explicit locking, or redesigned materialized invariants may be needed. Later concurrency modules develop these mechanisms; this module requires identifying the invariant's scope.

Audit records should capture operation ID, actor/tenant, request digest/version, old/new authoritative values or a governed delta, action, reason, source, transaction/commit correlation, and time from a trusted source. Avoid logging secrets. An audit table written outside the domain transaction can report a change that rolled back or miss a committed change.

Testing begins with insert, update, identical replay, same-key different payload, stale version, equal-version conflict, absent target, unauthorized target, tombstone, nulls, constraint failure, duplicate source keys, trigger changes, cascade, partition boundary, deadlock, serialization retry, timeout before/after commit, and concurrent same-key writers. Verify state, returned evidence, audit/outbox, row counts, locks, and retry behavior.

## Definitions and Notation

Let stored state for identity `i` be `S_i=(version,value,last_token)` and request `r=(i,v,x,k,digest)`:

- insert is valid when `i` is absent and initial-version rules hold;
- update is valid when `v` advances according to policy and transition constraints hold;
- replay occurs when `k` exists with the same digest and recorded outcome;
- token conflict occurs when `k` exists with another digest;
- stale occurs when `v` is older than stored version;
- version conflict occurs when versions are equal but authoritative payload differs;
- optimistic update succeeds only if the expected stored version predicate matches atomically.

Idempotence is `W(W(S,r).state,r).state=W(S,r).state` for the same logical request, with an equivalent recorded outcome. It does not follow from ordinary upsert alone.

## Mechanisms, Invariants, or Proof Structure

A modification review should:

1. state business operation, target identity, tenant, old/new grain, and expected cardinality;
2. define allowed lifecycle/version transitions and every insert/update/no-op/stale/conflict/replay outcome;
3. enforce identity, null, range, FK, and cross-row invariants with appropriate database mechanisms;
4. place authorization, expected version, and state guards atomically in the write;
5. bind idempotency token to canonical request digest and committed outcome;
6. validate multirow source uniqueness and deterministic merge/action order;
7. include defaults, generated values, triggers, cascades, partitions, policies, audit, and outbox in the effect model;
8. test concurrent interleavings, uncertain commits, deadlocks, serialization retries, and cancellation;
9. reconcile proposed, inserted, updated, deleted, skipped, stale, conflicted, replayed, and returned rows; and
10. inspect actual plans, locks, waits, log volume, replication lag, retry rates, privileges, and upgrades.

The finite model below applies versioned, payload-bound events to a tenant-scoped key map. It records explicit insert, update, replay, stale, and version-conflict outcomes. It models sequential semantic decisions, not database locking or transaction isolation.

<!-- bijux-verify: {"id":"finite-versioned-upsert","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"actions=(('e1', 'update'), ('e1', 'replay'), ('e2', 'stale'), ('e3', 'insert'), ('e4', 'version_conflict'), ('e5', 'insert'), ('e5', 'replay'))\nfinal_rows=((('t1', 'a'), 3, 15, 'e1'), (('t1', 'b'), 1, 5, 'seed-b'), (('t1', 'c'), 1, 7, 'e3'), (('t2', 'a'), 1, 20, 'e5'))\noutcome_counts=(('insert', 2), ('replay', 2), ('stale', 1), ('update', 1), ('version_conflict', 1))\naudit=(('e1', 'update', ('t1', 'a'), (2, 10), (3, 15)), ('e3', 'insert', ('t1', 'c'), None, (1, 7)), ('e5', 'insert', ('t2', 'a'), None, (1, 20)))\n","stderr":""}} -->
```python
from collections import Counter

rows = {
    ("t1", "a"): {"version": 2, "value": 10, "token": "seed-a"},
    ("t1", "b"): {"version": 1, "value": 5, "token": "seed-b"},
}
events = (
    ("t1", "a", 3, 15, "e1"),
    ("t1", "a", 3, 15, "e1"),
    ("t1", "a", 2, 99, "e2"),
    ("t1", "c", 1, 7, "e3"),
    ("t1", "b", 1, 6, "e4"),
    ("t2", "a", 1, 20, "e5"),
    ("t2", "a", 1, 20, "e5"),
)

token_payloads = {}
actions = []
audit = []
for tenant, entity, version, value, token in events:
    key = (tenant, entity)
    payload = (key, version, value)
    if token in token_payloads:
        outcome = "replay" if token_payloads[token] == payload else "token_conflict"
    elif key not in rows:
        outcome = "insert"
        token_payloads[token] = payload
        rows[key] = {"version": version, "value": value, "token": token}
        audit.append((token, outcome, key, None, (version, value)))
    else:
        current = rows[key]
        if version < current["version"]:
            outcome = "stale"
        elif version == current["version"]:
            outcome = "replay" if token == current["token"] and value == current["value"] else "version_conflict"
        else:
            outcome = "update"
            token_payloads[token] = payload
            old = (current["version"], current["value"])
            rows[key] = {"version": version, "value": value, "token": token}
            audit.append((token, outcome, key, old, (version, value)))
    actions.append((token, outcome))

final_rows = tuple((key, row["version"], row["value"], row["token"]) for key, row in sorted(rows.items()))
counts = Counter(outcome for _, outcome in actions)

print(f"actions={tuple(actions)}")
print(f"final_rows={final_rows}")
print(f"outcome_counts={tuple(sorted(counts.items()))}")
print(f"audit={tuple(audit)}")
```

The model does not persist tokens for rejected stale/conflict requests and does not model crashes. Python dictionary equality, ordering, and integers are not database unique constraints, numeric types, locking, isolation, triggers, or commit behavior. A production implementation stores idempotency and domain changes atomically.

## Alternatives and Trade-Offs

Optimistic version updates avoid long-held locks and work well under moderate contention, but conflicts require caller resolution or bounded retry. Pessimistic row locks simplify some read-modify-write sequences but add waits/deadlocks and do not automatically protect absent rows or cross-row predicates. Atomic relative updates are concise for counters but require operation idempotency.

Vendor upsert primitives are direct and often provide strong unique-conflict behavior, but differ across engines. MERGE expresses multiple actions and source relations but has complex matching and concurrency semantics. Separate INSERT then guarded UPDATE can expose clearer outcomes inside a transaction, but naïve read-then-write races. Stored procedures centralize logic near constraints; application orchestration can be easier to evolve but must preserve atomicity and error detail.

## Failure Modes and Misconceptions

- “A SELECT found no row, so INSERT is safe.” Another transaction can insert before yours; enforce unique identity.
- “Upsert is idempotent.” An update that increments or overwrites newer state is not retry-safe without request identity.
- “Any duplicate means replay.” The same key with a different payload is a conflict.
- “Affected rows equals business changes.” Counts and no-op behavior differ by engine and client flags.
- “REPLACE updates the row.” MySQL replacement semantics can delete and insert, affecting identity and side effects.
- “MERGE and ON CONFLICT are interchangeable.” Matching, actions, and concurrency guarantees differ.
- “A version column solves concurrency.” It protects only writes whose guards include it and not arbitrary cross-row invariants.
- “Timeout means rollback.” Commit may be uncertain; reconcile by operation key.
- “Audit can be written afterward.” A crash can separate audit and domain state; use one transaction/outbox.
- “One green sequential test proves safety.” Concurrent interleavings, locks, retries, triggers, and isolation must be exercised.

## Worked Examples

### Example 1

Insert a user with explicit `(tenant_id,external_id,email)` columns and let the database generate internal ID and creation time. Return those generated values and the new version. Omitting the column list risks semantic shift after schema evolution.

### Example 2

An account update uses `WHERE tenant_id=? AND id=? AND version=7`, sets approved fields and version 8, and requires one returned row. Zero means stale/absent/unauthorized and triggers safe diagnosis; it is not silently retried as the same replacement.

### Example 3

Two clients increment inventory from 10. Application read-plus-write can leave 11 instead of 12. Atomic `quantity=quantity+1` preserves both increments, but each increment still needs a unique operation token so a timeout retry does not produce 13.

### Example 4

Upsert keyed only by external ID allows tenant A's input to conflict with tenant B. The correct arbiter is unique `(tenant_id,external_id)`, and every update/policy predicate carries tenant. The returned row is checked against the requested tenant.

### Example 5

Stored version 9 receives event version 8. Updating would regress state, so outcome is stale and the row is unchanged. Version 9 with a different payload is a version conflict requiring reconciliation. Identical operation token and payload is replay.

### Example 6

A batch contains two proposed rows with the same arbiter key. PostgreSQL `ON CONFLICT DO UPDATE` can reject an attempt to affect one existing row twice. Reject the batch or deterministically consolidate it using an owned ordering/version rule before modification.

### Example 7

Replacing a parent row to change one field can activate delete/insert semantics, defaults, identity changes, or cascades. An explicit update preserves row identity and changes only governed fields. Test triggers and child references on the exact MySQL engine before any REPLACE use.

### Example 8

A MERGE source has two rows matching one target. Even if input happens to be ordered, that is not a winner policy. Enforce source uniqueness at the target key, quarantine duplicates, and make action predicates depend on version/state rather than source order.

### Example 9

The database commits a payment but the response connection drops. The retry sends the same idempotency key and digest; the service reads the committed record and returns its stored payment ID. Reuse of that key with another amount is rejected and audited.

### Example 10

A million-row backfill updates in stable primary-key ranges, records high-water marks and counts, limits transaction/log size, monitors locks and replication lag, and rechecks the predicate after completion. Each batch is restartable without overwriting rows changed by newer application versions.

## Cross-Program Connections

- [Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) supplies races, atomic transitions, locks, and retry reasoning.
- [Software Engineering Patterns](../../11-software-engineering-patterns/ROADMAP.md) covers idempotency, optimistic concurrency, outbox, and saga boundaries.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) applies versioned upsert to CDC, replay, deduplication, and backfills.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) owns request idempotency, error contracts, and uncertain-outcome reconciliation.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) governs tenant scope, least privilege, row policies, audit integrity, and destructive-operation controls.

## References

1. PostgreSQL Global Development Group, [INSERT](https://www.postgresql.org/docs/18/sql-insert.html), PostgreSQL 18 `ON CONFLICT`, arbiter, concurrency, and RETURNING documentation.
2. PostgreSQL Global Development Group, [UPDATE](https://www.postgresql.org/docs/18/sql-update.html), PostgreSQL 18 documentation.
3. PostgreSQL Global Development Group, [DELETE](https://www.postgresql.org/docs/18/sql-delete.html), PostgreSQL 18 documentation.
4. PostgreSQL Global Development Group, [MERGE](https://www.postgresql.org/docs/18/sql-merge.html), PostgreSQL 18 action and RETURNING documentation.
5. SQLite Project, [UPSERT](https://www.sqlite.org/lang_upsert.html), SQLite documentation.
6. SQLite Project, [ON CONFLICT Clause](https://www.sqlite.org/lang_conflict.html), SQLite documentation.
7. Oracle, [INSERT ... ON DUPLICATE KEY UPDATE](https://dev.mysql.com/doc/refman/8.4/en/insert-on-duplicate.html), MySQL 8.4 Reference Manual.
8. Oracle, [REPLACE Statement](https://dev.mysql.com/doc/refman/8.4/en/replace.html), MySQL 8.4 Reference Manual.

## Exercises

### Exercise 1

Specify a guarded update for changing an order from pending version 4 to approved version 5. State identity, tenant, authorization, lifecycle/version predicates, affected-cardinality outcomes, returned evidence, and concurrent behavior.

### Exercise 2

Design payload-bound idempotency for `POST /payments`. Cover canonical digest, uniqueness scope, pending/committed states, same-key different-payload behavior, timeout after commit, external publication, retention, and reconciliation.

### Exercise 3

Stored `(version=7,value=A)` receives: token k1/version 8/value B; identical k1 retry; token k2/version 6/value C; token k3/version 8/value C. Derive each outcome and final state.

### Exercise 4

Compare PostgreSQL ON CONFLICT, SQL-style MERGE, MySQL ON DUPLICATE KEY UPDATE, and MySQL REPLACE across arbiter identity, source duplicates, concurrency, action semantics, affected rows, triggers/identity, and portability.

### Exercise 5

Create a production evidence plan for a tenant-scoped bulk upsert of 50 million CDC events. Include source validation, ordering/version, duplicates, tombstones, constraints, batches, locks/deadlocks, isolation, idempotency, audit/outbox, plans/log/replication, uncertain commits, rollback, and upgrade testing.

## Answers to the Exercises

### Answer 1

Target unique `(tenant_id,order_id)` under an authorized actor. One atomic UPDATE requires tenant/order, `status='pending'`, and `version=4`; it sets only approved fields, `status='approved'`, `version=5`, actor/time, and returns identity, old/new status/version, and audit correlation. One row is success; zero is diagnosed as absent/unauthorized/stale/wrong state without leaking data; more than one contradicts identity. Concurrent attempts serialize through row locking/version guard so only one matches version 4.

### Answer 2

Create unique `(merchant,idempotency_key)` with canonical request digest, operation ID, state, and stored response/reference in the same transaction as payment creation. Identical committed retry returns that result; another digest fails. Pending recovery uses bounded lease/ownership and transaction evidence rather than duplicating payment. A transactional outbox publishes after commit with operation ID deduplication. Retention exceeds the client retry horizon and financial reconciliation period, and uncertain timeouts query the record before retry.

### Answer 3

k1 version 8 advances the row from `(7,A)` to `(8,B)`. Identical k1 is replay and leaves it unchanged. k2 version 6 is stale. k3 version 8 with value C conflicts because equal authoritative version has different payload. Final state is `(8,B,last_token=k1)` with one update audit entry and explicit replay/stale/conflict outcomes.

### Answer 4

PostgreSQL ON CONFLICT uses a named/inferred unique arbiter and documents atomic insert-or-update, deterministic one-affect-per-target behavior, and PostgreSQL-specific RETURNING. MERGE matches a source relation and ordered actions, supports broader insert/update/delete logic, but has different concurrent guarantees and needs source uniqueness. MySQL duplicate-key update reacts to primary/unique conflicts, has special affected-row counts, and is risky with several possible unique arbiters. REPLACE has replacement/delete-insert semantics that can alter triggers, identity, defaults, and references. None is a behavior-portable synonym; share the domain transition contract and implement/test per target.

### Answer 5

Validate a fixed source snapshot/manifests, canonical tenant/key schema, version order, operation IDs, payload digests, duplicate-key groups, tombstones, and null/type/unit rules. Enforce target unique identity and transition constraints; quarantine same-version conflicts; batch in stable source/key order with bounded transactions and restart checkpoints. Exercise concurrent same-key writers, deadlock/serialization retries, timeout-before/after-commit, and payload-bound idempotency. Couple audit/outbox to each domain transaction, reconcile every proposed outcome and final version, capture plans, locks/waits, log volume, replication lag, trigger/partition effects, and cancellation, and maintain forward repair/rollback. Re-run semantic interleavings and resource thresholds after database, driver, schema, index, policy, trigger, or configuration upgrades.
