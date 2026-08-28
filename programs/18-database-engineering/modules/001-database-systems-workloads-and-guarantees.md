---
module_id: DBE-001
program: Database Engineering
level: 1
module_number: 1
title: Database Systems, Workloads, and Guarantees
status: complete
last_verified: 2026-08-28
---

# Database Systems, Workloads, and Guarantees

## One-Page Review

### Governing question

How does a database system turn persistent shared data into a service with explicit behavior under concurrency, scale, and failure?

### Essential definitions

- A **database** is an organized collection of persistent data interpreted under a model and schema.
- A **database management system** (DBMS) mediates definition, access, mutation, protection, and recovery of that data.
- A **workload** is a distribution of operations, data, arrival patterns, concurrency, and service objectives—not merely a list of queries.
- A **transaction** is an application-chosen unit whose database effects receive stated atomicity, isolation, and durability behavior.
- A **guarantee** is a precisely scoped property with assumptions, boundary, failure model, and observable outcome.
- A **service-level objective** (SLO) is a measurable target; it is not a logical correctness guarantee.

### Central model, mechanism, or theorem

Treat a database service as a contract:

`model + state + operations + workload + guarantees + failure model + evidence`.

The logical model defines meaning; the engine maps operations through parsing, optimization, execution, concurrency control, storage, logging, and recovery. A useful claim states what clients may observe, under which failures, at which boundary, and how the claim is tested.

### Critical invariants

- Committed data must respect declared integrity constraints.
- Acknowledgement semantics determine what “successful write” means.
- Isolation claims refer to histories, not simply to concurrent threads being safe.
- Durability is scoped to named failures and persistence boundaries.
- Replication, backup, and integrity constraints solve different problems.
- Workload measurements preserve operation mix, data distribution, concurrency, and tail behavior.

### Common failures

Frequent errors are choosing an engine by label, equating replication with backup, treating ACID as one binary feature, benchmarking only averages, assuming a TCP-ready process can serve the required workload, ignoring hot keys and skew, and claiming durability without naming acknowledgement and failure boundaries.

### Compact example

A transfer service debits one account and credits another. Its database contract must define a transaction boundary, prevent negative balances if that is a rule, preserve total value absent fees, specify concurrent-transfer visibility, and state when success is acknowledged. Fast individual updates do not provide these guarantees by themselves.

### Connections

[DBE-002](../ROADMAP.md) introduces the relational model. Workload shape connects to [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md); physical persistence connects to [Operating Systems](../../22-operating-systems/ROADMAP.md); recovery and availability connect to [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md).

## Governing Question

A database is not merely a file format, a server process, or a query language. It is a system that controls shared state while clients issue operations concurrently and components fail. The engineering question is therefore not “Which database is fastest?” but “Which model, mechanisms, and operated evidence satisfy this workload's required guarantees?”

