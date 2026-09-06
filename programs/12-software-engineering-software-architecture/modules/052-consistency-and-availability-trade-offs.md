---
module_id: SARCH-052
program: Software Engineering: Software Architecture
level: 2
module_number: 52
title: Consistency and Availability Trade-Offs
status: complete
last_verified: 2026-09-06
---

# Consistency and Availability Trade-Offs

## One-Page Review

### Governing question

For each operation and business invariant, what may a distributed system return or accept when replicas cannot communicate, and how should architects trade freshness, ordering, latency, availability, convergence, and harm without reducing the decision to a “CP versus AP” label?

### Essential definitions

- **consistency model** constrains the values and operation histories clients may observe;
- **linearizability** makes each completed operation appear atomic at one point between invocation and response while respecting real-time order;
- **sequential consistency** gives one order consistent with each participant's program order but not necessarily real time;
- **causal consistency** preserves the order of causally related operations while permitting concurrent operations to appear in different orders;
- **eventual convergence** means replicas that receive the same updates and no new updates eventually agree; it does not bound staleness or establish invariant safety;
- **session guarantee** constrains one client's observations, including read-your-writes or monotonic reads;
- **partition** is loss or excessive delay of communication between subsets that otherwise continue;
- **CAP availability** requires every request to a non-failing node eventually receive a response; it is not a latency SLO or a promise of business success;
- **quorum** is a required subset of replicas for an operation; intersection is a set property, not by itself a consistency proof;
- **staleness** is distance from an authority's current state, measured by time, versions, operations, or domain meaning;
- **conflict** is concurrent or otherwise incompatible state that cannot be combined by ordinary ordering alone;
- **escrow or rights allocation** partitions permission so local operations preserve a global bound without synchronous coordination.

### Central model, mechanism, or theorem

Under the asynchronous partition model formalized by Gilbert and Lynch, a read/write service cannot guarantee both atomic consistency and availability for every request during a partition. Partition tolerance is the circumstance: when communication is unavailable, an operation must sometimes wait/reject to preserve its consistency contract or return/accept using incomplete knowledge.

For $N$ replicas, any read quorum of size $R$ and write quorum of size $W$ intersect when

$$
R+W>N.
$$

The guaranteed intersection has at least $R+W-N$ replicas. Write/write intersection similarly requires $2W>N$. These conditions support protocols only when versions, failures, membership, concurrent writes, repair, and response rules are correct.

### Critical invariants

- choose consistency and degraded behavior per operation and invariant, not per product slogan;
- define CAP terms precisely and separate them from latency, durability, uptime, and error-rate measures;
- a timeout or failed quorum does not identify the newest value or prove that no write committed;
- reads expose their authority, freshness, version, and session assumptions where decisions depend on them;
- every conflict has a domain-valid detection, prevention, merge, compensation, or human-resolution policy;
- last-write-wins never substitutes clock order for business semantics without explicit acceptance;
- monotonic and read-your-writes guarantees preserve their session identity across routing and failover;
- quorum arithmetic is paired with version and membership protocols and tested under concurrency;
- invariants requiring coordination are either coordinated, redesigned, or safely partitioned by rights;
- asynchronous acceptance is distinguished from durable convergence and final business completion;
- degraded availability states which operations, regions, tenants, and guarantees remain;
- recovery includes anti-entropy, conflict handling, replay, reconciliation, and evidence;
- common dependencies and control planes remain in the availability model;
- tests cover partitions, delay, clock error, membership change, retries, old clients, and restoration.

### Common failures

Common failures include calling a system “AP” because it has replicas; treating CAP availability as five-nines uptime; claiming network partitions force every operation to choose the same policy; using `R+W>N` as a linearizability proof; returning a local denial from stale authorization state; assuming eventual consistency means “within seconds”; ordering financial conflicts by wall-clock timestamp; losing read-your-writes after region failover; accepting inventory sales in two partitions without allocated rights; merging deletions as ordinary values; hiding conflict repair from users; and declaring recovery when replicas match but external effects remain divergent.

