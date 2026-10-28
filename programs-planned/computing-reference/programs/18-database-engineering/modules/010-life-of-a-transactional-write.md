---
module_id: DBE-010
program: Database Engineering
level: 1
module_number: 10
title: Life of a Transactional Write
status: complete
last_verified: 2026-08-30
---

# Life of a Transactional Write

## One-Page Review

### Governing question

How does a requested write become a validated, concurrent, committed, visible, durable, recoverable, and safely acknowledged database fact?

### Essential definitions

A **transaction** is the database boundary that groups operations into commit or abort. A **write set** is the logical and physical state a transaction proposes to change. A **constraint** rejects states outside declared rules. **Concurrency control** orders or rejects conflicting work. A **dirty page** contains changes not yet propagated to its durable data-file location. A **write-ahead log (WAL)** records recovery information before dependent data pages reach durable storage. A **commit point** is the engine-defined event after which the transaction is committed; an **acknowledgment point** is when success is reported to the client. **Outcome uncertainty** occurs when the client loses communication without knowing whether commit occurred.

### Central model, mechanism, or theorem

A portable write trace is:

`receive -> parse/bind/plan -> begin/join transaction -> read/lock/validate -> create versions/index changes -> record recovery information -> validate commit -> make committed -> satisfy durability policy -> acknowledge -> later writeback/reclaim`.

Actual engines reorder, combine, or omit stages. The critical write-ahead invariant is that recovery information required to redo a committed change reaches the promised durable boundary before that change is acknowledged as durable; data pages may be written later. Atomicity requires recovery to expose all committed effects and none of an aborted transaction's effects under the engine's protocol.

### Critical invariants

- The business operation and all database-enforced effects share an intentional transaction boundary.
- Constraints and authorization are evaluated in the correct role, schema, snapshot, and deferral context.
- Conflicting writes are serialized, validated, retried, or rejected; lost updates are not silently accepted.
- Every affected heap/record, index, generated value, trigger, and outbox/ledger consequence is included.
- Required log records precede dependent durable page state under the recovery protocol.
- Success means a documented local/replicated durability level, not merely “statement ran.”
- Unknown outcomes are resolved by stable operation identity and authoritative lookup, not blind replay.
- Abort, deadlock, serialization failure, timeout, cancellation, disconnect, and crash leave a testable state.

### Common failures

Failures include autocommitting half a business operation, checking an invariant only in application code, reading then writing without concurrency protection, retrying non-idempotent work, assuming a timeout means abort, returning success before the promised durability boundary, equating dirty-page writeback with commit, copying database files during writes without a supported backup protocol, ignoring index and trigger amplification, holding transactions across network calls, handling deadlocks as fatal surprises, suppressing serialization retries, and publishing an event outside the authoritative commit.

### Compact example

A transfer of 30 from account 1 (100) to account 2 (50) locks or validates both accounts in a deterministic protocol, constructs balances 70 and 80, checks nonnegative balances and conserved total 150, records recovery information, commits atomically, and stores the request ID. Repeating the same ID returns the committed result without applying another transfer. A crash or rejection before the modeled commit leaves the prior committed map unchanged. This finite state machine illustrates invariants; it does not implement WAL or prove crash durability.

### Connections

[DBE-009](009-life-of-a-read-query.md) supplies parsing, binding, planning, visibility, and client transport. [DBE-011](../ROADMAP.md) begins relational querying. Later transaction, locking, MVCC, WAL, recovery, and replication blocks refine every mechanism introduced here. Security, Distributed Systems, and API Engineering govern authorization, ambiguous outcomes, and retry contracts.

## Governing Question

A client sends `INSERT`, `UPDATE`, `DELETE`, `MERGE`, or a procedure call and eventually receives success, an error, or silence. Between those endpoints, the system may resolve objects and types, acquire locks, read versions, fire triggers, check constraints, update indexes, dirty buffers, append logs, coordinate replicas, flush storage, and release resources. Some work is undone logically on abort; some physical bytes remain but are invisible and later reclaimed.

