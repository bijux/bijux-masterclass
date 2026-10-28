---
module_id: DIST-001
program: Distributed Systems Engineering
level: 1
module_number: 1
title: Why Distribution Changes the Problem
status: complete
last_verified: 2026-08-29
---

# Why Distribution Changes the Problem

## One-Page Review

### Governing question

Why does placing computation or state in independently executing processes connected by an imperfect network change what can be observed, guaranteed, recovered, and proved?

### Essential definitions

- A **distributed system** contains independently executing processes that coordinate by communication and lack instantaneous shared knowledge of the whole execution.
- A **process** or **node** has local state and observes local events plus messages it sends or receives; it does not directly observe another process's state.
- A **message** can be delayed, lost, duplicated, reordered, corrupted unless protected below the model, or delivered after a sender has abandoned the operation.
- **Partial failure** means some components or communication paths fail while others continue, so participants can disagree about whether the system is working.
- A **system model** declares timing, communication, process, storage, and adversary assumptions under which an algorithm's claims are evaluated.
- **Safety** means a forbidden outcome never occurs; **liveness** means a desired outcome eventually occurs under stated fairness and failure assumptions.
- **Indistinguishability** means a process has the same local observation in two executions even though the relevant global states differ.
- A **timeout** is a local policy decision based on elapsed time. By itself it cannot distinguish slow response, lost request, lost reply, remote crash, overload, or partition.

### Central model, mechanism, or theorem

Model an execution as local events and message edges rather than one global program trace. For process $p$, decision $D_p$ can depend only on local history $H_p$. If executions $e_1$ and $e_2$ produce the same $H_p$ but require different correct actions, no deterministic local rule can always choose correctly without additional communication, assumptions, stable records, identifiers, coordination, or a weakened contract. This epistemic gap—not merely network latency—is the defining change.

### Critical invariants

Every distributed guarantee names the process, link, timing, storage, membership, and fault model. Local observations are never silently promoted to global facts. Retries preserve effect semantics through identifiers, deduplication, commutativity, transactions, or compensation. Safety and liveness are reviewed separately. Timeouts trigger bounded action but are not failure oracles. Recovery accounts for messages and effects that cross a crash boundary. Evidence includes adversarial schedules, duplication, loss, delay, reordering, restart, partition, version skew, and resource exhaustion appropriate to the claim.

### Common failures

Engineers treat remote calls as slow local calls; infer remote failure from silence; use wall-clock timestamps as universal causal order; retry non-idempotent commands blindly; equate acknowledgement with durable effect; assume exactly-once delivery from a library label; conflate replication with consistency; hide partial success behind one status; test only one message schedule; claim CAP as “pick any two” without the formal conditions; or quote an impossibility result without its model.

### Compact example

A client sends `debit(request_id=R, amount=10)`. The server commits the debit, then the reply is lost. At timeout, the client's local history is identical to an execution in which the request never arrived. Retrying with a fresh identity may debit twice; never retrying may omit the debit. A durable request identity plus atomic record of outcome and replayable status can narrow the ambiguity. The timeout itself cannot.

### Connections

Concurrency contributes interleavings, but distribution removes shared memory and reliable immediate observation. Networking supplies delay, loss, paths, and partitions. Operating systems supply processes, clocks, storage, and crashes. Databases supply transactions and durability. Later modules formalize models, failures, snapshots, time, ordering, delivery, replication, consistency, consensus, transactions, partitioning, and verification.

## Governing Question

What additional assumptions, protocols, and evidence are required when participants make progress from different local histories and communication may fail independently of computation?

The practical answer begins with humility: “I did not receive a response” is a fact about one observer, not a fact about remote execution. The theoretical answer begins with a model: what events exist, which information can reach which process, how long communication may take, what can crash, and what persistence survives.

## Why This Matters

Distribution is justified by independent ownership, geography, scale, fault containment, data locality, or availability—not because remote boundaries are fashionable. Once introduced, it creates latency, concurrency, partial failure, independent deployment, version skew, security boundaries, uncertain ordering, and operational coordination. A modular design can be logically clean yet become less reliable when converted into network calls.