### Compact example

Two isolated regions each see one remaining seat. If both accept a reservation, the global capacity invariant is violated; if one waits for authority, that region sacrifices availability for the operation. An alternative preallocates one reservation right to exactly one region. The owning region may accept locally while the other rejects or waits. Rights allocation changes the state model and utilization; it does not make the impossibility disappear.

### Connections

[SARCH-041](041-system-of-record-boundaries.md) supplies authority; [SARCH-044](044-asynchronous-messaging-integration.md) supplies delivery semantics; [SARCH-051](051-partial-failure-as-an-architectural-constraint.md) supplies partition ambiguity and recovery. [SARCH-053](../ROADMAP.md) next examines partitioning and data placement. Distributed Systems Engineering owns formal algorithms and proofs; this module owns architectural contracts and consequences.

## Governing Question

Replicas improve read locality, capacity, and failure tolerance, but they create multiple observations and update paths. When communication is delayed, no participant can distinguish a partition from a slow peer with perfect certainty. An operation must act using incomplete knowledge, delay, or refuse.

The architectural question is not whether the entire system is consistent or available. It is which history each operation promises, which invariant it must preserve, which stale or conflicting result is tolerable, and how the system returns to a trustworthy state.

## Why This Matters

Different operations have different harm. A stale product description may be acceptable; stale revocation may disclose data. A “like” counter can merge concurrent increments; allocating the last intensive-care bed cannot blindly accept both. A customer can often tolerate a pending status but not a double charge.

Overbroad labels conceal this variation. They also hide latency outside partitions: coordinating replicas across continents may preserve a strong order while consuming the user deadline. Good architecture makes the consistency contract visible at API, data, deployment, operational, and product boundaries.

## Prerequisites and Retrieval

Retrieve replica, operation history, invocation, response, happens-before, concurrency, version, quorum, partition, failure detector, invariant, transaction, authority, idempotency, conflict, merge, compensation, convergence, failover, and reconciliation.

From SARCH-011 retrieve availability tactics; SARCH-017 provides interoperability; SARCH-035 and SARCH-044 provide event and message structure; SARCH-041 and SARCH-042 provide data authority; and SARCH-051 provides partial-failure models and ambiguous outcomes.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish linearizable, sequential, causal, convergent, and session guarantees;
2. state the CAP result without conflating availability with an operational SLO;
3. classify consistency needs per operation and invariant;
4. derive read/write quorum intersection conditions and state their limitations;
5. design freshness and session contracts visible to clients and operators;
6. distinguish prevention, deterministic merge, compensation, and manual conflict resolution;
7. use rights allocation to preserve selected invariants during partition;
8. evaluate latency, locality, durability, and availability outside binary labels;
9. plan repair and reconciliation after communication returns;
10. review current system evidence without inferring guarantees from vendor category names.

## Core Exposition

**Begin with histories, not storage brands.** A consistency model constrains a history of invocations and responses. It says what orders or values an observer may see. It does not automatically describe durability, uptime, latency, transaction scope, or correctness of business rules.

Name the object and operation scope. A system can provide linearizable account reservations, causal social conversations, monotonic session reads, and convergent analytics in one product. “The database is eventually consistent” is too coarse to guide behavior.

**Define linearizability precisely.** Each completed operation appears to take effect at one instant between its invocation and response, and if operation A completes before B begins, A precedes B. Concurrent operations may be ordered either way if the object's sequential specification permits it.

Linearizability is compositional across independently linearizable objects, but a business invariant spanning objects still needs an appropriate transaction or protocol. It also does not guarantee progress: an implementation can preserve safety by refusing operations.

**Separate sequential and causal consistency.** Sequential consistency preserves each participant's program order in one global sequence but may reorder operations that are separated in real time. Causal consistency preserves potential influence: a reply cannot appear before the message it answers. Concurrent independent updates may be observed in different orders.

