---
module_id: DBE-087
program: Database Engineering
level: 2
module_number: 87
title: Distributed Transactions and Two-Phase Commit
status: complete
last_verified: 2026-09-05
---

# Distributed Transactions and Two-Phase Commit

## One-Page Review

### Governing question

How can independent transactional resource managers reach one durable atomic commit/abort outcome despite crashes and message loss, and what blocking, lock, recovery, and operational costs follow from that promise?

### Essential definitions

A **distributed transaction** has effects at more than one independently committing resource manager. **Atomic commitment** requires every participant to commit or every participant to abort. A **transaction manager/coordinator** discovers participants, requests votes, durably decides, and drives completion. A **participant/resource manager** executes a local branch. During **prepare**, a participant votes `YES` only after making its branch able to commit later despite required failures; otherwise it votes `NO` and aborts. A **prepared** or **in-doubt** branch has voted yes but lacks the final outcome and must retain recovery state and usually locks. **Two-phase commit (2PC)** consists of prepare/vote followed by decision/completion. A **global transaction identifier (XID)** and distinct branch IDs make recovery and retries refer to the same work. A **heuristic outcome** is a participant's unilateral operator/system decision while in doubt; it can violate atomicity. **Presumed abort/commit** optimize logging/messages by defining the meaning of missing coordinator records.

### Central model, mechanism, or theorem

For participants $P=\{p_1,\ldots,p_n\}$ with durable votes $v_i$, the coordinator may durably decide commit only if every participant voted yes:

$$
D=COMMIT \Rightarrow \bigwedge_{i=1}^{n}(v_i=YES).
$$

Once any participant has durably prepared, it cannot independently infer abort from coordinator silence because a commit decision may exist but be delayed. Basic 2PC is therefore safe under its logging/recovery assumptions but can block during coordinator/decision unavailability. Replicating participant and coordinator state can improve availability only when the replication protocol preserves those durable state transitions.

### Critical invariants

- One globally unique XID identifies the transaction; branch IDs identify every enlisted resource exactly once.
- A `YES` vote is emitted only after local changes, locks/validation state, and prepare record survive the declared failure model.
- The coordinator durably records the final decision before telling a participant to commit.
- Commit is chosen only after all required durable yes votes; any durable no/prepare failure yields abort.
- A prepared participant accepts only the recorded global decision and applies repeated commit/rollback idempotently.
- Recovery reconstructs participant set, votes, coordinator decision, and acknowledgements without guessing from elapsed time.
- Locks, versions, uniqueness reservations, and schema assumptions held by prepared work remain valid until resolution.
- Topology/failover retains XIDs and prepared/decision records on promoted replicas.
- External nontransactional effects are not claimed atomic merely because database branches use 2PC.

### Common failures

Failures include calling 2PC “two-phase locking”; voting yes before durable prepare; forgetting a dynamically enlisted participant; recording the decision after sending commit; timing out and aborting an in-doubt yes voter; retrying with a new XID; leaving prepared transactions indefinitely; holding hot locks across coordinator outage; letting failover choose replicas missing prepare/decision records; committing email/payment/cache side effects that are not resource managers; allowing DDL or session-local objects that cannot prepare; using heuristic commit/abort without global reconciliation; and enabling prepared transactions without an external transaction manager, monitoring, quotas, and recovery drills.

### Compact example

Coordinator C enlists shards A and B under XID x. A and B each durably prepare and vote yes. C durably writes `COMMIT(x)`, then sends it. If C crashes before B receives the decision, A may already commit while B remains prepared. B must not abort on timeout; after recovery it learns the durable commit and commits. If B had voted no, C would durably decide abort. The protocol preserves atomic outcome but can hold B's locks while decision access is unavailable.

### Connections

Retrieve [Crash Recovery](078-crash-recovery.md), [Group Commit](077-group-commit.md), [Leader Election and Failover](085-leader-election-and-failover.md), and [Sharding and Data Placement](086-sharding-and-data-placement.md). Continue through [the program roadmap](../ROADMAP.md) to consensus-backed replication, distributed SQL/global transactions, and consistency/latency/availability evaluation.

## Governing Question

A local database transaction can make one storage engine's updates atomic with one commit log. Once an operation modifies two shards, databases, queues, or other transactional resources, independent local commits can split: A commits while B aborts. Retrying cannot always repair the invariant, especially when other transactions observe or act on the partial result.

