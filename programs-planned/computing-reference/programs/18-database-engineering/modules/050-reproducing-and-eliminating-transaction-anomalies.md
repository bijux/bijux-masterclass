---
module_id: DBE-050
program: Database Engineering
level: 1
module_number: 50
title: Reproducing and Eliminating Transaction Anomalies
status: complete
last_verified: 2026-08-30
---

# Reproducing and Eliminating Transaction Anomalies

## One-Page Review

### Governing question

How can engineers turn a suspected transaction anomaly into a deterministic, minimal, portable-enough experiment and then prove that a repair eliminates the unsafe history without introducing unhandled failure behavior?

### Essential definitions

A **transaction test** controls multiple real sessions, their transaction boundaries, and a partial order of operations. A **schedule** is one concrete interleaving that preserves each session's program order. A **barrier** releases operations only after named observations or waits occur; a sleep merely guesses at timing. An **observable history** records invocations, responses, versions/read-from information where available, commits, aborts, errors, and relevant real-time order. An **oracle** decides whether the history satisfies a declared isolation model, serial specification, or domain invariant. A **witness** is a history that falsifies a claim; **shrinking** removes irrelevant operations/data while preserving failure. A repair is **eliminating** only when unsafe schedules are prevented or rejected and every new abort/block/retry path is handled correctly.

### Central model, mechanism, or theorem

Testing is a refinement loop: claim → executable transaction programs → controlled schedule → complete observation → independent oracle → minimized witness → mechanism repair → adversarial regression. A passing schedule proves only that execution. A failing schedule disproves any universal claim that includes it. Systematic exploration is finite evidence unless the explored state space is complete under stated bounds; randomized stress estimates discovery ability, not absence of anomalies.

### Critical invariants

- Each logical session owns a distinct connection; pooling never silently changes the session mid-transaction.
- Setup, isolation, autocommit, snapshot acquisition, SQL, parameters, and teardown are explicit and reproducible.
- Barriers synchronize logical events or known waits, never elapsed-time hopes.
- Observations preserve operation identity, read values/versions, affected rows, outcomes, errors, and final state.
- The oracle is independent of the implementation path being tested and covers returned values, not just final rows.
- Expected blocking has a controlled release; every test has bounded cancellation and cleanup.
- Repair tests assert permitted outcomes: safe commit, constraint rejection, blocking into safe state, or retriable abort.
- Retried attempts use fresh reads and stable external operation identity; no aborted result escapes.

### Common failures

Failures include sharing one connection between supposed transactions; relying on sleeps; omitting explicit isolation; testing a mock/in-memory substitute; observing only final rows; treating timeout as proof of correct blocking; accepting any error as prevention; forgetting autocommit; reusing state across schedules; assuming an engine label is portable; failing to capture versions/outcomes; shrinking away the predicate that caused the bug; testing the database but not the retry loop; disabling durability or constraints unlike production without labeling; and claiming no anomaly because random stress did not find one.

### Compact example

Two transactions implement `read counter; write counter+1`. There are six interleavings that preserve each transaction's read-before-write order. Four let both read 0 and finish at 1, losing one increment; two serial schedules finish at 2. A deterministic harness forces `T1:R0, T2:R0, T1:W1, T2:W1`, records both committed logical operations, and compares final 1 with serial oracle 2. Replacing the split program with atomic `counter=counter+1` leaves two operation orders and both finish at 2. The repair test must also cover constraints, returned values, retry, and the actual target engine.

### Connections

Retrieve [Read and Write Anomalies](042-read-and-write-anomalies.md), [Isolation Levels](048-isolation-levels.md), and [Serializable Snapshot Isolation](049-serializable-snapshot-isolation.md). Continue through the Database Engineering [roadmap](../ROADMAP.md) to Level II query processing, optimization, recovery, replication, and operational correctness.

## Governing Question

