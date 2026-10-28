---
module_id: CONPAR-082
program: Programming Languages: Concurrent & Parallel Programming
level: 2
module_number: 82
title: Point-to-Point Message Passing
status: complete
last_verified: 2026-08-29
---

# Point-to-Point Message Passing

## One-Page Review

### Governing question

How can two communicator members exchange typed payloads with unambiguous matching, safe buffer lifetimes, valid ordering/progress assumptions, and a protocol that cannot deadlock when implementation buffering changes?

### Essential definitions

- A **message envelope** identifies communicator/context, source, destination, and tag; a receive pattern may use allowed wildcards.
- A **payload signature** is count plus datatype; sender and receiver signatures must be compatible and the receive capacity sufficient.
- **Message matching** selects an eligible send for a posted receive using communicator, destination, source pattern, and tag pattern.
- A **status** reports actual source/tag and supports querying the received element count.
- A **blocking send** returns according to its send mode; it need not mean the receiver processed the message.
- **Standard send** may use buffering or rendezvous; correctness must not depend on an eager threshold.
- **Synchronous send** completes only after matching receive initiation has begun; **buffered send** uses application-attached buffer; **ready send** requires an already posted matching receive.
- A **nonblocking operation** returns a request; only completion permits protected send-buffer mutation or receive-buffer access.
- **Nonovertaking** gives scoped order for successive matching operations under MPI's conditions; it is not a total order across sources or logically concurrent threads.
- **Progress** guarantees apply once matching communication is enabled as specified; MPI does not generally guarantee fairness.
- **Probe/matched probe** discovers an incoming envelope/size before receiving, with concurrency distinctions.
- A **communication protocol** defines message kinds/tags, state transitions, counts/types, ordering, termination, errors, and resource bounds.

### Central model, mechanism, or theorem

Treat each transfer as an envelope plus a typed byte/element contract inside a protocol state machine. The receive matches only messages allowed in the current state, validates actual source/tag/count, and advances state exactly once. Prove safety by matching compatibility and buffer lifetime; prove deadlock freedom with a wait-for graph or by posting receives before potentially blocking sends/using a reviewed combined exchange; prove boundedness without assuming standard sends buffer. Wildcards and concurrent completion introduce nondeterminism that must be either excluded or included in the result contract.

### Critical invariants

Source/destination ranks are valid in the same communicator; tag values are in range and partitioned by durable protocol meaning; sender/receiver datatype signatures and counts are compatible; receive capacity cannot truncate; actual status is checked when wildcard/dynamic behavior matters; ordinary message buffers do not overlap illegally and live unchanged/inaccessible until operation completion; requests complete exactly once before reuse/free; protocol states accept only expected kinds/generations; required receives can be posted without waiting cyclically; correctness is independent of eager/rendezvous thresholds and incidental progress threads; cancellation is completed/tested rather than assumed; and errors/partial payloads never authorize application commit.

### Common failures

Teams send raw pointers, swap count/type, ignore truncation/status, reuse one tag for unrelated protocols, use `ANY_SOURCE` then assume sender, receive a header and payload from different sources, post blocking sends in a cycle, rely on small messages being eagerly buffered, treat send return as remote processing, mutate an `Isend` buffer early, read an `Irecv` buffer before wait/test, drop requests, confuse local and remote completion, assume thread call order, poll unfairly, probe while another thread can steal the message, cancel without completing the request, or terminate while peers still expect data.

### Compact example

An inbox at destination rank 1 contains `(source,tag,sequence)` envelopes `(0,7,0)`, `(2,7,0)`, `(0,7,1)`, `(0,9,2)`. An exact receive `(0,7)` takes the first; wildcard source/tag 7 then takes source 2; the next exact `(0,7)` takes sequence 1; tag 9 takes control. This deterministic list model illustrates patterns and status, not MPI arrival or wildcard scheduling.

### Connections

