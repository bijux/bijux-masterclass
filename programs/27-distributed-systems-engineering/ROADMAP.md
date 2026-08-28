# 27. Distributed Systems Engineering

**Program code:** `DIST`

**Purpose:** Develop rigorous command of computation across unreliable, concurrent machines, including time, ordering, replication, consistency, consensus, transactions, partitioning, and fault tolerance.

**Level-II professional outcome:** Ready to design, implement, test, and operate distributed services, coordination systems, replicated storage, event systems, and geo-distributed platforms.

**Prerequisites:** algorithms; networking; concurrency; databases and operating systems basics.

**Primary ownership:** distributed models and failure; time and ordering; communication semantics; replication; consistency models; consensus; distributed transactions; partitioning and coordination; CRDTs and Byzantine resilience; distributed-system testing and operations.

**Explicit exclusions:** large-scale data engine specifics (Program 21); database internals (Program 18); network protocol engineering (Program 24); API design (Program 28).

## Level I — Undergraduate Core

Modules 001–050 establish the complete foundational model and canonical mechanisms.

### Block 01 — Distributed Models and Partial Failure

| Module | Canonical chapter | Future file |
|---:|---|---|
| 001 | **Why Distribution Changes the Problem** | `001-why-distribution-changes-the-problem.md` |
| 002 | **Processes, Nodes, Links, and Executions** | `002-processes-nodes-links-and-executions.md` |
| 003 | **Synchronous, Asynchronous, and Partially Synchronous Models** | `003-synchronous-asynchronous-and-partially-synchronous-models.md` |
| 004 | **Crash, Omission, Timing, and Byzantine Failures** | `004-crash-omission-timing-and-byzantine-failures.md` |
| 005 | **Network Partitions** | `005-network-partitions.md` |
| 006 | **Failure Detection** | `006-failure-detection.md` |
| 007 | **Distributed Snapshots and Consistent Cuts** | `007-distributed-snapshots-and-consistent-cuts.md` |
| 008 | **Idempotency and Duplicate Effects** | `008-idempotency-and-duplicate-effects.md` |
| 009 | **Safety and Liveness in Distributed Protocols** | `009-safety-and-liveness-in-distributed-protocols.md` |
| 010 | **Writing Explicit Assumptions for a Distributed Design** | `010-writing-explicit-assumptions-for-a-distributed-design.md` |

### Block 02 — Time, Ordering, and Causality

| Module | Canonical chapter | Future file |
|---:|---|---|
| 011 | **Physical Clocks and Drift** | `011-physical-clocks-and-drift.md` |
| 012 | **Clock Synchronization** | `012-clock-synchronization.md` |
| 013 | **Monotonic and Wall Clocks** | `013-monotonic-and-wall-clocks.md` |
| 014 | **Lamport Logical Clocks** | `014-lamport-logical-clocks.md` |
| 015 | **Vector Clocks** | `015-vector-clocks.md` |
| 016 | **Happens-Before and Causal Order** | `016-happens-before-and-causal-order.md` |
| 017 | **Total Order and Partial Order** | `017-total-order-and-partial-order.md` |
| 018 | **Hybrid Logical Clocks** | `018-hybrid-logical-clocks.md` |
| 019 | **Version Vectors** | `019-version-vectors.md` |
| 020 | **Diagnosing an Ordering Bug from an Event History** | `020-diagnosing-an-ordering-bug-from-an-event-history.md` |

### Block 03 — Communication and Messaging Semantics

| Module | Canonical chapter | Future file |
|---:|---|---|
| 021 | **Request-Response Communication** | `021-request-response-communication.md` |
| 022 | **Remote Procedure Calls** | `022-remote-procedure-calls.md` |
| 023 | **Message Queues** | `023-message-queues.md` |
| 024 | **Distributed Logs** | `024-distributed-logs.md` |
| 025 | **Message Delivery Semantics** | `025-message-delivery-semantics.md` |
| 026 | **Exactly-Once Effects and Their Boundaries** | `026-exactly-once-effects-and-their-boundaries.md` |
| 027 | **Timeouts, Retries, and Backoff** | `027-timeouts-retries-and-backoff.md` |
| 028 | **Request Deduplication** | `028-request-deduplication.md` |
| 029 | **Backpressure and Flow Control** | `029-backpressure-and-flow-control.md` |
| 030 | **Designing a Failure-Aware Communication Protocol** | `030-designing-a-failure-aware-communication-protocol.md` |

