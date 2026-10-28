---
module_id: DBE-088
program: Database Engineering
level: 2
module_number: 88
title: Consensus-Backed Replication
status: complete
last_verified: 2026-09-05
---

# Consensus-Backed Replication

## One-Page Review

### Governing question

How does a database turn several fallible replicas into one authoritative, ordered state machine, and which quorum, durability, read, reconfiguration, and operational assumptions make that abstraction honest?

### Essential definitions

A **consensus instance** chooses one value despite concurrent proposals and failures. A **replicated state machine (RSM)** uses a sequence of consensus decisions to give deterministic replicas the same ordered commands. A **term**, **ballot**, or **view** identifies a leadership epoch. A **quorum** is a set large enough to intersect every quorum that could decide a conflicting value. The **leader** sequences proposals; leadership is authority constrained by protocol state, not proof that the node is current. A log entry is **appended** when stored locally, **replicated** when copied, **committed** when the protocol makes its position durable against allowed failures, and **applied** when the state machine executes it. A **linearizable** operation appears to take effect once between invocation and response. A **lease** grants time-bounded authority only under explicit clock and fencing assumptions. A **snapshot** compacts an applied prefix while preserving its last included index, epoch, and state. **Joint consensus** overlaps old and new configurations while membership changes.

### Central model, mechanism, or theorem

For $n=2f+1$ crash-fault replicas, a majority quorum has size

$$q=\left\lfloor\frac{n}{2}\right\rfloor+1=f+1.$$

Any two majorities intersect because $2q>n$. If a protocol preserves accepted log state on the intersection and elects only a leader whose history contains all safely committed entries, two conflicting values cannot both become committed at one log position. This is a conditional safety argument: losing durable protocol state, changing membership without overlap, acknowledging before required persistence, or allowing stale authority breaks its premises. Consensus normally preserves safety without a quorum but cannot promise progress.

### Critical invariants

- One log position has at most one committed command across all epochs and configurations.
- Every quorum capable of committing intersects the quorum evidence used by later leaders.
- A replica never forgets durable vote/accepted/log state required by the algorithm.
- A leader commits only according to the exact protocol rule; local append or follower receipt is insufficient.
- Replicas apply only committed entries, in index order, exactly once to deterministic database state.
- Client deduplication ties a retry to the original command result, not a second mutation.
- Linearizable reads prove current authority and that the serving state includes the required committed prefix.
- Membership changes preserve quorum overlap and never count one physical failure domain as independent replicas.
- Snapshot installation retains configuration, term/index, checksum, and application state consistent with the compacted prefix.
- External side effects are not emitted speculatively from entries that may be overwritten or replayed.

### Common failures

Failures include equating “three copies” with a consensus group; acknowledging a leader-local append; committing an older-term entry with an invalid shortcut; serving linearizable reads from a stale leader; using a lease without bounded-clock and fencing premises; applying uncommitted entries; losing accepted state after disk replacement; non-deterministic state-machine execution; reconfiguring directly from old to disjoint new membership; counting two replicas on one host as two fault domains; snapshotting without membership metadata; replaying a client retry as a new write; letting log catch-up starve foreground traffic; and interpreting safety under partition as availability.

### Compact example

Replicas A, B, and C use majority quorums. Leader A stores command x at index 42 on A and B and commits it. A then fails. Any successful election needs two replicas, so its election quorum intersects {A,B}; with the protocol's log-up-to-date rule, a candidate missing x cannot win from B. The next leader preserves x. If A had replied after storing x only on itself, B and C could elect a history without x: the client-visible write would disappear.

### Connections

Retrieve [Leader Election and Failover](085-leader-election-and-failover.md), [Sharding and Data Placement](086-sharding-and-data-placement.md), and [Distributed Transactions and Two-Phase Commit](087-distributed-transactions-and-two-phase-commit.md). Continue through [the program roadmap](../ROADMAP.md) to distributed SQL/global transactions and explicit consistency, latency, and availability evaluation.

## Governing Question

Replication can copy bytes without establishing which copy is authoritative. During partitions, retries, and simultaneous leadership claims, “send to every replica” does not prevent divergent histories. A database needs a protocol that selects one command for each position, preserves the selected prefix across leader changes, and exposes precisely when a client-visible operation becomes safe.

Consensus-backed replication supplies that ordering within a replication group. It does not by itself provide SQL transactions across groups, serializable execution, correct query evaluation, geographic availability, or immunity to Byzantine behavior. Those properties require additional protocols and assumptions.

## Why This Matters

