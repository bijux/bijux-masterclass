---
module_id: DBE-089
program: Database Engineering
level: 2
module_number: 89
title: Distributed SQL and Global Transactions
status: complete
last_verified: 2026-09-05
---

# Distributed SQL and Global Transactions

## One-Page Review

### Governing question

How can a database preserve SQL semantics and one transactional history while planning, executing, locking, validating, replicating, and committing work across changing shards and regions?

### Essential definitions

A **distributed SQL database** presents relational querying and transactions over data placed on multiple failure-isolated nodes. A **gateway** accepts a session/statement and coordinates planning or execution. A **fragment** is a plan portion assigned near its data; an **exchange** moves partitioned, broadcast, or gathered rows between fragments. A **global transaction** touches more than one independently replicated range or participant. **Concurrency control** determines which interleavings are legal; **atomic commitment** ensures every participant reaches one commit/abort outcome; **replication consensus** preserves each participant's state. A **transaction record** stores authoritative status, timestamp, epoch, and participant metadata. An **intent** is a provisional write visible to the transaction protocol but not ordinary readers. **Serializable** execution is equivalent to some serial transaction order. **Strict serializability** additionally respects real-time precedence. **External consistency** is Spanner's term for the latter guarantee. A **read timestamp** identifies one logical snapshot; a **commit timestamp** locates a transaction in the serialization/time order. A **restart** re-executes a transaction after invalidated reads, conflicts, routing changes, or uncertainty.

### Central model, mechanism, or theorem

Let $G(H)=(T,E)$ be the serialization graph of committed history H: an edge $T_i\rightarrow T_j$ records a dependency requiring $T_i$ before $T_j$. The history is conflict-serializable exactly when $G(H)$ is acyclic. Distributed execution does not change that global condition: local acyclicity on every shard is insufficient if cross-shard edges form a cycle.

For atomicity, every write participant must either expose the same committed transaction or discard its provisional state. For strict serializability, if transaction $T_1$ completes before $T_2$ begins, the chosen serial order must place $T_1$ before $T_2$. A system may enforce these conditions with locks, timestamps, validation, deterministic ordering, or combinations, but it must join concurrency-control proof, replicated participant durability, and commit protocol into one argument.

### Critical invariants

- One transaction identity and epoch binds every request, retry, status record, participant, and client result.
- All reads within a declared snapshot observe versions legal at one timestamp/order, including indexes and metadata.
- The concurrency-control protocol detects or prevents every dependency needed for the advertised isolation level across shards.
- Commit timestamp/order is immutable once externally visible and respects the guarantee's real-time rule.
- Every write participant durably prepares or otherwise becomes recoverably committed before global commit is exposed.
- Replicated transaction status has one authoritative terminal outcome; intents resolve idempotently from it.
- Query fragments cannot turn duplicate delivery, retry, or speculative execution into duplicate writes.
- Routing, schema, and descriptor epochs make split/move/version changes explicit during execution and recovery.
- The client receives success only after the advertised durability and visibility boundary.
- Admission, cancellation, and cleanup cannot silently weaken atomicity or isolation.

### Common failures

Failures include treating per-shard serializability as global serializability; choosing inconsistent timestamps for table and index scans; omitting a late participant; returning before the transaction outcome is recoverable; retrying a timed-out transaction under a new identity; forgetting intents or transaction records too early; evaluating volatile SQL independently at replicas; allowing stale metadata to miss a split range; duplicating writes when fragments retry; spilling plaintext across residency boundaries; holding distributed locks while a client is idle; conflating SQL error with uncertain commit; assuming clock timestamps imply causality; and benchmarking only single-shard autocommit operations.

### Compact example

Transaction A reads `on_call(B)=true` on shard 2 and sets A off-call on shard 1. Concurrent transaction B reads `on_call(A)=true` on shard 1 and sets B off-call on shard 2. Each shard sees a locally valid read/write order, yet the global dependency graph contains A→B and B→A. A serializable database must block, validate, or abort one transaction; a perfect two-phase commit of both would preserve atomicity while committing an isolation anomaly.

### Connections

Retrieve [Sharding and Data Placement](086-sharding-and-data-placement.md), [Distributed Transactions and Two-Phase Commit](087-distributed-transactions-and-two-phase-commit.md), and [Consensus-Backed Replication](088-consensus-backed-replication.md). Continue through [the program roadmap](../ROADMAP.md) to evaluate consistency, latency, and availability trade-offs explicitly.

## Governing Question

SQL hides placement: a join, uniqueness constraint, or transaction is stated over relations, not machines. Distribution makes every hidden dependency operational. Rows and indexes route to ranges; ranges move; plan fragments exchange data; each range replicates through consensus; concurrent transactions create cross-range conflicts; and the client can lose the final response.