Two-phase commit turns each participant's tentative branch into a durable promise, then publishes one global decision. The promise solves atomic outcome under stated crash/recovery assumptions. It does not eliminate network partitions, guarantee progress, provide serializable isolation by itself, or include arbitrary external effects.

## Why This Matters

Cross-shard account transfer, global unique reservation, order plus inventory, metadata plus data movement, and coordinated schema/catalog changes can require atomic commitment. Avoiding cross-shard work through good placement is valuable, but some invariants are genuinely global.

The cost is not merely two network rounds. Prepared participants retain locks, versions, transaction IDs, log, memory, and conflict edges after the client session disappears. A lost coordinator decision can block business work. Long prepared transactions can obstruct vacuum/garbage collection, cause deadlocks, exhaust configured slots, and turn recovery into an operator emergency.

Current PostgreSQL 18 provides `PREPARE TRANSACTION`, `COMMIT PREPARED`, `ROLLBACK PREPARED`, and `pg_prepared_xacts`, intended for an external transaction manager; its documentation recommends leaving the feature disabled when no manager promptly resolves prepared work. Current MySQL 8.4 implements XA branch states and `XA RECOVER`, with detached prepared XA transactions enabled by default. These version-sensitive resource-manager interfaces were checked on 2026-09-05; neither is an application-level global coordinator by itself.

## Prerequisites and Retrieval

Retrieve these ideas:

- local atomicity, durability, isolation, and recovery are separate properties;
- WAL/redo must establish a durable transaction state before an acknowledgement can rely on it;
- locks and MVCC versions can outlive client sessions and block garbage collection;
- shard placement determines which operations need distributed commitment;
- leader election/failover must preserve the committed/prepared prefix and fence stale writers;
- idempotency means repeating a command for the same XID does not create another effect;
- timeouts reveal missing timely responses, not the remote transaction state;
- consensus chooses one durable value among proposals, while atomic commitment constrains commit on unanimous participant readiness;
- nontransactional messaging and external effects need outbox/inbox, idempotency, escrow, saga, or compensation designs;
- authentication and authorization apply to prepare, recovery enumeration, and commit/rollback decisions.

This module treats database participants as replicated or recoverable state machines with documented prepare semantics. It does not assume a process-local coordinator record is sufficiently durable for production.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish atomic commitment, consensus, concurrency control, and two-phase locking;
2. derive the prepare and decision invariants of 2PC;
3. trace coordinator and participant logs through crash/message-loss cuts;
4. explain why prepared participants can block and why timeout is not safe resolution;
5. design globally unique XIDs, enlistment, idempotent completion, and recovery scans;
6. account for locks, MVCC/vacuum, deadlocks, quotas, and latency;
7. compare 2PC, one-phase/read-only optimizations, presumed outcomes, replicated commit, sagas, and outbox patterns;
8. validate distributed commit through exhaustive state/failure matrices and business invariants.

## Core Exposition

**Define scope and participants.** A global transaction has XID x, coordinator C, and a closed participant set P. Each resource receives a branch ID unique within x. Dynamic enlistment must close before the final prepare decision; otherwise an omitted resource can commit independently or be absent from abort.

The transaction manager records business command identity, participants, branch mappings, deadlines as liveness policy, and final outcome. XIDs must not be reused within any resource's retention/recovery horizon. Random uniqueness without durable mapping is insufficient if the same client retry generates another XID.

**Execute local branches.** During the active phase, the coordinator/app performs operations at participants under x. Local concurrency control obtains locks or validates versions according to the chosen isolation level. 2PC does not determine isolation: two globally atomic transactions can still exhibit write skew under local snapshot isolation if cross-participant conflicts are not coordinated.

Abort immediately on a branch error when no durable yes promise prevents it. Close cursors, streams, and session-local state that cannot survive prepare. Discover every implicit participant, including global indexes, metadata shards, transactional queues, and audit resource managers.

**Phase 1: prepare and vote.** C sends `PREPARE(x, participant-set/hash, protocol epoch)`. Each participant validates local constraints, deadlock/serialization outcome, space, schema/version, privileges, branch completeness, and ability to commit after crash. It durably records `PREPARED(x, branch, metadata)` with required undo/redo and retains locks/reservations, then replies `YES`.

If validation or durable prepare fails, the participant records/executes abort as required and replies `NO`. A participant must not vote yes on volatile state or assume the client connection will remain. After yes, it has surrendered unilateral choice: it awaits the global outcome.

