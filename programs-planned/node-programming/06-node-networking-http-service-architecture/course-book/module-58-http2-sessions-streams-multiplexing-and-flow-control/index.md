# Module 58 — HTTP/2: Sessions, Streams, Multiplexing, and Flow Control

**Progress: 58/100**

## The governing question

> How do you preserve one application protocol while requests become concurrent streams inside a shared session with its own capacity, flow control, errors, negotiation, and shutdown?

## Why this module comes now

HTTPS established secure transport identity and ALPN. HTTP/2 changes the connection model above that transport. Instead of one sequence of HTTP/1.1 requests on a connection, several independent streams can be active concurrently within one session.

Multiplexing reduces some serialization costs, but it also introduces shared session state, per-stream state, flow-control windows, settings, stream reset, and GOAWAY. The application must not interpret “one connection” as “one request” or let a stream-local failure destroy unrelated work unnecessarily.

ServiceWire uses h2c for deterministic local study and keeps its application protocol independent of the adapter. The same typed commands and results serve HTTP/1.1 and HTTP/2.

## Observable outcomes

By the end of the module, you can:

- distinguish HTTP/2 session lifecycle from stream lifecycle;
- map pseudo-headers into the finite application boundary;
- bound sessions, concurrent streams, and each stream body independently;
- understand flow control as a protocol capacity mechanism;
- write and end responses under stream pressure;
- classify stream reset, stream error, session error, GOAWAY, close, and destroy;
- configure and inspect settings without assuming peer compliance beyond the protocol;
- drain sessions gracefully and abort after a deadline;
- test multiplexing without relying on completion order;
- explain where TLS/ALPN applies and where h2c is appropriate only for controlled study.

## The HTTP/2 ledger

| Dimension | Session | Stream |
|---|---|---|
| identity | one transport/protocol connection | one request/response exchange |
| capacity | max sessions | max concurrent streams |
| input bound | connection-level buffers/settings | request body bytes |
| output pressure | shared transport and flow windows | stream write pressure |
| failure | session protocol/socket error | reset or stream-local error |
| graceful close | GOAWAY and close | end response |
| force close | destroy session/socket | close/reset stream |
| owner | runtime session registry | request/stream scope |

A correct design tracks both columns.

## Pseudo-headers are protocol fields

HTTP/2 represents method, path, scheme, and authority through pseudo-headers such as:

```text
:method
:path
:scheme
:authority
```

They must appear before ordinary headers and have protocol-specific rules. Node exposes them through the headers object.

The adapter should normalize these into the same neutral request model used by HTTP/1.1:

```ts
interface FiniteRequest {
  readonly method: string;
  readonly url: URL;
  readonly headers: ReadonlyMap<string, string | readonly string[]>;
  readonly body: AsyncIterable<Uint8Array>;
}
```

Do not pass raw HTTP/2 stream objects into the domain layer.

## Multiplexing changes schedule, not semantics

Several streams can execute concurrently. Completion order can differ from creation order. Product responses remain associated with stream identity, so clients need not reconstruct source order as in a batch engine.

Tests should create several streams with different work durations and assert:

- each receives the right response;
- one slow stream does not semantically corrupt another;
- a reset stream terminates once;
- final session cleanup sees all stream owners complete.

Do not assert an arbitrary completion order unless the protocol promises it.

## Session and stream admission

A server needs separate limits:

- total HTTP/2 sessions;
- streams per session;
- global active application requests;
- body bytes per stream;
- output bytes per response;
- connection-level memory.

Peer settings such as `maxConcurrentStreams` communicate protocol constraints, but the application still needs its own admission policy. A peer can open streams up to negotiated limits while the application is already at job or idempotency capacity.

When overloaded, reject at the narrowest authority that knows the reason. A stream can receive a 503 response without destroying the entire session.

## Flow control

HTTP/2 uses flow-control windows to limit how much DATA can be in flight. This is distinct from Node stream high-water marks and from application admission.

Think in three layers:

```text
application output production
        ↓
Node stream buffering
        ↓
HTTP/2 flow-control window
        ↓
transport
```

A write can encounter pressure even when application capacity is available. The response producer must respect write return values and terminal events.

Do not manually tune windows before establishing evidence. Understand defaults and measure later in Course 9.

## Request bodies

Each stream carries its own body. Enforce `maxRequestBodyBytes` per stream. Several streams can reach their limits concurrently, so the worst-case retained body budget includes concurrency:

```text
max concurrent admitted body streams × max body bytes
```

If the adapter buffers complete bodies, this product must be intentional. A future streaming endpoint may use a different contract.

On overflow, stop normal body processing and send or reset according to whether a clean HTTP response remains possible. Ensure the stream owner settles exactly once.

## Stream-local errors

Examples:

- invalid application request;
- body too large;
- client resets stream;
- response write failure;
- route not found.

Most should remain stream-local. Session-level termination is reserved for connection/protocol failures or runtime shutdown policy.

If a client resets after the server commits a job, the domain operation remains committed. This is the same ambiguous response observation seen in HTTP/1.1.

## Session errors

Session-level events include:

- transport error;
- protocol error;
- remote GOAWAY;
- local GOAWAY;
- close;
- destruction.

A session error can terminate several streams. The runtime should preserve each accepted stream's terminal outcome rather than only logging one session error.

## GOAWAY and graceful shutdown

GOAWAY tells the peer that the session is closing and communicates a last processed stream identifier under protocol semantics. It is part of graceful shutdown, not a guarantee that all streams have already completed.

A server shutdown can:

1. stop accepting new sessions;
2. mark readiness false;
3. send GOAWAY or close sessions gracefully;
4. allow active streams to finish under one grace deadline;
5. destroy remaining sessions;
6. observe every stream and session terminal event.

Do not wait forever for a peer to close a session after GOAWAY.

## h2c versus TLS-negotiated h2

HTTP/2 can operate over TLS with ALPN or in cleartext modes such as prior-knowledge h2c in controlled environments. Public browser-facing service use normally involves TLS negotiation.

ServiceWire exposes h2c only for local course tests. The HTTPS endpoint remains HTTP/1.1 in the base capstone. An independent extension can combine TLS and `h2` after Module 57's identity policy.

The documentation must not present h2c as equivalent security.

## Worked case — three multiplexed streams

One session opens:

```text
stream 1: GET /v1/jobs/job-1
stream 3: POST /v1/jobs (sleep operation)
stream 5: GET /v1/stats
```

The stats stream may complete before the sleep submission response. Stream IDs and response objects preserve association. If stream 3 is reset after job commit, streams 1 and 5 remain valid; the job remains committed and can be reconciled by idempotency key.

During shutdown, the server stops new sessions, sends GOAWAY, allows streams 1 and 5 to finish, and waits for stream 3's owner to observe reset. After grace, it destroys the session if still open.

## Adapting one application protocol

The HTTP/2 adapter should produce the same application call and receive the same result as the HTTP/1.1 adapter. This prevents:

- divergent validation;
- different error codes;
- different idempotency behavior;
- inconsistent ETags;
- events emitted by one transport but not another.

Transport-specific code owns pseudo-headers, stream body, flow control, and session lifecycle. The application owns commands and representations.

## Push and optional features

HTTP/2 includes features beyond the needs of this course. Do not add server push, complex prioritization, or custom window tuning merely because the API exists. Each feature creates compatibility and resource obligations.

Course quality comes from a narrow correct protocol, not maximum API coverage.

## Common wrong models

### “One HTTP/2 connection means one request at a time”

Streams are concurrent and independently terminating.

### “Stream reset means session failure”

It is often stream-local.

### “Multiplexing removes backpressure”

It adds protocol flow control and shared session capacity.

### “Peer settings are my application limits”

They are protocol negotiation, not complete product admission.

### “GOAWAY means all work is finished”

