---
module_id: SEPAT-071
program: Software Engineering: Patterns
level: 2
module_number: 71
title: Reactor
status: complete
last_verified: 2026-08-29
---

# Reactor

## One-Page Review

### Governing question

How can one or a small number of threads demultiplex many concurrent I/O sources while preserving nonblocking progress, explicit state ownership, fairness, backpressure, cancellation safety, bounded latency, and failure isolation?

### Essential definitions

- A **Reactor** waits for readiness events from many registered handles and synchronously dispatches each event to its associated handler.
- A **handle** identifies an I/O or event source such as a socket, pipe, timer, signal source, or wakeup mechanism.
- A **synchronous event demultiplexer** blocks until one or more registered interests appear ready and returns a ready set.
- An **interest set** declares readiness categories the loop wants to observe; a **ready set** reports categories currently indicated by the demultiplexer.
- An **event handler** owns protocol/application state for a handle and performs bounded nonblocking work when dispatched.
- **readiness** is a hint that an operation may progress without blocking; it is not the completion of the operation and can become stale.
- **level-triggered** notification repeats while a readiness condition remains; **edge-triggered** notification reports transitions and normally requires draining nonblocking I/O until `would block`.
- **run-to-completion** means a callback executes cooperatively until it returns; it must not imply unbounded work.
- **loop lag** is delay between an event becoming actionable and its handler starting; it exposes blocking, overload, and unfairness.
- **handler generation** is a lifecycle token used to reject stale callbacks/worker completions after cancellation, close, or handle reuse.

### Central model, mechanism, or theorem

At iteration $t$, demultiplexer returns ready registrations $R_t\subseteq I_t$. Dispatcher invokes each corresponding handler with budget $b_i$. For a single loop with event arrival rate $\lambda$ and mean loop-thread service time $E[S]$, a necessary idealized stability condition is

$$
\rho=\lambda E[S]<1.
$$

This excludes kernel work, bursts, timers, retries, cross-thread commands, and offloaded completions; safe capacity requires headroom and measured tails. If a round visits $n$ continuously ready handlers once, a newly ready handler's cooperative scheduling delay is bounded approximately by

$$
W\le\sum_{i=1}^{n}b_i+C_{poll}+C_{dispatch},
$$

only when budgets are enforced, callbacks do not block, and the ready scheduler is fair. The bound fails if one callback performs unbounded parse, CPU, logging, DNS, file I/O, lock wait, or output flush.

### Critical invariants

- Every registered handle has one current owner, handler, interest set, generation, state machine, and close path.
- All operations performed on the reactor thread are nonblocking; `would block`, partial I/O, EOF, error, and readiness races are normal states.
- Each dispatch has byte/item/time/work budgets and requeues unfinished work fairly rather than monopolizing the loop.
- Edge-triggered handlers drain to `would block`; level-triggered handlers maintain interests so persistent readiness cannot create accidental busy loops.
- Read interest and accept admission are disabled or throttled when bounded input/output/downstream capacity is exhausted, then restored at a low watermark.
- CPU-bound, blocking, or unpredictable work is offloaded to bounded executors; completions return through an owned wakeup queue and validate generation/current state.
- Partial protocol state, output buffers, timers, cancellation, half-close, error, and cleanup are explicit; callbacks never assume a full message or full write.
- Close/unregister is idempotent and prevents stale events, file-descriptor reuse, or late completions from mutating a new connection.
- Callback failure is contained to the owning operation/connection unless policy explicitly escalates; loop invariants and cleanup remain intact.
- Loop lag, callback duration/budget, ready-queue age, buffer pressure, interest changes, offload saturation, errors, closes, and stale completions are observable.

### Common failures

Common failures include confusing readiness with completion, calling blocking APIs on the loop, reading only once under edge-triggering, always subscribing to write readiness, unbounded accept/read/parse/write loops, assuming one read equals one message, ignoring partial writes, allocating before frame limits, letting one hot connection starve timers, offloading to an unbounded pool, mutating loop-owned state from workers, accepting a late completion after close, relying only on descriptor number, nested event loops and reentrancy, uncaught callback exceptions, busy polling at zero timeout, using wall clock for durations, no high/low watermarks, logging synchronously during overload, and measuring throughput without loop-lag tails.

### Compact example

Two registrations are continuously ready: A has four units and B has three. A fair reactor gives each at most two units per round. Round one processes A2/B2 and requeues both; round two processes A2/B1. All seven units complete, B is not forced to wait for A's entire backlog, and the loop returns to polling between bounded rounds.

### Connections

