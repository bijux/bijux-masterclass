# Course 8 — Rust Async and Networked Services

## Futures, Tokio, Protocols, and Resilient Service Lifecycles

Course 8 begins with the `Future::poll` contract and then builds Tokio task trees, bounded codecs, connection lifecycles, versioned protocols, admission control, cancellation-safe operations, a small Hyper surface, and idempotent retry policy.

> **Governing question:** How do suspension, wakeup, task ownership, framing, protocol state, capacity, cancellation, retry, and shutdown remain explicit when peers and timing are only partly observable?

## Entry point

You should be able to reason about thread ownership, synchronization, backpressure, liveness, atomics, deterministic reconciliation, system I/O, and bounded resources.

The immediate prerequisite is [Course 7: Rust Concurrency and Parallelism](../07-rust-concurrency-parallelism/course-book/index.md). Entering mid-program is reasonable only when you can complete the previous course’s final review and one independent construction without following its solution.

## Ten-day route

| Day | Module | Capability added | Independent laboratory |
|---:|---|---|---|
| 1 | [71 — Futures, Polling, Wakers, and Async State Machines](course-book/module-71-futures-polling-wakers-and-async-state-machines/index.md) | Explain why a future is inert until polled | [One-Shot Signal](labs/module-01-one-shot-signal/README.md) |
| 2 | [72 — Tokio Runtimes, Tasks, and Structured Async Lifecycles](course-book/module-72-tokio-runtimes-tasks-and-structured-async-lifecycles/index.md) | Distinguish a runtime, worker thread, task, future, reactor, and blocking pool | [Task Nursery](labs/module-02-task-nursery/README.md) |
| 3 | [73 — Async I/O, Buffers, Streams, and Framing](course-book/module-73-async-io-buffers-streams-and-framing/index.md) | Distinguish readiness from transfer completion | [Bounded Length Codec](labs/module-03-bounded-length-codec/README.md) |
| 4 | [74 — TCP, UDP, DNS, and Connection Lifecycles](course-book/module-74-tcp-udp-dns-and-connection-lifecycles/index.md) | Distinguish bind, listen, accept, connect, resolve, read, write, half-close, and full close | [Deadline Echo Service](labs/module-04-deadline-echo-service/README.md) |
| 5 | [75 — Protocol State Machines, Versioning, and Defensive Parsing](course-book/module-75-protocol-state-machines-versioning-and-defensive-parsing/index.md) | Separate framing, text decoding, syntax parsing, semantic validation, state legality, and application execution | [Negotiated Command Protocol](labs/module-05-negotiated-command-protocol/README.md) |
| 6 | [76 — Backpressure, Admission Control, and Fair Work Distribution](course-book/module-76-backpressure-admission-control-and-fair-work-distribution/index.md) | Find every accumulation point in an async service | [Bounded Relay Broker](labs/module-06-bounded-relay-broker/README.md) |
| 7 | [77 — Cancellation Safety, Deadlines, and Graceful Shutdown](course-book/module-77-cancellation-safety-deadlines-and-graceful-shutdown/index.md) | Derive cancellation behavior from future-owned state and external side effects | [Graceful Task Tree](labs/module-07-graceful-task-tree/README.md) |
| 8 | [78 — HTTP Services with Hyper: Requests, Bodies, and Connections](course-book/module-78-http-services-with-hyper-requests-bodies-and-connections/index.md) | Distinguish accepted transport, HTTP connection future, request future, body stream, and application service | [Hyper Health Surface](labs/module-08-hyper-health-surface/README.md) |
| 9 | [79 — Network Failure, Idempotency, Retries, and Deterministic Testing](course-book/module-79-network-failure-idempotency-retries-and-deterministic-testing/index.md) | Classify failures by phase, scope, retryability, and commit ambiguity | [Idempotent Retry Client](labs/module-09-idempotent-retry-client/README.md) |
| 10 | [80 — Integrated Async Service Architecture, Testing, and Audit](course-book/module-80-integrated-async-service-architecture-testing-and-audit/index.md) | Construct a complete async service dossier | [Async Service Audit](labs/module-10-async-service-audit/README.md) |

The route is cumulative. Day 1 establishes this course’s vocabulary and Day 10 requires an architectural change that preserves all earlier guarantees.

## Working method

Trace future state, wake source, task owner, frame state, protocol state, capacity, cancellation, commit ambiguity, and shutdown. Use the module-specific reasoning record named in each chapter. Freeze predictions before compiling, preserve causal diagnostics, and compare the lab reference only after recording your own design.

## Capstone — JobWire

JobWire is a bounded async job service with a framed TCP protocol, version negotiation, a broker authority, bounded queued and active work, idempotency records, structured cancellation, a small Hyper health surface, and deterministic tests.

The [engineering guide](course-book/capstone.md) supplies the ten integration steps. The executable [capstone directory](capstone/README.md) contains the product and tests. Each increment must name the changed invariant, the component that owns it, state after failure, and the earlier guarantee that must remain unchanged.

## Scope

The course builds a process-local network service. It does not attempt distributed consensus, TLS implementation, database transactions, service meshes, or framework-driven web development. Those concerns are discussed only where they affect the stated protocol and lifecycle guarantees.

Course 9 asks whether the service’s performance, memory, reliability, observability, security, artifact, and operational claims are supported by representative evidence.

## Exit standard

Complete this independent construction:

> Build a bounded async command service with a length-delimited protocol, tracked task tree, explicit admission, honest health semantics, cancellation-safe shutdown, and deterministic timeout tests.

Then complete this capstone extension:

> Add one streaming JobWire operation with an explicit per-stream capacity and cancellation contract while preserving protocol versioning and service shutdown.

The next step is [Course 9: Rust Performance and Production Engineering](../09-rust-performance-production-engineering/course-book/index.md).

## Reading and execution routes

- [Course book](course-book/index.md)
- [Ten-day study plan](course-book/study-plan.md)
- [Course reference](course-book/reference.md)
- [Final review](course-book/final-review.md)
- [Compiler and design investigations](compiler-labs/README.md)
- [Laboratories](labs/)

```bash
make static-proof
make compiler-labs
make check
make test
make starters
make docs
make proof
```

Static inspection and compilation answer different questions. The strongest completion route uses the pinned toolchain, executes tests and investigations, renders the book, and preserves the resulting evidence with the code under review.