It begins or communicates closure; active streams still need ownership and completion.

## Decision procedure

1. Define session admission.
2. Define stream admission.
3. Normalize pseudo-headers.
4. Bound each body.
5. Bound total concurrent body retention.
6. Share one application protocol.
7. Respect stream pressure.
8. classify stream versus session failures.
9. define GOAWAY, grace, and destroy.
10. test concurrent streams and resets.

## ServiceWire increment

Add an h2c adapter for finite endpoints:

- session registry;
- stream registry;
- per-stream body limits;
- shared application dispatch;
- stable response mapping;
- concurrent stream tests;
- GOAWAY-based drain and forced destroy.

SSE remains on HTTP/1.1 for the base product.

## Deep reasoning — a session is not a large request

HTTP/2 multiplexes streams over one connection. This changes the ownership graph:

```text
TCP/TLS connection
      ↓
HTTP/2 session
      ├── stream 1: GET /health
      ├── stream 3: POST /v1/jobs
      └── stream 5: GET /v1/stats
```

Each stream has independent headers, body, flow-control state, reset code, and terminal outcome. A session-level error may terminate all streams; an application error on one stream should normally produce one response and leave the session usable.

### Completion order is not request order

Suppose stream 1 sleeps for 50 ms, stream 3 returns health immediately, and stream 5 uploads a bounded body. The client may observe completion order 3, 5, 1. Tests that assert array position by completion time are wrong unless they attach explicit stream identity. Reconcile results by a request ID or by the promise associated with each stream.

### Two levels of capacity

A service should distinguish:

- accepted sessions;
- active streams per session;
- total active streams;
- body bytes per stream;
- retained response bytes per stream.

Limiting sessions alone does not bound stream work. Limiting streams alone does not bound connection-level memory and handshake cost. ServiceWire records sessions and streams separately.

### Flow control is not the same as application admission

HTTP/2 flow control bounds how much data may be in flight at protocol windows. It does not decide whether the application has capacity to create another job. A stream can be transport-admitted and then receive an application-level 503. Conversely, a stream may be waiting on flow-control credit before the application has seen the complete body.

Keep the layers separate:

| Layer | Resource | Terminal signal |
|---|---|---|
| session | connection and protocol state | close, error, GOAWAY |
| stream | one request/response exchange | end, reset, close |
| application | job/idempotency capacity | typed response or problem |
| executor | active operation slots | job terminal transition |

### GOAWAY and graceful close

A graceful server begins quiescence by refusing new externally accepted work. For HTTP/2, sending GOAWAY indicates that the session is winding down and constrains new streams. Existing accepted streams still need a grace period. At the deadline, remaining streams are reset and sessions destroyed. Server close, GOAWAY, stream completion, and session destruction are distinct observations.

A shutdown implementation that awaits `server.close()` before closing sessions can deadlock because the server callback may wait for those sessions. Correct ownership starts the close operation, signals sessions, waits within one grace, then destroys leftovers and observes all terminal events.

### Shared application semantics

ServiceWire maps HTTP/1.1 and HTTP/2 requests into one finite request model. It does not maintain two routers or two error vocabularies. Transport-specific code owns pseudo-headers, stream reset, and session lifecycle; the application dispatcher owns route semantics, validation, idempotency, and representation construction.

This division is the core architectural test of the module: protocol evolution should not fork domain truth.

## Ready to continue

You are ready for long-lived delivery when you can explain how one session can close gracefully while several streams have different terminal states.

## Primary Node.js references

- [HTTP/2](https://nodejs.org/docs/latest-v24.x/api/http2.html)
- [TLS](https://nodejs.org/docs/latest-v24.x/api/tls.html)
- [Stream](https://nodejs.org/docs/latest-v24.x/api/stream.html)

## Continue

- [Workbook](workbook.md)
- [Reasoned solutions](solutions.md)
- [Laboratory brief](../../labs/module-58-multiplexed-http2-service/README.md)
- [ServiceWire engineering guide](../capstone.md)