[SEPAT-070](070-designing-an-integration-flow-from-message-semantics.md) supplies the I/O protocol contract; [SEPAT-072](../ROADMAP.md) contrasts readiness dispatch with completion-driven Proactor. Reactor also connects to [Operating Systems](../../22-operating-systems/ROADMAP.md), [Network Engineering](../../24-network-engineering/ROADMAP.md), [Security Engineering](../../25-security-engineering/ROADMAP.md), [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md), and [Platform Engineering](../../29-platform-engineering/ROADMAP.md).

## Governing Question

When thousands of connections may be idle or intermittently ready, how should a small thread set wait, dispatch, and advance each protocol without blocking on any one source or losing lifecycle control?

The Reactor separates event detection from event-specific handling. The operating system or runtime multiplexes readiness; the application associates each registration with a stateful handler. This reduces thread-per-connection overhead and gives one loop serialized ownership of connection state. It also makes every accidental blocking call and unbounded callback a shared-latency incident.

## Why This Matters

Network servers, proxies, brokers, UI loops, device gateways, and embedded systems often manage far more logical sessions than active CPU work. Readiness multiplexing lets idle sessions cost registrations and buffers rather than blocked threads. Serialized handler execution can remove many locks and make state transitions deterministic.

The trade is cooperative concurrency. A callback that waits 100 ms delays unrelated sockets and timers on that loop. A client that keeps a descriptor perpetually ready can monopolize dispatch. A close racing with an offloaded computation can corrupt a reused connection. Production Reactor design is therefore as much about budgets, ownership, pressure, and lifetime as about an I/O polling API.

## Prerequisites and Retrieval

You should understand sockets/file descriptors, nonblocking I/O, TCP byte streams, partial reads/writes, queues, state machines, thread ownership, memory visibility, backpressure, timers, cancellation, and capacity. Retrieve these facts:

1. TCP delivers an ordered byte stream, not application message boundaries.
2. A nonblocking read/write may transfer fewer bytes than requested or report `would block`; both are ordinary control flow.
3. Readiness can be stale because another operation, thread, signal, close, or kernel condition changes state before use.
4. A single-threaded loop serializes callbacks but does not make external systems or worker completions serialized automatically.
5. File-descriptor integers and object addresses can be reused after close; logical generation/identity must outlive raw handles.
6. Backpressure requires bounded queues/buffers and an upstream admission action, not only a metric.
7. Readiness-driven Reactor and completion-driven Proactor assign different responsibilities to handlers.

## Learning Objectives

After completing this module, you should be able to:

- identify Reactor participants and trace registration, selection, dispatch, I/O, rearm, cancellation, and close;
- distinguish readiness, operation attempt, progress, message completion, and business completion;
- implement incremental read/parse/write state under partial I/O and level/edge-triggered semantics;
- derive fairness budgets and explain how callback duration creates loop-wide tail latency;
- design input/output watermarks, admission, load shedding, and downstream backpressure;
- offload blocking/CPU work through bounded queues while preserving loop ownership and lifecycle generation;
- handle errors, half-close, cancellation, timers, wakeups, exceptions, shutdown, and descriptor reuse safely;
- compare one loop, loop-per-core, acceptor/worker, and thread-per-connection arrangements;
- instrument loop lag, callback work, interests, buffers, executor pressure, connection lifecycle, and failure cohorts;
- verify with deterministic models, real socket tests, partial/spurious readiness, slow clients, faults, load, security, and shutdown races.

## Core Exposition

### Identify the participants

The initiator creates a handler and registers a handle plus interest mask with the Reactor. The synchronous demultiplexer waits. When readiness is reported, the dispatcher resolves the current registration and invokes the handler. The handler attempts nonblocking work, updates protocol state and interests, schedules timers/offload, or closes.

The handler should own a protocol state machine, not merely a callback function. Association state includes buffers, parser state, output queue, deadlines, authentication, generation, peer metadata, pressure state, and cleanup obligations.

### Readiness is a hint, not a completed operation

Readable can mean bytes, EOF, pending error, or a listening socket with an accept candidate. Writable often means some buffer space, not that the whole response can be written. Between notification and operation, conditions can change; the call may still return `would block`.

Treat nonblocking result variants explicitly: progress with byte count, zero/EOF where defined, `would block`, interruption, reset/error, and resource exhaustion. Never turn a readiness hint into a blocking call “because it should be ready.”

### Model incremental protocol state

Accumulate bytes up to a declared bound, parse only complete headers/frames, validate lengths before allocation, and retain partial state. One read may contain half a frame, one frame, or several frames. Apply a per-dispatch byte/frame budget and keep excess for a later turn.

For writes, queue immutable response segments or owned buffers, advance offsets after partial progress, and subscribe to write readiness only while pending output remains. Close or half-close only after protocol obligations and buffered output policy are satisfied.

