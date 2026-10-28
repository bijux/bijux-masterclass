---
module_id: CONPAR-009
program: Programming Languages: Concurrent & Parallel Programming
level: 1
module_number: 9
title: Message Passing and Ownership Transfer
status: complete
last_verified: 2026-08-29
---

# Message Passing and Ownership Transfer

## One-Page Review

### Governing question

When a value crosses a concurrency boundary, is it copied, immutably shared, or exclusively transferred, and what channel protocol proves that exactly the intended participant may mutate, consume, close, retry, or discard it?

### Essential definitions

- A **message** is an immutable logical value communicated between participants; its physical representation may be copied, moved, serialized, or referenced.
- **Message passing** coordinates participants through send and receive operations rather than unsynchronized access to shared mutable representation.
- **Ownership** is the authority and obligation to use, mutate, release, or transfer a resource according to its protocol.
- **Ownership transfer** moves exclusive authority from sender to channel or receiver; successful transfer makes continued sender use invalid.
- **Copy semantics** create an independent value; **immutable sharing** permits aliases that cannot mutate the shared value; **shared mutable aliasing** retains a synchronization obligation.
- A **channel** is a communication endpoint with specified capacity, ordering, blocking, close, and failure semantics.
- A **rendezvous channel** completes communication only when sender and receiver synchronize; a **buffered channel** decouples them up to capacity.
- **Backpressure** makes downstream capacity constrain upstream admission rather than allowing unbounded accumulation.
- A **protocol state machine** defines legal message sequences, roles, terminal states, and error transitions.
- **Linear or affine use** restricts a resource to exactly once or at most once, respectively; practical type systems vary.
- A **capability** is an unforgeable authority conveyed by possession of a reference, endpoint, or token.
- A **delivery guarantee** describes the communication mechanism, not automatically the end-to-end business effect.

### Central model, mechanism, or theorem

For transferable resource (r), define authority locations Sender, InTransit, Receiver, and Terminal. The conservation invariant is:

(owners(r) + in_flight(r) = 1) before terminal consumption, and both are zero afterward.

A successful send is a linearization point that removes sender authority and installs channel or receiver authority according to the API. A failed send retains or returns authority. The receiver may assume initialization visibility only when the channel specification supplies the required synchronization. If the payload contains mutable aliases governed elsewhere, moving the outer handle does not transfer exclusive ownership of those referents.

### Critical invariants

Every message has a schema and stable identity where retry matters. Copy, immutable share, and exclusive move are distinguished. A successful send has one defined ownership outcome; failure never loses ambiguous authority. Sender mutation stops after transfer. Receiver validation precedes use. Queue capacity is finite or explicitly justified. Ordering is stated per sender, channel, key, or globally. Close has one owner and a terminal receive rule. Cancellation accounts for buffered items. External effects use idempotency or deduplication when redelivery is possible. Memory visibility follows the actual channel contract.

### Common failures

Teams send a pointer and call it ownership transfer while the sender retains aliases; mutate a buffer immediately after enqueue; assume FIFO across multiple producers; use an unbounded mailbox as load control; treat a successful local send as proof of processing; close while producers can still send; encode termination with a poison value that collides with data or reaches only one consumer; drop buffered resources on cancellation; retry after an ambiguous send without identity; or equate “message passing” with absence of shared memory.

### Compact example

A producer constructs a mutable buffer, transfers it through a move-aware channel, and the consumer becomes its sole owner. Before successful send, the producer must clean up on failure. After successful send, the producer cannot read or modify the buffer. The consumer may mutate and eventually release it. If instead both endpoints retain references to the same backing array, the channel transferred only a reference value and the array still needs immutability or synchronization.

### Connections

[Critical Sections and Shared-State Invariants](008-critical-sections-and-shared-state-invariants.md) covers shared-memory authority; [Race Conditions and Atomicity Violations](005-race-conditions-and-atomicity-violations.md) supplies transfer linearization; [Deadlock, Livelock, and Starvation](006-deadlock-livelock-and-starvation.md) supplies bounded-capacity dependencies. The [program roadmap](../ROADMAP.md) next chooses models by workload, then develops threads, mutexes, conditions, queues, asynchronous runtimes, actors, and CSP-style channels.

## Governing Question

How can engineers replace implicit shared-state coordination with explicit communication while proving payload authority, ordering, capacity, visibility, failure, and lifecycle behavior from producer creation through terminal consumption?