Modern distributed databases commonly divide the keyspace into ranges or shards, then run a consensus group for each one. A range can survive some replica failures while maintaining a single ordered history; many such groups distribute throughput and capacity. The database layer still must connect consensus entries to MVCC, locks, transaction records, leases, reads, schema versions, and client results.

The gap between algorithm diagrams and production durability is where severe failures occur. An acknowledgement may precede stable storage, a replaced disk may silently erase voting history, a lease may outlive authority, or a snapshot may omit configuration state. Correct operation therefore requires one joined argument spanning consensus protocol, storage, state-machine application, client retry identity, membership, placement, and recovery.

The Raft extended paper, Paxos, Viewstamped Replication, Zab, and production accounts such as *Paxos Made Live* provide primary foundations. Google Spanner and the CockroachDB SIGMOD paper show database compositions rather than a universal recipe. CockroachDB's current stable replication documentation was checked on 2026-09-05; product details are examples, while quorum and state-machine reasoning remains protocol-specific and durable.

## Prerequisites and Retrieval

Retrieve these ideas:

- a crash fault stops or delays a process but does not model arbitrary malicious messages;
- network delay has no reliable upper bound in an asynchronous model, so timeout is suspicion rather than proof;
- durable storage claims depend on flush, device, filesystem, power, and recovery assumptions;
- physical/logical replication alone does not choose one history after conflicting writers;
- a database log record, a consensus log entry, and an applied MVCC mutation are different states;
- leader election must preserve committed history and fence superseded leaders;
- a shard/range is a placement and routing unit; each replication group orders only its own commands;
- 2PC coordinates one atomic outcome across participant groups, whereas consensus replicates the state of a group or coordinator;
- linearizability is a real-time single-object history property, while serializability orders transactions;
- idempotent retry and stable request identity are necessary when responses can be lost.

This chapter assumes crash/recovery faults, authenticated non-Byzantine members, and the exact safety rules of the selected consensus protocol. It does not transfer one algorithm's commit or reconfiguration shortcut to another.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish consensus, replicated state machines, synchronous replication, leader election, and atomic commit;
2. derive majority intersection and connect it to preserved durable state;
3. trace append, replication, commitment, application, and response as separate events;
4. explain election/log rules that prevent a stale leader from overwriting committed history;
5. design linearizable and explicitly stale read paths;
6. reason about snapshots, catch-up, membership changes, and replica replacement;
7. connect per-shard consensus to MVCC and distributed transaction protocols;
8. validate safety and liveness with histories, fault cuts, storage failures, and operational evidence.

## Core Exposition

**Start with the replicated-state-machine contract.** Each replica begins from equivalent application state and processes the same deterministic commands in the same order. Consensus chooses the ordered log; the database state machine interprets each command. If command evaluation reads local wall time, random numbers, environment variables, unreplicated files, or external services, replicas can diverge despite an identical log. Either replicate the chosen value as command data or prove the operation deterministic from replicated state.

The RSM abstraction has layers: proposal, accepted log, committed prefix, application, and externally observed result. A node can contain an entry that is not committed and may later be replaced. Applying or exposing that speculative entry violates the abstraction unless the system has an explicit rollback model that clients cannot confuse with commitment.

**Define fault and persistence models.** Let $n$ be voting replicas and $f$ the maximum simultaneous crash failures tolerated while preserving progress. With majority quorums, $n\ge 2f+1$. This arithmetic assumes independent voters and enough network connectivity; three processes sharing one host, disk, rack, power domain, or operator error do not provide three independent failure domains.

Consensus safety can survive arbitrarily delayed messages and loss of quorum when replicas retain required durable state. Progress needs a sufficiently connected live quorum and, in common partially synchronous protocols, an interval of bounded-enough delay for one leader to stabilize. Disk loss is not merely a process crash if the algorithm assumes votes and accepted entries survive restart.

**Derive quorum intersection.** For a universe of $n$ voters, two sets of size $q$ must intersect when $2q>n$. Majority size is therefore $\lfloor n/2\rfloor+1$. With five voters, any three-member quorum intersects any other three-member quorum. The shared member matters only if it truthfully retains and reports its protocol state; quorum arithmetic cannot compensate for discarded or corrupted history.

Flexible-quorum variants can use different phase/election and write quorum sizes when the algorithm requires their cross-phase intersection rather than every same-phase intersection. Do not change quorum sizes from a slogan. Derive the exact intersections required by the implemented protocol and failure model.