### Choose level versus edge triggering deliberately

Level-triggered readiness is easier: if data remains, the handle should be reported again. A bounded handler can stop before exhaustion and rely on another notification, though persistent readiness can spin if the handler makes no progress.

Edge-triggered readiness reports change and usually requires nonblocking operations until `would block`; stopping after one partial read can strand already available data without another edge. Even while draining, enforce a fairness budget: record the handle as locally ready and revisit it without waiting for a new kernel edge. One-shot modes require explicit rearm after state is consistent.

### Manage interest sets as state

Interest masks are control flow. Enable read when input capacity and protocol state permit; disable it at high watermark or while a serialized request is being processed. Enable write only with queued output; disable after draining. Always handle error/hangup semantics required by the platform even if not explicitly requested.

Batch interest changes when safe, but do not leave a window that loses required notification. Track desired versus installed interests and expose divergence. Cross-thread changes use the loop's command queue/wakeup, not unsynchronized direct mutation.

### Enforce cooperative fairness

Bound bytes, frames, accepts, writes, callbacks, and elapsed handler time per turn. Place unfinished local work at the tail of a fair ready queue. Reserve opportunities for timers, cross-thread completions, control commands, and shutdown. Priority can protect latency-critical control work but needs aging/quotas to avoid starvation.

Budgets are not free: very small quanta add dispatch/syscall overhead, while large quanta increase loop lag. Measure distributions under hot connections, not only uniform load. A fair kernel ready-list policy cannot compensate for an unbounded user callback.

### Keep blocking work off the loop

File I/O, DNS in blocking APIs, database calls, compression, certificate operations, image parsing, synchronous logging, lock waits, and CPU-heavy application logic can stall the loop. Either use truly nonblocking/integrated APIs or submit bounded work to an executor.

Executor submission itself needs capacity and a rejection/backpressure policy. Capture immutable input and a `(handler_id,generation,operation_id)` token. Worker code must not mutate loop-owned state. Completion enters a thread-safe bounded queue, wakes the loop, and is applied only if handler/generation/state still match.

### Preserve lifecycle and cancellation safety

Use explicit states such as `registered`, `active`, `read_paused`, `closing`, and `closed`. Close is idempotent: stop new interests, cancel timers/offloads where possible, detach registration, release buffers/claims, record terminal reason, and invalidate generation.

Queued readiness can arrive after cancellation. A descriptor number may be reused. Resolve event data to a registration object or token and validate current generation; ignore stale events/completions. Define whether close drains output, aborts immediately, or waits until deadline, and ensure shutdown cannot wait forever.

### Handle reentrancy and callback failure

Even one loop can be reentrant if a callback invokes user code that synchronously calls back, runs a nested loop, or completes a future inline. State invariants should hold before invoking external callbacks, and APIs should document which actions are deferred to the next turn.

Catch failures at a boundary that can close/quarantine one connection or operation, run cleanup, and keep loop bookkeeping valid. Fatal process invariants may require supervised restart, but arbitrary parser exceptions should not terminate every connection.

### Implement input backpressure and admission

Set per-connection and global input byte/frame limits, header/body deadlines, parser complexity limits, and maximum concurrent in-flight requests. At high watermark, disable read interest or stop accepting; resume below a lower watermark to avoid oscillation. Protocol-level flow control should align when available.

Accept loops need per-turn budgets and global connection/file-descriptor/memory quotas. On overload, prefer early bounded rejection or listener throttling over accepting unlimited sockets that cannot progress. Fairness across tenants may require separate pools or quotas.

### Implement output backpressure

Slow peers can make output queues grow indefinitely. Bound per-connection/global queued bytes, disable upstream production/read when responses cannot drain, coalesce only when semantics permit, and close/shedding under an explicit policy. Write readiness is commonly persistent, so subscribing without pending bytes causes a busy loop.

Propagate pressure beyond the loop: bounded worker queues, database concurrency, broker credits, and application admission. Dropping a response after committing an external effect may require retry/reconciliation semantics, not simple buffer deletion.

### Integrate timers correctly

Use a monotonic clock for durations and deadlines; wall-clock adjustments should not make timeouts run backward. Maintain a timer heap/wheel or runtime facility, compute poll timeout from the next due timer, and budget timer callbacks. Avoid scanning every connection on every tick.

Define simultaneous readiness/timeout ordering and validate current generation before timer action. Timer drift and loop lag must be observable; firing late does not prove a peer was inactive at the nominal instant.

### Scale across cores

One Reactor thread gives simple ownership but one-core capacity and failure domain. Common scaling uses one loop per core/thread and assigns each connection to one loop for life, reducing locks and cache migration. An acceptor can distribute new connections; kernel mechanisms can distribute listeners.

