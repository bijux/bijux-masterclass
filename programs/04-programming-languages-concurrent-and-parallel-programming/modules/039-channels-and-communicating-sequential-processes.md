---
module_id: CONPAR-039
program: Programming Languages: Concurrent & Parallel Programming
level: 1
module_number: 39
title: Channels and Communicating Sequential Processes
status: complete
last_verified: 2026-08-29
---

# Channels and Communicating Sequential Processes

## One-Page Review

### Governing question

How can sequential processes coordinate through typed channel events while keeping ownership, synchronization, buffering, choice, close, cancellation, deadlock, and termination semantics explicit?

### Essential definitions

- A **channel** is a communication endpoint/protocol carrying values between concurrent owners.
- **Send** offers or transfers a value; **receive** obtains it under language-specific synchronization rules.
- A **rendezvous/unbuffered channel** completes send and receive together when both parties are ready.
- A **buffered channel** permits send to complete while capacity exists before a receiver accepts the value.
- **Communicating Sequential Processes (CSP)** models processes that interact through named communication events and operators such as sequential prefix, choice, parallel composition, and hiding.
- **External choice/select** waits for one of several communication events and commits to a ready alternative.
- **Channel close/disconnect** is lifecycle state indicating some future operation is impossible; exact send/receive behavior varies.
- **Endpoint topology** is SPSC, MPSC, SPMC, MPMC, broadcast, watch/latest-value, or another declared relation.
- **Backpressure** makes producer progress depend on downstream capacity/demand.
- **Cancellation safety** states what happens to a pending channel operation and its value when abandoned.

### Central model, mechanism, or theorem

An unbuffered channel event synchronizes sender and receiver and transfers a value at one linearization point. A capacity-`K` buffered channel instead has state `(queue, send_open, receive_open)` with `0<=|queue|<=K`; send can enqueue when space exists and receive can dequeue when data exists. Buffering changes timing and reachable states but not the need for a protocol. Parallel processes terminate only when every wait has a matching event, cancellation/close alternative, or bounded recovery path.

### Critical invariants

Successful send transfers or copies value ownership exactly as declared. Channel state never exceeds capacity. Enqueue/dequeue linearization and memory-publication edges follow the API contract. One component owns close; repeated/competing close is defined. Receivers distinguish value, empty-now, drained-and-closed, timeout, and failure. Every sender clone/producer is accounted for before disconnect can prove completion. Select has a fairness/default policy and no duplicate operation registration. Cancellation returns/disposes unsent values correctly. No lock/permit needed by the peer is held during blocking channel operations. Shutdown closes sources, drains/rejects intentionally, and joins all processes.

### Common failures

Code uses an unbounded channel as architecture; assumes buffered send means processing; closes from receivers while senders remain; retains a sender clone and blocks shutdown; reads a zero/default value after close as real data; adds `default` to select and busy-spins; assumes select is fair; holds a lock while blocking send; creates a full-work/full-result cycle; cancels send after the value committed and retries it; treats broadcast as work distribution; or uses closure as both normal completion and fault without a typed cause.

### Compact example

A capacity-two channel accepts 10 and 20; sending 30 would block. Receiving 10 frees one slot, so 30 can enqueue. After the sole sender closes, receivers still drain 20 and 30; only then does receive report closed-and-empty. Thus close is not “the queue is empty,” send acceptance is not processing, and capacity bounds queued count—not payload bytes, producer-side inputs, or downstream effects.

### Connections

[Message Passing and Ownership Transfer](009-message-passing-and-ownership-transfer.md) supplies value ownership; [Actor Mailboxes and Message Ordering](038-actor-mailboxes-and-message-ordering.md) contrasts addressed mailboxes. The [program roadmap](../ROADMAP.md) next develops backpressure across pipelines.

## Governing Question

How should engineers choose and compose channel semantics so communication events establish the intended synchronization without hiding buffer growth, wait cycles, unfair selection, value loss, or nonterminating endpoint ownership?

A channel is a protocol edge, not merely a concurrent container.

## Why This Matters

Channels appear in Go, Rust, Kotlin, Clojure core.async, CSP/occam families, async runtimes, thread pools, pipelines, and hardware-style process networks. They can replace shared mutation with explicit value flow and make producer-consumer boundaries visible.

