---
module_id: CONPAR-038
program: Programming Languages: Concurrent & Parallel Programming
level: 1
module_number: 38
title: Actor Mailboxes and Message Ordering
status: complete
last_verified: 2026-08-29
---

# Actor Mailboxes and Message Ordering

## One-Page Review

### Governing question

When isolated state changes only through messages, which delivery, mailbox, processing, reentrancy, capacity, and failure guarantees are required for the actor's behavior to be correct and explainable?

### Essential definitions

- An **actor** owns private mutable state and reacts to messages, may send messages, and may create actors.
- An **actor reference/address** is a capability to send without direct state access.
- A **mailbox** stores messages accepted for an actor but not yet processed.
- **Enqueue order** is mailbox insertion order; **processing order** is handler selection order; **effect order** includes asynchronous/remote side effects.
- **Per-sender FIFO** preserves order from one sender to one receiver under stated lifetime/path assumptions.
- **Selective receive** chooses a matching message rather than necessarily the oldest message.
- **Turn/activation** is one interval in which an actor processes work with exclusive access to its state.
- **Actor reentrancy** allows another message/continuation to run while a prior async operation is suspended.
- A **dead letter** is a message that cannot be delivered to a live destination under runtime policy.
- **Delivery semantics** such as at-most-once or at-least-once describe transfer, not business-effect uniqueness.

### Central model, mechanism, or theorem

An actor transition is `(state, message) -> (new state, outgoing effects)` executed with exclusive actor-state authority for one turn. Correctness depends on a mailbox-selection relation, not a mythical total send order. Per-sender order constrains only comparable messages from the same sender/path. Messages from different senders are concurrent unless a sequencing authority establishes order. If handlers suspend reentrantly, state must be valid before suspension and revalidated on continuation.

### Critical invariants

Only the actor mutates its owned state. Every message has a schema/version and sender/operation identity. Delivery, enqueue, selection, processing, reply, and durable-effect order are distinguished. The stated ordering guarantee has an explicit scope and failure boundary. Duplicate/retry behavior is idempotent or deduplicated. Mailbox capacity and overload policy are finite. Long/blocked turns are prohibited or isolated. Async suspension preserves invariants under reentrancy. Failure/restart defines mailbox and state fate. Stop drains/rejects/dead-letters predictably. Observability never becomes a second ordering authority.

### Common failures

Code assumes a global order across senders; equates local send return with enqueue/delivery; treats actor isolation as transactionality across awaits; uses an unbounded mailbox; hides priority starvation; requeues/stashes indefinitely; processes duplicate commands twice; restarts state but replays an incompatible mailbox; blocks a dispatcher thread; shares a mutable payload; assumes supervision restores business state; loses replies after commit; or tests one observed schedule as a universal ordering guarantee.

### Compact example

Sender A issues A1 then A2; sender B issues B1 then B2. Per-sender FIFO requires A1 before A2 and B1 before B2, but permits interleavings A1,B1,A2,B2; B1,A1,B2,A2; or A1,A2,B1,B2. If business logic needs A2 after B1, one sequencer or acknowledgement dependency must establish it. Wall-clock call order on two threads does not.

### Connections

[Message Passing and Ownership Transfer](009-message-passing-and-ownership-transfer.md) supplies payload ownership; [Structured Concurrency](037-structured-concurrency.md) supplies lifecycle ownership. The [program roadmap](../ROADMAP.md) next studies channels and CSP.

## Governing Question

How should an actor protocol define message acceptance, ordering, processing, asynchronous continuation, overload, failure, and shutdown so isolation produces a correct state authority rather than a hidden queue of races?

Actors remove shared-state access; they do not remove distributed ordering or lifecycle design.

## Why This Matters

Actors are used in telecom systems, distributed services, UI/main actors, game entities, workflow engines, virtual actors, and embedded controllers. They localize mutation and often eliminate explicit locks inside one actor. Each message becomes a reviewable state transition.

The abstraction can invite overclaiming. A mailbox is not necessarily durable, bounded, FIFO, or exactly-once. Remote send can fail or duplicate under retry. Multiple senders have no natural total order. Selective receive and priority change processing order. An async handler can yield and permit another turn before its continuation. Restart can preserve, discard, or replay messages while state comes from memory, snapshot, or event log.