Message passing is not automatically safer than locks. It makes a boundary visible and can turn ownership into a protocol, but correctness depends on the payload's aliasing, the channel's exact semantics, and end-to-end handling of failure and effects.

## Why This Matters

Concurrency becomes easier to reason about when one participant owns mutable state and others request transitions through messages. The owner serializes decisions, invariants live in one place, and callers do not coordinate with its internal locks. Pipelines can transfer buffers from stage to stage, keeping one mutable owner while parallelizing across items. Actors can isolate state behind mailboxes. Channels can establish both communication and memory-order edges.

Yet the phrase “send a message” hides materially different mechanisms. An in-process queue may copy only a pointer. A language move may statically prevent later sender use. A distributed transport serializes bytes but can redeliver after retry. A rendezvous blocks until a receiver participates. An asynchronous unbounded queue reports success after local admission even if the consumer later disappears. The public protocol must state which one applies.

Capacity is part of correctness. Unbounded queues convert overload into latency and memory exhaustion. Bounded queues exert backpressure but can participate in deadlock when producers hold resources needed by consumers. Dropping policies preserve availability by changing delivery semantics. Coalescing preserves only the latest state for suitably replaceable messages. There is no neutral queue-full behavior.

Ownership also includes cleanup. A file descriptor, GPU buffer, transaction handle, or pooled connection has a release obligation. During transfer, failure must leave exactly one component responsible. Ambiguous authority leaks or double-frees resources. For ordinary garbage-collected values, logical ownership still matters because aliases can violate state invariants.

## Prerequisites and Retrieval

Retrieve:

- atomicity, linearization, retry, and idempotency from [Race Conditions and Atomicity Violations](005-race-conditions-and-atomicity-violations.md);
- safety, progress, fairness, and terminal outcomes from [Safety, Liveness, and Progress](004-safety-liveness-and-progress.md);
- bounded queues, wait-for dependencies, close, and cancellation completeness from [Deadlock, Livelock, and Starvation](006-deadlock-livelock-and-starvation.md);
- abstraction functions, invariant ownership, alias escape, and open calls from [Critical Sections and Shared-State Invariants](008-critical-sections-and-shared-state-invariants.md);
- deterministic ordering and canonical identity from [Determinism and Reproducibility](007-determinism-and-reproducibility.md);
- finite-state machines, sequences, partial orders, and conservation proofs; and
- practical familiarity with pointers, resource cleanup, serialization, and error values.

Retrieval prompt: draw states ProducerOwned, InTransit, ConsumerOwned, and Released. Add successful send, failed send, receive, cancellation, and cleanup transitions. For each transition, name exactly who must release the resource if execution stops immediately afterward.

## Learning Objectives

After completing this module, a learner can:

1. distinguish value copy, immutable sharing, reference passing, and exclusive ownership transfer;
2. define channel capacity, ordering, synchronization, blocking, close, and failure contracts;
3. prove an exactly-one-authority conservation invariant across send and receive;
4. identify mutable aliases that invalidate apparent ownership isolation;
5. design bounded pipelines with explicit backpressure and overload policy;
6. specify protocol state machines, message identities, terminal states, and version handling;
7. separate transport admission and delivery from end-to-end effect guarantees;
8. test ownership, close, retry, cancellation, and ordering with bounded evidence; and
9. identify safety-critical protocols requiring named authorized review.

## Core Exposition

### Model logical values separately from physical transport

A logical message is a value in a protocol. Its physical carrier may be:

- copied bytes with independent storage;
- an immutable shared object;
- a moved resource whose old binding becomes unusable;
- a reference to mutable shared state;
- a serialized network frame; or
- a capability granting access to another owner.

Do not infer semantics from syntax such as `send(x)`. Ask whether the channel copies `x`, consumes it, borrows it until completion, or stores an alias. Ask when the call returns and what return means. Ask who cleans up on every error.

Copying gives independent top-level storage but may be shallow. A copied record can retain pointers to shared children. Immutable sharing scales when the complete reachable graph is immutable or internally synchronized. Exclusive move is strongest for mutable resources because it makes authority conservation explicit. Reference passing is legitimate when the reference is a capability to an owner or when another protocol protects its referent; it is not isolation by itself.

### Ownership is authority plus obligation