What evidence is strong enough to reproduce a concurrency failure, distinguish engine behavior from harness artifacts, and justify that a chosen repair closes the entire invariant-bearing conflict domain?

## Why This Matters

Concurrency bugs often disappear under a debugger and reappear under production timing. A log says two requests overlapped, but not what each read, whether a statement blocked, which version was returned, or whether commit succeeded. A test with `sleep(0.1)` passes on one machine and races on another. A fix adds serializable isolation, but the application swallows `40001` and loses work. Without a disciplined evidence model, teams oscillate between irreproducible incidents and overly broad locking.

A deterministic transaction test converts timing into a partial order. Each session pauses after a named step; the controller releases the next operation when the required logical state is established. The experiment records enough history to reconstruct dependencies and compare outcomes with a serial or domain oracle. Once a witness is stable, shrinking exposes the smallest conflict and prevents incidental details from dictating the repair.

Elimination is broader than making the old script green. A correct remedy can transform an unsafe double commit into blocking, a uniqueness/constraint error, a serialization failure, a zero-row compare-and-set result, or a safe merged value. The application must interpret that outcome correctly. The test suite must therefore include the production transaction wrapper, connection pool, retry boundary, idempotency/outbox behavior, cancellation, and ambiguous commit handling.

Current systems provide useful but different harnesses. PostgreSQL's source tree includes an isolation tester with named sessions, steps, permutations, wait detection, setup/teardown, and expected output. Hermitage expresses classic anomaly schedules across multiple products. Elle infers dependency anomalies from client-observed histories designed to expose version order. None is a universal oracle: PostgreSQL's wait detection is implementation-specific, Hermitage cases are finite, and Elle explicitly scopes the observations and anomaly classes it can infer.

## Prerequisites and Retrieval

You should understand transactions, sessions/connections, autocommit, isolation levels, MVCC versions, locks/waits/deadlocks, read/write anomalies, serialization graphs, invariants, retries, idempotency, and test oracles. Retrieve partial order, interleaving, barrier, linear extension, read-from relation, commit/abort, serial reference model, predicate domain, false positive/negative, shrinking, fault injection, and flakiness.

DBE-041 through DBE-049 supplied transaction boundaries, anomaly names, locks, 2PL, deadlocks, MVCC, visibility, isolation, and SSI. This module integrates them into a reproducible verification workflow. Later modules will reuse the same evidence discipline for optimizer races, recovery, replication, online schema change, and distributed histories.

## Learning Objectives

After this module, you can:

1. translate an invariant and transaction program into explicit concurrent test steps;
2. generate or select schedules while preserving per-session order;
3. use barriers, hooks, and known-wait detection instead of sleeps;
4. capture a history sufficient for anomaly and serializability analysis;
5. construct independent serial, invariant, and model-specific oracles;
6. minimize a failing schedule without erasing its causal conflict;
7. compare database versions/configurations without false portability claims;
8. verify locks, constraints, atomic DML, compare-and-set, and serializable retry repairs;
9. extend tests across cancellation, deadlock, crash, ambiguous commit, and external effects; and
10. turn minimized incidents into stable regression, CI, canary, and production evidence.

## Core Exposition

**Begin with a falsifiable claim.** “Transactions are safe” cannot drive a test. State the transaction program, initial state, invariant, intended isolation, and observable result. Example: two committed `increment` operations starting from zero must return/leave the same result as applying `x:=x+1` twice serially, namely 2. Or: after any committed doctor-off-call transactions, `A+B>=1`. Include absent rows and predicates in the state domain.

Write the serial reference before the concurrent harness. For deterministic transactions over finite test data, enumerate serial orders and compute allowed reads/returns/final states. For commutative operations, define the algebra; for unique allocation, define a single-owner invariant; for reports, define a coherent-snapshot condition. A database constraint can serve as an additional oracle but should not be the only implementation-independent explanation.

