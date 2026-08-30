---
module_id: DBE-041
program: Database Engineering
level: 1
module_number: 41
title: ACID and Transaction Boundaries
status: complete
last_verified: 2026-08-30
---

# ACID and Transaction Boundaries

## One-Page Review

### Governing question

What exactly becomes one database transaction, which ACID claims apply at that boundary, and how should applications behave when concurrency, crashes, retries, implicit commits, or external systems make the outcome uncertain?

### Essential definitions

A **transaction** is a delimited unit of database work that ends in commit or abort. **Atomicity** means its database effects become committed as a unit or none become committed; it does not make nontransactional external effects disappear. **Consistency** means a committed transition preserves every declared invariant whose assumptions the transaction and database actually enforce; it is not an automatic promise that business logic is correct. **Isolation** constrains observable interference among concurrent transactions according to a named level/model; it does not necessarily mean literal serial execution. **Durability** means an acknowledged commit survives the failures covered by the configured system contract; it does not mean eternal retention or survival of every correlated disaster. A **transaction boundary** identifies the resource manager, start, commit/abort decision, operations, isolation, durability, and visibility scope. A **savepoint** permits partial rollback inside one transaction but is not an independent durable commit. An **ambiguous commit** occurs when the client loses the response and cannot tell whether the server committed.

### Central model, mechanism, or theorem

Model authoritative states as `s∈S`, transactions as partial transitions `T:S→S`, and invariants as predicate `I(s)`. A valid application transition establishes `I(T(s))` whenever its preconditions and `I(s)` hold. Atomic recovery exposes either the pre-state `s` or committed post-state `T(s)`, never an application-visible partial state. Isolation decides which concurrent histories are admitted; durability decides which failures an acknowledged committed state survives. These are separate properties implemented by constraints, concurrency control/MVCC, logging, commit records, checksums, flushing, replication, and recovery. If a local transaction writes row state and an outbox record together, both commit atomically; delivering the outbox later is a distinct retryable protocol, not part of that local atomic commit.

### Critical invariants

- The boundary names every database/resource included and explicitly excludes remote calls, files, caches, clocks, and other effects not enlisted in the same protocol.
- Commit is the only point that makes the local transaction durable/visible according to the engine contract; a savepoint or successful statement is not a commit.
- Every invariant is expressed as a database constraint, serialized decision, or application check whose concurrency assumptions are stated and tested.
- Errors, cancellation, connection loss, timeout, deadlock, serialization failure, and process crash have explicit abort, retry, and ambiguous-outcome handling.
- Retry identity is stable across attempts, and its deduplication record plus authoritative effect share the same transaction boundary when one-effect semantics are required.
- External publication is derived from committed state through an outbox/change-log protocol; remote acknowledgement is not falsely rolled back by a database abort.
- Durability claims name commit acknowledgement, log/data flush policy, storage/replica failure scope, recovery point, backup/restore, and verification.

### Common failures

Failures include treating ACID as one indivisible magic guarantee; calling consistency “valid data” without invariants; assuming a transaction prevents all anomalies; opening a transaction after reading the decision inputs; letting an ORM auto-commit each statement; returning success before commit; doing a remote call while holding locks; sending a message before commit; assuming rollback undoes an email; retrying an ambiguous commit with a new identity; catching an error and committing partial work; confusing nested scopes with nested commits; using savepoint release as durability; ignoring DDL implicit commits; mixing transactional and nontransactional resources; keeping transactions open across user think time; and equating durable commit with backup, replication, or permanent retention.

### Compact example

Inside one local transaction, transfer `25` from checking `70` to savings `30`, record command identity `tx-1`, and insert an outbox fact. The commit publishes balances `(45,55)`, the identity, and one outbox row together. Replaying `tx-1` changes nothing. A later transfer of `80` violates nonnegative balance and aborts, leaving `(45,55)`. Delivery of the outbox row remains a separate protocol. This demonstrates atomic state transition and retry identity, not real SQL, isolation, WAL, crash recovery, or external exactly-once delivery.

### Connections