The task is to identify the exact correctness and persistence boundary for the selected engine, version, storage stack, isolation level, and durability mode. “The row was written” is ambiguous: placed in a client buffer, sent to the server, changed in an engine buffer, visible inside the transaction, committed locally, flushed to durable media, replicated, applied remotely, returned to the client, or processed by a downstream consumer are different events.

## Why This Matters

Write failures change authoritative state. A split transaction can debit without crediting, reserve inventory without creating an order, or publish an event for data that later aborts. Concurrency can make individually valid application checks jointly invalid. A retry after a lost response can duplicate a payment. An unsafe durability configuration can acknowledge work that disappears after power loss.

Performance decisions are also correctness decisions. Batching can reduce round trips and amortize commit, but enlarges lock duration, rollback scope, log bursts, and tail latency. Extra indexes accelerate reads but every affected write may update additional structures and log more bytes. Asynchronous durability lowers acknowledgment latency by accepting a loss window; it must not be described as equivalent durability.

A rigorous trace makes incidents diagnosable. It distinguishes time waiting for a pool, locks, validation, log insertion, log flush, replication, page I/O, result transfer, and application work. It also distinguishes an aborted operation from an unknown client outcome, which requires lookup rather than assumption.

## Prerequisites and Retrieval

Retrieve transactions, ACID, constraints, foreign keys, indexes, triggers, generated values, isolation, snapshots, locks, deadlocks, MVCC, pages, buffers, WAL, flush/fsync, checkpoints, crash recovery, replication, timeouts, cancellation, idempotency, and request tracing.

Distinguish statement from transaction; logical change from physical version; log insertion from log flush; page dirtiness from page persistence; database commit from client observation; local durability from replica receipt, durable replica storage, and replica apply; and retryable rejection from an unknown outcome.

## Learning Objectives

After this module, you should be able to:

1. trace a write from request construction through acknowledgment and cleanup;
2. define transaction boundaries around business invariants;
3. explain constraint, trigger, generated-value, and index consequences;
4. distinguish locking, optimistic validation, MVCC versioning, and serialization failure;
5. explain WAL ordering without equating it to a specific implementation;
6. distinguish commit, visibility, durability, replication, and acknowledgment;
7. design safe retry and idempotency behavior for uncertain outcomes;
8. account for write amplification, batching, checkpoints, and backpressure;
9. test abort and crash boundaries using authoritative state; and
10. document what evidence is required before claiming a write is production-safe.

## Core Exposition

The application begins by defining one business operation and a stable identity. Values use protocol parameters; authorization is checked both at the service boundary and through a least-privilege database role. A request ID or domain command ID is not merely a log correlation token: when duplicates are possible, it participates in a uniqueness-backed idempotency protocol with a stored outcome.

Transaction scope must match the invariant. A funds transfer contains debit and credit; an order may contain header, lines, inventory reservation, and a durable event intent. Autocommitting each statement exposes partial states. Conversely, keeping a transaction open while calling an external service holds locks/versions and couples database availability to a network. Persist an intent or outbox atomically, then perform external work outside the transaction with its own delivery protocol.

The driver submits statements within an explicit or implicit transaction. Connection, role, database, isolation, read/write mode, search path, time zone, constraint mode, and durability settings belong to the trace. Pool checkout must start from known transaction/session state. A prior error can leave a connection in a failed transaction that must be rolled back before reuse.

Parsing, binding, rewriting, and planning follow the read-path concepts. Binding resolves the target, input types, defaults, generated expressions, functions, constraints, policies, triggers, conflict arbiters, and `RETURNING` expressions. A prepared write may reuse some work, but schema and plan invalidation remain engine-specific. Dynamic identifiers require allowlisting and correct quoting.

The executor locates target rows or insertion destinations. An update/delete may first execute a read-like plan. Which versions qualify depends on snapshot and concurrency rules; a row can change between predicate evaluation and attempted modification under some isolation mechanisms, requiring recheck, wait, restart, or rejection. `UPDATE ... WHERE` affecting zero rows may mean absence, authorization filtering, stale version, or already-applied intent—interpret it explicitly.