These distinctions affect user experience. A collaboration tool may need causality within a thread without one global order for unrelated threads. A leadership-election view may require real-time-sensitive authority that causal order alone cannot provide.

**Specify session guarantees.** Read-your-writes lets a session observe its accepted updates. Monotonic reads prevent it from moving backward. Monotonic writes preserve its update order; writes-follow-reads ensures later writes reflect the versions already observed.

Session guarantees need a stable session identity and metadata or routing. Device changes, anonymous sessions, cache layers, and region failover can break them. Say how the guarantee transfers, expires, or degrades; “sticky session” is one mechanism, not the contract.

**Treat convergence as a mechanism-dependent promise.** Eventual convergence assumes updates stop and all replicas eventually receive enough information. It does not specify how long, what a read sees before convergence, or whether intermediate states preserve constraints.

State merge algebra matters. Set union is associative, commutative, and idempotent for add-only facts. A delete needs tombstones or causally meaningful removal. Last-write-wins selects an order but can discard intent, and clocks can be wrong.

**State CAP in its model.** During a partition, atomic consistency and availability as defined by the theorem cannot both be guaranteed for every request. A consistency-preserving side may wait or reject because it cannot confirm authority. An availability-preserving side returns or accepts without complete knowledge and therefore may violate atomic visibility.

This is not “choose two of three” for all time. Without a partition, latency and failure still matter. During a partition, different operations can choose differently. The theorem does not select a business policy.

**Separate CAP availability from service availability.** CAP availability is a liveness property: every request delivered to a non-failing node eventually receives a response. An immediate `cannot decide` can satisfy response termination in some interface reasoning yet fail the user's useful-service objective; literature definitions and implementations must be read carefully.

Operational availability asks whether users receive acceptable outcomes within a time bound. Include latency, capacity, dependencies, correctness, and degraded behavior. Never translate an “AP” label into an SLO.

**Map invariants to coordination.** Ask what states must never coexist. Unique username, bounded inventory, account non-negativity, one leader, and mutually exclusive schedule reservations often require shared authority or partitioned rights.

Some operations commute and can merge; others can be redesigned. A globally unique human-readable name can become a non-authoritative display name plus immutable generated identity. Avoiding coordination may change product semantics, so stakeholders must accept the new contract.

**Use escrow and rights allocation.** Partition a bounded resource into non-overlapping rights. A region can spend only its local rights, preserving the global upper bound during disconnection. Rights can be transferred only through a safe protocol.

This trades utilization and fairness for availability. One region can exhaust rights while another has unused capacity. Forecast demand, retain reserve, expose rejection meaning, and reconcile consumption.

**Understand quorum intersection.** With $N$ replicas, any read set of size $R$ intersects any write set of size $W$ when $R+W>N$. Any two write sets intersect when $2W>N$. The minimum read/write overlap is $R+W-N$.

Intersection only ensures a shared replica exists. A protocol must select versions, handle concurrent writes, identify membership epochs, reject stale coordinators, repair replicas, and decide when acknowledgements make a write committed. Sloppy quorums or fallback nodes may not be subsets of the intended replica set.

**Choose latency and failure tolerance consciously.** Larger quorums wait for more replicas and tolerate fewer unavailable replicas for that operation. Smaller local reads reduce latency but may be stale. A leader provides a simple order but leader loss pauses writes until safe authority is restored.

Hedging and fastest-replica reads can bias toward stale versions. Cross-region quorum writes consume network latency. Measure tail latency, not only average, and preserve the stated semantics under timeout.

**Define freshness in domain units.** Time since last refresh is sometimes useful; version lag, number of missing operations, ledger period, market session, or policy epoch may be more meaningful. A value can be one second old and unsafe after revocation, or one day old and safe for a static description.

Expose freshness where clients choose. Do not show a cached balance as current without provenance. Define maximum age, behavior after expiry, and whether a bounded stale read can authorize a write.

