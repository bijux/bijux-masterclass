---
module_id: DBE-090
program: Database Engineering
level: 2
module_number: 90
title: Evaluating Consistency, Latency, and Availability Trade-Offs
status: complete
last_verified: 2026-09-05
---

# Evaluating Consistency, Latency, and Availability Trade-Offs

## One-Page Review

### Governing question

How should an engineer evaluate a distributed database's consistency, latency, and availability claims without collapsing precise history properties, fault-contingent impossibility results, normal-operation costs, and business requirements into slogans?

### Essential definitions

A **consistency model** is a set of permitted operation histories. **Linearizability** requires each operation on an object to appear atomic between invocation and response while respecting real-time precedence. **Serializability** requires transactions to match some serial order; **strict serializability** adds real-time precedence. **Staleness** measures how far an observation trails an authoritative version, logical position, or time. In the Gilbert–Lynch CAP model, **availability** requires every request received by a non-failing node eventually to return a response; it is not an ordinary percentage SLO. A **network partition** prevents required messages between components for an unbounded interval. **Safety** says a bad history never occurs; **liveness** says desired progress eventually occurs under stated conditions. A **quorum** is a response/decision set with defined intersection properties. **Tail latency** is a high percentile or worst relevant response time, not the mean. **Recovery point objective (RPO)** bounds tolerable lost data; **recovery time objective (RTO)** bounds restoration time. **PACELC** is a design heuristic: during partition, availability versus consistency; else, latency versus consistency. It is not the formal CAP theorem.

### Central model, mechanism, or theorem

In the asynchronous read/write-object model used by Gilbert and Lynch, no implementation can simultaneously guarantee atomic consistency, availability at every non-failing node, and tolerance of arbitrary message loss. During a partition separating replicas, a write accepted on one side cannot be known on the other. The other side must either answer a read without that knowledge, risking a non-linearizable result, or wait/refuse, violating the model's availability requirement.

The theorem is conditional and fault-specific. It does not say “choose any two forever,” compare serializability with uptime percentage, prescribe one database architecture, or eliminate design space. Outside partitions, coordination still creates latency; weaker histories, bounded staleness, locality, asynchronous replication, invariant decomposition, and degraded operations create different trade-offs that must be measured under explicit workloads and failures.

### Critical invariants

- Name the exact history property, its object/transaction scope, and every session or real-time clause.
- Name availability per operation, region, fault, deadline, and acceptable error/degraded result.
- Separate CAP availability from measured SLO availability and recovery objectives.
- State the fault model: delay, loss, partition topology, crash, storage loss, corruption, clock failure, and correlated domains.
- Measure latency distributions by operation path and participant/quorum geography, including timeouts and retries.
- Treat timeout/unknown outcome as a distinct result, never an inferred abort.
- Connect consistency choices to concrete business invariants and anomaly costs.
- Verify durability, isolation, replica consistency, and freshness separately.
- Include recovery and repair load in availability and latency evaluation.
- Restrict every conclusion to the tested versions, configuration, topology, workload, duration, and history checker.

### Common failures

Failures include “CAP means pick two”; calling eventual convergence “AP” without availability semantics; calling a majority system unavailable because one node fails; equating serializability with linearizability; using `R+W>N` as a universal proof; reporting mean latency without aborts/timeouts; measuring steady state but not partitions or repair; hiding stale reads behind cache terminology; treating clock time as causal truth; comparing different durability settings; excluding unknown results; accepting business-invariant violations because replicas later converge; testing one key while claiming transactional scope; and converting a consistency knob into a marketing category.

### Compact example

Five replicas require a three-voter write quorum. A partition leaves groups of three and two. The three side can commit; the two side cannot commit a strong write. If the two side returns “success” for an independent write, both sides may create irreconcilable real-time histories. If it rejects or waits, strong safety remains while CAP availability on that side does not. It may still serve an explicitly stale catalog read if that operation's contract permits it. The choice is per operation and invariant, not one label for the entire product.

### Connections

Retrieve [Replication Lag and Stale Reads](084-replication-lag-and-stale-reads.md), [Consensus-Backed Replication](088-consensus-backed-replication.md), and [Distributed SQL and Global Transactions](089-distributed-sql-and-global-transactions.md). Continue through [the program roadmap](../ROADMAP.md) to specialized engines and production database operations.

## Governing Question

Distributed database discussions often combine four different questions: which histories are legal, which requests complete during a fault, how long completed requests take, and how much committed data survives. A single “consistent and highly available” claim cannot answer them. One operation can be linearizable but slow across regions; another can be locally available but stale; a transaction can be atomic yet non-serializable; a service can meet 99.99% uptime while refusing minority-partition writes exactly as its safety model requires.