Cross-loop migration is complex because interests, buffers, timers, worker completions, and ownership move together. Prefer stable affinity unless measured skew justifies a protocol. Shared downstream state still needs synchronization even when connection state is isolated.

### Separate Reactor from Proactor

Reactor reports readiness, and the handler performs the nonblocking operation. Proactor initiates asynchronous operations and later dispatches completion results. Some libraries expose a common callback/future interface over readiness on one platform and completion mechanisms on another. Classify the responsibility at the abstraction boundary rather than by backend brand.

Never assume completion semantics merely because an API says “async.” It may offload blocking work, poll readiness, or complete inline. Cancellation and buffer ownership differ materially.

### Secure the event loop

Slowloris clients, oversized frames, decompression bombs, expensive parsers, TLS handshakes, repeated auth failures, connection churn, and output-stalling peers target shared loop resources. Enforce progressive deadlines, size/work budgets, connection/tenant quotas, bounded handshakes, and early authentication where appropriate.

Do not log raw secrets or untrusted format strings from the loop. Protect wakeup/control channels, validate cross-thread commands, and ensure one tenant cannot exhaust descriptors, buffers, timers, executor slots, or callback budget.

### Observe and verify

Measure poll wait/wakeup reason, ready-set size, iterations/s, loop lag and timer lateness, callback duration/work/budget exhaustion, bytes/frames, `would block`, interest transitions, input/output buffers, accept/reject, connection age/state, executor queue/runtime/rejection, wakeup depth, stale completions, exceptions and close reasons.

Test with socket pairs/real network: fragmented/coalesced frames, partial writes, EOF/half-close/reset, stale/spurious readiness, edge drain, one-shot rearm, hot and slow clients, output blockage, descriptor reuse, cancellation versus completion, executor saturation, timer storms, callback exceptions, accept floods, graceful/forced shutdown, and multi-loop skew. Use deterministic state-machine/model tests plus platform-specific integration and load evidence.

## Definitions and Notation

| Symbol or term | Meaning |
| --- | --- |
| $I_t$ | Registrations and interest sets installed at iteration $t$ |
| $R_t$ | Ready registrations returned/queued at iteration $t$ |
| $b_i$ | Cooperative work budget for handler $i$ per turn |
| $S$ | Reactor-thread service time per dispatched event/work unit |
| $\lambda$ | Arrival rate of reactor-thread work under stated workload |
| $\rho$ | Idealized loop utilization $\lambda E[S]$ |
| $L$ | Loop lag from actionable readiness/timer to handler start |
| $q_i^{in},q_i^{out}$ | Bounded input and output backlog for connection $i$ |
| generation | Monotone lifecycle token invalidating stale asynchronous work |
| `would block` | Non-error result: no progress currently possible without waiting |
| high/low watermark | Hysteretic thresholds for pausing and resuming admission/read/production |

The single-server utilization model is a necessary abstraction, not a latency theorem. Event costs are variable, arrivals burst/correlate, and one connection can generate several kinds of work. Queueing delay grows sharply near saturation; empirical tail distributions are required.

## Mechanisms, Invariants, or Proof Structure

### Ownership argument

Assume a connection's mutable state is accessed only by its assigned loop. Worker tasks receive immutable snapshots and return results through the loop queue with matching generation. Then handler transitions are serialized without connection-state locks. The argument does not cover shared databases, caches, other loops, signals, or libraries that mutate state outside the contract.

### Stale-completion safety

Every registration has identity $r$ and generation $g$. Close increments/invalidates $g$ before resources can be reused. A queued readiness, timer, or worker completion is applied only if its `(r,g,operation)` matches current state. Therefore an old completion cannot mutate a new generation through the guarded path. Unguarded external side effects require separate idempotency/fencing.

### Fairness argument

Assume a finite ready round, tail requeue, per-handler budget $b_i$, nonblocking callbacks, and fair selection. No continuously ready handler can consume more than its budget before every peer in that round gets a turn, so a peer's cooperative delay is bounded by the sum of preceding budgets and fixed overhead. Priorities, new arrivals, timer work and scheduler implementation require a refined bound.

### Executable finite model

The model gives two ready handlers a two-item budget per round and tail-requeues unfinished work. It illustrates cooperative fairness only; it does not perform I/O, model level/edge notifications, time, threads, cancellation, pressure, or kernel scheduling.