The surface word “channel” covers different contracts. Go channels are typed, may be buffered/unbuffered, support close and select, and closed receive has language-defined two-result behavior. Rust standard `mpsc` has multiple producers and one receiver, with unbounded and synchronous variants. Tokio async channels define distinct MPSC, broadcast, watch, and oneshot semantics. Kotlin channels have coroutine-specific send/receive/close/cancel rules. CSP algebra abstracts communication events more cleanly than any one library.

Correct use starts with event, topology, capacity, endpoint ownership, lifecycle, and failure—not with a familiar API call.

## Prerequisites and Retrieval

Retrieve:

- deadlock/progress from [Deadlock, Livelock, and Starvation](006-deadlock-livelock-and-starvation.md);
- ownership from [Message Passing and Ownership Transfer](009-message-passing-and-ownership-transfer.md);
- condition waiting from [Condition Variables and Predicate Waiting](013-condition-variables-and-predicate-waiting.md);
- resource capacity from [Semaphores and Resource Counting](014-semaphores-and-resource-counting.md);
- queue contracts from [Thread-Safe Queues](017-thread-safe-queues.md);
- cancellation cuts from [Cancellation and Timeouts](036-cancellation-and-timeouts.md); and
- actor-mailbox contrasts from [Actor Mailboxes and Message Ordering](038-actor-mailboxes-and-message-ordering.md).

Retrieval prompt: draw every channel endpoint owner and, for each blocked send/receive, the exact event or lifecycle transition that can release it.

## Learning Objectives

After completing this module, a learner can:

1. explain CSP process/event composition without confusing it with one library;
2. compare rendezvous, bounded, and unbounded channels;
3. specify ownership and memory-publication consequences of send/receive;
4. choose endpoint topology and distinguish queue, broadcast, watch, and oneshot;
5. define close, drain, disconnect, and typed failure semantics;
6. reason about select readiness, nondeterminism, fairness, and cancellation;
7. detect channel wait cycles and topology deadlocks;
8. preserve deterministic output despite nondeterministic receive order;
9. prove shutdown by accounting for endpoints, queued values, and joined processes; and
10. test channel protocols with controlled schedules rather than sleeps.

## Core Exposition

### CSP as a model of events

Hoare's CSP describes sequential processes interacting through communication events. In compact notation, `a -> P` performs event `a` then behaves as process `P`; choice offers alternatives; parallel composition synchronizes on shared events; hiding makes internal events unobservable. Traces record possible visible event sequences; failures/divergences add refusal and nontermination reasoning.

This algebra helps ask whether a protocol can deadlock, refuse an event, or produce an invalid trace. A practical Go/Rust channel program adds memory, buffers, cancellation, failures, payload ownership, scheduler behavior, and dynamic topology. CSP intuition informs design but does not substitute for the concrete API contract.

### Rendezvous communication

On a zero-capacity channel, send and receive meet. Neither completes alone. The event can establish both ownership transfer and synchronization. It naturally applies backpressure and minimizes queued storage.

Rendezvous couples availability: a producer cannot proceed until a consumer is ready. Cycles of processes each trying to send first deadlock. Latency-sensitive producers may need buffering or an alternative/cancellation branch. A rendezvous does not mean receiver has finished processing—only that the handoff completed.

Some APIs call capacity zero “unbuffered”; verify because others interpret zero as a special default or illegal capacity.

### Buffered communication

A capacity-`K` channel decouples sender and receiver by up to `K` queued values. Send linearizes on enqueue (or direct handoff), receive on dequeue. Capacity smooths bursts and permits pipeline overlap but introduces queueing latency and additional schedules.

Capacity is a correctness policy: maximum queued ownership obligations, not just tuning. Count does not bound bytes if messages vary. Producer input, in-flight processing, results, retries, and external buffers remain separate.

Large buffers delay backpressure and can make cancellation/shutdown drain stale work. Unbounded channels are safe only when total accepted messages/payload are bounded elsewhere and proved.

### Ownership and memory visibility