Production actor design therefore specifies the protocol at several layers: send initiation, transport acceptance, mailbox enqueue, selection, turn execution, durable commit, reply, supervision, and retirement.

## Prerequisites and Retrieval

Retrieve:

- concurrency/interleavings from [Concurrency, Parallelism, and Asynchrony](001-concurrency-parallelism-and-asynchrony.md);
- state-space reasoning from [Interleavings and State-Space Explosion](003-interleavings-and-state-space-explosion.md);
- ownership transfer from [Message Passing and Ownership Transfer](009-message-passing-and-ownership-transfer.md);
- bounded queues from [Thread-Safe Queues](017-thread-safe-queues.md);
- callback reentrancy from [Callbacks and Inversion of Control](032-callbacks-and-inversion-of-control.md);
- async suspension from [Async/Await State Machines](034-async-await-state-machines.md); and
- cancellation/lifecycle from [Structured Concurrency](037-structured-concurrency.md).

Retrieval prompt: for two messages, name the relation—same sender sequence, causality, mailbox arrival, priority, selected turn, or durable commit—that actually orders them.

## Learning Objectives

After completing this module, a learner can:

1. model an actor as isolated state plus message transitions;
2. distinguish send, enqueue, selection, processing, reply, and effect orders;
3. state per-sender FIFO without inventing a global total order;
4. analyze selective receive, priority mailboxes, stash, and reentrancy;
5. choose delivery/deduplication rules for commands and events;
6. bound mailboxes and connect overload to sender feedback;
7. separate supervision from state recovery and protocol correctness;
8. design request/reply, correlation, deadline, and late-reply behavior;
9. test actor schedules with deterministic mailbox control; and
10. define startup, passivation, migration, and shutdown message fate.

## Core Exposition

### The actor as state authority

An actor combines identity/address, private state, behavior, mailbox policy, execution context, and lifecycle. External code cannot mutate state directly; it sends typed messages. During one non-reentrant turn, the actor reads one selected message and commits a new valid state before another turn.

This replaces lock ownership with protocol ownership. It does not make an oversized actor, vague message union, or hidden global singleton modular. Partition actors by enduring state authority and invariant, not merely by class or endpoint.

Message payloads should be immutable, copied, serialized, or ownership-transferred. Passing a mutable object shared with the sender reintroduces data races behind an actor-shaped API.

### Six different orders

For message `m`, distinguish:

1. sender program order;
2. send/API acceptance order;
3. transport delivery order;
4. receiver mailbox enqueue order;
5. receiver selection/processing order; and
6. durable effect/reply observation order.

Only explicit contracts connect these. A local runtime can enqueue synchronously yet schedule later. A distributed transport can reconnect. A handler can start asynchronous I/O and process another message before the first effect completes. Replies can overtake each other.

Write statements such as “messages sent by actor A to live actor B through the same logical association are enqueued in sender order, barring documented system messages/failure.” Avoid “actors process messages in order” without scope.

### Per-sender FIFO and cross-sender concurrency

Per-sender FIFO creates a partial order. If A sends `a1 -> a2`, receiver must not process `a2` first under the guarantee. If B independently sends `b1`, no relation exists between `b1` and A's messages. Network delay and scheduler timing choose an allowed interleaving.

If a business rule needs total order, route commands through one sequencing authority, assign monotonically checked sequence numbers, or use a consensus/log service when distributed failure semantics require it. A central sequencer adds latency, bottleneck, availability, and failover rules.

Sender identity also needs definition across restart. A newly incarnated actor at the same logical address may have a new epoch; old sequence numbers/messages must not be mistaken for current traffic.

### Causality, sequence gaps, and barriers

Sequence numbers detect order only within a declared stream. When R expects sequence 8 after 7 but receives 9, policy must decide whether to buffer 9 under a finite gap window, request retransmission, reject it, or declare the sender epoch invalid. Waiting forever for 8 is an availability failure; processing 9 silently may violate state.

A causal chain can cross actors: A sends update to B; after B acknowledges committed version 12, A tells C to query version 12. The acknowledgement/version establishes an edge that wall-clock timestamps cannot. If C reads a replicated store lagging behind 12, the protocol must wait, route to an authority, or return not-yet-visible rather than claim causality implies immediate global visibility.