<!-- bijux-verify: {"id":"reactor-fair-dispatch","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"round=1 handled=a:2,b:2 remaining=a:2,b:1\nround=2 handled=a:2,b:1 remaining=a:0,b:0\nfair=True total=7 registrations=2\n","stderr":""}} -->
```python
class Reactor:
    def __init__(self, budget):
        self.budget = budget
        self.pending = {}
        self.ready = []
        self.total = 0

    def register(self, name, work):
        self.pending[name] = list(work)
        if work:
            self.ready.append(name)

    def run_once(self):
        current = list(self.ready)
        self.ready = []
        handled = []
        for name in current:
            count = min(self.budget, len(self.pending[name]))
            del self.pending[name][:count]
            self.total += count
            handled.append(f"{name}:{count}")
            if self.pending[name]:
                self.ready.append(name)
        remaining = ",".join(f"{name}:{len(self.pending[name])}" for name in current)
        return ",".join(handled), remaining


reactor = Reactor(budget=2)
reactor.register("a", [1, 2, 3, 4])
reactor.register("b", [1, 2, 3])

for round_number in [1, 2]:
    handled, remaining = reactor.run_once()
    print(f"round={round_number} handled={handled} remaining={remaining}")

fair = reactor.pending["a"] == [] and reactor.pending["b"] == []
print(f"fair={fair} total={reactor.total} registrations={len(reactor.pending)}")
```

## Alternatives and Trade-Offs

| Design | Advantage | Cost or limitation | Best fit |
| --- | --- | --- | --- |
| Reactor/readiness | Many mostly idle handles; explicit state ownership | Incremental I/O/state and cooperative blocking risk | High-concurrency network protocols |
| Proactor/completion | Operation results arrive completed | Buffer/cancellation/lifetime complexity; platform variation | Native asynchronous operation APIs |
| Thread per connection | Straight-line blocking code and isolation | Thread memory/scheduling/lock costs at large scale | Bounded connection counts or virtual-thread runtimes after validation |
| Loop per core | Scales ownership with low connection-state locking | Affinity/skew and cross-loop coordination | Multi-core network services |
| Acceptor plus reactors | Central admission and distribution | Acceptor bottleneck/failure and handoff cost | Controlled connection placement |
| Half-Sync/Half-Async | Keeps event layer responsive while sync workers run | Queue boundary, ordering and overload | Blocking domain/application layer |
| Edge-triggered | Fewer repeated notifications in some workloads | Must drain/rearm correctly; harder fairness | Carefully engineered high-throughput loops |
| Level-triggered | Simpler correctness and bounded turns | Repeated notifications/busy-loop risk | Default unless measurements justify edge mode |

Modern virtual threads can make thread-per-connection viable for some loads, but library pinning, CPU, memory, downstream limits, cancellation and observability still need measurement. The durable decision is ownership/blocking behavior, not fashion or API syntax.

## Failure Modes and Misconceptions

- **“Readable means a complete message.”** It may be one byte, EOF, error, or several frames.
- **“Writable means the whole buffer will fit.”** Only some progress may be possible.
- **“Readiness guarantees no blocking.”** It is a hint and can become stale; use nonblocking operations.
- **“Edge-triggering is always faster.”** Incorrect drain/rearm loses progress; fairness and syscall trade-offs are workload-specific.
- **“Drain until empty is always fair.”** A hot source can starve peers; combine edge-state tracking with budgets.
- **“Single-threaded means race-free.”** Workers, timers, close, external effects, reentrancy and shared state still race.
- **“No locks means no contention.”** The loop itself, buffers, executors and downstream services are serialized/finite resources.
- **“Async APIs never block.”** They may perform DNS, file I/O, logging, allocation, callbacks, or inline completion synchronously.
- **“Offload fixes blocking.”** An unbounded executor moves overload and can return stale results.
- **“Descriptor number identifies a connection.”** Numbers are reused; validate registration identity/generation.
- **“Always watch writable.”** Most sockets are often writable, causing a busy loop without queued output.
- **“Backpressure is dropping old buffers.”** It needs semantic admission and outcome policy.
- **“Timer fired means deadline was observed exactly.”** Loop lag can make it late; record scheduled and actual time.
- **“One event loop scales across all cores.”** It normally has one-thread CPU capacity unless sharded/offloaded.
- **“High throughput proves responsiveness.”** One hot callback can preserve average throughput while destroying tail latency.

## Worked Examples

### Example 1

**Situation.** A socket is reported readable; the handler requests a 12-byte header and receives 5 bytes.

**Reasoning.** Readiness promised possible progress, not a complete header. Store the 5 bytes in bounded connection state, return after budget, and retain read interest. On later readiness, append and parse only when 12 bytes exist; validate declared body length before allocating.

**Conclusion.** Incremental parsing turns partial I/O into ordinary state rather than an error/blocking wait.

### Example 2

**Situation.** Under edge-triggering, 2 KiB arrives and the handler reads only 1 KiB, then waits for another notification.

**Reasoning.** The readiness transition may already have been consumed; the remaining byte state may not create another edge. Continue nonblocking reads until `would block`, subject to a budget. If budget expires first, mark the handle locally ready and tail-requeue it.

**Conclusion.** Correct edge handling combines drain semantics with user-space fairness state.

### Example 3

**Situation.** A server registers write interest for every connected socket even when output queues are empty.

**Reasoning.** Sockets are commonly writable, so the poller returns immediately and the loop spins doing no useful work. Enable write interest only when bytes are queued; after draining to zero, disable it. Measure no-progress writable callbacks.

**Conclusion.** Interest masks are dynamic protocol state, not static capabilities.

### Example 4

**Situation.** One callback performs 80 ms of JSON validation while 2,000 connections and a 10 ms timer share the loop.

**Reasoning.** All peers and timers wait at least the callback duration. Bound parsing work and offload the CPU-heavy validation to a bounded executor with immutable bytes and generation token. Backpressure when executor capacity is exhausted.

**Conclusion.** A cooperative loop's worst callback contributes directly to unrelated tail latency.

### Example 5

**Situation.** A client sends one header byte every 20 seconds and holds thousands of sockets.

**Reasoning.** Nonblocking I/O alone does not stop Slowloris resource capture. Enforce header completion deadline, minimum progress policy where appropriate, per-tenant/IP admission, global descriptors/buffers, maximum header bytes, and bounded parsing. Close with an explicit reason at policy expiry.

**Conclusion.** Time and memory budgets are security invariants of the Reactor.

### Example 6

**Situation.** A peer stops reading while application responses continue accumulating.

**Reasoning.** Partial writes grow the output queue. At high watermark, stop upstream response production and possibly read/request admission; propagate pressure to worker/downstream queues. Resume below low watermark. If deadline/limit is exceeded, close or shed under a semantic policy and reconcile any committed effects.

**Conclusion.** Writable readiness does not provide infinite output capacity; backpressure crosses application boundaries.

### Example 7

**Situation.** Connection A closes and its descriptor is reused for B; an old worker completion for A arrives.

**Reasoning.** Descriptor equality is insufficient. A's close invalidates generation 8; B owns generation 9. Completion carries `(registration-A,8,operation)` and is rejected before state mutation. An already performed external effect still needs idempotency/reconciliation.

**Conclusion.** Logical registration generation fences loop-owned state from stale asynchronous work.

### Example 8

**Situation.** One always-ready stream drains 50,000 frames per callback while a heartbeat timer is due.

**Reasoning.** Limit frames/bytes/time per turn, tail-requeue the stream, and reserve timer processing. Track timer lateness and budget exhaustion. A priority timer queue may help, but continuous high-priority work needs its own quotas.

**Conclusion.** Fairness is an explicit scheduler policy above kernel readiness.

### Example 9

**Situation.** A one-loop server saturates one core while seven cores are idle.

**Reasoning.** Assign accepted connections across eight loop threads with stable affinity, independent pollers/buffers/timers, and bounded shared downstream resources. Hash/load-aware placement handles imbalance. Avoid live migration until evidence shows it is needed and its ownership protocol is verified.

**Conclusion.** Loop-per-core scales serialized ownership; it does not remove shared-service limits.

### Example 10

**Situation.** A clinical telemetry gateway uses one loop for device feeds; one malformed compressed frame triggers heavy decompression and synchronous audit logging.

**Reasoning.** Validate compressed and expanded limits, schema and device identity before expensive work; offload bounded decompression/validation; keep audit output asynchronous/durable with pressure policy; quarantine the device/message; preserve other device timers. Generation-check results if the session closes or credential is revoked.

**Conclusion.** High-stakes Reactor safety requires resource, identity, evidence, and isolation boundaries beyond nonblocking sockets.

## Cross-Program Connections

- [Operating Systems](../../22-operating-systems/ROADMAP.md): descriptors, readiness APIs, scheduling, signals, clocks and resource limits implement demultiplexing.
- [Network Engineering](../../24-network-engineering/ROADMAP.md): TCP streams, flow control, half-close, reset, congestion and protocol framing shape handlers.
- [Security Engineering](../../25-security-engineering/ROADMAP.md): Slowloris, parser/resource exhaustion, tenant quotas, identity and protected control paths constrain the loop.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md): deadlines, framing, idempotency, connection lifecycle and overload policy connect transport to service contracts.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md): event-loop metrics, executor sizing, deployment draining, limits and incident response make the design operable.
- [SEPAT-072](../ROADMAP.md) contrasts operation-completion ownership; [SEPAT-073](../ROADMAP.md) introduces a queue between asynchronous and synchronous layers.

