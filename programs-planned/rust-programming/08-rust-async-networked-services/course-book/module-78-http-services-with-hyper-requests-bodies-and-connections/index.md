# Module 78 — HTTP Services with Hyper: Requests, Bodies, and Connections

**Course 8 · Day 8 · Module 78 of 100**
`████████████████████░░░░░` **78/100**

[Program](../../../README.md) · [Course 8](../index.md) · [Workbook](workbook.md) · [Laboratory](../../labs/module-08-hyper-health-surface/README.md) · [JobWire guide](../capstone.md)

[← Module 77: Cancellation Safety, Deadlines, and Graceful Shutdown](../module-77-cancellation-safety-deadlines-and-graceful-shutdown/index.md) · [Module 79: Network Failure, Idempotency, Retries, and Deterministic Testing →](../module-79-network-failure-idempotency-retries-and-deterministic-testing/index.md)

## The question

> How do you build a small HTTP service while keeping transport ownership, HTTP connection driving, request-body policy, routing, application state, and health semantics separate?

## Why this comes now

The first seven modules built the mechanics that web frameworks usually hide: futures, tasks, framing, sockets, protocol state, capacity, cancellation, and shutdown. HTTP is now introduced as another protocol boundary, not as a shortcut around those responsibilities.

Hyper is intentionally low level. It represents HTTP messages and drives connection state, but it does not choose an application router, JSON model, authentication policy, body limit, task tree, or graceful-shutdown design. That makes it appropriate for learning the boundary clearly. A high-level framework can be used later with better judgment because you will know which guarantees come from HTTP, Hyper, Tokio, and your application.

JobWire uses HTTP only for operational read surfaces: `/health` and `/stats`. Its job protocol remains on the custom framed TCP channel. This separation demonstrates a common production architecture: one protocol optimized for domain interaction, another for standard operational integration.

### Prerequisite bridge

Module 77 established **Cancellation Safety, Deadlines, and Graceful Shutdown**. Before continuing, verify that you can state which operations may finish during shutdown and which must be rejected. This module preserves that capability and adds the ability to distinguish accepted transport, http connection future, request future, body stream, and application service;. Module 79, **Network Failure, Idempotency, Retries, and Deterministic Testing**, will rely on both when it asks: *When a network operation fails without revealing whether the remote side committed it, how do idempotency, retry budgets, failure classification, and deterministic tests preserve one semantic outcome?*

### Scope boundary

This module owns the reasoning for **http services with hyper: requests, bodies, and connections** inside Course 8. The course builds a process-local network service. It does not attempt distributed consensus, TLS implementation, database transactions, service meshes, or framework-driven web development. Those concerns are discussed only where they affect the stated protocol and lifecycle guarantees. The purpose of the boundary is to keep the decisive relationship visible before later mechanisms are layered on top of it.

## What you will be able to do

- distinguish accepted transport, HTTP connection future, request future, body stream, and application service;
- serve HTTP/1 connections with Hyper over Tokio I/O;
- construct stable response body types and status codes;
- route by method and path without mixing broker logic into transport code;
- bound request bodies before retaining them;
- define health, readiness, and statistics semantics honestly;
- avoid holding locks or permits across body production and slow client writes;
- track every HTTP connection task in the service task tree;
- coordinate shutdown with listener stop and connection draining;
- test routing as pure request/response behavior separately from socket tests.

## Core model

### Four layers remain distinct

A small Hyper server has four boundaries:

```text
TcpListener / TcpStream
        ↓ adapted I/O
Hyper HTTP connection driver
        ↓ Request<Incoming>
route and body policy
        ↓ typed application call
broker/status state
        ↓ Response<Body>
```

The listener owns admission and accepted transports. Hyper’s connection future owns HTTP parsing, framing, keep-alive, and response serialization for that connection. A service function maps one request to one response. The application owns domain state and product semantics.

Do not let the route function call `accept`, know about socket permits, or own shutdown joins. Do not let the listener parse URI paths manually from bytes. Separation improves tests and makes failure scope explicit.

### Hyper needs an I/O adapter

Hyper defines runtime-neutral HTTP machinery. `hyper-util` supplies `TokioIo`, adapting a Tokio stream to Hyper’s runtime I/O traits. The connection driver is an async future that must be awaited or spawned and observed.

Conceptually:

```rust
let io = TokioIo::new(stream);
let connection = http1::Builder::new()
    .serve_connection(io, service_fn(handler));
connection.await?;
```

If the task owning `connection` is dropped, the HTTP connection is cancelled. If the listener spawns one untracked connection task per accept, Course 72’s lifecycle defect returns in web clothing.