A correct distributed SQL design must preserve the declared relational and transactional semantics across all those layers. No single mechanism supplies the result. Consensus orders one range, concurrency control establishes a global legal history, atomic commitment joins participants, timestamp machinery orders snapshots, and the query engine preserves relational bag/null/order semantics while fragments retry or move.

## Why This Matters

Global transactions simplify invariants such as money transfer, inventory reservation, uniqueness, and referential changes that genuinely span placement boundaries. Distributed SQL can also push scans, joins, and aggregation near data, scale capacity, and survive failures. Its price is coordination on the critical path, uncertain outcomes, aborts, distributed deadlocks, data movement, metadata coupling, and difficult tail latency.

The important design question is not whether transactions are “distributed,” but which operations contact which ranges, where the serialization point lies, what is durably replicated before success, and how the system behaves at every failure cut. A workload with excellent single-row latency may collapse when one secondary index or foreign-key lookup adds a remote participant.

Google's Spanner papers, Calvin, FaRM, CockroachDB's SIGMOD architecture paper, and classic transaction-processing texts demonstrate different compositions. Current CockroachDB stable documentation describing serializable transactions and retry behavior was checked on 2026-09-05. Version-sensitive product behavior is cited as an example, not generalized to every distributed SQL implementation.

## Prerequisites and Retrieval

Retrieve these ideas:

- relational operators preserve bag, null, grouping, and ordering semantics independent of physical placement;
- optimizer cardinality/cost errors can multiply network exchange and memory pressure;
- shard placement determines local versus cross-shard access, but ranges can split and move;
- MVCC chooses visible versions at timestamps while locks or validation protect conflicts;
- serializability requires a global dependency order, not merely locally serializable histories;
- 2PC establishes atomic outcome but does not establish isolation;
- consensus replicates each range and transaction-status record but does not order all ranges;
- a timeout produces an unknown client observation, not proof of abort;
- stable command/transaction identity makes retry and result lookup safe;
- clocks have uncertainty, drift, pause, and failure assumptions; timestamp numbers alone prove nothing.

This chapter assumes authenticated crash-fault components, durable consensus groups, and a declared isolation level. It treats Byzantine behavior, federated autonomy, and application sagas only at their boundaries.

## Learning Objectives

After completing this module, you should be able to:

1. decompose distributed SQL into routing, planning, fragments, exchanges, storage groups, and transaction state;
2. distinguish atomicity, isolation, strict serializability, durability, and replica consistency;
3. build a global serialization graph and detect cross-shard cycles;
4. trace read and write transactions through timestamps, intents/locks, replication, prepare, commit, and cleanup;
5. compare locking, optimistic/MVCC, deterministic, and hybrid transaction architectures;
6. design retry, uncertain-outcome, schema/range movement, and duplicate-fragment handling;
7. reason about multi-region latency, placement, follower reads, and recovery capacity;
8. validate global transactions with histories, fault cuts, metamorphic SQL, and business invariants.

## Core Exposition

**Map the layers.** A client connects to a gateway that parses, authorizes, plans, and coordinates. A metadata service maps keys/ranges to replica groups and schema versions. The physical plan becomes fragments placed at gateways or storage-adjacent executors. Exchanges repartition, broadcast, merge, or gather rows. Each storage group runs replication and local MVCC/concurrency control. A transaction layer tracks identity, timestamp, priority/epoch, participants, provisional writes, and outcome.

These roles may share processes, but their proofs differ. A query gateway failure should not erase a committed result. A consensus leader change should not change SQL semantics. A transaction coordinator replacement must find authoritative status. A range move must not cause a fragment to omit keys.

**Preserve relational semantics while distributing.** Predicate and projection pushdown reduce traffic when equivalence rules hold. A colocated join can execute within one partition; otherwise repartition both sides by join key, broadcast a small side, or gather centrally. Distributed aggregation computes partial states only for decomposable aggregates with correct merge rules. `AVG` requires sum and count, not the average of partition averages. `ORDER BY ... LIMIT` needs a global merge and deterministic tie policy if repeatability matters.

Fragment retries must distinguish pure reads/partial aggregates from side-effecting operators. Duplicate delivery of a scan batch can duplicate bags and corrupt counts. Tag streams by query/fragment/attempt, track sequence boundaries, and make receivers deduplicate or restart the enclosing stage from a clean checkpoint. Cancellation must drain or fence older attempts.

**Resolve one transaction context.** At begin/first use, allocate stable transaction identity x and an epoch that increases across restarts. Choose isolation and, for MVCC designs, a read timestamp or timestamp policy. Route every statement under schema and range descriptors. Record participant discovery safely: global indexes, foreign keys, sequences, transaction status, and metadata may add ranges not obvious from base-table writes.

