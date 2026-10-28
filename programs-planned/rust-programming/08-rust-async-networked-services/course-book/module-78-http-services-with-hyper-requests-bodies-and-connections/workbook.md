# Workbook — Module 78: HTTP Services with Hyper: Requests, Bodies, and Connections

[Return to the chapter](index.md) · [Open the solutions](solutions.md) · [Open the JobWire guide](../capstone.md)

## Part 1 — Predict

1. A Hyper request handler calls `collect()` on any incoming body without a limit. What resource can a client control?
2. `/health` sends a message through the same saturated job queue as ordinary work. What operational failure appears?
3. A route holds a broker mutex while returning a streaming body. How long can the critical section last?
4. The listener spawns each HTTP connection and drops its handle. What shutdown evidence is missing?
5. `uri.path()` returns `/items/%2Fsecret`. Has percent decoding already produced an application identifier?
6. An application validation error is returned as `Err` from the Hyper service and closes the connection. Is that necessarily the best scope?
7. A response body is produced with `format!("{state:?}")`. What compatibility problem appears?
8. A health response says `healthy=true` because the HTTP event loop responds. Does that prove the broker accepts jobs?

## Part 2 — Diagnose and repair

A single function accepts sockets, constructs Hyper connections, routes requests, locks application state, collects bodies, formats debug output, and handles shutdown. Split it into four layers and define the error boundary of each.

## Part 3 — Focused exercises

### Exercise 1 — Pure router

Implement `GET /health`, `GET /stats`, 404, and 405 as a pure request-to-response function with deterministic bodies.

### Exercise 2 — Body limit

Implement a frame-counting body collector with a 4 KiB maximum. Return 413 without retaining more than the limit plus one inspected frame.

### Exercise 3 — Health semantics

Define liveness, readiness, and degraded states. State data source, staleness, and what each does not prove.

### Exercise 4 — Connection lifecycle

Add a listener, connection semaphore, `JoinSet`, shutdown token, grace period, abort, and join.

### Exercise 5 — Slow client

Prove a slow HTTP reader does not retain a broker lock or job permit.

## Part 4 — Independent laboratory

Build [Hyper Health Surface](../../labs/module-08-hyper-health-surface/README.md). Required evidence:

- pure route tests;
- exact status and content type;
- bounded or forbidden request bodies;
- explicit health semantics;
- tracked connection tasks;
- bounded admission;
- graceful shutdown under keep-alive.

## Part 5 — Capstone transfer

Add JobWire’s `/health` and `/stats` HTTP/1 routes using Hyper. Health must distinguish `starting`, `ready`, `shutting-down`, and `failed`. Stats are advisory and deterministic. The HTTP surface may not submit jobs or share the broker’s saturated work queue.

## Part 6 — Reconstruct and defend

1. Which layer accepts TCP?
2. Which layer drives HTTP connection state?
3. Where is body size enforced?
4. What does readiness prove?
5. Why should application errors often become responses?
6. Who joins HTTP connection tasks?

### Independent transfer

Design an HTTP upload route for a 10 MiB maximum file without collecting the whole body. State streaming ownership, temporary storage, cancellation, commit, response, and shutdown behavior.