**Separate epochs from authority.** Paxos ballots, Raft terms, and Viewstamped Replication views create monotonically ordered leadership epochs. A candidate gathers quorum evidence before acting. A higher epoch supersedes lower ones, but an integer alone does not fence external resources. Every storage mutation, lease, snapshot, and message must be checked against current replicated authority where stale processes could still act.

In leader-based protocols, election safety depends on history selection. Raft voters compare candidate log term/index and grant at most one vote per term; its rules ensure a leader contains committed entries. Paxos prepare/accept phases make a later proposer preserve values that may already have been chosen. These mechanisms differ internally but solve the same danger: a new leader must not invent a conflicting continuation over committed history.

**Trace the write path.** A client sends stable request identity r and command c to the current routing/leadership authority. The leader validates or evaluates according to database design, appends an entry with epoch/index, persists it as required, and replicates it. Followers validate predecessor/epoch and persist before acknowledging if the protocol's durability promise requires it. Once the exact quorum/term rule is satisfied, the leader advances commit, applies commands in order, and returns a result tied to r.

“Received by a majority” is incomplete. Which entries, which term, which storage boundary, which membership, and which commit rule matter. In Raft, a leader advances commit for an entry from its current term using a majority match index; earlier entries become committed indirectly through log prefix order. Copying an old-term entry to a majority is not, by itself, the general current-term commit test.

**Connect consensus durability to database durability.** A follower acknowledgement may mean bytes entered a process buffer, kernel page cache, device volatile cache, or durable medium. The system's failure claim determines the required boundary. If a power-loss claim requires forced stable storage, acknowledging before that boundary can make an apparent quorum evaporate together after correlated restart.

Checksums, torn-write detection, atomic metadata updates, and log repair protect the accepted state. Recovery must never truncate an entry known committed merely because local metadata is incomplete. When corruption is detected, obtain a verified snapshot/log from an authoritative peer; do not convert corruption into a fresh empty voter that can vote inconsistently.

**Apply in order and deduplicate.** Each replica applies committed index $k$ only after all prior indexes through $k-1$. The application records applied index with state atomically enough that crash replay cannot double-charge or skip a command. A client table maps `(client_id, request_sequence)` to the prior result inside replicated state. Then a retry after lost response returns the original result rather than appending a logically new mutation.

Database engines choose what the command contains. One design replicates logical commands and requires deterministic evaluation. Another evaluates under leader-side latches/MVCC and replicates a deterministic write batch plus metadata. The latter moves nondeterminism before replication but must prove the proposed batch remains valid when applied and that transactional conflict state is represented consistently.

**Design reads separately.** A local replica may be behind or may belong to a former leader. Reading it is useful only under an explicit bounded-staleness/session contract. A linearizable read must establish that the serving authority is current and that its state includes all writes that completed before the read began.

A protocol can append a read barrier/no-op, obtain a quorum confirmation such as a read-index procedure, or use a valid leader lease. A lease removes some read quorum traffic only if clock drift/uncertainty, pause, renewal, transfer, and fencing assumptions make two authorities impossible. A leadership flag or recent heartbeat alone is not a proof. After the read barrier, wait until the local applied index reaches the required committed index.

**Distinguish leader, leaseholder, and transaction coordinator.** They may be colocated for latency but are separate roles. The consensus leader orders entries for one group. A database leaseholder may serve reads and coordinate group requests subject to lease invariants. A transaction coordinator drives a multi-group transaction record and 2PC. Replacing one role does not automatically transfer the other roles' state or authority.

**Snapshot and compact safely.** Unbounded logs are impractical. After applying a prefix through index i, a replica creates a checksummed snapshot containing application state plus last included index/term, configuration, deduplication state, and any database metadata needed for deterministic continuation. Only then may it discard covered log entries under the protocol's retention rules.

A lagging replica can install the snapshot, verify it, atomically switch state, then receive later log entries. Snapshot creation and installation must coordinate with concurrent application, schema versions, encryption keys, and prepared transactions. A file copy whose database pages do not represent one logical applied index is not an RSM snapshot.

**Reconfigure through overlap.** Directly replacing old voters {A,B,C} with disjoint {D,E,F} permits one quorum in each configuration to decide conflicting histories. Joint consensus requires decisions to satisfy quorums of both old and new configurations during the transition, or uses another proven one-at-a-time protocol whose intermediate quorums preserve the necessary overlap.

Add a replica as a non-voting learner, catch it up, verify durability, then promote according to the protocol. Remove failed voters deliberately; automatic replacement must not permit a wiped node to rejoin under old identity while a replacement also votes. Store membership in the replicated log/snapshot, not only in an external orchestration database.