Concurrency control prevents incompatible histories. Locking protocols wait or reject conflicts; optimistic protocols validate reads/writes at commit; MVCC creates new versions while readers may retain old ones. Engines combine mechanisms. Define lock acquisition order where the application controls it, keep transactions bounded, observe waits, and handle deadlock victim errors. Avoid claiming that row locks alone enforce a multi-row predicate invariant.

Isolation defines allowed interactions, not just read freshness. Read-modify-write can lose an update if the application reads a value and later overwrites it without a guarded predicate, atomic expression, lock, or serialization. Write skew can preserve each row constraint while violating a cross-row invariant. Use database constraints where expressible, atomic SQL, appropriate locking, or serializable execution with whole-transaction retry.

The transaction constructs logical and physical effects. An insert may allocate identifiers, apply defaults, compute generated columns, route a partition, and create a row version. Updates may create a new version rather than overwrite in place. Deletes may mark a version deleted. Each affected index, materialized structure, foreign key, trigger, and change-capture mechanism adds work. Product documentation owns exact timing and representation.

Constraints define allowed committed state. Not-null, check, unique, exclusion, primary-key, and foreign-key checks may use indexes and concurrency coordination. Immediate constraints usually reject within the statement; supported deferrable constraints can be checked later, including commit. Constraint order is not an application API. Error handling should use structured identifiers/codes, not fragile message text, and should not expose sensitive values.

Triggers and stored procedures execute code inside the database transaction according to engine timing. They can centralize invariants but also hide reads, writes, locks, recursion, volatility, and latency. Inventory every side effect and test failure rollback. A notification emitted to an external system is not automatically rolled back; use a transactional outbox/change stream or a documented transactional integration.

Write amplification spans logical rows, physical row versions, indexes, log, replicas, backups, and downstream changes. Changing one indexed column may touch heap plus several index structures; a page split or compaction can expand physical work. Measure rows attempted/affected, log bytes, dirty buffers, storage writes, lock duration, version retention, replication lag, and downstream volume. Do not infer amplification from SQL row count alone.

In a write-ahead design, the engine creates log records sufficient for its recovery algorithm and assigns ordering positions. The fundamental ordering is that required log state becomes durable before a data page containing corresponding changes is allowed to become durable in a way recovery cannot interpret. This permits dirty data pages to be written before or after transaction commit under the engine's steal/no-force choices while recovery uses log plus transaction status to restore a valid state.

Log insertion into memory is not durable log flush. A commit record can be formed and later included with other transactions in a group flush. Group commit amortizes storage synchronization while each transaction waits for the relevant durable position. The exact leader, queue, batching interval, and device semantics are implementation/configuration details. Measure commit latency distributions and log flush throughput under concurrency.

Commit processing must perform remaining validation, including deferred constraints and optimistic/serializable checks where applicable. Failure can still occur after statement execution appeared successful. The application must treat commit itself as fallible. If commit rejects the transaction, every business effect is aborted even if earlier statements returned row counts or generated IDs inside the transaction.

The local commit point and durability acknowledgment depend on configuration. In PostgreSQL's default synchronous local behavior, commit success waits for the relevant WAL flush; asynchronous commit can report success before that flush and may lose recent acknowledged transactions after a crash while retaining database consistency. Other systems use rollback journals, copy-on-write, consensus logs, or storage transactions. State the selected guarantee rather than importing WAL language universally.

Replication adds several possible acknowledgment boundaries: local durable, replica received, replica operating-system written, replica durably flushed, quorum committed, or replica applied/visible. A label such as “synchronous” is incomplete without the exact wait condition and failure assumptions. Waiting for a replica can increase latency and reduce availability; not waiting increases recovery-point exposure. Later modules formalize these choices.