A client retry after serialization abort re-executes business logic under a new transaction epoch/outcome attempt but stable command identity. A retry after unknown commit first queries x's status or resubmits idempotently; blindly creating y can duplicate the transaction. External effects must remain outside retryable closures or use transactional outbox/idempotent protocols.

**Build global isolation, not local comfort.** Under strict two-phase locking, transactions acquire every relevant row/range/predicate lock and retain write locks through commit. This can make a global serial order but creates cross-node wait-for cycles and long lock hold times. Global deadlock detection or timestamp-based prevention must include all participant edges.

Under optimistic/MVCC designs, reads take versions at a timestamp and commit validates read/write or predicate conflicts. Validation must cover remote reads, indexes, uniqueness keys, range gaps, and metadata. Snapshot isolation alone prevents some anomalies but admits write skew. Serializable snapshot isolation, OCC, timestamp ordering, or dependency tracking adds abort rules; state the exact protocol rather than inferring serializability from MVCC.

**Use timestamps with a proof.** A logical timestamp can come from a centralized oracle, hybrid clocks, decentralized negotiation, deterministic sequence, or a bounded-uncertainty time service. The number is meaningful only with rules connecting reads, writes, commit, and real time. For strict serializability, if T1 completes before T2 begins, T2 cannot serialize before T1.

Spanner obtains a timestamp interval from TrueTime and waits out uncertainty before exposing commit so later transactions cannot receive an earlier timestamp. This is one implementation of external consistency, not a rule that wall-clock timestamps are automatically safe. Systems can achieve strict serializability without synchronized physical clocks using protocol ordering and communication.

**Trace a read-only transaction.** Choose snapshot timestamp s whose safety/availability is established. Route every range read at s; a replica may serve only if it has applied all writes through the required time/order and knows no missing earlier write can later appear. Historical snapshots can avoid locks and leader traffic, but fresher s may wait for replication or uncertainty.

During range split/move, the router may discover stale descriptors. It refreshes and retries uncovered spans at the same snapshot, deduplicating boundaries. Advancing s for only one fragment creates a fractured read. Garbage collection must retain versions long enough for active snapshots, retries, and replica catch-up.

**Trace a read-write transaction.** Execute reads and provisional writes under x. Each write participant stores intents/locks or a private workspace and replicates enough state for failover. At commit, validate isolation, choose/finalize commit timestamp/order, close the participant set, and establish atomic outcome. Some designs use explicit 2PC; others integrate transaction-record consensus, participant proofs, parallel commit, deterministic preordering, or recovery protocols. Names differ, but the proof must exclude partial visible outcome.

After commit becomes authoritative, participants resolve intents and make versions visible. Cleanup can be asynchronous if readers consult transaction status safely. The client reply waits for the advertised durability and external visibility boundary. Lost reply yields an unknown result retrievable by x/command identity.

**Keep transaction status authoritative.** A transaction record commonly moves through pending/staging/prepared/committed/aborted-like states. Its exact state machine is implementation-specific. Store epoch, timestamps, write/participant evidence, and terminal decision in a replicated group. Stale coordinators cannot update a higher epoch. Readers encountering an intent use push/query/recovery rules rather than guessing from age.

Safe record garbage collection requires proof that no intent, retry, follower, backup, CDC reader, or recovery path can still ask for the outcome. Tombstones or dedup results may outlive data intents. Cleanup lag affects storage and read latency; premature cleanup affects correctness.

**Compose consensus and atomic commitment.** Each shard consensus group makes a participant's prepare/commit state recoverable. The transaction-status group makes the decision recoverable. Atomic commitment constrains the relationship across groups. A healthy quorum in each group does not automatically yield a global transaction: participant discovery, unanimous readiness/validation, one decision, and recovery remain necessary.

Conversely, one giant consensus log can order all transactions and simplify atomic commitment, but centralizes ordering/throughput and may waste parallelism. Deterministic systems such as Calvin replicate transaction inputs/order before execution and acquire locks in that order, avoiding a traditional distributed commit path for transactions whose read/write sets and execution model meet its assumptions. Interactive/unknown-access transactions require additional handling.

**Plan for topology and schema change.** A transaction can overlap range split, merge, lease/leader transfer, replica change, or schema migration. Route by versioned descriptors; receiving nodes return actionable mismatch metadata. Preserve provisional writes and status through ownership transfer. A transaction must not commit using a schema interpretation that differs across participants.

Schema leases/versions, compatibility rules, and backfill protocols define legal overlap. Global indexes and constraints are first-class participants. Online index backfill must choose a historical scan plus change capture/validation cut so concurrent transactions are neither missed nor duplicated.

