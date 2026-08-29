---
module_id: DIST-002
program: Distributed Systems Engineering
level: 1
module_number: 2
title: Processes, Nodes, Links, and Executions
status: complete
last_verified: 2026-08-29
---

# Processes, Nodes, Links, and Executions

## One-Page Review

### Governing question

How can we describe a distributed system precisely enough to distinguish algorithmic state, deployment failure domains, communication behavior, possible executions, and the limited observations available to each participant?

### Essential definitions

- A **process** is a modeled sequential agent or state machine with local state and enabled actions; it is not necessarily an operating-system process.
- A **node** is a deployment or failure container that hosts one or more process incarnations, such as a machine, virtual machine, device, or isolated runtime under the declared model.
- An **incarnation** is one lifetime of a process or node identity. Restarted state must not be silently confused with its predecessor.
- A **link** or **channel** is a directed communication abstraction between endpoints. Its state and delivery properties belong to the model; a link is not automatically a physical cable, TCP connection, or reliable queue.
- A **configuration** is a modeled global state: the tuple of all process-local states, link/channel states, relevant environment state, and persistent state.
- An **action** is one atomic transition at the chosen abstraction level, such as an internal step, input, send, receive, crash, recovery, or environment event.
- An **execution** is an alternating sequence of configurations and actions in which every action is enabled and each transition obeys the system relation.
- A **schedule** is the action sequence selected from an execution; a **trace** is a projection that hides selected internal state or actions.
- A **local history** is one process's projection of an execution. Different global executions can yield the same local history.
- An **admissible execution** satisfies the model's declared timing, delivery, failure, fairness, environment, and adversary constraints.

### Central model, mechanism, or theorem

Let \(P\) be processes, \(L \subseteq P \times P\) directed links, and

\[
C = \left(\prod_{p\in P} S_p\right) \times
    \left(\prod_{\ell\in L} Q_\ell\right) \times E
\]

