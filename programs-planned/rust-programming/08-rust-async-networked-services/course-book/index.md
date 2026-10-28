# Course 8 — Rust Async and Networked Services

## Futures, Tokio, Protocols, and Resilient Service Lifecycles

## The promise

Course 8 begins with the `Future::poll` contract and then builds Tokio task trees, bounded codecs, connection lifecycles, versioned protocols, admission control, cancellation-safe operations, a small Hyper surface, and idempotent retry policy.

> **Governing question:** How do suspension, wakeup, task ownership, framing, protocol state, capacity, cancellation, retry, and shutdown remain explicit when peers and timing are only partly observable?

Course 7 established ownership, visibility, progress, and termination across threads. Course 8 keeps those obligations while work may suspend and peers may be remote. Futures, runtimes, framing, protocol state, backpressure, retry, and shutdown are therefore taught as one lifecycle rather than as unrelated async APIs.

## Before Day 1

You should be able to reason about thread ownership, synchronization, backpressure, liveness, atomics, deterministic reconciliation, system I/O, and bounded resources.

From a blank page, sketch one earlier product or a comparable program. Mark an owner, a valid and invalid state, a failure path, cleanup, and a public promise. Repair any relationship you cannot explain before adding this course’s mechanisms.

## Outcomes

- Explain why a future is inert until polled.
- Distinguish a runtime, worker thread, task, future, reactor, and blocking pool.
- Distinguish readiness from transfer completion.
- Distinguish bind, listen, accept, connect, resolve, read, write, half-close, and full close.
- Separate framing, text decoding, syntax parsing, semantic validation, state legality, and application execution.
- Find every accumulation point in an async service.
- Derive cancellation behavior from future-owned state and external side effects.
- Distinguish accepted transport, HTTP connection future, request future, body stream, and application service.
- Classify failures by phase, scope, retryability, and commit ambiguity.
- Construct a complete async service dossier.
- Integrate all ten mechanisms in JobWire without creating competing authorities.
- Complete and defend an unseen change using a async service dossier.

## The ten-day line

| Day | Module | Governing question | Capability that must become visible | Laboratory |
|---:|---|---|---|---|
| 1 | [71 — Futures, Polling, Wakers, and Async State Machines](./module-71-futures-polling-wakers-and-async-state-machines/index.md) | What exactly is an async computation before a runtime executes it, what must happen when it cannot complete, and what state remains when it is suspended or cancelled? | **Explain why a future is inert until polled.** | [One-Shot Signal](../labs/module-01-one-shot-signal/README.md) |
| 2 | [72 — Tokio Runtimes, Tasks, and Structured Async Lifecycles](./module-72-tokio-runtimes-tasks-and-structured-async-lifecycles/index.md) | Once futures are understood as poll-driven state machines, how should a runtime own, schedule, observe, cancel, and finish the tasks that execute them? | **Distinguish a runtime, worker thread, task, future, reactor, and blocking pool.** | [Task Nursery](../labs/module-02-task-nursery/README.md) |
| 3 | [73 — Async I/O, Buffers, Streams, and Framing](./module-73-async-io-buffers-streams-and-framing/index.md) | How do arbitrary, partial byte transfers become complete bounded messages without confusing readiness, reads, buffers, frames, or protocol meaning? | **Distinguish readiness from transfer completion.** | [Bounded Length Codec](../labs/module-03-bounded-length-codec/README.md) |
| 4 | [74 — TCP, UDP, DNS, and Connection Lifecycles](./module-74-tcp-udp-dns-and-connection-lifecycles/index.md) | What lifecycle does each network transport actually provide, and where should connection admission, name resolution, deadlines, half-close, datagram loss, and peer identity be represented? | **Distinguish bind, listen, accept, connect, resolve, read, write, half-close, and full close.** | [Deadline Echo Service](../labs/module-04-deadline-echo-service/README.md) |
| 5 | [75 — Protocol State Machines, Versioning, and Defensive Parsing](./module-75-protocol-state-machines-versioning-and-defensive-parsing/index.md) | Once frames arrive intact, how do they become legal protocol messages whose meaning depends on version, connection state, request identity, and error scope? | **Separate framing, text decoding, syntax parsing, semantic validation, state legality, and application execution.** | [Negotiated Command Protocol](../labs/module-05-negotiated-command-protocol/README.md) |
| 6 | [76 — Backpressure, Admission Control, and Fair Work Distribution](./module-76-backpressure-admission-control-and-fair-work-distribution/index.md) | When demand exceeds service capacity, where may work wait, which bound is authoritative, and how does overload become an explicit product outcome instead of memory growth, latency collapse, or starvation? | **Find every accumulation point in an async service.** | [Bounded Relay Broker](../labs/module-06-bounded-relay-broker/README.md) |
| 7 | [77 — Cancellation Safety, Deadlines, and Graceful Shutdown](./module-77-cancellation-safety-deadlines-and-graceful-shutdown/index.md) | When an async operation loses a race, exceeds a deadline, or receives shutdown, what state survives, which effects may already have committed, and how does every task reach a terminal joined state? | **Derive cancellation behavior from future-owned state and external side effects.** | [Graceful Task Tree](../labs/module-07-graceful-task-tree/README.md) |
| 8 | [78 — HTTP Services with Hyper: Requests, Bodies, and Connections](./module-78-http-services-with-hyper-requests-bodies-and-connections/index.md) | How do you build a small HTTP service while keeping transport ownership, HTTP connection driving, request-body policy, routing, application state, and health semantics separate? | **Distinguish accepted transport, HTTP connection future, request future, body stream, and application service.** | [Hyper Health Surface](../labs/module-08-hyper-health-surface/README.md) |
| 9 | [79 — Network Failure, Idempotency, Retries, and Deterministic Testing](./module-79-network-failure-idempotency-retries-and-deterministic-testing/index.md) | When a network operation fails without revealing whether the remote side committed it, how do idempotency, retry budgets, failure classification, and deterministic tests preserve one semantic outcome? | **Classify failures by phase, scope, retryability, and commit ambiguity.** | [Idempotent Retry Client](../labs/module-09-idempotent-retry-client/README.md) |
| 10 | [80 — Integrated Async Service Architecture, Testing, and Audit](./module-80-integrated-async-service-architecture-testing-and-audit/index.md) | Can the complete service be explained as one coherent set of lifecycle, protocol, capacity, cancellation, failure, compatibility, and operational contracts rather than as a pile of async APIs? | **Construct a complete async service dossier.** | [Async Service Audit](../labs/module-10-async-service-audit/README.md) |