Ownership answers two questions: who may act, and who must clean up? For resource (r), define a unique authority state. Initially producer owns it. Before send linearizes, producer may mutate and must release on failure. At a successful transfer point, producer authority ends. The channel holds in-flight responsibility or the receiver owns immediately, depending on the abstraction. Receive installs receiver authority. Terminal consumption or release ends the obligation.

Prove conservation. Let indicators (P,C,Q) represent producer ownership, consumer ownership, and in-flight channel custody. Before release, require (P+C+Q=1). Every transition preserves the sum:

- create: (0,0,0) to (1,0,0);
- successful enqueue: (1,0,0) to (0,0,1);
- receive: (0,0,1) to (0,1,0);
- failed enqueue: state remains (1,0,0), possibly through an error that returns the payload;
- cancel buffered item: (0,0,1) to a named cleanup owner, then terminal; and
- consume/release: (0,1,0) to terminal.

If an API returns success but the receiver may disconnect immediately, success proves admission under that API, not eventual receive. Rust's current standard `mpsc::Sender::send` documentation, for example, states that an error returns the value because it cannot be received, while success does not guarantee future receipt. Treat such documented details as contract, not folklore.

Linear and affine type systems can enforce parts of conservation statically. Rust's move semantics often prevent use of a non-`Copy` value after transfer into `send`, and `Send` bounds which types can cross thread boundaries safely. Unsafe code, interior mutability, reference-counted aliases, foreign resources, and application protocol still require review. Type safety is powerful evidence, not a universal end-to-end effect proof.

### Channels combine data and synchronization

Channel operations may establish memory visibility. The Go memory model states that a send is synchronized before completion of its corresponding receive. Java SE 26 `BlockingQueue` states that actions before placing an object happen-before actions after another thread accesses or removes it. These are specific guarantees; an arbitrary queue or network client may differ.

Visibility does not grant exclusivity. If producer and consumer retain mutable aliases, a happens-before edge publishes prior writes but does not order later concurrent mutation. Ownership transfer or another synchronization discipline must govern the payload after receive.

Rendezvous channels have zero capacity. Send and receive pair, often making handoff timing explicit. Buffered channels permit up to (K) admitted messages and decouple producer and consumer. With capacity (K), occupancy invariant is (0 <= q <= K); enqueue requires space and dequeue requires an item. The buffer becomes an owner in the resource proof.

An “unbounded” channel is bounded by memory, allocator behavior, quotas, and process survival. If production rate (lambda) persistently exceeds service rate (mu), backlog grows. Short bursts require a capacity based on burst size and acceptable latency, not wishful averages.

### Ordering must name a scope

FIFO can mean order of successful sends on one endpoint, order from each producer, order of channel linearization, or global causal order. Multiple producers can interleave. Multiple consumers can distribute messages so completion order differs from receive order. Priority and delay queues are intentionally not insertion FIFO.

State the order needed by the domain. Per-key sequence numbers permit independent parallel keys while detecting gaps and duplicates. A single global sequencer provides total order at a scalability and availability cost. If operations commute, the protocol may accept reordering and compare by a partial order or final state.

Do not attach sequence at processing completion if it is meant to describe admission. Define wraparound, persistence across restart, producer identity, and epoch changes. A sequence number detects anomalies only when its allocation and trust model are correct.

### Protocols are state machines, not bags of structs

Define roles, message variants, correlation IDs, legal sequences, timeouts, retries, and terminal outcomes. A request/reply protocol might be:

Pending -> Accepted -> Succeeded | Failed | Cancelled.

Every accepted request reaches exactly one terminal accounting state, even if replies are retried. Invalid transitions are rejected explicitly. Unknown message versions are not interpreted approximately. Duplicate terminal messages are deduplicated by stable operation identity or processed idempotently.

Separate control from data. Closing a channel is a state transition meaning no future messages will be admitted under a stated ownership rule. End-of-stream should not collide with a valid payload. A poison message in a multi-consumer queue may stop only one consumer, can be reordered by priority, and consumes capacity. Prefer a native close protocol where available or specify one control message per consumer with coordinated producers.

Java's `BlockingQueue` does not intrinsically define close; its documentation notes application-specific shutdown mechanisms such as poison objects. Go channels define close behavior. Rust `mpsc` receive termination depends on all senders being dropped. These different lifecycle models cannot be substituted without redesign.

### Backpressure and overload policy

A bounded send can block, fail immediately, time out, drop, overwrite, coalesce, or divert. Each is domain behavior:

- **block** preserves admission intent but propagates latency and creates dependency edges;
- **reject** preserves capacity and makes overload explicit to caller;
- **drop newest** protects queued work but loses recent updates;
- **drop oldest** favors freshness but invalidates FIFO history;
- **coalesce by key** is correct only when intermediate states are replaceable;
- **spill** moves pressure to durable storage with new capacity and recovery rules.

Never block while holding a resource the consumer needs. The wait-for graph includes sender -> channel capacity -> consumer -> retained resource. Reserve capacity before acquiring other resources, release before send, use nonblocking admission with rollback, or redesign ownership.

Backpressure crosses stages. Capacity at one queue does not bound the whole pipeline if upstream stages accumulate futures, retry buffers, or unacknowledged resources. Count items, bytes, expensive handles, and in-flight work. Establish one admission budget and terminal accounting.

### Delivery and business effects

“In memory, exactly once” may describe one dequeue. Across process failure, delivery systems commonly choose at-most-once or at-least-once behaviors. Exactly-once business effect needs an authoritative idempotency or transaction protocol connecting message identity with the effect.

A sender timeout can be ambiguous: the receiver may have accepted the request although the reply was lost. Retrying without the same idempotency key can duplicate an effect. Reusing a key for a different payload creates another defect. Bind key, operation, actor, scope, and result; persist the decision at the effect authority.

Acknowledgment semantics matter. Ack on receipt protects transport buffers but not processing. Ack after durable effect narrows loss but can redeliver after effect and before ack. Use an inbox, outbox, conditional write, or idempotent consumer as appropriate. This module does not relabel those mechanisms “exactly once” without proof.

### Cancellation, close, and resource drainage

Cancellation must decide what happens to queued and in-flight messages. Options include drain normally, reject new work and finish admitted work, cancel by identity, return ownership to sender, or dispose under channel ownership. Record terminal outcome exactly once.

Close ownership prevents send/close races. Common patterns are one producer closes, a coordinator waits for all producers, or reference-counted send endpoints close when the last endpoint disappears. A receiver discovering closure distinguishes clean end-of-stream from failure if the API supports it.

Drain resource-bearing payloads or transfer them to a cleanup owner. Dropping a queue object may free memory but not necessarily release external leases, temporary files, GPU allocations, or business reservations. Shutdown tests must cover full buffers, blocked senders, blocked receivers, duplicate cancellation, receiver failure, and late messages.

### Isolation boundaries and security

Messages should be immutable protocol values at the boundary. Validate schema, size, version, identity, authorization context, and capability scope before use. Treat deserialization as untrusted input across process or privilege boundaries.

Passing a capability can intentionally grant authority without exposing underlying state. Use least authority: a reply endpoint rather than a global broker, a scoped reservation token rather than database credentials. Revocation, expiry, delegation, and audit must be part of the capability protocol.

Do not serialize secrets into replay logs or dead-letter queues without explicit protection. Queue observability should record safe identifiers, sizes, states, ages, and error categories while respecting content sensitivity.

## Definitions and Notation

Let channel state be (Ch=(B,K,open)), where (B) is an ordered buffer and (K) capacity. Safety requires (0 <= |B| <= K). Send transition `send(m)` requires an open channel and available admission according to policy. Receive removes a message according to the ordering policy. Close makes future admission illegal and defines how receivers observe remaining (B).

For resource (r), let authority function (owner(r,s)) return Producer, Channel, Consumer, Cleanup, or None. Exclusive-ownership safety requires at most one non-None authority, plus exactly one before terminal release.

A message history contains `send_start`, `send_result`, `receive`, `ack`, effect, and terminal events. Ordering relation (prec) may be per-producer, per-key, channel-linearization, causal, or total; name it.

Delivery is **at-most-once** when an identified message is processed no more than once, possibly zero; **at-least-once** when it is retried until processed under assumptions, possibly multiple times. “Exactly once” requires both existence and uniqueness at the claimed boundary and failure model.

## Mechanisms, Invariants, or Proof Structure

Use this workflow:

1. **Define the logical protocol.** Roles, variants, identity, ordering, and terminal states come first.
2. **Classify payload semantics.** Deep copy, immutable share, exclusive move, or synchronized alias.
3. **Locate transfer linearization.** State authority before success, after success, and after every failure.
4. **Specify the channel.** Capacity, admission, ordering, visibility, blocking, fairness, close, and disconnect.
5. **Prove conservation.** Exactly one owner or cleanup obligation exists until terminal release.
6. **Bound overload.** Count items, bytes, handles, retries, and in-flight effects across the pipeline.
7. **Design failure.** Handle ambiguous send, redelivery, consumer crash, close race, cancellation, and poison data.
8. **Connect effects.** Bind identity to idempotency, inbox/outbox, or transactional authority.
9. **Validate the boundary.** Schema, version, authorization, capability, size, and sensitive data.
10. **Test adversarially.** Force full/empty queues, disconnects, duplicates, reorderings, shutdown, and cleanup.

Maintain these invariants:

- a payload's physical alias semantics match the claimed ownership model;
- successful transfer ends sender mutation authority;
- every error leaves one known cleanup owner;
- capacity and in-flight work remain within declared budgets;
- ordering claims identify their exact scope;
- close prevents later admission and defines buffer drainage;
- every accepted operation reaches one terminal accounting state;
- retries reuse identity only for the same logical operation;
- channel synchronization claims come from the actual API; and
- bounded tests do not imply universal delivery or effect guarantees.

## Alternatives and Trade-Offs

**Deep copy** provides isolation and simple lifetime at bandwidth and allocation cost. **Immutable sharing** avoids copying but requires transitively immutable data or synchronized internals. **Exclusive move** supports zero-copy mutation but constrains APIs and failure return paths.

**Rendezvous** supplies direct synchronization and zero queue backlog, while coupling participant availability. **Bounded buffering** absorbs bursts and exposes capacity policy. **Unbounded buffering** simplifies sends but makes memory and latency the hidden limit.

**One owner/actor** centralizes invariants and ordering. It can bottleneck, needs mailbox backpressure, and must recover owner state. **Sharded owners** scale by key but require routing, rebalancing, and a protocol for cross-shard operations.

**Typed protocols** reject invalid variants and can encode state transitions. Dynamic or versioned envelopes ease evolution but shift checks to runtime. **Capabilities** grant narrow authority but require revocation and lifecycle design.

**At-most-once delivery** avoids duplicate processing but may lose work. **At-least-once delivery** resists loss but requires idempotent effects. A transactional inbox/outbox strengthens coordination at storage and operational cost.

## Failure Modes and Misconceptions

- **“Messages eliminate shared state.”** Queues, payload referents, allocators, services, and owners still contain state.
- **“Sending a reference transfers ownership.”** The sender may retain aliases unless language or protocol prevents it.
- **“FIFO means global order.”** Define producer, channel, key, receive, and completion order separately.
- **“Send success means processed.”** It may mean only local admission.
- **“A seed or sequence number prevents duplicates.”** Identity enables detection; authoritative state must enforce the effect.
- **“Unbounded means nonblocking.”** Allocation, memory pressure, and receiver loss remain.
- **“A poison pill closes the queue.”** Multiple consumers, full buffers, priority, and valid-data collision complicate it.
- **“Drop on shutdown releases everything.”** Payloads may own external resources or reservations.
- **“Channels make deadlock impossible.”** Bounded capacity and rendezvous create wait-for dependencies.
- **“Exactly once is a transport option.”** End-to-end existence and uniqueness require a failure-scoped proof.
- **“Types prove the business protocol.”** They may prove movement and variants, not external effects or authorization.
- **“A passing pipeline test proves ordering.”** It covers observed schedules and one implementation only.

## Worked Examples

### Example 1

**Question:** A sender enqueues a mutable list and immediately appends to it while the receiver iterates.

**Reasoning:** The queue copied a reference, not the reachable list. Both participants retain mutable aliases.

**Conclusion:** Deep-copy, freeze, move exclusive ownership, or synchronize the referent.

### Example 2

**Question:** A move-aware send fails because the receiver disconnected and returns the payload.

**Reasoning:** Transfer did not complete, so returning the value restores one known cleanup owner.

**Conclusion:** The sender may retry or release; it must not assume channel custody.

### Example 3

**Question:** Two producers send FIFO streams A1,A2 and B1,B2 to one channel.

**Reasoning:** Per-producer order may be preserved while A and B interleave in several ways.

**Conclusion:** Do not claim one global order unless the channel linearization contract supplies it.

### Example 4

**Question:** A bounded queue is full while the producer holds a database connection needed by the consumer.

**Reasoning:** Producer waits for capacity, capacity waits for consumer, and consumer waits for the retained connection.