### Block 04 — Replication Fundamentals

| Module | Canonical chapter | Future file |
|---:|---|---|
| 031 | **Replication Goals and Costs** | `031-replication-goals-and-costs.md` |
| 032 | **Single-Leader Replication** | `032-single-leader-replication.md` |
| 033 | **Leader Election and Terms** | `033-leader-election-and-terms.md` |
| 034 | **Synchronous and Asynchronous Followers** | `034-synchronous-and-asynchronous-followers.md` |
| 035 | **Replication Lag** | `035-replication-lag.md` |
| 036 | **Multi-Leader Replication** | `036-multi-leader-replication.md` |
| 037 | **Leaderless Replication** | `037-leaderless-replication.md` |
| 038 | **Quorum Reads and Writes** | `038-quorum-reads-and-writes.md` |
| 039 | **Read Repair and Anti-Entropy** | `039-read-repair-and-anti-entropy.md` |
| 040 | **Selecting a Replication Model from Workload and Failure Requirements** | `040-selecting-a-replication-model-from-workload-and-failure-requirements.md` |

### Block 05 — Consistency Models

| Module | Canonical chapter | Future file |
|---:|---|---|
| 041 | **Linearizability** | `041-linearizability.md` |
| 042 | **Sequential Consistency for Replicated Operations** | `042-sequential-consistency-for-replicated-operations.md` |
| 043 | **Serializability** | `043-serializability.md` |
| 044 | **Snapshot Isolation** | `044-snapshot-isolation.md` |
| 045 | **Causal Consistency** | `045-causal-consistency.md` |
| 046 | **Eventual Consistency** | `046-eventual-consistency.md` |
| 047 | **Read-Your-Writes and Monotonic Reads** | `047-read-your-writes-and-monotonic-reads.md` |
| 048 | **Session Guarantees** | `048-session-guarantees.md` |
| 049 | **CAP and PACELC** | `049-cap-and-pacelc.md` |
| 050 | **Stating a Service's Consistency Contract Precisely** | `050-stating-a-service-s-consistency-contract-precisely.md` |

## Level II — Graduate and Professional Depth

Modules 051–100 add internals, difficult cases, production constraints, advanced theory, and independent technical judgment.

### Block 06 — Consensus and Replicated Logs

| Module | Canonical chapter | Future file |
|---:|---|---|
| 051 | **The Consensus Problem** | `051-the-consensus-problem.md` |
| 052 | **Quorums and Majority Intersection** | `052-quorums-and-majority-intersection.md` |
| 053 | **Paxos Roles and Safety** | `053-paxos-roles-and-safety.md` |
| 054 | **Multi-Paxos** | `054-multi-paxos.md` |
| 055 | **Raft Leader Election** | `055-raft-leader-election.md` |
| 056 | **Raft Log Replication** | `056-raft-log-replication.md` |
| 057 | **Membership Change** | `057-membership-change.md` |
| 058 | **Log Compaction and Snapshots** | `058-log-compaction-and-snapshots.md` |
| 059 | **Consensus Under Slow and Failed Nodes** | `059-consensus-under-slow-and-failed-nodes.md` |
| 060 | **Implementing and Testing a Replicated State Machine** | `060-implementing-and-testing-a-replicated-state-machine.md` |

### Block 07 — Distributed Transactions and Coordination

