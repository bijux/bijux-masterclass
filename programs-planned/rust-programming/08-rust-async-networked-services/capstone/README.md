# JobWire

## Course role

JobWire is a bounded async job service with a framed TCP protocol, version negotiation, a broker authority, bounded queued and active work, idempotency records, structured cancellation, a small Hyper health surface, and deterministic tests.

JobWire is not a showcase of ten independent features. It is the place where the course’s mechanisms must coexist without creating a second owner for state, validation, order, failure, compatibility, or resource policy.

## Invariants carried through the product

- Every future that can remain pending has a wake source or terminal event.
- Listeners, connections, broker work, HTTP tasks, and shutdown handles form one owned task tree.
- Frame lengths are bounded before reserve or allocation and partial reads preserve parser state.
- Protocol legality is an explicit state machine selected by negotiated version.
- Mailbox, queued work, active work, retained results, and duplicate waiters are independently bounded.
- Idempotency, retry, cancellation, quiescence, draining, abort, and join have separate semantics.

## Module-to-product map

| Module | Mechanism added | Acceptance criterion |
|---:|---|---|
| 71 | Futures, Polling, Wakers, and Async State Machines | Explain why a future is inert until polled |
| 72 | Tokio Runtimes, Tasks, and Structured Async Lifecycles | Distinguish a runtime, worker thread, task, future, reactor, and blocking pool |
| 73 | Async I/O, Buffers, Streams, and Framing | Distinguish readiness from transfer completion |
| 74 | TCP, UDP, DNS, and Connection Lifecycles | Distinguish bind, listen, accept, connect, resolve, read, write, half-close, and full close |
| 75 | Protocol State Machines, Versioning, and Defensive Parsing | Separate framing, text decoding, syntax parsing, semantic validation, state legality, and application execution |
| 76 | Backpressure, Admission Control, and Fair Work Distribution | Find every accumulation point in an async service |
| 77 | Cancellation Safety, Deadlines, and Graceful Shutdown | Derive cancellation behavior from future-owned state and external side effects |
| 78 | HTTP Services with Hyper: Requests, Bodies, and Connections | Distinguish accepted transport, HTTP connection future, request future, body stream, and application service |
| 79 | Network Failure, Idempotency, Retries, and Deterministic Testing | Classify failures by phase, scope, retryability, and commit ambiguity |
| 80 | Integrated Async Service Architecture, Testing, and Audit | Construct a complete async service dossier |

## Reading route

1. Read the JobWire contract and non-goals in the [engineering guide](../course-book/capstone.md).
2. Locate the type or component that owns each invariant above.
3. Run the baseline tests and one end-to-end demonstration before changing code.
4. Implement only the current module increment and its adversarial test.
5. Trace success, rejection, partial failure, cleanup, order, and capacity through the public surface.
6. Re-run the complete course route, then explain which claims remain conditioned on a compiler, target, scheduler, peer, workload, or operating system.

JobWire is the cumulative capstone for Course 8. It is a bounded single-process async job service with:

- a length-delimited TCP protocol;
- version negotiation;
- sequential request/response connections;
- one broker task as semantic state authority;
- bounded queued and active work;
- process-local idempotency records;
- controlled retry and deadline behavior;
- an HTTP/1 health and statistics surface;
- hierarchical cancellation and joined shutdown;
- deterministic protocol, saturation, retry, and lifecycle tests.

The implementation is intentionally direct. It does not use a web framework or serialization framework because the course needs the transport, body, protocol, and service boundaries to remain visible.

## Commands

```text
jobwire serve [--tcp ADDRESS] [--http ADDRESS]
jobwire submit ADDRESS REQUEST_ID IDEMPOTENCY_KEY OPERATION PAYLOAD
jobwire stats ADDRESS REQUEST_ID
jobwire ping ADDRESS REQUEST_ID
jobwire health HTTP_ADDRESS
jobwire demo
jobwire help
jobwire version
```

Supported operations:

```text
uppercase
word-count
checksum
sleep-ms
```

The `sleep-ms` payload is an integer duration bounded by configuration.

## Wire protocol

Every payload is carried in a four-byte big-endian length-prefixed frame.

```text
HELLO\t1
WELCOME\t1
SUBMIT\trequest-id\tidempotency-key\toperation\tpayload
OK\trequest-id\tresult
BUSY\trequest-id\tretry-after-ms
ERR\trequest-id-or-dash\tcode\tmessage
STATS\trequest-id
STATS-OK\trequest-id\thealth\tactive\tqueued\trecords\tcompleted\tfailed
PING\trequest-id
PONG\trequest-id
QUIT
BYE
```

V1 permits one in-flight request per connection. Concurrency exists across connections and broker jobs.

The configured result limit is smaller than the frame-payload limit because an `OK` response must also carry the response tag, request ID, and separators. `Config::validate` reserves a conservative 128-byte response envelope; an admitted terminal result therefore remains encodable under the same frame bound.

## Run

```bash
cargo run -- serve --tcp 127.0.0.1:7800 --http 127.0.0.1:7801
cargo run -- submit 127.0.0.1:7800 r-1 key-1 uppercase "hello rust"
cargo run -- health 127.0.0.1:7801
```

Use `scripts/demo.sh` for a complete local scenario.