be a configuration composed of local states \(S_p\), channel states \(Q_\ell\), and modeled environment state \(E\). A transition relation \(C \xrightarrow{a} C'\) defines enabled actions and their effects. An execution is

\[
C_0, a_1, C_1, a_2, C_2,\ldots
\]

with \(C_{i-1}\xrightarrow{a_i}C_i\) for every step. Correctness quantifies over all admissible executions, not one observed schedule. A participant decides from its local-history projection, not from the unobservable global configuration.

### Critical invariants

- Process identity, node placement, endpoint identity, and incarnation are separate and explicit.
- Every action has one declared abstraction boundary and one state transition.
- A receive of message identity \(m\) requires an allowed prior creation/send; the link contract decides loss, duplication, ordering, corruption, and delivery.
- Local-state transitions follow the process automaton; channel transitions follow the link automaton.
- A log or trace is an observation with a capture boundary, not automatically the authoritative global execution.
- Proofs range over all reachable configurations and admissible schedules relevant to the claim.
- Fairness and reliable-delivery assumptions never appear only inside an informal phrase such as “eventually.”

### Common failures

Teams equate a process with a machine; use an address as eternal identity; restart with stale authority; model a bidirectional network as one link; assume send means receive; assume TCP preserves application messages; omit messages in flight from global state; use one timestamp-sorted log as the execution; test only one scheduler; hide the environment; add fairness only when a liveness proof gets stuck; or prove an abstraction whose atomic actions cannot be implemented at the claimed boundary.

### Compact example

Client process \(c\) sends request `r7` over directed link \((c,w)\). The link duplicates it. Worker \(w\) applies the request once, records its identity durably, and replays the same acknowledgement for the duplicate. The execution has two receive actions but one effect. A client history ending before either acknowledgement is compatible with several global configurations: both copies queued, one applied with replies delayed, or link loss under a lossy model. The local history alone does not choose among them.

### Connections

[DIST-001](001-why-distribution-changes-the-problem.md) established local knowledge and partial failure. Later modules strengthen the base model with synchrony, fault classes, partitions, failure detectors, snapshots, ordering, and protocol properties. Operating systems explain runtime processes; networking explains packet transport; formal methods explain transition systems; deployment engineering explains real failure domains. None can replace an explicit distributed model.

## Governing Question

What precisely exists in the model, what can change in one step, which executions are permitted, and which portion of an execution can each participant or observer actually know?

Distributed reasoning goes wrong when deployment nouns substitute for semantic definitions. “Node A sent to node B” might mean a thread wrote to a library buffer, a process handed bytes to a kernel, a proxy accepted a request, or an application handler consumed it. Each interpretation creates a different transition and different evidence. The model must choose before the proof, test, or incident analysis begins.

## Why This Matters

An algorithm denotes possible behaviors under a declared environment. If a diagram omits channel contents, restart generations, external inputs, or schedules, different executions can look identical. If a proof assumes a FIFO reliable channel while production reconnects and retries, proof and deployment describe different systems.

Precise modeling exposes whether “exactly once” refers to receives or effects, whether a leader is a role or host, whether restart retains deduplication state, and whether progress depends on scheduler or network cooperation. The model need not reproduce every instruction or packet; it preserves distinctions capable of changing the claim. Treating a database transaction as one action is sound only when its atomicity is an explicit substrate assumption and the property does not inspect its recovery internals.

## Prerequisites and Retrieval

Retrieve sets, functions, tuples, sequences, relations, state machines, induction over execution prefixes, queues and multisets, process scheduling, network endpoints, persistent versus volatile state, and the local-knowledge discipline from [DIST-001](001-why-distribution-changes-the-problem.md).

Keep these distinctions ready:

- implementation object versus modeled variable;
- logical identity versus address;
- value equality versus message identity;
- event occurrence versus event observation;
- finite test trace versus all allowed behavior;
- nondeterministic choice versus probability;
- safety over prefixes versus liveness over admissible infinite executions.

No detailed synchrony, failure detector, snapshot, or consistency-model knowledge is assumed.

## Learning Objectives

By the end of this module, you should be able to:

1. distinguish processes, process incarnations, nodes, endpoints, and roles;
2. specify directed link state and delivery semantics without importing accidental transport guarantees;
3. represent a global configuration containing local, channel, persistent, and environment state;
4. define internal, input, output, send, receive, crash, and recovery actions at an explicit abstraction boundary;
5. validate whether an action sequence is an execution of a transition relation;
6. project an execution into a schedule, trace, and participant-local history;
7. explain why the same local history may correspond to different global executions;
8. state admissibility and fairness assumptions separately from transition safety;
9. choose an abstraction fine enough for the property yet small enough to analyze; and
10. bound executable traces, model exploration, logs, and operational evidence without overclaiming proof.

## Core Exposition

### Processes are semantic agents

A process is the unit whose state and next-step rule the model defines. Depending on the question, it may represent a client, replica, protocol role, actor, thread, service instance, device controller, or environment participant. The model commonly gives process \(p\) a state set \(S_p\), initial states \(I_p\), and actions whose enabling conditions and effects mention \(S_p\).

Calling the agent sequential does not claim its implementation has one thread. It means the abstraction presents a local order of atomic actions. A multithreaded server may be refined into several modeled processes when races matter, or abstracted as one process when its internal synchronization already establishes the exported transition relation.

Separate a **logical process identity** from a **process incarnation**. If `worker-3` crashes and restarts, the new runtime may reuse the name and address while lacking volatile state held by the old runtime. Represent incarnation as an epoch, generation, boot identifier, or fresh identity when stale messages or authority matter. A message addressed to role `leader` is not thereby addressed to the current authorized incarnation.

### Nodes are deployment and failure abstractions

A node hosts process incarnations and relevant resources. The placement function can be written \(host_C(p)=n\), indexed by configuration or time when migration and rescheduling are allowed. Several modeled processes on one node may fail together. One logical process may move across nodes. A physical server may contain virtual nodes with partly shared power, kernel, storage, network, or administration.

“Different nodes” does not prove independent failure. Name shared runtime, machine, power, network, identity, control-plane, software, and operator domains relevant to the claim. Conversely, two colocated processes can be distributed semantically when they communicate asynchronously without shared immediate state. Node state distinguishes relevant volatile, stable, external, credential, clock, and configuration state. Crash, replacement, and recovery actions state what disappears, persists, or receives a new incarnation; later modules refine the failure classes.

### Links are directed state machines

A link \(\ell=(p,q)\) models communication from endpoint \(p\) to endpoint \(q\). Bidirectional communication normally requires two directed links because delay, reachability, buffers, credentials, and failure may be asymmetric. The channel state \(Q_\ell\) could be:

- a sequence for FIFO delivery;
- a multiset when reordering is unconstrained;
- a set when duplicates collapse in the abstraction;
- a bounded sequence with admission or drop actions;
- a collection of packets, frames, stream bytes, or application messages;
- a richer automaton with connection generations, retransmission, authentication, and corruption states.

The representation follows the property. TCP's ordered byte-stream abstraction does not preserve application messages; a broker acknowledgement need not represent consumer effect; and local `send` may only enqueue data. Remote meaning requires a protocol guarantee. Separate message identity from payload: equal values may be distinct transmissions, and one occurrence may be delivered repeatedly. Retain the operation, transmission, incarnation, destination, fingerprint, sequence/epoch, and authentication fields relevant to deduplication or replay.

### Configurations include what is not locally visible

For fixed process and link sets, a configuration is often

\[
C=(s_1,\ldots,s_n,q_1,\ldots,q_m,e,d),
\]

where \(s_i\) are process-local states, \(q_j\) are channel states, \(e\) is environment state, and \(d\) represents modeled durable or external state. It is “global” as a mathematical description, not necessarily something any real observer can read atomically.

Messages in flight are part of state. Omitting them makes a send followed by a delayed receive appear to create information from nowhere. Pending timers, queued inputs, uncommitted operations, leases, membership, and process generations also belong if they influence enabled actions or properties.

Initial configurations \(Init\subseteq C\) declare allowed starting state. One deployment may have several valid initial configurations because input, placement, keying, or membership varies. Hidden assumptions often enter here: empty channels, unique IDs, consistent configuration, synchronized replicas, or no preexisting external effects. State them.

### Actions and transitions

An action label describes one transition at the selected granularity. Common categories are:

- **input:** an environment-controlled request, signal, or delivery;
- **output:** a system-visible response or externally observable action;
- **internal:** local computation hidden from an external trace;
- **send:** change local and channel state to introduce communication;
- **receive/deliver:** remove or select channel content and change receiver state;
- **environment:** schedule, user, device, or dependency behavior;
- **lifecycle:** crash, stop, recover, replace, migrate, join, or leave under the model.

The relation \(C\xrightarrow{a}C'\) means action \(a\) is enabled in \(C\) and taking it may produce \(C'\). A guard states when it is enabled; an effect states changed variables; a frame condition preserves everything else. If several successors are possible, the transition is nondeterministic.

Nondeterminism is not randomness. It represents underspecification, scheduler choice, environment choice, or behavior outside the abstraction. A probability distribution is an additional model, not implied by “one of these actions may occur.” Proving a safety invariant for all nondeterministic choices can be stronger than sampling likely schedules; quantitative reliability needs probabilistic evidence.

Atomic actions must have a refinement story. “Send request and receive response” cannot be one atomic action if timeout ambiguity matters. “Commit database row and outbox record” may be one action if a transactional substrate with that atomic guarantee is explicitly assumed. The abstraction boundary is valid relative to a claim, not universally.

### Executions, schedules, behaviors, and traces

An execution fragment is an alternating sequence

\[
C_0,a_1,C_1,\ldots,a_k,C_k
\]

where every adjacent transition is legal. It is an execution if \(C_0\in Init\). It may be finite or infinite. Its schedule is \(a_1,\ldots,a_k\). A behavior often means a state sequence or externally relevant execution projection; terminology varies, so define it in each analysis.

A **trace** hides internal actions and possibly internal values, retaining an interface projection. Two implementations can have different internal executions but the same external trace. Trace refinement asks whether every implementation trace is permitted by a higher-level specification. It does not make hidden resource, timing, or fault properties disappear unless the abstraction includes them.

A process history \(H_p\) projects to actions observed by or at \(p\), often plus local states. If \(H_p(e_1)=H_p(e_2)\), process \(p\) cannot choose different deterministic next actions based solely on those histories. This indistinguishability technique connects modeling to impossibility and safety arguments.

One recorded log is not automatically an execution. Entries can be missing, duplicated, export-reordered, clock-skewed, emitted before durable effect, or lost after it. Preserve event identity, incarnation, local sequence, message correlation, capture stage, and uncertainty.

### Reachability, prefixes, and invariants

A configuration is reachable if some finite execution leads to it. A state invariant \(Inv\) must hold in every reachable configuration. Inductive proof establishes:

\[
Init\Rightarrow Inv
\]

and

\[
Inv(C)\land Next(C,a,C')\Rightarrow Inv(C').
\]

The second obligation covers every enabled action, including link, environment, crash, and recovery actions admitted by the model. Checking only “normal” process actions proves a property of a smaller system.

Safety violations usually have a finite bad prefix. Model checking enumerates a bounded or finite representation of possible choices and can find counterexample schedules. It establishes the checked model, bounds, and properties—not the correctness of unmodeled code, infrastructure, operators, or assumptions.

### Admissibility, fairness, and progress

The transition relation describes what can happen. An admissibility condition restricts which complete executions the claim considers. It may bound failures, require authenticated delivery, constrain timing, restrict environment inputs, or add fairness.

Fairness prevents selected enabled work from being postponed forever. Weak fairness commonly says an action continuously enabled eventually occurs; strong fairness can require occurrence when enabled infinitely often. Framework definitions differ. State the exact version and scope. Fairness for process scheduling does not imply message delivery; reliable delivery does not imply a receiver is scheduled; a fair server does not imply the environment submits a request.

Safety should not depend on fairness: a forbidden state remains forbidden even in an unfair prefix. Liveness almost always needs progress assumptions. “Every request eventually completes” might require the client and server remain active, relevant links eventually deliver, retries continue, resources become available, and failures cease or stay within a tolerated pattern. Later modules refine timing and fault assumptions.

### A deterministic execution artifact

The following executable model presents one chosen schedule. A directed client-to-worker link duplicates a request. The worker's stable logical-operation set suppresses a second effect and replays an acknowledgement; the client suppresses the duplicate acknowledgement.

<!-- bijux-verify: {"id":"explicit-configuration-trace","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"00 client send request:r7 c2w=1 w2c=0\n01 link duplicate request:r7 c2w=2 w2c=0\n02 worker apply r7 c2w=1 w2c=1\n03 worker replay r7 c2w=0 w2c=2\n04 client accept ack:r7 c2w=0 w2c=1\n05 client suppress ack:r7 c2w=0 w2c=0\nfinal worker_effects=['r7'] client_acks=['r7']\n","stderr":""}} -->
```python
processes = {
    "client": {"acks": []},
    "worker": {"seen": [], "effects": []},
}
links = {"c2w": [], "w2c": []}
trace = []


def record(label):
    trace.append(
        f"{len(trace):02d} {label} "
        f"c2w={len(links['c2w'])} w2c={len(links['w2c'])}"
    )


request = ("request", "r7")
links["c2w"].append(request)
record("client send request:r7")

links["c2w"].append(links["c2w"][0])
record("link duplicate request:r7")

while links["c2w"]:
    message_type, request_id = links["c2w"].pop(0)
    assert message_type == "request"
    if request_id not in processes["worker"]["seen"]:
        processes["worker"]["seen"].append(request_id)
        processes["worker"]["effects"].append(request_id)
        outcome = "apply"
    else:
        outcome = "replay"
    links["w2c"].append(("ack", request_id))
    record(f"worker {outcome} {request_id}")

while links["w2c"]:
    message_type, request_id = links["w2c"].pop(0)
    assert message_type == "ack"
    if request_id not in processes["client"]["acks"]:
        processes["client"]["acks"].append(request_id)
        outcome = "accept"
    else:
        outcome = "suppress"
    record(f"client {outcome} ack:{request_id}")

for line in trace:
    print(line)
print(
    f"final worker_effects={processes['worker']['effects']} "
    f"client_acks={processes['client']['acks']}"
)
```

The run verifies state updates for one finite schedule in one toy model. It does not prove durability of `seen`, reliable delivery, all interleavings, process isolation, crash recovery, security, transport behavior, application correctness, or exactly-once effects beyond this in-memory boundary.

## Definitions and Notation

Let:

- \(P\) be a set of logical processes;
- \(N\) be nodes or declared deployment containers;
- \(host_C:P\rightarrow N\) map active incarnations to nodes in configuration \(C\);
- \(L\subseteq P\times P\) be directed links;
- \(S_p\) be local states of process \(p\);
- \(Q_\ell\) be states of link \(\ell\);
- \(E\) be relevant environment states;
- \(A=A_{in}\cup A_{out}\cup A_{int}\) be input, output, and internal action labels;
- \(Init\) be initial configurations;
- \(Next\subseteq C\times A\times C\) be the transition relation;
- \(\alpha=C_0,a_1,C_1,\ldots\) be an execution;
- \(sched(\alpha)\) be its action schedule;
- \(trace_V(\alpha)\) be its projection to visible interface \(V\); and
- \(H_p(\alpha)\) be process \(p\)'s local-history projection.

A **state** is a valuation at one abstraction level. A **configuration** combines all modeled component states. An **event** is an occurrence of an action in an execution, so two occurrences may have the same action label but distinct event identities.

An action is **enabled** when at least one allowed successor exists. An execution is **maximal** if it cannot be extended or is infinite. A **run** often means an execution of an implementation or test; because terminology differs, do not infer fairness or maximality from the word alone.

A **reachable set** \(Reach\) is the least set containing \(Init\) and closed under \(Next\). A **history** or **trace** is a projection, never automatically the entire configuration sequence. A **cut** selects prefixes of process histories; consistency of cuts is deferred to DIST-007.

## Mechanisms, Invariants, or Proof Structure

Build and review the model in this order:

1. **State the property and abstraction boundary.** Decide which differences can change the claim.
2. **Name participants and environment.** Separate process, role, incarnation, node, external authority, and observer.
3. **Define state ownership.** Local volatile state, durable state, channel contents, timers, configuration, and external effects.
4. **Define links.** Direction, message identity, ordering, duplication, loss, capacity, corruption/authentication, and creation lifecycle.
5. **Define actions.** Guards, effects, frame conditions, controlling participant, visible label, and atomicity assumption.
6. **Define initial configurations.** Include preexisting inputs, channel contents, membership, identities, versions, and persistent records.
7. **Generate legal executions.** Vary enabled choices rather than selecting a convenient schedule.
8. **Project observations.** Derive per-process histories, external traces, logs, and diagnostic evidence.
9. **State admissibility.** Timing, failures, fairness, environment, adversary, and resource bounds.
10. **Prove and test separately.** Induct over actions for invariants; explore schedules for counterexamples; validate implementation-to-model correspondence.

The **transition legality invariant** requires each observed or generated step to be enabled and to change only variables permitted by its action. The **message provenance invariant** requires a receive to correspond to message creation allowed by the channel/adversary model. The **incarnation invariant** prevents stale process state, messages, leases, or authority from being attributed to a replacement without a declared recovery transition.

The **projection discipline** forbids reasoning from information hidden by a participant's projection. A global execution diagram helps an analyst, but code at process \(p\) sees only \(H_p\) plus explicitly supplied or inferred facts. The **quantification discipline** requires a universal correctness claim to cover every admissible execution, including unfavorable schedules.

For an inductive invariant, check initiality and preservation for every action. For trace refinement, map concrete states/actions to abstract ones and show every concrete visible behavior is allowed; internal concrete steps may map to stuttering. For liveness, add exact fairness assumptions only after stating which continuously or repeatedly enabled actions must progress.

## Alternatives and Trade-Offs

**Process-per-service versus process-per-role.** Service-level agents keep models small but can hide concurrency, failover, and shared state. Role- or request-level agents reveal interactions but expand the state space. Split where internal order affects the property.

**Node-centric versus process-centric state.** Node models align with deployment and fault injection. Process models align with algorithms and proofs. Use both with an explicit placement relation when correlated failure, migration, or restart matters.

**FIFO sequence versus unordered multiset channel.** FIFO enables stronger algorithms and simpler reasoning but may import guarantees absent across reconnect, retry, broker partition, or multiple paths. A multiset exposes reorderings but enlarges behavior. Choose the weakest justified link.

**Messages versus bytes.** Message abstraction suits protocol semantics. Byte-stream abstraction exposes framing and partial-write behavior. A layered proof can assume a verified framing component, but the assumption must be visible.

**Fine versus coarse atomicity.** Fine actions expose races and failures but cause state explosion. Coarse actions improve tractability but need refinement evidence. Increase granularity until counterexamples relevant to the claim remain expressible.

**Nondeterministic versus probabilistic choice.** Nondeterminism supports worst-case universal reasoning. Probability supports likelihood and expected-cost claims but requires justified distributions and independence assumptions. Production frequency samples do not automatically supply those distributions.

## Failure Modes and Misconceptions

1. **“A node is a process.”** One is a deployment/failure abstraction; the other is an algorithmic agent.
2. **“An IP address identifies one participant forever.”** Addresses, routes, ports, and workloads can be reassigned.
3. **“Restart resumes the same state.”** Volatile state and authority may differ; incarnation must be modeled.
4. **“The network is one bidirectional link.”** Directional reachability and buffering can differ.
5. **“Reliable means immediate and exactly once.”** Reliability needs a definition and scope; delay and duplicate application effects remain possible.
6. **“TCP delivers messages.”** It exposes an ordered byte stream; framing belongs above it.
7. **“The queue is outside system state.”** In-flight messages change future behavior.
8. **“A send log proves receipt.”** It proves an observation at a named send stage.
9. **“Timestamp sorting reconstructs truth.”** Capture stages, clocks, export delay, and missing events remain.
10. **“One simulation run is the model.”** It is one execution selected from the model.
11. **“Random testing covers all schedules.”** Sampling can miss rare short counterexamples.
12. **“Fairness is realistic by definition.”** It is an assumption that excludes executions and must be defended.
13. **“Safety follows if nodes eventually recover.”** Safety must hold before eventual recovery.
14. **“An atomic box in a diagram is atomic in production.”** The refinement obligation remains.

## Worked Examples

### Example 1

**Question:** A service has three replicas on one virtual machine. How many processes and nodes exist?

**Reasoning:** The algorithm may have three replica processes but the deployment model has one shared node/failure container. A machine crash removes all three; process crashes might not.

**Conclusion:** Replication count and independent node count are different variables.

### Example 2

**Question:** `worker-9` restarts on the same address. Is it the same process?

**Reasoning:** It may retain a logical role, but it is a new incarnation. Old replies, leases, and cached authority require an epoch and recovery rule.

**Conclusion:** Stable names do not erase lifetime boundaries.

### Example 3

**Question:** A client library reports “write completed.” Which action occurred?

**Reasoning:** The answer depends on the abstraction: copied to user buffer, queued in kernel, acknowledged by transport peer, parsed by server, or committed by application. Only the API/protocol contract identifies it.

**Conclusion:** Name the transition and acknowledgement level.

### Example 4

**Question:** May a receive occur when the channel multiset contains two equal payloads?

**Reasoning:** Yes, if each is a permitted message occurrence. Payload equality does not determine identity. The model selects one occurrence and applies receiver/link transitions.

**Conclusion:** Preserve identity separately from value.

### Example 5

**Question:** Two action schedules lead to the same final balances. Are the executions equivalent?

**Reasoning:** Not necessarily. Intermediate overdraft, emitted notifications, observed reads, audit order, or external effects can differ. Equivalence is relative to a declared trace projection and property.

**Conclusion:** Final state alone does not characterize behavior.

### Example 6

**Question:** Can model checking five nodes prove a protocol for every cluster size?

**Reasoning:** It proves the encoded finite instances and bounds if exploration is exhaustive. A cutoff theorem, parameterized proof, or independent argument is needed to generalize.

**Conclusion:** Record model bounds and the generalization obligation.

### Example 7

**Question:** Does weak fairness ensure a message is delivered?

**Reasoning:** Only if the relevant delivery action remains continuously enabled and lies within the fairness set. A link that may drop the message, a receiver that crashes, or changing guards can defeat that premise.

**Conclusion:** Fairness attaches to exact actions and enabling conditions.

### Example 8

**Question:** A distributed trace lacks a server commit span. Did commit not occur?

**Reasoning:** The span may be unsampled, lost, emitted after a crash, rejected by export, or absent due to instrumentation. Conversely, a precommit log may exist although rollback follows.

**Conclusion:** Observability evidence needs capture and authority semantics.

### Example 9

**Question:** A payment workflow model treats “charge card and record order” as one action. Is its no-orphan-charge proof valid?

**Reasoning:** Only if a real substrate atomically controls both effects, which ordinary separate payment and database authorities generally do not. Otherwise split request, remote outcome, local record, reconciliation, refund, and ambiguous states. Payment, accounting, fraud, security, privacy, legal/regulatory, operations, accessibility, and independent assurance authorities must review production claims. No external review is claimed.

**Conclusion:** An unrealizable atomic action can prove the wrong system.

### Example 10

**Question:** A control system coordinates pumps over field links. Can exhaustive protocol-model exploration authorize physical operation?

**Reasoning:** No. The model can reveal schedules and invariant violations under encoded assumptions. Sensor/actuator physics, calibration, electrical/mechanical hazards, network behavior, human override, maintenance, cyber compromise, common-cause failures, emergency response, and regulatory evidence require named controls, process, mechanical, electrical, safety, human-factors, cybersecurity, operations, maintenance, and independent regulatory/assurance review.

**Conclusion:** Formal execution evidence is bounded evidence, not physical-safety authorization.

## Cross-Program Connections

[Programming Languages: Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) supplies state machines, schedules, atomicity, and memory models within processes. [Operating Systems](../../22-operating-systems/ROADMAP.md) supplies runtime processes, threads, scheduling, clocks, virtual memory, IPC, persistence, and crash behavior. These implementation mechanisms must be mapped to modeled actions.

[Network Engineering](../../24-network-engineering/ROADMAP.md) supplies packet, path, transport, and failure mechanics. A distributed link abstracts selected properties from those layers. [Computer Architecture](../../23-computer-architecture/ROADMAP.md) exposes hardware ordering, persistence, interrupts, and failure boundaries below a node abstraction.

[Database Engineering](../../18-database-engineering/ROADMAP.md) supplies transaction and recovery substrates that may justify coarse atomic actions. [Software Engineering: Patterns, Architecture, and Practice](../../11-software-engineering-patterns/ROADMAP.md) supplies component boundaries and interface contracts; distributed models test whether those boundaries preserve real execution semantics.

[Security Engineering](../../25-security-engineering/ROADMAP.md) adds authenticated principals, adversarial message creation, replay, compromise, and trust boundaries. [Systems Engineering](../../26-systems-engineering/ROADMAP.md) relates execution properties to operational context, hazards, people, enabling systems, and validation authority.

## References

- Nancy A. Lynch, [*Distributed Algorithms*](https://groups.csail.mit.edu/tds/distalgs.html), Morgan Kaufmann, 1996. Automata-theoretic treatment organized by timing and communication models.
- Nancy A. Lynch and Mark R. Tuttle, [Input/Output Automata resources](https://groups.csail.mit.edu/tds/i-o-automata.html), MIT Theory of Distributed Systems. Primary labeled-transition, action, execution, fairness, trace, and composition framework.
- Stephen J. Garland and Nancy A. Lynch, [*The IOA Language and Toolset*](https://groups.csail.mit.edu/tds/papers/Lynch/IOA-TR.html), MIT/LCS/TR-762, 1998. Specification, decomposition, validation, and implementation refinement using I/O automata.
- Leslie Lamport, [*Specifying Systems*](https://lamport.azurewebsites.net/tla/book.html), Addison-Wesley, 2002. State/action behaviors, stuttering, fairness, composition, and model checking.
- Leslie Lamport, [*Time, Clocks, and the Ordering of Events in a Distributed System*](https://lamport.azurewebsites.net/pubs/time-clocks.pdf), *Communications of the ACM* 21(7), 1978. Processes, events, message edges, and partial-order foundation.
- K. Mani Chandy and Leslie Lamport, [*Distributed Snapshots: Determining Global States of Distributed Systems*](https://lamport.azurewebsites.net/pubs/chandy.pdf), *ACM Transactions on Computer Systems* 3(1), 1985. Process/channel-state and global-state foundation.
- Michael J. Fischer, Nancy A. Lynch, and Michael S. Paterson, [*Impossibility of Distributed Consensus with One Faulty Process*](https://groups.csail.mit.edu/tds/papers/Lynch/jacm85.pdf), *Journal of the ACM* 32(2), 1985. Primary configuration, event, schedule, reachability, and admissible-run reasoning.
- Wesley M. Eddy, editor, [RFC 9293: Transmission Control Protocol](https://www.rfc-editor.org/rfc/rfc9293), IETF Internet Standard, 2022. Authoritative ordered reliable byte-stream transport specification and application-framing boundary.

## Exercises

### Exercise 1

Model a two-process request/reply protocol. Define process state, two directed links, message identities, initial configurations, send/receive/internal actions, and three legal executions ending in different observable states.

### Exercise 2

Given a deployment with two service processes per virtual machine, three virtual machines per physical host, and two hosts sharing one power feed, construct process, node, placement, incarnation, and nested failure-domain models. Explain which counts support which failure claim.

### Exercise 3

Audit an incident timeline built by sorting client, proxy, server, database, and queue logs by wall-clock timestamp. Identify projection, capture, identity, incarnation, clock, missing-event, and authority defects. Propose a more defensible execution reconstruction.

### Exercise 4

Write proof obligations for an invariant: “each logical request ID causes at most one inventory decrement.” Include initiality, every process/link/crash/recovery action, durable deduplication state, identity collision, retention, and external effect boundaries.

### Exercise 5

A multi-hospital medication-allocation service coordinates pharmacy inventory, prescriptions, transfers, delivery, and bedside administration across intermittent links. Define its processes, nodes, links, state, actions, executions, fairness/failure assumptions, invariants, evidence, and named human-review roles before operational acceptance.

## Answers to the Exercises

### Answer 1

Let client state be `idle`, `waiting(r)`, or `done(r,result)`; server state contain a durable map from request ID/fingerprint to status/result. Directed channel states \(Q_{cs}\) and \(Q_{sc}\) are multisets of request and response occurrences. Initial state is idle client, empty result map, and empty channels. `invoke(r,payload)` changes client state and appends a request; link actions may deliver, delay, duplicate, or drop according to the declared model; `handle` validates identity/fingerprint and atomically stores a result; `reply` adds a response; `accept` changes matching waiting state.

One execution delivers, handles, replies, and reaches `done`. A second delays the request and ends in a finite waiting prefix with it in \(Q_{cs}\). A third handles durably but delays the response, leaving client waiting, server result recorded, and response in \(Q_{sc}\). If finite executions need be maximal, add explicit stop/environment actions or call them execution fragments. The three client histories may initially match although global configurations differ.

### Answer 2

Model twelve service processes placed two per VM across six VM nodes, with incarnation IDs for each runtime lifetime. Map three VMs to each of two physical-host domains, and map both hosts to one power-feed domain. A process count supports algorithmic membership only. VM count supports isolation from process/runtime failures only under the hypervisor and resource assumptions. Host count supports tolerance of one host failure only if replicas are placed across hosts and the shared dependencies survive. The single power feed means the design has zero redundancy against that feed's loss.

Placement must be part of each configuration if rescheduling occurs. A replacement on another VM receives a new incarnation even when it assumes the same logical replica role. Add rack, network, storage, identity, release, operator, and region domains if relevant. Independence is never inferred from different labels; the failure model names shared causes and evidence.

### Answer 3

Each log is a capture-point projection: client “sent” may precede transmit, server “commit” may precede durability, and queue publish may record acceptance rather than consumption. Correlation values can be reused, missing generations can merge incarnations, clocks have error, and exporters reorder or drop entries. Preserve event, operation, transmission, and incarnation IDs; local sequence; matched send/receive edges; capture stage; clock bounds; sampling status; and authoritative transitions. Construct a partial order from verified edges, retain uncertain alternatives, reconcile durable records, and state gaps. Reconstruction is not an atomic global observation.

### Answer 4

Define the effect boundary first: the decrement must occur in the same authority as the durable deduplication record, or the invariant needs a cross-authority protocol. Initially no request ID is associated with more than one decrement. For every action, assume the invariant and prove preservation: request creation has collision-resistant or authority-unique identity; send/delay/drop/duplicate/reorder changes no inventory; receive does not decrement; validation binds ID to payload; the atomic apply action records ID and decrement together; matching retry returns recorded outcome; conflicting fingerprint rejects; reply actions do not decrement.

Crash preserves the atomic record or neither record/effect; recovery restores it before processing. Replacement and failover cannot expose a stale writable copy; epochs/fencing or one transactional authority enforce this. Retention must exceed every retry, replay, restore, and message lifetime or use a permanent business identity. Include administrator repair, backup restore, migration, reconciliation, and cancellation actions. If a warehouse actuator or external supplier decrements separately, the local invariant cannot cover that effect without idempotent cooperation and evidence.

### Answer 5

Processes include prescriber/order authority, hospital pharmacy services, inventory authorities, allocation coordinator, transfer/logistics services, identity/allergy/clinical-record interfaces, bedside administration record, monitoring, and explicit human roles. Nodes include hospital runtimes, databases, edge devices, scanners, mobile devices, network/control services, and replacement incarnations, mapped to power, provider, facility, software, identity, and operator failure domains. Use directed authenticated links with explicit ordering, duplication, delay, loss, capacity, replay, and disconnected behavior.

State includes prescription version/authority, patient/medication identity, units, lot/expiry, inventory reservations and physical reconciliation, allocation/transfer status, custody, administration, overrides, deduplication, epochs, channel contents, audit, and uncertainty. Actions cover order/correct/cancel, validate, reserve/release, pick, transfer custody, receive, administer/withhold, reconcile, expire, alert, crash/recover, disconnect/rejoin, override, and compensate. Invariants forbid unauthorized or conflicting orders, unit/identity mismatch, double allocation, stale authority, silent inventory creation/loss, administration without required checks, and erased provenance.

Executions cover duplicate/reordered messages, long partition, stale data, simultaneous demand, substitution, inventory mismatch, crash/restore, malicious input, clock error, overload, override, and reconciliation. Liveness requires named staff availability, eventual relevant connectivity or safe manual fallback, service recovery, and bounded faults; fairness attaches to actions, not patient outcomes. Evidence combines model/invariant work, implementation conformance, recovery and fault tests, pharmacy workflow and accessibility studies, audits, downtime exercises, staged pilots, incidents, and monitoring.

Named reviewers include clinicians, pharmacists, nursing and patient-safety specialists, clinical informatics, patient/accessibility representatives, logistics, biomedical engineering, distributed/data/network engineers, cybersecurity, privacy/legal, human factors, hospital operations, training/maintenance, emergency management, vendors, regulators, and independent clinical/technical assurance. Accountable clinical and hospital authorities accept residual risk. Internal model and code evidence provides no clinical authorization, regulatory acceptance, or external review.