Data pages need not be flushed at each commit in WAL systems. Buffer managers later write dirty pages, and checkpoints bound recovery work by establishing a recovery starting region under engine rules. This separation makes random data-page forcing unnecessary for every transaction. It also means a page visible in memory is not by itself durability evidence, and a disk write is not by itself commit evidence.

After the commit boundary, the engine makes the transaction's effects visible according to transaction-status and snapshot rules, releases locks at defined times, and eventually reclaims obsolete versions. Existing readers may continue seeing an older snapshot. Downstream replication or change capture may lag. “Committed” does not mean every reader everywhere immediately sees the change.

The server encodes command status, affected rows, generated/returned values, warnings, and errors. Large `RETURNING` results add serialization and network work. The client sees success only after response transfer. If the server commits and the connection fails before the response, the client has an unknown outcome. It must query by stable operation identity or safely repeat an idempotent command; assuming failure risks duplicates, while assuming success can omit work.

Idempotency is an atomic database protocol. Insert the operation ID and authoritative result in the same transaction as the effects, with uniqueness preventing concurrent duplicates. On conflict, retrieve the prior result and verify that reused identity has compatible input. Expiring keys too early reopens duplication. An idempotency table without atomic coupling to the business write is only a race-prone cache.

Not every error is retryable. Syntax, authorization, constraint, and invalid input usually require correction. Deadlock victim and serialization failures may be retried as an entire transaction from a fresh state, with bounded attempts, jitter/backoff, and deadline. Connection loss can mean unknown outcome and requires resolution. Retrying only the final statement can violate assumptions established earlier in the transaction.

Cancellation is a request, not proof of rollback. Determine whether the statement was canceled, transaction is failed, commit occurred, or connection state is unknown. Roll back when required and do not return a connection to the pool until protocol and transaction state are clean. Timeouts should cover pool acquisition, lock wait, statement, transaction lifetime, commit/replication, and request, with one coherent deadline budget.

Crash testing must target named cut points: before any log, after change construction, after log insertion but before flush, after durable commit but before data-page write, after commit but before response, during checkpoint, and during recovery. Validate authoritative invariants and idempotency after restart. Process kill, operating-system crash, power loss, torn writes, device-cache behavior, and correlated replica loss are not equivalent experiments.

Operational evidence connects request ID, transaction ID where safe, statement fingerprint, affected entities, wait events, constraint/deadlock/serialization errors, log generation/flush, dirty/writeback pressure, checkpointing, replication acknowledgment/lag, and client result. Avoid logging secrets or full sensitive rows. Metrics must distinguish rejected, aborted, unknown, committed, durable, and downstream-applied states.

## Definitions and Notation

For transaction `T`:

- `R(T)` and `W(T)` are its logical read and write sets under a stated model;
- `I(S)` means state `S` satisfies declared invariants;
- `LSN(r)` is an engine-specific log position for record `r` where such a log exists;
- `L_page(p)` is the greatest required log position represented on page `p`;
- `L_durable` is the durable-log frontier under the storage contract;
- `t_c`, `t_d`, `t_a`, and `t_v(r)` denote commit, promised durability, client acknowledgment, and visibility to reader `r`.

A WAL-style ordering requires `L_durable >= L_page(p)` before page `p` is safely persisted under that recovery protocol. It does not say every engine uses pages or WAL. A durability policy defines relations among `t_c`, `t_d`, and `t_a`; replication adds named receive, write, flush, commit, and apply events. Network clocks are not assumed perfectly synchronized.

## Mechanisms, Invariants, or Proof Structure

A transactional-write review should:

1. define operation identity, authorization, inputs, outputs, and invariant;
2. draw statement, transaction, external-effect, and acknowledgment boundaries;
3. enumerate read/write sets, constraints, triggers, indexes, generated data, and outbox effects;
4. state isolation, conflict handling, lock/validation order, and whole-transaction retry policy;
5. trace logical versions, dirty buffers, recovery records, commit validation, flush, and writeback;
6. state exact local and replicated durability acknowledgment semantics;
7. handle commit error, disconnect, timeout, cancellation, and unknown outcome;
8. measure write/log/index amplification, waits, tails, checkpoints, and replica/downstream lag;
9. crash and recover at named boundaries; and
10. reconcile authoritative state and prove duplicate suppression with concurrent/replayed requests.