**Treat conflicts as domain decisions.** Prevention coordinates before acceptance. Merge combines concurrent state when an algebra and business meaning permit it. Compensation performs a new action after detecting an invalid combined result. Manual resolution assigns accountable judgment.

Do not send every conflict to last-write-wins. A profile color can accept timestamp order; a dosage order or legal approval cannot. Preserve both intents and context when resolution requires a human.

**Separate command and observation consistency.** A stale projection may support browsing, but commands should revalidate critical invariants at their authority. A UI can display approximate inventory while checkout receives an authoritative accept/reject.

Explain this difference to users. Optimistic display must not promise reservation. If stale reads drive automated decisions, their consumers need the same freshness and harm analysis as writes.

**Design asynchronous acceptance honestly.** A local region may durably accept intent during partition and complete later. The response is `accepted locally` or `pending reconciliation`, not globally committed. State what can still reject or compensate.

Queues improve intake availability but not invariant satisfaction. Backlog expiry, schema compatibility, duplicate handling, and recovery authority remain.

**Plan multi-region authority.** Single-leader designs simplify order but make remote writes pay latency and leader partitions pause some paths. Multi-leader designs improve local acceptance but require conflict policy. Leaderless quorums distribute coordination but add repair and version complexity.

Select per data and operation. A multi-region application commonly mixes patterns. Record regional failure domains, shared identity/configuration dependencies, data residency, failover fencing, and operator authority.

**Preserve security and privacy semantics.** Stale allow decisions can violate revocation; stale deny decisions can harm availability. Cache authorization only with explicit subject, resource, action, policy version, expiry, and invalidation rules.

Conflicting privacy deletion and retained replicas need tombstone and completion evidence. Emergency access may be locally available under authenticated bounded authority, but it is a new policy, not silent weakening.

**Design repair as part of normal architecture.** Anti-entropy compares versions or state and transfers missing information. Read repair uses observations during reads. Background repair reduces divergence. None decides domain conflicts automatically.

After a partition, throttle repair to avoid overwhelming recovered links and authorities. Reconcile external effects and user-visible outcomes, not only replica bytes. Preserve evidence of automated and manual resolutions.

**Observe guarantees at their boundary.** Record request and object identity, session metadata, version or causal context, replica/region, quorum members, authority epoch, freshness, conflict, resolution, and terminal outcome without exposing secrets.

Metrics such as replication lag do not prove read-your-writes or invariant safety. Use history checking where appropriate, domain invariant audits, and user-outcome reconciliation. Evidence is bounded to observed operations and model assumptions.

**Test adversarial histories.** Inject one-way partition, asymmetric delay, duplicated and reordered messages, clock jumps, coordinator crash, membership change, leader isolation, slow repair, concurrent update, old client, rollback, and region recovery.

Check stated histories and invariants, not merely response codes. Testing cannot enumerate all schedules; combine systematic model reasoning, protocol verification where warranted, and risk-based experiments.

## Definitions and Notation

Let:

- $H$ be a history of operation invocations and responses;
- $x\prec_{rt}y$ mean operation $x$ completes before $y$ begins in real time;
- $x\rightarrow y$ mean $x$ causally precedes $y$;
- $N$ be the replica count, $R$ required read acknowledgements, and $W$ required write acknowledgements;
- $f_r=N-R$ be the maximum unavailable replicas from which an $R$-response operation can still collect enough replies, ignoring placement and protocol constraints;
- $s$ be staleness under an explicitly named metric;
- **atomic register** mean a read/write object whose operations satisfy linearizability;
- **concurrent updates** mean neither causally precedes the other;
- **tombstone** mean durable removal information used to prevent deleted state from reappearing during merge;
- **authority epoch** mean an ordered term identifying current decision authority.

Quorum counts assume a fixed membership set. Reconfiguration requires a protocol that preserves overlap and authority across epochs.

## Mechanisms, Invariants, or Proof Structure

### Per-operation decision procedure