The standard architecture separates logical concerns from physical mechanisms while coordinating query processing, transaction management, storage, and recovery. Hellerstein, Stonebraker, and Hamilton survey these interacting components in [*Architecture of a Database System*](https://dsf.berkeley.edu/papers/fntdb07-architecture.pdf). This chapter establishes their contract surface; later modules open each mechanism.

## Why This Matters

Two services with identical schemas can require different engines or configurations. An order-entry workload may contain short read-write transactions with strict invariants and bursty contention. A reporting workload may scan years of immutable facts and tolerate delayed refresh. Their query text alone does not capture concurrency, freshness, ingest, working set, skew, or recovery objectives.

Guarantee words also hide scope. “Durable” might mean process restart, host loss, zone loss, or regional disaster; it might begin after memory receipt, log flush, replica acknowledgement, or asynchronous backup. “Consistent” might refer to schema constraints, transaction isolation, replica visibility, or application invariants. A defensible design expands the adjective into an observable contract.

## Prerequisites and Retrieval

You should understand finite sets and sequences, basic programs and APIs, persistent versus volatile memory, concurrent requests, and elementary latency statistics. Recall that an invariant is a property intended to hold across allowed state transitions, and that a percentile such as p99 describes a distribution rather than a worst-case bound.

## Learning Objectives

After completing this module, you should be able to:

- distinguish a database, DBMS, database service, and application data model;
- describe the major paths through a database engine;
- characterize a workload beyond the labels OLTP and OLAP;
- separate logical correctness guarantees from performance objectives;
- scope atomicity, consistency, isolation, and durability claims;
- distinguish replication, backup, and recovery;
- identify guarantees that belong to the engine, platform, or application;
- design evidence that can falsify a database-service claim.

## Core Exposition

A database stores representations of facts. A data model defines the structures and operations used to interpret those representations. A schema constrains a particular database. The DBMS supplies controlled access: definition, query, update, transaction coordination, authorization, storage management, and recovery. A database service adds deployment, configuration, identity, monitoring, backup, failover, upgrades, and accountable operators.

The relational model's enduring contribution was to separate logical data from access paths; Codd's original paper argues for data independence and relation-based manipulation ([DOI 10.1145/362384.362685](https://doi.org/10.1145/362384.362685)). That separation does not make physical design irrelevant. It lets indexes, layouts, and algorithms change without redefining every client-visible fact, provided the logical contract is preserved.

A simplified request path is:

1. authenticate and establish session context;
2. parse and validate an operation;
3. derive or select an execution plan;
4. execute operators against cached or stored data;
5. coordinate concurrent reads and writes;
6. record enough history for the promised recovery behavior;
7. return results or acknowledge commit under a stated rule.

The path is not strictly linear. Execution can block, spill, retry, abort, or wait for logging and replication. Background work may flush dirty pages, compact storage, update statistics, or reclaim obsolete versions. Client-visible guarantees emerge from the composition, not one component.

A workload description should include:

- operation mix and transaction boundaries;
- arrival rate, bursts, concurrency, and think time;
- data volume, growth, working set, and retention;
- key and predicate distributions, including skew and correlation;
- read/write sets and contention;
- result sizes and scan selectivity;
- freshness, latency, throughput, and availability objectives;
- failure, maintenance, and recovery scenarios.

TPC-C is an industry benchmark for a multi-transaction order-entry workload, while TPC-H is a decision-support benchmark. Their value lies in defined data, operations, and measurement rules; neither automatically represents a particular application. The [TPC current-specification register](https://www.tpc.org/tpc_documents_current_versions/current_specifications5.asp) listed TPC-C 5.11.0 and TPC-H 3.0.1 when checked on 2026-08-28.

Guarantees fall into different categories. **Integrity** constrains valid states. **Transaction semantics** constrain how groups of operations appear under success, abort, and concurrency. **Durability and recovery** constrain acknowledged effects across failures. **Availability** constrains the ability to serve operations. **Security and privacy** constrain who can observe or change data. **Performance objectives** constrain measured distributions. One mechanism may support several categories, but the claims remain distinct.

## Definitions and Notation

Let database state be `S`, an operation or transaction be `T`, and an allowed transition be `S --T--> S'`. An invariant `P` requires `P(S')` for every committed allowed transition from a state satisfying `P`. This statement does not say how the DBMS enforces `P`; constraints, locking, validation, or application protocols may participate.

- **Atomicity:** the scoped transaction's effects commit together or abort according to the contract.
- **Consistency:** an overloaded word; name the specific invariant or visibility model.
- **Isolation:** constraints on observations produced by interleaved transactions.
- **Durability:** acknowledged committed effects survive a stated class of failures.
- **Recovery point objective (RPO):** targeted maximum data-loss interval.
- **Recovery time objective (RTO):** targeted time to restore the required service.
- **Throughput:** completed work per unit time under a defined workload.
- **Tail latency:** a high percentile of completion latency, with window and sample defined.

## Mechanisms, Invariants, or Proof Structure

To defend a guarantee, connect four layers:

1. **Claim:** what a client may observe.
2. **Assumptions:** valid inputs, topology, clocks, storage, and fault scope.
3. **Mechanism:** constraints, concurrency control, logs, replicas, backups, or protocols.
4. **Evidence:** history analysis, fault injection, restore drill, measurement, or proof.

For a money transfer without fees, define state as account balances and require nonnegative balances plus conservation of total value. The following model checks one atomic state transition. It does not validate any database engine.

<!-- bijux-verify: {"id":"atomic-transfer-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"committed: {'a': 5, 'b': 10} total=15\nrejected: insufficient funds\nunchanged: {'a': 5, 'b': 10} total=15\n","stderr":""}} -->
```python
def transfer(state, source, target, amount):
    if amount <= 0:
        raise ValueError("amount must be positive")
    candidate = state.copy()
    if candidate[source] < amount:
        raise ValueError("insufficient funds")
    before = sum(candidate.values())
    candidate[source] -= amount
    candidate[target] += amount
    assert min(candidate.values()) >= 0
    assert sum(candidate.values()) == before
    return candidate

balances = transfer({"a": 12, "b": 3}, "a", "b", 7)
print(f"committed: {balances} total={sum(balances.values())}")
try:
    balances = transfer(balances, "a", "b", 6)
except ValueError as error:
    print(f"rejected: {error}")
print(f"unchanged: {balances} total={sum(balances.values())}")
```

The next proof obligation is concurrency: every allowed history must preserve the invariant and promised observations. A sequential model and passing unit test cannot establish an isolation level.

## Alternatives and Trade-Offs

**General-purpose versus specialized engines.** A general DBMS reduces system count and integration cost. Specialized engines may fit access patterns better but increase movement, consistency, and operational boundaries.

**Strong guarantees versus coordination cost.** Stronger ordering or synchronous durability can simplify applications but add latency or reduce availability under partitions. Weaker guarantees are acceptable only when application semantics tolerate them explicitly.

**Normalization versus derived read models.** Canonical data reduces contradictory updates; precomputed or denormalized views reduce read work. Derivation freshness and repair become part of the contract.

**Managed service versus self-operation.** A provider can own infrastructure and engine mechanics. The application still owns schema meaning, queries, data quality, access policy, and validation that recovery satisfies business needs.

## Failure Modes and Misconceptions

1. A database is a durable dictionary. False: models, queries, concurrency, and recovery distinguish a DBMS from a file-backed map.
2. ACID means all databases behave identically. False: transaction boundaries, isolation, durability, and failures must be scoped.
3. Consistency has one database meaning. False: integrity and distributed visibility claims differ.
4. Replication is backup. False: replicas can reproduce deletion or corruption.
5. Average latency describes user experience. False: tails and timeout/cancellation policy matter.
6. A benchmark winner is universally fastest. False: results apply to specified data, workload, configuration, and metric.
7. An index only accelerates reads. False: it consumes space and adds write and maintenance work.
8. Commit acknowledgement proves regional disaster recovery. False unless that failure is inside the durability scope.
9. The platform owns every data guarantee. False: application invariants and schema evolution require domain authority.
10. A successful backup proves recoverability. False: restore, integrity, keys, dependencies, and elapsed time must be verified.

## Worked Examples

### Example 1

**Question:** Is a CSV file a database system?

**Reasoning:** It can be a persistent database in the broad sense, but it supplies no DBMS by itself: schema enforcement, concurrency control, query planning, authorization, and recovery must come from other components.

**Conclusion:** Persistent data is necessary but insufficient for a database service.

### Example 2

**Question:** Characterize a checkout workload.

**Reasoning:** Record transaction mix, basket sizes, inventory hot spots, payment latency, concurrent checkouts, retry policy, growth, and oversell tolerance—not just “many writes.”

**Conclusion:** Workload shape includes semantics and distributions.

### Example 3

**Question:** Characterize a monthly finance report.

**Reasoning:** It may scan large historical ranges, aggregate many rows, run at low concurrency, require snapshot coherence, tolerate hours-old data, and have a minutes-scale deadline.

**Conclusion:** Low request rate can still imply demanding throughput and memory behavior.

### Example 4

**Question:** What does a unique email constraint guarantee?

**Reasoning:** It prevents two stored keys considered equal by the chosen comparison semantics. It does not prove address ownership, deliverability, permanence, or global identity.

**Conclusion:** Integrity constraints are precise and narrower than domain truth.

### Example 5

**Question:** Scope “durable after commit.”

**Reasoning:** State whether commit waits for local stable storage, replicas, or neither; name covered failures and the evidence used after process, host, or zone loss.

**Conclusion:** Durability begins at an acknowledgement boundary and ends at a failure boundary.

### Example 6

**Question:** Why are five replicas not five backups?

**Reasoning:** A committed destructive transaction or propagated logical corruption can reach every replica. Historical, separately protected recovery points address a different failure class.

**Conclusion:** Availability copies and recovery history are complementary.

### Example 7

**Question:** Why record p99 alongside throughput?

**Reasoning:** A system can complete many requests while a small but important fraction waits behind locks, I/O, or queueing. The measurement window and offered load must also be stated.

**Conclusion:** One aggregate metric cannot characterize a workload.

### Example 8

**Question:** Who owns “an order total equals its lines plus tax”?

**Reasoning:** The application domain defines the invariant; schema constraints or transactions may enforce parts of it; platform storage cannot invent its tax semantics.

**Conclusion:** Mechanism ownership and semantic authority differ.

### Example 9

**Question:** Is a listening database ready?

**Reasoning:** It may still be replaying logs, lack write authority, have excessive replica lag, or await schema migration. Readiness must correspond to the operation clients require.

**Conclusion:** Process health is weaker than service capability.

### Example 10

**Question:** What would falsify a 15-minute RPO and 60-minute RTO claim?

**Reasoning:** Restore from representative failure boundaries, measure the newest recovered commit and elapsed service restoration, and verify integrity plus dependencies. A 22-minute loss or 75-minute restore falsifies the target.

**Conclusion:** Recovery objectives require restoration evidence, not backup-job success.

## Cross-Program Connections

- **Operating Systems:** filesystems, virtual memory, scheduling, and I/O shape engine mechanisms.
- **Distributed Systems:** replication and coordination define multi-node visibility and failure trade-offs.
- **Data Engineering:** pipelines consume change and produce derived data with freshness contracts.
- **Security Engineering:** authorization, encryption, auditing, and injection resistance protect database boundaries.
- **Reliability Engineering:** SLOs, capacity, backup, restore, and incident evidence turn an engine into a service.

## References

- Avi Silberschatz, Henry F. Korth, and S. Sudarshan. [*Database System Concepts*, 7th ed.](https://www.yale.db-book.com/) McGraw-Hill, 2019, ISBN 9780078022159. Author-maintained edition record checked 2026-08-28.
- Joseph M. Hellerstein, Michael Stonebraker, and James Hamilton. [“Architecture of a Database System.”](https://dsf.berkeley.edu/papers/fntdb07-architecture.pdf) *Foundations and Trends in Databases* 1(2), 2007, pp. 141–259.
- Edgar F. Codd. [“A Relational Model of Data for Large Shared Data Banks.”](https://doi.org/10.1145/362384.362685) *Communications of the ACM* 13(6), 1970, pp. 377–387.
- Transaction Processing Performance Council. [TPC-C 5.11.0 and TPC-H 3.0.1 current specifications](https://www.tpc.org/tpc_documents_current_versions/current_specifications5.asp). Version register checked 2026-08-28.
- Jim Gray and Andreas Reuter. *Transaction Processing: Concepts and Techniques*. Morgan Kaufmann, 1992, ISBN 9781558601901. Bibliographic record checked 2026-08-28.

## Exercises

### Exercise 1

Distinguish database, DBMS, and database service for a local SQLite application and a managed PostgreSQL deployment. Name responsibilities at each boundary.

### Exercise 2

Build a workload profile for a university course-registration opening hour. Include operations, distributions, concurrency, contention, objectives, and failure cases.

### Exercise 3

Formalize the money-transfer state invariant and transition. Explain what the executable example verifies and what concurrency and durability claims remain unverified.

### Exercise 4

Compare synchronous replication, asynchronous replication, and backups for process loss, host loss, accidental deletion, corruption, and regional loss. Avoid claiming guarantees not supplied by the mechanism alone.

### Exercise 5

Design an evidence plan for a medical-record service requiring no acknowledged record loss under single-zone failure, p99 reads below 200 ms at 2,000 requests per second, and recovery within four hours after regional loss.

## Answers to the Exercises

### Answer 1

An SQLite database is the persistent file and interpreted structures; the SQLite library is the embedded DBMS providing SQL, transactions, storage, and recovery within its documented environment. The application owns schema meaning, file placement, access control around the process, backups, and upgrades. In managed PostgreSQL, PostgreSQL remains the DBMS, while the service includes provisioned instances, storage, networking, identity integration, monitoring, backups, maintenance, and provider operations. The customer still owns schema, queries, client transactions, data classification, credentials policy, and proof that provider recovery meets the application requirement.

### Answer 2

Operations include seat lookup, prerequisite and hold checks, enrollment, drop, wait-list mutation, and schedule reads. The opening hour is bursty, with high concurrency and hot required courses; student and course popularity are skewed. Transactions contend on remaining capacity and a student's schedule. Record offered load, arrival curve, read/write mix, class-size distribution, working set, p50/p95/p99 latency, completed enrollments, aborts, and invariant violations. Required invariants include no enrollment beyond the declared policy and no duplicate enrollment. Test process and node loss during commits, retry storms, stale replicas, and downstream notification failure.

### Answer 3

For balances `b(a)≥0`, define `P(b)` as nonnegativity plus a fixed total absent deposits, withdrawals, or fees. A valid transfer of positive `v` from `s` to `t` requires `b(s)≥v` and produces `b'(s)=b(s)-v`, `b'(t)=b(t)+v`, with other balances unchanged. The snippet verifies two sequential transitions, rejection without mutation, nonnegativity, and conservation using unbounded integers. It does not test interleaved histories, isolation, crash recovery, log persistence, replication, or acknowledgement semantics.

### Answer 4

Replication can keep service available after process or host loss if topology, detection, and fencing work. Synchronous acknowledgement can reduce acknowledged-write loss within its replica failure scope; asynchronous replication permits lag. Both can propagate accidental deletion and logical corruption. Backups preserve historical recovery points when protected outside the affected boundary, but do not by themselves provide low failover latency. Regional guarantees require replica or backup placement, independence, keys, networking, promotion or restore procedures, and tested integrity. None of the three alone proves the broad claim “the data is safe.”

### Answer 5

Define acknowledgement to wait for durable copies in independent zones, then inject loss of any one zone during representative writes and reconcile acknowledged transaction identifiers after failover. Drive a production-shaped read/write mix at 2,000 requests per second, including skew and realistic data volume; report errors and latency distribution, not only p99. For regional loss, restore into an isolated region from independently stored recovery material, recover keys and configuration, verify schema and application-level record invariants, reconnect a test client, and measure from incident declaration to required service. Repeat enough times to expose variance. The four-hour objective and no-loss claim pass only within the precisely named failures; external academic or production certification is not implied.