Waldo, Wyant, Wollrath, and Kendall argued that local and distributed interactions cannot share one transparent abstraction because latency, memory access, concurrency, and partial failure differ intrinsically. Lamport showed that causal order is a partial order derived from local sequence and messages, not simply one global wall-clock timeline. Fischer, Lynch, and Paterson showed that deterministic consensus can fail to terminate in a fully asynchronous model with even one possible crash. Each result is conditional and precise; together they reject the illusion of a single reliable machine.

The payoff is not pessimism. Explicit models make strong systems possible. Sequence numbers expose duplicates, durable logs preserve decisions, quorums relate observations, leases add time assumptions, consensus orders commands, transactions couple state changes, reconciliation repairs divergence, and monitoring estimates failure. Their guarantees come from assumptions and mechanisms, never from distribution itself.

## Prerequisites and Retrieval

Retrieve processes, concurrency, state machines, graphs, sets, logical implication, invariants, basic probability, networking delay/loss, and database durability. Distinguish a function call from its externally visible effect. You should be comfortable tracing several possible event orders. No prior consensus or consistency-model knowledge is assumed.

## Learning Objectives

By the end of this module, you should be able to:

1. explain why remote communication is not equivalent to local invocation;
2. describe a distributed execution using local histories, events, and messages;
3. separate local observation, inferred remote state, and established global property;
4. demonstrate timeout and acknowledgement ambiguity with alternative executions;
5. distinguish concurrency, parallelism, and distribution;
6. state safety and liveness claims under explicit system and fault models;
7. identify duplicate, lost, late, reordered, and partially applied effects;
8. use identifiers, durable state, retry protocols, reconciliation, and compensation appropriately; and
9. bound theoretical, executable, and operational evidence without overclaiming correctness or safety.

## Core Exposition

A local program can often rely on one address space, one memory model, language-level calls, and a runtime that reports failure directly. A distributed process instead sends a representation of intent. Serialization, transport, authentication, routing, admission, remote scheduling, code version, storage, reply transport, and local decoding all lie between invocation and observation. Every stage has distinct failure and evidence.

Distribution is not the same as concurrency or parallelism. Concurrent activities overlap logically; parallel activities execute simultaneously; distributed activities execute in independently failing contexts that communicate. A multithreaded process can be concurrent without being distributed. Two sequential services communicating over a network form a distributed interaction. Distribution nearly always introduces concurrency because message arrivals and independent execution interleave.

Represent process $p$'s events as a local sequence $H_p=(e_{p,1},e_{p,2},\ldots)$. A message creates a send event at one process and, if delivered, a receive event at another. Lamport's **happens-before** relation includes local order, send-before-receive, and transitive closure. Concurrent events need not be causally ordered. Physical timestamps can be useful measurements but clock error and lack of causal connection prevent them from serving as automatic truth.

No participant directly reads the global state. It learns through messages whose contents were generated in an earlier local state. By arrival, the sender may have changed, crashed, restarted, or lost leadership. The receiver's view is therefore partial and stale by an unknown amount unless the protocol establishes stronger bounds. A dashboard, registry, cache, or health check is another distributed observer, not omniscience.

Partial failure creates asymmetric belief. Client A can reach server B while C cannot. A leader can contact a minority and believe peers failed while the majority elects another leader. A service can accept work while its reply path is broken. A disk can persist data while the process crashes before acknowledgement. Components that remain healthy must decide whether to wait, retry, degrade, isolate, or stop without perfect failure knowledge.

Silence is ambiguous. In an asynchronous model, there is no fixed upper bound on process speed or message delay. A process that has not answered is indistinguishable locally from a failed process for as long as the delay continues. Timeouts are indispensable engineering controls: they bound resource occupation and let callers choose another action. But they implement suspicion, not knowledge. Chandra and Toueg formalized failure detectors through completeness and accuracy properties, showing how additional or eventual assumptions enable progress.

Requests and effects require separate histories. Consider `create shipment`. The request can be lost before receipt; received then rejected; committed then crash before reply; committed with reply lost; or still executing after the caller's deadline. “At-most-once delivery” does not automatically mean at-most-once effect if identities change or side effects escape the deduplication boundary. “At-least-once” delivery needs effect idempotency or explicit duplicate handling.