Evaluation begins by replacing adjectives with contracts. Define operations, histories, scope, fault model, deadlines, durability, freshness, and business invariants. Then design experiments and formal checks that can falsify each claim.

## Why This Matters

The wrong trade-off can lose money, oversell inventory, violate authorization revocation, show old medical orders, or make a supposedly durable acknowledgement disappear. The opposite mistake also costs: imposing global coordination on harmless counters, feeds, or analytical snapshots can add wide-area latency and reduce availability without protecting a required invariant.

The CAP theorem is valuable because it exposes one unavoidable failure-time choice. Its popular “two of three” paraphrase is too coarse for engineering. Real systems make many choices: per operation, data class, region, topology, quorum, transaction scope, staleness bound, and degraded mode. They also operate mostly outside total partitions, where coordination latency, tail amplification, and repair capacity matter.

This module uses Gilbert and Lynch's formal result, Brewer's retrospective, Abadi's PACELC framing, highly available transaction and invariant-confluence research, and history-based consistency work. These are durable conceptual sources; no current vendor ranking is asserted.

## Prerequisites and Retrieval

Retrieve these ideas:

- replication lag is multi-dimensional: receive, durable, replay/apply, visibility, and wall-clock age;
- quorum intersection preserves evidence only with correct protocol and durable member state;
- consensus can preserve safety without quorum while losing progress;
- serializability and strict serializability concern multi-operation transactions, while linearizability is commonly stated per object;
- snapshot isolation can admit write skew despite atomic commit;
- asynchronous timeouts reveal uncertainty, not remote failure or outcome;
- a distributed transaction's latency follows its slowest required participant/quorum path;
- retry changes offered load, contention, and observed latency;
- RPO/RTO and durability are not consistency models;
- business invariants determine which anomalies matter.

We assume non-Byzantine components unless explicitly varied. “Available” never means “some endpoint returned some bytes”; the response must satisfy the defined operation contract.

## Learning Objectives

After completing this module, you should be able to:

1. state CAP's model and partition argument without the “choose two” misconception;
2. distinguish consistency models, freshness, durability, CAP availability, SLO availability, RPO, and RTO;
3. derive simple quorum intersection and latency consequences without overgeneralizing them;
4. translate a business invariant into operation-specific safety and degraded-mode contracts;
5. construct workload/fault matrices and collect latency, availability, staleness, and history evidence;
6. compare strong, causal/session, bounded-stale, and convergent designs honestly;
7. diagnose misleading benchmark and vendor claims;
8. make a documented, reversible production decision with explicit residual risk.

## Core Exposition

**Define histories before labels.** An operation history records invocation, response, process/session, arguments, results, and relevant real-time relationships. A consistency model accepts or rejects histories. “Strong consistency” is not sufficiently precise: it might mean linearizable registers, strict-serializable transactions, sequential consistency, session guarantees, or simply synchronous replication.

State scope. A system may provide linearizable metadata but stale table reads, serializable transactions without real-time order, single-key linearizability but weaker multi-key transactions, or strong primary-region writes with asynchronous disaster-recovery replicas. A test over one register cannot establish a multi-object transaction claim.

**Separate replica consistency and transaction isolation.** Replica consistency constrains observations across copies and clients. Transaction isolation constrains interleavings of multi-operation units. A database can synchronously replicate each shard while allowing write skew across shards, or provide serializable transactions whose read-only snapshots intentionally serialize in the past. Atomic commitment says all transaction branches share an outcome, not that the history is serializable or fresh.

**State CAP precisely.** Gilbert and Lynch formalize atomic consistency, availability, and partition tolerance in an asynchronous network model. Partition tolerance is the requirement that the system continue satisfying its chosen guarantees despite arbitrary message loss between components. During a partition, separated nodes cannot distinguish delayed messages from absent information.

Suppose a write completes on side A. A later read arrives at non-failing side B, which cannot communicate with A. Returning the old value contradicts atomic/linearizable ordering; waiting forever or rejecting contradicts the theorem's availability requirement. Randomization, clocks, and retries do not reveal the missing write. Thus both properties cannot be guaranteed for every partition execution.

This is not a rule that a designer freely drops partition tolerance while the network partitions. A single-node service may avoid distributed partitions but has different fault availability. A distributed service can prioritize safety and refuse some operations, prioritize response and permit histories a stronger model forbids, or expose multiple operations with different contracts.