The finite state machine below implements an atomic transfer over copied state, a uniqueness-backed request-result map, rejection, and a simulated pre-commit crash. It proves only its small in-memory transitions, not database concurrency or durable recovery.

<!-- bijux-verify: {"id":"finite-transactional-write","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"initial_balances=((1, 100), (2, 50))\ncommit_status=committed\nafter_commit=((1, 70), (2, 80))\nduplicate_status=replayed\nafter_duplicate=((1, 70), (2, 80))\noverdraft_status=rejected\nafter_rejection=((1, 70), (2, 80))\ncrash_before_commit=((1, 70), (2, 80))\ntotal_invariant=150\n","stderr":""}} -->
```python
class Ledger:
    def __init__(self):
        self.balances = {1: 100, 2: 50}
        self.results = {}

    def transfer(self, request_id, source, target, amount):
        if request_id in self.results:
            return "replayed", self.results[request_id]
        workspace = dict(self.balances)
        if amount <= 0 or source not in workspace or target not in workspace:
            return "rejected", None
        if workspace[source] < amount:
            return "rejected", None
        before_total = sum(workspace.values())
        workspace[source] -= amount
        workspace[target] += amount
        if min(workspace.values()) < 0 or sum(workspace.values()) != before_total:
            return "rejected", None
        result = tuple(sorted(workspace.items()))
        self.balances = workspace
        self.results[request_id] = result
        return "committed", result

    def simulate_crash_before_commit(self, source, target, amount):
        workspace = dict(self.balances)
        workspace[source] -= amount
        workspace[target] += amount
        return tuple(sorted(self.balances.items()))


ledger = Ledger()
print(f"initial_balances={tuple(sorted(ledger.balances.items()))}")
status, _ = ledger.transfer("transfer-1", 1, 2, 30)
print(f"commit_status={status}")
print(f"after_commit={tuple(sorted(ledger.balances.items()))}")
status, _ = ledger.transfer("transfer-1", 1, 2, 30)
print(f"duplicate_status={status}")
print(f"after_duplicate={tuple(sorted(ledger.balances.items()))}")
status, _ = ledger.transfer("transfer-2", 1, 2, 100)
print(f"overdraft_status={status}")
print(f"after_rejection={tuple(sorted(ledger.balances.items()))}")
print(f"crash_before_commit={ledger.simulate_crash_before_commit(1, 2, 10)}")
print(f"total_invariant={sum(ledger.balances.values())}")
```

The assignment of `balances` and `results` is sequential Python, not a durable atomic commit; a real database must couple them through its transaction and recovery machinery. The crash method simply discards a workspace. It does not simulate process death, caches, devices, WAL, locks, replicas, or torn writes.

## Alternatives and Trade-Offs

Pessimistic locking discovers conflicts early but can wait, deadlock, and retain resources. Optimistic/serializable validation permits more speculative overlap but can reject at commit and requires correct retry. Atomic conditional SQL reduces round trips and race windows but may be harder to express. Stored procedures keep multi-step logic near data but increase database code ownership. Application orchestration is flexible but must avoid transaction-spanning external calls.

Synchronous durability narrows acknowledged loss but pays flush/replication latency. Asynchronous acknowledgment improves latency by accepting a documented loss window. Larger transactions amortize commit and round trips but increase contention, log bursts, rollback work, and uncertainty scope. More indexes improve some reads but amplify writes and recovery. The decision is measured against integrity, p99 latency, throughput, recovery, and loss objectives.

## Failure Modes and Misconceptions

“The update returned one row, so it committed” ignores later statement, deferred-constraint, serialization, and commit failure. “The client timed out, so nothing happened” ignores commit-before-response. “Retry the last statement” ignores transaction-wide reads and invariants. “Idempotent endpoint” is unsupported unless identity, effects, and stored outcome are atomically coupled.

“WAL means the row is on its data page” misunderstands no-force commit. “The page reached disk, so the transaction committed” misunderstands transaction status and recovery. “Synchronous replication” is incomplete without receive/write/flush/apply and quorum definitions. “ACID” alone does not specify isolation level, durability mode, storage contract, or multi-system atomicity.

“Constraints are slow application validation” ignores concurrency-safe authority. “Triggers are invisible and therefore free” ignores their reads, writes, locks, failures, and amplification. “Exactly once delivery” does not remove the need for idempotency and reconciliation across uncertain failures.

## Worked Examples

### Example 1

A transfer debits and credits in one explicit transaction. A nonnegative constraint and conserved ledger entries protect state; a unique request ID stores the result. No network call occurs while locks are held.

### Example 2

Two sessions read stock 1 and both try to reserve it. An atomic conditional update `... WHERE stock >= 1`, guarded lock, or serializable transaction admits one; an application read followed by an unconditional write can oversell.

### Example 3

An order insert touches the order heap, primary key, customer index, status index, foreign key lookup, audit trigger, and outbox. “One row inserted” understates physical/logical amplification.

### Example 4

A deferred foreign key allows mutually dependent rows during the transaction but is checked at commit. Earlier statements succeed; commit rejects the entire transaction when the final graph is invalid.

### Example 5

Transactions lock accounts in opposite order and deadlock. The database aborts a victim; the application rolls back and retries the entire operation with a bounded policy, while deterministic lock order reduces recurrence.

### Example 6

Ten concurrent commits share one log flush. Throughput improves, but each transaction's success still waits for the durable frontier required by its policy. The experiment reports p50/p99 commit wait and flush batch size.

### Example 7

Asynchronous local commit returns before durable WAL. A crash can lose a recently acknowledged audit event without leaving a partially applied transaction. The system uses this only for explicitly reconstructible telemetry, not payments.

### Example 8

The server commits a payment, then the socket breaks. The client queries by payment operation ID and retrieves the stored outcome. Blindly issuing a new ID would risk a second payment.

### Example 9

A checkpoint writes dirty pages while writes continue. It is not a global commit of current transactions; recovery uses the checkpoint and subsequent required log according to the engine protocol.

### Example 10

A crash test kills only the database process and passes. The team does not claim power-loss durability until it also validates OS/device flush behavior, supported storage, recovery invariants, and—where required—correlated replica failures.

## Cross-Program Connections

- [Software Engineering Patterns](../../11-software-engineering-patterns/ROADMAP.md) supplies unit-of-work, repository, outbox, and explicit error-boundary patterns.
- [Operating Systems](../../22-operating-systems/ROADMAP.md) explains buffers, write ordering, fsync, device caches, scheduling, and process/OS crashes.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) governs authorization, injection resistance, audit evidence, secrets, and least privilege.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) formalizes replicated logs, quorum, uncertain outcomes, idempotency, and consensus.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) owns request identity, deadlines, retries, and client-visible status contracts.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) operationalizes log/flush metrics, capacity, safe configuration, recovery drills, and incident response.