### Request body is a stream, not an already bounded byte vector

A server request uses an incoming body type. Body frames may arrive incrementally. Calling `collect()` without a prior or enforced limit can retain attacker-controlled bytes until memory is exhausted.

For routes that should have no body, reject a nonzero declared length and still handle chunked transfer according to policy. For small bodies, aggregate through a limiter or count frames while reading. For large uploads, stream to a bounded sink rather than collecting.

A route’s body policy belongs next to the route contract:

| Route | Method | Body policy | Response maximum |
|---|---|---|---:|
| `/health` | GET | none | 1 KiB |
| `/stats` | GET | none | 8 KiB |
| `/admin/shutdown` | POST | at most 256 bytes, authenticated | 1 KiB |

JobWire implements only the two read routes.

### Stable response body types simplify the service

Hyper response bodies are generic. A small service can use `http_body_util::Full<bytes::Bytes>` for complete in-memory responses. Every route then returns the same concrete body type:

```rust
Response<Full<Bytes>>
```

This avoids boxing for a tiny fixed response surface. Streaming responses would use another body type or a boxed body abstraction, but that complexity should follow a real requirement.

Set status, headers, and body deliberately. Do not serialize `Debug` output as an API. Use stable content types and deterministic field order.

### Routing is a total function over method and path

A minimal router can match:

```text
(GET, /health) → health
(GET, /stats)  → stats
known path, wrong method → 405 Method Not Allowed
unknown path → 404 Not Found
```

A `405` response should advertise allowed methods when practical. Query strings and percent decoding have their own contracts; avoid pretending `uri.path()` includes decoded application parameters.

Keep routing pure enough to test with constructed requests. The socket integration test then proves connection wiring, not every branch of application behavior.

### Health has levels

“Healthy” is ambiguous. Separate at least:

- **liveness:** the process and HTTP task can respond;
- **readiness:** the service currently accepts new domain work;
- **dependency state:** required downstream systems are usable;
- **degraded state:** service responds but capacity or optional components are impaired.

JobWire’s `/health` returns a deterministic state derived from supervisor and broker snapshots:

```text
starting
ready
shutting-down
failed
```

It does not claim that every future job will succeed. `/stats` reports advisory counts. Counts can change immediately after observation and should not be used as transactional authority.

### Health must not wait behind saturated work

If `/health` sends a request through the same full broker queue as ordinary jobs, overload can make the service appear dead precisely when operators need status. Options include:

- an atomic or watch-based snapshot;
- a separate bounded control channel;
- direct read-only state designed for concurrent observation;
- a short status deadline with explicit unknown result.

The snapshot may be slightly stale. That is preferable to an unbounded or blocked health path when its semantics are documented.

### Do not hold application resources through network writes

The route handler should obtain or construct the response body, release broker locks or permits, then return the response. Hyper owns writing it to the client. A slow HTTP reader should consume only connection and output-buffer capacity, not job execution capacity or an application mutex.

Large streaming responses need a more detailed ownership model because the body producer remains active while the network drains. JobWire avoids that complexity with small bounded operational responses.

### HTTP errors are responses until the connection is broken

Application route failures should usually become HTTP responses:

- 400 for malformed input;
- 404 for unknown resource;
- 405 for method mismatch;
- 413 for body too large;
- 429 or 503 for overload, according to policy;
- 500 for controlled internal failure.

Connection parse errors, I/O failures, and protocol violations belong to Hyper’s connection result and may close the connection. Keep application errors out of the connection-error log severity unless the connection itself failed.

### Shutdown owns listener and connection tasks

A graceful HTTP shutdown sequence is:

1. stop the HTTP accept loop;
2. stop creating new connection tasks;
3. signal active connections or enable graceful shutdown on their connection drivers where supported;
4. allow in-flight requests a bounded grace;
5. abort and join leftovers;
6. release admission permits.

HTTP keep-alive means a connection can remain idle after one request. Service shutdown cannot wait for clients to close voluntarily.

### HTTP/1 and HTTP/2 differ

This course capstone uses HTTP/1 to keep the connection lifecycle visible. HTTP/2 introduces multiplexed streams, stream-level flow control, and different head-of-line behavior. The architectural ledgers still apply, but capacities need stream-level dimensions. Do not generalize an HTTP/1 one-request-at-a-time assumption to HTTP/2.

### Model checkpoint

Before the complete-program example, verify that the model can decide a design rather than merely name its mechanism.