[Processes and Ranks in Distributed-Memory Programs](081-processes-and-ranks-in-distributed-memory-programs.md) defines communicator-relative identity and lifetime. [Backpressure in Asynchronous Pipelines](040-backpressure-in-asynchronous-pipelines.md) supplies resource bounds. [Lock Ordering and Deadlock Prevention](018-lock-ordering-and-deadlock-prevention.md) supplies wait-for reasoning. The [program roadmap](../ROADMAP.md) next treats collectives and domain decomposition.

## Governing Question

For each protocol state, which envelope and payload may be sent or received, what completes locally and remotely, which buffers remain owned, and why can every legal execution progress without depending on undocumented buffering, timing, or fairness?

MPI point-to-point routines are a transport vocabulary, not a complete protocol. Source, tag, communicator, count, datatype, request, status, and state must agree across independently executing processes.

## Why This Matters

Point-to-point communication builds halos, work queues, pipelines, RPC-like services, distributed graphs, and collective algorithms. Its explicitness supports high performance and precise ownership, but small mistakes yield hangs, truncation, wrong-source data, nondeterminism, or silent corruption.

Many bugs hide in tests because implementations eagerly buffer small messages. At scale or with larger payloads, rendezvous removes the accidental slack and a cycle deadlocks. Production design assumes no buffering beyond the chosen send-mode contract and tests across thresholds.

## Prerequisites and Retrieval

Retrieve:

- processes, ranks, communicators, private addresses, lifecycle, thread support, placement, and failure from [Processes and Ranks in Distributed-Memory Programs](081-processes-and-ranks-in-distributed-memory-programs.md);
- channel capacity and overload policy from [Backpressure in Asynchronous Pipelines](040-backpressure-in-asynchronous-pipelines.md);
- wait-for cycles and acquisition ordering from [Lock Ordering and Deadlock Prevention](018-lock-ordering-and-deadlock-prevention.md); and
- happens-before versus observed time from [Happens-Before Relations](023-happens-before-relations.md).

Retrieval prompt: for every message kind, record communicator, sender set, receiver set, tag, header/version, count/datatype, maximum bytes, buffer owner/lifetime, send mode, posting/completion edge, accepted protocol states, sequence/generation, wildcard policy, timeout/error response, and termination rule. Draw the wait-for graph for minimum buffering.

## Learning Objectives

After completing this module, a learner can:

1. derive point-to-point matching from communicator, source, destination, tag, and receive posting;
2. validate count/datatype signatures, capacities, status, dynamic lengths, and truncation boundaries;
3. distinguish standard, synchronous, buffered, ready, blocking, nonblocking, persistent, and combined exchanges;
4. state local buffer ownership and completion rules for sends and receives;
5. apply nonovertaking, progress, fairness, wildcard, and multithreaded-order semantics correctly;
6. prove or refute deadlock freedom without assuming eager buffering;
7. design versioned tag/state protocols with bounded flow control and termination;
8. use probe/matched probe safely for dynamic messages and concurrent receivers;
9. test message sizes, schedules, process counts, thread modes, failures, and implementation thresholds; and
10. scope security, privacy, reproducibility, operations, and high-stakes review.

## Core Exposition

### Envelope matching and contexts

A send names destination rank and tag in communicator C; its source is the sender's rank in C and context comes from C. A receive at destination names source or `MPI_ANY_SOURCE`, tag or `MPI_ANY_TAG`, and the same communicator. An eligible message must match all constrained fields. Context isolation means identical ranks/tags in duplicated communicators do not collide.

Tags are finite nonnegative values through implementation-advertised `MPI_TAG_UB`. Allocate them by stable protocol kind—data, credit, termination, checkpoint—not temporary delivery sequence. If sequence/generation exceeds tag capacity or needs validation, place it in a versioned header. Never derive unbounded user IDs directly into tags.

Wildcards enable dynamic scheduling but introduce choice. With `ANY_SOURCE`, inspect status source and bind subsequent protocol actions to that sender/generation. A separate header receive followed by wildcard payload can splice two senders; use exact source from header or one packed/derived message. Separate communicators or matched probes isolate concurrent consumers.