## References

1. [PostgreSQL 18 Documentation, Transactions](https://www.postgresql.org/docs/18/tutorial-transactions.html)
2. [PostgreSQL 18 Documentation, Constraints](https://www.postgresql.org/docs/18/ddl-constraints.html)
3. [PostgreSQL 18 Documentation, Concurrency Control](https://www.postgresql.org/docs/18/mvcc.html)
4. [PostgreSQL 18 Documentation, Transaction Processing](https://www.postgresql.org/docs/18/transactions.html)
5. [PostgreSQL 18 Documentation, Reliability and the Write-Ahead Log](https://www.postgresql.org/docs/18/wal.html)
6. [PostgreSQL 18 Documentation, Write Ahead Log Configuration](https://www.postgresql.org/docs/18/runtime-config-wal.html)
7. [PostgreSQL 18 Documentation, SET CONSTRAINTS](https://www.postgresql.org/docs/18/sql-set-constraints.html)
8. [SQLite Documentation, Atomic Commit](https://www.sqlite.org/atomiccommit.html)

## Exercises

### Exercise 1

Trace an order placement containing inventory reservation, payment intent, order rows, and notification. Draw database and external boundaries and eliminate every partial-commit window.

### Exercise 2

Design an idempotency protocol for a payment API where the client may disconnect during commit. Address concurrent duplicates, input mismatch, stored output, retention, and authoritative lookup.

### Exercise 3

Explain WAL ordering using log insertion, durable log frontier, dirty pages, commit, checkpoint, and recovery. Identify which observations do not prove durability.

### Exercise 4

Design a concurrency experiment for an inventory decrement that distinguishes lost update, blocking, deadlock, serialization rejection, timeout, and unknown outcome.

### Exercise 5

Prepare a crash-and-recovery evidence plan for a transactional write under local synchronous and replicated durability policies.

## Answers to the Exercises

### Answer 1

Make inventory reservation, order header/lines, payment *intent*, and outbox notification intent one database transaction under constraints and concurrency control. Do not call the payment provider or message broker while it is open. After commit, workers deliver external effects using stable operation/event IDs, record outcomes idempotently, and retry safely. Compensating domain actions handle an externally accepted payment that cannot lead to fulfillment; they do not pretend separate systems were one atomic transaction. Reconcile outbox-to-consumer and payment-intent-to-provider state, including deletes/cancellations and poison events.

### Answer 2

Require a caller-scoped stable idempotency key and canonical request digest. In the same database transaction as the payment state change, insert a unique `(caller,key)` record containing digest, status, and authoritative response reference. Concurrent inserts conflict; the loser reads the winner. A reused key with a different digest is rejected. After disconnect, lookup returns committed outcome; absence under an authoritative consistent read permits a bounded retry with the same key. Retention covers the maximum retry/dispute horizon, and archival/tombstone policy prevents old keys from silently becoming reusable.

### Answer 3

The engine first constructs changes and recovery records, inserts log records into a log buffer, and advances a durable frontier only after the required storage synchronization. Before a dirty page with log position `L_page` is safely persisted, the recovery protocol requires `L_durable >= L_page`. Commit acknowledgment under a synchronous local policy waits for the transaction's required commit log position, while data pages can be written later. Checkpoints establish a bounded recovery starting point, not a transaction boundary. A dirty page, page write, log-buffer insertion, statement row count, or server process survival alone does not prove promised durability; verify flush configuration, storage contract, commit acknowledgment, and recovery.

### Answer 4

Use a versioned fixture with stock one and barriers that start two transactions at controlled points. Test an unsafe read-then-unconditional-write, an atomic guarded decrement, explicit locking, and serializable execution. Record statement/transaction IDs, lock waits, affected rows, deadlock victim, serialization code, deadlines, commit/rollback, final stock, and operation IDs. Inject lock timeout, client timeout, and disconnect after server commit. Lost update means both appear successful with an invalid final history; blocking is observed wait then valid completion; deadlock/serialization are explicit aborts; timeout needs server/transaction resolution; disconnect can be unknown until operation lookup.

### Answer 5

Define expected local flush and each replicated receive/write/flush/apply or quorum boundary. Use a durable operation ledger plus domain invariants. Inject process death, OS crash, power interruption where safely supported, storage fault, primary loss, network partition, replica loss, commit-before-response disconnect, checkpoint overlap, and recovery restart at named cut points. After each, run engine integrity checks, recover through documented procedure, query every operation ID, validate all-or-none effects and totals/constraints, measure acknowledged loss and recovery time, and reconcile replicas/downstream state. Record engine, OS, filesystem, device/cache, configuration, topology, exact fault mechanism, logs, and limitations; a process-kill result does not certify power-loss or correlated-replica durability.