## References

1. Schmidt, Douglas C., Michael Stal, Hans Rohnert, and Frank Buschmann. *Pattern-Oriented Software Architecture, Volume 2: Patterns for Concurrent and Networked Objects*. Wiley, 2000. Reactor and related concurrency patterns.
2. Schmidt, Douglas C. “Reactor: An Object Behavioral Pattern for Demultiplexing and Dispatching Handles for Synchronous Events.” Pattern Languages of Program Design, 1995.
3. Kerrisk, Michael. “epoll(7).” *Linux man-pages 6.18*, 2026-02-08. <https://man7.org/linux/man-pages/man7/epoll.7.html>. Accessed 2026-08-29.
4. Kerrisk, Michael. “epoll_wait(2).” *Linux man-pages 6.18*. <https://man7.org/linux/man-pages/man2/epoll_wait.2.html>. Accessed 2026-08-29.
5. Oracle. “Selector” and “SelectionKey,” Java SE 17 API. <https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/nio/channels/Selector.html> and <https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/nio/channels/SelectionKey.html>. Accessed 2026-08-29.
6. libuv. “Design overview,” version 1.x documentation. <https://docs.libuv.org/en/v1.x/design.html>. Accessed 2026-08-29.
7. Mathewson, Nick. “Working with an event loop.” *Libevent Book*. <https://libevent.org/libevent-book/Ref3_eventloop.html>. Accessed 2026-08-29.
8. Stevens, W. Richard, Bill Fenner, and Andrew M. Rudoff. *UNIX Network Programming, Volume 1*, 3rd ed. Addison-Wesley, 2003. Nonblocking I/O and multiplexing.
9. Kerrisk, Michael. *The Linux Programming Interface*. No Starch Press, 2010. File descriptors, signals, timers and alternative I/O models.
10. IETF. *RFC 9293: Transmission Control Protocol (TCP)*. August 2022. <https://www.rfc-editor.org/rfc/rfc9293>.
11. Nygard, Michael T. *Release It!*, 2nd ed. Pragmatic Bookshelf, 2018. Timeouts, bulkheads, backpressure and stability.
12. Gregg, Brendan. *Systems Performance*, 2nd ed. Addison-Wesley, 2020. Utilization, latency, queueing, profiling and observability.