### Payload signatures and status

MPI describes buffers with count and datatype. Matching requires compatible type signatures; different type maps can place compatible basic elements into noncontiguous memory. Receive capacity must hold the incoming signature. Too small causes truncation/error; excess receive capacity is allowed, and status/count queries reveal actual length subject to datatype semantics.

Use checked conversions and large-count interfaces where needed. Count times datatype extent can overflow application allocation/index arithmetic even if MPI represents counts. Derived datatypes need valid displacements, extents, committed lifetime, and underlying objects. Padding/uninitialized bytes, language representations, and heterogeneous portability require review.

For variable messages, send a bounded validated header then exact-source payload, or probe to discover the envelope/count before allocation. `MPI_Mprobe/Improbe` reserves a matched message, avoiding another receiver consuming it between probe and receive. Still enforce size quotas before allocation.

### What completion means

A blocking receive returns when its receive buffer contains the message and status is available. It does not mean the sender has continued or processed an acknowledgment. A standard blocking send returns when the send buffer may be reused; depending on protocol, the data may be copied locally or matching receive may be involved. It does not mean application-level remote consumption.

Synchronous-send completion establishes that a matching receive was initiated, useful for handshake evidence but not receiver processing. Buffered send copies into an attached user-managed buffer and can fail if space is insufficient; account for MPI overhead. Ready send is legal only when the matching receive is already posted—an assertion requiring its own proof.

Separate three acknowledgments that are often collapsed. Transport-local completion releases the sender's buffer. Receive completion makes bytes available to the receiver. Application acknowledgment states that the receiver validated and acted on a particular generation. Only the last can support business/scientific commit, and even it may need durable-storage or collective evidence. Encode application acknowledgments as ordinary versioned protocol messages with bounded retry/deduplication; do not infer them from send mode.

Blocking describes the calling thread, not necessarily the network algorithm. A blocking call can perform internal progress and return; a nonblocking initiation can still spend meaningful local time registering memory or copying metadata. Likewise, synchronous describes completion semantics, not that both processes execute in clock synchrony. Name each axis—blocking, send mode, persistence/partitioning—rather than using “synchronous” as a vague synonym for safe.

Nonblocking initiation creates a request. After `Isend`, do not modify/access protected buffer portions contrary to binding rules until completion. After `Irecv`, do not read/write receive region until completion. Wait/test variants complete requests and return statuses; dropping/freeing a request handle does not necessarily cancel the underlying operation or release buffer obligations.

### Ordering, progress, and fairness

MPI messages are nonovertaking under specific successive-operation/matching conditions. Two successive sends from one single-threaded rank to the same destination that both match a receive cannot be received second-first. This is not a total order across sources, different tags/receive patterns, communicator contexts, or logically concurrent threads. `ANY_SOURCE`, wait-any, cancellation, and concurrency add nondeterminism.

Progress says that once matching send/receive operations are initiated, at least one completes under the standard's conditions even if the counterpart is not executing another MPI call. It does not broadly promise asynchronous progress while processes compute or block outside MPI, and does not guarantee fairness. A message/receive can starve through repeated overtaking by other matches. Applications provide bounded arbitration where fairness matters.

Do not spin forever on `Iprobe` without backoff, progress calls, scheduling, shutdown, and starvation policy. A progress thread is implementation/configuration behavior with thread/CPU costs, not a portable premise unless explicitly required and qualified.

### Deadlock and buffering independence

Construct a wait-for graph whose vertices are protocol actions/processes and edges mean “cannot proceed until.” A cycle of receives waiting for sends that occur later always deadlocks. A cycle of standard blocking sends may deadlock when no buffers suffice, even if it works for small messages.