1. Name the operation, actors, object, authority, and terminal outcomes.
2. State invariants and the harm of stale, rejected, delayed, or conflicting results.
3. Select the required history and session guarantees.
4. State partition behavior: wait, reject, serve stale, accept pending, spend local rights, or delegate emergency authority.
5. Define identity, versions, causal context, freshness, and client-visible status.
6. Choose leader, quorum, merge, escrow, cache, or asynchronous mechanisms.
7. Define conflict detection, resolution, compensation, and manual ownership.
8. Define recovery, repair, throttling, reconciliation, and evidence.
9. Test partitions with concurrency, deployment skew, membership change, and external effects.

### Quorum derivation

Two subsets of an $N$-element replica set with sizes $R$ and $W$ must overlap if $R+W>N$: otherwise disjoint subsets would contain $R+W$ distinct elements, exceeding $N$. Their minimum intersection is $R+W-N$. Replace $R$ with $W$ to obtain write/write condition $2W>N$.

This proves set intersection only. It does not prove that the overlapping replica has the latest committed version, that clocks order writes correctly, or that membership did not change.

### Architectural invariants

- no consistency label without operation, object, history, failure model, and scope;
- no “available” claim without a defined useful response and time boundary;
- no local acceptance presented as global completion;
- no conflict resolution without domain semantics and accountable ownership;
- no failover or reconfiguration without current authority and cross-epoch safety;
- no convergence declaration before replicas and external business effects are reconciled.

## Alternatives and Trade-Offs

| Choice | Preserves | Sacrifices or risks | Typical evidence |
|---|---|---|---|
| single leader | simple total order | remote latency; write pause on authority loss | epoch, commit, failover tests |
| local stale read | low latency and read continuity | freshness and monotonicity | version age and user outcome |
| quorum read/write | set intersection under assumptions | tail latency and reduced failure tolerance | members, versions, repair |
| causal replication | cause-before-effect | no single order for concurrency | causal context and session tests |
| deterministic merge | local acceptance and convergence | only valid for mergeable semantics | algebraic laws and conflict cases |
| last-write-wins | simple deterministic selection | lost intent and clock dependence | clock/ordering limitations |
| escrow rights | invariant-safe local operations | stranded capacity and transfer complexity | rights conservation audit |
| wait or reject | strong invariant protection | operation unavailability | explicit status and recovery |
| accept pending | intake continuity | later rejection or compensation | durable intent and reconciliation |
| manual resolution | contextual judgment | delay, cost, inconsistency | queue ownership and audit |

## Failure Modes and Misconceptions

1. **“CAP says choose two of three.”** Partition is the failure circumstance; the trade-off applies to guarantees during it.
2. **“AP means highly available.”** CAP availability is not an uptime or latency SLO.
3. **“CP means correct.”** Atomic ordering does not establish domain correctness, security, or durability.
4. **“One database has one consistency model.”** guarantees differ by operation, transaction, replica, and configuration.
5. **“Quorum intersection proves linearizability.”** version, commit, membership, concurrency, and recovery protocols remain.
6. **“Eventual means soon.”** no bound follows from eventual convergence.
7. **“Converged means valid.”** replicas can agree on a state violating a business invariant.
8. **“Last timestamp wins preserves the latest intent.”** clocks and business causality can disagree.
9. **“Sticky routing guarantees read-your-writes.”** failover and cache layers can lose the session path.
10. **“All writes require coordination.”** commutative updates or allocated rights may preserve selected invariants locally.
11. **“All operations should make the same choice.”** harm and invariant needs differ.
12. **“A queue makes a write available.”** it may only accept pending intent.
13. **“Stale reads are harmless.”** authorization and automated action can turn staleness into damage.
14. **“Conflict resolution is infrastructure.”** many conflicts encode business policy.
15. **“Replica repair completes recovery.”** external effects and user outcomes may remain inconsistent.
16. **“Partition tests prove the model.”** explored histories and environments remain bounded evidence.

## Worked Examples

### Example 1

**Situation.** Two isolated bank regions each see an account balance of 100 and receive a withdrawal of 80.