**Do not confuse availability definitions.** CAP availability is qualitative eventual response from every non-failing node in the model, with no fixed deadline. A service-level objective such as 99.99% successful requests within 500 ms is quantitative, scoped to traffic and a time window. RTO concerns recovery duration after an incident. Yield/uptime may exclude invalid requests, planned maintenance, or specific regions. Report all denominators, exclusions, and semantics.

A safety-preserving database may return a prompt “quorum unavailable” error. That is operationally responsive but not a successful read/write in the CAP definition. Conversely, a system could eventually answer after hours and satisfy the theorem's liveness definition while failing every practical latency SLO.

**Use PACELC as a question generator.** PACELC highlights two situations: if a partition occurs, systems trade some consistency against some availability; else, many designs trade consistency/coordination against latency. This is a taxonomy, not a universal theorem or binary product label. Even without partitions, local reads, leader reads, quorum reads, commit waits, synchronous cross-region writes, and asynchronous replicas yield different latency/freshness points.

Ask which operation, consistency property, partition topology, and latency percentile. A database can make different choices for catalog browse, account debit, authentication revocation, analytics, and backups.

**Derive quorum arithmetic carefully.** In a simple fixed membership of N replicas, requiring read quorum R and write quorum W with $R+W>N$ makes every read set intersect every write set. Requiring $2W>N$ makes write quorums intersect. With version comparison and correct durable participants, those conditions help find a recent value.

They do not by themselves prove linearizability, transactional isolation, safe membership change, correct conflict resolution, or durability. Concurrent writes, sloppy quorums, hinted handoff, clock-based last-write-wins, stale topology, erased state, and read repair alter the model. Consensus protocols impose additional epoch/history rules. Use `R+W>N` only inside its stated algorithm.

**Model latency by critical path.** A quorum acknowledgement is commonly determined by an order statistic: the slowest member among the fastest sufficient quorum, plus leader, persistence, queueing, and processing costs. It is not the sum of all replica RTTs. For a distributed transaction, sequential stages add while parallel participants contribute their maximum; retries and contention add new attempts.

Report p50, p95, p99, p99.9, maximum relevant window, abort rate, timeout rate, and unknown-outcome rate. Condition results by local/cross-region path, participant count, payload, key popularity, durability mode, and fault state. Coordinated omission can hide periods when the system could not accept offered work; open-loop and closed-loop load produce different evidence.

**Measure availability per operation.** Define an operation matrix: read current value, read at bounded staleness, write one key, conditional write, multi-key transaction, schema operation, backup, or recovery query. For each fault, state allowed success, explicit failure, waiting, stale success, and recovery behavior.

Availability is asymmetric. A minority partition may safely serve immutable content or an old snapshot but not a linearizable conditional update. A primary-region outage may leave local historical reads while global writes stop. Dependencies such as metadata, timestamp oracle, key service, DNS, identity, and transaction status can reduce effective availability even when data replicas have quorum.

**Translate business invariants.** Begin with consequences: balances conserve value, one coupon redeems once, revoked credentials stop authorizing, inventory never falls below zero, profiles converge, feed order may lag. Identify operations that can commute or be escrowed and those requiring coordination.

Invariant confluence asks whether independently valid transactions can merge without violating the invariant. If yes, coordination may be avoidable for that workload. If no, some coordination, partition ownership, escrow allocation, or rejected operation is required. “Eventually consistent” is not permission to violate a permanent invariant before convergence.

**Define staleness explicitly.** Version staleness counts committed positions; time staleness measures age relative to an authoritative timeline; bounded-staleness contracts constrain both delay and knowledge. A read at replica apply index 100 is not “fresh” without knowing the latest relevant committed index. Wall clocks can mismeasure lag under skew.

For session guarantees, track causal/session tokens: read-your-writes, monotonic reads, monotonic writes, and writes-follow-reads. Sticky routing can help but is an assumption, not a global guarantee. Causal consistency preserves dependencies while allowing concurrent operations to appear in different orders; it is neither arbitrary eventual behavior nor linearizability.

**Compare conflict resolution semantics.** Last-write-wins discards all but one version according to a timestamp/order; it can lose logically concurrent updates and depends on timestamp semantics. Multi-value registers preserve conflicts for resolution. CRDTs provide convergent merge for specific data types under delivery assumptions but do not automatically preserve arbitrary cross-object invariants.

Application merge must be associative, commutative, and idempotent where replay/order vary, or carry sufficient causal metadata. A shopping cart union and a bank balance have different correctness needs. Tombstones and deletion retention complicate convergence and storage.