Safe pair exchange can post nonblocking receives, post sends, then wait for all; use `MPI_Sendrecv`; or impose an acyclic order such as even/odd roles. Check buffer aliasing and status. Synchronous sends are useful stress tests because they expose missing receives rather than eager buffering.

Bounded communication requires credits/windows. A sender may have at most K outstanding messages per peer/stream; receiver returns credit after consuming/releasing capacity. Credits themselves need an initial condition, protected accounting, termination, and loss/failure policy. MPI's internal buffers are not application backpressure.

### Executable matching model

This sequential Python inbox demonstrates exact and wildcard matching plus returned status. It does not model MPI arrival, network transport, buffering, datatype, concurrency, progress, fairness, or deadlock.

<!-- bijux-verify: {"id":"message-envelope-matching","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"initial_envelopes=[(0, 7, 0), (2, 7, 0), (0, 7, 1), (0, 9, 2)]\nreceive_1=('A0', {'source': 0, 'tag': 7, 'sequence': 0, 'count': 2})\nreceive_2=('B0', {'source': 2, 'tag': 7, 'sequence': 0, 'count': 2})\nreceive_3=('A1', {'source': 0, 'tag': 7, 'sequence': 1, 'count': 2})\nreceive_4=('CTRL', {'source': 0, 'tag': 9, 'sequence': 2, 'count': 4})\nremaining=0\nsource_0_tag_7_order=[0, 1]\n","stderr":""}} -->
```python
inbox = [
    {"source": 0, "tag": 7, "sequence": 0, "payload": "A0"},
    {"source": 2, "tag": 7, "sequence": 0, "payload": "B0"},
    {"source": 0, "tag": 7, "sequence": 1, "payload": "A1"},
    {"source": 0, "tag": 9, "sequence": 2, "payload": "CTRL"},
]
print(f"initial_envelopes={[(m['source'], m['tag'], m['sequence']) for m in inbox]}")

def receive(source, tag):
    for index, message in enumerate(inbox):
        source_matches = source is None or message["source"] == source
        tag_matches = tag is None or message["tag"] == tag
        if source_matches and tag_matches:
            selected = inbox.pop(index)
            status = {
                "source": selected["source"],
                "tag": selected["tag"],
                "sequence": selected["sequence"],
                "count": len(selected["payload"]),
            }
            return selected["payload"], status
    raise RuntimeError("no matching message")

results = [receive(0, 7), receive(None, 7), receive(0, 7), receive(0, 9)]
for index, result in enumerate(results, start=1):
    print(f"receive_{index}={result}")
print(f"remaining={len(inbox)}")
print(f"source_0_tag_7_order={[result[1]['sequence'] for result in results if result[1]['source'] == 0 and result[1]['tag'] == 7]}")
```

### Protocol state, termination, and errors

Define a versioned header with magic/version, message kind, run/stream/generation, logical object ID, element count/type/schema, payload bytes/digest if needed, flags, and error/termination semantics. Validate before allocation or state change. Network byte representation and MPI datatype portability are distinct decisions.

Model peer states: created, negotiating, active, draining, closed/failed. Accept data only in active state and expected generation. A termination message is ordered within its protocol stream but must account for outstanding data/credits. “No more sends” and “all prior data consumed/committed” are separate conditions; acknowledgments or collective termination may be needed.

MPI errors can surface at initiation or completion and error-handler behavior varies. Continuing after an MPI error is not generally guaranteed. Never interpret partially updated buffers/status as valid unless the standard/API explicitly defines it. Include communicator/job abort or supported recovery in the design.

Cancellation is exceptional. Calling cancel is only a request; complete/test the request and inspect cancelled status. Send cancellation is deprecated in MPI 4.1 and may be expensive. Protocol-level cancellation messages with generation and acknowledgment are often clearer, but cannot revoke already committed effects.

### Performance, verification, and operations

Latency combines software overhead, network path, serialization, queueing, rendezvous handshake, copying/registration, and contention. Bandwidth tests depend on size, in-flight depth, placement, NUMA/NIC affinity, transport, and memory type. Eager thresholds are implementation tuning details, not semantic boundaries. Optimize after measuring real traffic with validated results.

Aggregate small messages to amortize envelopes but bound latency/memory. Nonblocking overlap requires useful independent work and actual progress; posting thousands of requests can exhaust resources. Persistent/partitioned communication can amortize repeated setup or expose partitions, but retains matching, request, readiness, and completion contracts.

Test P=2,3,many; self and `MPI_PROC_NULL` where used; zero/one/maximum/dynamic counts; sizes around every observed protocol threshold; tags and `TAG_UB`; exact/wildcard sources; reordered/delayed messages; multiple threads; different communicators; nonblocking wait/test orders; synchronous sends; limited application credits; cancellation; peer error/exit; and shutdown with in-flight data. Use message/race/deadlock tools where available and deterministic model/reference outputs.

Security review covers untrusted sizes/tags/headers, allocation bombs, stale receive buffers, padding, cross-tenant transports, traffic metadata, logs/dumps, authentication/encryption requirements, and denial by message floods/starvation. MPI does not itself make an untrusted network/application protocol safe.

Operational evidence includes MPI/transport/NIC versions/config, eager/rendezvous settings only as observations, mapping/affinity, message-size/in-flight distributions, request high-water marks, progress CPU use, timeouts, terminal statuses, tracing overhead, and cleanup. High-stakes message correctness requires domain validation beyond delivery.

## Definitions and Notation

- `C`: communicator with context `ctx(C)` and group `G_C`.
- `s,d`: source and destination ranks in C.
- `t`: tag in `[0,TAG_UB]`.
- `E=(ctx(C),s,d,t)`: message envelope.
- `sigma=(n,D)`: count n and datatype D signature.
- `R=(s_pattern,t_pattern,C)`: receive matching pattern.
- `Q`: communication request and its lifecycle state.
- `B_s,B_r`: send and receive buffer regions.
- `K`: application credit/window bound.
- `g`: protocol generation/sequence.
- `W`: wait-for graph.
- `commit(g)`: application-level durable acceptance, distinct from MPI completion.

The receiver's actual source/tag/count come from status; send completion is not `commit(g)`.

## Mechanisms, Invariants, or Proof Structure

### Matching proof

For each receive state, enumerate allowed envelope patterns. Show exactly the intended sends can match in context C. If wildcards permit several, either every choice is semantically equivalent or status binds subsequent processing to the chosen sender/generation. Datatype signatures and capacity are compatible.

### Buffer-lifetime proof

From initiation to request/blocking completion, sender does not modify protected `B_s` and receiver does not access protected `B_r`. Datatype and communicator objects remain live. Completion occurs exactly once before buffer/request/object reuse/free; application acknowledgment is separate.

### Deadlock proof

Construct W under zero internal buffering and synchronous-send stress. Show W is acyclic, or prove at least one enabled receive/combined exchange breaks every potential cycle. Credits/resources are included; progress assumptions are only MPI-specified ones.

### Ordering/nondeterminism proof

Use nonovertaking only for ordered operations whose envelopes match the same receive conditions. Identify wildcard, multi-source, multithreaded, wait-any, cancellation, and race choices. Prove result invariance or record nondeterminism as part of the contract.

### Protocol/termination proof

Every header validates before effect; state transitions are total for valid inputs and reject invalid generation/kind/size. Data, credits, errors, and termination drain without leaks. External commit is idempotent/deduplicated and requires validated payload, not transport completion alone.

## Alternatives and Trade-Offs

| Mechanism | Main benefit | Principal risk/limitation |
|---|---|---|
| Blocking exact receive | simple state/ownership | idle/deadlock if ordered badly |
| Standard send | portable default | buffering-dependent completion timing |
| Synchronous send | handshake/stress safety | latency and potential cycles |
| Buffered send | local completion capacity | manual buffer sizing/failure |
| Ready send | reduced handshake opportunity | illegal unless receive preposted |
| Nonblocking send/receive | overlap and deadlock-safe posting | requests/lifetime/resource pressure |
| Send-receive | paired exchange without ordering cycle | fixed exchange shape |
| Probe then receive | dynamic sizes | race with concurrent receivers |
| Matched probe/receive | reserves discovered message | object/lifecycle complexity |
| Wildcard receive | dynamic work distribution | nondeterminism/starvation |
| Persistent/partitioned | repeated setup/fine readiness | more state and support constraints |

Prefer exact, bounded protocols; introduce wildcard/dynamic behavior only when its scheduling value is demonstrated.

## Failure Modes and Misconceptions

- **“Tag identifies a message globally.”** communicator/context, source, destination, and receive matter.
- **“Matching checks C struct layout.”** MPI matches datatype signatures, not application schema intent.
- **“Large receive count changes the message.”** it supplies capacity; status reveals actual count.
- **“Send return means peer processed it.”** usually only local buffer reuse is established.
- **“Small standard sends cannot deadlock.”** eager buffering is not guaranteed.
- **“Synchronous send is a remote acknowledgment.”** it proves matching receive initiation, not business processing.
- **“Ready send waits for readiness.”** it requires readiness already proven.
- **“Nonblocking means background progress.”** overlap/progress outside MPI is implementation-dependent.
- **“Request free cancels communication.”** operation/buffer obligations may remain.
- **“Messages always preserve send order.”** the guarantee is scoped, not global.
- **“Wildcard receive is deterministic.”** eligible sources can vary.
- **“MPI is fair.”** starvation prevention belongs to the application.
- **“Probe locks the message.”** ordinary probe can race with another receiver; matched probe reserves.
- **“Cancel immediately succeeds.”** complete and inspect cancellation.
- **“MPI buffers provide flow control.”** define application credits/limits.
- **“Transport success validates payload.”** schema, identity, digest, and domain checks remain.
- **“Timeout allows free.”** peer/device/runtime work may still access state; follow failure policy.

## Worked Examples

### Example 1

**Exact match.** Rank 1 receives source 0/tag 7 while source 2/tag 7 is queued. **Conclusion:** source pattern is part of protocol selection.

### Example 2

**Wildcard binding.** `ANY_SOURCE` returns source 2; the response uses status source 2, not assumed rank 0. **Conclusion:** actual status controls continuation.

### Example 3

**Header splice.** Wildcard header comes from rank 2 and wildcard payload from rank 3. Exact-source payload or one message fixes it. **Conclusion:** multi-message protocols bind generation/source.

### Example 4

**Truncation.** Sender sends 1,000 doubles; receiver allocates 100. **Conclusion:** validate/probe bounded count before receive.

### Example 5

**Eager deadlock.** Every ring rank blocking-sends a large message before receiving; rendezvous stalls the cycle. **Conclusion:** prove with zero buffering.

### Example 6

**Safe halo exchange.** Post left/right `Irecv`, post sends, wait-all, using `MPI_PROC_NULL` boundaries. **Conclusion:** preposted receives plus completion make ownership explicit.

### Example 7

**Early mutation.** Sender overwrites an `Isend` buffer before wait; receiver sees mixed data. **Conclusion:** request lifetime owns the region.

### Example 8

**Thread ordering.** Two sender threads issue same-tag messages without a defined order. Receiver cannot infer source-thread sequence. **Conclusion:** encode sequence and synchronize locally.

### Example 9

**Credit bound.** Receiver grants four credits; sender never exceeds four outstanding payloads. **Conclusion:** application capacity is independent of MPI eager buffers.

### Example 10

**Distributed insulin-control simulation.** Messages must preserve patient/scenario/model/time-step identity, units, physiology/control parameters, ordering, numeric/integration policy, deadlines, missing/duplicate behavior, checkpoints, privacy, and validated commit. Named endocrinology, control/biomedical, numerical, MPI/runtime, software-safety, security/privacy, operations, quality/regulatory, human-factors, and independent validation reviewers must approve requirements and evidence; none is claimed here. **Conclusion:** matched delivery and deadlock freedom do not establish medical validity or safety.

## Cross-Program Connections

- **Networks:** envelopes, framing, flow control, rendezvous, congestion, and reliability underpin transports.
- **Distributed systems:** protocol states, correlation IDs, backpressure, deduplication, termination, and partial failure recur.
- **Programming languages:** datatypes, buffer ownership, requests/futures, effects, and lifetimes constrain bindings.
- **Operating systems:** process isolation, pinned/registered memory, progress threads, affinity, and signals affect behavior.
- **Formal methods:** matching relations, state machines, wait-for graphs, and invariants support verification.
- **Algorithms:** halos, work queues, graph traversal, pipelines, and reductions build on messages.
- **Security:** untrusted lengths, floods, metadata, padding, logs, and transport boundaries need controls.
- **Testing:** threshold sweeps, schedule perturbation, synchronous stress, fault injection, and protocol models expose bugs.
- **Performance:** latency/bandwidth, aggregation, registration, in-flight depth, progress, and topology guide tuning.
- **Operations:** transport versions, affinities, request limits, timeouts, traces, terminal status, and cleanup sustain runs.

## References

1. MPI Forum, *MPI: A Message-Passing Interface Standard, Version 4.1*, Chapter 4, 2023. <https://www.mpi-forum.org/docs/mpi-4.1/mpi41-report.pdf>
2. MPI Forum, *MPI-4.1: Point-to-Point Communication Introduction*, 2023. <https://www.mpi-forum.org/docs/mpi-4.1/mpi41-report/node54.htm>
3. MPI Forum, *MPI-4.1: Communication Modes*, 2023. <https://www.mpi-forum.org/docs/mpi-4.1/mpi41-report/node67.htm>
4. MPI Forum, *MPI-4.1: Semantics of Point-to-Point Communication*, 2023. <https://www.mpi-forum.org/docs/mpi-4.1/mpi41-report/node68.htm>
5. MPI Forum, *MPI-4.1: Communication Initiation*, 2023. <https://www.mpi-forum.org/docs/mpi-4.1/mpi41-report/node73.htm>
6. MPI Forum, *MPI-4.1: Semantics of Nonblocking Communication Operations*, 2023. <https://www.mpi-forum.org/docs/mpi-4.1/mpi41-report/node75.htm>
7. MPI Forum, *MPI-4.1: Probe*, 2023. <https://www.mpi-forum.org/docs/mpi-4.1/mpi41-report/node79.htm>
8. MPI Forum, *MPI-4.1: Matched Probe*, 2023. <https://www.mpi-forum.org/docs/mpi-4.1/mpi41-report/node80.htm>
9. MPI Forum, *MPI-4.1: Cancel*, 2023. <https://www.mpi-forum.org/docs/mpi-4.1/mpi41-report/node82.htm>
10. Open MPI Project, *Point-to-Point Communication Manual Pages*, current documentation; retrieved 2026-08-29. <https://docs.open-mpi.org/en/main/man-openmpi/man3/MPI_Send.3.html>

## Exercises

### Exercise 1

Given multiple messages/sources/tags and exact/wildcard receives, derive all eligible matches, guaranteed orders, possible outcomes, and the status fields required for safe continuation.

### Exercise 2

Design a bounded variable-length protocol with versioned header, matched probe or exact-source receive, quotas, datatype/count validation, digest, response, error, and termination states.

### Exercise 3

Analyze a four-rank blocking-send ring under eager and rendezvous behavior, construct its wait-for graph, and redesign it three ways without relying on buffering.

### Exercise 4

Specify buffer/request ownership for a nonblocking bidirectional halo exchange, including zero neighbors, derived datatypes, wait/test choices, thread behavior, cancellation, and failure.

### Exercise 5

A regulated genomic pipeline uses wildcard work distribution and variable payloads. Specify identity, ordering, numeric, privacy, flow-control, failure/commit, performance, and human-review evidence.

## Answers to the Exercises

### Answer 1

Match only same communicator context/destination with source and tag satisfying the receive patterns. Exact `(s,t)` has one protocol class; wildcard source permits any eligible source and status source must bind processing/response; wildcard tag requires status tag dispatch validation. Successive single-threaded sends from one source to one destination that both match the same receive pattern are nonovertaking, but cross-source order, different patterns, logically concurrent threads, wait-any, and cancellations can vary. Enumerate inbox/posting interleavings rather than assuming arrival order. Validate status source/tag, cancellation, and count; then check sequence/generation in the payload header. If different eligible choices change output, the protocol is nondeterministic and needs ordering/arbitration or an explicit nondeterministic contract.

### Answer 2

Use a dedicated communicator and matched probe for allowed data tags, inspect status source/tag, query count, reject sizes beyond per-message/per-peer/global quotas, allocate from a bounded pool, then matched-receive. Header contains magic/version/kind/run/stream/generation/object/schema/count/bytes/digest/flags. Validate signature, checked byte arithmetic, generation/state and authorization before payload effect; verify digest/schema afterward. Maintain K credits per sender and return credit only after buffer release/commit. Response/ack names source and generation. Error messages are bounded and do not allocate based on attacker input. Draining stops admission, consumes/acknowledges prior generations, exchanges termination confirmation, and releases communicator only after requests complete. Define timeout/job-abort or supported recovery.

### Answer 3

If each rank k standard-sends to `(k+1) mod 4` before receiving from `(k-1) mod 4`, rendezvous can make each send wait for a receive that occurs after the next blocked send: a four-edge cycle. Eager buffering may hide it only below resource thresholds. Redesign (1) post all `Irecv`, post `Isend`, then wait-all; (2) use `MPI_Sendrecv` with predecessor/successor; (3) even ranks send then receive while odd receive then send (check wrap/parity for topology). Synchronous-send stress should still pass. Include buffer disjointness, tags/generation, completion, boundary peers, errors, and P variations.

### Answer 4

Create committed row/column/face datatypes with valid extents and keep them live. Post `Irecv` into disjoint ghost regions for each real neighbor; `MPI_PROC_NULL` may simplify missing boundaries with defined no-op status/buffer behavior. Post sends from immutable owned boundary regions. Keep request array with direction/generation and complete with wait-all when all halos are needed, or test/wait-some only if computation consumes a completed direction safely. No thread touches protected regions; if multiple threads call MPI, provided thread level/order covers them. Complete requests before datatype/buffer/communicator release. Protocol cancellation must drain/complete and inspect status; on MPI error do not trust partial ghosts unless explicitly supported—abort/recover by policy.

### Answer 5

Use stable run/sample/read/reference/coordinate/task/generation identities independent of worker rank; status source plus header binds wildcard result. Define exact integer and floating/reduction/statistical semantics, output ownership/order, duplicates, retries, and model/reference versions. Bound headers/payloads, counts, allocations, per-worker credits, outstanding requests, queue ages, and starvation; authenticate/authorize message kinds if trust boundary exists. Encrypt/minimize genomic data, isolate communicators/jobs/pools, prevent padding/log/dump leakage, audit access, retain/erase. Validate exact/wildcard schedules, variable/extreme sizes, P/threads/transports, synchronous threshold stress, duplicate/delayed messages, worker exit, timeout, cancellation, retry/deduplication, and commit. Measure complete queue/message/end-to-end distributions, bytes, in-flight high water, fairness, correctness, and failure. Named genomics, bioinformatics/statistics, clinical/laboratory where applicable, numerical, MPI/runtime, security/privacy, operations/SRE, quality/regulatory, human-factors, and independent validation reviewers approve validity, bias, limitations, and residual risk. Message correctness alone establishes no biological or clinical validity.