Retrieve [Dirty Pages and Writeback](028-dirty-pages-and-writeback.md), [Checksums and Page Corruption](029-checksums-and-page-corruption.md), [Tracing a Record from Logical Row to Persistent Bytes](030-tracing-a-record-from-logical-row-to-persistent-bytes.md), and [Index Maintenance and Write Amplification](039-index-maintenance-and-write-amplification.md). Continue through the [Database Engineering roadmap](../ROADMAP.md) to DBE-042, Read and Write Anomalies, and DBE-043, Lock Modes and Granularity.

## Governing Question

How can an engineer draw the actual transaction boundary, state the precise ACID contract at that boundary, preserve invariants under concurrency and failure, and coordinate effects that cannot participate in the same atomic commit?

## Why This Matters

“Use a transaction” is not a design until the boundary and guarantees are named. An HTTP handler can issue three auto-committed statements and have no multi-statement atomicity. A function can open two database connections and span two independent resource managers. A database transaction can commit while the client times out. An email sent before rollback remains sent. A message sent after commit can be lost if the process crashes between the two actions. These are boundary facts, not unusual edge cases.

ACID vocabulary is also frequently blurred. Atomicity concerns all-or-none commit, isolation concerns concurrent histories, consistency concerns declared invariants and valid transitions, and durability concerns post-commit failure survival. Strong atomic recovery does not prevent write skew; serializable isolation does not validate an incorrect tax formula; constraints do not make an external API transactional; synchronous replication does not replace backups or repair operator deletion.

Transaction boundaries determine correctness, latency, contention, log pressure, version retention, retry behavior, and ownership. Too narrow a boundary exposes partial state. Too broad a boundary holds locks/snapshots, expands deadlock/retry work, couples remote latency, and blocks cleanup. The engineering objective is the smallest boundary that atomically protects one authoritative invariant-bearing decision—not the fewest commits or largest possible unit.

## Prerequisites and Retrieval

You should understand logical/physical database state, constraints and keys, pages and WAL, crash recovery at a high level, client/server failure, and basic concurrent execution. Retrieve precondition/postcondition, invariant, history, snapshot, commit record, idempotency key, authoritative state, and failure domain. The next modules derive anomalies, locking, MVCC, deadlocks, and isolation in detail; this chapter establishes the vocabulary and boundary discipline they depend on.

## Learning Objectives

After this module, you can:

1. define atomicity, consistency, isolation, and durability independently and reject common overclaims;
2. draw a transaction boundary across client, connection/session, database, storage engine, and external resources;
3. specify state invariants and show how constraints, application logic, and isolation jointly preserve them;
4. distinguish statement atomicity, savepoints/subtransactions, transaction commit, request completion, and workflow completion;
5. trace begin, reads, writes, validation, log/commit decision, acknowledgement, abort, and recovery states;
6. classify failure before commit, after commit, during acknowledgement, and during retry;
7. design stable idempotency, uniqueness, outbox, and reconciliation for ambiguous/external effects;
8. identify autocommit, implicit-commit, mixed-engine, pooling, cancellation, and long-transaction hazards;
9. define durability as a tested failure contract rather than a slogan; and
10. test boundaries through schedule, fault, crash, recovery, and invariant oracles.

## Core Exposition

**A transaction is a scoped state transition.** Let `S` be possible database states and `I:S→{true,false}` a declared invariant such as nonnegative balances and conservation for an internal transfer. Transaction `T` has preconditions and produces a tentative post-state. Correct application logic aims to establish

`I(s) ∧ pre_T(s) ⇒ I(T(s))`.

The database can enforce some invariants directly through type/domain, `NOT NULL`, `CHECK`, unique, foreign-key, exclusion, trigger, or assertion-like mechanisms. Others require reading multiple rows and choosing writes. Those reads and writes must occur in an isolation regime that makes the proof valid. Checking `I` in application memory before the transaction or against a snapshot permitting a conflicting commit can invalidate the reasoning.

**Atomicity.** During execution, a transaction may dirty pages, append log records, acquire locks, create versions, or expose its own writes to itself. Atomicity is about the committed outcome: either the transaction's database effects are accepted as a unit or they are aborted/undone/ignored during recovery. It does not require physical pages to change simultaneously. WAL and recovery can reconstruct the logical all-or-none result from non-simultaneous physical writes.