**Include durability and disaster recovery.** A linearizable history can still lose data after a disaster if acknowledgements rely on replicas in one correlated domain. Conversely, an asynchronously replicated backup may meet a nonzero RPO while not serving current reads. State acknowledgement persistence, failure domains, backup/restore, RPO, RTO, and corruption recovery separately.

Test power/device/domain loss, not only process termination. Verify restored state against acknowledged-operation history, checksums, and business invariants. Measure repair bandwidth and time; degraded replication increases risk and tail latency.

**Account for clocks and leases.** Physical time supports bounded-staleness and external-order techniques only when uncertainty, drift, synchronization failure, process pause, and fencing are modeled. A lease may lower read latency by avoiding a quorum round trip, but must ensure stale holders cannot serve after authority transfers.

Hybrid/logical clocks preserve useful ordering without claiming perfect physical time. Never compare client timestamps from unsynchronized hosts as proof that the newest write won. Inject clock steps, drift, uncertainty growth, leap behavior where relevant, and long process pauses.

**Design the experiment matrix.** Cross workload dimensions (read/write mix, transaction size, key skew, payload, concurrency, region) with topology (replicas, voters, placement), consistency/durability configuration, and faults (delay, loss, partition shapes, crash, pause, disk stall/full/corruption, clock, dependency outage, repair). Predefine hypotheses and oracles.

Collect complete histories with stable operation IDs, invocation/response times from a trustworthy harness, session identity, arguments, results, and uncertainty/timeout classification. Verify clocks only to the extent the checker needs. Preserve server logs/config/version and fault timing. A history checker can establish a counterexample; a passed finite run supplies bounded evidence, not a proof.

**Test the dangerous boundaries.** Partition before and after write acknowledgement; isolate leader from followers and clients asymmetrically; delay only acknowledgements; pause processes; reorder retry responses; lose the client after commit; change membership; start repair; corrupt a replica; and overlap schema/range movement. Run enough duration to cover elections, anti-entropy, GC, compaction, backups, and repair.

Measure during fault, not only before and after. A system that recovers eventually can still violate latency or availability for hours. A system that returns quickly can still return an illegal value. Track recovery convergence and whether repair overwrites the correct version.

**Evaluate degraded modes as APIs.** If strong writes fail, can the product accept a queued command, allocate from regional escrow, or offer a stale read? Define response types so callers cannot mistake “accepted for later” for “committed.” Attach version/snapshot age where safe, preserve stable identity, and reconcile explicitly.

Degradation must respect authorization and privacy. Serving cached public catalog data may be acceptable; serving stale revocation or residency metadata may not. Test transitions into and out of degraded mode, because overlapping strong and weak writers can violate assumptions.

**Make the decision auditable.** Write an evidence table: requirement, formal/operational definition, configuration, measured result, counterexamples, residual risks, and owner. Record costs including latency, unavailable operations, stale decisions, reconciliation work, complexity, and recovery burden. Prefer reversible knobs only when applications can correctly interpret every mode.

Reject conclusions based on brand categories. The same database can expose several consistency levels, transaction scopes, replica-read modes, and durability settings. Evaluate the exact version and configuration actually deployed.

The executable fixture below checks majority/quorum arithmetic, an order-statistic latency, an illustrative monthly SLO allowance, and a staleness decision. It is not a CAP proof, database, consensus protocol, availability experiment, history checker, or production SLO calculation.