Barrier messages work only when ordered relative to the traffic they fence. A barrier from a different sender or transport association may overtake the target messages. Encode source, epoch, high-water sequence, and receiver acknowledgement explicitly.

### Mailbox selection policies

FIFO selects the oldest enqueued eligible message. Priority chooses by class and needs stability/aging to prevent starvation. Selective receive scans for a matching message, leaving older unmatched messages. Stash temporarily removes messages and later reinserts them under runtime-specific order.

These are observable semantics. Selective receive can make a later `ready` message run before an earlier `request`. Unbounded scanning makes cost grow with mailbox length. A stash can become another unbounded queue. Define capacity, match complexity, requeue order, starvation, and expiry.

System/control messages may use a separate mailbox or ordering channel. Do not infer their relationship to user messages without runtime documentation.

### Turn atomicity and reentrancy

Classic turn processing executes one message handler to completion before the next. Actor state is not concurrently mutated, so the handler can preserve invariants without locks.

With async actor methods, an await can split the turn. Some systems keep the actor unavailable; others permit reentrancy and process another message while suspended. The continuation resumes against potentially changed state.

Before await, commit a valid state such as FETCHING with operation ID/version. After resume, verify actor incarnation, request ID, version, and deadline before applying. Never retain assumptions such as “balance is still x” across a reentrant suspension. A non-reentrant actor avoids that interleaving but can suffer head-of-line blocking during slow I/O.

### Request/reply is a protocol

A request includes correlation ID, sender/reply capability, deadline, idempotency key if effects matter, and schema version. The caller owns a pending entry until reply, timeout, or cancellation. A timeout does not remove an already-enqueued request or roll back its effect.

The actor may receive cancellation/withdrawal as another ordered message. It can act only relative to its mailbox and commit state. A reply that arrives after caller timeout is late and must be observed/disposed. Reusing correlation IDs risks matching an old reply to a new request.

Avoid turning every message into synchronous-looking ask/response; cycles of actors awaiting one another can deadlock logically even though no mutex exists. One-way commands plus events/state queries can better expose the protocol.

### Delivery guarantees

At-most-once delivery may lose a message but avoids transport-induced duplicates. At-least-once retries until acknowledgement and can duplicate; receiver needs idempotency/deduplication. Exactly-once business effect requires stable identity, durable atomic deduplication with the effect, and recovery—it is not obtained from an actor mailbox label.

Delivery acknowledgement can mean accepted by transport, enqueued in volatile mailbox, durably logged, processed, or committed. Name it. Sender crash, receiver crash, partition, restart, and mailbox overflow each create different uncertainty.

Do not deduplicate forever in unbounded memory. Define key scope, sender/incarnation, retention, durable storage, and behavior after expiry.

### Bounded mailboxes and backpressure

An unbounded mailbox converts overload into memory growth and stale work. Bound count and often bytes/cost. Define overflow: reject sender, await capacity, drop newest/oldest, coalesce by key, dead-letter, or fail actor. Each changes semantics.

Local asynchronous send that always returns immediately cannot provide true upstream backpressure without an acknowledgement/credit protocol. Remote queues add more buffers. Track sender queue, transport, receiver mailbox, stash, in-flight effects, reply queue, and dead-letter retention.

Prioritize control/cancellation only with quotas; an attacker who can mark messages urgent can starve business work. Admission should authenticate authority and reserve capacity for lifecycle messages.

### Fairness and throughput

A dispatcher may process one or many messages per actor activation. Throughput batches reduce scheduling overhead but can let a hot actor monopolize a worker. Bound messages/time per activation and requeue. Mailbox priority and dispatcher fairness interact.

Long CPU handlers and blocking calls prevent other actors on the same dispatcher from running. Partition work, use bounded worker pools, or dedicate dispatchers for blocking APIs. The actor remains the state authority: workers return results tagged with operation/version, and the actor validates them.

One actor can be a scalability bottleneck. Sharding by stable state key increases concurrency but changes ordering: only messages for the same shard retain actor-local order. Cross-shard invariants need protocols, not shared assumptions.

### Failure and supervision

When a handler fails, distinguish domain rejection from defect/panic. Supervision can stop, restart, resume, or escalate an actor depending on runtime/policy. It does not reconstruct correct business state automatically.