A robust retry protocol typically uses a stable operation identifier chosen before the first attempt. The authority stores identifier, request fingerprint, status, and result atomically with the governed effect, or documents the remaining gap. A repeat with the same identifier returns the same committed outcome; a conflicting payload is rejected. Retention must cover the retry horizon. This can provide exactly-once effect inside a bounded authority even though messages remain duplicated or lost. It does not create universal exactly-once behavior across unrelated external effects.

Acknowledgements have levels. “Received in memory,” “accepted into a queue,” “replicated to a quorum,” “durably committed,” “side effect completed,” and “observable to all permitted readers” differ. Name what an acknowledgement proves, which faults it survives, and which downstream work remains. Otherwise producers and consumers attach incompatible semantics to the same `200 OK` or `ack` bit.

Ordering is also scoped. A process has local order. A channel may provide FIFO order per connection while retries use another connection. A broker may order within a partition, not across partitions. A logical clock can extend causal precedence but does not by itself implement mutual exclusion or real-time order. Total order needs an agreed tie-breaking or coordination protocol and has availability and latency consequences.

Snapshots expose the absence of a simultaneous global read. Reading node A and then B can mix states from different logical times and omit or double-count in-flight work. Chandy and Lamport showed how markers and channel assumptions can record a consistent global state without stopping the computation. The lesson here is not the later algorithm detail: system-wide counters, backups, and diagnoses need a defined consistency relation.

Replication multiplies copies and failure paths. It can improve read capacity or survival of some faults, but it creates questions: who accepts writes, how versions order, when acknowledgements occur, what reads may observe, how conflicts resolve, and what happens during partitions. “Three replicas” is inventory, not a consistency or availability contract.

Safety and liveness pull differently under uncertainty. Waiting for more evidence may protect safety but harm liveness. Proceeding with partial information may preserve availability but risk conflicting effects. A protocol must state forbidden states, required progress, and the environmental/failure assumptions under which each holds. Gilbert and Lynch's CAP result is one precise example for atomic consistency and availability under partitions in an asynchronous setting; it is not a product-selection slogan.

FLP is another often-misused result. It does not say consensus systems never work or that one crash always stops them. It says every deterministic consensus protocol in the fully asynchronous crash model has some admissible execution that does not terminate, even with one possible faulty process. Real protocols introduce partial synchrony, randomization, failure detectors, stable leaders, operational intervention, or conditional liveness. Safety can often remain unconditional while progress waits for a favorable period.

Failure models matter. Crash-stop assumes a failed process never returns. Crash-recovery introduces persisted and lost state plus identities across incarnations. Omission covers send/receive loss. Timing failures violate deadlines. Byzantine behavior can be arbitrary or adversarial. Storage can tear, lose acknowledged writes, or corrupt data unless excluded by assumption. A proof against crash-stop faults says nothing about credential compromise or correlated operator error.

The executable model below encodes four possible remote histories that are locally identical at a client timeout. Half contain the requested effect and half do not. It demonstrates indistinguishability; it does not model a real network.