**Reasoning.** Accepting both violates non-negativity. A single reachable authority may accept one while the other waits or rejects. Alternatively allocate withdrawal rights totaling at most 100; each region can spend only its share. The latter improves local availability but may strand funds.

**Conclusion.** Invariant-safe availability requires coordination or a redesigned rights model.

### Example 2

**Situation.** A catalog description replica is twelve minutes behind during a partition.

**Reasoning.** If policy permits descriptions up to one hour old, serve it with version and freshness evidence. Price and recall status may have stricter authorities and must not inherit the catalog rule. The page can remain partially useful without pretending every field is current.

**Conclusion.** Consistency and degraded behavior should be chosen per field and operation.

### Example 3

**Situation.** A user changes a shipping address, then region failover shows the old address.

**Reasoning.** Read-your-writes was lost. Carry a session version or causal token to the new region, route to a replica at least that current, wait, or explicitly report pending synchronization. Sticky routing alone fails when the original region is unavailable.

**Conclusion.** Session guarantees require transferable context and explicit failover behavior.

### Example 4

**Situation.** A fixed set has $N=5$, $R=3$, and $W=3$.

**Reasoning.** $R+W=6>5$, so every read and write quorum overlap by at least one replica. Also $2W=6>5$, so writes overlap. A correct protocol still needs version and commit rules, fencing, and repair.

**Conclusion.** The arithmetic establishes intersection, not the full consistency guarantee.

### Example 5

**Situation.** The same set uses $R=2$ and $W=2$.

**Reasoning.** $R+W=4\le5$ and $2W=4\le5$. Disjoint read/write and write/write sets are possible. A read can miss an acknowledged write, and concurrent writes can live on disjoint replicas. Later merge needs domain semantics.

**Conclusion.** Low quorum sizes improve response tolerance while permitting histories stronger contracts forbid.

### Example 6

**Situation.** Two regions sell the last ten tickets while disconnected.

**Reasoning.** Divide ten rights, perhaps six and four. Each accepted sale consumes one local right, so total accepted cannot exceed ten. A region that exhausts rights rejects or waits even if the other has unused rights. Transfer requires safe communication and conservation evidence.

**Conclusion.** Escrow preserves a bounded invariant by trading utilization for local availability.

### Example 7

**Situation.** A reply appears before the comment it answers on another replica.

**Reasoning.** Attach causal context from the parent to the reply. A reader waits for or fetches the parent before showing the reply, while unrelated concurrent threads need no global order. If the parent is deleted, removal semantics must still explain the reply.

**Conclusion.** Causal order can preserve conversational meaning without total ordering.

### Example 8

**Situation.** Privacy deletion races with an offline profile edit and ordinary last-write-wins restores the profile.

**Reasoning.** Deletion is a governed fact, not an empty value. Retain an authorized tombstone or deletion epoch through the offline-update horizon, reject edits based on older context, and audit every replica and derivative. Wall-clock order alone is unsafe.

**Conclusion.** Conflict semantics must preserve authoritative removal intent.

### Example 9

**Situation.** A hospital loses central policy connectivity during urgent care.

**Reasoning.** Stale blanket authorization must not silently permit all access. Predefine authenticated break-glass roles, limited records and actions, expiry, local audit, patient-safety rationale, and later review. Ordinary administrative changes wait or fail closed.

**Conclusion.** Degraded availability can be safe only as an explicit scoped policy.

### Example 10

**Situation.** A commerce platform uses linearizable inventory reservations, causal order history, stale catalog reads, and convergent analytics.

**Reasoning.** Each contract follows harm: inventory protects a bound; customer history preserves cause and response; descriptions favor locality; aggregates tolerate delay. APIs expose pending and freshness states, and recovery reconciles money and orders before analytics.

**Conclusion.** A coherent architecture commonly combines consistency models by operation.

## Cross-Program Connections