**Separate program order from schedule order.** If T1 has steps `r1,w1,c1`, every legal schedule retains that order, while interleaving T2's steps. The controller chooses a linear extension of the per-session partial orders. Exhaustive enumeration grows combinatorially: two sequences of lengths m and n have `(m+n)!/(m!n!)` interleavings before blocking/outcome branches. Use equivalence reduction, targeted boundaries, small models, and randomized exploration rather than pretending a large state space was exhausted.

The executable finite model enumerates every interleaving of two two-step read-then-write increments. It records one minimized lost-update witness and compares a repaired atomic-operation model.

<!-- bijux-verify: {"id":"lost-update-schedule-exploration","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"split_schedules=6\nsplit_anomalies=4\nminimal_witness=('T1:R0', 'T2:R0', 'T1:W1', 'T2:W1')\nminimal_final=1\nserial_oracle=2\natomic_schedules=2\natomic_anomalies=0\nevidence=exhaustive_bounded_schedule_model\n","stderr":""}} -->
```python
def interleavings(left, right, prefix=()):
    if not left and not right:
        return (prefix,)
    schedules = ()
    if left:
        schedules += interleavings(left[1:], right, prefix + (left[0],))
    if right:
        schedules += interleavings(left, right[1:], prefix + (right[0],))
    return schedules

def run_split(schedule):
    value = 0
    observed = {}
    trace = []
    for transaction, operation in schedule:
        if operation == "R":
            observed[transaction] = value
            trace.append(f"{transaction}:R{value}")
        else:
            value = observed[transaction] + 1
            trace.append(f"{transaction}:W{value}")
    return value, tuple(trace)

split = interleavings((('T1', 'R'), ('T1', 'W')), (('T2', 'R'), ('T2', 'W')))
bad = tuple((trace, final) for final, trace in map(run_split, split) if final != 2)
atomic = interleavings((('T1', 'I'),), (('T2', 'I'),))
atomic_finals = tuple(sum(operation == 'I' for _, operation in schedule) for schedule in atomic)

print(f"split_schedules={len(split)}")
print(f"split_anomalies={len(bad)}")
print(f"minimal_witness={bad[0][0]}")
print(f"minimal_final={bad[0][1]}")
print("serial_oracle=2")
print(f"atomic_schedules={len(atomic)}")
print(f"atomic_anomalies={sum(final != 2 for final in atomic_finals)}")
print("evidence=exhaustive_bounded_schedule_model")
```

This model assumes reads/writes are indivisible, both logical operations succeed, one scalar item exists, and no locks, versions, aborts, retries, failures, or database product semantics intervene. “Exhaustive” applies only to its six explicitly bounded interleavings, not arbitrary programs or real schedulers.

**Use real sessions and controlled barriers.** A database transaction is connection-scoped in most APIs. Lease two independent physical connections; disable/declare autocommit; set isolation at the documented point; begin; verify settings; execute exact SQL and parameters. A shared connection serializes operations or corrupts protocol use, while a pool can silently move later work to another session if the transaction handle is not pinned.

A barrier records arrival after a logical event such as “both decision SELECTs returned.” Only then does it release writes. For blocking tests, launch the potentially blocking operation asynchronously, observe a documented wait state or a server hook, perform the releasing commit/rollback, and join the blocked operation. Every wait has a deadline and cancellation path. A timeout alone says only that something failed to finish.

Avoid sleeps as ordering evidence. Sleep can be useful after ordering is already established—for example, holding a lock for observation—but never proves which statement ran first. Instrumented failpoints/hooks are strongest for engine tests; external clients can use advisory coordination tables/channels when those do not alter the conflict being studied.

**Capture complete observations.** For every operation record stable test/run, logical transaction, attempt, session/backend, step, invocation/completion order, statement kind, sanitized parameters, returned value/version, affected-row count, error class/code, and transaction outcome. Capture configured isolation, engine/build, storage mode, schema/indexes, query plan where relevant, autocommit, and snapshot/transaction identifiers exposed safely.

Do not infer commit from a successful final statement; record commit response. Connection loss during commit is ambiguous, not abort. Do not infer read-from solely from equal values; repeated values need version tags or traceable datatypes. Elle deliberately uses traceable objects such as append-only lists so client observations constrain version order. History design and oracle capability are coupled.

Final state is necessary but insufficient. Lost updates may show final corruption, but dirty/intermediate reads can cause external decisions even if the writer later aborts and state returns. Serializability includes observed returns. A queue test must record which worker claimed which job; a uniqueness test records success/error identity; a report test records the entire coherent tuple/set.

**Choose layered oracles.** A domain invariant answers whether the business state is legal. A serial oracle enumerates allowed transaction orders and returned values. An anomaly oracle classifies dirty/nonrepeatable/phantom/lost-update/read-skew/write-skew evidence. A dependency oracle constructs `wr`, `ww`, `rw` edges when observations justify them. A mechanism oracle checks expected blocking, abort code, affected rows, or constraint rejection. No single layer substitutes for all others.

Independence matters. If application code calculates the expected balance using the same stale object/method as production, the test can repeat the bug. Implement small mathematical models, SQL constraints, or separate algorithms. Validate the checker with planted safe and unsafe histories; a checker never exercised against known counterexamples is weak evidence.

**Reproduce before repairing.** Preserve the original engine version, configuration, schema/indexes/statistics, driver, pool, isolation, and SQL shape where practical. Start with the smallest realistic data. Force the suspected order multiple times; require the old system to produce the precise witness, not merely “sometimes fails.” If the incident cannot be reproduced, retain it as an unconfirmed hypothesis and strengthen telemetry; do not invent certainty.

Cross-engine matrices need separate expected outcomes. The same label can use different locking/snapshot rules. Treat blocked, aborted, and committed results according to each documented contract. Record unavailable products/configurations rather than silently substituting SQLite or an in-memory mock for PostgreSQL, InnoDB, or SQL Server.

**Shrink without laundering causality.** Remove transactions, operations, rows, indexes, triggers, and failures one at a time while rerunning the oracle. Preserve per-session order, outcomes, the conflict predicate, and the failing observation. Normalize irrelevant generated IDs/timestamps. The minimal witness should still answer which versions were read, why both decisions were admitted, and which invariant/serial result failed.

Some context is causally essential despite appearing large: an index plan determines predicate locking; a trigger performs the hidden write; a retry creates duplication; a failover produces ambiguity. Keep the smallest causal environment, not the shortest SQL file.

**Repair the conflict domain.** For a single arithmetic item, atomic DML may eliminate split read/write schedules. Compare-and-set protects a named version and turns conflict into zero affected rows. A native unique/exclusion/check/foreign-key constraint rejects representable invalid states. Locking protects rows/ranges/guards actually locked. Serializable isolation rejects nonserial histories but requires whole-transaction retry. Schema redesign can materialize a predicate into an authoritative guard or allocate unique capacity units.

For every repair, state how unsafe schedules change. They may serialize, one transaction may reread safe state, one may abort/retry, or a constraint may reject it. “The test no longer reaches the line” is not an oracle. Also test unrelated transactions still progress, lock ordering does not create unacceptable deadlock, retry load remains bounded, and indexes cover intended predicates.

**Test the failure interface.** Force deadlock and serialization victims; verify exact retryable classification, rollback, connection cleanup, fresh reads, bounded attempts, jitter/deadline, and exhaustion response. A stable idempotency key remains constant across attempts. Insert an outbox record in the same transaction and prove only a committed attempt publishes once. Inject cancellation before begin, during read, during blocked write, after server commit but before client acknowledgement, and during retry delay.

Ambiguous commit requires durable operation lookup/reconciliation, not blind replay with a new identity. Crash testing distinguishes client/process/database/host failures and durability settings. A transaction anomaly test with durability disabled proves isolation mechanics only; label that evidence and run target durability/recovery lanes separately.

**Combine deterministic and generative testing.** Keep one minimized deterministic regression per discovered mechanism. Systematically enumerate small schedules/state with model checking or a custom explorer. Generate longer concurrent histories and check them offline. Inject realistic faults where the claimed model covers them. Use seed recording and shrinking for randomized runs. Coverage dimensions include transaction types, conflict keys/predicates, data cardinality, isolation, plans/indexes, commit order, abort/retry, and failure point.

PostgreSQL's isolation tester illustrates named steps and explicit permutations; it can also enumerate interleavings subject to session order. Its known-wait detection is tied to heavyweight locks and needs annotations for timing/report stabilization, so do not copy that assumption to every wait mechanism. Hermitage provides reusable finite anomaly patterns across engines. Elle provides sound inference for declared observable histories and datatypes, while noting limitations such as predicate inference. Match tool proof boundaries to the claim.

**Promote evidence carefully.** Run deterministic regressions on every relevant code/schema/configuration change. Run bounded matrix/generative suites nightly or before release. Canary engine upgrades and isolation changes with shadow/reconciliation or privacy-safe histories. Monitor invariant violations, constraint conflicts, zero-row CAS, deadlocks, serialization failures, retry depth/exhaustion, ambiguous outcomes, long transactions/snapshots, waits, and tail latency by transaction class.

No anomalies observed is not proof of universal correctness. Report schedules/models/versions covered, seeds and runtime, untested fault modes, and checker limitations. A discovered counterexample is strong: it refutes the claim in scope and becomes a permanent minimized regression.

## Definitions and Notation

- **Program order:** required order of operations within one transaction/session.
- **Schedule/history:** an interleaving/record of operations and outcomes; usage must state whether invocations/responses and versions are included.
- **Linear extension:** total order consistent with a partial order.
- **Barrier:** synchronization point released by named logical conditions.
- **Witness:** concrete observed history falsifying a stated guarantee or invariant.
- **Oracle:** independent decision procedure for allowed histories/results.
- **Serial oracle:** results produced by all permitted serial orders of the transaction programs.
- **Read-from relation:** mapping from a read to the write/version it observed.
- **Shrinking:** reducing a failing case while preserving the oracle failure.
- **Ambiguous commit:** client cannot tell whether commit became durable.
- **Evidence scope:** exact engine/version/configuration/model/schedules/faults for which observations apply.
- `C(m+n,m)`: number of interleavings of two fixed sequences of lengths m,n before outcome pruning.

## Mechanisms, Invariants, or Proof Structure

A deterministic witness proof has five parts: establish initial state S0; establish each transaction's program and isolation; force schedule H while preserving program order; record successful outcomes/read-from evidence; show oracle O rejects H. For lost increment, both operations commit, both reads return 0, both writes store 1, and final 1 differs from every serial composition result 2.

An elimination proof quantifies over the tested schedule set: for each schedule, the repair either commits an oracle-accepted result or rejects/blocks/retries according to the declared interface. For atomic increments in the finite model, each transaction is one indivisible step, both two-operation orders produce 2, and the anomaly count is zero. This does not prove the real SQL implementation atomic; that requires target-engine evidence.

Exhaustive bounded exploration is proof only under its abstraction and bounds. A failing case transfers to the real system when the observed operations/refinement match; a passing abstract model transfers only with a simulation/refinement argument. Randomized absence supplies no universal quantifier. State these directions explicitly.

## Alternatives and Trade-Offs

- **Sleep versus barrier/hook:** sleeps are simple but nondeterministic; logical barriers/hooks give reproducible order at instrumentation cost.
- **Hand schedule versus exhaustive small exploration:** hand cases target known risks; enumeration finds combinations but grows combinatorially.
- **Black-box history versus engine instrumentation:** black-box matches client observables and portability; internals expose versions/waits but couple to implementation.
- **Domain oracle versus dependency checker:** domain oracle catches business harm; graph checker classifies general isolation but needs sufficient version evidence.
- **Mock/model versus real engine:** models explore cheaply and independently; only target engines prove SQL/locking/version/configuration behavior.
- **Atomic/constraint repair versus locking/serializable:** exact local mechanisms can be cheaper; broad dynamic invariants may require predicate conflict or serializable retry.
- **Per-change versus nightly/fault matrix:** fast deterministic tests protect review; expensive generative/failure suites broaden evidence outside the critical loop.

## Failure Modes and Misconceptions

- “Concurrent tasks mean concurrent transactions.” One physical connection may serialize them.
- “A short sleep orders operations.” Scheduler/load variance makes it a probability, not a happens-before fact.
- “The final row is correct.” Returned values or external actions may still reflect an invalid history.
- “Any exception prevents the anomaly.” It may be a harness timeout, syntax error, or lost connection with ambiguous commit.
- “Serializable made the test pass.” The application must retry the entire transaction and suppress aborted effects.
- “All schedules were tested.” State the finite bound and abstraction; real engines add outcome branches.
- “Same isolation name means same expectation.” Bind engine, version, storage/configuration, and statement type.
- “A mock database is faster evidence.” It proves the mock, not target concurrency semantics.
- “Random stress passed overnight.” Discovery probability is not universal correctness.
- “Minimal means fewest SQL characters.” Preserve the causal predicate, plan, trigger, retry, and failure boundary.
- “Lower abort count means safer.” It may mean weaker detection or bypassed transactions.
- “One regression test proves elimination.” Pair the witness with mechanism coverage, adversarial variants, retries, and production evidence.

## Worked Examples

### Example 1

Two async functions share one connection and appear to overlap, but the driver queues commands. No database concurrency occurred. Conclusion: use distinct pinned physical connections and record backend/session identities.

### Example 2

Both transactions read counter 0 behind a barrier, then write 1 and commit. Serial oracle is 2. Conclusion: the exact four-operation witness proves lost update for that SQL/engine/configuration.

### Example 3

Replacing read-then-write with `SET value=value+1` yields final 2, but the test ignores returned values. Conclusion: assert affected rows and returned committed values as well as final state.

### Example 4

T1's update blocks; a 200 ms timeout fires and the test declares correct locking. The server was actually stalled on I/O. Conclusion: observe a documented lock wait and then release it deliberately.

### Example 5

Two empty range checks admit overlapping reservations. Adding row locks on returned rows changes nothing. Conclusion: the minimized witness preserves the empty predicate and motivates range/predicate, guard, exclusion, or serializable protection.

### Example 6

PostgreSQL aborts a serializable transaction with `40001`; MySQL repeatable read instead commits a product-specific history. Conclusion: use per-engine expected outcomes and never normalize labels into false equivalence.

### Example 7

An index removal changes a range scan to a full scan and serialization aborts rise. Correctness remains, precision changes. Conclusion: include schema/statistics/plan fingerprints and capacity oracles in regressions.

### Example 8

A property test finds an anomaly after seed 91827 with 40 operations. Shrinking reduces it to two transactions and four steps. Conclusion: retain seed, original history, minimized witness, checker version, and shrink log.

### Example 9

Connection loss occurs during commit; retry with a new request ID creates a second allocation. Conclusion: classify outcome ambiguous and query stable durable operation identity before replay.

### Example 10

A serializable repair prevents invalid rows but retries raise p99 beyond the SLO under a hot tenant. Partitioned guard keys and admission control reduce overlap while invariant tests remain green. Conclusion: correctness is non-negotiable; contention design optimizes the cost of preserving it.

## Cross-Program Connections

- [Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) supplies happens-before, barriers, schedule exploration, race detection, and deterministic schedulers.
- [Software Engineering Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) supplies property testing, shrinking, differential testing, fault injection, and evidence labeling.
- [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) supplies partial orders, combinatorial interleavings, graph oracles, and state-space reduction.
- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) supplies traceable histories, immutable logs, sets/maps, and graph representations.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies linearizability/serializability checking, nemesis design, ambiguous outcomes, and history analysis.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) supplies hermetic environments, CI matrices, observability, capacity gates, and reproducible artifacts.