<!-- bijux-verify: {"id":"timeout-indistinguishability-check","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"client_observation=timeout\ntimeout_histories=4\neffect_applied=2\neffect_not_applied=2\ndecision=retry_requires_idempotency_or_status_protocol\n","stderr":""}} -->
```python
histories = [
    {"name": "request_lost", "client": "timeout", "effect": False},
    {"name": "rejected_reply_lost", "client": "timeout", "effect": False},
    {"name": "committed_reply_lost", "client": "timeout", "effect": True},
    {"name": "committed_reply_delayed", "client": "timeout", "effect": True},
]

observations = {history["client"] for history in histories}
assert observations == {"timeout"}
applied = sum(history["effect"] for history in histories)

print("client_observation=timeout")
print(f"timeout_histories={len(histories)}")
print(f"effect_applied={applied}")
print(f"effect_not_applied={len(histories) - applied}")
print("decision=retry_requires_idempotency_or_status_protocol")
```

Execution establishes only that the encoded local observation maps to several encoded global histories. It does not prove message probabilities, network behavior, database atomicity, idempotency, durability, a failure detector, protocol correctness, or fitness for any production or high-stakes decision.

## Definitions and Notation

Let $P=\{p_1,\ldots,p_n\}$ be processes and $M$ messages. An execution $e$ is an interleaving or partial order of local events, sends, receives, failures, recoveries, and external actions allowed by model $\mathcal{M}$. Process $p$'s projection is local history $H_p(e)$. Executions $e_1\sim_p e_2$ are indistinguishable to $p$ when $H_p(e_1)=H_p(e_2)$.

Write $a\rightarrow b$ when event $a$ happens before $b$: local program order, send-before-corresponding-receive, or transitive consequence. If neither $a\rightarrow b$ nor $b\rightarrow a$, the events are concurrent in this relation. The relation captures potential causal influence, not elapsed physical duration.

A safety property is commonly prefix-closed: once violated, a finite bad prefix witnesses the failure. A liveness property states that something good eventually occurs and depends on infinite-execution fairness or progress assumptions. **Fault tolerance** means specified properties continue under a declared set and number of faults; it never means tolerance of every failure.

## Mechanisms, Invariants, or Proof Structure

Use a failure-aware design chain:

1. **Justify the boundary.** State what independent ownership, scale, locality, or resilience distribution provides.
2. **Declare the model.** Processes, links, timing, clocks, membership, storage, authentication, faults, recovery, and adversary.
3. **Define operations and effects.** Authority, identifier, preconditions, commit point, acknowledgement level, visible result, and compensation.
4. **Separate properties.** State safety, liveness, consistency, durability, availability, and bounded-degradation claims independently.
5. **Enumerate ambiguous histories.** Loss before/after effect, lost reply, delay, duplicate, reorder, crash, restart, partition, and concurrent command.
6. **Add protocol evidence.** Durable identities, fencing, deduplication, quorum/consensus, reconciliation, monitoring, or explicit weakened semantics.
7. **Test schedules and faults.** Deterministic models where possible, fault injection, restart, network control, invariant checks, and production observation.
8. **Record claim limits.** Unsupported fault classes, timing assumptions, external effects, retention horizons, operator dependencies, and untested scale.

The **local-knowledge invariant** forbids conclusions not derivable from a participant's history and model assumptions. A timeout can justify abandoning local wait, not declaring remote rollback. A health probe can support suspicion, not proof of process death. A lease can grant temporary authority only under its clock and timing assumptions.

The **stable-identity invariant** requires retries and recovery to refer to the same logical operation and process incarnation where semantics depend on identity. Randomly generating a new request ID on each attempt defeats deduplication. Reusing an old process epoch can let a stale leader issue accepted commands unless fencing rejects it.

The **effect-boundary invariant** requires exactly-once or atomicity claims to name all included effects. A database row and outbox record can be atomic in one transaction; an email, payment network, actuator, and another database are not silently included. Cross-boundary protocols need acknowledgement, reconciliation, compensation, or accepted uncertainty.

## Alternatives and Trade-Offs

**Local composition versus remote separation.** Local calls minimize latency and partial failure and can share transactions. Remote boundaries enable independent ownership, deployment, scaling, technology, geography, and fault containment. Distribute only when those benefits exceed coordination cost.

**Wait versus proceed.** Waiting gathers evidence and can preserve consistency but harms deadlines and availability. Proceeding preserves local progress but can create conflicts or duplicate effects. Tie policy to operation semantics, risk, and recovery.

**Synchronous versus asynchronous replication.** Waiting for replicas improves survival and read guarantees but adds latency and can block during faults. Asynchronous replication reduces foreground latency but permits lag and acknowledged-data loss under some failures.

**Coordination versus convergence.** Consensus or locking serializes decisions under a model. Conflict-free or application-specific merge reduces coordination when operations commute or conflicts are tolerable. Semantic conflicts cannot be wished away by an “eventual” label.

**Transparent RPC versus explicit messaging.** Call-like APIs are familiar but can hide partial outcomes and retry boundaries. Messaging exposes asynchronous lifecycle but adds correlation, state, backpressure, and operational complexity. Either surface must preserve remote semantics.

**Timeouts versus failure detectors.** Fixed timeouts are simple and bound resources but misclassify slow components. Adaptive suspicion improves behavior but remains an inference. Liveness contracts must state eventual timing or detector assumptions.

**Strong global claims versus scoped claims.** Global serial order or atomic cross-system effects are powerful and expensive. Per-key order, session guarantees, bounded staleness, monotonic workflows, or compensatable effects may match needs better. Weaken contracts deliberately, never accidentally.

## Failure Modes and Misconceptions

- **“A remote call is a local call with latency.”** It has serialization, independent execution, partial outcomes, and ambiguous failure.
- **“Timeout means failure.”** It means the observer's wait policy expired.
- **“Retry means reliability.”** A retry can duplicate or reorder effects and amplify overload.
- **“Acknowledged means complete.”** The acknowledgement level and remaining downstream work must be named.
- **“Exactly once is a transport property.”** Useful claims require an effect boundary, identity, durable state, and replay semantics.
- **“Wall clocks give the event order.”** Clock error and causal independence invalidate universal ordering.
- **“Replication makes data consistent.”** It creates copies; a protocol defines consistency and conflict behavior.
- **“Health checks know what is alive.”** They sample reachability and behavior from one observation point.
- **“CAP says pick any two.”** The formal properties and partitioned execution model matter; designs make finer per-operation choices.
- **“FLP says consensus is impossible in practice.”** It is a nontermination result under a precise asynchronous deterministic model.
- **“One green integration test proves a protocol.”** It observes one schedule and fault pattern.
- **“Independent nodes mean independent failures.”** power, networks, software, credentials, operators, and providers create correlated faults.

## Worked Examples

### Example 1

**Question:** A local method throws before returning. Does a remote timeout provide the same information?

**Reasoning:** No. The remote request may be absent, queued, executing, committed, rejected, or replied on a broken path. The caller sees only deadline expiry.

**Conclusion:** Remote failure needs a protocol state, not local-call intuition.

### Example 2

**Question:** Can a monitor prove node B crashed because three probes failed?

**Reasoning:** It establishes three failed observations from the monitor. B may be slow, isolated in one direction, overloaded, paused, or healthy behind a failed path. Suspicion can trigger failover if fencing protects safety.

**Conclusion:** Detection policy and authority transfer must be separated.

### Example 3

**Question:** A request is retried with the same ID but a different amount. What should happen?

**Reasoning:** The authority must bind the ID to a request fingerprint. Returning the old result would hide caller corruption; applying the new payload would break identity. Reject the conflict and investigate.

**Conclusion:** Idempotency identity includes semantic request equality.

### Example 4

**Question:** Two services log events at `10:00:00.100` and `10:00:00.090`. Did the second happen first?

**Reasoning:** Not necessarily. Clock offset, adjustment, precision, capture stage, and causal messages are unknown. Use trace/message relations or bounded-clock evidence appropriate to the claim.

**Conclusion:** Timestamp comparison is conditional evidence, not universal causality.

### Example 5

**Question:** Does three-way replication survive one failure?

**Reasoning:** Only under named faults, placement, acknowledgement, recovery, and corruption assumptions. Three copies in one power domain running the same defective release may fail together.

**Conclusion:** Replica count does not define a fault-tolerance contract.

### Example 6

**Question:** A queue advertises at-least-once delivery. What must the consumer do?

**Reasoning:** Expect duplicates and late delivery, preserve stable message identity, make effects idempotent or deduplicated at their authority, handle poison messages, and define retention and replay horizons.

**Conclusion:** Delivery semantics become application effect obligations.

### Example 7

**Question:** A dashboard totals balances by reading five shards sequentially. Is the total a global state?

**Reasoning:** It combines observations from different logical times while transfers can cross shards. A snapshot protocol, transaction, versioned cut, or explicitly approximate semantics is needed.

**Conclusion:** Aggregation requires a consistency definition for the cut.

### Example 8

**Question:** Why can adding a remote service reduce availability even if it is 99.99% available?

**Reasoning:** A synchronous dependency adds its failures and latency to the caller's critical path. Correlation, fan-out, retry storms, DNS, identity, network, and client limits can further reduce end-to-end success.

**Conclusion:** Component availability percentages do not compose automatically.

### Example 9

**Question:** A medication-order platform coordinates prescriber, pharmacy, allergy, inventory, and administration systems. Can automated protocol tests establish clinical safety?

**Reasoning:** No. Conflicting updates, stale identity/allergy data, duplicate orders, units, substitutions, downtime, human overrides, reconciliation, audit, privacy, and clinical workflow require named prescribing, pharmacy, nursing, patient-safety, informatics, human-factors/accessibility, privacy/legal, security, operations, vendor, regulator, and independent clinical/technical assurance review. No external review is claimed.

**Conclusion:** Distributed correctness evidence is necessary but not clinical authorization.

### Example 10

**Question:** When is distribution justified?

**Reasoning:** When independent ownership, geographic placement, capacity, fault containment, or locality benefits are explicit; operation semantics and model are defensible; partial-failure mechanisms and evidence exist; and simpler local alternatives fail important requirements.

**Conclusion:** Distribution is a costed architectural conclusion, not a default topology.

## Cross-Program Connections

[Concurrency, Parallelism, and Asynchrony](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) supplies schedules, synchronization, safety, and liveness inside shared contexts. [Network Engineering](../../24-network-engineering/ROADMAP.md) supplies reachability, delay, loss, paths, and network failures. [Operating Systems](../../22-operating-systems/ROADMAP.md) supplies process, clock, storage, scheduling, and crash mechanisms.

[Database Engineering](../../18-database-engineering/ROADMAP.md) owns local transactions, storage, recovery, and query guarantees. [Large-Scale Data Systems Engineering](../../21-large-scale-data-systems-engineering/ROADMAP.md) owns partitioned dataflow and storage at scale. [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) turns selected interactions into public contracts but cannot erase distributed execution.

[Security Engineering](../../25-security-engineering/ROADMAP.md) extends crash and omission models with hostile behavior, trust, identity, and compromise. [Systems Engineering](../../26-systems-engineering/ROADMAP.md) connects protocol properties to stakeholder outcomes, multidisciplinary interfaces, hazards, validation, operation, and lifecycle evidence.

## References

- Leslie Lamport, [*Time, Clocks, and the Ordering of Events in a Distributed System*](https://doi.org/10.1145/359545.359563), *Communications of the ACM* 21(7), 1978. Primary happens-before, logical-clock, and distributed-ordering foundation.
- Michael J. Fischer, Nancy A. Lynch, and Michael S. Paterson, [*Impossibility of Distributed Consensus with One Faulty Process*](https://groups.csail.mit.edu/tds/papers/Lynch/jacm85.pdf), *Journal of the ACM* 32(2), 1985. Primary asynchronous deterministic consensus nontermination result.
- K. Mani Chandy and Leslie Lamport, [*Distributed Snapshots: Determining Global States of Distributed Systems*](https://doi.org/10.1145/214451.214456), *ACM Transactions on Computer Systems* 3(1), 1985. Primary consistent-global-state algorithm.
- Tushar Deepak Chandra and Sam Toueg, [*Unreliable Failure Detectors for Reliable Distributed Systems*](https://doi.org/10.1145/226643.226647), *Journal of the ACM* 43(2), 1996. Primary completeness/accuracy failure-detector framework.
- Seth Gilbert and Nancy Lynch, [*Brewer's Conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services*](https://www.cs.princeton.edu/courses/archive/spr22/cos418/papers/cap.pdf), *SIGACT News* 33(2), 2002. Formal consistency, availability, and partition result under stated models.
- Jim Waldo, Geoff Wyant, Ann Wollrath, and Sam Kendall, [*A Note on Distributed Computing*](https://waldo.scholars.harvard.edu/publications/note-distributed-computing), Sun Microsystems Laboratories, 1994. Primary argument against transparent local/remote equivalence.
- Jim Gray, [*Why Do Computers Stop and What Can Be Done About It?*](https://jimgray.azurewebsites.net/jimgraypublications.htm), Tandem Technical Report 85.7, 1985. Operational failure, repair, and availability evidence.
- Nancy A. Lynch, [*Distributed Algorithms*](https://groups.csail.mit.edu/tds/distalgs.html), Morgan Kaufmann, 1996. Graduate-level automata-theoretic algorithms and impossibility framework.

## Exercises

### Exercise 1

Enumerate at least six global histories compatible with a client timing out after sending `reserve(item, request_id)`. For each, state whether the effect occurred and what evidence could distinguish it.

### Exercise 2

Design a retry-safe `create shipment` protocol. Define identity, request fingerprint, authority, atomic state, acknowledgement levels, status lookup, retention, conflicting retries, downstream effects, and recovery limits.

### Exercise 3

Separate safety and liveness for a two-node primary/backup service during a network partition. Explain why a timeout cannot alone enable both nodes to accept conflicting writes safely.

### Exercise 4

Critique: “Our service is CAP compliant because it chooses availability and partition tolerance.” Name the missing definitions, operation scope, consistency contract, failure model, and evidence.

### Exercise 5

A regional emergency-dispatch system replicates incident, unit, location, and hospital-capacity data across two control centers and mobile terminals. Define models, invariants, degraded behavior, tests, reconciliation, and named human-review roles required before operational acceptance.

## Answers to the Exercises

### Answer 1

Compatible histories include request lost before server; request delayed; server receives then rejects and reply is lost; server commits and reply is lost; server commits and reply is delayed; server crashes before commit; server commits durably then crashes before reply; or a proxy accepts while downstream remains pending. Effects are absent in loss-before-receipt, rejection, and crash-before-commit; present after commit; unresolved while delayed/pending. Stable request identity plus authoritative durable status can distinguish committed, rejected, and known-pending states after connectivity returns. Correlated client/server logs, message identifiers, transactional records and downstream reconciliation add evidence. None lets the original timeout prove the global state at that instant.

### Answer 2

The client generates one durable request ID before the first attempt and reuses it with an immutable payload fingerprint. The shipment authority atomically records ID, fingerprint, status and shipment identity with creation. A matching retry returns the stored status/result; a differing fingerprint is rejected. A receipt acknowledgement means only accepted; a committed acknowledgement names durable shipment creation. Status lookup is authorized and returns pending/committed/rejected/unknown with epoch and evidence. Deduplication retention exceeds every retry/replay horizon. Downstream label, carrier and notification effects use an outbox or their own identities and remain outside the local atomic boundary; reconciliation and compensation cover them. Recovery tests crash before/after each durable write and reply. The protocol cannot claim exactly-once effects in downstream authorities without their cooperation.

### Answer 3

Safety can require at most one authority accepts writes for an epoch and no two committed values occupy the same log position. Liveness can require that writes eventually complete while a quorum communicates and timing becomes favorable. During a partition, each node sees only silence from the other; the primary cannot distinguish backup isolation from its own isolation, and the backup cannot distinguish primary crash from delay. Letting both promote on timeout violates single-writer safety. Use quorum/third-party authority, leases with bounded clocks, or fencing and accept that a minority blocks. With only two nodes and no extra assumptions, preserving safety can sacrifice write liveness during partition.

### Answer 4

“CAP compliant” is not a useful property. Define the data object and operations; atomic/linearizable or another consistency semantics; availability as which nonfailed requests receive responses and within what bound; partition as which messages may be lost indefinitely; and synchrony, client, failure and durability assumptions. State choices per operation and state: some reads may serve stale data while writes reject, or ownership may partition by key. Test isolated sides, concurrent operations, recovery, conflict/reconciliation and histories against the consistency checker. Ordinary uptime and replica-count evidence do not establish the theorem's properties.

### Answer 5

Declare centers, terminals, links, clocks, identity, membership, storage, crash/recovery, partition and Byzantine/compromise assumptions. Safety invariants include unique incident/unit identities; authorized command epochs; no unit simultaneously committed to incompatible assignments; preserved priority, provenance and correction history; and no silent loss of acknowledged emergency state. Liveness names conditions for intake, dispatch, acknowledgement, handoff and recovery. Define read/write behavior during center separation, mobile disconnection, stale hospital data, duplicate reports, lost acknowledgements and overload; show uncertainty rather than false freshness. Use durable IDs, fenced authority, replicated logs or carefully scoped ownership, offline queues, idempotent effects, conflict detection, reconciliation and audited manual override. Test deterministic schedules, message loss/delay/duplication/reorder, center/terminal crash, storage fault, clock disturbance, power/provider loss, cyber incident, version skew, failover/restoration, surge and long partition, plus field exercises. Named reviewers include emergency dispatchers and incident command, police/fire/medical services, hospital coordination, public-safety communications, geospatial experts, distributed/network/data engineers, cybersecurity, privacy/legal/records, safety/reliability, human-factors and accessibility, field/mobile operators, training/maintenance, telecom providers, regulators, affected jurisdictions and independent operational/technical assurance. Automated tests cannot validate emergency doctrine, human comprehension, jurisdictional authority, clinical/public-safety outcomes or field readiness; no external acceptance is claimed.