- **Distributed Systems Engineering:** owns formal consistency models, consensus, quorum protocols, CRDTs, and impossibility results in depth.
- **Database Engineering:** owns isolation, replication, transactions, MVCC, recovery, and database-specific guarantees.
- **API and Service Engineering:** exposes freshness, idempotency, pending state, conflict, and session contracts to clients.
- **Data Architecture Engineering:** owns cross-system authority, lineage, governance, deletion, and reconciliation.
- **Security Engineering:** owns revocation, emergency access, integrity, privacy deletion, and adversarial partitions.
- **Platform Engineering:** supplies placement, routing, failure domains, membership, configuration, and observable versions.
- **Software Delivery and Reliability Engineering:** owns SLOs, incidents, failover, repair operation, and evidence collection.
- **Systems Engineering:** connects consistency choices to physical process, people, and safety consequences.

## References

1. Seth Gilbert and Nancy Lynch, “Brewer's Conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services,” *SIGACT News* 33(2), 2002. <https://doi.org/10.1145/564585.564601>
2. Eric Brewer, “CAP Twelve Years Later: How the ‘Rules’ Have Changed,” *Computer* 45(2), 2012. <https://doi.org/10.1109/MC.2012.37>
3. Maurice P. Herlihy and Jeannette M. Wing, “Linearizability: A Correctness Condition for Concurrent Objects,” *ACM TOPLAS* 12(3), 1990. <https://doi.org/10.1145/78969.78972>
4. Leslie Lamport, “Time, Clocks, and the Ordering of Events in a Distributed System,” *Communications of the ACM* 21(7), 1978. <https://doi.org/10.1145/359545.359563>
5. Douglas B. Terry et al., “Session Guarantees for Weakly Consistent Replicated Data,” *PDIS 1994*. <https://doi.org/10.1109/PDIS.1994.331722>
6. Peter Bailis et al., “Highly Available Transactions: Virtues and Limitations,” *PVLDB* 7(3), 2013. <https://www.vldb.org/pvldb/vol7/p181-bailis.pdf>
7. Werner Vogels, “Eventually Consistent,” *Communications of the ACM* 52(1), 2009. <https://doi.org/10.1145/1435417.1435432>
8. Martin Kleppmann, *Designing Data-Intensive Applications*, O'Reilly Media, 2017.

## Exercises

### Exercise 1

Define consistency model, linearizability, sequential consistency, causal consistency, eventual convergence, read-your-writes, monotonic reads, partition, CAP availability, quorum, staleness, conflict, tombstone, and escrow rights.

### Exercise 2

For fixed membership $N=7$, analyze $(R,W)=(3,5)$, $(4,4)$, and $(2,3)$. Compute minimum read/write and write/write intersections, and the simple unavailable-replica tolerance for collecting each quorum. State what the arithmetic cannot prove.

### Exercise 3

Diagnose a globally replicated account system that accepts withdrawals in every partition, uses wall-clock last-write-wins, advertises “strong eventual consistency,” and repairs bytes after reconnection without financial reconciliation. Provide a safe set of alternatives.

### Exercise 4

Compare single-leader, quorum, causal multi-leader, deterministic merge, and escrow designs for usernames, shopping-cart additions, inventory reservation, access revocation, and analytics. Choose per operation and explain partition, latency, conflict, and recovery behavior.

### Exercise 5

Design consistency and availability contracts for an intermittently connected international vaccine-distribution system spanning national depots, clinics, shipment devices, recall authorities, inventory, appointments, and adverse-event reporting. Cover invariants, freshness, rights, sessions, privacy, conflict, partitions, degraded operation, repair, evidence, and manual authority.

## Answers to the Exercises

### Answer 1

A **consistency model** constrains observable histories. **Linearizability** gives atomic operations respecting real time; **sequential consistency** gives one program-order-respecting sequence without real-time order; **causal consistency** preserves cause before effect. **Eventual convergence** makes replicas agree after updates stop and delivery completes. **Read-your-writes** exposes a session's accepted writes; **monotonic reads** prevent that session moving backward. A **partition** prevents timely communication between active subsets. **CAP availability** requires responses from non-failing nodes under the model, not an SLO. A **quorum** is a required replica subset. **Staleness** is distance from authoritative current state. A **conflict** is incompatible concurrent state. A **tombstone** preserves removal knowledge. **Escrow rights** partition permission so bounded local actions conserve a global invariant.