In ownership languages, successful send moves `T`; failed send may return it. In shared-memory languages, a reference may be copied, so mutable aliases can still race. Prefer immutable data or ownership transfer. Handles inside a message can retain shared state.

Channel synchronization commonly establishes a happens-before/publication relationship under the language specification, but its scope differs. It does not make unrelated shared state race-free. The sender must finish initialization before send; receiver becomes responsible for value cleanup after receive.

If cancellation races a send, determine whether ownership remained with sender, entered queue, or reached receiver. An API that cannot return the value may require idempotent external ownership.

### Endpoint topology

SPSC has one sender and receiver. MPSC merges producers; receive order across producers is scheduler-dependent. SPMC distributes values among receivers, not to all. MPMC combines both. Broadcast gives each subscriber a copy/reference and needs lag policy. Watch/latest-value coalesces state. Oneshot carries one terminal value.

Do not substitute one topology by cloning endpoints unless the API supports the intended semantics. A cloned receiver often means competing consumers; it does not broadcast. A cloned sender can keep the channel open after the coordinator believes production ended.

Draw endpoint ownership, cloning authority, and who may create further endpoints.

### Close, disconnect, and drain

Close means no future sends through some/all endpoints under the API. Buffered values may remain receivable. A receiver needs to distinguish temporary empty from drained-and-closed. Go's comma-ok receive provides this distinction; iterating a channel stops after close/drain. Sending to a closed Go channel panics, while other libraries return an error.

Who closes matters. Usually the owner that knows no more values will be produced closes the sending side. With many producers, a coordinator counts/joins producers and closes after all finish. An arbitrary receiver closing while producers race can lose work or trigger failure.

Disconnect caused by dropped endpoints can mean normal completion, cancellation, panic, or forgotten ownership. Carry a typed terminal/fault message or out-of-band result when cause matters. Closure alone has low diagnostic bandwidth.

### Selection and external choice

Select waits on several channel operations and commits to one ready alternative. If multiple are ready, the language/runtime chooses by a specified or intentionally nondeterministic policy. Go specifies pseudo-random uniform selection among ready communications; other libraries rotate, bias, or leave fairness unspecified.

Never depend on a favored branch unless priority is encoded explicitly. A default branch makes selection nonblocking; in a loop it can busy-spin and starve peer work. Add blocking, a timer, scheduler yield, or redesign.

Selection registration must be atomic enough to avoid lost readiness and ensure losing alternatives are withdrawn. Otherwise one message can be consumed by an abandoned branch. Cancellation safety is per operation/runtime.

### Fairness and starvation

FIFO wait queues, random ready selection, and scheduler fairness are distinct. A channel can preserve value FIFO while one receiver repeatedly wins. An always-ready high-rate input can starve a rare control input if selection is biased.

Use explicit rotation, quotas, priorities with aging, or separate control flow when required. Document fairness strength and test long-run/tail behavior, but do not turn statistical observation into a proof.

Ordering across MPSC senders is partial unless the channel linearization produces an observable total enqueue order; even then, the application may not know it beforehand. Stable IDs allow deterministic final assembly without serializing processing.

### Deadlock as a wait graph

For every blocking send/receive, draw an edge to the process/event that enables it. A cycle with no alternative/close/cancellation edge is deadlock. Common examples:

- A sends to B while B sends to A on rendezvous channels;
- coordinator fills work queue while workers fill result queue that only coordinator drains;
- sender holds a lock needed by receiver during full-channel send;
- parent waits to join child before closing channel child waits to drain; and
- pipeline downstream exits early but upstream keeps sending.

Increasing buffer capacity may postpone rather than eliminate the cycle. Repair topology and ownership: drain concurrently, close/cancel upstream, avoid locks across blocking send, separate collector, or add a correctly owned alternative.

### Cancellation safety

A pending receive that is cancelled should not silently consume a value unless the API documents recovery. A pending send may retain the value, enqueue it, or hand it off just as cancellation wins. Select implementations need reservations/commit protocols.

Tokio documents cancellation safety for individual methods; Go select chooses a communication before executing branch body. Read the exact API. If a command might have committed, use identity/deduplication rather than retrying blindly.

