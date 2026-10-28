# Node.js Networking, HTTP, and Service Architecture

**Course 6 of the Node.js Programming program · Modules 51–60**

This course turns the asynchronous and streaming foundations of Courses 4 and 5 into complete network services. It begins below HTTP, with addresses, DNS, sockets, deadlines, and connection state. It then builds HTTP semantics, client policy, TLS identity, HTTP/2 multiplexing, long-lived delivery, and whole-service lifecycle.

The central question is not “How do I start a server?” It is:

> How do I define a network contract whose bytes, messages, capacity, identities, deadlines, retries, overload behavior, and shutdown states remain explicit from the socket boundary to the public API?

## What you build

You complete ten independent laboratories and one cumulative capstone, **ServiceWire**.

ServiceWire is a bounded in-memory job service with:

- strict HTTP/1.1 and HTTPS interfaces;
- an HTTP/2 adapter;
- idempotent job submission;
- conditional reads with entity tags;
- replayable server-sent events;
- deadline-aware clients;
- optional UDP discovery for a local controlled network;
- explicit admission and overload policy;
- startup rollback and complete graceful shutdown.

The service is deliberately process-local. Durable databases, message brokers, distributed transactions, consensus, and multi-service workflow semantics belong to Course 7. Course 6 establishes the network and service contracts those later mechanisms must preserve.

## Entry standard

Begin this course only when you can already:

- explain promise and task ownership;
- compose cancellation and one absolute deadline;
- reason about `Buffer` ownership, views, and copies;
- implement bounded incremental framing;
- use `pipeline()` without losing causal failure;
- supervise child processes and complete their lifecycle;
- design strict runtime validation from `unknown`;
- test asynchronous behavior without relying on arbitrary sleeps.

Use the repair routes in Courses 4 and 5 when any of those skills are unstable.

## Learning route

Read the authoritative chapter first. Write predictions before running code. Complete the workbook without opening its solutions. Build the laboratory from `starter/`, then compare with `reference/` only after your own adversarial tests pass. Finally, transfer the mechanism into ServiceWire and explain how it changes the system's invariants.

```text
chapter
   ↓
written prediction
   ↓
causal diagnosis
   ↓
focused construction
   ↓
independent laboratory
   ↓
ServiceWire transfer
   ↓
closed-book defense
```

## Course map

| Module | Topic | Independent product | ServiceWire responsibility |
|---:|---|---|---|
| 51 | Addresses, DNS, sockets, and time | Address Resolution Observatory | endpoint and connection-budget model |
| 52 | TCP framing and connection state | Bounded TCP Frame Server | connection lifecycle and framing discipline |
| 53 | UDP datagrams and correlation | Reliable Datagram Protocol | optional local discovery |
| 54 | HTTP/1.1 messages and semantics | Strict HTTP Message Server | strict finite request/response adapter |
| 55 | Routing, validation, errors, and idempotency | Typed HTTP Router | public application protocol |
| 56 | HTTP clients, pooling, redirects, and retry | Deadline-Aware HTTP Client | supported client and retry policy |
| 57 | TLS identity, trust, SNI, and ALPN | Local TLS Identity Lab | HTTPS endpoint |
| 58 | HTTP/2 sessions and streams | Multiplexed HTTP/2 Service | bounded HTTP/2 adapter |
| 59 | SSE, replay, and long-lived delivery | Replayable SSE Channel | job-event stream |
| 60 | Admission, overload, health, and shutdown | Network Service Audit | integrated product and independent change |

## Commands

```bash
make audit
make links
make source-audit
make investigations
make typecheck
make test
make verify
make proof
```

`make verify` runs every available check under the installed compatibility toolchain and reports baseline differences. `make proof` requires the pinned Node.js, npm, and TypeScript baseline and strict documentation rendering.

## Continue

- [Course book](course-book/index.md)
- [Ten-day study plan](course-book/study-plan.md)
- [Outcomes](course-book/outcomes.md)
- [Reference desk](course-book/reference.md)
- [ServiceWire engineering guide](course-book/capstone.md)
- [Laboratories](labs/README.md)
- [Compiler and runtime investigations](compiler-labs/README.md)