**Phase 2: decide and complete.** C chooses commit only after durable yes from every participant; otherwise abort. It durably writes `DECISION(x,D,P)` before sending D. Participants receiving D durably commit/rollback the branch, release locks/resources after the local outcome is safe, and acknowledge completion. C forgets x only after the protocol's acknowledgement/retention rules permit recovery and late messages.

Messages can duplicate, reorder, or vanish. `PREPARE`, `COMMIT`, `ROLLBACK`, and acknowledgement handling must be idempotent by XID/branch. A participant receiving a repeated decision returns its durable outcome. A conflicting decision for the same XID is a protocol safety fault.

**Understand uncertainty states.** Before voting yes, a participant can usually abort on coordinator loss under the protocol. After durable yes, silence is ambiguous: C might have recorded commit and told other participants. Unilateral abort could split the outcome. The participant remains in doubt and queries C, a replicated decision service, or other authorized recovery path.

A coordinator crash before durable decision can resolve according to its recovery protocol, often abort when there is no commit record under presumed-abort logging. A crash after durable commit must retransmit commit. This is why decision-record order is part of safety.

**2PC can block.** Basic 2PC ensures atomic decision but does not guarantee nonblocking progress when all participants are prepared and the unique decision record is unavailable. Locks can halt unrelated work. Replicating C's decision log with consensus can make it available through some failures; replicating each participant's prepared state protects failover. It does not make an unavailable quorum progress or remove the unanimity condition for commit.

Paxos Commit and related protocols replicate participant/decision choices to tolerate coordinator failures. Preserve the exact algorithm; adding a “backup coordinator” that has not durably learned the participant set/votes/decision can issue a contradictory outcome.

**Couple replication and prepare.** When a participant is a replicated shard, its yes vote must mean the prepared branch is committed to the replication level required for participant failover. A newly promoted leader must recover prepared branches and accept the same XID decisions. If the prepare exists only on the lost leader, a global commit can become impossible to complete correctly.

The coordinator decision likewise needs defined durability and failover. A client-hosted in-memory coordinator is unsafe for long in-doubt work. Store the decision in a replicated transaction-status record whose authority, membership, and retention are explicit.

**Manage locks and MVCC.** Prepared transactions can hold row/table/advisory locks, uniqueness reservations, predicate locks, transaction ID horizons, old versions, and schema dependencies. Limit count and age, expose owner/business/XID/participants, and alert well before storage or wraparound risk. Kill the originating session does not resolve a detached prepared transaction.

Distributed deadlocks can span participants: x waits at A for y while y waits at B for x. Local detectors see only halves. Use global wait-for detection, wound-wait/wait-die ordering, deterministic scheduling, time-bounded pre-prepare work, or abort/retry protocols. Never time out an already prepared yes branch as if it were active work.

**Optimize without weakening semantics.** A participant that did no writes and holds no relevant state can vote `READ_ONLY`, omit phase 2, and release resources. A single write participant can use one-phase commit only when the coordinator knows no other durable participant exists and recovery semantics preserve the outcome.

Presumed abort omits some abort records/messages by interpreting absent coordinator outcome as abort under carefully defined recovery states. Presumed commit optimizes commit-heavy workloads with different forced-log trade-offs. These are protocols, not permission to guess. Group commit can batch prepare/decision flushes while retaining ordering and durability.

**Choose isolation explicitly.** Atomic commit says either all branches take effect or none. It does not decide a serial order across shards. Strict two-phase locking can hold locks through global commit and support serializability under complete conflict coverage, at latency/deadlock cost. Optimistic/MVCC protocols validate read/write sets or assign timestamps. Predicate constraints and global uniqueness require participants representing those conflicts.

An isolation failure cannot be repaired by a perfectly durable commit decision. Test anomalies across shards, including write skew and phantom predicates.

**Handle topology and schema change.** Pin or version participant routing for the transaction. If a shard splits/moves between branch execution and recovery, the new owner must inherit prepared state and route decisions by XID. A directory epoch alone cannot make the branch disappear. Block incompatible DDL while branches are prepared or make schema transitions interpret old branch state safely.

Recovery discovery must follow authoritative ownership across old/new shard IDs. Keep tombstones/forwarding metadata until every possible prepared XID and late decision expires under governed retention.