Cancellation also affects wait-queue fairness: removing a waiter can lose its position. This is acceptable only when policy says so. On shutdown, cancellation must wake blocked senders/receivers or close endpoints so they can terminate.

### Typed channel protocols

A channel of arbitrary strings or nullable values hides lifecycle. Use a sum type: Data(payload), Completed(summary), Failed(cause), Cancelled(reason), perhaps with version and sequence. However, sending one Stop per worker is fragile if counts change or Stop sits behind unbounded work.

Channel closure can represent “no more data,” while a separate joined producer result explains success/failure. Or one terminal message can travel through a single-producer stream. Ensure exactly one terminal authority and specify whether queued data precedes terminal.

Session types refine this idea: endpoint types encode legal sequences, such as send Request then receive Reply or Cancel. Linear endpoints can prove some protocol misuse absent, though dynamic failure, timeouts, and external effects still need handling.

### Fan-in, fan-out, and deterministic results

Fan-in merges channels; it must close output only after every input producer ends, and must propagate cancellation upstream when consumer stops. Receive order across inputs is nondeterministic. Attach source/index/sequence.

Fan-out can distribute each item to one worker (work queue), partition by key, or copy to all (broadcast). These are different semantics. Work queues need retry/ownership if a worker dies after receive. Broadcast needs per-subscriber lag/drop policy.

For batches, store terminal results in source-indexed slots and validate exactly one per accepted item. Completion events may remain completion-ordered for live observation.

### Pipelines and backpressure

In a linear bounded pipeline, a slow downstream fills its input, blocks the previous stage, and eventually slows the source. This is useful backpressure if every stage's wait and cancellation path is correct.

Hidden unbounded buffers break propagation. Multiple branches can deadlock if a stage sends outputs sequentially and one consumer stops. Define whether fan-out requires all subscribers, any, or drop/lag. The next module develops quantitative pipeline backpressure.

Capacity planning includes queue count/bytes, active work, output buffers, and maximum retained graph. Avoid holding permits across a channel wait unless the topology proves progress.

### Distributed channels are protocols

An in-process channel's shared runtime can provide atomic enqueue and memory ordering. A network queue faces partitions, duplication, persistence, broker acknowledgement, consumer redelivery, and independent clocks. Do not apply local close or rendezvous semantics to a socket/broker without protocol evidence.

Distributed “channel” APIs need message identity, durability level, ordering partition, acknowledgement/commit semantics, retention, rebalance, poison handling, and recovery. Exactly-once effect remains an application/storage protocol.

### Shutdown proof

A finite channel system shutdown typically:

1. stops admission;
2. signals cancellation where required;
3. drops/closes every producer endpoint after accepted sends;
4. lets receivers drain or explicitly discard under policy;
5. closes downstream channels after upstream producers join;
6. records all terminal outcomes and unsent/abandoned values;
7. joins every sender/receiver process; and
8. verifies no endpoint, queued value, permit, or task remains owned ambiguously.

Order follows data dependencies. Closing results before workers finish loses outcomes; retaining a coordinator sender clone prevents result receivers from detecting completion.

### Observability and testing

Record channel identity/type/topology/capacity, endpoint owner/clones, send wait/commit/fail, receive wait/commit, queue depth/bytes/age, select alternatives/winner, close cause, discarded values, and join. Instrumentation must not consume or reorder messages.

Deterministic tests control readiness and capacity. Exercise zero/full/one-slot, concurrent producers, multiple ready selects, default, cancellation at reservation/commit, close with queued data, retained clone, receiver exit, panic, wait cycles, late values, and shutdown. Use barriers and model schedules, not sleeps.

## Definitions and Notation

For capacity `K`, queue state `Q` satisfies `0<=|Q|<=K`. Successful buffered send increments occupancy unless it rendezvous-delivers; receive decrements occupancy unless direct handoff occurs.

For item identity `i`, let `S_i` indicate successful transfer commitment and `R_i` successful receive. Under reliable in-process ownership and complete drain, `sum S_i = sum R_i`; cancellation/discard/failure requires additional terminal categories rather than silently violating accounting.

Process wait graph `G=(P,E)` has edge `p->q` when process `p` can progress only through an action owned by `q`. A cycle is a deadlock candidate; proving deadlock also excludes ready alternatives, close, timeout, and external progress.

