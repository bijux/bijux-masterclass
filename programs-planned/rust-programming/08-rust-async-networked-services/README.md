# Rust Async and Networked Services

## Futures, Tokio, Protocols, and Resilient Service Design

This is Course 8 of the Rust Programming path and covers Modules 71–80. The first seven courses established typed program construction, ownership and memory, architectural contracts, explicit dataflow, compile-time authority, systems boundaries, and concurrent coordination. This course asks how those guarantees change when work may suspend, resume later, and interact with remote peers that can be slow, malformed, duplicated, disconnected, or only partly observable.

The course does not begin with a framework. It begins with the contract behind `async` itself: a future is an inert state machine that advances only when polled; `Poll::Pending` must arrange a future wakeup; dropping the future is cancellation; and values held across suspension points become part of the state machine. Tokio is introduced only after this model is operational.

Network programming is treated as protocol engineering rather than socket syntax. Every service is reviewed through nine questions:

1. **Suspension:** which operation may return `Pending`, and what event makes another poll useful?
2. **Ownership:** which task owns every socket half, channel endpoint, request, response, and cleanup obligation?
3. **Framing:** where does one message end, how are partial reads handled, and what bounds allocation?
4. **Protocol state:** which messages are legal in each state, and what closes the connection after an error?
5. **Capacity:** what bounds connections, queued work, active work, response buffering, and retry amplification?
6. **Cancellation:** which operations are safe to abandon, and which need an explicit cleanup or commit protocol?
7. **Failure:** how are timeout, disconnect, malformed input, rejection, duplicate request, and internal failure distinguished?
8. **Determinism:** which results and tests must remain independent of runtime scheduling and network chunking?
9. **Observability:** which metrics are advisory, which state is authoritative, and what can health endpoints honestly claim?

The course book is the primary product. Each chapter teaches one complete reasoning model. Workbooks expose whether that model is usable. Labs isolate one mechanism. The cumulative capstone, **JobWire**, forces futures, framing, protocol state, bounded work, idempotency, HTTP health, cancellation, and graceful shutdown to coexist in one service.

## Prerequisites

Begin only after you can:

- explain ownership, borrowing, pinning, `Send`, `Sync`, and cancellation by dropping an owned resource;
- design bounded threaded work with channels, semaphores, atomics, joins, and explicit shutdown;
- separate protocol state from transport mechanics;
- parse hostile bytes with explicit limits and causal errors;
- distinguish data-race freedom from liveness, boundedness, and deterministic output;
- use traits, generics, closures, iterators, tests, and Cargo workspaces;
- state whether a technical claim is a language guarantee, library contract, operating-system observation, or product policy.

The [course overview](course-book/index.md) includes a readiness diagnosis and repair route.

## Ten modules

71. [Futures, Polling, Wakers, and Async State Machines](course-book/module-71-futures-polling-wakers-and-async-state-machines/index.md) — What is a future, what does `poll` promise, and how do wakeups, pinning, suspension, and drop shape correctness?
72. [Tokio Runtimes, Tasks, and Structured Async Lifecycles](course-book/module-72-tokio-runtimes-tasks-and-structured-async-lifecycles/index.md) — Who owns spawned tasks, how are results and panics observed, and how is blocking work kept from freezing the runtime?
73. [Async I/O, Buffers, Streams, and Framing](course-book/module-73-async-io-buffers-streams-and-framing/index.md) — How are arbitrary byte chunks turned into bounded messages without assuming read boundaries or allocating from hostile lengths?
74. [TCP, UDP, DNS, and Connection Lifecycles](course-book/module-74-tcp-udp-dns-and-connection-lifecycles/index.md) — What lifecycle does each transport actually provide, and where do admission, half-close, deadlines, peer identity, and datagram loss belong?
75. [Protocol State Machines, Versioning, and Defensive Parsing](course-book/module-75-protocol-state-machines-versioning-and-defensive-parsing/index.md) — Which messages are legal in which state, how is version negotiation separated from framing, and how are syntax and semantic failures scoped?
76. [Backpressure, Admission Control, and Fair Work Distribution](course-book/module-76-backpressure-admission-control-and-fair-work-distribution/index.md) — Where can demand accumulate, which capacity is authoritative, and how does overload become a deliberate response instead of an outage?
77. [Cancellation Safety, Deadlines, and Graceful Shutdown](course-book/module-77-cancellation-safety-deadlines-and-graceful-shutdown/index.md) — What state survives when a future is dropped, how are deadlines propagated, and how does a service stop accepting work, drain, abort, and join completely?
78. [HTTP Services with Hyper: Requests, Bodies, and Connections](course-book/module-78-http-services-with-hyper-requests-bodies-and-connections/index.md) — How do transport, HTTP connection driving, request routing, body bounds, response construction, and application state remain separate?
79. [Network Failure, Idempotency, Retries, and Deterministic Testing](course-book/module-79-network-failure-idempotency-retries-and-deterministic-testing/index.md) — Which failures are retryable, how do idempotency keys resolve ambiguous commits, and how are time and I/O tested without sleeping and hoping?
80. [Integrated Async Service Architecture, Testing, and Audit](course-book/module-80-integrated-async-service-architecture-testing-and-audit/index.md) — How do lifecycle, protocol, capacity, cancellation, retry, health, and compatibility claims form one defensible service?

## Course rhythm

One module is one dense day:

```text
chapter → frozen predictions → causal repair → focused construction
        → independent lab → JobWire increment → reconstruction
```

Do not open a reference solution until your own state diagram, resource envelope, or protocol trace has been written. Async code can pass ordinary happy-path tests while losing wakeups, retaining tasks, accepting unbounded work, corrupting a frame after cancellation, or retrying an already committed request. The written model is part of the implementation.

## Primary commands

```bash
make static-proof
make compiler-labs
make check
make test
make starters
make fmt
make clippy
make docs
make proof
```

`make proof` is the strongest route. It requires Rust, Cargo, rustfmt, Clippy, rustdoc, and MkDocs.

## Continue

Begin with the [course overview and readiness diagnosis](course-book/index.md), then follow the [ten-day study plan](course-book/study-plan.md).