Specify:

- whether the failing message is dropped, retried, dead-lettered, or durably recorded;
- whether queued messages survive restart;
- how state is reconstructed (initial, snapshot, event log, external authority);
- how child actors and watchers change;
- whether the reference points to a new incarnation; and
- how duplicates/old replies are fenced.

Restarting with empty state while keeping a mailbox built for previous state can violate invariants. Poison-message retry can form a crash loop; cap attempts and quarantine with evidence.

### Persistence and event-sourced actors

A persistent actor may validate a command, append an event durably, apply it to state, and emit replies/effects. The durable log order is the authoritative state order, not mailbox arrival alone. Reply-after-commit avoids acknowledging effects that recovery cannot reproduce.

External side effects need an outbox, idempotent effect processor, or another atomicity protocol. Crashing after log append but before sending can cause replay; crashing after send but before marking can duplicate. Actor serialization does not solve dual-write atomicity.

Snapshot/version migration must preserve event schema, deterministic replay assumptions, and actor incarnation. Corrupted or unknown events require quarantine/recovery policy, not silent skipping.

### Lifecycle: start, stop, passivation, migration

Actor creation can race with first messages; virtual actor systems may activate on demand. Define how duplicate activations are prevented or reconciled, how state loads before processing, and what happens to messages during migration/passivation.

Stopping should transition to CLOSING, reject or buffer new messages under policy, finish/cancel in-flight work, drain or dead-letter mailbox, close children/resources, and publish termination. A stop message ordered behind an unbounded queue is not prompt shutdown; a system signal may bypass user order but must define user-message fate.

Addresses can outlive incarnations. Include epoch/generation where stale commands would be unsafe. Dead letters are diagnostic outcomes, not guaranteed durable queues; bound their retention and avoid sensitive payload leakage.

### Protocol evolution and rolling upgrades

Mailboxes can retain old messages while a new actor version activates. Each message schema needs version and compatibility policy; unknown variants must be rejected, quarantined, or translated by an owned boundary. Do not deserialize unknown fields into unsafe defaults.

Rolling upgrades can route successive messages from one logical sender through different nodes or associations, weakening transport-specific ordering. Preserve sender epoch/sequence at the application protocol when order matters, and fence old actor incarnations before the new one commits. State snapshots, event handlers, dedup records, replies, and outbox entries must evolve together.

Compatibility tests enqueue old/new messages around activation, restart, migration, and partial rollout. They verify ordering, rejection, deduplication, state migration, reply shape, and rollback behavior. A runtime upgrade also requires checking documented mailbox, reentrancy, supervision, and remoting semantics rather than trusting unchanged API names.

### Observability and deterministic testing

Record actor logical ID and incarnation, message type/version, sender/epoch/sequence, correlation/idempotency key, enqueue/select/start/end/commit/reply times, mailbox depth/bytes/age, stash, duplicate decision, outcome, restart, and dead-letter reason. Sampling must not change ordering authority.

Deterministic tests drive a mailbox manually. Generate allowed interleavings from multiple senders, duplicate/drop/retry, selective receive, priorities, reentrant completion, stale continuation, overflow, crash/restart, passivation, and shutdown. Assert state invariants and specified partial orders, not a total order the contract does not provide.

## Definitions and Notation

For actor `R`, message `m` has sender `s(m)`, sender sequence `q(m)`, incarnation `e(m)`, enqueue time/order `enq(m)`, processing position `proc(m)`, and optional commit order `commit(m)`.

Per-sender FIFO states: for comparable messages `m1,m2` on the guaranteed path, if `s(m1)=s(m2)`, `e(m1)=e(m2)`, and `q(m1)<q(m2)`, then `proc(m1)<proc(m2)`. It says nothing about a message from another sender.

An actor transition is `delta(x,m)=(x',O)` for state `x`, new state `x'`, and outgoing intents `O`. Deterministic transition logic does not imply deterministic arrival order.

For mailbox capacity `K`, accepted queued messages satisfy `0<=|M|<=K`; in-flight/stashed/transport buffers require separate bounds. For deduplication identity `d`, applied effect count ideally satisfies `effects(d)<=1` within the declared retention/authority scope.

## Mechanisms, Invariants, or Proof Structure

Audit an actor protocol in this order:

1. name actor identity/incarnation, private state, reference, and state authority;
2. define immutable/owned message schema, sender identity, sequence, correlation, and deadline;
3. distinguish send, delivery, enqueue, selection, process, commit, reply, and observation order;
4. state exact per-sender/global/priority/selective ordering scope and failure boundary;
5. define non-reentrant or reentrant await semantics with version validation;
6. define at-most/at-least delivery, acknowledgement level, deduplication, and retention;
7. bound mailbox, stash, transport, effects, replies, and dead letters;
8. make overflow and sender feedback semantically explicit;
9. isolate blocking/CPU work while retaining actor commit authority;
10. define handler failure, supervision, restart state, message fate, and poison policy;
11. define durable log/outbox, activation/passivation, stale epochs, and shutdown; and
12. test partial orders and adversarial schedules with deterministic control.

The executable model uses FIFO mailbox arrival A1,B1,A2,B2. It checks per-sender sequence while applying serialized balance transitions.

<!-- bijux-verify: {"id":"actor-mailbox-order-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"processed=['A1:+5', 'B1:-2', 'A2:+3', 'B2:-1']\nper_sender_fifo=True\nfinal_balance=5\nmailbox_capacity=4\naccepted=4\nremaining=0\nturns=4\n","stderr":""}} -->
```python
mailbox = [
    ("A", 1, 5),
    ("B", 1, -2),
    ("A", 2, 3),
    ("B", 2, -1),
]
capacity = 4
accepted = len(mailbox)
last_sequence = {"A": 0, "B": 0}
ordered = True
processed = []
balance = 0

while mailbox:
    sender, sequence, change = mailbox[0]
    mailbox = mailbox[1:]
    if sequence != last_sequence[sender] + 1:
        ordered = False
    last_sequence[sender] = sequence
    balance += change
    processed.append(f"{sender}{sequence}:{change:+d}")

print(f"processed={processed}")
print(f"per_sender_fifo={ordered}")
print(f"final_balance={balance}")
print(f"mailbox_capacity={capacity}")
print(f"accepted={accepted}")
print(f"remaining={len(mailbox)}")
print(f"turns={len(processed)}")
```

Limitations: this finite single-thread FIFO model stipulates arrival and equal-cost turns. It has no multiple threads, transport, drops, duplicates, retries, selective receive, priorities, reentrancy, asynchronous effects, persistence, overflow, failure, supervision, restart, passivation, deadlines, or security boundaries.

## Alternatives and Trade-Offs

**Shared state plus locks** allows direct multi-object transactions but exposes interleavings and lock protocols.

**Actor isolation** serializes one authority and scales by partitioning. Cross-actor invariants become asynchronous protocols.

**Unbounded mailbox** makes send convenient but hides overload. **Bounded mailbox** makes capacity explicit but forces blocking/rejection/drop/coalescing policy.

**FIFO** is simple and starvation-resistant for one queue. **Priority/selective receive** improves responsiveness for control work but changes order and can starve/scan.

**Non-reentrant turns** simplify state reasoning but slow unrelated messages during I/O. **Reentrant actors** improve utilization but require state/version checks after suspension.

**At-most-once** limits duplicate transport work but can lose commands. **At-least-once** improves eventual delivery at duplicate cost. Durable effect uniqueness needs application identity.

**Persistent actors** improve recovery and auditability, with serialization, migration, replay, storage, and dual-write complexity.

**One actor per key** localizes order. Coarse actors bottleneck; fine actors make cross-key coordination more complex.

## Failure Modes and Misconceptions

- “Actors process messages globally FIFO.” Ordering is usually partial and scoped.
- “Send returned, so receiver accepted.” API return may mean only local handoff.
- “Per-sender FIFO survives every restart/path change.” Incarnation and transport assumptions matter.
- “Actor state cannot race.” Reentrant continuations can observe intervening turns.
- “No locks means no deadlock.” Request/reply cycles and full bounded mailboxes can deadlock.
- “Mailbox delivery is exactly-once effect.” Deduplication and commit atomicity are separate.
- “Supervision restores business state.” Restart policy needs authoritative recovery.
- “Priority handles emergencies safely.” Unlimited urgent traffic starves ordinary and cleanup work.
- “Unbounded mailbox preserves availability.” It converts overload to memory/latency failure.
- “Dead letters are durable recovery.” They are runtime-specific diagnostics unless explicitly persisted.
- “Reply order follows request order.” Async effects can complete differently.
- “Sharding preserves all actor order.” Only per-shard state remains serialized.
- “Immutable message type guarantees valid authority.” Sender capability and validation still matter.
- “One successful trace proves ordering.” Tests must cover every allowed interleaving.

## Worked Examples

### Example 1

A sends increment 1 then increment 2 to counter R; B sends read independently. Per-sender FIFO orders A's increments but the read may occur before, between, or after them. If B requires both applied, B needs an acknowledgement/version barrier from R, not synchronized wall-clock calls.

### Example 2

A priority mailbox always chooses urgent health checks while an attacker floods them. Payment commands starve. Authenticate priority authority, cap urgent bursts, age ordinary messages, reserve lifecycle capacity, and measure oldest-message age by class.

### Example 3

Selective receive waits for `ready` and skips 10,000 earlier data messages. Matching becomes linear and data starves. Separate protocol phase/mailbox, bound stash, reject impossible data before readiness, or encode state at the sender; document chosen order.

### Example 4

A reentrant account actor stores balance 100, awaits fraud scoring, and later subtracts 80. Another withdrawal commits during await. Continuation cannot reuse 100; it validates operation/version and re-evaluates or reserves funds before suspension.

### Example 5

A caller times out after sending `charge`. The actor later commits and replies to a closed correlation entry. Stable idempotency/status recovery prevents retry duplication; a late-reply sink records/disposes response. Mailbox cancellation after charge cannot imply rollback.

### Example 6

An at-least-once transport delivers command ID 7 twice after lost acknowledgement. Actor atomically records ID 7 with its state transition and replays the stored response. An in-memory “seen” set lost on restart would not protect a durable effect.

### Example 7

A handler offloads compression to a worker. While it runs, actor processes new config. Worker result includes config generation; actor discards/recomputes stale output. Letting the worker mutate actor state would break single authority.

### Example 8

Actor crashes on malformed message. Restart retains the mailbox and retries the same head forever. Validate at admission/handler boundary, cap attempts, quarantine with bounded redacted evidence, restore state from authority, and continue/escalate under policy.

### Example 9

Event-sourced actor appends `OrderAccepted` then crashes before publishing downstream. Recovery replays state, while a transactional outbox emits the event once under deduplication. Sending directly before append risks an effect absent from recovered state; after append without outbox risks omission/duplication.

### Example 10

A railway interlocking actor receives route commands from two control stations. Actor serialization alone does not define which concurrent command is authoritative or prove physical track state. Protocol needs authenticated authority, command epochs/sequences, conflict rules, independent sensing/interlocks, bounded mailbox/control priority, fail-safe state, and verified restart. Named signalling, rail operations, controls, real-time, functional-safety, cybersecurity, human-factors, verification, and regulatory reviewers must approve evidence; this chapter cannot.

## Cross-Program Connections

- **Programming-language semantics:** actors combine capabilities, effects, isolation, and partial-order semantics.
- **Distributed systems:** remoting introduces partitions, incarnation, deduplication, and causal order.
- **Databases:** persistent actors need logs, snapshots, idempotency, and outbox atomicity.
- **Security:** actor references are capabilities; message schema and priority require authorization.
- **Reliability:** supervision, dead letters, poison handling, and recovery are lifecycle policies.
- **Performance:** mailbox age, batching, sharding, and dispatcher isolation control latency/throughput.
- **Software architecture:** actor boundaries should align with state authority and invariant ownership.
- **Safety engineering:** serialized commands do not replace independent physical interlocks.

## References

1. Carl Hewitt, Peter Bishop, and Richard Steiger. “A Universal Modular ACTOR Formalism for Artificial Intelligence.” IJCAI, 1973. <https://www.ijcai.org/Proceedings/73/Papers/027B.pdf>.
2. Gul Agha. “Actors: A Model of Concurrent Computation in Distributed Systems.” MIT Press, 1986. <https://dspace.mit.edu/handle/1721.1/6952>.
3. Ericsson. “Erlang Reference Manual: Processes and Signal Ordering.” <https://www.erlang.org/doc/system/ref_man_processes.html#signals>.
4. Ericsson. “Erlang Reference Manual: Expressions — Receive.” <https://www.erlang.org/doc/system/expressions.html#receive>.
5. Akka Project. “Message Delivery Reliability.” <https://doc.akka.io/libraries/akka-core/current/general/message-delivery-reliability.html>.
6. Akka Project. “Mailboxes.” <https://doc.akka.io/libraries/akka-core/current/mailboxes.html>.
7. Akka Project. “Supervision and Monitoring.” <https://doc.akka.io/libraries/akka-core/current/general/supervision.html>.
8. Swift Project. “SE-0306: Actors.” <https://github.com/swiftlang/swift-evolution/blob/main/proposals/0306-actors.md>.
9. Microsoft. “Orleans: Request Scheduling.” <https://learn.microsoft.com/en-us/dotnet/orleans/implementation/scheduler>.
10. Pony Project. “Actor Model.” <https://tutorial.ponylang.io/types/actors.html>.

## Exercises

### Exercise 1

Two senders A and B each send messages 1 then 2 to actor R. Enumerate the ordering constraints and three valid global processing orders.

### Exercise 2

An actor awaits remote I/O reentrantly. Define the state/version protocol needed to reject a stale continuation.

### Exercise 3

Design a bounded mailbox for commands, queries, and lifecycle messages. Specify priority authority, overflow, sender feedback, fairness, and shutdown.

### Exercise 4

Specify at-least-once command processing for a persistent actor across crash/restart, including idempotency, reply replay, event log, and outbox.

### Exercise 5

An electrical-grid actor serializes breaker commands from two operators and is claimed safe because “actors process one message at a time.” Diagnose the claim and define human review evidence.

## Answers to the Exercises

### Answer 1

Required partial orders are A1 before A2 and B1 before B2, assuming the runtime's per-sender guarantee and same incarnations/path. No cross-sender edge exists. Valid orders include A1,A2,B1,B2; A1,B1,A2,B2; and B1,A1,B2,A2. Invalid examples place A2 before A1 or B2 before B1. A required cross-sender order needs acknowledgement, sequencer, causal token, or stronger protocol.

### Answer 2

Before await, move state to an explicit pending phase with stable operation ID, input snapshot, actor incarnation, and expected state/config version; reserve resources if required. Let other turns maintain valid invariants. On continuation, compare incarnation, operation still pending, version, deadline, cancellation, and worker-result generation. Apply once, recompute, discard, or compensate according to policy. Remove the pending entry and release leases on every result/error/cancel/restart path.

### Answer 3

Set count/byte bounds per class and globally. Only authenticated runtime/owner paths can label lifecycle traffic. Reserve a small lifecycle quota, cap its burst, and age commands/queries to prevent starvation. Commands normally reject/await capacity rather than drop silently; coalescible queries may replace older same-key entries. Sender receives typed accepted/rejected/deadline feedback. Metrics expose class depth/age/drops. Closing rejects new user work, admits bounded stop control, drains/cancels under deadline, and dead-letters/redacts residuals under policy.

### Answer 4

Each command carries durable idempotency key, sender/incarnation, sequence, fingerprint, and reply correlation. In one storage transaction, validate ordering, append event/state change, store dedup key and canonical result, and enqueue an outbox record. After commit, reply/outbox delivery may retry; duplicates return the stored compatible result and conflicting fingerprints are rejected. Recovery replays/migrates events, rebuilds dedup state, resumes outbox, fences old incarnation, and never re-applies committed command. Retention/expiry and status recovery are explicit.

### Answer 5

Serialization chooses some mailbox order; it does not authenticate operator authority, resolve concurrent command precedence, prove remote delivery, or establish physical breaker state. The system needs command epochs/sequences, role and conflict policy, interlocks, independent telemetry, acknowledgement/commit identity, stale/duplicate rejection, bounded priority/capacity, fail-safe behavior, and recovery. Production evidence requires named grid operations, protection/power-systems, controls/SCADA, real-time, functional-safety, cybersecurity, human-factors, verification, and regulatory reviewers; hazard/requirements traceability; hardware-in-the-loop, timing, fault-injection, communications, and failover tests; applicable-standard assessment; and signed residual-risk acceptance. This chapter provides no grid authorization.