| Module | Canonical chapter | Future file |
|---:|---|---|
| 061 | **Atomic Commit** | `061-atomic-commit.md` |
| 062 | **Two-Phase Commit** | `062-two-phase-commit.md` |
| 063 | **Coordinator Failure and Recovery** | `063-coordinator-failure-and-recovery.md` |
| 064 | **Three-Phase Commit Limits** | `064-three-phase-commit-limits.md` |
| 065 | **Distributed Locking** | `065-distributed-locking.md` |
| 066 | **Leases and Fencing Tokens** | `066-leases-and-fencing-tokens.md` |
| 067 | **Sagas** | `067-sagas.md` |
| 068 | **Transactional Messaging and Outbox Patterns** | `068-transactional-messaging-and-outbox-patterns.md` |
| 069 | **Distributed Deadlock** | `069-distributed-deadlock.md` |
| 070 | **Choosing Between Atomicity, Compensation, and Redesign** | `070-choosing-between-atomicity-compensation-and-redesign.md` |

### Block 08 — Partitioning, Placement, and Distributed Storage

| Module | Canonical chapter | Future file |
|---:|---|---|
| 071 | **Hash and Range Partitioning** | `071-hash-and-range-partitioning.md` |
| 072 | **Consistent Hashing** | `072-consistent-hashing.md` |
| 073 | **Rebalancing** | `073-rebalancing.md` |
| 074 | **Hot Partitions** | `074-hot-partitions.md` |
| 075 | **Replica Placement** | `075-replica-placement.md` |
| 076 | **Distributed Hash-Table Protocols** | `076-distributed-hash-table-protocols.md` |
| 077 | **Distributed B-Trees and Ordered Stores** | `077-distributed-b-trees-and-ordered-stores.md` |
| 078 | **Metadata and Directory Services** | `078-metadata-and-directory-services.md` |
| 079 | **Erasure Coding** | `079-erasure-coding.md` |
| 080 | **Designing Placement for Locality, Durability, and Scale** | `080-designing-placement-for-locality-durability-and-scale.md` |

### Block 09 — Convergence, Byzantine Faults, and Advanced Models

| Module | Canonical chapter | Future file |
|---:|---|---|
| 081 | **Conflict Resolution** | `081-conflict-resolution.md` |
| 082 | **Last-Writer-Wins and Its Limits** | `082-last-writer-wins-and-its-limits.md` |
| 083 | **Operation-Based CRDTs** | `083-operation-based-crdts.md` |
| 084 | **State-Based CRDTs** | `084-state-based-crdts.md` |
| 085 | **Causal Broadcast** | `085-causal-broadcast.md` |
| 086 | **Gossip Protocols** | `086-gossip-protocols.md` |
| 087 | **Byzantine Agreement Foundations** | `087-byzantine-agreement-foundations.md` |
| 088 | **Practical Byzantine Fault Tolerance** | `088-practical-byzantine-fault-tolerance.md` |
| 089 | **Trusted Hardware and Hybrid Fault Models** | `089-trusted-hardware-and-hybrid-fault-models.md` |
| 090 | **Choosing a Convergence or Agreement Mechanism** | `090-choosing-a-convergence-or-agreement-mechanism.md` |

### Block 10 — Geo-Distribution, Testing, and Production Judgment

| Module | Canonical chapter | Future file |
|---:|---|---|
| 091 | **Geo-Replication and Latency** | `091-geo-replication-and-latency.md` |
| 092 | **Global Ordering and TrueTime-Style Approaches** | `092-global-ordering-and-truetime-style-approaches.md` |
| 093 | **Data Sovereignty and Placement** | `093-data-sovereignty-and-placement.md` |
| 094 | **Consistency During Multi-Region Failover** | `094-consistency-during-multi-region-failover.md` |
| 095 | **Jepsen-Style History Checking** | `095-jepsen-style-history-checking.md` |
| 096 | **Deterministic Simulation** | `096-deterministic-simulation.md` |
| 097 | **Fault Injection and Network Nemeses** | `097-fault-injection-and-network-nemeses.md` |
| 098 | **Distributed Tracing and Causal Diagnosis** | `098-distributed-tracing-and-causal-diagnosis.md` |
| 099 | **Capacity and Overload in Distributed Services** | `099-capacity-and-overload-in-distributed-services.md` |
| 100 | **Conducting an Adversarial Distributed-System Design Review** | `100-conducting-an-adversarial-distributed-system-design-review.md` |

## Completion standard

This program is complete only when all 100 future module files satisfy `MODULE_CONTENT_CONTRACT.md`. The roadmap itself is not course completion.