**Avoid heuristic outcomes.** Operators may be tempted to `COMMIT PREPARED` or `ROLLBACK PREPARED` to release locks when C is unavailable. That is safe only when authoritative decision evidence exists. A heuristic guess can conflict with another committed branch. If emergency policy permits it, require dual authorization, preserve all logs/state, record the heuristic, block automatic forgetting, and reconcile every participant/business effect.

Do not infer outcome from “probably timed out,” another participant's absence, or business preference. Reconstruct the participant set and consult the authoritative decision protocol.

**Bound operational risk.** Admission-control distributed transactions by count, participant count, age, lock footprint, log/storage footprint, and tenant. Use deadlines before prepare; after prepare, deadlines trigger escalation/recovery, not unilateral abort. Monitor active/preparing/prepared/decided/unacknowledged counts, oldest age, locks, blocked sessions, retries, coordinator quorum, and replica coverage.

Run a continuous recovery scanner: enumerate prepared branches at every resource, join them to coordinator decisions, retransmit outcomes, and flag orphans/unknown XIDs. Protect `RECOVER`/prepared views because XIDs and business metadata can be sensitive. Least-privilege transaction-manager credentials may prepare and resolve only owned branches.

**Compare alternatives.** Prefer local transactions by colocating data when it preserves other goals. Sagas split work into committed steps with compensations; they offer progress and business visibility but not isolation or automatic rollback of irreversible effects. A transactional outbox atomically records an event with one local state change, then delivers it idempotently; it does not atomically commit the consumer.

Escrow/reservations, commutative operations, invariant-confluent designs, and deterministic ordering can avoid 2PC for some invariants. Conversely, disguising a required atomic invariant as retries produces partial state. Choose from domain semantics and failure outcomes, not aversion to protocol latency.

**Validate exhaustive cuts.** Model active, preparing, prepared, decided-commit, decided-abort, locally completed, acknowledged, and forgotten states. Cut coordinator/participant processes, storage, network, replicas, and leaders before/after every durable record and message. Duplicate/reorder prepare/decision/ack; reuse XIDs; lose coordinator quorum; promote replicas; move shards; exhaust prepared slots; hold hot locks; induce global deadlock; change schema; and restart after checkpoints.

The oracle asserts one global outcome, commit only with all yes, no committed branch under global abort, durable prepared recoverability, idempotent decisions, retained authoritative outcome until safe forgetting, serializability/isolation separately, and correct business invariant. Measure prepare/decision latency, blocking duration, lock impact, log growth, recovery time, and uncertain client results.

The finite executable model below demonstrates all-yes commit, one-no abort, idempotent decision replay, and blocking when a prepared participant lacks the decision. It is not a database, durable log, network, replication, concurrency-control, consensus, or XA implementation.