Statement atomicity is narrower than a multi-statement transaction. With autocommit, each successful statement may be its own transaction. If an application debits one account in statement one and credits another in statement two, a crash between them can commit only the debit. Explicitly delimiting both statements is necessary, though concurrent invariant preservation may additionally require locking or serializable validation.

A savepoint marks a point inside the current transaction. Rolling back to it discards later work while retaining earlier tentative work; releasing it does not make anything independently durable. Many frameworks call nested scopes “nested transactions” while implementing savepoints. Determine whether an inner commit is independent, merely releases a savepoint, or is prohibited. Only the outer commit may decide the local transaction.

**Consistency.** The C in ACID is not a database oracle for all business truth. It is the obligation that valid committed states transition to valid committed states under declared rules. The DBMS can enforce registered constraints and its own structural invariants. It cannot infer that a refund needs authorization, a ledger must balance across an unmodeled service, or an exchange rate is correct. Name each invariant, authority, inputs, time semantics, and enforcement mechanism.

Consistency also includes representation agreement. If a balance, ledger entries, idempotency record, and outbox fact must describe one decision, store them under one atomic boundary when possible. If a derived cache/search index is outside it, define lag, rebuild, version, and reconciliation. Do not label eventual repair “ACID consistency”; it is a separate convergence contract.

**Isolation.** Isolation constrains which effects of concurrent transactions may be observed and which histories may commit. Serializable means committed effects are equivalent to some serial order, not that the engine literally runs one transaction at a time. Weaker levels admit specified phenomena. Names differ in implementation: current PostgreSQL, for example, maps requested Read Uncommitted to Read Committed and provides behavior stronger than the standard minimum in some cases. Always use engine/version behavior, not the label alone.

Isolation does not mean an application can ignore retry. Deadlock victims, serialization failures, lock timeouts, cancellations, or failover can abort transactions. A correct serializable design includes a bounded whole-transaction retry policy with stable external identity. Retrying only the last statement can reuse stale reads and violate the transaction's decision logic.

**Durability.** A transaction becomes committed at an engine-defined durable decision point, normally protected by a log/commit protocol before data pages need reach their final locations. PostgreSQL documents WAL's rule that data-file changes need not be flushed on every commit when corresponding log records have been flushed. SQLite documents a concrete atomic-commit protocol shaped by rollback journal or WAL mode, filesystem and storage assumptions. Mechanism matters.

Durability is conditional on configuration and failures: synchronous-commit setting, storage acknowledgement, filesystem/device behavior, checksums, torn-write handling, replication quorum, region/fault independence, encryption/key availability, operator privilege, and recovery software. A local durable commit may still be absent from an asynchronous replica immediately. Replication can copy corruption or deletion. Backups provide a different historical recovery contract and require restore tests. Retention can deliberately remove durable data later.

**Draw the boundary.** For every use case, list:

1. authoritative resource manager/database and exact tables/partitions;
2. connection/session and storage engines participating;
3. begin/autocommit state, isolation/access mode, timeout, and retry identity;
4. reads establishing the decision and writes enforcing it;
5. constraints and invariant validation;
6. commit/abort point and acknowledgement semantics;
7. excluded effects—remote APIs, queues, files, caches, metrics, emails;
8. ambiguity, recovery, reconciliation, and owner.

A process, request, ORM unit-of-work, method, or tracing span is not automatically the transaction boundary. Inspect emitted SQL and connection behavior. Returning a connection to a pool with an open transaction can leak locks/snapshot/state into another request; robust code commits or rolls back on every exit and resets session characteristics.

**Autocommit and implicit boundaries.** Autocommit is useful for independent statements, but multi-step invariants need explicit delimitation. APIs may begin transactions implicitly. DDL and administrative statements vary: current MySQL documents statements that implicitly commit, often before and sometimes after execution, even though supported atomic DDL has its own internal atomicity. Mixing transactional and nontransactional tables can leave partial effects. Test the exact engine, storage engine, driver, and migration tool behavior.