1. **Outcome 1.** For distinguish accepted transport, HTTP connection future, request future, body stream, and application service, construct one positive and one causal negative example. Mark the first decisive fact in the **HTTP boundary map** and state which evidence could falsify the claim.

2. **Outcome 2.** For serve HTTP/1 connections with Hyper over Tokio I/O, construct one positive and one causal negative example. Mark the first decisive fact in the **HTTP boundary map** and state which evidence could falsify the claim.

3. **Outcome 3.** For construct stable response body types and status codes, construct one positive and one causal negative example. Mark the first decisive fact in the **HTTP boundary map** and state which evidence could falsify the claim.

4. **Outcome 4.** For route by method and path without mixing broker logic into transport code, construct one positive and one causal negative example. Mark the first decisive fact in the **HTTP boundary map** and state which evidence could falsify the claim.

5. **Preservation.** Name one earlier invariant that an easier but less precise implementation could regress.

6. **Boundary.** State one claim this module can justify and one adjacent claim that requires a later course, platform contract, peer behavior, or measurement.

A strong answer records state before and after the operation, the failure path, and the public consequence. An API name by itself is not a model.

## Use the idea in a complete program

A pure router plus one connection driver keeps boundaries visible:

```rust
use bytes::Bytes;
use http_body_util::Full;
use hyper::{
    body::Incoming,
    server::conn::http1,
    service::service_fn,
    Method, Request, Response, StatusCode,
};
use hyper_util::rt::TokioIo;
use std::{convert::Infallible, sync::Arc};
use tokio::net::TcpStream;

#[derive(Debug)]
pub struct StatusSnapshot {
    pub ready: bool,
    pub active_jobs: usize,
    pub queued_jobs: usize,
}

type Body = Full<Bytes>;

fn text(status: StatusCode, body: String) -> Response<Body> {
    Response::builder()
        .status(status)
        .header("content-type", "text/plain; charset=utf-8")
        .body(Full::new(Bytes::from(body)))
        .expect("static response construction")
}

pub async fn route(
    request: Request<Incoming>,
    snapshot: Arc<StatusSnapshot>,
) -> Result<Response<Body>, Infallible> {
    let response = match (request.method(), request.uri().path()) {
        (&Method::GET, "/health") => {
            let state = if snapshot.ready { "ready" } else { "not-ready" };
            text(StatusCode::OK, format!("state={state}\n"))
        }
        (&Method::GET, "/stats") => text(
            StatusCode::OK,
            format!(
                "active_jobs={}\nqueued_jobs={}\n",
                snapshot.active_jobs, snapshot.queued_jobs
            ),
        ),
        (_, "/health" | "/stats") => text(
            StatusCode::METHOD_NOT_ALLOWED,
            "method not allowed\n".to_owned(),
        ),
        _ => text(StatusCode::NOT_FOUND, "not found\n".to_owned()),
    };
    Ok(response)
}

pub async fn serve_connection(
    stream: TcpStream,
    snapshot: Arc<StatusSnapshot>,
) -> Result<(), hyper::Error> {
    let io = TokioIo::new(stream);
    http1::Builder::new()
        .serve_connection(io, service_fn(move |request| {
            route(request, Arc::clone(&snapshot))
        }))
        .await
}
```

The `expect` covers a response built from static valid header data; a production style may avoid it. The snapshot here is immutable for brevity. JobWire uses a live read model. The route ignores request bodies because GET routes require none; the complete service enforces that policy explicitly.

## Practice sequence

1. Draw transport, connection, route, and application layers.
2. Build pure route tests for status and body.
3. Add body policy and maximums.
4. Define liveness versus readiness semantics.
5. Ensure health does not wait behind the job queue.
6. Track HTTP connection tasks in the service tree.
7. Add graceful shutdown and keep-alive tests.
8. Transfer `/health` and `/stats` into JobWire.

## Ready to continue

Continue only when you can explain:

- what Hyper owns and what Tokio owns;
- why request body size is not automatically bounded;
- why routes should return controlled response types;
- what health actually proves;
- why a slow HTTP client must not retain broker capacity;
- who owns every connection future;
- how HTTP shutdown joins keep-alive connections.

## Primary Rust references

- Hyper `server::conn`, `service_fn`, request, response, and body documentation;
- `hyper-util::rt::TokioIo` documentation;
- `http-body-util` body adapters;
- Tokio listener, task, and shutdown contracts from prior modules.

## Continue

Continue to [Module 79 — Network Failure, Idempotency, Retries, and Deterministic Testing](../module-79-network-failure-idempotency-retries-and-deterministic-testing/index.md) after completing the workbook, independent laboratory, capstone increment, and closed-book explanation for this module.