**Compose with sharding and transactions.** A database may run thousands of small consensus groups, one per range. Consensus gives one ordered history within each group; it does not create a single total order across all ranges. A transaction touching A and B still needs a transaction protocol, timestamp/locking rules, and atomic commitment. Its transaction-status record and prepared branches may themselves be replicated by consensus.

Group movement and splitting must preserve both shard ownership and consensus state. Reconfiguration, data snapshot transfer, routing epoch, and authority cut interact. Starting a new group from copied application data without transferring a correct committed cut can create two authoritative histories. Metadata groups are not exempt; their unavailability can halt routing even while data quorums are healthy.

**Budget latency and throughput.** A fault-free write commonly pays routing plus leader communication and at least one round trip to a sufficiently fast quorum, plus persistence and apply/queue time. Geographic voter placement therefore shapes commit latency. Adding voters can improve placement options and fault tolerance only with matching quorum design; it also increases replication traffic and can move the majority farther away.

Batching amortizes flush/network overhead but adds queue delay. Pipelining permits multiple outstanding indexes but requires bounded memory and ordered commit/application. Flow control prevents a slow follower or snapshot transfer from exhausting leader memory/disk. Admission control should protect consensus heartbeats, votes, log replication, and recovery work from foreground overload.

**Treat liveness as an operational property.** Repeated elections can arise from CPU starvation, long runtime pauses, disk stalls, packet loss, asymmetric reachability, priority inversion, or overloaded event loops—not only host failure. Raising timeouts may hide symptoms while increasing failover duration. Observe proposal-to-commit latency, commit-to-apply delay, term/view churn, leader transfer, quorum RTT, fsync latency, match indexes, log growth, snapshots, catch-up, rejected stale messages, and client retry/dedup rates.

Measure per-group behavior and tail distributions; cluster averages hide one hot unavailable range. Alert on loss of placement diversity and on configurations one failure away from quorum loss. Capacity planning must reserve recovery bandwidth so one failure does not make the remaining quorum too overloaded to heal.

**Validate histories and fault cuts.** Unit tests of a happy leader are insufficient. Enumerate elections, concurrent proposals, stale messages, duplicate requests, leader crash before/after local append, follower acknowledgement, quorum commit, application, response, snapshot, and membership transition. Cut power or emulate the claimed durability failure, not only kill processes. Partition asymmetrically, pause clocks/processes, corrupt/truncate logs, replace disks, and restart with stale snapshots.

Safety oracles assert one committed command per index, prefix agreement, state equivalence through equal applied index, monotonic applied index, no lost acknowledged write under the stated model, request deduplication, and valid configuration transitions. Liveness evidence records workload, timing/failure assumptions, quorum availability, and recovery bounds; finite tests cannot prove every execution.

The finite executable model below checks majority sizes and intersections for three and five voters, and demonstrates why two disjoint two-of-four “quorums” are unsafe. It is not a Paxos, Raft, Viewstamped Replication, Zab, storage, network, lease, reconfiguration, or database implementation.