Errors also vary. Some engines abort the entire transaction after certain errors; others roll back only a statement and leave the transaction usable. Constraint violation caught by application code does not prove all prior work was undone. Adopt explicit rollback-on-error discipline and verify driver state. Cancellation is an error path: whether the server observed it, rolled back, or completed commit can be ambiguous.

**Commit ambiguity.** Consider four points: before the server receives commit, while it decides/writes the commit record, after durable commit but before response, and after client receives success. A connection loss before an acknowledgement does not identify which point occurred. Treating “timeout” as “rollback” can duplicate a transfer on retry; treating it as success can omit a needed effect.

Use a stable operation/command ID chosen before the first attempt. In the same transaction as the authoritative effect, insert a unique deduplication/result record. Retry with the same ID; if present, return the recorded outcome rather than repeat. The request payload/actor/version should be bound to the identity so accidental key reuse with different intent is rejected. Expiry must outlive all legitimate retries or be reconciled with permanent business identity.

The finite model below stages balances, command results, and an outbox row in one copy. Commit validates conservation/nonnegativity before atomically replacing local state. Replay of the same command returns the stored result. Failure aborts the staged copy. It is an executable specification of a tiny local boundary, not a storage engine.

<!-- bijux-verify: {"id":"local-transaction-boundary","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"after_commit=(('checking', 45), ('savings', 55))\noutbox=(('tx-1', 'transferred 25'),)\nreplay_changed=False\nafter_abort=(('checking', 45), ('savings', 55))\noutbox_after_abort=(('tx-1', 'transferred 25'),)\ntotal=100\ninvariants=True\n","stderr":""}} -->
```python
class Database:
    def __init__(self) -> None:
        self.state = {
            "balances": {"checking": 70, "savings": 30},
            "commands": {},
            "outbox": [],
        }

    def transfer(self, command_id: str, source: str, destination: str, amount: int) -> bool:
        staged = {
            "balances": dict(self.state["balances"]),
            "commands": dict(self.state["commands"]),
            "outbox": list(self.state["outbox"]),
        }
        if command_id in staged["commands"]:
            return False
        if amount <= 0 or staged["balances"][source] < amount:
            raise ValueError("invalid transfer")
        staged["balances"][source] -= amount
        staged["balances"][destination] += amount
        message = f"transferred {amount}"
        staged["commands"][command_id] = message
        staged["outbox"].append((command_id, message))
        if min(staged["balances"].values()) < 0 or sum(staged["balances"].values()) != 100:
            raise AssertionError("invariant violation")
        self.state = staged
        return True


database = Database()
database.transfer("tx-1", "checking", "savings", 25)
after_commit = tuple(sorted(database.state["balances"].items()))
replay_changed = database.transfer("tx-1", "checking", "savings", 25)
try:
    database.transfer("tx-2", "checking", "savings", 80)
except ValueError:
    pass
after_abort = tuple(sorted(database.state["balances"].items()))
outbox = tuple(database.state["outbox"])

print(f"after_commit={after_commit}")
print(f"outbox={outbox}")
print(f"replay_changed={replay_changed}")
print(f"after_abort={after_abort}")
print(f"outbox_after_abort={outbox}")
print(f"total={sum(database.state['balances'].values())}")
print(
    "invariants="
    f"{after_commit == after_abort and len(outbox) == 1 and len(database.state['commands']) == 1}"
)
```

The copy assignment is atomic only within this single-threaded model. It omits SQL, MVCC, locks, logs, flushing, crashes, external delivery, concurrency, isolation, and performance. The outbox row means “committed fact awaiting publication,” not “message delivered.”

**External effects.** A database rollback cannot unsend an email, revoke a remote charge reliably, or erase an already acknowledged queue message. Calling a remote system inside a transaction also holds database resources across unbounded network latency and can return timeout after the remote committed. Unless resources participate in a deliberately engineered distributed atomic-commit protocol, assume separate commit boundaries.

For database state plus message publication, write the domain state and outbox record in one local transaction. A relay reads committed outbox rows, publishes with stable message identity, and marks/records progress. Crashes can cause retries, so consumers deduplicate or make effects idempotent under their own transaction boundaries. This yields one committed local fact plus at-least-once delivery attempts under named identities—not magical end-to-end exactly-once execution.

For long workflows, model explicit states, commands, events, timeouts, retries, and compensations. Compensation is a new business transaction, not time travel: inventory may no longer exist, exchange rates change, and external observers saw the original effect. Preserve audit facts and define which invariants hold at every intermediate state versus only at convergence.

**Boundary size.** Start the transaction before the reads on which the decision depends, but do nontransactional preparation outside where safe. Keep human think time, slow computation, and network calls outside. Inside: acquire/read the authoritative state under the chosen isolation, validate, write all coupled state, write deduplication/outbox, and commit. After commit: respond or publish derived effects. If post-commit response fails, stable identity resolves ambiguity.

Shorter transactions reduce lock/snapshot duration, deadlock surface, version retention, and retry work. But splitting an invariant-bearing decision merely to improve latency introduces partial commit. If work is too large, redesign the invariant and checkpointed workflow so each smaller transaction leaves a valid explicit state; do not pretend chunks form one atomic transaction.

**Verification.** A happy-path commit proves little. Test invariant property over generated states; concurrent schedules at the exact isolation; constraint conflicts; deadlock/serialization abort; error after each statement; rollback and savepoint behavior; connection loss before/during/after commit; process crash with durable recovery; retry with same/different identity; outbox crash before/after publish/mark; duplicate/out-of-order consumer messages; mixed resource/DDL behavior; long transaction cleanup impact; replica visibility; backup restore; and corruption/error injection supported by the system.

Observe transaction duration/open count, commits/rollbacks, abort reasons, deadlocks, serialization retries, lock waits, snapshot age, WAL/redo/fsync/commit latency, unknown outcomes, dedup hits/conflicts, outbox backlog/age/attempts, replica commit/apply lag, recovery time, constraint failures, and invariant/reconciliation discrepancies. Metrics need transaction/command identity without exposing sensitive payload.

## Definitions and Notation

- `S`: possible authoritative database states; `s_0` and `s_1` are pre/post states.
- `I(s)`: a declared invariant predicate; its authority and enforcement scope must be named.
- `T:S⇀S`: a transaction's partial state-transition function, undefined when preconditions fail.
- `H`: a concurrent history of reads/writes/commit/abort events; isolation defines admitted/observable histories.
- `commit(T)`: durable decision for local resource manager under its configured failure contract.
- `rid`: stable request/command identity stored transactionally with the authoritative result.
- `O`: transactional outbox relation; membership proves a local fact committed, not external delivery.
- **Atomicity:** committed outcome is all transaction effects or none.
- **Consistency:** valid transition preserves declared invariants under stated assumptions.
- **Isolation:** named constraints on concurrent visibility/history.
- **Durability:** acknowledged committed effects survive declared failures and recovery.
- **Linearization/serialization point:** abstract point/order explaining an operation/history; it need not be the client acknowledgement instant.
- **Ambiguous outcome:** client evidence cannot distinguish committed from aborted/not-run.

## Mechanisms, Invariants, or Proof Structure

The transfer proof assumes `amount>0`, sufficient source funds, a pre-state with nonnegative balances and total 100, and isolation preventing a conflicting decision from invalidating those reads. Subtracting and adding the same `amount` preserves total algebraically; the funds check plus atomic writes preserves nonnegativity. A unique transactional `rid` makes every retry observe the prior result or create exactly one local result. The proof fails if balance reads occur outside the protected boundary or two transactions can both validate stale funds and commit an inadmissible history.

Atomic recovery is a visibility proof, not simultaneous I/O: if no durable commit decision exists, recovery treats tentative changes as aborted/undoable; if it exists, redo/visibility installs the committed outcome according to the log protocol. Correctness depends on log ordering, stable storage assumptions, recovery idempotence, and corruption handling. This chapter does not re-prove a vendor implementation.

The outbox proof has two parts. Local atomicity guarantees `(domain_effect ∧ outbox_fact)` or neither. Relay retry plus stable identity guarantees attempts are not lost after eventual recovery, under retention/liveness assumptions. It does not guarantee one network delivery; a crash after broker acceptance before marking can duplicate. A consumer's transactionally stored message identity plus effect can guarantee one committed consumer effect within that consumer's local boundary.

Commit ambiguity is indistinguishability from the client: a dropped response can follow either pre-decision failure or post-decision success. No inference from timeout resolves it. Querying by stable identity/reconciling authoritative state adds evidence; blind retry without identity can create another valid transaction and duplicate the business effect.

## Alternatives and Trade-Offs

- **Autocommit versus explicit transaction:** autocommit is simple for independent statements; explicit grouping protects multi-statement decisions but adds duration/error responsibility.
- **Constraint versus application validation:** constraints serialize/enforce close to authority; application checks express rich policy but require correct isolation and can race. Combine them.
- **Pessimistic locking versus optimistic/serializable retry:** locking can prevent conflicting progress but blocks/deadlocks; validation/MVCC allows concurrency but aborts and requires whole-transaction retry.
- **Large transaction versus valid-state workflow:** one commit gives strong atomicity but large log/locks/rollback; smaller transactions scale only when every intermediate state is explicitly valid/recoverable.
- **Distributed atomic commit versus outbox/workflow:** atomic commit gives one decision across enlisted resources but adds coordination/blocking/recovery coupling; outbox/workflows expose intermediate states and require idempotency/compensation.
- **Synchronous replication versus asynchronous:** synchronous acknowledgement can widen failure survival but adds latency/availability coupling; asynchronous lowers commit latency but permits lag/data-loss windows under failover policy.
- **Savepoint versus abort/retry:** savepoints recover local subwork but retain the outer snapshot/locks and cannot erase external effects; full retry is simpler when the decision inputs may have changed.

## Failure Modes and Misconceptions

- “ACID means no concurrency bugs.” Only a named isolation implementation plus correct transaction logic addresses histories.
- “Consistency is supplied by the database.” The database enforces declared rules; unmodeled business invariants remain application design.
- “Atomicity means pages change simultaneously.” Logging/recovery can expose an atomic logical result from staged physical writes.
- “A successful statement is committed.” Explicit transactions commit only at their boundary; autocommit/implicit behavior must be known.
- “A released savepoint is durable.” It remains subordinate to outer abort.
- “Rollback undoes remote work.” It controls only enlisted transactional resources.
- “Timeout means failure.” Commit acknowledgement may have been lost after durable success.
- “Retry the failed line.” A concurrency abort invalidates the transaction's decision; retry the complete unit with stable identity.
- “Serializable means no retries.” Serialization enforcement commonly aborts a participant.
- “Durable means backed up forever.” Commit recovery, replicas, backups, retention, and disaster scope are distinct.
- “One request equals one transaction.” Connection, ORM, autocommit, and resource boundaries decide reality.
- “Longer transactions are safer.” They can protect more state but amplify contention, stale snapshots, cleanup delay, and retry cost.

## Worked Examples

### Example 1

Debit and credit execute under autocommit as two statements. The debit commits; the process crashes before credit. Each statement is atomic, but the transfer is not. Conclusion: statement atomicity cannot replace the required multi-statement boundary.

### Example 2

Inside one transaction, an order row succeeds, a savepoint is set, an optional audit enrichment fails, and rollback-to-savepoint removes only enrichment. Outer commit persists the order. Conclusion: savepoint controls tentative subwork; it neither creates an independent commit nor undoes outside effects.

### Example 3

Two doctors independently observe another on call and each marks themselves off under an isolation level admitting the history. Both local rows satisfy constraints, but the cross-row invariant fails. Conclusion: atomic commits and declared row constraints do not alone provide serializable invariant preservation.

### Example 4

The server durably commits `tx-1`, then the network drops its response. Retrying with `tx-2` transfers twice; retrying `tx-1` reads the stored result. Conclusion: stable identity resolves ambiguous outcomes; timeout classification does not.

### Example 5

An application sends an email, then its database insert violates uniqueness and rolls back. The email remains. Conclusion: external effect preceded authority and cannot be repaired by local atomicity; commit an outbox fact first.

### Example 6

Domain row and outbox row commit together. Relay publishes, crashes before marking, and republishes. Consumer records message ID and effect together, so the second attempt changes nothing. Conclusion: duplicates remain possible in transport while one committed local consumer effect is achievable.

### Example 7

A migration runs DML, then a MySQL DDL statement documented to cause implicit commit, then fails. Earlier DML is already committed despite an application rollback call. Conclusion: DDL transaction behavior is engine-specific and must be tested before migration design.

### Example 8

A transaction updates an InnoDB table and a nontransactional table, then rolls back. Only the transactional effect is undone. Conclusion: syntax-level transaction scope is not proof that every storage resource participates.

### Example 9

A checkout opens a transaction, calls a payment API for 30 seconds, then commits. It holds database resources while the remote result can be ambiguous independently. Conclusion: separate ownership boundaries; persist intent/outbox/workflow state and make remote commands idempotent.

### Example 10

A durable primary acknowledges commit, but an asynchronous replica has not replayed it. Immediate replica read returns old data. Conclusion: primary durability and cross-replica read-your-writes visibility are different contracts.

## Cross-Program Connections

- [Software Design and Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md) supplies aggregate invariants, ownership, and use-case boundaries.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) supplies request identity, deadlines, ambiguous responses, and public error contracts.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) supplies outbox/change capture, replay, reconciliation, and derived-state convergence.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies atomic commit, consensus, failure detectors, idempotency, and sagas.
- [Software Delivery and Reliability Engineering](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) supplies fault injection, SLOs, recovery drills, and safe rollout.