<!-- bijux-verify: {"id":"finite-two-phase-commit","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"all_yes_decision=commit\none_no_decision=abort\ncommit_requires_all_yes=true\nprepared_can_unilaterally_abort=false\ncommit_replay_idempotent=true\nmissing_decision_state=blocked\nevidence=finite_two_phase_commit\n","stderr":""}} -->
```python
def decide(votes):
    return "commit" if votes and all(vote == "yes" for vote in votes.values()) else "abort"

participant = {"state": "prepared", "decision": None}

def apply_decision(branch, decision):
    if branch["decision"] is not None and branch["decision"] != decision:
        raise ValueError("conflicting global decision")
    branch["decision"] = decision
    branch["state"] = "committed" if decision == "commit" else "aborted"
    return branch["state"]

all_yes = decide({"A": "yes", "B": "yes"})
one_no = decide({"A": "yes", "B": "no"})
first = apply_decision(participant, "commit")
second = apply_decision(participant, "commit")
in_doubt = {"state": "prepared", "decision": None}

print(f"all_yes_decision={all_yes}")
print(f"one_no_decision={one_no}")
print(f"commit_requires_all_yes={str(one_no != 'commit').lower()}")
print("prepared_can_unilaterally_abort=false")
print(f"commit_replay_idempotent={str(first == second == 'committed').lower()}")
print(f"missing_decision_state={'blocked' if in_doubt['decision'] is None else 'resolved'}")
print("evidence=finite_two_phase_commit")
```

## Definitions and Notation

- $x$: globally unique transaction identifier (XID).
- $P=\{p_1,\ldots,p_n\}$: closed set of enlisted participants/resource managers.
- $b_i$: branch identifier for participant $p_i$ under x.
- $v_i\in\{YES,NO,READ\_ONLY\}$: participant vote.
- $D\in\{COMMIT,ABORT\}$: single durable global decision.
- **Active:** local branch is executing and has not voted yes.
- **Prepared/in doubt:** durable yes promise exists, but final decision is unknown locally.
- **Transaction manager:** owner of participant discovery, voting, durable decision, recovery, and completion.
- **Resource manager:** transactional system able to durably prepare/commit/rollback one branch.
- **Presumed abort/commit:** optimized logging/recovery protocols assigning meaning to absent records under exact rules.
- **Heuristic outcome:** unilateral resolution without authoritative global decision.
- **Safe forgetting:** removal of protocol state only after no participant/recovery path can still require it.

## Mechanisms, Invariants, or Proof Structure

**Commit validity.** Coordinator code chooses commit only after receiving authenticated durable yes from every member of closed P. Therefore `COMMIT` implies the conjunction of yes votes. Dynamic omission, volatile votes, or participant-set disagreement invalidates the implication.

**Agreement.** C durably records exactly one decision before distribution; participants accept only that decision for x and reject contradictions. Recovery/retransmission eventually makes completed branches agree when decision service and participants become available. Basic 2PC's unique coordinator log is a liveness dependency, not a second permissible decision source.

**Prepared blocking proof.** Consider participant A after durable yes and loss of C. Execution E1 has C durably commit and its message delayed; E2 has C crash before deciding. A's local observation is identical. Aborting is unsafe in E1, while committing is unsafe if another participant voted no in E2. Without additional decision evidence, A can safely choose neither, so it blocks.

**Decision ordering.** If C sends commit before durably recording it, a participant can commit and C can crash/forget, later reconstructing abort. Durable-decision-before-send prevents that recovery contradiction under the log failure model.

**Idempotent completion.** For fixed x and D, reapplying the same decision returns the same durable local terminal state. A different D is a protocol fault. This permits retries after lost acknowledgements without duplicating business effects within the branch.

## Alternatives and Trade-Offs

| Design | Guarantee/benefit | Cost or limitation | Evidence required |
| --- | --- | --- | --- |
| Local transaction | atomicity with one RM | requires colocation | local recovery/isolation tests |
| Basic 2PC | atomic outcome across prepared RMs | blocking and locks | durable votes/decision/recovery |
| Read-only participant | skips phase 2 safely | must hold no commit-relevant state | read-only vote proof |
| One-phase optimization | fewer round trips for one RM | unsafe if hidden participant exists | closed participant set |
| Presumed abort | fewer abort log/messages | exact missing-record semantics | recovery matrix |
| Presumed commit | optimized commit-heavy path | more abort/recovery state | recovery matrix |
| Replicated/Paxos commit | tolerates some coordinator loss | quorum/algorithm complexity | consensus and state replication tests |
| Strict 2PL + 2PC | serializable conflict control + atomicity | distributed deadlock/long locks | global conflict/deadlock tests |
| Saga | independent progress/compensation | no atomic visibility; compensation can fail | business workflow invariants |
| Transactional outbox | atomic local state + event intent | consumer is asynchronous | relay/idempotency/reconciliation |
| Escrow/commutative design | avoids coordination for bounded operations | domain-specific decomposition | invariant proof |

## Failure Modes and Misconceptions

- **“2PC is two-phase locking.”** 2PC is atomic commitment; 2PL is concurrency control.
- **“2PC guarantees serializability.”** Isolation requires a separate global conflict/timestamp protocol.
- **“YES means the branch probably can commit.”** It is a durable promise under the failure model.
- **“Coordinator timeout means abort.”** Commit may already be durably decided and delivered elsewhere.
- **“A prepared participant can release locks.”** Doing so can invalidate the promised later commit/isolation.
- **“A backup coordinator can decide from partial state.”** It needs authoritative replicated participant/vote/decision evidence.
- **“Replication automatically preserves prepare.”** The participant's acknowledged prepare level must cover failover.
- **“Retry with a new XID is recovery.”** It creates another global transaction and possible duplicate effects.
- **“Prepared rows disappear when the session closes.”** Prepared branches are intentionally detached/recoverable in many RMs.
- **“Heuristic rollback is harmless cleanup.”** Another participant may have committed.
- **“A transactional queue makes email atomic.”** The queue enqueue may be transactional; sending/receiving effects need their own protocol.
- **“Shards can move without prepared-state routing.”** Late decisions must find the authoritative branch after movement.
- **“All participants committed means the client saw success.”** Response loss still creates client ambiguity.
- **“Disabling 2PC avoids distributed consistency choices.”** It may merely replace atomicity with partial failure.

## Worked Examples

### Example 1

**Situation.** A and B durably prepare x and vote yes. C records commit, A receives it, then C crashes before B receives it.

**Reasoning.** A commits. B stays prepared because timeout cannot distinguish delayed commit from absent decision. When C's durable log/replica recovers, it retransmits commit; B applies it idempotently and releases locks.

**Conclusion.** Durable decision plus prepared promises preserves agreement across lost messages, with temporary blocking.

### Example 2

**Situation.** A votes yes; B detects a uniqueness violation and votes no.

**Reasoning.** The all-yes commit predicate fails. C durably decides abort and tells both. A must roll back its prepared branch despite being locally valid; B is already or becomes aborted.

**Conclusion.** One no vote forces global abort.

### Example 3

**Situation.** A writes `YES(x)` only in memory, replies yes, crashes, and recovers without the branch after C decided commit.

**Reasoning.** A cannot fulfill the commit promise, while other participants may commit. The protocol's durability premise is broken. A must force sufficient prepare state before replying, including replication coverage if failover can replace it.

**Conclusion.** A volatile yes vote destroys atomic commitment safety.

### Example 4

**Situation.** C sends commit to A, then crashes before writing its decision record. B remains prepared.

**Reasoning.** A has committed, but recovered C may see no commit and choose abort under its rules, splitting the outcome. The correct order is durable global decision before any commit message.

**Conclusion.** Decision logging order is a safety requirement, not an optimization detail.

### Example 5

**Situation.** The client retries a timed-out transfer using new XID y instead of original x.

**Reasoning.** If x committed with a lost response, y is a second valid transfer. Use one stable command-to-XID mapping, query x's authoritative outcome, and replay completion messages rather than re-executing as y.

**Conclusion.** Global transaction identity is the unit of retry and reconciliation.

### Example 6

**Situation.** Prepared x holds a row lock on a popular inventory item while the coordinator decision service is unavailable for 20 minutes.

**Reasoning.** The resource cannot safely abort x merely due to age. New operations block or abort, causing an availability incident. Restore authoritative decision access, then commit/rollback by evidence; monitor prepared age and design coordinator replication/admission to prevent recurrence.

**Conclusion.** 2PC blocking converts coordinator unavailability into retained-lock impact.

### Example 7

**Situation.** x waits at shard A for y, while y waits at shard B for x; both are active but not prepared.

**Reasoning.** Local detectors see one outgoing wait each, not the cycle. A global detector/order protocol finds the cycle and aborts a victim before prepare. Once a branch has prepared yes, arbitrary timeout abort is no longer safe.

**Conclusion.** Distributed deadlock control must operate across participant wait-for edges and respect prepared state.

### Example 8

**Situation.** A transaction reads catalog shard R but makes no writes or retained reservation there; it writes shards A and B.

**Reasoning.** If R can prove its read needs no phase-2 state under the isolation protocol, it votes `READ_ONLY` and leaves. A and B prepare normally. If R's predicate read participates in serializable validation, it may not be safely read-only without retaining conflict metadata.

**Conclusion.** Read-only optimization depends on concurrency-control semantics, not absence of row updates alone.

### Example 9

**Situation.** Shard A moves after preparing x. The old owner is deleted before x's commit decision arrives.

**Reasoning.** If prepared state was not transferred and the new owner cannot resolve branch ID, global completion is lost. Movement must copy/replicate prepared records, preserve XID forwarding/tombstones, and fence ownership only when the new owner can answer recovery.

**Conclusion.** Prepared transactions are part of shard state and routing retention.

### Example 10

**Situation.** An order service needs database row plus customer email notification.

**Reasoning.** SMTP is not a prepare-capable resource manager. 2PC across the database and an SMTP call is impossible. Commit the order and an outbox row locally, deliver email at least once with stable message identity, and record/retry delivery; define business handling for repeated or permanently failed notification.

**Conclusion.** A transactional outbox converts an external effect into asynchronous, idempotent workflow rather than false atomicity.

## Cross-Program Connections

- Distributed Systems owns consensus, failure detectors, replicated logs, and atomic-commit theory; database 2PC composes those mechanisms with resource-manager promises.
- Software Engineering Patterns owns saga, outbox/inbox, idempotent consumer, and compensation patterns used when global atomicity is unavailable or undesirable.
- API and Service Engineering owns stable command IDs, timeout/unknown outcomes, and status lookup across client retries.
- Data Engineering owns exactly-once-effect claims and sink checkpoints; transactional sinks are resource managers only when their prepare/commit semantics are explicit.
- Operating Systems owns durable flush and crash recovery beneath a participant's yes vote.
- Security Engineering owns XID confidentiality, transaction-manager privileges, recovery authorization, and audit of heuristic/manual decisions.

## References

1. C. Mohan, Bruce Lindsay, and Ron Obermarck. [Transaction Management in the R* Distributed Database Management System](https://doi.org/10.1145/7239.7266). *ACM TODS* 11(4), 1986. Two-phase, presumed-abort/commit, recovery, and distributed-deadlock foundations.
2. Jim Gray and Andreas Reuter. *Transaction Processing: Concepts and Techniques*. Morgan Kaufmann, 1993. Atomic commitment, recovery, logging, and transaction-manager foundations.
3. Philip A. Bernstein and Eric Newcomer. *Principles of Transaction Processing*, 2nd ed. Morgan Kaufmann, 2009. XA, resource managers, 2PC, recovery, and concurrency control.
4. Jim Gray and Leslie Lamport. [Consensus on Transaction Commit](https://lamport.azurewebsites.net/pubs/transaction.pdf). *ACM TODS* 31(1), 2006. 2PC blocking and Paxos Commit.
5. The Open Group. [Distributed Transaction Processing: The XA Specification](https://pubs.opengroup.org/onlinepubs/009680699/toc.pdf). X/Open CAE Specification C193, 1991. Transaction-manager/resource-manager and XID model.
6. PostgreSQL Global Development Group. [PostgreSQL 18: Two-Phase Transactions](https://www.postgresql.org/docs/18/two-phase.html). Current prepared-transaction architecture checked 2026-09-05.
7. PostgreSQL Global Development Group. [PostgreSQL 18: `PREPARE TRANSACTION`](https://www.postgresql.org/docs/18/sql-prepare-transaction.html) and [`pg_prepared_xacts`](https://www.postgresql.org/docs/18/view-pg-prepared-xacts.html). Current operational cautions and recovery visibility checked 2026-09-05.
8. Oracle. [MySQL 8.4 Reference Manual: XA Transaction SQL Statements](https://dev.mysql.com/doc/refman/8.4/en/xa-statements.html). Current XID, prepare/commit/rollback, and recover interfaces checked 2026-09-05.
9. Oracle. [MySQL 8.4 Reference Manual: XA Transaction States](https://dev.mysql.com/doc/refman/8.4/en/xa-states.html). Current active/idle/prepared state and detached-XA behavior checked 2026-09-05.
10. Peter Bailis et al. [Coordination Avoidance in Database Systems](https://www.vldb.org/pvldb/vol8/p185-bailis.pdf). PVLDB 8(3), 2014. Invariant-confluence framework for determining when coordination is necessary.

## Exercises

### Exercise 1

Distinguish 2PC from two-phase locking and consensus. State what each contributes to a distributed transaction and what it does not guarantee.

### Exercise 2

Trace a transaction with participants A, B, C where all prepare, the coordinator durably commits, A acknowledges commit, then the coordinator and B become unreachable. State the safe state/action of A, B, C, and a recovering coordinator.

### Exercise 3

A system creates a new XID on every retry, stores coordinator decisions on one ephemeral application host, votes yes before replica flush, and automatically rolls back prepared branches after 60 seconds. Identify at least six failure modes and specify minimum corrections.

### Exercise 4

Compare strict-2PL-plus-2PC, optimistic/MVCC validation plus 2PC, a saga, and transactional outbox for order, inventory, payment, and email. Recommend boundaries and state the remaining failure/consistency behaviors.

### Exercise 5

Design production 2PC across three replicated database shards that can split/move during normal operation. Include XID/enlistment, prepare durability, coordinator replication, isolation/deadlocks, timeouts, topology epochs, failover, recovery scans, operational limits, security, client ambiguity, and exhaustive tests.

## Answers to the Exercises

### Answer 1

**2PC** is an atomic-commit protocol: all enlisted branches reach one commit/abort outcome, but basic 2PC can block and does not impose serializable ordering. **Two-phase locking** is concurrency control: locks grow then shrink, and strict variants retain write locks through commit; it can support serializability but does not coordinate one atomic outcome across independent resource managers. **Consensus** chooses one value consistently among replicas/proposers under its fault/membership model and can replicate coordinator/participant decisions; ordinary consensus does not make `COMMIT` valid when a required participant cannot prepare. A distributed transaction often uses concurrency control for isolation, 2PC rules for unanimous atomic commit, and consensus replication for availability of state.

### Answer 2

A has durably committed and acknowledged; repeated commit is idempotent. B is prepared/in doubt and must retain locks/state—it cannot abort from silence. C (the participant, distinct from the coordinator) is also prepared unless it received the decision; it behaves like B. The recovering coordinator reads its durable `COMMIT` record and complete participant set, then retransmits commit to B and C (and safely to A) until acknowledgements arrive. If the coordinator record was replicated, another authorized leader can do this. It must never choose abort because commit was already durable and visible at A.

### Answer 3

New XIDs duplicate globally committed business operations after response loss. Ephemeral coordinator loss makes decisions unavailable or forgotten. A yes before replica/durable flush can vanish on participant failover. Timeout rollback can conflict with an already durable global commit. The system may forget the participant set, reuse identifiers, leak locks, or allow contradictory recovery leaders.

Map one stable command identity to one globally unique XID and branch set. Close/durably record enlistment. Participants force/replicate complete prepared state before yes. Store exactly one decision in a durable replicated decision service before broadcasting. Treat post-yes timeout as in-doubt escalation, never unilateral abort. Implement idempotent prepare/decision/recover, authenticated epochs, continuous orphan scans, prepared age/count/lock quotas, and client status lookup. Test each crash/message boundary and participant failover.

### Answer 4

Strict 2PL plus 2PC is appropriate when order, inventory reservation, and a transactional payment ledger are true resource managers and require serializable atomic state; it holds cross-service/shard locks and can deadlock/block. MVCC/optimistic validation plus 2PC reduces read locking but must validate all global conflicts/predicates and may abort under contention; it still blocks after prepare.

A third-party payment gateway and SMTP generally cannot promise XA prepare. Treat payment as an idempotent external command with pending/confirmed/failed state and compensation/refund policy—a saga—rather than claim atomicity. Commit order/inventory state plus an outbox event in one local transaction when colocated; otherwise use narrowly scoped 2PC across database shards, then publish. Consumers deduplicate. Email is asynchronous outbox delivery. The remaining behavior includes temporary pending visibility, repeated delivery, failed compensation, and human reconciliation; document it as workflow consistency, not ACID rollback.

### Answer 5

Give each business command one durable globally unique XID; record the closed set of shard IDs, branch IDs, routing epochs, and schema/protocol version. At each replicated shard, prepare validates constraints/isolation, writes undo/redo and branch metadata, retains locks/conflict state, and replicates that prepared record to the same durability needed for shard-leader failover before voting yes. The coordinator decision record and participant set live in a consensus-replicated status service; commit is durably chosen only after every yes, then retransmitted idempotently.

Use strict 2PL with global wait-for detection or an explicitly proven MVCC validation/timestamp protocol. Deadlines before prepare may abort; after yes they trigger recovery escalation. On shard split/move, transfer prepared records and XID forwarding under the same snapshot/delta and ownership epoch; retain old mappings until the maximum recovery horizon. A promoted shard leader must recover branches before serving decisions. Membership/leader fencing prevents stale replicas resolving branches.

A scanner enumerates prepared transactions on every shard, joins them to authoritative decisions, retransmits, and quarantines unknown/orphan XIDs. Limit per-tenant/global active and prepared counts, participants, lock/log footprint, and age; alert on oldest in-doubt, blocked work, decision quorum, and replication coverage. Restrict prepare/recover/commit privileges to authenticated transaction-manager identities, protect XID data, audit manual/heuristic actions, and require dual control for emergency intervention. Clients retry by XID and query outcome; lost responses remain unknown until resolved.

Exhaustively cut coordinator, participant leader/replicas, storage, and network before/after branch mutation, prepare force/replication, yes, decision force, each decision message, local commit, acknowledgement, movement cut, and forgetting. Inject duplicates/reordering, deadlocks, slot/disk exhaustion, stale routing, schema change, shard split, leader failover, coordinator quorum loss, and second failures. Oracles assert commit only after all yes, one global outcome, prepared recoverability, serializability separately, correct participant discovery, idempotent completion, no unsafe forgetting, and the business invariant. Record blocking and recovery duration, not only fault-free throughput.