<!-- bijux-verify: {"id":"finite-majority-intersection","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"n3_majority=2\nn3_min_intersection=1\nn5_majority=3\nn5_min_intersection=1\ntwo_of_four_intersects=false\nfive_voters_tolerate=2\nsafety_without_quorum=true\nprogress_without_quorum=false\nevidence=finite_majority_intersection\n","stderr":""}} -->
```python
from itertools import combinations


def majority(n):
    return n // 2 + 1


def minimum_intersection(n):
    q = majority(n)
    groups = [set(c) for c in combinations(range(n), q)]
    return min(len(left & right) for left in groups for right in groups)


print(f"n3_majority={majority(3)}")
print(f"n3_min_intersection={minimum_intersection(3)}")
print(f"n5_majority={majority(5)}")
print(f"n5_min_intersection={minimum_intersection(5)}")
print(f"two_of_four_intersects={str(bool({0, 1} & {2, 3})).lower()}")
print(f"five_voters_tolerate={(5 - 1) // 2}")
print("safety_without_quorum=true")
print("progress_without_quorum=false")
print("evidence=finite_majority_intersection")
```

## Definitions and Notation

- **Consensus:** agreement on one value with validity and integrity under a stated fault model; termination is conditional on liveness assumptions.
- **Replicated state machine:** deterministic application of one consensus-ordered command sequence at multiple replicas.
- **Voter / learner:** a replica that does / does not count in decision and election quorums.
- **Epoch:** monotonically ordered term, ballot, or view that distinguishes leadership attempts.
- **Log index:** position in the replicated command sequence; it is not a wall-clock timestamp.
- **Committed prefix:** indexes whose commands are protocol-safe against allowed future leadership changes.
- **Applied index:** greatest committed position incorporated into local database state.
- **Linearizability:** each completed operation appears at one instant respecting real-time precedence.
- **Quorum loss:** insufficient connected eligible voters for progress; it need not imply conflicting decisions.
- **Fencing:** rejecting effects from superseded authority using protocol-recognized epochs/tokens.
- **Snapshot installation:** verified replacement of state through an included log index, followed by ordered catch-up.
- **Configuration:** authoritative voting membership whose transition is itself protocol state.

## Mechanisms, Invariants, or Proof Structure

**Majority intersection proof.** Suppose two quorums $Q_1,Q_2$ each have $q>n/2$ members. If disjoint, their union would contain $2q>n$ distinct members, impossible in an $n$-member universe. Hence $Q_1\cap Q_2\ne\varnothing$. Safety additionally requires intersection members to preserve and report accepted state.

**Committed-prefix argument.** A protocol defines when value x at index i is chosen/committed. Every later leader-selection quorum intersects the deciding evidence, and the selection rule carries x or a log containing x forward. Inductively, later leaders cannot commit y != x at i. This argument fails if configuration quorums do not overlap or persistent state is erased.

**Application equivalence.** If replicas begin with equal state, apply identical deterministic commands in identical order, and execute no unreplicated mutation, induction on applied index gives equal state after every shared index. Nondeterministic commands or side effects violate the induction premise.

**Availability bound.** In a majority group of $2f+1$, any $f+1$ connected healthy voters can form a quorum, so up to f voter crashes can preserve progress. With only f voters reachable, safety can remain but a new decision cannot be made. Placement correlations can make fewer physical failures remove more than f voters.

**Read proof obligation.** A read returning state through committed index c is linearizable only if the server proves no later authority committed a write before the read's linearization point and applies through the barrier index. Lease, quorum confirmation, or log ordering supplies that proof under different assumptions.

## Alternatives and Trade-Offs

| Design | Benefit | Cost or limitation | Required evidence |
| --- | --- | --- | --- |
| Asynchronous primary/replica | low write latency, simple followers | acknowledged writes can be lost; promotion choice | loss and RPO tests |
| Majority RSM | one fault-tolerant ordered history | quorum latency and loss-of-quorum stalls | protocol/storage history tests |
| Paxos family | flexible proposer/acceptor decomposition | implementation and teaching complexity | ballot/value preservation proof |
| Raft | explicit leader/log/election decomposition | exact current-term and membership rules still subtle | term/log/reconfiguration tests |
| Viewstamped Replication | integrated views and replication | distinct terminology and recovery rules | view-change proof/tests |
| Zab-style atomic broadcast | primary-order broadcast for service state | protocol-specific discovery/synchronization | prefix/order evidence |
| Quorum-confirmed read | avoids clock lease premise | quorum round trip | read-index/applied-index tests |
| Leader lease read | lower read coordination | bounded-clock, pause, renewal, and fencing risk | clock/lease fault tests |
| Stale follower read | local availability/latency | explicit staleness and session anomalies | lag-bound contract |
| Per-range groups | scalable placement and parallelism | cross-range transactions and metadata coupling | group plus transaction tests |

## Failure Modes and Misconceptions

- **“Replication is consensus.”** Copies can diverge without one decision rule.
- **“The leader has committed it.”** A local append is not a quorum-backed commit.
- **“Any majority copy of any entry commits it.”** Protocol epoch and commit rules matter.
- **“No quorum means split brain.”** A correct protocol stops progress and preserves safety.
- **“Three replicas tolerate any two failures.”** Three majority voters tolerate one unavailable voter for progress.
- **“Processes equal failure domains.”** Shared host, rack, power, storage, or control plane creates correlated loss.
- **“A current term proves a current lease.”** Lease authority needs its own bounded-time and fencing evidence.
- **“Followers can serve linearizable reads after a heartbeat.”** State may lag and leadership may have changed.
- **“Consensus makes commands deterministic.”** It orders inputs; the application can still diverge.
- **“Snapshots are ordinary backups.”** They must represent a precise applied prefix and protocol metadata.
- **“Replace membership in one configuration write.”** Disjoint old/new quorums can decide conflicting values.
- **“Consensus replaces 2PC.”** One group order does not atomically commit multiple independent groups.
- **“Committed means applied everywhere.”** Followers may apply later; serving rules must account for apply lag.
- **“Passing chaos tests proves consensus.”** Tests find counterexamples; proof and implementation evidence remain bounded.

## Worked Examples

### Example 1

**Situation.** A three-voter group {A,B,C} commits x using A and B; A then crashes and C starts an election.

**Reasoning.** C needs another vote. B's durable history contains x, so the protocol's up-to-date/history-preservation rule prevents a candidate that would discard x from winning. If B erased its accepted log, quorum intersection would exist only on paper.

**Conclusion.** Majority overlap protects history only when persistent state and election rules preserve it.

### Example 2

**Situation.** Leader A appends a debit locally, replies success, and crashes before B or C stores it.

**Reasoning.** B and C can form the next quorum without the debit. The reply claimed stronger durability than the protocol established. Stable request identity can detect retry, but cannot recover an entry no quorum accepted.

**Conclusion.** Client success must follow the declared commit boundary.

### Example 3

**Situation.** In a five-voter group, voters {A,B,C} accept x while a partition leaves {D,E} together.

**Reasoning.** The two-node side cannot elect or commit with a majority of three. The three-node side may progress if its leader/election conditions hold. If both sides were allowed two-of-five writes, disjoint quorums could choose conflicts.

**Conclusion.** Quorum loss sacrifices progress on the minority side to preserve one history.

### Example 4

**Situation.** A former leader receives a read after being isolated; its local log is applied through 90 while the new leader committed a write at 91.

**Reasoning.** A leadership flag or cached heartbeat cannot exclude the newer leader. A may serve the read only as explicitly stale, or first re-establish current authority and apply through an appropriate barrier.

**Conclusion.** Linearizable reads need authority and freshness evidence.

### Example 5

**Situation.** The command `set_expiry(now()+3600)` is replicated logically to three deterministic state-machine loops.

**Reasoning.** Each replica reads a different local clock and stores a different expiry. Consensus agreed on command text but not its nondeterministic value. The leader must select an expiry and replicate that value, or use a replicated logical time rule.

**Conclusion.** Ordered nondeterminism still diverges replicas.

### Example 6

**Situation.** The system replaces {A,B,C} directly with {D,E,F}; A and B commit x while D and E commit y at the same logical position.

**Reasoning.** Both are majorities within their respective configurations, but the configurations do not intersect. A joint configuration requiring majorities from both sets, or another proven overlapping transition, prevents independent decisions.

**Conclusion.** Membership change is part of consensus safety, not orchestration metadata.

### Example 7

**Situation.** A follower snapshot contains rows through index 500 but omits deduplication records and the active voter configuration.

**Reasoning.** After installation, a retried command may execute twice and the node may vote under stale membership. A valid snapshot must capture all state-machine and protocol metadata required to continue after index 500.

**Conclusion.** Snapshot completeness is defined by recovery invariants, not table bytes alone.

### Example 8

**Situation.** One range's three voters occupy separate processes but all use one physical host.

**Reasoning.** Process restart testing shows apparent tolerance, yet one host, power, filesystem, or kernel failure removes the entire quorum. Placement must map voters to independent failure domains appropriate to the service objective.

**Conclusion.** Logical replica count is not physical fault tolerance.

### Example 9

**Situation.** A transfer touches ranges R1 and R2, each with a healthy Raft group.

**Reasoning.** Each group can order its own debit or credit, but neither local log alone ensures both effects commit. A transaction record, concurrency-control protocol, and atomic commitment still coordinate the two groups; consensus can replicate each participant's state.

**Conclusion.** Per-range consensus is a component of, not a substitute for, distributed transactions.

### Example 10

**Situation.** After one voter fails, snapshot catch-up of its replacement saturates the two survivors; heartbeats time out and leadership churns.

**Reasoning.** The group had logical quorum but insufficient recovery headroom. Rate-limit snapshot traffic, prioritize consensus control traffic, reserve disk/network/CPU, and monitor term churn and apply lag while healing.

**Conclusion.** Liveness depends on capacity and scheduling as well as voter arithmetic.

## Cross-Program Connections

- Distributed Systems owns general consensus proofs, partial synchrony, atomic broadcast, membership, and formal verification; this module applies them to database logs, reads, and state.
- Operating Systems owns persistence boundaries, torn writes, filesystem/device behavior, scheduling pauses, and crash recovery beneath durable votes.
- Data Structures Engineering owns persistent logs, indexes, checksums, and snapshot representations.
- Systems Engineering owns failure-domain placement, capacity margins, recovery objectives, and coupled control-plane risk.
- Security Engineering owns member authentication, message integrity, key rotation, anti-replay, and Byzantine threat boundaries.
- API and Service Engineering owns stable request identity, uncertain responses, retry/status contracts, and client-visible linearizability.

## References

1. Leslie Lamport. [Paxos Made Simple](https://lamport.azurewebsites.net/pubs/paxos-simple.pdf). *ACM SIGACT News* 32(4), 2001. Ballots, majority acceptance, and value preservation.
2. Diego Ongaro and John Ousterhout. [In Search of an Understandable Consensus Algorithm](https://raft.github.io/raft.pdf). USENIX ATC, 2014, extended version. Raft election, log, commitment, membership, and safety foundations.
3. Barbara Liskov and James Cowling. [Viewstamped Replication Revisited](https://pmg.csail.mit.edu/papers/vr-revisited.pdf). MIT-CSAIL-TR-2012-021, 2012. View changes and replicated service operation.
4. Tushar D. Chandra, Robert Griesemer, and Joshua Redstone. [Paxos Made Live: An Engineering Perspective](https://research.google/pubs/paxos-made-live-an-engineering-perspective/). PODC, 2007. Production gaps between protocol and implementation.
5. Patrick Hunt et al. [ZooKeeper: Wait-free Coordination for Internet-scale Systems](https://www.usenix.org/legacy/event/atc10/tech/full_papers/Hunt.pdf). USENIX ATC, 2010. Zab-backed coordination-service architecture and client semantics.
6. James C. Corbett et al. [Spanner: Google's Globally-Distributed Database](https://research.google/pubs/spanner-googles-globally-distributed-database-2/). OSDI, 2012. Per-partition replication and database transaction composition.
7. Rebecca Taft et al. [CockroachDB: The Resilient Geo-Distributed SQL Database](https://www.cockroachlabs.com/pdf/cockroachdb-the-resilient-geo-distributed-sql-database-sigmod-2020.pdf). SIGMOD, 2020. Range replication, leases, MVCC, and transaction integration.
8. Heidi Howard, Dahlia Malkhi, and Alexander Spiegelman. [Flexible Paxos: Quorum Intersection Revisited](https://arxiv.org/abs/1608.06696). OPODIS, 2016. Cross-phase rather than universal quorum-intersection requirements.
9. Diego Ongaro. [Consensus: Bridging Theory and Practice](https://web.stanford.edu/~ouster/cgi-bin/papers/OngaroPhD.pdf). Stanford PhD dissertation, 2014. Raft implementation, reads, clients, and membership detail.
10. Cockroach Labs. [Replication Layer](https://www.cockroachlabs.com/docs/stable/architecture/replication-layer.html). Current stable documentation for range replicas, Raft, leases, snapshots, and rebalancing, checked 2026-09-05.

## Exercises

### Exercise 1

Distinguish consensus, a replicated state machine, synchronous replication, leader election, and two-phase commit. State one guarantee and one non-guarantee for each.

### Exercise 2

For groups of 3, 4, 5, and 7 voters, compute majority quorum size and tolerated unavailable voters for continued progress. Prove any two majority quorums intersect, then explain why durable state is still required.

### Exercise 3

A five-voter database acknowledges after leader-local append, serves reads from any recent follower, uses local wall time inside replicated commands, and wipes failed voters before rejoining them with the same identity. Diagnose the safety and client-semantic failures and specify corrections.

### Exercise 4

Compare a quorum-confirmed linearizable read, a leader-lease read, and a bounded-stale follower read for a multi-region database. State assumptions, latency, failure behavior, and suitable workload for each.

### Exercise 5

Design a consensus-backed replication group for a sharded transactional database. Include command representation, persistence/acknowledgement, reads, retries, snapshots, reconfiguration, placement, transaction composition, observability, recovery capacity, security, and validation.

## Answers to the Exercises

### Answer 1

**Consensus** selects one value under a fault model; it does not execute database semantics or coordinate every shard. An **RSM** applies a consensus-ordered deterministic command sequence to produce equivalent replica state; it does not make nondeterministic code deterministic or external side effects atomic. **Synchronous replication** waits for selected replica acknowledgements; without a protocol for authority, quorum intersection, and failover history it does not alone prevent divergent primaries. **Leader election** selects an authority epoch while preserving history under its protocol; it does not make a leader's local append committed. **2PC** obtains one commit/abort outcome across prepared resource managers; it can block and does not choose each participant's replicated log. A database may compose all five mechanisms at distinct layers.

### Answer 2

Majority size is $q=\lfloor n/2\rfloor+1$ and progress tolerates $n-q$ unavailable voters: for 3, $q=2$ and one unavailable; for 4, $q=3$ and one; for 5, $q=3$ and two; for 7, $q=4$ and three. Even-sized majority groups spend an extra replica without increasing the crash-progress bound relative to the preceding odd size.

For any two majorities $Q_1,Q_2$, both sizes exceed $n/2$. If they were disjoint, $|Q_1\cup Q_2|=|Q_1|+|Q_2|>n$, impossible. Thus they intersect. The proof establishes a shared voter, not preserved knowledge. If that voter forgets a vote or accepted entry after restart, lies, or is replaced under the same identity with empty state, later leadership cannot recover the evidence the protocol relies on. Durable protocol state and identity/recovery rules are therefore premises of safety.

### Answer 3

Leader-local acknowledgement can be lost when that leader fails before replication, so successful writes may disappear. Recent-follower reads can violate linearizability because “recent” proves neither current authority nor inclusion of writes completed before the read. Local wall time makes replicas compute different state from the same command. Wiping a voter erases votes/log entries and reusing its identity can make one logical member vote inconsistently across histories.

Reply only after the implemented protocol's quorum, epoch, and stable-storage commit rule holds, then apply through that index. Serve linearizable reads through a log/read-index barrier or a proven lease and wait for applied state; label local follower reads with explicit staleness semantics. Select time/random/external values once and replicate them as data. Recover a failed voter from a verified snapshot/log as a learner, give replacements controlled identity, and promote only through a safe membership transition. Preserve terms, votes, configuration, deduplication, and accepted entries durably.

### Answer 4

A **quorum-confirmed read** proves the leader is current by communicating with a quorum, obtains a commit/read barrier, waits for local application, and reads. It avoids bounded-clock assumptions but pays quorum latency; use it for infrequent strongly consistent reads or when clocks/leases are unsuitable.

A **leader-lease read** serves locally while a non-overlapping authority lease is valid. It can lower latency and load for read-heavy strong-consistency workloads, but needs bounded clock uncertainty/drift, pause handling, conservative renewal/expiry, lease-transfer ordering, fencing, and applied-index checks. On uncertainty it must stop or fall back rather than guess.

A **bounded-stale follower read** is local and remains available on replicas that cannot contact a quorum, provided the application accepts a stated timestamp/index/lag bound. It can return data older than a completed write and may violate read-your-writes unless session routing/tokens repair that. It suits analytics, feeds, and caches with explicit staleness budgets, not uniqueness checks or read-after-write control decisions.

### Answer 5

Use an odd number of voters placed across independent failure domains and document the crash, storage, partition, and corruption model. Encode each entry with group/configuration ID, epoch/index, schema version, stable client/request sequence, and a deterministic mutation or validated write batch. Persist terms/votes/log at the boundary required by the service durability claim; acknowledge only after the exact protocol commits and the result can be recovered. Apply committed entries in order with atomic applied-index/state updates and replicated result deduplication.

Provide linearizable reads via a quorum/read-index barrier or a rigorously fenced lease, always waiting for the needed applied index. Offer follower reads only with explicit timestamp/index staleness and session semantics. Snapshot one consistent applied prefix including configuration, term/index, MVCC/lock/transaction state, schema, encryption metadata, and dedup records; checksum, atomically install, then catch up. Add replacements as learners, verify catch-up and durable identity, and use joint/otherwise proven overlapping reconfiguration before removing old voters.

Each range owns one group, while routing metadata identifies its configuration and authority. Split/move only through a committed state cut and fenced ownership transition. Cross-range serializability and atomicity use MVCC/locking/timestamp validation plus 2PC; consensus replicates participant prepare and transaction-status records but does not replace that protocol. Authenticate and authorize members, bind messages to group/epoch, protect keys and snapshots, audit membership, and define the non-Byzantine boundary.

Observe proposal, quorum, persistence, commit, apply, and read latency separately; term churn, quorum RTT, match/applied indexes, log/snapshot size, catch-up, rejected stale messages, placement diversity, dedup hits, and per-range availability. Reserve CPU, disk, and network for heartbeat and repair under one failure. Validate model invariants and implementation histories across every crash/message/storage/snapshot/reconfiguration cut, asymmetric partitions, pauses, corruption, disk replacement, duplicates, nondeterministic inputs, clock faults for leases, overload, and rolling versions. Report both counterexamples found and the exact finite scope tested.