## References

1. PostgreSQL Global Development Group, [Transactions](https://www.postgresql.org/docs/current/tutorial-transactions.html), current transaction blocks, atomic grouping, and savepoint overview.
2. PostgreSQL Global Development Group, [Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html), current standard phenomena and PostgreSQL isolation behavior.
3. PostgreSQL Global Development Group, [SAVEPOINT](https://www.postgresql.org/docs/current/sql-savepoint.html), current partial rollback and release semantics.
4. PostgreSQL Global Development Group, [Write-Ahead Logging](https://www.postgresql.org/docs/current/wal-intro.html), current WAL durability and data-page flushing rationale.
5. SQLite Project, [Transaction](https://www.sqlite.org/lang_transaction.html), official automatic/explicit transactions, read/write behavior, and error handling.
6. SQLite Project, [Atomic Commit](https://www.sqlite.org/atomiccommit.html), official rollback-journal commit/recovery mechanism and storage assumptions.
7. Oracle, [MySQL 8.4 START TRANSACTION, COMMIT, and ROLLBACK](https://dev.mysql.com/doc/refman/8.4/en/commit.html), current autocommit and explicit transaction behavior.
8. Oracle, [MySQL 8.4 Statements That Cause an Implicit Commit](https://dev.mysql.com/doc/refman/8.4/en/implicit-commit.html), current boundary exceptions.
9. Jim Gray, [“The Transaction Concept: Virtues and Limitations”](https://jimgray.azurewebsites.net/papers/theTransactionConcept.pdf), *VLDB*, 1981, transaction properties and boundaries.
10. Theo Härder and Andreas Reuter, [“Principles of Transaction-Oriented Database Recovery”](https://research.ibm.com/publications/principles-of-transaction-oriented-database-recovery), *ACM Computing Surveys* 15(4), 1983, atomicity/durability and recovery taxonomy; DOI `10.1145/289.291`.

## Exercises

### Exercise 1

For order creation involving inventory, payment API, local order rows, an outbox, email, cache, and analytics, draw every authority/commit boundary. State which effects can share local ACID, which cannot, and invariants at each intermediate state.

### Exercise 2

Formally prove conservation/nonnegativity for a local transfer, then show a concurrent history that invalidates the proof under stale reads. State the isolation/locking or constraint mechanism needed.

### Exercise 3

Trace failures at eight points from transaction begin through WAL/commit acknowledgement, response, outbox publication, and consumer commit. For each, specify authoritative evidence, retry identity, duplicate possibility, and recovery action.

### Exercise 4

Design a robust application transaction wrapper across connection pooling, autocommit, savepoints, expected constraint errors, deadlock/serialization retry, cancellation, implicit-commit DDL, logging, and metrics.

### Exercise 5

Design a test and operational evidence program for a money-movement boundary, including generated invariants, schedules, crash recovery, storage/replica failure, ambiguous commit, outbox/consumer duplication, backup restore, and limitations.

## Answers to the Exercises

### Answer 1

Local order, reservation/intention state, stable command result, and outbox can share one database transaction only if they use the same transactional resource manager. Payment acceptance is the payment provider's commit; email provider acceptance, cache write, and analytics ingestion are separate. Begin by persisting order/payment intent and outbox command under one local commit. A worker invokes payment with stable provider idempotency identity, then records observed outcome through another local transaction; model unknown outcome explicitly and reconcile by provider identity. Publish committed order facts through outbox; consumers deduplicate. Email/cache/analytics failures do not roll back the order. Invariants: no order is silently both payable and abandoned; one local result per command; reservation state is explicit; money/inventory authority is never inferred from a timeout; every committed external intent is retryable/reconcilable; compensation is a new state transition.

### Answer 2

Let source `a≥x>0`, destination `b≥0`, total `K=a+b`. Post-state is `a'=a-x≥0`, `b'=b+x≥0`, and `a'+b'=a-x+b+x=K`; atomic commit exposes pre or post. With two transactions reading `a=10`, each validates transfer `x=8`, then both independently write based on stale state or otherwise commit an admitted lost-update/write-skew-like history, the assumed pre-state is not exclusive and aggregate obligations can fail. Protect the decision with row locking/atomic conditional update, serializable isolation with whole-transaction retry, or a database constraint/mechanism capable of enforcing the exact invariant. A check performed before the transaction is insufficient. State the engine's actual history rules; “ACID” alone does not supply the premise.

### Answer 3

Before begin/first write, retry is safe with same identity. After tentative writes but before commit decision, abort/recovery removes them. During commit, connection loss is ambiguous: query stable `rid`/authoritative result or retry same identity, never invent a new ID. After durable commit before response, same-ID retry returns stored result. After response, client records success but may still repeat; dedup handles it. After outbox commit before publication, relay finds backlog. After broker acceptance before publisher mark, duplicate publication is possible. After consumer effect before acknowledgement/offset, duplicate delivery is possible; consumer stores message ID and effect atomically. Evidence includes database command/result/outbox rows, commit/recovery status where exposed, broker identity, consumer inbox/effect, and reconciliation—not absence of a response. Every retry is bounded/backed off and poison/unknown cases escalate without guessing.

### Answer 4

Acquire one known-reset connection, begin explicitly with named isolation/access mode/timeouts, and ensure all decision reads/writes use it. The wrapper invokes a side-effect-free transaction function and commits only after all constraints/outbox/dedup state pass. On every exception/cancellation path, issue rollback and discard/reset a suspect connection before pooling. Use savepoints only for documented recoverable subwork; release is not commit. Classify expected constraint conflicts into domain results; deadlock/serialization failures abort and retry the entire function with stable command identity, fresh reads, bounded attempts/jitter/deadline. Connection loss during commit becomes unknown and resolves by identity. Prohibit remote calls and implicit-commit DDL inside ordinary wrappers; migrations use separately tested semantics. Emit duration, attempt, outcome/unknown, abort class, waits, and identity hash without payload. Test driver error states and pool leakage.

### Answer 5

Define conservation, nonnegativity, one command result, ledger/balance agreement, authorization/currency/rounding, and outbox correspondence as executable oracles. Generate valid states/amounts plus invalid boundaries; run concurrent schedules for same/different accounts under the selected isolation and verify serializable/reference outcomes. Inject errors after every statement and savepoint; deadlocks, serialization aborts, cancellation, timeout, connection loss around commit; process/host crash before/after durable decision; torn/corrupt storage only through supported harness; replica loss/lag/failover under declared configuration. Repeatedly restore and reconcile WAL/log, balances, commands, outbox, consumer inbox/effects. Test publisher/consumer crashes around accept/mark/commit and duplicate/out-of-order delivery. Restore backups to measured RPO/RTO and verify keys/config. Report engine/version, durability settings, failure scope, unavailable destructive tests, statistical coverage, and that internal tests do not prove payment-provider or external exactly-once guarantees.