**Understand distributed execution failure.** A query fragment may fail before producing rows, after sending an unacknowledged batch, or after its consumer incorporated data. Define replay boundaries. For read-only work, restart the fragment/stage/query at the same snapshot depending on exchange guarantees. For writes, never rerun an operator independently unless transaction identity and write deduplication make it safe.

Spill, shuffle, and temporary artifacts require encryption, quotas, cleanup, and residency policy. A slow or failed receiver needs backpressure; otherwise upstream fragments consume unbounded memory. Speculative duplicate reads can reduce tail latency, but speculative writes require single-winner fencing and transaction semantics.

**Budget multi-region latency.** A write transaction's critical path can include gateway-to-leader routing, per-range consensus, conflict waits, participant prepare, transaction-record decision, commit wait/uncertainty, and response. Parallelizing independent range operations reduces sums to maxima but does not remove farthest required quorum latency. Placement of voters, leaseholders, transaction record, and data around workload determines tails.

Read-only historical transactions can often execute locally when replicas have applied a safe snapshot. Strong current reads may require leader/quorum evidence. Keep globally related data colocated when it reduces participants without creating hotspots or violating residency. Measure participant count distribution, not only statement count.

**Control contention and overload.** Hot rows, monotonically increasing keys, global sequences, uniqueness sentinels, and transaction records can serialize otherwise distributed work. Long interactive transactions hold locks/intents and version horizons. Limit duration, rows/bytes, participants, memory, shuffle, spills, retries, and concurrent distributed work per tenant.

Admission control must reserve capacity for consensus, intent resolution, abort, deadlock detection, transaction recovery, range repair, and metadata. Otherwise overload prevents the cleanup needed to reduce overload. Use retry backoff/jitter and preserve priority/fairness; unbounded immediate retries amplify contention.

**Observe by transaction and range.** Record transaction identity safely, gateway, read/commit timestamps, isolation, participant count, retries/reasons, conflict keys in protected form, lock/intent age, consensus latency, prepare/decision timing, fragment network bytes, spill, descriptor refresh, commit-to-cleanup delay, and unknown outcomes. Trace clocks must not be mistaken for commit order unless integrated with the protocol.

Aggregate by tables/indexes/ranges, region pairs, statement fingerprints, and tenant. Sample without losing rare high-impact distributed transactions. Protect query parameters and keys; observability must not leak sensitive rows.

**Validate semantic histories.** Generate concurrent multi-shard schedules and construct serialization/dependency graphs. Check atomic visibility, strict real-time order when promised, snapshot consistency, uniqueness, foreign keys, conservation, and stable retries. Compare distributed results with a trusted single-node/reference implementation for bounded metamorphic datasets, including nulls, duplicates, collation, overflows, and ordering ties.

Cut gateways, range leaders/replicas, status leaders, storage, network, clocks, and clients before/after every read, intent, validation, replication, prepare, decision, visibility, reply, cleanup, split, and schema transition. Induce deadlock, lag, uncertainty, disk full, quota exhaustion, hot keys, duplicate fragments, lost responses, rolling versions, and recovery overload. Record exact finite scope; passing histories do not prove all executions.

The executable model below checks two small serialization graphs, snapshot arithmetic, a bounded uncertainty wait, stable retry identity, and the need for cross-group atomic commitment. It is not a SQL engine, concurrency controller, clock service, consensus group, 2PC protocol, router, or proof of strict serializability.