### Answer 2

For $(3,5)$, read/write overlap is at least $3+5-7=1$ and write/write overlap at least $10-7=3$; a read can collect with four unavailable and a write with two. For $(4,4)$, both minimum overlaps are one; each can collect with three unavailable. For $(2,3)$, $2+3-7<0$ and $2(3)-7<0$, so zero overlap is guaranteed; reads tolerate five unavailable and writes four, ignoring placement. Counts do not prove latest-version selection, commit rules, linearizability, durability, correct membership, protection from stale coordinators, latency, or domain invariants.

### Answer 3

The system cannot both accept every withdrawal under partition and preserve global non-negativity without a redesigned constraint. Options are a single or safely elected account authority that makes one side wait; quorum or consensus-backed reservation under explicit failure assumptions; or escrow withdrawal rights whose total never exceeds balance. Wall-clock last-write-wins can lose one withdrawal and does not repair money. Preserve immutable transaction identities and causal or authority epochs, reject stale writers, and reconcile ledger entries and external cash effects after recovery. “Strong eventual consistency” describes convergence properties only if the merge algebra satisfies them; it does not legalize invalid intermediate balances. Expose pending or unavailable outcomes honestly, audit rights and conflicts, and require authorized repair.

### Answer 4

Usernames requiring immediate uniqueness fit one leader or coordinated reservation; alternatively relax uniqueness by generated identity. Shopping-cart additions can use causal or deterministic set/multiset merge if quantity and removal semantics are explicitly designed. Inventory reservation needs leader/quorum coordination or conserved escrow rights. Access revocation favors an authoritative strongly ordered policy epoch, bounded caches, and fail-closed or explicit emergency behavior. Analytics can accept convergent asynchronous updates with recorded lag. Single leader pays remote latency and pauses on unsafe failover; quorums pay tail latency and protocol complexity; causal multi-leader preserves related order but exposes concurrent conflict; deterministic merge works only for valid algebra; escrow trades utilization for local invariant-safe acceptance. Every choice needs repair and domain-outcome reconciliation.

### Answer 5

The global recall authority owns recall identity, affected lot, effective time, supersession, and severity. Inventory ownership is partitioned by depot and clinic with shipment transfer records; dose allocation uses conserved rights so offline clinics cannot collectively administer more tracked stock than assigned. Appointment display may be bounded stale, but administration checks local authoritative stock, lot recall epoch, patient identity, dose interval, and clinician authority. A patient session carries accepted appointment and vaccination versions across reconnect; it never authorizes another patient.

Recall and safety updates use authenticated monotonic epochs, tombstones, expiry, and urgent channels. A disconnected clinic enters visible degraded mode: locally cached current-enough policy, allocated stock rights, bounded appointments, and authenticated manual clinical authority; expired critical policy blocks ordinary administration unless an explicit public-health emergency rule applies. Concurrent demographic edits may merge field-by-field under ownership, while conflicting dose administrations and recalls require reconciliation rather than timestamps. Privacy deletion propagates authoritative tombstones while regulated clinical facts follow retention law.

On reconnection, exchange causal/version context, deduplicate shipment and administration identities, conserve rights, repair replicas gradually, and reconcile physical stock, administered doses, appointments, recalls, and adverse-event reports. Do not equate message delivery with patient safety. Evidence records artifact and policy epochs, data versions, freshness, rights transfers, session context, conflicts, manual decisions, physical counts, and resolutions without exposing unnecessary health data. National and clinic authorities own named queues and escalation. Tests cover one-way partition, clock error, old devices, duplicate shipment, recall during administration, exhausted rights, lost clinic, and restoration from backup.