The table is a dependency chain, not a menu. A later module may use an earlier mechanism but may not silently weaken its ownership, failure, ordering, capacity, safety, compatibility, or evidence contract.

## Decision rules

| Decision | Rule used throughout this course |
|---|---|
| Future | List stored states, wake source, completion, and drop behavior before writing `poll` or `async` code. |
| Task lifecycle | Every spawned task is observed, joined, aborted, or deliberately detached with a stated owner. |
| Framing | Treat transport chunks as arbitrary; validate frame length before allocation. |
| Cancellation | Identify the exact suspension points after which dropping the future can leave an external effect. |
| Retry | Use one overall deadline and an idempotency strategy when commit may be ambiguous. |

Use these rules during prediction and review. When a rule does not decide the case, write the missing product requirement instead of selecting an API by habit.

## The reasoning record

The ten module-specific records culminate in a **async service dossier**. Trace future state, wake source, task owner, frame state, protocol state, capacity, cancellation, commit ambiguity, and shutdown. Keep the record small enough to inspect but complete enough to expose the first unsupported assumption.

## Scope and handoff

The course builds a process-local network service. It does not attempt distributed consensus, TLS implementation, database transactions, service meshes, or framework-driven web development. Those concerns are discussed only where they affect the stated protocol and lifecycle guarantees.

Course 9 asks whether the service’s performance, memory, reliability, observability, security, artifact, and operational claims are supported by representative evidence.

## Capstone — JobWire

JobWire is a bounded async job service with a framed TCP protocol, version negotiation, a broker authority, bounded queued and active work, idempotency records, structured cancellation, a small Hyper health surface, and deterministic tests.

Open the [engineering guide](capstone.md) before Day 1 so the final architecture is visible. Implement only the current increment. The independent laboratory remains separate so that the mechanism can be learned without hiding behind accumulated capstone code.

## Completion

The course is complete when you can build and defend:

> Build a bounded async command service with a length-delimited protocol, tracked task tree, explicit admission, honest health semantics, cancellation-safe shutdown, and deterministic timeout tests.

and then change the capstone under this constraint:

> Add one streaming JobWire operation with an explicit per-stream capacity and cancellation contract while preserving protocol versioning and service shutdown.

A passing test suite is necessary. It is not sufficient unless you can explain why the tests are capable of falsifying the claim and which target-, scheduler-, workload-, peer-, or policy-dependent facts remain outside them.

## Continue

- [Ten-day plan](study-plan.md)
- [Module 71 — Futures, Polling, Wakers, and Async State Machines](./module-71-futures-polling-wakers-and-async-state-machines/index.md)
- [JobWire engineering guide](capstone.md)
- [Course reference](reference.md)
- [Final review](final-review.md)
- [Compiler and design investigations](../compiler-labs/README.md)
- [Independent laboratories](../labs/)