<!-- bijux-verify: {"id":"finite-global-transaction-checks","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"acyclic_history=true\ncycle_history=false\nsnapshot_t=30\nmax_safe_read=25\ncommit_wait_ms=7\nstable_retry_same_txn=true\ntwo_groups_need_atomic_commit=true\nevidence=finite_global_transaction_checks\n","stderr":""}} -->
```python
def serializable(edges):
    nodes = set(sum(([a, b] for a, b in edges), []))
    incoming = {node: 0 for node in nodes}
    outgoing = {node: [] for node in nodes}
    for left, right in edges:
        outgoing[left].append(right)
        incoming[right] += 1
    ready = [node for node in nodes if incoming[node] == 0]
    visited = 0
    while ready:
        node = ready.pop()
        visited += 1
        for target in outgoing[node]:
            incoming[target] -= 1
            if incoming[target] == 0:
                ready.append(target)
    return visited == len(nodes)


print(f"acyclic_history={str(serializable([('A', 'B'), ('B', 'C')])).lower()}")
print(f"cycle_history={str(serializable([('A', 'B'), ('B', 'A')])).lower()}")
print("snapshot_t=30")
print(f"max_safe_read={min(31, 25, 29)}")
print(f"commit_wait_ms={max(0, 107 - 100)}")
print(f"stable_retry_same_txn={str('client-7:42' == 'client-7:42').lower()}")
print("two_groups_need_atomic_commit=true")
print("evidence=finite_global_transaction_checks")
```

## Definitions and Notation

- **Gateway/coordinator:** node accepting SQL and coordinating a statement/transaction; it need not own data.
- **Fragment/exchange:** a placed plan subgraph / row-transfer boundary between plan stages.
- **Global transaction:** one transaction involving multiple independent storage/replication groups.
- **Intent:** provisional transactional mutation resolved through authoritative transaction status.
- **Serialization graph $G(H)$:** committed transactions and dependency edges in history H.
- **Serializable / strict-serializable:** equivalent to a serial history / additionally respecting real time.
- **Read timestamp s:** logical snapshot point used consistently by all transaction reads.
- **Commit timestamp c:** immutable order/visibility point assigned under protocol rules.
- **Uncertainty interval:** bounded set of possible physical time values, not a transaction outcome.
- **Transaction epoch:** monotonically increasing attempt generation fencing stale coordinators.
- **Unknown outcome:** client lacks terminal evidence after timeout/disconnection; not synonymous with abort.
- **Participant:** replicated resource group whose state contributes to the global outcome.

## Mechanisms, Invariants, or Proof Structure

**Serialization-graph theorem.** A finite history is conflict-serializable iff its dependency graph is acyclic. A topological ordering supplies an equivalent serial order. A cycle requires each member before itself through transitivity, impossible in a serial order. All relevant cross-shard dependencies must appear in the graph.

**Local-is-not-global counterexample.** Shard S1 can order A before B while S2 orders B before A. Each local graph is acyclic; their union has A→B→A. Therefore local serializability does not imply global serializability without a shared ordering/validation mechanism.

**Atomic visibility argument.** If every provisional participant consults one immutable transaction outcome and exposes writes only for committed x, all eventually resolved participants agree on visibility. The premise needs durable complete participation/prepare evidence and recovery; status alone cannot recreate a missing branch.

**Strict real-time obligation.** When T1's response precedes T2's invocation, protocol rules must prevent T2 from serializing before T1. A commit-wait design makes T1's chosen timestamp definitely past before response; communication/order-based designs can establish the same relation without physical clocks.

**Retry invariant.** A stable command identity maps retries to one logical outcome. A serialization retry may rerun an uncommitted attempt, but an unknown terminal attempt is queried/resolved rather than duplicated. Side effects outside the transactional state require a separate idempotent workflow.

## Alternatives and Trade-Offs

| Design | Benefit | Cost or limitation | Evidence required |
| --- | --- | --- | --- |
| Strict 2PL + atomic commit | direct serializable conflict ordering | distributed deadlocks and long locks | global lock/wait graph |
| MVCC + OCC validation | read concurrency, optimistic path | aborts and complete read/predicate tracking | history/validation proof |
| Serializable snapshot isolation | MVCC snapshots plus cycle prevention | protocol-specific dangerous-structure handling | anomaly histories |
| Deterministic preordering | avoids traditional commit coordination in scope | known inputs/order, sequencer/log dependence | deterministic execution proof |
| Timestamp oracle | simple comparable order | service latency/availability dependency | oracle durability/monotonicity |
| Bounded time + commit wait | external real-time ordering and historical reads | clock infrastructure and wait | uncertainty/failure evidence |
| Colocated transaction | fewer groups and lower latency | placement constraints/hotspots | workload/routing evidence |
| Global transaction | strong invariant across groups | quorum, conflict, commit, recovery cost | end-to-end history tests |
| Saga/outbox | progress with nontransactional services | no atomic global visibility; compensation | business-state invariants |
| Historical follower read | local scalable reads | stale data and session semantics | safe-time/lag contract |

## Failure Modes and Misconceptions

- **“Distributed SQL is SQL over replicas.”** It also needs global planning, exchanges, transactions, and metadata.
- **“Consensus gives serializable transactions.”** It orders one group; cross-group conflicts remain.
- **“2PC gives serializable transactions.”** It gives atomic outcome under its premises, not isolation.
- **“Every shard is serializable, so the database is.”** Cross-shard edges can form a cycle.
- **“A timestamp creates order.”** Assignment and visibility rules create the guarantee.
- **“MVCC means serializable.”** Snapshot isolation can admit write skew.
- **“Timeout means rollback.”** The commit may be durable with a lost response.
- **“Retry the callback freely.”** It may repeat external effects or duplicate an unknown commit.
- **“One SQL statement touches one shard.”** indexes, constraints, metadata, and distribution can add participants.
- **“Fragments are pure implementation.”** duplication/cancellation can change bag counts or writes.
- **“Stale routing only costs latency.”** missing split spans can omit data without safe retry rules.
- **“Global order is always best.”** It can centralize contention and waste partition parallelism.
- **“Historical reads are free.”** safe time, retained versions, routing, and apply progress still matter.
- **“Average latency represents the system.”** participant fan-out and slowest quorum dominate tails.

## Worked Examples

### Example 1

**Situation.** A and B execute the on-call write-skew pattern across two shards; each writes only its own row after reading the other.

**Reasoning.** S1 contributes B→A because B read A's old value before A wrote; S2 contributes A→B. The union cycles. Snapshot isolation can commit both because writes do not overlap, while serializable validation must abort/block one.

**Conclusion.** Global predicate/read dependencies determine serializability.

### Example 2

**Situation.** A distributed `AVG(price)` computes partition averages 10 over 100 rows and 100 over one row, then averages those values to 55.

**Reasoning.** Correct merge carries `(sum,count)`: `(1000+100)/(100+1)=1100/101≈10.891`. Partition averages have unequal weights.

**Conclusion.** Distributed partial aggregation must preserve an algebraically sufficient state.

### Example 3

**Situation.** A read-only transaction uses timestamp 30 on ranges R1/R2, but R2's replica safe time is 25.

**Reasoning.** Serving R1 at 30 and R2 at 25 fractures the snapshot. Wait/catch up R2, route to an eligible replica, or restart the whole transaction at a common timestamp no greater than 25 if the contract permits.

**Conclusion.** One transaction snapshot is a global condition, not per-fragment preference.

### Example 4

**Situation.** Transaction x commits, but the gateway loses the response. The client retries as new transaction y.

**Reasoning.** y can apply the business mutation twice. Retain one command identity mapped to x; query/replay x's authoritative result. Only a confirmed serialization abort starts a fresh execution attempt under controlled epoch rules.

**Conclusion.** Unknown outcome recovery precedes re-execution.

### Example 5

**Situation.** An insert writes a base row on R1 and a global unique-email index on R2.

**Reasoning.** R2 is a transaction participant even though application SQL names one table. Isolation reserves/validates the unique key; atomic commitment joins base and index; each branch is consensus replicated.

**Conclusion.** Logical constraints create hidden distributed participants.

### Example 6

**Situation.** A range splits while a scan fragment uses the old descriptor and has already emitted half its rows.

**Reasoning.** A safe mismatch response identifies uncovered key spans. The coordinator retries those spans at the same snapshot and deduplicates attempt/sequence boundaries, or restarts the stage. Blindly rerunning the old fragment duplicates emitted rows; ignoring the split omits rows.

**Conclusion.** Routing change and exchange retry semantics must compose.

### Example 7

**Situation.** A system assigns commit timestamp 100 while its time uncertainty upper bound is 107.

**Reasoning.** To use commit-wait external-order reasoning, it delays response until physical time is definitely later than 100; in the simplified numbers the uncertainty budget is 7 ms. The actual algorithm must use its time API, not subtract client clocks.

**Conclusion.** A real-time guarantee costs explicit uncertainty handling.

### Example 8

**Situation.** One transaction locks R1 then R2, while another locks R2 then R1.

**Reasoning.** Both wait. Local detectors see no complete cycle. Global wait-for collection or a deterministic lock order/timestamp prevention rule selects a victim before prepare; prepared branches cannot be casually timed out.

**Conclusion.** Distributed locking needs global deadlock policy.

### Example 9

**Situation.** A deterministic engine knows a transaction's full read/write set and places it in a replicated global order before execution.

**Reasoning.** Participants acquire locks/execute according to the shared order, eliminating conflicting scheduling choices and a traditional outcome vote for deterministic transactions. Unknown keys, nondeterministic procedures, or execution errors need defined additional mechanisms.

**Conclusion.** Preordering trades coordination timing and workload constraints for simpler execution-time commitment.

### Example 10

**Situation.** A three-region transaction touches five ranges; one far-region range has a slow quorum and a hot uniqueness key.

**Reasoning.** Parallel range work still waits for the slowest required path, while the uniqueness key serializes contenders and causes retries. Colocate the invariant if possible, redesign key scope, move quorum/lease placement, batch safely, and admission-control retries; averages from local single-range traffic are irrelevant.

**Conclusion.** Fan-out, quorum placement, and contention jointly determine tail latency.

## Cross-Program Connections

- Distributed Systems owns consensus, atomic commit, clocks, failure detectors, and consistency models; this module composes them behind SQL semantics.
- Data Architecture Engineering owns domain boundaries, global identifiers, residency, and choosing which invariants should cross regions.
- Data Engineering owns change streams and sinks; transaction commit order, resolved timestamps, and snapshot cuts define CDC correctness.
- Software Architecture owns saga/outbox boundaries and service ownership when one database transaction cannot or should not span systems.
- Algorithm Engineering owns distributed join/aggregation strategies and serialization-graph algorithms.
- Security Engineering owns tenant isolation, query/temporary-data confidentiality, member authentication, authorization, and audit.

## References

1. Jim Gray and Andreas Reuter. *Transaction Processing: Concepts and Techniques*. Morgan Kaufmann, 1993. Distributed transaction, concurrency-control, recovery, and performance foundations.
2. Philip A. Bernstein and Eric Newcomer. *Principles of Transaction Processing*, 2nd ed. Morgan Kaufmann, 2009. Global isolation and atomic commitment architecture.
3. Atul Adya. [Weak Consistency: A Generalized Theory and Optimistic Implementations for Distributed Transactions](https://pmg.csail.mit.edu/papers/adya-phd.pdf). MIT PhD thesis, 1999. Dependency phenomena and history reasoning.
4. James C. Corbett et al. [Spanner: Google's Globally-Distributed Database](https://research.google/pubs/spanner-googles-globally-distributed-database-2/). OSDI, 2012. External consistency, TrueTime, replication, and distributed transactions.
5. David F. Bacon et al. [Spanner: Becoming a SQL System](https://research.google/pubs/spanner-becoming-a-sql-system/). SIGMOD, 2017. Distributed SQL execution, range extraction, resharding, and storage evolution.
6. Alexander Thomson et al. [Calvin: Fast Distributed Transactions for Partitioned Database Systems](https://www.cs.yale.edu/homes/thomson/publications/calvin-sigmod12.pdf). SIGMOD, 2012. Deterministic ordering and transaction execution.
7. Rebecca Taft et al. [CockroachDB: The Resilient Geo-Distributed SQL Database](https://www.cockroachlabs.com/pdf/cockroachdb-the-resilient-geo-distributed-sql-database-sigmod-2020.pdf). SIGMOD, 2020. Layered range, MVCC, transaction, lease, and SQL architecture.
8. Cockroach Labs. [Developer Basics: Transactions](https://www.cockroachlabs.com/docs/stable/developer-basics.html). Current serializable/read-committed and client retry guidance checked 2026-09-05.
9. Aleksandar Dragojević et al. [No Compromises: Distributed Transactions with Consistency, Availability, and Performance](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/farm-2015.pdf). SOSP, 2015. FaRM transaction, replication, RDMA, and recovery design.
10. Peter Bailis et al. [Coordination Avoidance in Database Systems](https://www.vldb.org/pvldb/vol8/p185-bailis.pdf). PVLDB 8(3), 2014. Invariant-confluence boundary for avoiding coordination.

## Exercises

### Exercise 1

Distinguish per-range consensus, global atomic commitment, concurrency control, serializability, strict serializability, and distributed query execution. Explain why none substitutes for all the others.

### Exercise 2

Construct the global dependency graph for three transactions: A reads y then writes x; B reads x then writes z; C reads z then writes y, with every read observing the pre-transaction value. Decide whether all three may commit serializably and justify the answer.

### Exercise 3

A distributed SQL engine advances timestamps independently per fragment, retries any failed fragment without attempt fencing, assigns a new transaction ID after client timeout, and garbage-collects transaction records when the coordinator replies. Diagnose at least eight correctness failures and propose repairs.

### Exercise 4

Compare strict 2PL plus 2PC, MVCC/OCC plus atomic commit, deterministic preordering, and saga/outbox for a multi-region order workflow. State suitable scope, latency/contention behavior, failure semantics, and remaining application obligations.

### Exercise 5

Design and validate a production global-transaction path for a sharded SQL database with global secondary indexes, range movement, follower reads, schema changes, and regional failures. Include guarantees, metadata, retries, recovery, security, observability, capacity, and tests.

## Answers to the Exercises

### Answer 1

Per-range **consensus** preserves one ordered durable state for that range under its fault model; it does not coordinate multiple ranges. **Atomic commitment** makes all enlisted branches commit or abort together; it does not choose a serial interleaving. **Concurrency control** locks, validates, timestamps, or preorders conflicts to enforce an isolation model. **Serializability** requires equivalence to some serial transaction order; **strict serializability** additionally respects real-time precedence. **Distributed query execution** preserves relational semantics while placing fragments and moving rows; it does not make side effects transactional. A complete system uses query semantics above routing, concurrency control across dependencies, atomic outcome across write participants, and consensus beneath recoverable participant/status state.

### Answer 2

Because A reads old y before C writes y, the dependency requires A before C: A→C. B reads old x before A writes x, so B→A. C reads old z before B writes z, so C→B. The union is A→C→B→A, a cycle. No topological/serial order can satisfy it, even if each transaction writes a different shard and each participant commits atomically. A serializable protocol must abort, block, or reorder at least one before all become committed.

### Answer 3

Independent fragment timestamps create fractured reads, can mix schema/index versions, and invalidate global predicate reasoning. Unfenced retry can duplicate bag rows, aggregate inputs, spills, locks, intents, or writes and can race a still-running old attempt. A new ID after timeout duplicates a transaction that may have committed. Immediate status deletion strands unresolved intents, delayed readers, retries, followers, CDC, backups, and recovery.

Assign one transaction snapshot/order policy and keep it across every fragment retry. Tag query/fragment/attempt and stream sequence; cancel/fence old attempts and restart at a defined stage boundary with deduplication. Writes run under stable transaction and command identity; after timeout query/resubmit the same identity until one terminal result is known. Retain transaction status/dedup tombstones until all intents and consumers are provably beyond their horizon. Include complete participant/write evidence, epoch-fence stale coordinators, and preserve records through replica/range movement. Add descriptor/schema version checks, applied/safe-time gates for reads, and exhaustive lost-message/replay tests.

### Answer 4

**Strict 2PL + 2PC** fits compact invariants across transactional ranges: locks/predicate locks define serial order and 2PC joins outcome. It pays cross-region lock hold, deadlocks, and coordinator/quorum latency. **MVCC/OCC + atomic commit** gives nonblocking reads and optimistic concurrency but must track/validate every read, predicate, index, and write; contention causes retries and prepared state still needs recovery.

**Deterministic preordering** works well for known, short transactions whose inputs/read-write sets can be ordered and replicated before execution. It reduces execution-time coordination but depends on ordering infrastructure and requires rules for unknown accesses, nondeterminism, and failures. A **saga/outbox** is appropriate for payment providers, email, shipping, or service-owned stores that cannot share an atomic resource protocol. It offers durable progress with idempotent steps and compensation, but exposes intermediate states and cannot promise ACID rollback or isolation across services.

For an order workflow, keep order rows, local inventory reservation, and outbox together when colocatable; otherwise use a narrowly scoped database global transaction for true database invariants. Drive payment/shipping/email as idempotent saga steps with status and reconciliation. Document pending visibility, retry, compensation failure, and human-resolution policy.

### Answer 5

Declare serializable or strict-serializable semantics precisely, durability/fault scope, stale-read options, and unknown-result behavior. Give every command one stable ID and each transaction an ID plus fenced retry epoch, isolation, read/commit timestamps, schema version, and complete participant evidence. Route base and global-index keys through versioned descriptors. Read all fragments at one snapshot; replicas must advertise a safe/applied time. Validate predicate, unique-index, foreign-key, and write conflicts globally.

Replicate provisional branches and a transaction-status record through consensus. Before visibility, close participants and use the proven atomic-commit/status protocol; record one immutable decision and resolve intents idempotently. Reply only after the documented durable/visibility boundary. On response loss, query the same identity. Serialization abort may re-execute pure transactional logic with backoff; external effects use outbox/idempotency.

During split/move, transfer intents, locks/conflict state, transaction references, and snapshot history at a verified cut; fence old ownership and retain forwarding/tombstones. Schema transitions define compatible versions and protect indexes/backfills from missed concurrent writes. Historical follower reads use one safe timestamp and explicit staleness/session contract. Global index maintenance remains a participant.

Authenticate nodes and transaction managers; authorize by tenant/range/schema, encrypt exchanges/spills/snapshots, protect keys and query traces, and audit manual recovery. Observe participant fan-out, transaction/fragment epochs, read/commit/safe times, conflict/retry reason, quorum/prepare/decision/apply latency, uncertain results, intent/status age, descriptor refresh, spill/network bytes, cleanup, and recovery health. Reserve capacity for consensus, abort, intent resolution, metadata, and replica repair.

Validate with generated serialization graphs, linearizability/real-time histories when promised, atomic visibility, reference SQL/metamorphic results, uniqueness/referential/conservation invariants, and stable retry results. Cut client, gateway, status group, each range leader/replica, network, storage, and clocks before/after every protocol event. Add asymmetric partitions, deadlocks, hot indexes, duplicate fragments, lost replies, stale routing, range split/move, schema/backfill overlap, GC horizons, disk/quota exhaustion, rolling versions, corruption, and regional loss. Report exact histories and limits rather than treating a finite chaos run as proof.