For a rendezvous event `c.v`, sender and receiver synchronize at one communication transition. Buffered enqueue and dequeue are separate transitions; therefore buffer size changes observable traces.

## Mechanisms, Invariants, or Proof Structure

Audit a channel system in this order:

1. name channel semantics, topology, capacity units, and endpoint cloning authority;
2. define send/receive linearization, ownership transfer, and memory visibility;
3. distinguish rendezvous, enqueue acceptance, processing, effect, and acknowledgement;
4. define empty/full/closed/disconnected/failed outcomes without sentinel ambiguity;
5. assign one close authority and account for every endpoint clone;
6. state selection readiness, tie, default, fairness, and cancellation rules;
7. draw wait graph including locks, permits, results, cancellation, and close edges;
8. define unsent, queued, received, in-flight, discarded, and terminal value ownership;
9. bound queues by count/bytes plus producer, worker, result, and retry state;
10. encode protocol states, identity, sequencing, failure, and deduplication;
11. stop admission, propagate cancellation, close in dependency order, drain/discard, and join; and
12. test every capacity/lifecycle race with controlled schedules.

The executable model demonstrates capacity-two enqueue, would-block, receive-created capacity, close, drain, and final closed-and-empty state.

<!-- bijux-verify: {"id":"bounded-channel-lifecycle-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"send_results=['accepted', 'accepted', 'would_block', 'accepted']\nreceived=[10, 20, 30]\nmax_depth=2\nclosed_after_drain=True\nsum_received=60\naccepted=3\nremaining=0\n","stderr":""}} -->
```python
capacity = 2
queue = []
send_open = True
send_results = []
received = []
max_depth = 0

def send(value):
    global max_depth
    if not send_open:
        return "closed"
    if len(queue) >= capacity:
        return "would_block"
    queue.append(value)
    if len(queue) > max_depth:
        max_depth = len(queue)
    return "accepted"

def receive():
    if queue:
        value = queue[0]
        queue[:] = queue[1:]
        return value
    return "closed" if not send_open else "empty"

send_results.append(send(10))
send_results.append(send(20))
send_results.append(send(30))
received.append(receive())
send_results.append(send(30))
send_open = False
received.append(receive())
received.append(receive())
closed_after_drain = receive() == "closed"

print(f"send_results={send_results}")
print(f"received={received}")
print(f"max_depth={max_depth}")
print(f"closed_after_drain={closed_after_drain}")
print(f"sum_received={sum(received)}")
print(f"accepted={send_results.count('accepted')}")
print(f"remaining={len(queue)}")
```

Limitations: this single-thread teaching queue returns would-block instead of suspending and stipulates FIFO. It does not model threads, atomics, memory ordering, wakeups, rendezvous, selection, fairness, cancellation races, failures, endpoint clones, typed causes, payload ownership, networks, or real resource cleanup.

## Alternatives and Trade-Offs

**Shared state with locks** supports direct multi-party mutation but requires explicit invariant and wait protocols.

**Rendezvous channel** gives immediate synchronization/backpressure with no queue, at tighter availability coupling.

**Bounded channel** permits controlled decoupling and backpressure, with wait-cycle and queue-latency risk.

**Unbounded channel** simplifies send and avoids producer blocking but needs an independently proven total bound.

**Work queue** distributes each value to one consumer. **Broadcast** sends to all. **Watch/latest** coalesces. **Oneshot** carries one outcome.

**Select/external choice** composes alternative events but introduces nondeterminism/fairness and cancellation-reservation complexity.

**Typed terminal messages** carry causes and can be ordered with data; **close plus joined producer result** separates stream exhaustion from failure.

**Channel pipeline** makes flow visible; **actor mailbox** ties messages to one state authority; **structured task return** can be simpler for fixed child results.

## Failure Modes and Misconceptions

- “Channel means CSP.” Libraries implement concrete subsets/extensions with different failure semantics.
- “Unbuffered means asynchronous.” Rendezvous couples sender and receiver synchronously at the event.
- “Buffered send means processed.” It usually means enqueued or handed off.
- “Capacity K bounds memory.” Payloads and other buffers also matter.
- “Cloning a receiver broadcasts.” It commonly creates competing consumers.
- “Close means empty.” Buffered values may remain.
- “Disconnect proves success.” Panic, cancellation, and dropped endpoints can also disconnect.
- “Select is fair.” Tie policy is runtime-specific and often weak.
- “Default prevents deadlock.” It can create busy-spin/livelock.
- “A bigger buffer fixes deadlock.” It can postpone the same wait cycle.
- “Cancellation before branch body means no send.” Communication may already have committed.
- “Channel transfer makes all contained state exclusive.” Shared handles inside payload remain shared.
- “One Stop message closes all workers.” Counts/topology and queued order matter.
- “Local channel rules apply to brokers.” Distributed durability/delivery need separate protocols.

## Worked Examples

### Example 1

An unbuffered request channel makes producer and server rendezvous. Send completion proves server accepted ownership of the request value, not that processing or durable commit completed. A separate reply/acknowledgement defines those later events.

### Example 2

A capacity-two queue accepts values 10 and 20. Third send blocks. Receiver removes 10, allowing 30. Closing the only sender prevents future sends but receiver drains 20 and 30 before closed-and-empty. Treating close as immediate emptiness would lose accepted work.

### Example 3

Coordinator fills bounded work channel while workers fill bounded results; coordinator does not receive until submission ends. Both sides wait. Drain results concurrently, use a dedicated collector, or use an unbounded result channel only under a proven finite batch-result bound.

### Example 4

A sender holds configuration mutex while blocking on full channel; receiver needs the mutex before receiving. Move/copy the message and release lock before send. Increasing capacity masks the cycle until a larger burst.

### Example 5

Two select branches are ready. Code assumes cancellation branch always wins, but runtime chooses data. Encode priority through an explicit preliminary nonblocking cancellation check plus correctly owned race policy, while still handling cancellation after data commitment.

### Example 6

Three producer clones finish but a coordinator retains the original sender. Receiver waits forever for disconnect. Draw every clone owner; close/drop the coordinator endpoint once spawning completes, then join producers and drain.

### Example 7

A work item is received and worker crashes before result. Channel ownership removed it from queue. At-least-once processing needs an acknowledgement/lease queue that reclaims unacked items; simple in-memory receive is at-most-once transfer under crash.

### Example 8

A consumer stops after ten values but upstream remains blocked sending the eleventh. Early-return must cancel/close upstream and join producers, or drain intentionally. Dropping only the local receiver may wake senders with error, whose unsent values still need policy.

### Example 9

Results from four workers arrive nondeterministically. Each carries source index; coordinator writes one terminal slot per accepted item and renders source order after join. Deterministic reporting does not serialize execution or erase completion trace.

### Example 10

A reactor-protection pipeline uses bounded channels between sensors, voting, and trip actuation. A full queue, cancelled send, or unfair select can delay/drop a trip command. Software channel reasoning alone cannot establish required response or physical safe state. Named nuclear systems, instrumentation/control, real-time, functional-safety, cybersecurity, human-factors, operations, verification, and regulatory reviewers must approve architecture and evidence; this chapter cannot.

## Cross-Program Connections

- **Formal methods:** CSP traces, refusals, divergence, and refinement support protocol verification.
- **Operating systems:** blocking, wakeups, pipes, and scheduler fairness implement channel waits.
- **Distributed systems:** brokers add durability, redelivery, partition order, and rebalance.
- **Software architecture:** topology reveals ownership and backpressure boundaries.
- **Security:** bounded admission and payload validation resist resource exhaustion.
- **Data systems:** work acknowledgement and deduplication resemble queue transaction protocols.
- **Reliability:** close causes, poison work, retries, and shutdown need terminal accounting.
- **Performance:** capacity trades burst absorption against latency, memory, and stale work.

## References

1. C. A. R. Hoare. “Communicating Sequential Processes.” Communications of the ACM 21(8), 1978. <https://dl.acm.org/doi/10.1145/359576.359585>.
2. C. A. R. Hoare. “Communicating Sequential Processes.” Prentice Hall, 1985. <https://www.cs.cmu.edu/~crary/819-f09/Hoare78.pdf>.
3. Go Project. “The Go Programming Language Specification: Channel Types.” <https://go.dev/ref/spec#Channel_types>.
4. Go Project. “The Go Programming Language Specification: Select Statements.” <https://go.dev/ref/spec#Select_statements>.
5. Go Project. “Effective Go: Channels.” <https://go.dev/doc/effective_go#channels>.
6. Rust Project. “std::sync::mpsc.” <https://doc.rust-lang.org/std/sync/mpsc/>.
7. Rust Project. “The Rust Programming Language: Using Message Passing to Transfer Data Between Threads.” <https://doc.rust-lang.org/book/ch16-02-message-passing.html>.
8. Tokio Project. “tokio::sync::mpsc.” <https://docs.rs/tokio/latest/tokio/sync/mpsc/>.
9. Kotlin Foundation. “Channels.” <https://kotlinlang.org/docs/channels.html>.
10. Clojure Project. “core.async.” <https://clojure.github.io/core.async/>.

## Exercises

### Exercise 1

Compare rendezvous, capacity-three, and unbounded channels for ownership, blocking, buffering, and backpressure.

### Exercise 2

Draw and repair the deadlock where a coordinator fills work while workers fill results and only the coordinator receives results.

### Exercise 3

Specify close/disconnect for an MPSC stream with three producers, buffered data, typed producer failure, and one receiver.

### Exercise 4

Design a select loop over data, cancellation, and deadline. State tie/fairness, cancellation commitment, default behavior, and shutdown.

### Exercise 5

A train-braking controller uses a channel send return as proof that brakes applied. Diagnose the semantics and define human evidence required for production.

## Answers to the Exercises

### Answer 1

Rendezvous retains value at sender until receiver meets it and directly synchronizes both, so it has strongest immediate backpressure but tight coupling. Capacity-three transfers/enqueues up to three values before blocking; it bounds queued count and absorbs bursts, not bytes or processing. Unbounded send normally does not block for fixed capacity and can grow memory/latency unless total input is independently finite. All require endpoint/lifecycle rules; none makes receiver processing complete at send return.

### Answer 2

Edges are coordinator -> worker receive because work channel is full, and each worker -> coordinator receive because result channel is full; coordinator cannot drain while blocked sending. Repair by concurrently draining results during submission, using a dedicated joined collector, or choosing a result buffer proven to hold the finite maximum while still handling failures. Release locks/permits before blocking sends, stop admission on failure, close work after submission, drain terminal outcomes, close results after workers end, and join all.

### Answer 3

Assign one coordinator as close authority. Register each producer identity/handle before start; producers cannot close shared output independently. Each sends Data with stable sequence/index and returns a typed terminal result to coordinator. After all three join, coordinator sends/records aggregate failure if protocol uses terminal messages, then drops the final sender. Receiver drains buffered data and distinguishes empty-open from drained-disconnected. It combines stream exhaustion with joined producer results to classify normal success, cancellation, or failure and validates terminal accounting.

### Answer 4

Use a blocking select with data receive, cancellation signal, and deadline timer; define runtime tie behavior as nondeterministic unless an explicit priority layer is added. If data receive wins, ownership may already have transferred even if cancellation is observed next, so finish/dispose it under policy. No unconditional default loop; default is only for bounded opportunistic work followed by a real wait/yield. Remove timer/registrations, close/cancel upstream, drain/discard under declared rules, record late values, and join producers. Test all simultaneous-ready permutations with controlled time.

### Answer 5

Send return proves only the channel's handoff/enqueue event, not that the receiver processed the command, actuator accepted it, or physical braking occurred. The system needs command identity/sequence, authoritative processing acknowledgement, actuator-state sensing, stale/duplicate rules, bounded queue/select response, independent interlocks, fail-safe behavior, and recovery. Production evidence requires named railway systems, braking/controls, embedded/real-time, functional-safety, cybersecurity, human-factors, operations, verification, and regulatory reviewers; hazard/requirements traceability; hardware-in-the-loop, timing, saturation, fault-injection, environmental, and failover tests; applicable-standard assessment; and signed residual-risk acceptance. This chapter provides no authorization.