## References

1. PostgreSQL Global Development Group, [Isolation Tests README](https://github.com/postgres/postgres/blob/master/src/test/isolation/README), current source documentation, retrieved 2026-08-30; sessions, steps, permutations, known waits, and deterministic expected output.
2. Martin Kleppmann and contributors, [Hermitage: Testing Transaction Isolation Levels](https://github.com/ept/hermitage), retrieved 2026-08-30; finite cross-database anomaly schedules and observed outcomes.
3. Kyle Kingsbury and Peter Alvaro, [“Elle: Inferring Isolation Anomalies from Experimental Observations”](https://www.vldb.org/pvldb/vol14/p268-alvaro.pdf), *PVLDB* 14(3), 2021; observable histories, version inference, sound anomaly detection, and limitations.
4. Atul Adya, [*Weak Consistency: A Generalized Theory and Optimistic Implementations for Distributed Transactions*](https://publications.csail.mit.edu/lcs/pubs/pdf/MIT-LCS-TR-786.pdf), MIT PhD thesis, 1999; history and dependency definitions.
5. Hal Berenson et al., [“A Critique of ANSI SQL Isolation Levels”](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr-95-51.pdf), Microsoft Research Technical Report MSR-TR-95-51, 1995; anomaly phenomena and snapshot-isolation counterexamples.
6. PostgreSQL Global Development Group, [Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html), PostgreSQL 18 current documentation, retrieved 2026-08-30; product behavior and retry requirements.
7. Oracle, [MySQL 8.4 InnoDB Transaction Isolation Levels](https://dev.mysql.com/doc/refman/8.4/en/innodb-transaction-isolation-levels.html), current documentation, retrieved 2026-08-30; cross-engine snapshot and locking behavior.
8. Microsoft, [SET TRANSACTION ISOLATION LEVEL](https://learn.microsoft.com/en-us/sql/t-sql/statements/set-transaction-isolation-level-transact-sql?view=sql-server-ver17), current SQL Server documentation, retrieved 2026-08-30; locking and row-versioned configurations.
9. SQLite Project, [Isolation In SQLite](https://www.sqlite.org/isolation.html), current documentation, retrieved 2026-08-30; serialized writes, WAL snapshots, and promotion failure.
10. PostgreSQL Global Development Group, [Serializable Transaction Isolation Regression Specifications](https://github.com/postgres/postgres/tree/master/src/test/isolation/specs), current source tests, retrieved 2026-08-30; executable engine regression cases and expected scheduling conventions.

## Exercises

### Exercise 1

Enumerate the six legal schedules for two `read; write+1` transactions, compute reads/writes/final values, and classify each against serial oracle 2.

### Exercise 2

Design a two-session deterministic write-skew test for an at-least-one-doctor invariant, including barriers, exact observations, expected outcomes under SI and serializable execution, timeouts, and cleanup.

### Exercise 3

Given an incident log with equal values but no version IDs, partial timestamps, one connection ID, and a client timeout during commit, state which anomaly claims are supported, contradicted, or unverifiable and what stronger evidence is needed.

### Exercise 4

Compare atomic DML, compare-and-set, guard locking, native constraint, and serializable retry as repairs for a tenant quota. Define the conflict domain and a regression matrix for each.

### Exercise 5

Design a release-grade transaction correctness program across PostgreSQL and MySQL, covering deterministic witnesses, generative histories, engine/version/configuration matrices, retries, ambiguous commit, crash/failover, CI/canary evidence, privacy, and claim limitations.

## Answers to the Exercises

### Answer 1

Preserving each read before its write gives: `R1 W1 R2 W2` and `R2 W2 R1 W1`, which read 0 then 1 and finish 2; and `R1 R2 W1 W2`, `R1 R2 W2 W1`, `R2 R1 W1 W2`, `R2 R1 W2 W1`, where both read 0 and each writes 1, finishing 1. Thus four of six schedules violate the serial functional result 2. This assumes indivisible scalar reads/writes and both logical operations commit; a real database test must record versions, isolation, SQL semantics, outcomes, and returned values.

### Answer 2

Seed A=B=1 with constraint oracle `A+B>=1`. Pin two connections, set/verify target isolation, begin both, and barrier after T1 reads B and T2 reads A (or both read both). Release disjoint updates A=0 and B=0, then commits in controlled alternative orders. Record engine/version/configuration, backend IDs, snapshots/versions where available, reads, affected rows, waits, errors/SQLSTATE, commit outcomes, and final state. Under plain SI, the expected witness where supported is both commits and `(0,0)`; under serializable, require not all unsafe attempts commit—one may block into safe observation or abort with documented retry class. Bound waits, cancel/join, roll back survivors, and reset per schedule. Finally exercise whole retry and require a committed `(0,1)` or `(1,0)` without escaped aborted results.

### Answer 3

Equal values do not identify read-from versions, partial client timestamps do not establish server operation order, and one connection ID suggests there may have been no concurrent database sessions. The timeout does not establish abort because commit may be ambiguous. Therefore dirty/lost-update/write-skew/serializability classifications are unverifiable; final invariant failure, if independently recorded after outcomes settle, may support domain harm but not mechanism. Gather distinct backend/session IDs, exact isolation/autocommit, invocation/response events, transaction IDs/snapshots or traceable values, SQL/parameters/affected rows, server wait/error logs, explicit commit responses, and durable operation lookup after timeout. Reproduce with barriers before assigning an anomaly name.

### Answer 4

The conflict domain is every qualifying reservation for one tenant/period, including absent future rows and all write paths. Atomic DML works if quota is one authoritative aggregate updated conditionally; test concurrent increments, boundary equal limit, zero affected rows, and overflow. CAS protects a versioned aggregate but requires recompute/reject; test stale versions and retry. Guard locking serializes one tenant-period row; test empty reservations, lock order/deadlock, hotspot, and missing guard. A native constraint is ideal if capacity/nonoverlap is exactly representable; test every insertion/update path and concurrent constraint errors. Serializable covers dynamic predicates if all participants use it; test write skew, `40001`, whole retry, exhaustion, and bypass writers. Every matrix includes unrelated keys for progress, plans/indexes, cancellation, ambiguous commit, idempotency/outbox, and invariant reconciliation.

### Answer 5

Inventory transaction programs, invariants, predicates, SQL/read types, drivers/pools, external effects, and target versions/configuration. Keep minimized deterministic dirty/nonrepeatable/phantom/lost-update/read-skew/write-skew/deadlock cases per engine with separate expected outcomes. Generate traceable histories with recorded seeds; validate the checker on planted safe/unsafe cases, shrink failures, and state predicate/version limitations. Test production transaction wrappers for pinned connections, isolation verification, complete retry, stable idempotency, outbox, cancellation, exhaustion, and commit ambiguity. Add database-process/host crash and failover lanes under production durability/replication, distinguishing isolation-only fast lanes. CI runs narrow witnesses; nightly/release runs version/configuration/plans and fault matrices; canary gates invariant reconciliation, constraint/CAS conflicts, deadlock/serialization/retry/exhaustion, ambiguous outcomes, waits, snapshots, pools, p99, lag, and resources. Sanitize values while preserving operation/version identity. Report exact schedules, seeds, runtime, unavailable systems, and that passing finite/observational tests cannot prove all histories, engine defect absence, or cross-system atomicity.