Readiness, edge/level, one-shot, fairness, cancellation and thread-safety behavior varies by platform and library. Current Linux, Java, libuv and Libevent documentation was checked on 2026-08-29; implementations must verify their exact OS, runtime, API, version and configuration.

## Exercises

### Exercise 1

Name the Reactor participants and distinguish readiness, I/O progress, frame completion, handler completion, and business completion for a readable TCP socket.

### Exercise 2

Five continuously ready handlers have enforced budgets of 0.4, 0.8, 0.3, 1.0, and 0.5 ms. Poll/dispatch overhead is 0.2 ms per round. Derive the cooperative one-round delay bound under the stated model. If arrivals are 8,000 events/s and mean loop-thread work is 90 microseconds, compute idealized utilization and assess stability/headroom.

### Exercise 3

Design a length-prefixed connection handler supporting partial reads/writes, edge-triggering, two in-flight requests, output watermarks, a 5-second request deadline, CPU offload, cancellation, and graceful close. State its lifecycle and generation checks.

### Exercise 4

Diagnose a service that watches every socket writable, performs blocking DNS and logging on the loop, has an unbounded worker pool, sees timer lag under a hot client, and occasionally applies results to reused descriptors. Provide a remediation and verification plan.

### Exercise 5

Design a Reactor-based gateway for emergency industrial shutdown sensors. Address admission, authenticated framing, deadlines, priority/fairness, partial I/O, pressure, blocking work, stale completion, redundant loops, failure isolation, audit, safe degradation, and required external review.

## Answers to the Exercises

### Answer 1

The initiator registers a nonblocking handle and interest set with the Reactor; the synchronous event demultiplexer waits and returns readiness; the dispatcher resolves the current registration; its event handler owns protocol state and attempts I/O. Readiness is a hint that a read may progress. I/O progress is a byte count/EOF/error/`would block`. Frame completion occurs only when the incremental parser has all validated bytes. Handler completion means the bounded callback returned after updating interests/state. Business completion may require authenticated processing, durable effect, response/outbox and reconciliation beyond the socket callback. None of the earlier stages implies the later one.

### Answer 2

The sum of budgets is

$$
0.4+0.8+0.3+1.0+0.5=3.0\text{ ms}.
$$