**Conclusion:** This is a capacity deadlock; release/reorder resources or redesign admission.

### Example 5

**Question:** A service times out after sending a debit command and retries with a new ID.

**Reasoning:** The first command may have committed although its reply was lost. A new identity defeats deduplication.

**Conclusion:** Retry the same logical operation identity and query/replay the authoritative result.

### Example 6

**Question:** One poison message is inserted for four consumers.

**Reasoning:** At most one consumer necessarily receives it; forwarding can race with failure and ordering.

**Conclusion:** Use an explicit coordinated close or a fully specified multi-consumer termination protocol.

### Example 7

**Question:** Does a channel's happens-before guarantee make later sender writes safe?

**Reasoning:** It publishes writes sequenced before send to the matching receive. It does not order later concurrent access to an aliased payload.

**Conclusion:** Visibility is not exclusive ownership.

### Example 8

**Question:** What does this ownership state-machine enumeration establish?

<!-- bijux-verify: {"id":"exclusive-transfer-state-machine","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"candidate_orders=24\naccepted_orders=1\nrejected_orders=23\naccepted_invariant_violations=0\n","stderr":""}} -->
```python
actions = ["create", "send", "receive", "release"]
orders = []

def arrange(prefix, remaining):
    if not remaining:
        orders.append(prefix)
        return
    for index in range(len(remaining)):
        arrange(prefix + [remaining[index]], remaining[:index] + remaining[index + 1:])

arrange([], actions)
accepted = 0
violations = 0

for order in orders:
    owner = "none"
    valid = True
    for action in order:
        expected = {
            "create": "none",
            "send": "producer",
            "receive": "channel",
            "release": "consumer",
        }[action]
        replacement = {
            "create": "producer",
            "send": "channel",
            "receive": "consumer",
            "release": "none",
        }[action]
        if owner != expected:
            valid = False
            break
        owner = replacement
    if valid:
        accepted += 1
        if owner != "none":
            violations += 1

print(f"candidate_orders={len(orders)}")
print(f"accepted_orders={accepted}")
print(f"rejected_orders={len(orders) - accepted}")
print(f"accepted_invariant_violations={violations}")
```

**Conclusion:** Guards accept the one legal four-action order and reject 23 permutations. This finite model does not prove a language move system, queue, cleanup action, external resource, or production protocol correct.

### Example 9

**Question:** A close rejects new sends but silently drops three queued GPU buffers.

**Reasoning:** Admission lifecycle is correct, but resource conservation has no cleanup transition.

**Conclusion:** Drain, return, or dispose every buffered resource under a named owner.

### Example 10

**Question:** May this protocol alone approve message handoff between flight-control components?

**Reasoning:** Timing, hardware faults, partitioning, redundancy, stale commands, certification, and physical hazards exceed the state machine.

**Conclusion:** No. Named authorized avionics safety, systems, verification, and regulatory reviewers must approve the real protocol. No external review is claimed.

## Cross-Program Connections

- **Programming languages:** affine types, borrowing, effects, and memory models can enforce transfer and visibility properties.
- **Operating systems:** pipes, sockets, shared-memory queues, handles, and scheduler blocking define transport behavior.
- **Distributed systems:** acknowledgments, redelivery, partitions, epochs, and durable logs extend the failure model.
- **Databases:** inbox/outbox tables, unique constraints, and conditional transactions connect messages to effects.
- **Security:** capabilities, schema validation, deserialization, least authority, and sensitive queue retention protect boundaries.
- **Cloud engineering:** brokers, autoscaling, dead-letter policies, quotas, and observability operationalize backpressure.
- **Formal methods:** session types, communicating automata, refinement, and model checking verify protocol sequences.

## References

1. C. A. R. Hoare, “Communicating Sequential Processes,” *Communications of the ACM* 21(8), 1978, [doi:10.1145/359576.359585](https://doi.org/10.1145/359576.359585).
2. Gilles Kahn, “The Semantics of a Simple Language for Parallel Programming,” in *Information Processing 74*, North-Holland, 1974, [scan](https://www.cs.cmu.edu/~crary/819-f09/Kahn74.pdf).
3. Carl Hewitt, Peter Bishop, and Richard Steiger, “A Universal Modular ACTOR Formalism for Artificial Intelligence,” *IJCAI 1973*, [proceedings](https://www.ijcai.org/Proceedings/73/Papers/027B.pdf).
4. Robin Milner, *Communicating and Mobile Systems: The Pi Calculus*, Cambridge University Press, 1999.
5. Simon J. Gay and Malcolm Hole, “Subtyping for Session Types in the Pi Calculus,” *Acta Informatica* 42, 2005, [doi:10.1007/s00236-005-0177-z](https://doi.org/10.1007/s00236-005-0177-z).
6. Maurice Herlihy et al., *The Art of Multiprocessor Programming*, second edition, Morgan Kaufmann, 2020.
7. Go Authors, “The Go Memory Model,” June 2022, [official documentation](https://go.dev/ref/mem) (retrieved 2026-08-29).
8. Rust Project, “`std::sync::mpsc::Sender`,” Rust 1.98 documentation, [official API](https://doc.rust-lang.org/std/sync/mpsc/struct.Sender.html) (retrieved 2026-08-29).
9. Oracle, “`BlockingQueue`,” Java SE 26 API, [official API](https://docs.oracle.com/en/java/javase/26/docs/api/java.base/java/util/concurrent/BlockingQueue.html) (retrieved 2026-08-29).
10. Tyler Akidau et al., “The Dataflow Model,” *VLDB 2015*, [doi:10.14778/2824032.2824076](https://doi.org/10.14778/2824032.2824076).

## Exercises

### Exercise 1

Model ownership of a pooled buffer through create, enqueue, dequeue, processing, cancellation, and release. State authority after every success and failure.

### Exercise 2

A three-stage pipeline has queue capacities 20 and 10, but stage one also holds 100 pending futures. Define a complete admission budget and backpressure policy.

### Exercise 3

Specify ordering for two producers and three consumers processing per-customer commands. Preserve per-customer order while allowing cross-customer parallelism.

### Exercise 4

Design shutdown for multiple producers, a bounded queue, and resource-bearing messages. Cover blocked sends, closure ownership, drainage, cancellation, and terminal accounting.

### Exercise 5

A medical-device gateway retries actuator commands after ambiguous timeouts. Identify what message identity and deduplication can establish and what requires named authorized review.

## Answers to the Exercises

### Answer 1

Creation installs producer ownership. Before enqueue success the producer releases on failure. Successful enqueue moves authority to the channel; sender access ends. Dequeue moves authority to the processor. Processing success or failure must release, return, or transfer to a cleanup owner. Cancellation before enqueue leaves producer authority; cancellation while buffered requires atomic removal and cleanup ownership; after dequeue it becomes a processor cancellation transition. Maintain exactly one authority until terminal release and test disconnect at each boundary.

### Answer 2

The queues alone permit 30 buffered items, but 100 futures create additional admitted work. Define one budget over queued items, active stage work, future payload bytes, scarce handles, and retry reservations. Acquire an admission token before stage one creates a future and release it only at success, failure, or cancellation. When exhausted, block without retained downstream resources, reject explicitly, or coalesce only replaceable work. Instrument occupancy, bytes, age, and terminal counts across every stage.

### Answer 3

Assign each customer to one logical shard owner using stable routing and attach per-customer epoch and sequence. One shard serializes that customer's commands; different shards run concurrently. Consumers may process several shards, but ownership of a shard is exclusive during an epoch. Rebalancing fences the old owner before advancing epoch. Reject gaps, deduplicate repeated sequence numbers by operation identity, and specify whether failed commands block later ones or create an explicit terminal result.

### Answer 4

Use a coordinator that stops admission, waits for every producer endpoint to finish or cancel, then closes once. Blocked sends wake with a defined error returning payload ownership. Receivers drain admitted work or the coordinator atomically transfers remaining messages to cleanup. Every buffer, lease, and reservation reaches succeeded, failed, cancelled, returned, or disposed exactly once. Test full queues, producer crash, receiver crash, repeated close, late send, and cancellation during dequeue. A poison value alone is insufficient for multiple consumers.

### Answer 5

Stable identity bound to exact command, device, authorization, and epoch lets an authoritative device or durable gateway return the previously committed result and reject key reuse with another payload. It can prevent duplicate logical effect within the proven storage and failure boundary. It cannot establish safe actuator timing, stale-command policy, physical state, device failover, dosage or motion limits, or clinical suitability. Named authorized medical-device safety, clinical, controls, cybersecurity, and regulatory reviewers must approve those claims and deployment. This chapter claims no external review.