<!-- bijux-verify: {"id":"finite-tradeoff-checks","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"majority_5=3\nr3_w3_intersect=true\nr1_w3_intersect=false\nquorum_ack_ms=47\nmonthly_99_99_downtime_min=4.32\nlag_within_200ms=false\nminority_strong_write_available=false\nsafety_can_hold_without_progress=true\nevidence=finite_tradeoff_checks\n","stderr":""}} -->
```python
replicas = 5
majority = replicas // 2 + 1
latencies_ms = sorted([8, 12, 47, 55, 90])

print(f"majority_5={majority}")
print(f"r3_w3_intersect={str(3 + 3 > replicas).lower()}")
print(f"r1_w3_intersect={str(1 + 3 > replicas).lower()}")
print(f"quorum_ack_ms={latencies_ms[majority - 1]}")
print(f"monthly_99_99_downtime_min={30 * 24 * 60 * (1 - 0.9999):.2f}")
print(f"lag_within_200ms={str(240 <= 200).lower()}")
print("minority_strong_write_available=false")
print("safety_can_hold_without_progress=true")
print("evidence=finite_tradeoff_checks")
```

## Definitions and Notation

- **History H:** invocations and responses with process/session and real-time relations.
- **Consistency model:** set of histories declared legal.
- **Safety / liveness:** nothing bad occurs / something good eventually occurs under assumptions.
- **CAP availability:** every request at a non-failing node eventually completes in the formal model.
- **SLO availability:** measured success/latency target over a stated population and window.
- **Partition:** communication failure separating components for the relevant protocol interval.
- **Freshness/staleness:** distance from an authoritative version, position, or time.
- **N, R, W:** fixed replica count, read quorum size, and write quorum size in a simplified quorum model.
- **Tail latency:** high-quantile latency including defined errors/retries rather than only successful means.
- **RPO / RTO:** acceptable data-loss bound / acceptable recovery-duration bound.
- **Degraded operation:** explicitly weaker or deferred result with a distinct contract.
- **Residual risk:** failure or anomaly not eliminated by the chosen design and controls.

## Mechanisms, Invariants, or Proof Structure

**Partition argument.** After write w completes at A, real-time linearizability requires later read r at B to return w or later. With all A–B messages lost, B's local state is indistinguishable from an execution without w. Returning old state violates consistency in the execution with w; waiting forever violates availability. The contradiction depends on the formal definitions and asynchronous partition execution.

**Quorum intersection.** For fixed universe N, if $R+W>N$, a disjoint read and write set would contain R+W distinct members, impossible. If $2W>N$, two write sets intersect. This set proof says nothing about which version the intersection member reports or whether protocol metadata is durable.

**Tail amplification.** A parallel operation completing after all k independent components has CDF $F_{max}(t)=F(t)^k$. Even with simplifying independence, more participants worsen the maximum's tail. Real components are correlated, so measure rather than extrapolate blindly.

**SLO arithmetic.** A 99.99% monthly availability target over a simplified 30-day continuous denominator permits $0.0001\times30\times24\times60=4.32$ minutes outside target. Real SLOs must define requests, windows, exclusions, error budgets, and latency threshold.

**Invariant decision rule.** If two partition-local valid updates can merge and preserve invariant I, coordination may be avoidable for those operations. A counterexample merge that violates I proves that unrestricted independent acceptance is unsafe; it does not prescribe which coordination/escrow/ownership mechanism to choose.

## Alternatives and Trade-Offs

| Choice | Benefit | Cost/risk | Evidence |
| --- | --- | --- | --- |
| Linearizable operation | real-time single-object semantics | quorum/authority unavailability and latency | operation histories |
| Strict-serializable transaction | global serial order respecting real time | conflict and multi-group coordination | transactional histories |
| Serializable transaction | strong isolation without required real-time order | stale-but-serial legal placement | dependency graphs |
| Causal/session consistency | preserves dependencies with local progress | concurrent operations need no single order | session/causal histories |
| Bounded-stale read | local predictable read when safe time advances | explicitly old data | version/time lag evidence |
| Convergent/CRDT state | offline/concurrent updates for suitable type | metadata, tombstones, limited invariants | merge algebra + histories |
| Majority quorum | fault-tolerant authoritative decisions | slowest-needed replica and quorum loss | protocol/fault tests |
| Asynchronous replica | low primary-path latency, DR/read scaling | nonzero lag/RPO, stale promotion risk | lag/restore/failover evidence |
| Escrow/partitioned ownership | local acceptance within allocated bounds | allocation/rebalancing complexity | invariant proof |
| Explicit rejection/queue | preserves invariant during partition | unavailable or delayed business operation | degraded-mode SLO |

## Failure Modes and Misconceptions

- **“CAP says choose two.”** It describes incompatible guarantees during specified partition executions.
- **“CA means a distributed system ignores partitions.”** A real partition still forces behavior or violates assumptions.
- **“AP means every response is correct eventually.”** The allowed history and convergence/conflict rules must be defined.
- **“CP means the service is usually down.”** It may tolerate minority failures and refuse only operations lacking authority.
- **“99.99% availability satisfies CAP availability.”** The definitions and denominators differ.
- **“Serializable means latest.”** Serializability alone does not impose real-time order.
- **“Synchronous replicas imply linearizability.”** authority, ordering, reads, and failover rules matter.
- **“R+W>N proves correctness.”** It proves set intersection in a simplified fixed universe.
- **“Eventual consistency is one model.”** Convergence, causal/session rules, conflicts, and timing vary.
- **“CRDTs preserve business invariants.”** They preserve a data type's merge semantics, not arbitrary cross-object constraints.
- **“Mean latency captures user experience.”** tails, aborts, timeouts, and retries dominate distributed paths.
- **“Timeout is unavailability only.”** It can also hide a committed unknown outcome.
- **“Repair is outside the benchmark.”** Repair consumes resources and changes risk/latency.
- **“No anomaly found proves the claim.”** Finite testing is bounded evidence; a counterexample disproves the tested claim.

## Worked Examples

### Example 1

**Situation.** A partition separates replicas A and B. A acknowledges write `x=1`; afterward a client invokes read at B.

**Reasoning.** B cannot distinguish the completed-write history from one where the write never occurred. Returning 0 is illegal under linearizability in the first history; waiting/rejecting fails CAP availability for that request.

**Conclusion.** The partition creates a consistency-versus-availability choice for this operation.

### Example 2

**Situation.** A three-voter consensus group loses one voter.

**Reasoning.** Two voters still form a majority, so strong reads/writes can progress if routing and leadership recover. Calling every safety-prioritizing design “unavailable under one failure” ignores quorum fault tolerance.

**Conclusion.** Availability depends on topology and remaining authority, not the label “CP.”

### Example 3

**Situation.** In a five-replica fixed quorum store, configuration uses R=3 and W=3.

**Reasoning.** R+W=6>5 and 2W=6>5, so read/write and write/write sets intersect. A configuration R=1,W=3 lacks guaranteed read/write intersection. Neither calculation proves version selection or membership safety.

**Conclusion.** Quorum arithmetic is one premise, not the entire consistency protocol.

### Example 4

**Situation.** Five replica response times are 8, 12, 47, 55, and 90 ms and a three-ack quorum is needed.

**Reasoning.** Ignoring other costs, completion waits for the third-fastest response: 47 ms, not 212 ms and not 12 ms. Persistence, queueing, leader routing, and correlation must be added in real measurement.

**Conclusion.** Quorum latency is an order statistic on the critical path.

### Example 5

**Situation.** A feed read is 240 ms stale under a 200 ms contract.

**Reasoning.** It violates bounded staleness even if data eventually converges and the request returned quickly. A 500 ms contract would accept the same history. The evaluator needs authoritative commit/apply timing, not only replica wall clocks.

**Conclusion.** Freshness is a measurable contract separate from response availability.

### Example 6

**Situation.** Two partitioned regions independently decrement inventory from 1 and later merge by summing deltas.

**Reasoning.** Both local preconditions pass, but merged inventory is -1. Unrestricted acceptance is not invariant-confluent. Allocate regional escrow whose total is at most 1, establish exclusive ownership, or reject when authority cannot be reached.

**Conclusion.** Business invariants determine where coordination is unavoidable.

### Example 7

**Situation.** A database reports 99.99% monthly availability but excludes serialization aborts, client timeouts, and minority-region errors.

**Reasoning.** The number cannot answer the application SLO without denominators. Over a simplified 30-day continuous window, 0.01% is 4.32 minutes, but request-weighted errors and excluded results may tell a different story.

**Conclusion.** Availability percentages require operation populations, windows, latency thresholds, and exclusions.

### Example 8

**Situation.** A benchmark reports 10 ms mean latency for successful single-key reads while 2% of requests time out at 5 seconds.

**Reasoning.** Removing timeouts conditions on success and hides the most important tail. Report the full result distribution, timeout/error/unknown rates, offered load, and retry amplification.

**Conclusion.** Success-only averages can reverse a design decision.

### Example 9

**Situation.** An asynchronous disaster-recovery replica normally lags 100 ms, but after primary-region loss it is missing 12 seconds of acknowledged writes.

**Reasoning.** The service may restore within its RTO yet violate an RPO smaller than 12 seconds. Replica convergence and read consistency do not prove durability across correlated regional loss.

**Conclusion.** Consistency, RPO, and RTO need independent evidence.

### Example 10

**Situation.** During quorum loss, an authorization service offers cached reads and queued revocations.

**Reasoning.** Cached public profile data may be acceptable, but stale authorization can grant access after revocation. Marking revocation “accepted” without enforcement is dangerous. The safe degraded API rejects protected access or uses a locally enforceable short-lived capability policy with explicit risk.

**Conclusion.** Degraded availability must be designed per operation and consequence.

## Cross-Program Connections

- Distributed Systems owns formal consistency, CAP, consensus, causal order, and failure models; Database Engineering maps them to transaction and storage behavior.
- Systems Engineering owns SLOs, failure-domain analysis, recovery objectives, capacity, incident evidence, and degraded operation.
- Data Architecture Engineering owns classification of invariants, geographic ownership, residency, and acceptable staleness by data product.
- API and Service Engineering owns response semantics for committed, rejected, accepted-later, stale, and unknown outcomes.
- Security Engineering owns freshness requirements for authorization/revocation and integrity of test histories and membership.
- Algorithm Engineering owns quorum/set reasoning, dependency graphs, merge algebra, and statistical latency analysis.

## References

1. Seth Gilbert and Nancy Lynch. [Brewer's Conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services](https://groups.csail.mit.edu/tds/papers/Gilbert/Brewer6.pdf). *SIGACT News* 33(2), 2002. Formal CAP models and impossibility argument.
2. Maurice Herlihy and Jeannette Wing. [Linearizability: A Correctness Condition for Concurrent Objects](https://cs.brown.edu/~mph/HerlihyW90/p463-herlihy.pdf). *ACM TOPLAS* 12(3), 1990. History and real-time definition.
3. Eric Brewer. [CAP Twelve Years Later: How the “Rules” Have Changed](https://doi.org/10.1109/MC.2012.37). *Computer* 45(2), 2012. Scope, partitions, and design nuance.
4. Daniel Abadi. [Consistency Tradeoffs in Modern Distributed Database System Design](https://www.cs.umd.edu/~abadi/papers/abadi-pacelc.pdf). *Computer* 45(2), 2012. PACELC framing.
5. Peter Bailis et al. [Highly Available Transactions: Virtues and Limitations](https://www.vldb.org/pvldb/vol7/p181-bailis.pdf). PVLDB 7(3), 2013. Availability definitions and transactional limits.
6. Peter Bailis et al. [Coordination Avoidance in Database Systems](https://www.vldb.org/pvldb/vol8/p185-bailis.pdf). PVLDB 8(3), 2014. Invariant confluence and coordination boundaries.
7. Atul Adya. [Weak Consistency: A Generalized Theory and Optimistic Implementations for Distributed Transactions](https://pmg.csail.mit.edu/papers/adya-phd.pdf). MIT PhD thesis, 1999. Transaction dependency phenomena.
8. Paolo Viotti and Marko Vukolić. [Consistency in Non-Transactional Distributed Storage Systems](https://arxiv.org/abs/1512.00168). *ACM Computing Surveys* 49(1), 2016. Consistency-model taxonomy.
9. Eric Brewer. [Spanner, TrueTime and the CAP Theorem](https://research.google/pubs/spanner-truetime-and-the-cap-theorem/). Google Research, 2017. CAP interpretation and global database example.
10. Peter Bailis et al. [Probabilistically Bounded Staleness for Practical Partial Quorums](https://arxiv.org/abs/1204.6082). PVLDB 5(8), 2012. Quantifying partial-quorum staleness.

## Exercises

### Exercise 1

State the Gilbert–Lynch CAP result precisely enough to explain why “choose two of three” is misleading. Distinguish CAP availability from a 99.99% service SLO.

### Exercise 2

For N=7, compute majority size and evaluate R/W configurations (4,4), (1,4), and (3,5) for read/write and write/write intersection. Explain what the arithmetic does not prove.

### Exercise 3

An evaluation reports p50 of successful requests, kills one process, tests one key for five minutes, and concludes that all transactions are linearizable, highly available, and region-durable. Identify at least ten evidence defects and redesign the evaluation.

### Exercise 4

Compare a linearizable quorum read, a causal/session read, a bounded-stale follower read, and a convergent CRDT read for account balances, product catalogs, authorization state, and shopping carts. Recommend contracts and residual risks.

### Exercise 5

Design an evidence-based consistency/latency/availability decision for a three-region database supporting transfers, inventory, profiles, and analytics. Include definitions, topology, degraded modes, durability, workload/fault matrix, measurements, oracles, and decision records.

## Answers to the Exercises

### Answer 1

In the asynchronous model, an atomic read/write object cannot guarantee that every operation submitted to every non-failing node eventually completes while tolerating arbitrary message loss between components. After a completed write on one partition side, the other side lacks information needed for a later linearizable read. It must return a potentially illegal value or fail to complete successfully. The result concerns a defined partition execution and properties; it does not assign permanent product categories or say a designer can make a real partition disappear by “choosing CA.”

CAP availability is a qualitative liveness property over every request at a non-failing node, without a practical deadline. A 99.99% SLO is a quantitative target over a chosen request population/window, normally with a latency threshold and exclusions. A prompt quorum error can count against SLO success and CAP availability differently depending on definitions; an hours-late success may satisfy eventual termination but fail the SLO. Both contracts must be reported independently.

### Answer 2

For N=7, majority size is 4. With R=4,W=4, R+W=8>7 and 2W=8>7, so read/write and write/write sets intersect. With R=1,W=4, 1+4=5 is not greater than 7, so read/write intersection is not guaranteed; write quorums still intersect because 8>7. With R=3,W=5, 3+5=8>7 and 10>7, so both intersections hold.

These inequalities prove only set overlap in one fixed-membership abstraction. They do not prove the intersecting member returns the newest valid version, that writes are ordered, that concurrent conflicts resolve correctly, that acknowledgements are durable, that membership transitions are safe, or that reads/transactions are linearizable or serializable. The protocol, epochs, version rules, storage, topology, and failure model supply those premises.

### Answer 3

The report omits p95/p99/tails, failed/time-out/unknown requests, offered load, retries, aborts, participant counts, durability configuration, and repair periods. One process kill does not cover partitions, asymmetric delay/loss, leader isolation, disk/power/domain loss, corruption, pauses, clock faults, dependency outages, membership changes, or regional loss. One key establishes no multi-key or transactional property. Five minutes may miss elections, GC, compaction, anti-entropy, backup, and repair. Successful response timing may be incomplete or clock-invalid. No formal history model/checker or business invariant is stated. “Region durable” has no RPO, acknowledgement boundary, or correlated-domain test.

Redesign with exact per-operation consistency and durability contracts, stable-ID complete histories, trustworthy harness timing, transactional dependency/linearizability checkers at their proper scope, and business invariants. Cross read/write mix, key skew, transaction size, regions, concurrency, payload, consistency/durability settings, and open/closed-loop load. Inject every protocol-boundary crash, asymmetric partitions, delay/loss/reorder, client response loss, process pause, disk stall/full/corruption/power loss, clock/lease faults, membership/range/schema changes, dependency failure, and regional loss. Measure complete latency distributions plus abort/error/timeout/unknown, staleness, RPO/RTO, repair load, and post-fault convergence for long enough to exercise background mechanisms. Record versions/configuration and bound conclusions to tested evidence.

### Answer 4

**Account balances** need serializable/strict-serializable transactions for transfers and typically linearizable current reads for decisions; causal or stale reads may be offered only as labeled statements, never authorization to spend. **Product catalogs** often tolerate bounded-stale local reads with version/age, while price/inventory commitment uses strong transactional state. **Authorization/revocation** generally needs current authoritative reads or short, explicitly risk-bounded capabilities; stale availability can become a security violation. **Shopping carts** can often use an observed-remove set or other domain-specific CRDT with causal/session guarantees, provided quantity, deletion, duplicate, and checkout semantics are defined.

A linearizable quorum read pays authority/quorum latency and can stop under partition. A causal/session read preserves dependencies/read-your-writes with routing/tokens but may not show unrelated latest updates. A bounded-stale follower read lowers latency and may remain available but must expose a trustworthy safe version/time and can violate current-decision requirements. A CRDT read converges for its type under delivery assumptions but can expose concurrent states and does not preserve cross-object invariants. Residual risks include quorum loss, session-token loss, exceeded lag bounds, tombstone/merge bugs, and application misuse of weaker results.

### Answer 5

Define strict-serializable, region-durable transfers; nonnegative inventory with either coordinated reservation or bounded regional escrow; causal/read-your-writes profiles with a convergence target; and snapshot-consistent analytics with explicit age. Define CAP/SLO availability separately per operation, plus latency percentiles, RPO/RTO, and unknown-outcome behavior.

Place voting replicas across three independent regions according to regional-failure goals, and document which two-region quorum path determines writes. Place historical followers near analytics. Transfers stop without a safe quorum and recover by stable transaction ID; inventory consumes only local escrow during isolation or rejects; profiles may accept convergent/causal updates if merge semantics are proven; analytics serves the latest safe snapshot and reports its timestamp. Never label queued work committed.

Specify persistence before acknowledgement, backups, corruption response, repair bandwidth, and tested regional RPO/RTO. Cross normal and skewed workloads, transaction fan-out, payload, concurrency, and region with no fault, latency/loss, asymmetric partitions, one node/zone/region failure, storage/clock/dependency faults, repair, membership/range/schema change, and lost client responses. Measure all latency percentiles, throughput/yield, abort/retry/timeout/unknown, staleness, invariant violations, quorum/participant paths, recovery and repair.

Use linearizability and strict-serializability histories at their exact scope, causal/session checks, snapshot/version bounds, conservation/nonnegative inventory invariants, CRDT merge algebra, and restore-versus-acknowledged-history comparison. Preserve versions, configuration, fault timeline, raw histories, checker output, and limitations. The decision record maps each requirement to evidence, rejected alternatives, cost, residual risk, owner, review date, and rollback/migration plan.