Adding 0.2 ms poll/dispatch overhead gives an approximate 3.2 ms one-round bound under finite ready set, fair once-per-round scheduling, nonblocking callbacks, enforced budgets and no higher-priority/new work. Idealized utilization is

$$
\rho=8000\times90\times10^{-6}=0.72.
$$

It satisfies the necessary $\rho<1$ condition but does not prove sufficient headroom or tail latency. Bursts, variable service, timers, syscalls, offloaded completions, GC/scheduling, hot connections and downstream pressure require measured distributions; 72% average may still violate a strict tail SLO.

### Answer 3

Use states `registered -> reading_header -> reading_body -> processing -> writing -> closing -> closed`, allowing up to two request operation records. On edge readiness, nonblocking-read until `would block` or byte/frame/time budget; accumulate a fixed-size length header, reject oversized length before allocation, then accumulate body and parse complete frames. Disable read at two in-flight requests or input high watermark and reenable below low watermark. Each request has monotonic 5-second timer and operation ID.

Submit immutable validated bytes to a bounded CPU executor with `(registration_id,generation,operation_id)`; on rejection, pause/read-throttle or return bounded overload result. Worker completion enters the loop wakeup queue. Apply only if registration/generation/operation remains current and deadline/policy permits. Queue response buffers with offsets; enable write only when nonempty; drain under edge semantics to `would block` or budget; enforce high/low output watermarks and propagate pressure.

Cancellation marks operation, invalidates applicable token, removes timers, and ignores late results. Graceful close stops new reads, lets permitted in-flight operations/output drain until close deadline, then unregisters/closes idempotently and increments generation before reuse. EOF/half-close/error have explicit protocol outcomes. Tests cover every partial boundary, multiple frames/read, partial writes, edge budget/local requeue, timeout versus completion, executor saturation, pressure, EOF/reset, close/reuse and forced shutdown.

### Answer 4

Permanent write interest makes the poller return sockets with no work, creating CPU spin. Blocking DNS/logging stalls all callbacks and timers. The unbounded pool hides overload in threads/queues and late results keyed only by reused descriptors corrupt new sessions. Enable write interest only with queued bytes and disable after drain. Use an asynchronous resolver or bounded executor; route logging through a bounded nonblocking pipeline with overload policy. Bound executor queue/concurrency and make submission rejection pause/admit/shedding explicit.

Add per-handler byte/frame/time budgets and tail requeue, reserve timers/control turns, input/output high/low watermarks, connection/tenant quotas, and downstream limits. Bind every task to registration object/ID plus generation and operation; close invalidates generation before handle reuse, and completion validates on the loop. Measure poll wake reasons, no-progress writable calls, loop/timer lag, callback duration, executor depth/rejection, buffer pressure and stale completions. Verify with hot/slow clients, fragmented I/O, DNS/log sink delay, executor saturation, timer storm, cancellation/close versus completion, descriptor reuse, overload and graceful/forced shutdown.

### Answer 5

Use at least two independently supervised loop shards with stable sensor-connection ownership, bounded listener admission, descriptor/memory quotas, and a documented redundant ingestion/failover protocol; duplication is handled by stable sensor/event/operation identity. Authenticate device and framing before accepting commands/data, enforce fixed maximum frame and incremental parsing, integrity/sequence/timestamp checks, monotonic heartbeat/deadline timers, and current device authorization. Never treat a transport trace ID as control authority.

Give shutdown signals a bounded high-priority class but enforce tenant/device quotas and reserve turns so telemetry, timers and control remain live. Nonblocking reads/writes handle partial progress; edge handlers drain with local fair requeue. Bound input/output buffers and in-flight decisions, disable reads or reject admission under downstream pressure, and define safe degradation: local hardware safety interlocks must not depend solely on the gateway, and an unavailable/ambiguous remote signal escalates rather than fabricating success.

Offload cryptography or expensive validation only to bounded isolated executors; return immutable results through wakeup queues with registration/generation/operation checks. Close/revocation invalidates late work. Contain malformed/compromised sensors, preserve sanitized immutable evidence, and keep audit emission durable/bounded without blocking the loop. Observe deadline slack, loop/timer lag, per-priority budgets, sequence gaps, auth/integrity, buffers, executor pressure, shard health, duplicates, stale results and terminal control outcomes.

Test fragmentation/coalescing, partial writes, slow/flooding/hostile sensors, clock/sequence boundary, auth/key rotation, parser/crypto exhaustion, executor/audit/downstream outage, loop/process/region failure, duplicate/reordered signals, close/reuse, failover and manual/local fallback. Production claims require named control-systems, functional-safety, security, networking, operations and regulatory reviewers plus hardware-in-the-loop, fault-injection and emergency-drill evidence.
